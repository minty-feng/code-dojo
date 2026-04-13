from pydantic import BaseModel
from datetime import datetime
from typing import Optional

# 游戏开始请求
class GameStartRequest(BaseModel):
    player_id: str
    ip_address: Optional[str] = None
    user_agent: Optional[str] = None
    device_info: Optional[dict] = None  # 📱 设备信息字典
    device_type: Optional[str] = None
    browser: Optional[str] = None
    os: Optional[str] = None
    screen_resolution: Optional[str] = None
    language: Optional[str] = None
    timezone: Optional[str] = None
    country: Optional[str] = None
    city: Optional[str] = None

# 游戏结束请求
class GameEndRequest(BaseModel):
    player_id: str
    final_hope: int
    final_papers: int
    graduation_status: str
    is_winner: bool
    slack_off_count: int
    total_actions: int = 0
    read_paper_actions: int = 0
    work_actions: int = 0
    slack_off_actions: int = 0
    conference_actions: int = 0

# 游戏记录响应
class PlayerGameResponse(BaseModel):
    id: int
    player_id: str
    start_time: datetime
    end_time: Optional[datetime]
    game_duration: Optional[float]
    final_hope: Optional[int]
    final_papers: Optional[int]
    graduation_status: Optional[str]
    is_winner: bool
    slack_off_count: int
    
    # 设备和网络信息
    ip_address: Optional[str]
    user_agent: Optional[str]
    device_info: Optional[dict]  # 📱 设备信息字典
    device_type: Optional[str]
    browser: Optional[str]
    os: Optional[str]
    screen_resolution: Optional[str]
    language: Optional[str]
    timezone: Optional[str]
    country: Optional[str]
    city: Optional[str]
    
    # 游戏行为统计
    total_actions: int
    read_paper_actions: int
    work_actions: int
    slack_off_actions: int
    conference_actions: int
    
    created_at: datetime

    class Config:
        from_attributes = True

# 统计信息响应
class GameStatsResponse(BaseModel):
    total_players: int
    total_games: int
    winners_count: int
    dropout_count: int
    average_hope: float
    average_papers: float
    average_duration: float
    slack_off_masters: int  # 划水大师数量

# 玩家列表项响应
class PlayerListItem(BaseModel):
    player_id: str
    start_time: datetime
    end_time: Optional[datetime]
    graduation_status: Optional[str]
    is_winner: bool
    created_at: datetime

    class Config:
        from_attributes = True

# 分页玩家列表响应
class PlayerListResponse(BaseModel):
    players: list[PlayerListItem]
    total_count: int
    page: int
    size: int
    total_pages: int
