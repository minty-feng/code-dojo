/**
 * 🎮 游戏状态管理系统
 * 
 * 这个模块负责管理游戏的完整生命周期状态，包括:
 * - 游戏会话的创建、暂停、恢复和结束
 * - 游戏状态的数据持久化
 * - 会话超时检测和清理
 * - 游戏统计信息的收集
 * 
 * 🔄 状态流转:
 * NOT_STARTED → PLAYING → PAUSED → PLAYING → ENDED
 *                    ↓
 *                 MANUAL_QUIT
 * 
 * 💾 持久化策略:
 * - 使用localStorage保存会话状态
 * - 支持会话恢复和超时处理
 * - 24小时会话超时机制
 * 
 * 🔗 与后端集成:
 * - 为API请求提供会话信息
 * - 支持游戏暂停/恢复功能
 * - 确保游戏数据的连续性
 */

/**
 * 🎯 游戏状态枚举
 * 
 * 定义游戏在整个生命周期中可能处于的各种状态
 */
export enum GameStatus {
    NOT_STARTED = 'not_started',  // 🚫 游戏未开始
    PLAYING = 'playing',           // ▶️ 游戏进行中
    PAUSED = 'paused',            // ⏸️ 游戏暂停
    ENDED = 'ended'               // 🏁 游戏已结束
}

/**
 * 🏁 游戏结束原因枚举
 * 
 * 定义游戏结束的各种原因，用于:
 * - 后端数据记录和分析
 * - 前端UI显示和统计
 * - 游戏逻辑判断
 */
export enum GameEndReason {
    GRADUATION = 'graduation',           // 🎓 正常毕业 (希望值达到要求)
    DROPOUT = 'dropout',                 // 🚪 退学 (希望值过低)
    SECRET_GRADUATION = 'secret_graduation', // 😴 划水毕业 (划水次数过多但仍毕业)
    TIMEOUT = 'timeout',                 // ⏰ 超时 (游戏时间过长)
    MANUAL_QUIT = 'manual_quit'          // 🖱️ 手动退出 (玩家主动退出)
}

/**
 * 🎯 游戏会话数据结构
 * 
 * 记录单个游戏会话的完整信息，包括:
 * - 会话标识和时间信息
 * - 当前状态和结束原因
 * - 活跃状态标志
 */
export interface GameSession {
    sessionId: string;           // 🆔 会话唯一标识符
    startTime: Date;             // 🕐 游戏开始时间
    endTime?: Date;              // 🕐 游戏结束时间 (可选)
    status: GameStatus;          // 🎯 当前游戏状态
    endReason?: GameEndReason;   // 🏁 游戏结束原因 (可选)
    isActive: boolean;           // ✅ 会话是否活跃
}

/**
 * 🚀 游戏状态管理器类
 * 
 * 单例模式实现，负责管理整个游戏的会话状态。
 * 提供完整的游戏生命周期管理功能。
 * 
 * 🔄 主要功能:
 * - 游戏会话的创建和管理
 * - 状态转换和验证
 * - 数据持久化和恢复
 * - 超时检测和清理
 * - 统计信息收集
 */
export class GameStateManager {
    private static instance: GameStateManager;           // 🎯 单例实例
    private currentSession: GameSession | null = null;  // 🎮 当前游戏会话
    private readonly SESSION_KEY = 'phd_game_current_session';  // 💾 存储键名
    private readonly SESSION_TIMEOUT = 24 * 60 * 60 * 1000;    // ⏰ 会话超时时间 (24小时)

    /**
     * 🚫 私有构造函数
     * 
     * 防止外部直接实例化，确保单例模式。
     * 在构造时自动加载已存在的会话。
     */
    private constructor() {
        this.loadSessionFromStorage();
    }

