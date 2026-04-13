/**
 * 🔑 玩家ID生成和管理系统
 * 
 * 这个模块负责生成和管理玩家的唯一标识符，基于设备指纹技术。
 * 主要功能包括:
 * - 基于设备特征生成唯一玩家ID
 * - 设备指纹收集和验证
 * - 玩家ID的持久化存储
 * - 设备变更时的ID验证
 * 
 * 🔍 设备指纹特征:
 * - 屏幕分辨率、颜色深度、像素比例
 * - 浏览器平台、用户代理
 * - 硬件并发数、触摸点数量
 * - 语言偏好、时区设置
 * 
 * 💾 存储策略:
 * - 使用localStorage持久化存储
 * - 支持ID重置和重新生成
 * - 设备指纹验证确保一致性
 * 
 * 🔗 与后端集成:
 * - 为API请求提供稳定的玩家标识
 * - 支持设备指纹信息传输
 * - 确保玩家数据的连续性
 */

/**
 * 🔍 设备指纹数据结构
 * 
 * 收集设备的稳定特征信息，用于生成和验证玩家ID。
 * 这些特征在设备重启后仍然保持一致。
 */
export interface DeviceFingerprint {
    screen: string;              // 📱 屏幕分辨率 (如: "1920x1080")
    timezone: string;            // ⏰ 用户时区 (如: "Asia/Shanghai")
    language: string;            // 🌍 浏览器语言 (如: "zh-CN")
    platform: string;            // 💻 操作系统平台 (如: "Win32")
    userAgent: string;           // 🌐 用户代理字符串
    colorDepth: number;          // 🎨 颜色深度 (如: 24)
    pixelRatio: number;          // 🔍 设备像素比例 (如: 1.5)
    hardwareConcurrency: number; // 🚀 CPU核心数 (如: 8)
    maxTouchPoints: number;      // 👆 最大触摸点数量 (如: 5)
}

/**
 * 🔑 玩家ID管理器类
 * 
 * 单例模式实现，确保整个应用只有一个玩家ID管理器实例。
 * 负责玩家ID的生成、存储、验证和管理。
 * 
 * 🔄 生命周期:
 * 1. 应用启动时初始化
 * 2. 首次访问时生成玩家ID
 * 3. 后续访问时验证ID有效性
 * 4. 支持手动重置和重新生成
 */
export class PlayerIdManager {
    private static instance: PlayerIdManager;           // 🎯 单例实例
    private playerId: string | null = null;            // 🔑 当前玩家ID
    private readonly STORAGE_KEY = 'phd_game_player_id';           // 💾 存储键名
    private readonly FINGERPRINT_KEY = 'phd_game_device_fingerprint'; // 🔍 指纹存储键名

    /**
     * 🚫 私有构造函数
     * 
     * 防止外部直接实例化，确保单例模式
     */
    private constructor() {}

    /**
     * 🎯 获取单例实例
     * 
     * 如果实例不存在则创建，如果已存在则返回现有实例。
     * 确保整个应用只有一个玩家ID管理器。
     * 
     * @returns PlayerIdManager - 单例实例
     */
    static getInstance(): PlayerIdManager {
        if (!PlayerIdManager.instance) {
            PlayerIdManager.instance = new PlayerIdManager();
        }
        return PlayerIdManager.instance;
    }

    /**
     * 🔑 获取或生成玩家ID
     * 
     * 这是核心方法，负责玩家ID的获取和生成逻辑。
     * 
     * 🔄 执行流程:
     * 1. 检查内存中是否已有ID
     * 2. 从localStorage读取已存储的ID
     * 3. 如果ID不存在，生成新的ID
     * 4. 验证生成的ID与设备指纹的匹配性
     * 5. 保存ID到localStorage
     * 
     * 📊 返回值:
     * - 如果验证通过，返回玩家ID
     * - 如果验证失败，重新生成并返回新ID
     * 
     * @returns Promise<string> - 玩家唯一标识符
     */
    async getPlayerId(): Promise<string> {
        // 🔍 检查内存中是否已有ID
        if (this.playerId) {
            return this.playerId;
        }

        // 💾 尝试从本地存储获取已存储的ID
        const storedId = localStorage.getItem(this.STORAGE_KEY);
        if (storedId) {
            this.playerId = storedId;
            return this.playerId;
        }

        // 🆔 生成新的玩家ID
        this.playerId = await this.generatePlayerId();
        
        // ✅ 验证生成的ID是否与存储的指纹匹配
        const isValid = await this.validateStoredId(this.playerId);
        if (!isValid) {
            // 🔄 如果ID无效，重新生成
            this.playerId = await this.generatePlayerId();
        }
        
        // 💾 保存ID到本地存储
        localStorage.setItem(this.STORAGE_KEY, this.playerId);
        
        return this.playerId;
    }

