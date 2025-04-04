# Bitwarden 记录去重工具

这是一个简单的Python工具，用于对Bitwarden密码管理器导出的CSV文件进行去重处理。

## 功能特点

- 自动检测CSV文件编码
- 基于多个字段进行智能去重：type, name, login_uri, login_username, login_password
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

```bash
python bitwarden_deduplicator.py 输入文件.csv [-o 输出文件.csv]
```

### 参数说明

- `输入文件.csv`：必需，Bitwarden导出的CSV文件路径
- `-o, --output_file 输出文件.csv`：可选，指定输出文件的路径。如不指定，将在输入文件同目录下创建名为"原文件名_deduplicated.csv"的文件

### 示例

```bash
# 基本用法
python bitwarden_deduplicator.py bitwarden_export.csv

# 指定输出文件
python bitwarden_deduplicator.py bitwarden_export.csv -o cleaned_export.csv
```

## 注意事项

- 请确保CSV文件是Bitwarden标准导出格式
- 默认使用`utf-8-sig`编码保存输出文件，以确保与各种工具的兼容性

## 许可

本项目采用MIT许可证，详情请参阅LICENSE文件。