    /**
     * 🎯 获取单例实例
     * 
     * 如果实例不存在则创建，如果已存在则返回现有实例。
     * 确保整个应用只有一个游戏状态管理器。
     * 
     * @returns GameStateManager - 单例实例
     */
    static getInstance(): GameStateManager {
        if (!GameStateManager.instance) {
            GameStateManager.instance = new GameStateManager();
        }
        return GameStateManager.instance;
    }

    /**
     * 🎮 开始新游戏
     * 
     * 创建新的游戏会话，如果已有未完成的会话会先结束它。
     * 这是游戏生命周期的起点。
     * 
     * 🔄 执行流程:
     * 1. 检查是否有未完成的会话
     * 2. 如果有，先结束现有会话
     * 3. 创建新的游戏会话
     * 4. 设置状态为进行中
     * 5. 保存到本地存储
     * 
     * 📊 返回数据:
     * - 新创建的游戏会话对象
     * - 包含会话ID、开始时间等信息
     * 
     * @returns GameSession - 新创建的游戏会话
     */
    startGame(): GameSession {
        // 🔄 如果有未完成的会话，先结束它
        if (this.currentSession && this.currentSession.isActive) {
            this.endGame(GameEndReason.MANUAL_QUIT);
        }

        // 🆔 创建新会话
        this.currentSession = {
            sessionId: this.generateSessionId(),
            startTime: new Date(),
            status: GameStatus.PLAYING,
            isActive: true
        };

        // 💾 保存会话到本地存储
        this.saveSessionToStorage();
        console.log('🎮 游戏开始:', this.currentSession.sessionId);
        
        return this.currentSession;
    }

    /**
     * ⏸️ 暂停游戏
     * 
     * 将当前游戏状态设置为暂停，但不结束游戏。
     * 玩家可以稍后恢复游戏继续。
     * 
     * 🔄 执行流程:
     * 1. 检查是否有活跃的游戏会话
     * 2. 将状态设置为暂停
     * 3. 保存状态到本地存储
     * 
     * 📊 状态变化:
     * PLAYING → PAUSED
     */
    pauseGame(): void {
        if (this.currentSession && this.currentSession.isActive) {
            this.currentSession.status = GameStatus.PAUSED;
            this.saveSessionToStorage();
            console.log('⏸️ 游戏暂停');
        }
    }

    /**
     * ▶️ 恢复游戏
     * 
     * 将暂停的游戏状态恢复为进行中。
     * 只有在游戏处于暂停状态时才能恢复。
     * 
     * 🔄 执行流程:
     * 1. 检查游戏是否处于暂停状态
     * 2. 将状态恢复为进行中
     * 3. 更新本地存储
     * 
     * 📊 状态变化:
     * PAUSED → PLAYING
     */
    resumeGame(): void {
        if (this.currentSession && this.currentSession.status === GameStatus.PAUSED) {
            this.currentSession.status = GameStatus.PLAYING;
            this.saveSessionToStorage();
            console.log('▶️ 游戏恢复');
        }
    }

    /**
     * 🏁 结束游戏
     * 
     * 将当前游戏会话标记为结束状态，记录结束原因和时间。
     * 结束后的会话将不再活跃，但保留所有历史数据。
     * 
     * 🔄 执行流程:
     * 1. 检查是否有活跃会话
     * 2. 设置结束时间和状态
     * 3. 记录结束原因
     * 4. 保存到本地存储
     * 5. 返回结束的会话对象
     * 
     * 📊 状态变化:
     * PLAYING/PAUSED → ENDED
     * 
     * @param reason - 游戏结束原因
     * @returns GameSession | null - 结束的会话对象，如果没有活跃会话则返回null
     */
    endGame(reason: GameEndReason): GameSession | null {
        if (!this.currentSession || !this.currentSession.isActive) {
            console.warn('⚠️ 没有活跃会话，无法结束游戏');
            return null;  // 🔴 没有活跃会话，无法结束
        }

        // 🏁 设置结束信息
        this.currentSession.endTime = new Date();
        this.currentSession.status = GameStatus.ENDED;
        this.currentSession.endReason = reason;
        this.currentSession.isActive = false;

        // 💾 保存会话到本地存储
        this.saveSessionToStorage();
        console.log('🏁 游戏结束:', reason, this.currentSession.sessionId);
        
        return this.currentSession;
    }

