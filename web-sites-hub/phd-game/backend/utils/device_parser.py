"""
🔍 设备信息解析工具

这个模块负责:
- 解析用户代理字符串 (User-Agent)
- 识别设备类型和操作系统
- 解析屏幕分辨率信息
- 从IP地址推断地理位置
- 提取和标准化设备特征

🔗 主要功能:
- 设备类型识别 (desktop/mobile/tablet)
- 浏览器和操作系统检测
- 屏幕分辨率标准化
- IP地理位置推断
- 设备指纹生成

📱 支持的设备类型:
- Desktop: 桌面电脑
- Mobile: 移动设备
- Tablet: 平板设备
- Unknown: 未知设备

🌍 地理位置支持:
- 本地网络识别
- 常见IP段映射
- 可扩展第三方服务集成
"""

import re
from typing import Dict, Optional
from user_agents import parse

def parse_user_agent(user_agent_string: str) -> Dict[str, str]:
    """
    🌐 解析用户代理字符串
    
    使用user-agents库解析浏览器发送的User-Agent字符串，
    提取浏览器、操作系统和设备类型信息。
    
    📊 解析内容:
    - 浏览器名称和版本
    - 操作系统名称和版本
    - 设备类型 (desktop/mobile/tablet)
    
    🔄 解析流程:
    1. 使用user-agents库解析字符串
    2. 提取浏览器信息
    3. 提取操作系统信息
    4. 判断设备类型
    5. 返回标准化结果
    
    ⚠️ 错误处理:
    - 解析失败时返回默认值
    - 确保API不会因解析错误而崩溃
    
    Args:
        user_agent_string (str): 用户代理字符串
        
    Returns:
        Dict[str, str]: 包含浏览器、操作系统、设备类型的字典
        
    📝 示例:
    >>> parse_user_agent("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36")
    {
        "browser": "Chrome 120.0.0.0",
        "os": "Windows 10",
        "device_type": "desktop"
    }
    """
    try:
        # 🔍 使用user-agents库解析用户代理
        ua = parse(user_agent_string)
        
        # 📊 提取设备信息
        return {
            "browser": f"{ua.browser.family} {ua.browser.version_string}",  # 🌐 浏览器信息
            "os": f"{ua.os.family} {ua.os.version_string}",                 # 💻 操作系统信息
            "device_type": _get_device_type(ua),                            # 📱 设备类型
        }
    except:
        # ❌ 解析失败时返回默认值
        return {
            "browser": "Unknown",      # 🌐 未知浏览器
            "os": "Unknown",            # 💻 未知操作系统
            "device_type": "Unknown"    # 📱 未知设备类型
        }

def _get_device_type(ua) -> str:
    """
    📱 判断设备类型
    
    根据用户代理信息判断设备的具体类型。
    支持桌面、移动设备、平板等分类。
    
    🔍 判断逻辑:
    1. 优先检查是否为移动设备
    2. 其次检查是否为平板设备
    3. 最后检查是否为桌面设备
    4. 都不匹配时返回未知
    
    📊 设备类型:
    - mobile: 移动设备 (手机)
    - tablet: 平板设备
    - desktop: 桌面设备 (电脑)
    - unknown: 未知设备
    
    Args:
        ua: user-agents解析后的用户代理对象
        
    Returns:
        str: 设备类型字符串
    """
    if ua.is_mobile:
        return "mobile"      # 📱 移动设备
    elif ua.is_tablet:
        return "tablet"      # 📱 平板设备
    elif ua.is_pc:
        return "desktop"     # 💻 桌面设备
    else:
        return "unknown"     # ❓ 未知设备

def parse_screen_resolution(resolution_string: str) -> str:
    """
    📱 解析屏幕分辨率
    
    将各种格式的屏幕分辨率字符串标准化为统一格式。
    支持多种输入格式，确保数据一致性。
    
    📊 支持的输入格式:
    - "1920x1080" (标准格式)
    - "1920 x 1080" (带空格)
    - "1920X1080" (大写X)
    - 其他格式返回原值
    
    🔄 解析流程:
    1. 使用正则表达式匹配分辨率格式
    2. 提取宽度和高度数值
    3. 标准化为 "宽x高" 格式
    4. 处理异常情况
    
    Args:
        resolution_string (str): 原始分辨率字符串
        
    Returns:
        str: 标准化的分辨率字符串
        
    📝 示例:
    >>> parse_screen_resolution("1920 x 1080")
    "1920x1080"
    """
    if not resolution_string:
        return "Unknown"  # 🔴 空值返回未知
    
    # 🔍 使用正则表达式匹配分辨率格式
    # 支持: "1920x1080", "1920 x 1080", "1920X1080" 等
    match = re.search(r'(\d+)\s*[xX]\s*(\d+)', resolution_string)
    if match:
        width, height = match.groups()  # 📐 提取宽度和高度
        return f"{width}x{height}"      # 🔄 标准化格式
    
    # 🔴 格式不匹配时返回原值
    return resolution_string

