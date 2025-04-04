# Flutter.01.桌面开发

Flutter是Google开发的跨平台UI框架，2018年发布。原生支持移动端，2021年起正式支持桌面平台（Windows/Linux/macOS）。

## Flutter简介

### 核心特性

- **单一代码库**：一套代码，6个平台（iOS/Android/Web/Windows/macOS/Linux）
- **热重载**：秒级刷新UI，提升开发效率
- **高性能**：自绘引擎（Skia），60fps流畅
- **响应式UI**：Widget树，声明式编程
- **Dart语言**：JIT开发，AOT发布

### 桌面平台支持

| 平台 | 稳定性 | 发布时间 |
|------|--------|----------|
| Windows | 稳定 | 2021-03 |
| macOS | 稳定 | 2021-03 |
| Linux | 稳定 | 2021-03 |

## 环境搭建

### 安装Flutter

```bash
# macOS/Linux
git clone https://github.com/flutter/flutter.git -b stable
export PATH="$PATH:`pwd`/flutter/bin"

# 或使用包管理器
# macOS
brew install flutter

# 验证
flutter doctor

# 启用桌面支持
flutter config --enable-windows-desktop
flutter config --enable-macos-desktop
flutter config --enable-linux-desktop

# 验证桌面支持
flutter devices
```

### 开发工具

**VS Code（推荐）：**
```bash
# 安装插件
- Flutter
- Dart

# 调试配置自动生成
```

**Android Studio：**
```bash
# 安装Flutter和Dart插件
Settings → Plugins → Flutter
```

### 创建桌面项目

```bash
# 创建项目
flutter create myapp

# 或指定平台
flutter create --platforms=windows,macos,linux myapp

cd myapp

# 运行（自动检测平台）
flutter run

# 指定设备
flutter run -d windows
flutter run -d macos
flutter run -d linux

# 构建
flutter build windows
flutter build macos
flutter build linux
```

## 项目结构

```
myapp/
├── lib/
│   └── main.dart        # 应用入口
├── windows/             # Windows平台代码
├── macos/              # macOS平台代码
├── linux/              # Linux平台代码
├── web/                # Web平台代码
├── android/            # Android平台代码
├── ios/                # iOS平台代码
├── test/               # 测试
├── pubspec.yaml        # 依赖配置
└── README.md
```

## Hello World

### main.dart

```dart
import 'package:flutter/material.dart';

void main() {
  runApp(const MyApp());
}

class MyApp extends StatelessWidget {
  const MyApp({Key? key}) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Flutter Desktop',
      theme: ThemeData(
        primarySwatch: Colors.blue,
      ),
      home: const MyHomePage(title: 'Flutter Desktop Demo'),
    );
  }
}

class MyHomePage extends StatefulWidget {
  const MyHomePage({Key? key, required this.title}) : super(key: key);

  final String title;

  @override
  State<MyHomePage> createState() => _MyHomePageState();
}

class _MyHomePageState extends State<MyHomePage> {
  int _counter = 0;

  void _incrementCounter() {
    setState(() {
      _counter++;
    });
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text(widget.title),
      ),
      body: Center(
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: <Widget>[
            const Text(
              'You have pushed the button this many times:',
            ),
            Text(
              '$_counter',
              style: Theme.of(context).textTheme.headlineMedium,
            ),
          ],
        ),
      ),
      floatingActionButton: FloatingActionButton(
        onPressed: _incrementCounter,
        tooltip: 'Increment',
        child: const Icon(Icons.add),
      ),
    );
  }
}
```

## Widget基础

### 常用Widget

```dart
// 文本
Text('Hello Flutter', style: TextStyle(fontSize: 24, color: Colors.blue))

// 按钮
ElevatedButton(
  onPressed: () { print('Clicked'); },
  child: Text('Click Me'),
)

TextButton(onPressed: () {}, child: Text('Text Button'))
IconButton(onPressed: () {}, icon: Icon(Icons.favorite))

// 输入框
TextField(
  decoration: InputDecoration(
    labelText: 'Username',
    hintText: 'Enter your name',
    border: OutlineInputBorder(),
  ),
  onChanged: (value) { print(value); },
)

// 容器
Container(
  width: 200,
  height: 100,
  padding: EdgeInsets.all(16),
  margin: EdgeInsets.symmetric(vertical: 8),
  decoration: BoxDecoration(
    color: Colors.blue,
    borderRadius: BorderRadius.circular(8),
  ),
  child: Text('Container'),
)

// 图片
Image.network('https://example.com/image.jpg')
Image.asset('assets/logo.png')

// 图标
Icon(Icons.home, size: 48, color: Colors.blue)

// 列表
ListView.builder(
  itemCount: items.length,
  itemBuilder: (context, index) {
    return ListTile(
      title: Text(items[index]),
    );
  },
)

// 网格
GridView.count(
  crossAxisCount: 2,
  children: List.generate(100, (index) {
    return Center(child: Text('Item $index'));
  }),
)
```