    /**
     * 🎯 获取当前游戏会话
     * 
     * 返回当前活跃或最近结束的游戏会话信息。
     * 用于获取会话状态、ID、时间等信息。
     * 
     * 📊 返回数据:
     * - 当前会话对象，包含完整的状态信息
     * - 如果没有会话则返回null
     * 
     * @returns GameSession | null - 当前游戏会话或null
     */
    getCurrentSession(): GameSession | null {
        return this.currentSession;
    }

    /**
     * ✅ 检查游戏是否进行中
     * 
     * 判断当前是否有活跃的游戏会话。
     * 用于控制游戏逻辑和UI状态。
     * 
     * 📊 返回值:
     * - true: 有活跃的游戏会话
     * - false: 没有活跃的游戏会话
     * 
     * @returns boolean - 游戏是否活跃
     */
    isGameActive(): boolean {
        return this.currentSession?.isActive === true;
    }

    /**
     * ⏸️ 检查游戏是否暂停
     * 
     * 判断当前游戏是否处于暂停状态。
     * 用于控制暂停/恢复按钮的显示。
     * 
     * 📊 返回值:
     * - true: 游戏处于暂停状态
     * - false: 游戏不处于暂停状态
     * 
     * @returns boolean - 游戏是否暂停
     */
    isGamePaused(): boolean {
        return this.currentSession?.status === GameStatus.PAUSED;
    }

    /**
     * ⏱️ 获取游戏时长
     * 
     * 计算当前游戏会话的持续时间。
     * 如果游戏已结束，返回总时长；如果进行中，返回当前时长。
     * 
     * 📊 计算逻辑:
     * - 游戏进行中: 当前时间 - 开始时间
     * - 游戏已结束: 结束时间 - 开始时间
     * 
     * @returns number - 游戏时长 (毫秒)
     */
    getGameDuration(): number {
        if (!this.currentSession) return 0;
        
        const endTime = this.currentSession.endTime || new Date();
        return endTime.getTime() - this.currentSession.startTime.getTime();
    }

    /**
     * ⏰ 检查会话是否超时
     * 
     * 判断当前会话是否超过了预设的超时时间。
     * 用于自动清理过期的游戏会话。
     * 
     * 📊 超时设置:
     * - 默认超时时间: 24小时
     * - 超时后会话会被自动清理
     * 
     * @returns boolean - 会话是否超时
     */
    isSessionTimeout(): boolean {
        if (!this.currentSession) return false;
        
        const now = new Date();
        const duration = now.getTime() - this.currentSession.startTime.getTime();
        return duration > this.SESSION_TIMEOUT;
    }

    /**
     * 🆔 生成会话ID
     * 
     * 生成唯一的游戏会话标识符。
     * 使用时间戳和随机数确保唯一性。
     * 
     * 🔄 生成策略:
     * 1. 使用当前时间戳
     * 2. 添加随机字符串
     * 3. 格式: "session_时间戳_随机字符串"
     * 
     * @returns string - 唯一的会话ID
     */
    private generateSessionId(): string {
        const timestamp = Date.now();
        const random = Math.random().toString(36).substr(2, 9);
        return `session_${timestamp}_${random}`;
    }

    /**
     * 💾 保存会话到本地存储
     * 
     * 将当前游戏会话信息保存到localStorage。
     * 支持会话的持久化和恢复。
     * 
     * 🔄 保存内容:
     * - 会话ID和状态
     * - 开始和结束时间
     * - 结束原因
     * - 活跃状态标志
     */
    private saveSessionToStorage(): void {
        if (this.currentSession) {
            localStorage.setItem(this.SESSION_KEY, JSON.stringify(this.currentSession));
        }
    }

