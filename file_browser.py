import os
from typing import List, Dict, Any
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("File Browser MCP", json_response=True)

CODE_FOLDER = "D:\\code"


@mcp.tool()
def list_directory(path: str = "") -> List[Dict[str, Any]]:
    """
    List contents of a directory under D:\\code.
    
    Args:
        path: Optional subpath relative to D:\\code. If empty, lists D:\\code itself.
        
    Returns:
        List of dictionaries with name, type (file/directory), and size (for files)
    """
    full_path = os.path.join(CODE_FOLDER, path) if path else CODE_FOLDER
    
    if not os.path.exists(full_path):
        return [{"error": f"Path does not exist: {full_path}"}]
    
    if not os.path.isdir(full_path):
        return [{"error": f"Path is not a directory: {full_path}"}]
    
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


@mcp.tool()
def read_file(file_path: str) -> str:
    """
    Read contents of a file under D:\\code.
    
    Args:
        file_path: Path to the file relative to D:\\code.
        
    Returns:
        File contents as string, or error message if file cannot be read.
    """
    full_path = os.path.join(CODE_FOLDER, file_path)
    
    if not os.path.exists(full_path):
        return f"Error: File does not exist: {full_path}"
    
    if not os.path.isfile(full_path):
        return f"Error: Path is not a file: {full_path}"
    
    try:
        with open(full_path, 'r', encoding='utf-8') as f:
            return f.read()
    except UnicodeDecodeError:
        try:
            with open(full_path, 'r', encoding='latin-1') as f:
                return f.read()
        except Exception as e:
            return f"Error reading file: {str(e)}"
    except Exception as e:
        return f"Error reading file: {str(e)}"


@mcp.tool()
def get_file_info(file_path: str) -> Dict[str, Any]:
    """
    Get detailed information about a file or directory under D:\\code.
    
    Args:
        file_path: Path to the file/directory relative to D:\\code.
        
    Returns:
        Dictionary with detailed information about the file/directory.
    """
    full_path = os.path.join(CODE_FOLDER, file_path)
    
    if not os.path.exists(full_path):
        return {"error": f"Path does not exist: {full_path}"}
    
    stat = os.stat(full_path)
    
    return {
        "name": os.path.basename(full_path),
        "full_path": full_path,
        "type": "directory" if os.path.isdir(full_path) else "file",
        "size": stat.st_size,
        "created": stat.st_ctime,
        "modified": stat.st_mtime,
        "accessed": stat.st_atime,
        "is_readable": os.access(full_path, os.R_OK),
        "is_writable": os.access(full_path, os.W_OK)
    }


if __name__ == "__main__":
    mcp.run(transport="stdio")
