use actix_files::Files;
use actix_session::{storage::CookieSessionStore, Session, SessionMiddleware};
use actix_web::{
    cookie::SameSite,
    http::header::{CACHE_CONTROL, EXPIRES, PRAGMA, STRICT_TRANSPORT_SECURITY},
    middleware::{DefaultHeaders, Logger},
    web, App, HttpRequest, HttpResponse, HttpResponseBuilder, HttpServer,
};
use chrono::prelude::*;
use log::{error, info, warn};
use nanoid::nanoid;
use once_cell::sync::Lazy;
use rusqlite::{params, Connection, Result};
use serde::{Deserialize, Serialize};
use std::sync::Mutex;
use std::{env, fs};

const AUTH_TEMPLATE: &str = "templates/auth.html";
const RESUME_TEMPLATE: &str = "templates/resume.html";

// 根据编译模式决定模板加载方式：
// - debug 模式：磁盘加载（支持热更新，方便开发）
// - release 模式：内存加载（性能优化，适合生产）
fn template_load_mode() -> &'static str {
    if cfg!(debug_assertions) {
        "disk"
    } else {
        "memory"
    }
}

// 内存缓存模式：启动时加载模板到内存
static AUTH_TEMPLATE_CACHED: Lazy<String> = Lazy::new(|| {
    fs::read_to_string(AUTH_TEMPLATE).unwrap_or_else(|err| {
        eprintln!("错误：无法读取登录模板 {}: {}", AUTH_TEMPLATE, err);
        String::from("<!DOCTYPE html><html><body><h1>服务器错误：无法加载登录页面</h1></body></html>")
    })
});

static RESUME_TEMPLATE_CACHED: Lazy<String> = Lazy::new(|| {
    fs::read_to_string(RESUME_TEMPLATE).unwrap_or_else(|err| {
        eprintln!("错误：无法读取简历模板 {}: {}", RESUME_TEMPLATE, err);
        String::from("<!DOCTYPE html><html><body><h1>服务器错误：无法加载简历页面</h1></body></html>")
    })
});

struct AppState {
    db: Mutex<Connection>,
}

#[derive(Deserialize)]
struct InviteCode {
    code: String,
}

#[derive(Serialize)]
struct AuthResponse {
    success: bool,
    message: String,
}

#[actix_web::main]
async fn main() -> std::io::Result<()> {
    env_logger::init();

    // 根据编译模式决定模板加载方式
    let load_mode = template_load_mode();
    info!("模板加载模式: {} (编译模式: {})", 
          load_mode,
          if cfg!(debug_assertions) { "debug" } else { "release" });
    
    // 如果是内存模式，预加载模板（触发 Lazy 初始化）
    if load_mode == "memory" {
        info!("预加载模板到内存...");
        let _ = AUTH_TEMPLATE_CACHED.as_str();
        let _ = RESUME_TEMPLATE_CACHED.as_str();
        info!("模板已加载到内存");
    }

    let db_conn = init_db().expect("Failed to initialize database");
    let app_state = web::Data::new(AppState {
        db: Mutex::new(db_conn),
    });

    let secret_key = actix_web::cookie::Key::generate();

    let use_secure_cookie = env::var("SECURE_RESUME_SECURE_COOKIE")
        .map(|val| val == "1" || val.eq_ignore_ascii_case("true"))
        .unwrap_or(!cfg!(debug_assertions));

    info!("安全简历系统启动在 http://127.0.0.1:8080");

    HttpServer::new(move || {
        App::new()
            .app_data(app_state.clone())
            .wrap(
                DefaultHeaders::new()
                    .add((
                        STRICT_TRANSPORT_SECURITY,
                        "max-age=31536000; includeSubDomains",
                    ))
                    .add(("X-Frame-Options", "DENY"))
                    .add(("X-Content-Type-Options", "nosniff"))
                    .add(("Referrer-Policy", "strict-origin-when-cross-origin")),
            )
            .wrap(Logger::default())
            .wrap(
                SessionMiddleware::builder(CookieSessionStore::default(), secret_key.clone())
                    .cookie_secure(use_secure_cookie)
                    .cookie_same_site(SameSite::Strict)
                    .cookie_name("secure_resume_session".into())
                    .build(),
            )
            .route("/", web::get().to(index))
            .route("/api/auth", web::post().to(verify_invite_code))
            .route("/api/logout", web::post().to(logout))
            .route("/api/generate", web::post().to(generate_invite_codes))
            .route("/api/stats", web::get().to(get_stats))
            .service(
                Files::new("/static", "./static")
                    .prefer_utf8(true)
                    .use_last_modified(true),
            )
    })
    .bind("127.0.0.1:8080")?
    .run()
    .await
}

fn init_db() -> Result<Connection> {
    let conn = Connection::open("invites.db")?;

    conn.execute(
        "CREATE TABLE IF NOT EXISTS invites (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            code TEXT UNIQUE NOT NULL,
            used BOOLEAN DEFAULT FALSE,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            used_at DATETIME,
            visitor_ip TEXT
        )",
        [],
    )?;

    Ok(conn)
}