    /**
     * 📱 从本地存储加载会话
     * 
     * 在应用启动时从localStorage恢复游戏会话。
     * 支持游戏的中断和恢复。
     * 
     * 🔄 加载流程:
     * 1. 从localStorage读取会话数据
     * 2. 检查会话是否超时
     * 3. 如果超时则清理，否则恢复会话
     * 4. 解析时间信息并重建会话对象
     * 
     * ⚠️ 错误处理:
     * - 解析失败时自动清理
     * - 超时会话自动清理
     */
    private loadSessionFromStorage(): void {
        try {
            // 💾 从存储中读取会话数据
            const stored = localStorage.getItem(this.SESSION_KEY);
            if (stored) {
                // 📖 解析存储的会话数据
                const session = JSON.parse(stored);
                
                // ⏰ 检查会话是否超时
                if (this.isSessionTimeout()) {
                    console.log('⏰ 会话超时，清理旧会话');
                    this.cleanupExpiredSession();
                    return;
                }

                // 🔄 恢复会话状态
                this.currentSession = {
                    ...session,
                    startTime: new Date(session.startTime),
                    endTime: session.endTime ? new Date(session.endTime) : undefined
                };

                console.log('📱 恢复游戏会话:', this.currentSession.sessionId);
            }
        } catch (error) {
            // ❌ 加载失败，清理过期会话
            console.warn('⚠️ 加载会话失败:', error);
            this.cleanupExpiredSession();
        }
    }

    /**
     * 🧹 清理过期会话
     * 
     * 清除过期的游戏会话数据。
     * 包括内存中的会话对象和本地存储的数据。
     * 
     * 🧹 清理内容:
     * - 内存中的currentSession
     * - localStorage中的会话数据
     * 
     * 🔄 调用时机:
     * - 会话超时时
     * - 加载失败时
     * - 手动重置时
     */
    private cleanupExpiredSession(): void {
        this.currentSession = null;
        localStorage.removeItem(this.SESSION_KEY);
    }

    /**
     * 🔄 重置游戏状态
     * 
     * 清除所有游戏状态和会话信息，恢复到初始状态。
     * 主要用于开发和测试环境，生产环境不建议使用。
     * 
     * ⚠️ 注意事项:
     * - 此操作会清除所有本地存储的游戏数据
     * - 玩家将失去游戏进度和会话信息
     * - 下次访问时会创建全新的游戏会话
     * 
     * 🧹 清理内容:
     * - 内存中的currentSession
     * - localStorage中的会话数据
     */
    reset(): void {
        this.currentSession = null;
        localStorage.removeItem(this.SESSION_KEY);
        console.log('🔄 游戏状态已重置');
    }

    /**
     * 📊 获取游戏统计信息
     * 
     * 收集当前游戏的统计信息，包括:
     * - 会话数量和总游戏时间
     * - 平均会话时长
     * - 游戏完成率
     * 
     * 📊 统计内容:
     * - totalSessions: 总会话数
     * - totalPlayTime: 总游戏时间
     * - averageSessionTime: 平均会话时长
     * - completionRate: 完成率
     * 
     * @returns 游戏统计信息对象
     */
    getGameStats(): {
        totalSessions: number;
        totalPlayTime: number;
        averageSessionTime: number;
        completionRate: number;
    } {
        // 📊 这里可以从localStorage读取历史会话数据
        // 当前返回当前会话信息
        const currentDuration = this.getGameDuration();
        
        // 安全地检查会话状态
        let completionRate = 0;
        if (this.currentSession !== null) {
            if (this.currentSession!.endReason !== undefined) {
                completionRate = 100;
            }
        }
        
        return {
            totalSessions: this.currentSession ? 1 : 0,
            totalPlayTime: currentDuration,
            averageSessionTime: currentDuration,
            completionRate: completionRate
        };
    }
}

// 🌍 导出单例实例
export const gameStateManager = GameStateManager.getInstance();
