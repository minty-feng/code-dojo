from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session
from sqlalchemy import func
from datetime import datetime
import uuid

from models.database import get_db, PlayerGame
from models.schemas import (
    GameStartRequest, 
    GameEndRequest, 
    PlayerGameResponse, 
    GameStatsResponse,
    PlayerListResponse,
    PlayerListItem
)
from utils.device_parser import extract_device_info

router = APIRouter()

@router.post("/game/start", response_model=PlayerGameResponse)
def start_game(request: GameStartRequest, http_request: Request, db: Session = Depends(get_db)):
    """开始新游戏"""
    # 检查玩家是否已有未完成的游戏
    existing_game = db.query(PlayerGame).filter(
        PlayerGame.player_id == request.player_id,
        PlayerGame.end_time.is_(None)
    ).first()
    
    if existing_game:
        # 如果已有未完成游戏，返回现有记录
        return existing_game
    
    # 获取客户端IP地址
    client_ip = http_request.client.host
    if http_request.headers.get("x-forwarded-for"):
        client_ip = http_request.headers["x-forwarded-for"].split(",")[0]
    
    # 提取设备信息
    device_info = extract_device_info({
        "ip_address": client_ip,
        "user_agent": request.user_agent,
        "screen_resolution": request.screen_resolution,
        "language": request.language,
        "timezone": request.timezone
    })
    
    # 创建新游戏记录
    game = PlayerGame(
        player_id=request.player_id,
        start_time=datetime.utcnow(),
        ip_address=client_ip,
        user_agent=request.user_agent,
        device_info=request.device_info,  # 📱 存储完整的设备信息
        device_type=device_info.get("device_type"),
        browser=device_info.get("browser"),
        os=device_info.get("os"),
        screen_resolution=device_info.get("screen_resolution"),
        language=device_info.get("language"),
        timezone=device_info.get("timezone"),
        country=device_info.get("country"),
        city=device_info.get("city")
    )
    
    db.add(game)
    db.commit()
    db.refresh(game)
    
    return game

@router.post("/game/end", response_model=PlayerGameResponse)
def end_game(request: GameEndRequest, db: Session = Depends(get_db)):
    """结束游戏"""
    # 查找玩家的游戏记录
    game = db.query(PlayerGame).filter(
        PlayerGame.player_id == request.player_id,
        PlayerGame.end_time.is_(None)
    ).first()
    
    if not game:
        raise HTTPException(status_code=404, detail="未找到进行中的游戏")
    
    # 计算游戏时长
    end_time = datetime.utcnow()
    duration = (end_time - game.start_time).total_seconds() / 60  # 转换为分钟
    
    # 更新游戏记录
    game.end_time = end_time
    game.game_duration = duration
    game.final_hope = request.final_hope
    game.final_papers = request.final_papers
    game.graduation_status = request.graduation_status
    game.is_winner = request.is_winner
    game.slack_off_count = request.slack_off_count
    
    # 更新游戏行为统计
    game.total_actions = request.total_actions
    game.read_paper_actions = request.read_paper_actions
    game.work_actions = request.work_actions
    game.slack_off_actions = request.slack_off_actions
    game.conference_actions = request.conference_actions
    
    db.commit()
    db.refresh(game)
    
    return game

@router.get("/game/{player_id}", response_model=PlayerGameResponse)
def get_player_game(player_id: str, db: Session = Depends(get_db)):
    """获取玩家游戏记录"""
    game = db.query(PlayerGame).filter(PlayerGame.player_id == player_id).first()
    
    if not game:
        raise HTTPException(status_code=404, detail="未找到玩家游戏记录")
    
    return game

