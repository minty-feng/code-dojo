import { load as loadYaml } from 'js-yaml';
import queryString from 'query-string';

import { GuiGameWindow, GuiGameWindowDefinition } from './gui/guiGame';
import { LocalizationDictionary } from './i18n/localization';
import { GameEngine, GameConfig, GameActionProxy } from './gameEngine';
import { SimpleGameTextEngine } from './gui/textEngine';
import { downloadAndParse } from './utils/network';
import { SetBuilder } from './utils/collection';
import { gameApi, configureGameApi } from './utils/gameApi';

interface DebugConfig {
    dumpTranslationKeys?: boolean;
}

interface AppConfig extends GameConfig {
    guiDefinitionUrl?: string;
    languageFileUrl?: string;
    debugConfig?: DebugConfig;
}

class App {

    private _config: AppConfig;
    private _container: HTMLElement;
    private _localizer: LocalizationDictionary;
    private _gameEngine: GameEngine;
    private _actionProxy: GameActionProxy;
    private _gui?: GuiGameWindow;
    private _started: boolean = false;

    constructor(container: HTMLElement, config: AppConfig) {
        this._config = config;
        this._container = container;
        this._actionProxy = new GameActionProxy();
        this._gameEngine = new GameEngine(config, this._actionProxy);
        this._localizer = new LocalizationDictionary();
    }

    async start(): Promise<void> {
        if (this._started) {
            throw new Error('App already started!');
        }
        // The language file needs to be loaded first before rendering the game
        // GUI.
        if (this._config.languageFileUrl) {
            await this._localizer.loadFrom(this._config.languageFileUrl);
        } else {
            console.warn('Missing language file!');
        }
        const textEngine = new SimpleGameTextEngine(this._localizer,
                                                    this._gameEngine.variableStore,
                                                    this._gameEngine.random);
        if (!this._config.guiDefinitionUrl) {
            throw new Error('Missing GUI config file!');
        }
        let guiDef = await <GuiGameWindowDefinition>downloadAndParse(
            this._config.guiDefinitionUrl, loadYaml);
        let gui = new GuiGameWindow(this._container, textEngine,
                                    this._gameEngine, guiDef);
        this._actionProxy.attachGui(gui);
        this._gameEngine.onGameEnd = (sender, event) => {
            // 记录游戏结束数据到后端
            this._recordGameEnd(event);
            
            window.dispatchEvent(new CustomEvent('gameEnd', {
                detail: {
                    state: event.state,
                    endingType: event.endingType
                }
            }));
        };
        await this._gameEngine.start(false);
        // Debugging info for translation keys
        if (this._config.debugConfig) {
           this._dumpDebugInfo(this._config.debugConfig);
        }
        // 记录游戏开始数据到后端
        await this._recordGameStart();
        
        // Start game loop
        const gameLoop = () => {
            setTimeout(() => this._gameEngine.tick().then(gameLoop), 50);
        };
        gameLoop();
        this._started = true;
    }

    private _dumpDebugInfo(debugConfig: DebugConfig): void {
        if (debugConfig.dumpTranslationKeys) {
            const allEvents = this._gameEngine.eventEngine.getEvents();
            const builder = new SetBuilder<string>();
            for (let event of allEvents) {
                builder.addAll(event.collectTranslationKeys());
            }
            this._gameEngine.itemRegistry.forEach((item) => {
                this._localizer.addRequiredKey(item.unlocalizedName);
                this._localizer.addRequiredKey(item.unlocalizedDescription);
            });
            this._gameEngine.statusRegistry.forEach((status) => {
                this._localizer.addRequiredKey(status.unlocalizedName);
                this._localizer.addRequiredKey(status.unlocalizedDescription);
            })
            builder.get().forEach((key) => this._localizer.addRequiredKey(key));
            const requiredKeys = this._localizer.dumpRequiredTranslationKeys();
            console.log(`# Required translation keys (${requiredKeys.length}):\n${requiredKeys.join('\n')}`);
            const missingKeys = this._localizer.dumpMissingTranslationKeys();
            console.log(`# Missing translation keys (${missingKeys.length}):\n${missingKeys.join('\n')}`);
            const unnecessaryKeys = this._localizer.dumpUnnecessaryTranslationKeys();
            console.log(`# Unnecessary translation keys (${unnecessaryKeys.length}):\n${unnecessaryKeys.join('\n')}`);
        }
    }

