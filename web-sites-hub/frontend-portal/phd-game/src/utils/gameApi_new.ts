/**
 * 🎮 游戏API调用服务
 * 
 * 提供完整的游戏状态管理和会话控制功能。
 * 主要功能包括:
 * - 完整的游戏会话生命周期管理
 * - 设备指纹识别和验证
 * - 游戏暂停/恢复功能
 * - 详细的游戏结束原因分析
 * 
 * 📡 主要功能:
 * - 游戏生命周期数据记录 (开始/结束/暂停/恢复)
 * - 游戏统计信息获取
 * - 排行榜数据获取
 * - 玩家个人记录查询
 * - 游戏状态管理和监控
 * 
 * 🔗 后端API端点:
 * - POST /api/game/start - 记录游戏开始
 * - POST /api/game/end - 记录游戏结束
 * - GET /api/stats - 获取游戏统计
 * - GET /api/leaderboard - 获取排行榜
 * - GET /api/game/{player_id} - 获取玩家记录
 * 
 * 📚 依赖模块:
 * - playerIdManager: 玩家ID管理
 * - gameStateManager: 游戏状态管理
 */

import { playerIdManager } from './playerId';
import { gameStateManager, GameEndReason } from './gameState';

/**
 * 📊 游戏开始请求数据结构
 * 
 * 包含以下字段:
 * - player_id: 玩家唯一标识符
 * - user_agent: 用户代理字符串
 * - screen_resolution: 屏幕分辨率
 * - language: 浏览器语言偏好
 * - timezone: 用户时区
 */
export interface GameStartData {
    player_id: string;           // 🔑 玩家唯一标识符
    user_agent?: string;         // 🌐 用户代理字符串
    screen_resolution?: string;  // 📱 屏幕分辨率 (如: "1920x1080")
    language?: string;           // 🌍 浏览器语言偏好 (如: "zh-CN")
    timezone?: string;           // ⏰ 用户时区 (如: "Asia/Shanghai")
    device_info?: any;          // 📱 完整的设备指纹信息
}

/**
 * 📊 游戏结束请求数据结构
 * 
 * 包含以下字段:
 * - session_id: 游戏会话ID
 * - game_duration: 游戏时长
 * - end_reason: 游戏结束原因
 */
export interface GameEndData {
    player_id: string;           // 🔑 玩家唯一标识符
    session_id: string;          // 🎯 游戏会话ID
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
    game_duration: number;       // ⏱️ 游戏时长 (毫秒)
    end_reason: string;          // 🏁 游戏结束原因
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
 * 提供完整的游戏状态管理和会话控制功能。
 * 负责处理所有与后端API的通信逻辑，包括数据发送、响应处理、错误处理等。
 * 
 * 🔧 主要功能:
 * - 游戏会话管理 (开始/暂停/恢复/结束)
 * - 设备指纹验证
 * - 游戏状态监控
 * - 详细的结束原因分析
 */
class GameApiService {
    private baseUrl: string;           // 🌐 API基础URL

    /**
     * 🏗️ 构造函数
     * 
     * @param baseUrl - API服务器的基础URL
     *                 - 空字符串表示使用相对路径
     *                 - 例如: "https://api.example.com" 或 ""
     */
    constructor(baseUrl: string = '') {
        this.baseUrl = baseUrl;
    }

