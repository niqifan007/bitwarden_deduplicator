import pandas as pd
import argparse
import os
import chardet

def detect_encoding(file_path):
    """检测文件编码"""
    with open(file_path, 'rb') as f:
        raw_data = f.read(10000)  # 读取前10000个字节
        result = chardet.detect(raw_data)
    return result['encoding']

def deduplicate_bitwarden_csv(input_file, output_file=None):
    """
    对Bitwarden导出的CSV文件进行去重
    去重依据: type, name, login_uri, login_username, login_password
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
    
    # 基于指定字段去重
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

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='对Bitwarden导出的CSV文件进行去重')
    parser.add_argument('input_file', help='输入的CSV文件路径')
    parser.add_argument('-o', '--output_file', help='输出的CSV文件路径 (可选)')
    
    args = parser.parse_args()
    
    if not os.path.exists(args.input_file):
        print(f"错误: 输入文件 '{args.input_file}' 不存在")
    else:
        deduplicate_bitwarden_csv(args.input_file, args.output_file)