    /**
     * 🎮 记录游戏开始数据
     * 
     * 当游戏启动时自动调用，向后端API发送游戏开始记录。
     * 记录的信息包括:
     * - 玩家ID (基于设备指纹生成)
     * - 设备信息 (屏幕分辨率、语言、时区)
     * - 游戏会话ID
     * - 开始时间戳
     * 
     * 🔄 调用时机:
     * - 应用启动完成后
     * - 游戏引擎初始化完成
     * - 语言文件加载完成
     * 
     * 📡 后端API: POST /api/game/start
     * 
     * ⚠️ 错误处理:
     * - 网络错误时记录警告日志
     * - 不影响游戏正常启动
     * - 支持离线模式继续游戏
     */
    private async _recordGameStart(): Promise<void> {
        try {
            // 🌐 调用游戏API记录开始数据
            await gameApi.startGame();
        } catch (error) {
            // ❌ 记录失败时不影响游戏启动
            console.warn('⚠️ 记录游戏开始失败:', error);
        }
    }

    /**
     * 🏁 记录游戏结束数据
     * 
     * 当游戏结束时自动调用，向后端API发送完整的游戏结果数据。
     * 记录的信息包括:
     * - 最终游戏状态 (希望值、论文数、毕业状态)
     * - 游戏结果 (是否获胜、退学原因)
     * - 行为统计 (各种操作次数、划水次数)
     * - 游戏时长和会话信息
     * 
     * 🔄 调用时机:
     * - 游戏引擎触发onGameEnd事件
     * - 玩家达到毕业条件或退学条件
     * - 游戏超时或手动退出
     * 
     * 📡 后端API: POST /api/game/end
     * 
     * 📊 收集的数据:
     * - final_hope: 最终希望值 (0-100)
     * - final_papers: 最终论文数量
     * - graduation_status: 毕业状态 ("毕业" | "退学" | "未知")
     * - is_winner: 是否获胜
     * - slack_off_count: 划水次数
     * - total_actions: 总操作次数
     * - read_paper_actions: 读论文次数
     * - work_actions: 工作相关操作次数
     * - slack_off_actions: 划水操作次数
     * - conference_actions: 参加会议次数
     * 
     * ⚠️ 错误处理:
     * - 网络错误时记录警告日志
     * - 不影响游戏结束流程
     * - 支持离线模式
     */
    private async _recordGameEnd(event: any): Promise<void> {
        try {
            // 📊 获取游戏引擎的变量存储
            const variableStore = this._gameEngine.variableStore;
            
            // 🔍 收集完整的游戏数据
            const gameData = {
                final_hope: variableStore.getVar('player.hope', false) || 0,                    // 💪 最终希望值
                final_papers: variableStore.getVar('player.readPapers', false) || 0,           // 📚 最终论文数
                graduation_status: this._getGraduationStatus(event),                 // 🎓 毕业状态
                is_winner: this._isWinner(event),                                    // 🏆 是否获胜
                slack_off_count: variableStore.getVar('player.consecutiveSlackOff', false) || 0, // 😴 划水次数
                total_actions: this._countTotalActions(),                            // 📝 总操作次数
                read_paper_actions: variableStore.getVar('player.readPapers', false) || 0,     // 📖 读论文次数
                work_actions: this._countWorkActions(),                              // 💼 工作操作次数
                slack_off_actions: variableStore.getVar('player.consecutiveSlackOff', false) || 0, // 😴 划水操作次数
                conference_actions: variableStore.getVar('player.canAttendConf', false) || 0   // 🎤 会议次数
            };

            // 🌐 调用游戏API记录结束数据
            await gameApi.endGame(gameData);
        } catch (error) {
            // ❌ 记录失败时不影响游戏结束流程
            console.warn('⚠️ 记录游戏结束失败:', error);
        }
    }

