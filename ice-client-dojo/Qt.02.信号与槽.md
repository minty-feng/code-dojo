# Qt.02.信号与槽

信号与槽是Qt的核心机制，实现对象间松耦合通信。信号发射时自动调用连接的槽函数。

## 基本概念

**信号（Signal）：**事件发生时发射  
**槽（Slot）：**响应信号的函数  
**连接（Connect）：**建立信号和槽的关联

```cpp
connect(sender, SIGNAL(signalName()), receiver, SLOT(slotName()));
```

## 基本用法

### 连接信号和槽

```cpp
#include <QPushButton>
#include <QApplication>
#include <QDebug>

int main(int argc, char *argv[])
{
    QApplication app(argc, argv);
    
    QPushButton button("Click Me");
    
    // 连接clicked信号到quit槽
    QObject::connect(&button, &QPushButton::clicked,
                     &app, &QApplication::quit);
    
    button.show();
    return app.exec();
}
```

### 自定义信号和槽

```cpp
// myclass.h
#include <QObject>

class MyClass : public QObject
{
    Q_OBJECT  // 必须宏

public:
    explicit MyClass(QObject *parent = nullptr);

signals:
    void valueChanged(int newValue);  // 信号：只声明，不实现
    void statusUpdated(const QString &status);

public slots:
    void setValue(int value);  // 槽函数
    void reset();

private:
    int m_value;
};

// myclass.cpp
#include "myclass.h"

MyClass::MyClass(QObject *parent) : QObject(parent), m_value(0)
{
}

void MyClass::setValue(int value)
{
    if (m_value != value) {
        m_value = value;
        emit valueChanged(m_value);  // 发射信号
    }
}

void MyClass::reset()
{
    setValue(0);
    emit statusUpdated("Reset complete");
}
```

### 连接方式

```cpp
// 方式1：宏连接（Qt 4风格）
connect(sender, SIGNAL(valueChanged(int)),
        receiver, SLOT(onValueChanged(int)));

// 方式2：函数指针（Qt 5推荐）
connect(sender, &MyClass::valueChanged,
        receiver, &MyClass::onValueChanged);

// 方式3：Lambda表达式
connect(button, &QPushButton::clicked, [=]() {
    qDebug() << "Button clicked";
});

// 捕获变量
int counter = 0;
connect(button, &QPushButton::clicked, [&counter]() {
    counter++;
    qDebug() << "Clicked" << counter << "times";
});
```

### 断开连接

```cpp
// 断开特定连接
QMetaObject::Connection conn = connect(sender, &MyClass::valueChanged,
                                       receiver, &MyClass::onValueChanged);
disconnect(conn);

// 断开所有连接
disconnect(sender, nullptr, nullptr, nullptr);

// 断开特定信号
disconnect(sender, &MyClass::valueChanged, nullptr, nullptr);

// 断开到特定接收者
disconnect(sender, nullptr, receiver, nullptr);
```

## 信号槽特性

### 一对多

```cpp
// 一个信号连接多个槽
connect(button, &QPushButton::clicked, this, &MainWindow::onClicked1);
connect(button, &QPushButton::clicked, this, &MainWindow::onClicked2);
connect(button, &QPushButton::clicked, this, &MainWindow::onClicked3);

// 点击button，三个槽都会被调用
```

### 信号连接信号

```cpp
// 信号直接连接信号（转发）
connect(sender, &Sender::signalA, receiver, &Receiver::signalB);

// sender发射signalA时，receiver发射signalB
```

### 带参数的信号槽

```cpp
class Counter : public QObject
{
    Q_OBJECT

signals:
    void valueChanged(int newValue, int oldValue);

public slots:
    void setValue(int value) {
        int oldValue = m_value;
        m_value = value;
        emit valueChanged(value, oldValue);
    }

private:
    int m_value = 0;
};

// 连接
connect(counter, &Counter::valueChanged, [](int newVal, int oldVal) {
    qDebug() << "Changed from" << oldVal << "to" << newVal;
});
```

### 重载信号处理

```cpp
class MyWidget : public QWidget
{
    Q_OBJECT

signals:
    void customSignal();           // 无参数
    void customSignal(int value);  // 有参数（重载）

public:
    void test() {
        // Qt 5需要指定重载版本
        connect(this, qOverload<>(&MyWidget::customSignal),
                this, &MyWidget::onCustomSignal1);
        
        connect(this, qOverload<int>(&MyWidget::customSignal),
                this, &MyWidget::onCustomSignal2);
    }

private slots:
    void onCustomSignal1() {
        qDebug() << "No parameter";
    }
    
    void onCustomSignal2(int value) {
        qDebug() << "Value:" << value;
    }
};
```

