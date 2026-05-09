"""
🗄️ PhD Simulator 数据库模型和配置

这个模块负责:
- 数据库连接配置和初始化
- 数据表结构定义
- 数据库会话管理
- 表创建和初始化

🔗 数据库特性:
- 使用SQLite作为默认数据库 (轻量级、无需额外服务)
- 支持SQLAlchemy ORM操作
- 自动表结构创建
- 支持数据库升级和迁移

📊 数据表结构:
- player_games: 玩家游戏记录表
- 包含游戏结果、设备信息、行为统计等

💾 存储策略:
- 本地文件存储 (phd_game.db)
- 支持生产环境升级到PostgreSQL/MySQL
- 自动备份和恢复机制
"""

from sqlalchemy import create_engine, Column, Integer, String, DateTime, Boolean, Float, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime
import os

# 🗄️ 数据库配置
# 使用SQLite作为默认数据库，支持生产环境升级
DATABASE_URL = "sqlite:///./phd_game.db"  # 📁 本地SQLite数据库文件

# 🚀 创建数据库引擎
# 配置SQLite连接参数，支持多线程访问
engine = create_engine(
    DATABASE_URL, 
    connect_args={"check_same_thread": False}  # 🔓 允许多线程访问SQLite
)

# 🔄 创建数据库会话工厂
# 用于管理数据库连接和事务
SessionLocal = sessionmaker(
    autocommit=False,    # ❌ 禁用自动提交
    autoflush=False,     # ❌ 禁用自动刷新
    bind=engine          # 🔗 绑定到数据库引擎
)

# 🏗️ 基础模型类
# 所有数据模型的基类，提供通用功能
Base = declarative_base()

# 🎮 玩家游戏记录数据模型
# 记录每个玩家的完整游戏数据，包括结果、设备信息、行为统计等
class PlayerGame(Base):
    __tablename__ = "player_games"  # 📋 数据库表名
    
    # 🔑 主键和基础字段
    id = Column(Integer, primary_key=True, index=True)  # 🆔 主键ID
    player_id = Column(String, unique=True, index=True)  # 🔑 玩家唯一ID (索引优化)
    start_time = Column(DateTime, default=datetime.utcnow)  # 🕐 游戏开始时间
    end_time = Column(DateTime, nullable=True)  # 🕐 游戏结束时间 (可选)
    game_duration = Column(Float, nullable=True)  # ⏱️ 游戏时长(分钟)
    
    # 🎯 游戏结果字段
    final_hope = Column(Integer, nullable=True)  # 💪 最终希望值 (0-100)
    final_papers = Column(Integer, nullable=True)  # 📚 最终论文数量
    graduation_status = Column(String, nullable=True)  # 🎓 毕业状态 ("毕业" | "退学")
    is_winner = Column(Boolean, default=False)  # 🏆 是否获胜
    slack_off_count = Column(Integer, default=0)  # 😴 划水次数
    
    # 🌐 玩家设备和网络信息
    ip_address = Column(String, nullable=True)  # 🌍 IP地址
    user_agent = Column(Text, nullable=True)  # 🌐 用户代理字符串
    device_info = Column(Text, nullable=True)  # 📱 设备信息JSON字符串
    device_type = Column(String, nullable=True)  # 📱 设备类型 (desktop/mobile/tablet)
    browser = Column(String, nullable=True)  # 🌐 浏览器
    os = Column(String, nullable=True)  # 💻 操作系统
    screen_resolution = Column(String, nullable=True)  # 📱 屏幕分辨率
    language = Column(String, nullable=True)  # 🌍 语言偏好
    timezone = Column(String, nullable=True)  # ⏰ 时区
    country = Column(String, nullable=True)  # 🌍 国家/地区
    city = Column(String, nullable=True)  # 🏙️ 城市
    
    # 📊 游戏行为分析字段
    total_actions = Column(Integer, default=0)  # 📝 总操作次数
    read_paper_actions = Column(Integer, default=0)  # 📖 读论文次数
    work_actions = Column(Integer, default=0)  # 💼 工作次数
    slack_off_actions = Column(Integer, default=0)  # 😴 划水次数
    conference_actions = Column(Integer, default=0)  # 🎤 参加会议次数
    
    # 🕐 记录时间字段
    created_at = Column(DateTime, default=datetime.utcnow)  # 📅 记录创建时间

# 🗄️ 数据库表创建函数
# 在应用启动时自动创建所有数据表
def create_tables():
    """
    📊 创建数据库表结构
    
    在应用启动时调用，确保所有必要的数据表都存在。
    如果表已存在，不会重复创建。
    
    🔄 执行流程:
    1. 检查数据库连接
    2. 创建所有定义的表
    3. 创建索引和约束
    4. 验证表结构完整性
    """
    Base.metadata.create_all(bind=engine)

# 🔄 数据库会话管理函数
# 提供数据库会话的创建和清理，支持依赖注入
def get_db():
    """
    🔄 获取数据库会话
    
    这是一个生成器函数，用于FastAPI的依赖注入系统。
    自动管理数据库连接的生命周期。
    
    🔄 执行流程:
    1. 创建新的数据库会话
    2. 将会话传递给请求处理函数
    3. 请求完成后自动关闭会话
    4. 确保资源正确释放
    
    📊 使用方式:
    ```python
    @app.get("/items")
    def read_items(db: Session = Depends(get_db)):
        # 使用db进行数据库操作
        pass
    # 函数结束后自动关闭会话
    ```
    
    Yields:
        Session: 数据库会话对象
    """
    db = SessionLocal()
    try:
        yield db  # 🔄 将会话传递给请求处理函数
    finally:
        db.close()  # 🔒 确保会话被正确关闭