    /**
     * 🎓 获取毕业状态
     * 
     * 根据游戏引擎的事件状态判断玩家的最终毕业状态。
     * 这个状态将用于后端数据记录和统计分析。
     * 
     * 📊 状态映射:
     * - 'winning' → '毕业' (玩家成功毕业)
     * - 'losing' → '退学' (玩家退学)
     * - 其他状态 → '未知' (异常状态)
     * 
     * 🔗 与后端集成:
     * - 作为graduation_status字段发送到后端
     * - 用于统计毕业率和退学率
     * - 支持排行榜和成就系统
     * 
     * @param event - 游戏引擎的结束事件对象
     * @returns string - 毕业状态字符串
     */
    private _getGraduationStatus(event: any): string {
        if (event.state === 'winning') {
            return '毕业';      // 🎓 玩家成功毕业
        } else if (event.state === 'losing') {
            return '退学';      // 🚪 玩家退学
        } else {
            return '未知';      // ❓ 异常状态
        }
    }

    /**
     * 🏆 判断是否获胜
     * 
     * 根据游戏引擎的事件状态判断玩家是否获胜。
     * 这个布尔值将用于后端数据记录和统计分析。
     * 
     * 📊 判断逻辑:
     * - event.state === 'winning' → true (获胜)
     * - 其他状态 → false (未获胜)
     * 
     * 🔗 与后端集成:
     * - 作为is_winner字段发送到后端
     * - 用于统计获胜率和成功率
     * - 支持成就系统和排行榜
     * 
     * @param event - 游戏引擎的结束事件对象
     * @returns boolean - 是否获胜
     */
    private _isWinner(event: any): boolean {
        return event.state === 'winning';  // 🏆 只有winning状态才算获胜
    }

    /**
     * 📝 统计总操作次数
     * 
     * 计算玩家在整个游戏过程中执行的所有操作的总次数。
     * 这个统计数据将用于后端分析和玩家行为研究。
     * 
     * 📊 统计的操作类型:
     * - 读论文操作 (player.readPapers)
     * - 参加会议操作 (player.canAttendConf)
     * - 划水操作 (player.consecutiveSlackOff)
     * 
     * 🔗 与后端集成:
     * - 作为total_actions字段发送到后端
     * - 用于分析玩家的游戏活跃度
     * - 支持游戏平衡性调整
     * 
     * 📈 计算逻辑:
     * 总操作数 = 读论文次数 + 会议次数 + 划水次数
     * 
     * @returns number - 总操作次数
     */
    private _countTotalActions(): number {
        // 📊 获取游戏引擎的变量存储
        const variableStore = this._gameEngine.variableStore;
        
        // 🔢 计算总操作次数
        return (
            (variableStore.getVar('player.readPapers', false) || 0) +      // 📖 读论文次数
            (variableStore.getVar('player.canAttendConf', false) || 0) +   // 🎤 参加会议次数
            (variableStore.getVar('player.consecutiveSlackOff', false) || 0) // 😴 划水次数
        );
    }

    /**
     * 💼 统计工作相关操作次数
     * 
     * 计算玩家在整个游戏过程中执行的工作相关操作的总次数。
     * 这个统计数据将用于后端分析玩家的学习态度和工作效率。
     * 
     * 📊 统计的操作类型:
     * - 读论文操作 (player.readPapers) - 提升学术能力
     * - 参加会议操作 (player.canAttendConf) - 扩展学术视野
     * 
     * 🔗 与后端集成:
     * - 作为work_actions字段发送到后端
     * - 用于分析玩家的学习投入度
     * - 支持教育效果评估
     * 
     * 📈 计算逻辑:
     * 工作操作数 = 读论文次数 + 会议次数
     * 
     * 💡 业务意义:
     * - 反映玩家的学习积极性
     * - 用于计算工作效率指标
     * - 支持游戏平衡性调整
     * 
     * @returns number - 工作相关操作次数
     */
    private _countWorkActions(): number {
        // 📊 获取游戏引擎的变量存储
        const variableStore = this._gameEngine.variableStore;
        
        // 🔢 计算工作相关操作次数
        return (
            (variableStore.getVar('player.readPapers', false) || 0) +      // 📖 读论文次数
            (variableStore.getVar('player.canAttendConf', false) || 0)     // 🎤 参加会议次数
        );
    }
}

let appConfig: AppConfig = {};
let appConfigJson = document.getElementById('app_config')?.textContent;
if (appConfigJson) {
    appConfig = {...JSON.parse(appConfigJson)};
}
let parsedHash = queryString.parse(window.location.hash || '');
let seed = parsedHash['init_seed'];
if (typeof seed === 'string') {
    appConfig['initialRandomSeed'] = seed;
}

const app = new App(document.body, appConfig);
app.start().then(() => {
    console.log('App started successfully.');
});