## 连接类型

```cpp
// 自动连接（默认）
Qt::AutoConnection

// 直接连接（同步，同一线程立即调用）
connect(sender, &Sender::signal, receiver, &Receiver::slot,
        Qt::DirectConnection);

// 队列连接（异步，事件循环处理）
connect(sender, &Sender::signal, receiver, &Receiver::slot,
        Qt::QueuedConnection);

// 阻塞队列连接（等待槽执行完成）
connect(sender, &Sender::signal, receiver, &Receiver::slot,
        Qt::BlockingQueuedConnection);

// 唯一连接（防止重复连接）
connect(sender, &Sender::signal, receiver, &Receiver::slot,
        Qt::UniqueConnection);
```

## 跨线程通信

### 线程间信号槽

```cpp
#include <QThread>

class Worker : public QObject
{
    Q_OBJECT

public:
    Worker() {}

signals:
    void resultReady(const QString &result);

public slots:
    void doWork() {
        QString result = "Work done";
        emit resultReady(result);  // 发射信号
    }
};

// 主线程
QThread *thread = new QThread;
Worker *worker = new Worker;

worker->moveToThread(thread);  // 移动到工作线程

// 连接（自动使用QueuedConnection）
connect(thread, &QThread::started, worker, &Worker::doWork);
connect(worker, &Worker::resultReady, this, &MainWindow::handleResult);
connect(worker, &Worker::resultReady, thread, &QThread::quit);
connect(thread, &QThread::finished, worker, &QObject::deleteLater);
connect(thread, &QThread::finished, thread, &QObject::deleteLater);

thread->start();  // 启动线程
```

## 实战案例

### 按钮点击计数器

```cpp
class MainWindow : public QMainWindow
{
    Q_OBJECT

public:
    MainWindow(QWidget *parent = nullptr) : QMainWindow(parent), count(0)
    {
        QPushButton *button = new QPushButton("Click Me", this);
        QLabel *label = new QLabel("Count: 0", this);
        
        connect(button, &QPushButton::clicked, [=]() mutable {
            count++;
            label->setText(QString("Count: %1").arg(count));
        });
    }

private:
    int count;
};
```

### 定时器

```cpp
#include <QTimer>

QTimer *timer = new QTimer(this);

connect(timer, &QTimer::timeout, [=]() {
    qDebug() << "Timer fired";
});

timer->start(1000);  // 每1000ms触发一次

// 单次定时器
QTimer::singleShot(5000, [=]() {
    qDebug() << "5秒后执行";
});
```

### 进度对话框

```cpp
#include <QProgressDialog>
#include <QThread>

QProgressDialog *progress = new QProgressDialog("Processing...", "Cancel", 0, 100, this);
progress->setWindowModality(Qt::WindowModal);

QTimer *timer = new QTimer(this);
int value = 0;

connect(timer, &QTimer::timeout, [=]() mutable {
    value++;
    progress->setValue(value);
    if (value >= 100) {
        timer->stop();
    }
});

connect(progress, &QProgressDialog::canceled, timer, &QTimer::stop);

timer->start(50);
```

## 性能优化

### 避免不必要的连接

```cpp
// ❌ 重复连接
for (int i = 0; i < 100; i++) {
    connect(button, &QPushButton::clicked, this, &MainWindow::onClicked);
}
// 点击一次，槽被调用100次

// ✅ 使用UniqueConnection
connect(button, &QPushButton::clicked, this, &MainWindow::onClicked,
        Qt::UniqueConnection);
```

### 及时断开连接

```cpp
// ✓ 对象销毁时自动断开
class MyWidget : public QWidget {
    // 析构时自动断开所有连接
};

// ✓ 显式断开
disconnect(sender, &Sender::signal, this, &MyWidget::slot);
```

### 使用QObject父子关系

```cpp
// 父对象销毁时，子对象自动销毁
QPushButton *button = new QPushButton("Click", this);  // this是父对象
// 无需手动delete button
```

**核心：** 信号与槽实现松耦合对象通信，支持跨线程调用。Qt自动管理连接生命周期。