@router.get("/stats", response_model=GameStatsResponse)
def get_game_stats(db: Session = Depends(get_db)):
    """获取游戏统计信息"""
    # 总玩家数
    total_players = db.query(func.count(func.distinct(PlayerGame.player_id))).scalar()
    
    # 总游戏数
    total_games = db.query(func.count(PlayerGame.id)).scalar()
    
    # 获胜者数量
    winners_count = db.query(func.count(PlayerGame.id)).filter(PlayerGame.is_winner == True).scalar()
    
    # 退学数量
    dropout_count = db.query(func.count(PlayerGame.id)).filter(
        PlayerGame.graduation_status == "退学"
    ).scalar()
    
    # 平均希望值
    avg_hope = db.query(func.avg(PlayerGame.final_hope)).filter(
        PlayerGame.final_hope.isnot(None)
    ).scalar() or 0
    
    # 平均论文数
    avg_papers = db.query(func.avg(PlayerGame.final_papers)).filter(
        PlayerGame.final_papers.isnot(None)
    ).scalar() or 0
    
    # 平均游戏时长
    avg_duration = db.query(func.avg(PlayerGame.game_duration)).filter(
        PlayerGame.game_duration.isnot(None)
    ).scalar() or 0
    
    # 划水大师数量（划水10次以上的）
    slack_off_masters = db.query(func.count(PlayerGame.id)).filter(
        PlayerGame.slack_off_count >= 10
    ).scalar()
    
    return GameStatsResponse(
        total_players=total_players,
        total_games=total_games,
        winners_count=winners_count,
        dropout_count=dropout_count,
        average_hope=round(avg_hope, 2),
        average_papers=round(avg_papers, 2),
        average_duration=round(avg_duration, 2),
        slack_off_masters=slack_off_masters
    )

@router.get("/leaderboard")
def get_leaderboard(db: Session = Depends(get_db)):
    """获取排行榜"""
    # 按希望值排序的前10名
    top_hope = db.query(PlayerGame).filter(
        PlayerGame.final_hope.isnot(None)
    ).order_by(PlayerGame.final_hope.desc()).limit(10).all()
    
    # 按论文数排序的前10名
    top_papers = db.query(PlayerGame).filter(
        PlayerGame.final_papers.isnot(None)
    ).order_by(PlayerGame.final_papers.desc()).limit(10).all()
    
    # 划水大师排行榜
    slack_off_masters = db.query(PlayerGame).filter(
        PlayerGame.slack_off_count >= 10
    ).order_by(PlayerGame.slack_off_count.desc()).limit(10).all()
    
    return {
        "top_hope": [
            {
                "player_id": game.player_id,
                "final_hope": game.final_hope,
                "graduation_status": game.graduation_status
            } for game in top_hope
        ],
        "top_papers": [
            {
                "player_id": game.player_id,
                "final_papers": game.final_papers,
                "graduation_status": game.graduation_status
            } for game in top_papers
        ],
        "slack_off_masters": [
            {
                "player_id": game.player_id,
                "slack_off_count": game.slack_off_count,
                "graduation_status": game.graduation_status
            } for game in slack_off_masters
        ]
    }

@router.get("/players", response_model=PlayerListResponse)
def get_players(
    page: int = 1, 
    size: int = 20, 
    db: Session = Depends(get_db)
):
    """
    分页查询所有玩家列表
    
    参数:
    - page: 页码 (从1开始)
    - size: 每页大小 (默认20，最大100)
    
    返回:
    - players: 玩家列表
    - total_count: 总玩家数
    - page: 当前页码
    - size: 每页大小
    - total_pages: 总页数
    """
    # 参数验证
    if page < 1:
        page = 1
    if size < 1:
        size = 20
    if size > 100:
        size = 100
    
    # 计算偏移量
    offset = (page - 1) * size
    
    # 查询总玩家数
    total_count = db.query(func.count(func.distinct(PlayerGame.player_id))).scalar()
    
    # 计算总页数
    total_pages = (total_count + size - 1) // size
    
    # 查询玩家列表 (按创建时间倒序)
    players = db.query(PlayerGame).order_by(
        PlayerGame.created_at.desc()
    ).offset(offset).limit(size).all()
    
    # 转换为响应格式
    player_list = []
    for player in players:
        player_list.append(PlayerListItem(
            player_id=player.player_id,
            start_time=player.start_time,
            end_time=player.end_time,
            graduation_status=player.graduation_status,
            is_winner=player.is_winner,
            created_at=player.created_at
        ))
    
    return PlayerListResponse(
        players=player_list,
        total_count=total_count,
        page=page,
        size=size,
        total_pages=total_pages
    )
