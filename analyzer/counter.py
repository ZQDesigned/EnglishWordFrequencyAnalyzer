"""
词频统计器模块
负责统计词汇出现频率并提供排序、筛选等功能
"""

from collections import Counter
from typing import List, Dict, Tuple


class WordCounter:
    """词频统计器类"""

    def __init__(self):
        """初始化词频统计器"""
        self.word_counts = Counter()
        self.total_words = 0

    def count_words(self, words: List[str]) -> Counter:
        """
        统计词频
        
        Args:
            words (List[str]): 词汇列表
            
        Returns:
            Counter: 词频统计结果
        """
        if not words:
            return Counter()

        self.word_counts = Counter(words)
        self.total_words = len(words)

        return self.word_counts

    def get_most_common(self, n: int = 10) -> List[Tuple[str, int]]:
        """
        获取最常见的N个词汇
        
        Args:
            n (int): 返回的词汇数量，默认10个
            
        Returns:
            List[Tuple[str, int]]: 词汇及其频次的元组列表
        """
        return self.word_counts.most_common(n)

    def get_word_frequency(self, word: str) -> int:
        """
        获取指定词汇的出现次数
        
        Args:
            word (str): 目标词汇
            
        Returns:
            int: 出现次数
        """
        return self.word_counts.get(word.lower(), 0)

    def get_total_unique_words(self) -> int:
        """
        获取不重复词汇总数
        
        Returns:
            int: 不重复词汇数量
        """
        return len(self.word_counts)

    def get_total_words(self) -> int:
        """
        获取总词汇数（包含重复）
        
        Returns:
            int: 总词汇数
        """
        return self.total_words

    def filter_by_frequency(self, min_freq: int = 1, max_freq: int = None) -> Dict[str, int]:
        """
        按频率范围筛选词汇
        
        Args:
            min_freq (int): 最小出现次数，默认1
            max_freq (int, optional): 最大出现次数，无限制则为None
            
        Returns:
            Dict[str, int]: 筛选后的词频字典
        """
        filtered_words = {}

        for word, count in self.word_counts.items():
            if count >= min_freq:
                if max_freq is None or count <= max_freq:
                    filtered_words[word] = count

        return filtered_words

    def get_words_by_length(self, min_length: int = 1, max_length: int = None) -> Dict[str, int]:
        """
        按词汇长度筛选
        
        Args:
            min_length (int): 最小词汇长度，默认1
            max_length (int, optional): 最大词汇长度，无限制则为None
            
        Returns:
            Dict[str, int]: 筛选后的词频字典
        """
        filtered_words = {}

        for word, count in self.word_counts.items():
            word_len = len(word)
            if word_len >= min_length:
                if max_length is None or word_len <= max_length:
                    filtered_words[word] = count

        return filtered_words

    def get_statistics(self) -> Dict[str, any]:
        """
        获取统计概况
        
        Returns:
            Dict[str, any]: 包含各种统计信息的字典
        """
        if not self.word_counts:
            return {
                'total_words': 0,
                'unique_words': 0,
                'avg_frequency': 0,
                'max_frequency': 0,
                'min_frequency': 0,
                'most_common_word': None
            }

        frequencies = list(self.word_counts.values())
        most_common = self.word_counts.most_common(1)

        return {
            'total_words': self.total_words,
            'unique_words': len(self.word_counts),
            'avg_frequency': sum(frequencies) / len(frequencies),
            'max_frequency': max(frequencies),
            'min_frequency': min(frequencies),
            'most_common_word': most_common[0] if most_common else None
        }

    def to_dict(self) -> Dict[str, int]:
        """
        将词频统计结果转换为普通字典
        
        Returns:
            Dict[str, int]: 词频字典
        """
        return dict(self.word_counts)

    def merge_counts(self, other_counter: 'WordCounter'):
        """
        合并另一个词频统计器的结果
        
        Args:
            other_counter (WordCounter): 另一个词频统计器实例
        """
        if other_counter.word_counts:
            self.word_counts.update(other_counter.word_counts)
            self.total_words += other_counter.total_words

    def clear(self):
        """清空统计结果"""
        self.word_counts.clear()
        self.total_words = 0


def main():
    """测试函数"""
    # 测试词频统计功能
    test_words = [
        'python', 'data', 'analysis', 'python', 'machine', 'learning',
        'data', 'science', 'python', 'programming', 'data', 'analysis',
        'visualization', 'statistics', 'python', 'data'
    ]

    print("测试词汇列表:")
    print(test_words)
    print("\n" + "=" * 50 + "\n")

    # 创建词频统计器并统计
    counter = WordCounter()
    word_counts = counter.count_words(test_words)

    print("词频统计结果:")
    for word, count in word_counts.items():
        print(f"{word}: {count}")

    print(f"\n前5个高频词:")
    for word, count in counter.get_most_common(5):
        print(f"{word}: {count}")

    print(f"\n统计概况:")
    stats = counter.get_statistics()
    for key, value in stats.items():
        print(f"{key}: {value}")

    print(f"\n筛选频率>=2的词汇:")
    high_freq_words = counter.filter_by_frequency(min_freq=2)
    for word, count in high_freq_words.items():
        print(f"{word}: {count}")


if __name__ == "__main__":
    main()
