# 🎮 PhD Simulator 后端系统

## 📋 功能特性

### 🎯 核心功能
- ✅ 记录玩家游戏开始/结束
- ✅ 统计游戏时长和结果
- ✅ 记录玩家设备和网络信息
- ✅ 分析游戏行为数据
- ✅ 提供排行榜和统计信息

### 📊 记录的数据
- **基本信息**: 玩家ID、游戏时长、最终状态
- **设备信息**: IP地址、浏览器、操作系统、设备类型
- **网络信息**: 地理位置、时区、语言偏好
- **行为统计**: 总操作次数、读论文次数、工作次数、划水次数

## 🚀 快速开始

### 1. 安装依赖
```bash
cd backend
pip install -r requirements.txt
```

### 2. 启动服务
```bash
# 方式1: 使用启动脚本
python run.py

# 方式2: 直接运行
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

### 3. 访问服务
- 🎮 **游戏**: http://localhost:8000
- 📖 **API文档**: http://localhost:8000/docs
- 🔍 **健康检查**: http://localhost:8000/health

## 📡 API 接口

### 游戏管理
- `POST /api/game/start` - 开始游戏
- `POST /api/game/end` - 结束游戏
- `GET /api/game/{player_id}` - 获取玩家记录

### 统计分析
- `GET /api/stats` - 获取游戏统计
- `GET /api/leaderboard` - 获取排行榜

## 🗄️ 数据库

### 数据表结构
```sql
player_games
├── id (主键)
├── player_id (玩家ID)
├── start_time (开始时间)
├── end_time (结束时间)
├── game_duration (游戏时长)
├── final_hope (最终希望值)
├── final_papers (最终论文数)
├── graduation_status (毕业状态)
├── is_winner (是否获胜)
├── slack_off_count (划水次数)
├── ip_address (IP地址)
├── user_agent (用户代理)
├── device_type (设备类型)
├── browser (浏览器)
├── os (操作系统)
├── screen_resolution (屏幕分辨率)
├── language (语言)
├── timezone (时区)
├── country (国家)
├── city (城市)
├── total_actions (总操作数)
├── read_paper_actions (读论文次数)
├── work_actions (工作次数)
├── slack_off_actions (划水次数)
├── conference_actions (会议次数)
└── created_at (创建时间)
```

## 🔧 配置说明

### 环境变量
```bash
# 数据库配置
DATABASE_URL=sqlite:///./phd_game.db

# 服务配置
HOST=0.0.0.0
PORT=8000
```

### 生产环境部署
```bash
# 1. 安装依赖
pip install -r requirements.txt

# 2. 使用 gunicorn 启动
gunicorn main:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000

# 3. 配置 Nginx 反向代理
```

## 📈 数据统计示例

### 游戏统计
```json
{
  "total_players": 150,
  "total_games": 300,
  "winners_count": 45,
  "dropout_count": 80,
  "average_hope": 65.5,
  "average_papers": 2.8,
  "average_duration": 25.3,
  "slack_off_masters": 12
}
```

### 排行榜
```json
{
  "top_hope": [
    {"player_id": "player_001", "final_hope": 95, "graduation_status": "毕业"}
  ],
  "top_papers": [
    {"player_id": "player_002", "final_papers": 5, "graduation_status": "毕业"}
  ],
  "slack_off_masters": [
    {"player_id": "player_003", "slack_off_count": 15, "graduation_status": "划水毕业"}
  ]
}
```

## 🚨 注意事项

### 安全考虑
- 生产环境应限制 CORS 域名
- 考虑添加 API 认证
- 保护用户隐私信息

### 性能优化
- 数据库索引优化
- API 响应缓存
- 数据分页处理

## 🔗 前端集成

### 游戏开始时
```javascript
// 发送游戏开始请求
fetch('/api/game/start', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    player_id: generatePlayerId(),
    screen_resolution: `${screen.width}x${screen.height}`,
    language: navigator.language,
    timezone: Intl.DateTimeFormat().resolvedOptions().timeZone
  })
});
```

### 游戏结束时
```javascript
// 发送游戏结束请求
fetch('/api/game/end', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    player_id: playerId,
    final_hope: gameState.hope,
    final_papers: gameState.papers,
    graduation_status: gameState.status,
    is_winner: gameState.isWinner,
    slack_off_count: gameState.slackOffCount,
    total_actions: gameState.totalActions,
    read_paper_actions: gameState.readPaperActions,
    work_actions: gameState.workActions,
    slack_off_actions: gameState.slackOffActions,
    conference_actions: gameState.conferenceActions
  })
});
```

## 🎉 完成！