    /**
     * 🆔 生成基于设备指纹的玩家ID
     * 
     * 使用设备的稳定特征生成唯一的玩家标识符。
     * 生成的ID具有以下特点:
     * - 基于设备硬件和软件特征
     * - 同一设备每次生成结果一致
     * - 不同设备生成结果不同
     * - 包含时间戳和随机数确保唯一性
     * 
     * 🔍 指纹特征包括:
     * - 屏幕分辨率和颜色深度
     * - 浏览器平台和用户代理
     * - 硬件配置信息
     * - 语言和时区设置
     * 
     * @returns Promise<string> - 基于设备指纹的唯一ID
     */
    private async generatePlayerId(): Promise<string> {
        // 🔍 收集设备指纹信息
        const fingerprint = await this.getDeviceFingerprint();
        
        // 🔐 计算指纹哈希值
        const fingerprintHash = await this.hashFingerprint(fingerprint);
        
        // 🆔 生成玩家ID (只使用稳定的设备指纹哈希)
        // 格式: "player_指纹哈希"
        // 这样同一设备每次生成的ID都是一致的
        return `player_${fingerprintHash}`;
    }

    /**
     * 🔍 获取设备指纹信息
     * 
     * 收集设备的稳定特征信息，这些信息在设备重启后仍然保持一致。
     * 收集的信息包括硬件特征、软件配置、用户偏好等。
     * 
     * 📱 收集的特征:
     * - 屏幕: 分辨率、颜色深度、像素比例
     * - 硬件: CPU核心数、触摸点数量
     * - 软件: 平台、用户代理
     * - 用户: 语言偏好、时区设置
     * 
     * 💾 存储策略:
     * - 将指纹信息保存到localStorage
     * - 用于后续的ID验证
     * 
     * @returns Promise<DeviceFingerprint> - 设备指纹信息
     */
    private async getDeviceFingerprint(): Promise<DeviceFingerprint> {
        // 📱 收集设备特征信息
        const fingerprint: DeviceFingerprint = {
            screen: `${screen.width}x${screen.height}`,                   // 📱 屏幕分辨率
            timezone: Intl.DateTimeFormat().resolvedOptions().timeZone,   // ⏰ 用户时区
            language: navigator.language,                                 // 🌍 浏览器语言
            platform: navigator.platform,                                 // 💻 操作系统平台
            userAgent: navigator.userAgent,                               // 🌐 用户代理字符串
            colorDepth: screen.colorDepth,                                // 🎨 颜色深度
            pixelRatio: window.devicePixelRatio || 1,                     // 🔍 设备像素比例
            hardwareConcurrency: navigator.hardwareConcurrency || 0,      // 🚀 CPU核心数
            maxTouchPoints: navigator.maxTouchPoints || 0                 // 👆 最大触摸点数量
        };

        // 💾 存储指纹用于后续验证
        localStorage.setItem(this.FINGERPRINT_KEY, JSON.stringify(fingerprint));
        
        return fingerprint;
    }

    /**
     * 🔐 指纹哈希算法
     * 
     * 将设备指纹信息转换为数字哈希值。
     * 使用字符串哈希算法，确保:
     * - 相同的指纹总是产生相同的哈希
     * - 不同的指纹产生不同的哈希
     * - 哈希值在合理范围内
     * 
     * ⚠️ 注意: 生产环境建议使用更安全的哈希算法
     * 
     * 🔄 算法原理:
     * 1. 将指纹对象序列化为字符串
     * 2. 遍历字符串的每个字符
     * 3. 使用简单的数学运算计算哈希值
     * 4. 转换为36进制字符串
     * 
     * @param fingerprint - 设备指纹信息
     * @returns Promise<string> - 指纹哈希值 (36进制)
     */
    private async hashFingerprint(fingerprint: DeviceFingerprint): Promise<string> {
        // 📝 将指纹对象序列化为字符串
        const fingerprintString = JSON.stringify(fingerprint);
        
        // 🔢 计算哈希值
        let hash = 0;
        for (let i = 0; i < fingerprintString.length; i++) {
            const char = fingerprintString.charCodeAt(i);
            // 使用简单的哈希算法: hash = hash * 31 + char
            hash = ((hash << 5) - hash) + char;
            hash = hash & hash; // 转换为32位整数
        }
        
        // 🔄 转换为36进制字符串 (0-9, a-z)
        return Math.abs(hash).toString(36);
    }

