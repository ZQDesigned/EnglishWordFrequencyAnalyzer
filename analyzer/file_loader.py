"""
文件加载器模块
负责读取指定目录下所有 .txt 文件的内容
"""

import os
from pathlib import Path
from typing import List, Dict


class FileLoader:
    """文件加载器类"""

    def __init__(self):
        self.loaded_files = {}  # 存储已加载的文件内容

    def load_txt_files(self, directory: str) -> Dict[str, str]:
        """
        加载指定目录下所有 .txt 文件
        
        Args:
            directory (str): 目标目录路径
            
        Returns:
            Dict[str, str]: 文件名与内容的字典映射
        """
        if not os.path.exists(directory):
            raise FileNotFoundError(f"目录不存在: {directory}")

        txt_files = {}
        directory_path = Path(directory)

        # 查找所有 .txt 文件
        for file_path in directory_path.glob("*.txt"):
            try:
                with open(file_path, 'r', encoding='utf-8') as file:
                    content = file.read()
                    txt_files[file_path.name] = content
                    print(f"成功加载文件: {file_path.name}")
            except UnicodeDecodeError:
                # 如果 UTF-8 解码失败，尝试其他编码
                try:
                    with open(file_path, 'r', encoding='gbk') as file:
                        content = file.read()
                        txt_files[file_path.name] = content
                        print(f"成功加载文件 (GBK编码): {file_path.name}")
                except Exception as e:
                    print(f"加载文件失败 {file_path.name}: {str(e)}")
            except Exception as e:
                print(f"加载文件失败 {file_path.name}: {str(e)}")

        self.loaded_files = txt_files
        return txt_files

    def get_all_content(self) -> str:
        """
        获取所有已加载文件的合并内容
        
        Returns:
            str: 合并后的文本内容
        """
        if not self.loaded_files:
            return ""

        all_content = []
        for filename, content in self.loaded_files.items():
            all_content.append(content)

        return "\n".join(all_content)

    def get_file_list(self) -> List[str]:
        """
        获取已加载的文件名列表
        
        Returns:
            List[str]: 文件名列表
        """
        return list(self.loaded_files.keys())

    def get_file_count(self) -> int:
        """
        获取已加载的文件数量
        
        Returns:
            int: 文件数量
        """
        return len(self.loaded_files)


def main():
    """测试函数"""
    loader = FileLoader()

    # 测试加载文件功能
    try:
        # 这里可以修改为实际的测试目录
        test_directory = "./test_texts"
        files = loader.load_txt_files(test_directory)

        print(f"总共加载了 {loader.get_file_count()} 个文件:")
        for filename in loader.get_file_list():
            print(f"  - {filename}")

        # 显示合并内容的前100个字符
        all_content = loader.get_all_content()
        print(f"\n合并内容预览: {all_content[:100]}...")

    except FileNotFoundError as e:
        print(f"错误: {e}")


if __name__ == "__main__":
    main()