### 布局Widget

```dart
// 列布局
Column(
  mainAxisAlignment: MainAxisAlignment.center,
  crossAxisAlignment: CrossAxisAlignment.start,
  children: [
    Text('Item 1'),
    Text('Item 2'),
    Text('Item 3'),
  ],
)

// 行布局
Row(
  children: [
    Icon(Icons.star),
    Text('5.0'),
  ],
)

// 栈布局
Stack(
  children: [
    Image.asset('background.jpg'),
    Positioned(
      top: 16,
      left: 16,
      child: Text('Title'),
    ),
  ],
)

// 弹性布局
Expanded(
  flex: 2,
  child: Container(color: Colors.blue),
)

// 对齐
Center(child: Text('Centered'))
Align(
  alignment: Alignment.topRight,
  child: Icon(Icons.close),
)

// 间距
SizedBox(width: 16, height: 16)
Spacer()  // 占据剩余空间
Padding(
  padding: EdgeInsets.all(16),
  child: Text('Padded'),
)
```

## 状态管理

### StatefulWidget

```dart
class Counter extends StatefulWidget {
  @override
  State<Counter> createState() => _CounterState();
}

class _CounterState extends State<Counter> {
  int _count = 0;

  void _increment() {
    setState(() {
      _count++;  // setState触发重建
    });
  }

  @override
  Widget build(BuildContext context) {
    return Column(
      children: [
        Text('Count: $_count'),
        ElevatedButton(
          onPressed: _increment,
          child: Text('Increment'),
        ),
      ],
    );
  }
}
```

### Provider（推荐）

```dart
// pubspec.yaml
dependencies:
  provider: ^6.0.0

// 定义Model
class CounterModel extends ChangeNotifier {
  int _count = 0;
  
  int get count => _count;
  
  void increment() {
    _count++;
    notifyListeners();  // 通知更新
  }
}

// 提供Model
void main() {
  runApp(
    ChangeNotifierProvider(
      create: (context) => CounterModel(),
      child: MyApp(),
    ),
  );
}

// 消费Model
class CounterWidget extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    final counter = Provider.of<CounterModel>(context);
    
    return Column(
      children: [
        Text('Count: ${counter.count}'),
        ElevatedButton(
          onPressed: counter.increment,
          child: Text('Increment'),
        ),
      ],
    );
  }
}

// 或使用Consumer
Consumer<CounterModel>(
  builder: (context, counter, child) {
    return Text('${counter.count}');
  },
)
```

## 桌面特性

### 窗口管理

```dart
// pubspec.yaml
dependencies:
  window_manager: ^0.3.0

// main.dart
import 'package:window_manager/window_manager.dart';

void main() async {
  WidgetsFlutterBinding.ensureInitialized();
  
  await windowManager.ensureInitialized();
  
  WindowOptions windowOptions = WindowOptions(
    size: Size(800, 600),
    center: true,
    backgroundColor: Colors.transparent,
    skipTaskbar: false,
    titleBarStyle: TitleBarStyle.hidden,
  );
  
  windowManager.waitUntilReadyToShow(windowOptions, () async {
    await windowManager.show();
    await windowManager.focus();
  });
  
  runApp(MyApp());
}

// 控制窗口
await windowManager.setTitle('My App');
await windowManager.setSize(Size(1000, 700));
await windowManager.setMinimumSize(Size(600, 400));
await windowManager.setAlwaysOnTop(true);
await windowManager.setFullScreen(true);
```

### 系统托盘

