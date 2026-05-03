import os
import sys

# 添加当前目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# 测试导入
try:
    from mcp.server.fastmcp import FastMCP
    print("MCP SDK 已成功导入")
except ImportError as e:
    print(f"导入错误: {e}")
    sys.exit(1)

# 我们的核心功能
CODE_FOLDER = "D:\\code"

def list_directory(path: str = ""):
    """列出目录内容"""
    full_path = os.path.join(CODE_FOLDER, path) if path else CODE_FOLDER
    
    if not os.path.exists(full_path):
        return [{"error": f"路径不存在: {full_path}"}]
    
    if not os.path.isdir(full_path):
        return [{"error": f"路径不是目录: {full_path}"}]
    
    contents = []
    for item in os.listdir(full_path):
        item_path = os.path.join(full_path, item)
        item_type = "directory" if os.path.isdir(item_path) else "file"
        size = os.path.getsize(item_path) if item_type == "file" else None
        
        contents.append({
            "name": item,
            "type": item_type,
            "size": size,
            "full_path": item_path
        })
    
    return contents

if __name__ == "__main__":
    print("=" * 60)
    print("查询 D:\\code 目录下的文件和文件夹")
    print("=" * 60)
    
    # 列出D:\code目录
    contents = list_directory()
    
    if contents and "error" in contents[0]:
        print(f"错误: {contents[0]['error']}")
    else:
        # 分别统计文件夹和文件
        directories = [item for item in contents if item["type"] == "directory"]
        files = [item for item in contents if item["type"] == "file"]
        
        print(f"\nD:\\code 目录下共有 {len(contents)} 个项目:")
        print(f"  - 文件夹: {len(directories)} 个")
        print(f"  - 文件: {len(files)} 个")
        
        # 显示文件夹
        if directories:
            print("\n文件夹列表:")
            for directory in directories:
                print(f"  [文件夹] {directory['name']}")
        
        # 显示文件
        if files:
            print("\n文件列表:")
            for file in files:
                size_str = f"{file['size']} 字节" if file['size'] else "未知大小"
                print(f"  [文件] {file['name']} ({size_str})")
        
        print("\n" + "=" * 60)
        print("查询完成！")
        print("=" * 60)