def get_location_from_ip(ip_address: str) -> Dict[str, str]:
    """
    🌍 从IP地址获取地理位置信息
    
    根据IP地址推断地理位置信息，包括国家和城市。
    支持本地网络和常见IP段识别。
    
    📊 支持的地理位置:
    - 本地网络 (192.168.x.x, 10.x.x.x, 172.x.x.x)
    - 常见公共IP段 (Google DNS, 114 DNS等)
    - 其他IP返回未知位置
    
    🔄 识别逻辑:
    1. 检查是否为本地网络IP
    2. 检查是否为已知的公共IP段
    3. 返回对应的地理位置信息
    4. 未知IP返回默认值
    
    💡 扩展建议:
    - 集成第三方地理位置服务
    - 添加IP地址数据库
    - 支持更精确的地理位置信息
    
    Args:
        ip_address (str): IP地址字符串
        
    Returns:
        Dict[str, str]: 包含国家和城市信息的字典
        
    📝 示例:
    >>> get_location_from_ip("8.8.8.8")
    {"country": "United States", "city": "Mountain View"}
    """
    # 🏠 本地网络IP识别
    if ip_address.startswith("192.168.") or ip_address.startswith("10.") or ip_address.startswith("172."):
        return {
            "country": "Local Network",  # 🏠 本地网络
            "city": "Local Network"      # 🏠 本地网络
        }
    
    # 🌍 常见公共IP段识别
    # Google DNS (8.8.8.8)
    if ip_address.startswith("8.8."):
        return {"country": "United States", "city": "Mountain View"}
    # 114 DNS (114.114.114.114)
    elif ip_address.startswith("114.114."):
        return {"country": "China", "city": "Nanjing"}
    
    # ❓ 未知IP返回默认值
    return {
        "country": "Unknown",  # ❓ 未知国家
        "city": "Unknown"      # ❓ 未知城市
    }

def extract_device_info(request_data: Dict) -> Dict[str, str]:
    """
    🔍 提取设备信息
    
    从请求数据中提取和解析各种设备信息，
    包括浏览器、操作系统、屏幕分辨率、地理位置等。
    
    📊 提取的信息类型:
    - 设备特征 (浏览器、操作系统、设备类型)
    - 显示信息 (屏幕分辨率)
    - 用户偏好 (语言、时区)
    - 地理位置 (国家、城市)
    
    🔄 处理流程:
    1. 解析用户代理字符串
    2. 标准化屏幕分辨率
    3. 提取语言和时区信息
    4. 推断IP地理位置
    5. 整合所有设备信息
    
    📱 返回信息:
    - browser: 浏览器信息
    - os: 操作系统信息
    - device_type: 设备类型
    - screen_resolution: 屏幕分辨率
    - language: 语言偏好
    - timezone: 时区设置
    - country: 国家信息
    - city: 城市信息
    
    Args:
        request_data (Dict): 包含设备信息的请求数据字典
        
    Returns:
        Dict[str, str]: 整合后的设备信息字典
        
    📝 示例:
    >>> extract_device_info({
    ...     "user_agent": "Mozilla/5.0...",
    ...     "screen_resolution": "1920x1080",
    ...     "language": "zh-CN",
    ...     "timezone": "Asia/Shanghai"
    ... })
    {
        "browser": "Chrome 120.0.0.0",
        "os": "Windows 10",
        "device_type": "desktop",
        "screen_resolution": "1920x1080",
        "language": "zh-CN",
        "timezone": "Asia/Shanghai",
        "country": "Unknown",
        "city": "Unknown"
    }
    """
    device_info = {}  # 📱 初始化设备信息字典
    
    # 🌐 解析用户代理字符串
    if request_data.get("user_agent"):
        ua_info = parse_user_agent(request_data["user_agent"])
        device_info.update(ua_info)  # 🔄 更新浏览器、操作系统、设备类型
    
    # 📱 标准化屏幕分辨率
    if request_data.get("screen_resolution"):
        device_info["screen_resolution"] = parse_screen_resolution(
            request_data["screen_resolution"]
        )
    
    # 🌍 提取语言偏好
    if request_data.get("language"):
        device_info["language"] = request_data["language"]
    
    # ⏰ 提取时区信息
    if request_data.get("timezone"):
        device_info["timezone"] = request_data["timezone"]
    
    # 🌍 推断IP地理位置
    if request_data.get("ip_address"):
        location_info = get_location_from_ip(request_data["ip_address"])
        device_info.update(location_info)  # 🔄 更新国家和城市信息
    
    return device_info  # 📤 返回完整的设备信息