```dart
// pubspec.yaml
dependencies:
  tray_manager: ^0.2.0

// 创建托盘
await trayManager.setIcon('assets/tray_icon.png');

Menu menu = Menu(
  items: [
    MenuItem(key: 'show', label: 'Show Window'),
    MenuItem.separator(),
    MenuItem(key: 'exit', label: 'Exit'),
  ],
);

await trayManager.setContextMenu(menu);

// 监听点击
trayManager.addListener(TrayListener());

class TrayListener extends TrayListener {
  @override
  void onTrayIconMouseDown() {
    windowManager.show();
  }
  
  @override
  void onTrayMenuItemClick(MenuItem menuItem) {
    if (menuItem.key == 'exit') {
      exit(0);
    }
  }
}
```

### 文件选择

```dart
// pubspec.yaml
dependencies:
  file_picker: ^5.0.0

import 'package:file_picker/file_picker.dart';

// 选择文件
FilePickerResult? result = await FilePicker.platform.pickFiles(
  type: FileType.custom,
  allowedExtensions: ['jpg', 'png', 'pdf'],
  allowMultiple: true,
);

if (result != null) {
  List<File> files = result.paths.map((path) => File(path!)).toList();
}

// 选择目录
String? directoryPath = await FilePicker.platform.getDirectoryPath();

// 保存文件
String? outputFile = await FilePicker.platform.saveFile(
  dialogTitle: 'Save file',
  fileName: 'output.txt',
);
```

### 本地存储

```dart
// pubspec.yaml
dependencies:
  shared_preferences: ^2.2.0

import 'package:shared_preferences/shared_preferences.dart';

// 存储
final prefs = await SharedPreferences.getInstance();
await prefs.setString('username', 'Alice');
await prefs.setInt('count', 10);
await prefs.setBool('isLoggedIn', true);

// 读取
String? username = prefs.getString('username');
int? count = prefs.getInt('count');
bool? isLoggedIn = prefs.getBool('isLoggedIn');

// 删除
await prefs.remove('username');
await prefs.clear();  // 清除所有
```

## 路由导航

### 基本路由

```dart
// 导航到新页面
Navigator.push(
  context,
  MaterialPageRoute(builder: (context) => SecondPage()),
);

// 返回
Navigator.pop(context);

// 传递参数
Navigator.push(
  context,
  MaterialPageRoute(
    builder: (context) => DetailPage(id: 123),
  ),
);

// 命名路由
MaterialApp(
  initialRoute: '/',
  routes: {
    '/': (context) => HomePage(),
    '/details': (context) => DetailsPage(),
    '/settings': (context) => SettingsPage(),
  },
);

// 使用命名路由
Navigator.pushNamed(context, '/details', arguments: {'id': 123});

// 接收参数
final args = ModalRoute.of(context)!.settings.arguments as Map;
```

## HTTP请求

```dart
// pubspec.yaml
dependencies:
  http: ^1.1.0

import 'package:http/http.dart' as http;
import 'dart:convert';

// GET请求
Future<List<User>> fetchUsers() async {
  final response = await http.get(
    Uri.parse('https://api.example.com/users'),
  );
  
  if (response.statusCode == 200) {
    List<dynamic> jsonData = jsonDecode(response.body);
    return jsonData.map((json) => User.fromJson(json)).toList();
  } else {
    throw Exception('Failed to load users');
  }
}

// POST请求
Future<User> createUser(String name, String email) async {
  final response = await http.post(
    Uri.parse('https://api.example.com/users'),
    headers: {'Content-Type': 'application/json'},
    body: jsonEncode({
      'name': name,
      'email': email,
    }),
  );
  
  if (response.statusCode == 201) {
    return User.fromJson(jsonDecode(response.body));
  } else {
    throw Exception('Failed to create user');
  }
}

// 使用
class _MyWidgetState extends State<MyWidget> {
  late Future<List<User>> futureUsers;

  @override
  void initState() {
    super.initState();
    futureUsers = fetchUsers();
  }

  @override
  Widget build(BuildContext context) {
    return FutureBuilder<List<User>>(
      future: futureUsers,
      builder: (context, snapshot) {
        if (snapshot.hasData) {
          return ListView.builder(
            itemCount: snapshot.data!.length,
            itemBuilder: (context, index) {
              return ListTile(
                title: Text(snapshot.data![index].name),
              );
            },
          );
        } else if (snapshot.hasError) {
          return Text('Error: ${snapshot.error}');
        }
        
        return CircularProgressIndicator();
      },
    );
  }
}
```

## 平台集成

### 调用原生代码（Method Channel）