    /**
     * 🎮 记录游戏开始
     * 
     * 当玩家开始新游戏时调用此方法，向后端发送:
     * - 玩家ID和会话ID
     * - 设备信息 (屏幕分辨率、语言、时区)
     * - 设备指纹信息
     * 
     * 🔄 流程:
     * 1. 获取玩家ID
     * 2. 开始游戏会话
     * 3. 收集设备信息
     * 4. 发送数据到后端
     * 
     * 📡 请求: POST /api/game/start
     * 📊 响应: 成功返回true，失败返回false
     * 
     * @returns Promise<boolean> - 记录是否成功
     */
    async startGame(): Promise<boolean> {
        try {
            // 🔑 获取玩家ID
            const playerId = await playerIdManager.getPlayerId();
            
            // 🎯 开始游戏会话
            const session = gameStateManager.startGame();
            
            // 🔍 获取设备指纹信息
            const deviceInfo = await playerIdManager.getPlayerIdInfo();
            
            // 📱 收集设备信息
            const data: GameStartData = {
                player_id: playerId,
                user_agent: navigator.userAgent,                        // 🌐 用户代理
                screen_resolution: `${screen.width}x${screen.height}`,  // 📱 屏幕分辨率
                language: navigator.language,                          // 🌍 浏览器语言
                timezone: Intl.DateTimeFormat().resolvedOptions().timeZone,  // ⏰ 用户时区
                device_info: deviceInfo                                // 📱 完整的设备指纹信息
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
                console.log('✅ 游戏开始记录成功:', session.sessionId);
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
     * 当游戏结束时调用此方法，向后端发送完整的游戏结果数据。
     * 包含会话管理和结束原因分析功能。
     * 
     * 🔄 流程:
     * 1. 获取玩家ID和当前会话
     * 2. 分析游戏结束原因
     * 3. 结束游戏会话并计算时长
     * 4. 发送完整数据到后端
     * 
     * 📡 请求: POST /api/game/end
     * 📊 响应: 成功返回true，失败返回false
     * 
     * @param gameData - 游戏结束数据 (不包含player_id、session_id、game_duration、end_reason)
     * @returns Promise<boolean> - 记录是否成功
     */
    async endGame(gameData: Omit<GameEndData, 'player_id' | 'session_id' | 'game_duration' | 'end_reason'>): Promise<boolean> {
        try {
            // 🔑 获取玩家ID
            const playerId = await playerIdManager.getPlayerId();
            
            // 🎯 获取当前游戏会话
            const session = gameStateManager.getCurrentSession();
            if (!session) {
                console.warn('⚠️ 没有活跃的游戏会话');
                return false;
            }
            
            // 🏁 分析游戏结束原因并结束会话
            const endReason = this._determineEndReason(gameData);
            const endedSession = gameStateManager.endGame(endReason);
            
            if (!endedSession) {
                console.warn('⚠️ 游戏会话结束失败');
                return false;
            }
            
            // ⏱️ 计算游戏时长 (毫秒)
            const gameDuration = endedSession.endTime!.getTime() - endedSession.startTime.getTime();
            
            // 🔧 构建完整的请求数据
            const data: GameEndData = {
                player_id: playerId,
                session_id: session.sessionId,
                game_duration: gameDuration,
                end_reason: endReason,
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
                console.log('✅ 游戏结束记录成功:', session.sessionId);
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
     * ⏸️ 暂停游戏
     * 
     * 暂停当前游戏会话，但不结束游戏。
     * 玩家可以稍后恢复游戏继续。
     * 
     * 🔄 流程:
     * 1. 检查是否有活跃的游戏会话
     * 2. 将游戏状态设置为暂停
     * 3. 保存会话状态到本地存储
     */
    pauseGame(): void {
        gameStateManager.pauseGame();
        console.log('⏸️ 游戏已暂停');
    }

    /**
     * ▶️ 恢复游戏
     * 
     * 恢复之前暂停的游戏会话。
     * 只有在游戏处于暂停状态时才能恢复。
     * 
     * 🔄 流程:
     * 1. 检查游戏是否处于暂停状态
     * 2. 将游戏状态恢复为进行中
     * 3. 更新会话状态
     */
    resumeGame(): void {
        gameStateManager.resumeGame();
        console.log('▶️ 游戏已恢复');
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
            // 🔑 获取玩家ID
            const playerId = await playerIdManager.getPlayerId();
            
            // 🌐 发送GET请求获取玩家记录
            const response = await fetch(`${this.baseUrl}/api/game/${playerId}`);
            
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

    /**
     * 📊 获取当前游戏状态
     * 
     * 获取当前游戏的完整状态信息，包括:
     * - 当前会话信息
     * - 玩家信息
     * - 游戏统计信息
     * 
     * 📊 返回数据:
     * - session: 当前游戏会话
     * - playerInfo: 玩家信息
     * - gameStats: 游戏统计
     * 
     * @returns 当前游戏状态对象
     */
    getCurrentGameState() {
        return {
            session: gameStateManager.getCurrentSession(),
            playerInfo: playerIdManager.getPlayerIdInfo(),
            gameStats: gameStateManager.getGameStats()
        };
    }

    /**
     * 🔄 重置游戏状态 (用于测试)
     * 
     * 清除所有游戏状态和玩家ID，恢复到初始状态。
     * 主要用于开发和测试环境。
     * 
     * ⚠️ 注意: 此操作会清除所有本地存储的游戏数据
     */
    resetGameState(): void {
        gameStateManager.reset();
        playerIdManager.resetPlayerId();
        console.log('🔄 游戏状态已重置');
    }

    /**
     * 🏁 确定游戏结束原因
     * 
     * 根据游戏结果数据智能分析游戏结束的原因。
     * 支持多种结束场景:
     * - 正常毕业: 获胜且划水次数 < 10
     * - 划水毕业: 获胜但划水次数 >= 10
     * - 退学: 游戏失败
     * 
     * @param gameData - 游戏结果数据
     * @returns GameEndReason - 游戏结束原因
     */
    private _determineEndReason(gameData: any): GameEndReason {
        if (gameData.is_winner) {
            if (gameData.slack_off_count >= 10) {
                return GameEndReason.SECRET_GRADUATION;  // 😴 划水毕业
            } else {
                return GameEndReason.GRADUATION;         // 🎓 正常毕业
            }
        } else {
            return GameEndReason.DROPOUT;                // 🚪 退学
        }
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
