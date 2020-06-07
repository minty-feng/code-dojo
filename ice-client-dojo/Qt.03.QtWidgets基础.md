# Qt.03.QtWidgets基础

QtWidgets提供桌面应用的UI控件，包括按钮、标签、输入框、布局等。

## 常用控件

### 按钮类

```cpp
// QPushButton：普通按钮
QPushButton *button = new QPushButton("Click Me", this);
connect(button, &QPushButton::clicked, [=]() {
    qDebug() << "Clicked";
});

// QCheckBox：复选框
QCheckBox *checkBox = new QCheckBox("Remember me", this);
connect(checkBox, &QCheckBox::stateChanged, [=](int state) {
    qDebug() << "Checked:" << (state == Qt::Checked);
});

// QRadioButton：单选按钮
QRadioButton *radio1 = new QRadioButton("Option 1", this);
QRadioButton *radio2 = new QRadioButton("Option 2", this);
radio1->setChecked(true);
```

### 输入控件

```cpp
// QLineEdit：单行输入
QLineEdit *lineEdit = new QLineEdit(this);
lineEdit->setPlaceholderText("Enter text...");
connect(lineEdit, &QLineEdit::textChanged, [=](const QString &text) {
    qDebug() << "Text:" << text;
});

// QTextEdit：多行文本
QTextEdit *textEdit = new QTextEdit(this);
textEdit->setPlainText("Multi-line\ntext");

// QComboBox：下拉框
QComboBox *comboBox = new QComboBox(this);
comboBox->addItems({"Option 1", "Option 2", "Option 3"});
connect(comboBox, QOverload<int>::of(&QComboBox::currentIndexChanged),
        [=](int index) {
            qDebug() << "Selected:" << comboBox->itemText(index);
        });

// QSpinBox：数字输入
QSpinBox *spinBox = new QSpinBox(this);
spinBox->setRange(0, 100);
spinBox->setValue(50);
```

### 显示控件

```cpp
// QLabel：标签
QLabel *label = new QLabel("Hello Qt", this);
label->setAlignment(Qt::AlignCenter);

// 显示图片
QLabel *imageLabel = new QLabel(this);
QPixmap pixmap("image.png");
imageLabel->setPixmap(pixmap.scaled(200, 200, Qt::KeepAspectRatio));

// QListWidget：列表
QListWidget *listWidget = new QListWidget(this);
listWidget->addItems({"Item 1", "Item 2", "Item 3"});

// QTableWidget：表格
QTableWidget *table = new QTableWidget(3, 2, this);  // 3行2列
table->setHorizontalHeaderLabels({"Name", "Age"});
table->setItem(0, 0, new QTableWidgetItem("Alice"));
table->setItem(0, 1, new QTableWidgetItem("25"));
```

## 布局管理

### 水平/垂直布局

```cpp
// QVBoxLayout：垂直布局
QVBoxLayout *vLayout = new QVBoxLayout;
vLayout->addWidget(new QPushButton("Button 1"));
vLayout->addWidget(new QPushButton("Button 2"));
vLayout->addWidget(new QPushButton("Button 3"));

QWidget *widget = new QWidget;
widget->setLayout(vLayout);

// QHBoxLayout：水平布局
QHBoxLayout *hLayout = new QHBoxLayout;
hLayout->addWidget(new QPushButton("Left"));
hLayout->addWidget(new QPushButton("Center"));
hLayout->addWidget(new QPushButton("Right"));

// 嵌套布局
QVBoxLayout *mainLayout = new QVBoxLayout;
mainLayout->addLayout(hLayout);
mainLayout->addWidget(new QTextEdit);
```

### 网格布局

```cpp
QGridLayout *gridLayout = new QGridLayout;

gridLayout->addWidget(new QLabel("Name:"), 0, 0);
gridLayout->addWidget(new QLineEdit, 0, 1);

gridLayout->addWidget(new QLabel("Age:"), 1, 0);
gridLayout->addWidget(new QSpinBox, 1, 1);

gridLayout->addWidget(new QPushButton("Submit"), 2, 0, 1, 2);  // 跨2列
```

### 表单布局

```cpp
QFormLayout *formLayout = new QFormLayout;

formLayout->addRow("Name:", new QLineEdit);
formLayout->addRow("Email:", new QLineEdit);
formLayout->addRow("Password:", new QLineEdit);
formLayout->addRow(new QPushButton("Register"));
```

## 对话框

### 消息框

```cpp
#include <QMessageBox>

// 信息框
QMessageBox::information(this, "Title", "Information message");

// 警告框
QMessageBox::warning(this, "Warning", "Warning message");

// 错误框
QMessageBox::critical(this, "Error", "Error message");

// 询问框
int ret = QMessageBox::question(this, "Question", "Are you sure?",
                                  QMessageBox::Yes | QMessageBox::No);
if (ret == QMessageBox::Yes) {
    // 用户点击Yes
}

// 自定义按钮
QMessageBox msgBox;
msgBox.setText("Do you want to save?");
msgBox.setStandardButtons(QMessageBox::Save | QMessageBox::Discard | QMessageBox::Cancel);
msgBox.setDefaultButton(QMessageBox::Save);
int ret = msgBox.exec();
```

### 文件对话框

```cpp
#include <QFileDialog>

// 打开文件
QString fileName = QFileDialog::getOpenFileName(this,
    "Open File",
    QDir::homePath(),
    "Text Files (*.txt);;All Files (*)");

if (!fileName.isEmpty()) {
    // 处理文件
}

// 保存文件
QString fileName = QFileDialog::getSaveFileName(this,
    "Save File",
    "untitled.txt",
    "Text Files (*.txt)");

// 选择目录
QString dir = QFileDialog::getExistingDirectory(this,
    "Select Directory",
    QDir::homePath());

// 多文件选择
QStringList files = QFileDialog::getOpenFileNames(this,
    "Select Files",
    QDir::homePath(),
    "Images (*.png *.jpg)");
```

## Model/View编程

### QListView + QStringListModel

```cpp
QStringListModel *model = new QStringListModel;
QStringList list;
list << "Item 1" << "Item 2" << "Item 3";
model->setStringList(list);

QListView *listView = new QListView;
listView->setModel(model);

// 添加项
list << "Item 4";
model->setStringList(list);

// 获取选中项
connect(listView->selectionModel(), &QItemSelectionModel::currentChanged,
        [=](const QModelIndex &current) {
            QString text = model->data(current, Qt::DisplayRole).toString();
            qDebug() << "Selected:" << text;
        });
```

### QTableView + QStandardItemModel

```cpp
QStandardItemModel *model = new QStandardItemModel(3, 2);  // 3行2列
model->setHorizontalHeaderLabels({"Name", "Age"});

model->setItem(0, 0, new QStandardItem("Alice"));
model->setItem(0, 1, new QStandardItem("25"));

QTableView *tableView = new QTableView;
tableView->setModel(model);
```

**核心：** QtWidgets提供丰富桌面控件，布局管理器自动调整UI，Model/View分离数据和界面。