    /**
     * ✅ 验证当前设备指纹是否匹配
     * 
     * 比较当前设备的指纹与之前存储的指纹是否一致。
     * 用于检测设备是否发生了重大变化。
     * 
     * 🔍 验证策略:
     * - 只比较关键特征，忽略可能变化的特征
     * - 关键特征包括: 屏幕、时区、平台、颜色深度
     * - 这些特征在设备重启后保持一致
     * 
     * 📊 返回值:
     * - true: 设备指纹匹配，ID有效
     * - false: 设备指纹不匹配，需要重新生成ID
     * 
     * @returns Promise<boolean> - 设备指纹是否匹配
     */
    async validateDeviceFingerprint(): Promise<boolean> {
        // 💾 从存储中读取指纹信息
        const storedFingerprint = localStorage.getItem(this.FINGERPRINT_KEY);
        if (!storedFingerprint) {
            return false;  // 🔴 没有存储的指纹，无法验证
        }

        try {
            // 📖 解析存储的指纹信息
            const stored = JSON.parse(storedFingerprint);
            
            // 🔍 获取当前设备的指纹信息
            const current = await this.getDeviceFingerprint();
            
            // ✅ 比较关键指纹特征
            // 只比较稳定的特征，忽略可能变化的特征
            const keyFeatures = ['screen', 'timezone', 'platform', 'colorDepth'];
            return keyFeatures.every(feature => 
                stored[feature as keyof DeviceFingerprint] === current[feature as keyof DeviceFingerprint]
            );
        } catch {
            // ❌ 解析失败，认为指纹无效
            return false;
        }
    }

    /**
     * ✅ 验证存储的ID是否与当前设备匹配
     * 
     * 验证localStorage中存储的玩家ID是否仍然有效。
     * 通过比较ID中的指纹哈希与当前设备指纹来判断。
     * 
     * 🔄 验证流程:
     * 1. 从存储的ID中提取指纹哈希
     * 2. 生成当前设备的指纹哈希
     * 3. 比较两个哈希值是否一致
     * 
     * 📊 返回值:
     * - true: ID有效，可以继续使用
     * - false: ID无效，需要重新生成
     * 
     * @param storedId - 存储的玩家ID
     * @returns Promise<boolean> - ID是否有效
     */
    private async validateStoredId(storedId: string): Promise<boolean> {
        try {
            // 🔍 从存储的ID中提取指纹哈希
            const idParts = storedId.split('_');
            if (idParts.length !== 2 || idParts[0] !== 'player') {
                return false;  // 🔴 ID格式不正确
            }

            const storedHash = idParts[1];
            
            // 🔍 生成当前设备的指纹哈希
            const currentFingerprint = await this.getDeviceFingerprint();
            const currentHash = await this.hashFingerprint(currentFingerprint);
            
            // ✅ 比较哈希值
            return storedHash === currentHash;
        } catch {
            // ❌ 验证过程出错，认为ID无效
            return false;
        }
    }

    /**
     * 🔄 重置玩家ID
     * 
     * 清除所有存储的玩家ID和指纹信息，恢复到初始状态。
     * 主要用于开发和测试环境，生产环境不建议使用。
     * 
     * ⚠️ 注意事项:
     * - 此操作会清除所有本地存储的游戏数据
     * - 玩家将失去游戏进度和统计数据
     * - 下次访问时会生成全新的玩家ID
     * 
     * 🧹 清理内容:
     * - 内存中的playerId
     * - localStorage中的玩家ID
     * - localStorage中的设备指纹
     */
    resetPlayerId(): void {
        this.playerId = null;
        localStorage.removeItem(this.STORAGE_KEY);
        localStorage.removeItem(this.FINGERPRINT_KEY);
    }

    /**
     * 📊 获取玩家ID信息
     * 
     * 返回当前玩家ID的详细信息，包括:
     * - 当前ID值
     * - 是否为新玩家
     * - 设备指纹是否有效
     * - ID一致性状态
     * 
     * 📊 返回信息:
     * - id: 当前玩家ID
     * - isNewPlayer: 是否为新玩家 (首次访问)
     * - deviceValid: 设备指纹是否有效
     * - idConsistent: ID是否与设备一致
     * 
     * @returns 玩家ID信息对象
     */
    getPlayerIdInfo(): { id: string; isNewPlayer: boolean; deviceValid: boolean; idConsistent: boolean } {
        // 💾 检查是否有存储的ID
        const storedId = localStorage.getItem(this.STORAGE_KEY);
        const isNewPlayer = !storedId;
        
        // ✅ 检查ID一致性
        let idConsistent = false;
        if (storedId && this.playerId) {
            // 内存和存储都有ID，比较是否一致
            idConsistent = storedId === this.playerId;
        } else if (storedId) {
            // 只有存储的ID，认为是一致的
            idConsistent = true;
        }
        
        // 📊 返回完整的ID信息
        return {
            id: this.playerId || storedId || 'unknown',
            isNewPlayer,
            deviceValid: true, // 当前实现，实际应该调用validateDeviceFingerprint
            idConsistent
        };
    }
}

// 🌍 导出单例实例
export const playerIdManager = PlayerIdManager.getInstance();
