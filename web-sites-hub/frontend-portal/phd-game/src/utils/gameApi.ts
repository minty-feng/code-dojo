/**
 * 🎮 游戏API调用服务
 * 
 * 这个模块负责与后端API进行通信，记录玩家的游戏数据。
 * 包括游戏开始、结束、统计信息获取等功能。
 * 
 * 📡 主要功能:
 * - 游戏生命周期数据记录 (开始/结束)
 * - 游戏统计信息获取
 * - 排行榜数据获取
 * - 玩家个人记录查询
 * 
 * 🔗 后端API端点:
 * - POST /api/game/start - 记录游戏开始
 * - POST /api/game/end - 记录游戏结束
 * - GET /api/stats - 获取游戏统计
 * - GET /api/leaderboard - 获取排行榜
 * - GET /api/game/{player_id} - 获取玩家记录
 */

/**
 * 📊 游戏开始请求数据结构
 * 
 * 当玩家开始新游戏时，前端会发送这些数据到后端
 */
export interface GameStartData {
    player_id: string;           // 🔑 玩家唯一标识符
    user_agent?: string;         // 🌐 用户代理字符串
    screen_resolution?: string;  // 📱 屏幕分辨率 (如: "1920x1080")
    language?: string;           // 🌍 浏览器语言偏好 (如: "zh-CN")
    timezone?: string;           // ⏰ 用户时区 (如: "Asia/Shanghai")
}

/**
 * 📊 游戏结束请求数据结构
 * 
 * 当游戏结束时，前端会发送完整的游戏结果数据到后端
 * 这些数据将用于统计分析、排行榜计算等
 */
export interface GameEndData {
    player_id: string;           // 🔑 玩家唯一标识符
    final_hope: number;          // 💪 最终希望值 (0-100)
    final_papers: number;        // 📚 最终论文数量
    graduation_status: string;   // 🎓 毕业状态 ("毕业" | "退学" | "未知")
    is_winner: boolean;          // 🏆 是否获胜
    slack_off_count: number;     // 😴 划水次数
    total_actions: number;       // 📝 总操作次数
    read_paper_actions: number;  // 📖 读论文操作次数
    work_actions: number;        // 💼 工作操作次数
    slack_off_actions: number;   // 😴 划水操作次数
    conference_actions: number;  // 🎤 参加会议操作次数
}

/**
 * 📈 游戏统计信息响应数据结构
 * 
 * 后端返回的全局游戏统计数据
 */
export interface GameStats {
    total_players: number;       // 👥 总玩家数量
    total_games: number;         // 🎮 总游戏次数
    winners_count: number;       // 🏆 获胜者数量
    dropout_count: number;       // 🚪 退学人数
    average_hope: number;        // 📊 平均希望值
    average_papers: number;      // 📚 平均论文数
    average_duration: number;    // ⏱️ 平均游戏时长(分钟)
    slack_off_masters: number;   // 😴 划水大师数量(划水10次以上)
}

/**
 * 🏆 排行榜数据结构
 * 
 * 包含三种不同类型的排行榜数据
 */
export interface LeaderboardData {
    top_hope: Array<{            // 💪 希望值排行榜
        player_id: string;       // 🔑 玩家ID
        final_hope: number;      // 💪 最终希望值
        graduation_status: string; // 🎓 毕业状态
    }>;
    top_papers: Array<{          // 📚 论文数量排行榜
        player_id: string;       // 🔑 玩家ID
        final_papers: number;    // 📚 论文数量
        graduation_status: string; // 🎓 毕业状态
    }>;
    slack_off_masters: Array<{   // 😴 划水大师排行榜
        player_id: string;       // 🔑 玩家ID
        slack_off_count: number; // 😴 划水次数
        graduation_status: string; // 🎓 毕业状态
    }>;
}

/**
 * 🚀 游戏API服务类
 * 
 * 负责处理所有与后端API的通信逻辑
 * 包括数据发送、响应处理、错误处理等
 */
class GameApiService {
    private baseUrl: string;           // 🌐 API基础URL
    private playerId: string | null = null; // 🔑 当前玩家ID

