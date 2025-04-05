# Bitwarden 记录去重工具

这是一个简单的Python工具，用于对Bitwarden密码管理器导出的CSV文件进行去重处理。

## 功能特点

- 自动检测CSV文件编码
- 基于多个字段进行智能去重：type, name, login_uri, login_username, login_password
- **新增域名级别去重**：可选择仅使用域名部分（忽略路径）进行去重
- **交互式模式**：提供友好的交互界面，引导用户完成操作
- 保留原始数据的所有字段
- 提供命令行界面，简单易用

## 安装

```bash
# 克隆仓库
git clone https://github.com/niqifan007/bitwarden_deduplicator.git
cd bitwarden_deduplicator

# 安装依赖
pip install -r requirements.txt
```

## 使用方法

本工具提供两种运行模式：交互式模式和命令行模式。

### 交互式模式

```bash
# 直接启动交互式模式
python bitwarden_deduplicator.py

# 或者通过-i参数启动交互式模式
python bitwarden_deduplicator.py -i
```

在交互式模式下，程序会引导您：
1. 输入CSV文件路径
2. 设定输出文件名
3. 选择去重方式（标准模式或域名模式）
4. 确认设置并执行去重

### 命令行模式

```bash
python bitwarden_deduplicator.py 输入文件.csv [-o 输出文件.csv] [-d]
```

### 参数说明

- `输入文件.csv`：Bitwarden导出的CSV文件路径
- `-o, --output_file 输出文件.csv`：可选，指定输出文件的路径。如不指定，将在输入文件同目录下创建名为"原文件名_deduplicated.csv"的文件
- `-d, --domain_only`：可选，启用域名级别去重，忽略URL的路径部分
- `-i, --interactive`：可选，启动交互式模式

### 示例

```bash
# 基本用法
python bitwarden_deduplicator.py bitwarden_export.csv

# 指定输出文件
python bitwarden_deduplicator.py bitwarden_export.csv -o cleaned_export.csv

# 使用域名级别去重
python bitwarden_deduplicator.py bitwarden_export.csv -d

# 启动交互式模式
python bitwarden_deduplicator.py -i
```

## 注意事项

- 请确保CSV文件是Bitwarden标准导出格式
- 默认使用`utf-8-sig`编码保存输出文件，以确保与各种工具的兼容性
- 域名级别去重功能对于同一网站不同页面的记录特别有用，例如将`https://example.com/`和`https://example.com/login`视为相同网站
- 交互式模式适合不熟悉命令行的用户，提供了更友好的操作体验

## 许可

本项目采用MIT许可证，详情请参阅LICENSE文件。