async fn index(session: Session) -> HttpResponse {
    let load_mode = template_load_mode();
    
    // 检查是否已登录
    let is_authenticated = session
        .get::<bool>("authenticated")
        .unwrap_or(None)
        .unwrap_or(false);
    
    if is_authenticated {
        // 已登录：返回简历页面
        let html = if load_mode == "memory" {
            // release 模式：使用内存缓存的模板
            RESUME_TEMPLATE_CACHED.as_str()
        } else {
            // debug 模式：每次从磁盘读取（支持热更新）
            match fs::read_to_string(RESUME_TEMPLATE) {
                Ok(content) => {
                    return no_store_response(HttpResponse::Ok())
                        .content_type("text/html; charset=utf-8")
                        .body(content);
                }
                Err(err) => {
                    error!("读取简历模板失败: {}", err);
                    return HttpResponse::InternalServerError()
                        .content_type("text/plain; charset=utf-8")
                        .body("服务器暂时无法加载简历内容，请稍后重试");
                }
            }
        };
        
        return no_store_response(HttpResponse::Ok())
            .content_type("text/html; charset=utf-8")
            .body(html);
    }

    // 未登录：返回登录页面
    let html = if load_mode == "memory" {
        // release 模式：使用内存缓存的模板
        AUTH_TEMPLATE_CACHED.as_str()
    } else {
        // debug 模式：每次从磁盘读取（支持热更新）
        match fs::read_to_string(AUTH_TEMPLATE) {
            Ok(content) => {
                return no_store_response(HttpResponse::Ok())
                    .content_type("text/html; charset=utf-8")
                    .body(content);
            }
            Err(err) => {
                error!("读取登录模板失败: {}", err);
                return HttpResponse::InternalServerError()
                    .content_type("text/plain; charset=utf-8")
                    .body("服务器暂时无法加载登录页面，请稍后重试");
            }
        }
    };
    
    no_store_response(HttpResponse::Ok())
        .content_type("text/html; charset=utf-8")
        .body(html)
}

async fn verify_invite_code(
    form: web::Json<InviteCode>,
    state: web::Data<AppState>,
    session: Session,
    req: HttpRequest,
) -> HttpResponse {
    let db = state.db.lock().unwrap();
    let client_ip = req
        .connection_info()
        .realip_remote_addr()
        .unwrap_or("unknown")
        .to_string();

    info!("收到邀请码校验请求，code={} ip={}", form.code, client_ip);

    match db.query_row(
        "SELECT code, used FROM invites WHERE code = ?1",
        [&form.code],
        |row| Ok((row.get::<_, String>(0)?, row.get::<_, bool>(1)?)),
    ) {
        Ok((code, used)) => {
            if used {
                warn!("邀请码已被使用，拒绝访问，code={} ip={}", code, client_ip);
                HttpResponse::BadRequest().json(AuthResponse {
                    success: false,
                    message: "邀请码已被使用".to_string(),
                })
            } else {
                let now = Utc::now().naive_utc();
                match db.execute(
                    "UPDATE invites SET used = TRUE, used_at = ?1, visitor_ip = ?2 WHERE code = ?3",
                    params![now, client_ip, code],
                ) {
                    Ok(_) => {
                        info!(
                            "邀请码验证成功，标记为已用，code={} ip={} at={}",
                            code, client_ip, now
                        );
                        session.insert("authenticated", true).unwrap();
                        session.insert("invite_code", &code).unwrap();

                        HttpResponse::Ok().json(AuthResponse {
                            success: true,
                            message: "验证成功".to_string(),
                        })
                    }
                    Err(e) => {
                        error!(
                            "更新邀请码状态失败，code={} ip={} err={}",
                            code, client_ip, e
                        );
                        HttpResponse::InternalServerError().json(AuthResponse {
                            success: false,
                            message: "服务器错误".to_string(),
                        })
                    }
                }
            }
        }
        Err(_) => {
            warn!("无效的邀请码尝试，code={} ip={}", form.code, client_ip);
            HttpResponse::NotFound().json(AuthResponse {
                success: false,
                message: "无效的邀请码".to_string(),
            })
        }
    }
}

async fn logout(session: Session) -> HttpResponse {
    info!("收到注销请求");
    session.purge();
    no_store_response(HttpResponse::Ok()).json(serde_json::json!({
        "success": true,
        "message": "已退出"
    }))
}

async fn generate_invite_codes(state: web::Data<AppState>) -> HttpResponse {
    let db = state.db.lock().unwrap();
    let mut codes = Vec::new();

    for _ in 0..5 {
        let code = nanoid!(32);
        if db
            .execute("INSERT OR IGNORE INTO invites (code) VALUES (?1)", [&code])
            .is_ok()
        {
            codes.push(code);
        }
    }

    if codes.is_empty() {
        warn!("邀请码生成请求未插入任何新邀请码（可能是重复）");
    } else {
        info!("成功生成 {} 个邀请码: {}", codes.len(), codes.join(", "));
    }

    HttpResponse::Ok().json(serde_json::json!({
        "success": true,
        "codes": codes,
        "message": format!("成功生成 {} 个邀请码", codes.len())
    }))
}

async fn get_stats(state: web::Data<AppState>) -> HttpResponse {
    let db = state.db.lock().unwrap();

    let total: i64 = db
        .query_row("SELECT COUNT(*) FROM invites", [], |row| row.get(0))
        .unwrap_or(0);
    let used: i64 = db
        .query_row(
            "SELECT COUNT(*) FROM invites WHERE used = TRUE",
            [],
            |row| row.get(0),
        )
        .unwrap_or(0);

    HttpResponse::Ok().json(serde_json::json!({
        "total": total,
        "used": used,
        "available": total - used
    }))
}

fn no_store_response(mut builder: HttpResponseBuilder) -> HttpResponseBuilder {
    builder.insert_header((CACHE_CONTROL, "no-store, no-cache, must-revalidate"));
    builder.insert_header((PRAGMA, "no-cache"));
    builder.insert_header((EXPIRES, "0"));
    builder
}