```dart
// Dart侧
import 'package:flutter/services.dart';

class NativeBridge {
  static const platform = MethodChannel('com.example.app/native');

  Future<String> getPlatformVersion() async {
    try {
      final String version = await platform.invokeMethod('getPlatformVersion');
      return version;
    } on PlatformException catch (e) {
      return "Failed: '${e.message}'";
    }
  }
  
  Future<void> showNotification(String title, String message) async {
    await platform.invokeMethod('showNotification', {
      'title': title,
      'message': message,
    });
  }
}
```

**Windows（C++）：**
```cpp
// windows/runner/flutter_window.cpp
void FlutterWindow::RegisterMethodChannel() {
    auto channel = std::make_unique<flutter::MethodChannel<>>(
        flutter_controller_->engine()->messenger(),
        "com.example.app/native",
        &flutter::StandardMethodCodec::GetInstance()
    );

    channel->SetMethodCallHandler([](const auto& call, auto result) {
        if (call.method_name() == "getPlatformVersion") {
            result->Success("Windows 10");
        } else {
            result->NotImplemented();
        }
    });
}
```

**macOS（Swift）：**
```swift
// macos/Runner/AppDelegate.swift
let channel = FlutterMethodChannel(
    name: "com.example.app/native",
    binaryMessenger: controller.engine.binaryMessenger
)

channel.setMethodCallHandler { (call, result) in
    if call.method == "getPlatformVersion" {
        result("macOS " + ProcessInfo.processInfo.operatingSystemVersionString)
    } else {
        result(FlutterMethodNotImplemented)
    }
}
```

## 桌面UI适配

### 自适应布局

```dart
class ResponsiveLayout extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return LayoutBuilder(
      builder: (context, constraints) {
        if (constraints.maxWidth > 800) {
          // 桌面布局
          return Row(
            children: [
              NavigationRail(...),  // 侧边栏
              Expanded(child: MainContent()),
            ],
          );
        } else {
          // 移动布局
          return Column(
            children: [
              MainContent(),
              BottomNavigationBar(...),
            ],
          );
        }
      },
    );
  }
}
```

### 桌面风格

```dart
// Material Design（Android风格）
MaterialApp(...)

// Cupertino（iOS风格）
CupertinoApp(...)

// Fluent Design（Windows风格）
// pubspec.yaml: fluent_ui: ^4.0.0
FluentApp(
  theme: FluentThemeData(
    accentColor: Colors.blue,
    brightness: Brightness.light,
  ),
  home: NavigationView(
    pane: NavigationPane(
      items: [
        PaneItem(icon: Icon(FluentIcons.home), title: Text('Home')),
        PaneItem(icon: Icon(FluentIcons.settings), title: Text('Settings')),
      ],
    ),
  ),
)

// macOS风格
// pubspec.yaml: macos_ui: ^2.0.0
MacosApp(
  theme: MacosThemeData.light(),
  home: MacosWindow(
    sidebar: Sidebar(...),
    child: ContentArea(...),
  ),
)
```

## 打包发布

### Windows

```bash
flutter build windows --release

# 输出：build/windows/runner/Release/
# 包含：
# - myapp.exe
# - flutter_windows.dll
# - data/ 目录
```

### macOS

```bash
flutter build macos --release

# 输出：build/macos/Build/Products/Release/myapp.app

# 签名和公证
codesign --deep --force --verify --verbose --sign "Developer ID" myapp.app
```

### Linux

```bash
flutter build linux --release

# 输出：build/linux/x64/release/bundle/
# 打包为AppImage、snap或deb
```

## 常用插件

```yaml
dependencies:
  # 窗口管理
  window_manager: ^0.3.0
  
  # 托盘图标
  tray_manager: ^0.2.0
  
  # 文件选择
  file_picker: ^5.0.0
  
  # 本地存储
  shared_preferences: ^2.2.0
  
  # HTTP请求
  http: ^1.1.0
  dio: ^5.0.0
  
  # 状态管理
  provider: ^6.0.0
  riverpod: ^2.0.0
  
  # 数据库
  sqflite: ^2.2.0  # 移动端
  sqlite3: ^2.0.0  # 桌面端
  
  # 路径
  path_provider: ^2.0.0
  
  # URL启动
  url_launcher: ^6.1.0
```

**核心：** Flutter通过单一代码库实现跨平台开发，热重载提升效率，Widget树构建响应式UI，桌面支持日趋成熟。

