import pandas as pd
import argparse
import os
import chardet
import re
from urllib.parse import urlparse

def detect_encoding(file_path):
    """检测文件编码"""
    with open(file_path, 'rb') as f:
        raw_data = f.read()  # 读取整个文件以确保准确检测编码
        result = chardet.detect(raw_data)
    return result['encoding']

def deduplicate_bitwarden_csv(input_file, output_file=None, domain_only=False):
    """
    对Bitwarden导出的CSV文件进行去重
    去重依据: type, name, login_uri (可选择仅使用域名), login_username, login_password
    
    参数:
        input_file: 输入的CSV文件路径
        output_file: 输出的CSV文件路径 (可选)
        domain_only: 是否仅使用域名进行去重 (默认为False)
    """
    # 检测文件编码
    encoding = detect_encoding(input_file)
    print(f"检测到文件编码: {encoding}")
    
    # 读取CSV文件
    try:
        df = pd.read_csv(input_file, encoding=encoding)
        print(f"成功读取CSV文件，共有 {len(df)} 条记录")
    except Exception as e:
        print(f"读取文件时出错: {str(e)}")
        return
    
    # 检查必要的列是否存在
    required_columns = ['type', 'name', 'login_uri', 'login_username', 'login_password']
    missing_columns = [col for col in required_columns if col not in df.columns]
    
    if missing_columns:
        print(f"警告: CSV文件缺少以下列: {', '.join(missing_columns)}")
        print("请确保CSV文件是Bitwarden导出的标准格式")
        return
    
    # 记录去重前的数量
    before_count = len(df)
    
    # 如果选择了仅使用域名去重，则提取域名
    if domain_only:
        print("使用域名级别去重...")
        # 创建域名列
        df['domain'] = df['login_uri'].apply(extract_domain)
        print(f"提取了 {len(df['domain'].unique())} 个不同的域名")
        # 基于域名和其他字段去重
        df_deduplicated = df.drop_duplicates(subset=['type', 'name', 'domain', 'login_username', 'login_password'])
    else:
        # 使用完整URI去重
        df_deduplicated = df.drop_duplicates(subset=['type', 'name', 'login_uri', 'login_username', 'login_password'])
    
    # 记录去重后的数量
    after_count = len(df_deduplicated)
    removed_count = before_count - after_count
    
    print(f"去重前记录数: {before_count}")
    print(f"去重后记录数: {after_count}")
    print(f"移除了 {removed_count} 条重复记录")
    
    # 如果没有指定输出文件，则使用原文件名加上"_deduplicated"
    if output_file is None:
        file_name, file_ext = os.path.splitext(input_file)
        output_file = f"{file_name}_deduplicated{file_ext}"
    
    # 保存去重后的文件
    df_deduplicated.to_csv(output_file, index=False, encoding='utf-8-sig')
    print(f"去重后的文件已保存至: {output_file}")

def extract_domain(url):
    """从URL中提取域名"""
    if not url or pd.isna(url):
        return ''
    try:
        parsed_url = urlparse(url)
        domain = parsed_url.netloc
        # 如果没有域名但有路径，可能是相对URL，直接返回原始值
        if not domain and parsed_url.path:
            return url
        return domain
    except:
        return url

def display_banner():
    """显示程序横幅"""
    banner = """
    ┌─────────────────────────────────────────────────┐
    │                                                 │
    │       Bitwarden CSV 去重工具                    │
    │                                                 │
    └─────────────────────────────────────────────────┘
    """
    print(banner)

def interactive_mode():
    """交互式模式"""
    display_banner()
    print("欢迎使用 Bitwarden CSV 去重工具！")
    
    # 获取输入文件
    while True:
        input_file = input("\n请输入 Bitwarden CSV 文件路径 (输入 'q' 退出): ")
        if input_file.lower() == 'q':
            print("\n感谢使用，再见！")
            return
        
        # 检查文件是否存在
        if not os.path.exists(input_file):
            print(f"错误: 文件 '{input_file}' 不存在，请重新输入。")
            continue
        
        # 检查文件扩展名
        if not input_file.lower().endswith('.csv'):
            confirm = input(f"警告: 文件 '{input_file}' 可能不是CSV文件。是否继续？(y/n): ")
            if confirm.lower() != 'y':
                continue
        
        break
    
    # 询问输出文件
    default_output = os.path.splitext(input_file)[0] + "_deduplicated.csv"
    output_file = input(f"\n请输入输出文件路径 (直接回车使用默认值: '{default_output}'): ")
    if not output_file:
        output_file = default_output
    
    # 询问去重方式
    print("\n请选择去重方式:")
    print("1. 标准模式 - 使用完整URL地址去重")
    print("2. 域名模式 - 仅使用域名部分去重 (忽略路径)")
    
    while True:
        choice = input("请选择 (1/2): ")
        if choice in ['1', '2']:
            break
        print("无效的选择，请输入 1 或 2。")
    
    domain_only = (choice == '2')
    
    # 确认去重设置
    print("\n去重设置:")
    print(f"- 输入文件: {input_file}")
    print(f"- 输出文件: {output_file}")
    print(f"- 去重模式: {'域名模式 (仅使用域名)' if domain_only else '标准模式 (使用完整URL)'}")
    
    confirm = input("\n确认以上设置并开始去重? (y/n): ")
    if confirm.lower() == 'y':
        # 执行去重
        deduplicate_bitwarden_csv(input_file, output_file, domain_only)
        print("\n去重操作完成！")
        
        # 询问是否继续处理其他文件
        continue_choice = input("\n是否处理其他文件? (y/n): ")
        if continue_choice.lower() == 'y':
            interactive_mode()  # 递归调用自身继续处理
        else:
            print("\n感谢使用，再见！")
    else:
        print("\n操作已取消。")
        # 询问是否返回主菜单
        retry = input("是否重新设置? (y/n): ")
        if retry.lower() == 'y':
            interactive_mode()  # 递归调用自身重新开始
        else:
            print("\n感谢使用，再见！")

def command_line_mode():
    """命令行模式"""
    parser = argparse.ArgumentParser(description='对Bitwarden导出的CSV文件进行去重')
    parser.add_argument('input_file', nargs='?', help='输入的CSV文件路径')
    parser.add_argument('-o', '--output_file', help='输出的CSV文件路径 (可选)')
    parser.add_argument('-d', '--domain_only', action='store_true', help='仅使用域名进行去重，忽略路径部分')
    parser.add_argument('-i', '--interactive', action='store_true', help='使用交互式模式')
    
    args = parser.parse_args()
    
    # 如果指定了交互式模式或者没有提供输入文件，则使用交互式模式
    if args.interactive or not args.input_file:
        interactive_mode()
    else:
        # 命令行模式
        if not os.path.exists(args.input_file):
            print(f"错误: 输入文件 '{args.input_file}' 不存在")
        else:
            deduplicate_bitwarden_csv(args.input_file, args.output_file, args.domain_only)

if __name__ == "__main__":
    command_line_mode()
