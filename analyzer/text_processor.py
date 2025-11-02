"""
文本处理器模块
负责文本清洗、分词、停用词过滤等预处理工作
"""

import re
from typing import List, Set

import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize


class TextProcessor:
    """文本处理器类"""

    def __init__(self, custom_stopwords_path: str = None):
        """
        初始化文本处理器
        
        Args:
            custom_stopwords_path (str, optional): 自定义停用词文件路径
        """
        self._ensure_nltk_data()
        self.stopwords_set = self._load_stopwords(custom_stopwords_path)

    def _ensure_nltk_data(self):
        """确保NLTK数据已下载"""
        try:
            nltk.data.find('tokenizers/punkt')
        except LookupError:
            print("下载NLTK punkt数据...")
            nltk.download('punkt')

        try:
            nltk.data.find('corpora/stopwords')
        except LookupError:
            print("下载NLTK stopwords数据...")
            nltk.download('stopwords')

    def _load_stopwords(self, custom_path: str = None) -> Set[str]:
        """
        加载停用词集合
        
        Args:
            custom_path (str, optional): 自定义停用词文件路径
            
        Returns:
            Set[str]: 停用词集合
        """
        # 获取NLTK默认英文停用词
        english_stopwords = set(stopwords.words('english'))

        # 如果提供了自定义停用词文件，则追加
        if custom_path and os.path.exists(custom_path):
            try:
                with open(custom_path, 'r', encoding='utf-8') as f:
                    custom_words = set(word.strip().lower() for word in f.readlines())
                    english_stopwords.update(custom_words)
                    print(f"已加载自定义停用词: {len(custom_words)} 个")
            except Exception as e:
                print(f"加载自定义停用词失败: {e}")

        return english_stopwords

    def clean_text(self, text: str) -> str:
        """
        清洗文本：转小写、去除标点符号和特殊字符
        
        Args:
            text (str): 原始文本
            
        Returns:
            str: 清洗后的文本
        """
        if not text:
            return ""

        # 转为小写
        text = text.lower()

        # 去除标点符号和特殊字符，只保留字母和空格
        text = re.sub(r'[^a-zA-Z\s]', ' ', text)

        # 去除多余的空格
        text = re.sub(r'\s+', ' ', text).strip()

        return text

    def tokenize(self, text: str) -> List[str]:
        """
        分词处理
        
        Args:
            text (str): 待分词的文本
            
        Returns:
            List[str]: 分词结果列表
        """
        if not text:
            return []

        try:
            tokens = word_tokenize(text)
            return tokens
        except Exception as e:
            print(f"分词失败: {e}")
            # 如果NLTK分词失败，使用简单的空格分割
            return text.split()

    def remove_stopwords(self, tokens: List[str]) -> List[str]:
        """
        去除停用词
        
        Args:
            tokens (List[str]): 词汇列表
            
        Returns:
            List[str]: 去除停用词后的词汇列表
        """
        if not tokens:
            return []

        # 去除停用词，同时过滤掉长度小于2的单词
        filtered_tokens = [
            token for token in tokens
            if token.lower() not in self.stopwords_set
               and len(token) >= 2
               and token.isalpha()  # 只保留纯字母单词
        ]

        return filtered_tokens

    def process_text(self, text: str) -> List[str]:
        """
        完整的文本处理流程
        
        Args:
            text (str): 原始文本
            
        Returns:
            List[str]: 处理后的词汇列表
        """
        # 1. 清洗文本
        cleaned_text = self.clean_text(text)

        # 2. 分词
        tokens = self.tokenize(cleaned_text)

        # 3. 去除停用词
        filtered_tokens = self.remove_stopwords(tokens)

        return filtered_tokens

    def get_stopwords_count(self) -> int:
        """
        获取停用词数量
        
        Returns:
            int: 停用词数量
        """
        return len(self.stopwords_set)

    def add_custom_stopwords(self, words: List[str]):
        """
        添加自定义停用词
        
        Args:
            words (List[str]): 要添加的停用词列表
        """
        for word in words:
            self.stopwords_set.add(word.lower().strip())


# 需要导入os模块
import os


def main():
    """测试函数"""
    processor = TextProcessor()

    # 测试文本
    test_text = """
    Hello World! This is a test document for analyzing word frequency.
    The quick brown fox jumps over the lazy dog. This sentence contains 
    various words that we want to analyze and count their frequency.
    Data analysis is important for understanding patterns in text data.
    """

    print("原始文本:")
    print(test_text)
    print("\n" + "=" * 50 + "\n")

    # 测试完整处理流程
    processed_tokens = processor.process_text(test_text)

    print("处理后的词汇列表:")
    print(processed_tokens)
    print(f"\n总词数: {len(processed_tokens)}")
    print(f"停用词数量: {processor.get_stopwords_count()}")


if __name__ == "__main__":
    main()