    /**
     * 🏗️ 构造函数
     * 
     * @param baseUrl - API服务器的基础URL
     *                 - 空字符串表示使用相对路径
     *                 - 例如: "https://api.example.com" 或 ""
     */
    constructor(baseUrl: string = '') {
        this.baseUrl = baseUrl;
        this.playerId = this.generatePlayerId();
    }

    /**
     * 🔑 生成玩家唯一ID
     * 
     * 策略:
     * 1. 优先从localStorage读取已存在的ID
     * 2. 如果不存在，生成新的唯一ID并保存
     * 3. 确保同一设备每次生成的ID都一致
     * 
     * @returns 玩家唯一标识符
     */
    private generatePlayerId(): string {
        // 🔍 检查本地存储中是否已有ID
        let storedId = localStorage.getItem('phd_game_player_id');
        if (storedId) {
            return storedId;
        }

        // 🆔 生成新的唯一ID
        // 格式: "player_时间戳_随机字符串"
        const newId = 'player_' + Date.now() + '_' + Math.random().toString(36).substr(2, 9);
        
        // 💾 保存到本地存储
        localStorage.setItem('phd_game_player_id', newId);
        return newId;
    }

    /**
     * 🔑 获取当前玩家ID
     * 
     * @returns 当前玩家的唯一标识符
     * @throws 如果playerId未初始化会抛出错误
     */
    getPlayerId(): string {
        return this.playerId!;
    }

    /**
     * 🎮 记录游戏开始
     * 
     * 当玩家开始新游戏时调用此方法，向后端发送:
     * - 玩家ID
     * - 设备信息 (屏幕分辨率、语言、时区)
     * 
     * 📡 请求: POST /api/game/start
     * 📊 响应: 成功返回true，失败返回false
     * 
     * @returns Promise<boolean> - 记录是否成功
     */
    async startGame(): Promise<boolean> {
        try {
            // 📱 收集设备信息
            const data: GameStartData = {
                player_id: this.playerId!,
                user_agent: navigator.userAgent,                       // 🌐 用户代理字符串
                screen_resolution: `${screen.width}x${screen.height}`,  // 📱 屏幕分辨率
                language: navigator.language,                          // 🌍 浏览器语言
                timezone: Intl.DateTimeFormat().resolvedOptions().timeZone  // ⏰ 用户时区
            };

            // 🌐 发送HTTP请求到后端
            const response = await fetch(`${this.baseUrl}/api/game/start`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',  // 📋 指定JSON格式
                },
                body: JSON.stringify(data)  // 📦 序列化请求数据
            });

            // ✅ 处理响应
            if (response.ok) {
                console.log('✅ 游戏开始记录成功');
                return true;
            } else {
                console.warn('⚠️ 游戏开始记录失败:', response.status);
                return false;
            }
        } catch (error) {
            // ❌ 网络错误或其他异常
            console.warn('⚠️ 游戏开始记录失败:', error);
            return false;
        }
    }

    /**
     * 🏁 记录游戏结束
     * 
     * 当游戏结束时调用此方法，向后端发送完整的游戏结果数据
     * 这些数据将用于:
     * - 统计分析
     * - 排行榜计算
     * - 玩家行为分析
     * 
     * 📡 请求: POST /api/game/end
     * 📊 响应: 成功返回true，失败返回false
     * 
     * @param gameData - 游戏结束数据 (不包含player_id，会自动添加)
     * @returns Promise<boolean> - 记录是否成功
     */
    async endGame(gameData: Omit<GameEndData, 'player_id'>): Promise<boolean> {
        try {
            // 🔧 构建完整的请求数据
            const data: GameEndData = {
                player_id: this.playerId!,  // 🔑 自动添加玩家ID
                ...gameData                 // 📊 展开传入的游戏数据
            };

            // 🌐 发送HTTP请求到后端
            const response = await fetch(`${this.baseUrl}/api/game/end`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(data)
            });

            // ✅ 处理响应
            if (response.ok) {
                console.log('✅ 游戏结束记录成功');
                return true;
            } else {
                console.warn('⚠️ 游戏结束记录失败:', response.status);
                return false;
            }
        } catch (error) {
            // ❌ 网络错误或其他异常
            console.warn('⚠️ 游戏结束记录失败:', error);
            return false;
        }
    }

    /**
     * 📊 获取游戏统计信息
     * 
     * 从后端获取全局的游戏统计数据，包括:
     * - 总玩家数和游戏数
     * - 获胜者和退学人数
     * - 平均希望值、论文数、游戏时长
     * - 划水大师数量
     * 
     * 📡 请求: GET /api/stats
     * 📊 响应: GameStats对象或null
     * 
     * @returns Promise<GameStats | null> - 统计信息或null
     */
    async getGameStats(): Promise<GameStats | null> {
        try {
            // 🌐 发送GET请求获取统计数据
            const response = await fetch(`${this.baseUrl}/api/stats`);
            
            if (response.ok) {
                // ✅ 成功获取数据，解析JSON
                return await response.json();
            }
        } catch (error) {
            // ❌ 网络错误或其他异常
            console.warn('⚠️ 获取游戏统计失败:', error);
        }
        return null;  // 🔴 失败时返回null
    }

    /**
     * 🏆 获取排行榜数据
     * 
     * 从后端获取三种类型的排行榜:
     * 1. 希望值排行榜 (按最终希望值排序)
     * 2. 论文数量排行榜 (按论文数排序)
     * 3. 划水大师排行榜 (按划水次数排序)
     * 
     * 📡 请求: GET /api/leaderboard
     * 📊 响应: LeaderboardData对象或null
     * 
     * @returns Promise<LeaderboardData | null> - 排行榜数据或null
     */
    async getLeaderboard(): Promise<LeaderboardData | null> {
        try {
            // 🌐 发送GET请求获取排行榜
            const response = await fetch(`${this.baseUrl}/api/leaderboard`);
            
            if (response.ok) {
                // ✅ 成功获取数据，解析JSON
                return await response.json();
            }
        } catch (error) {
            // ❌ 网络错误或其他异常
            console.warn('⚠️ 获取排行榜失败:', error);
        }
        return null;  // 🔴 失败时返回null
    }

    /**
     * 👤 获取玩家个人游戏记录
     * 
     * 获取当前玩家的详细游戏记录，包括:
     * - 游戏开始和结束时间
     * - 最终状态和分数
     * - 设备信息和行为统计
     * 
     * 📡 请求: GET /api/game/{player_id}
     * 📊 响应: 玩家游戏记录对象或null
     * 
     * @returns Promise<any | null> - 玩家记录或null
     */
    async getPlayerGame(): Promise<any | null> {
        try {
            // 🌐 发送GET请求获取玩家记录
            const response = await fetch(`${this.baseUrl}/api/game/${this.playerId}`);
            
            if (response.ok) {
                // ✅ 成功获取数据，解析JSON
                return await response.json();
            }
        } catch (error) {
            // ❌ 网络错误或其他异常
            console.warn('⚠️ 获取玩家记录失败:', error);
        }
        return null;  // 🔴 失败时返回null
    }
}

// 🌍 创建全局API服务实例
export const gameApi = new GameApiService();

/**
 * ⚙️ 配置游戏API基础URL
 * 
 * 用于动态设置API服务器的地址，支持:
 * - 开发环境: 相对路径或localhost
 * - 生产环境: 完整的域名和协议
 * 
 * @param baseUrl - API服务器的基础URL
 *                 - 例如: "https://api.example.com" 或 "http://localhost:8000"
 * 
 * 📝 使用示例:
 * ```typescript
 * // 开发环境
 * configureGameApi('http://localhost:8000');
 * 
 * // 生产环境
 * configureGameApi('https://api.joketop.com.cn');
 * ```
 */
export function configureGameApi(baseUrl: string) {
    // 🔄 重新创建实例以更新baseUrl
    // 使用Object.assign保持引用不变，但更新所有属性
    Object.assign(gameApi, new GameApiService(baseUrl));
}
