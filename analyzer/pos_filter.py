"""
词性过滤器模块
提供词性分析和过滤功能的接口
当前暂未启用，但保留接口以便后续扩展
"""

from typing import List, Set

import nltk


class POSFilter:
    """词性过滤器类"""

    def __init__(self, enabled: bool = False):
        """
        初始化词性过滤器
        
        Args:
            enabled (bool): 是否启用词性过滤，默认为False
        """
        self.enabled = enabled
        self.allowed_pos_tags = set()

        if self.enabled:
            self._ensure_nltk_pos_data()

    def _ensure_nltk_pos_data(self):
        """确保NLTK词性标注数据已下载"""
        try:
            nltk.data.find('taggers/averaged_perceptron_tagger')
        except LookupError:
            print("下载NLTK词性标注数据...")
            nltk.download('averaged_perceptron_tagger')

    def set_allowed_pos_tags(self, pos_tags: List[str]):
        """
        设置允许的词性标签
        
        Args:
            pos_tags (List[str]): 允许的词性标签列表
                常见的词性标签包括：
                - NN, NNS, NNP, NNPS (名词)
                - VB, VBD, VBG, VBN, VBP, VBZ (动词)
                - JJ, JJR, JJS (形容词)
                - RB, RBR, RBS (副词)
        """
        self.allowed_pos_tags = set(pos_tags)

    def filter_by_pos(self, words: List[str]) -> List[str]:
        """
        根据词性过滤词汇
        
        Args:
            words (List[str]): 待过滤的词汇列表
            
        Returns:
            List[str]: 过滤后的词汇列表
        """
        # 如果未启用词性过滤，直接返回原词汇列表
        if not self.enabled or not self.allowed_pos_tags:
            return words

        if not words:
            return []

        try:
            # 使用NLTK进行词性标注
            pos_tagged = nltk.pos_tag(words)

            # 筛选符合指定词性的词汇
            filtered_words = [
                word for word, pos in pos_tagged
                if pos in self.allowed_pos_tags
            ]

            return filtered_words

        except Exception as e:
            print(f"词性过滤失败: {e}")
            # 如果词性标注失败，返回原词汇列表
            return words

    def get_pos_tags(self, words: List[str]) -> List[tuple]:
        """
        获取词汇的词性标签
        
        Args:
            words (List[str]): 词汇列表
            
        Returns:
            List[tuple]: (词汇, 词性标签) 的元组列表
        """
        if not self.enabled or not words:
            return [(word, 'N/A') for word in words]

        try:
            return nltk.pos_tag(words)
        except Exception as e:
            print(f"词性标注失败: {e}")
            return [(word, 'ERROR') for word in words]

    def enable_filter(self, pos_tags: List[str] = None):
        """
        启用词性过滤
        
        Args:
            pos_tags (List[str], optional): 允许的词性标签列表
        """
        self.enabled = True
        self._ensure_nltk_pos_data()

        if pos_tags:
            self.set_allowed_pos_tags(pos_tags)

    def disable_filter(self):
        """禁用词性过滤"""
        self.enabled = False
        self.allowed_pos_tags.clear()

    def is_enabled(self) -> bool:
        """
        检查词性过滤是否已启用
        
        Returns:
            bool: 是否启用
        """
        return self.enabled

    def get_allowed_pos_tags(self) -> Set[str]:
        """
        获取当前允许的词性标签
        
        Returns:
            Set[str]: 允许的词性标签集合
        """
        return self.allowed_pos_tags.copy()


def main():
    """测试函数"""
    # 测试词性过滤器（当前禁用状态）
    pos_filter = POSFilter(enabled=False)

    test_words = ['python', 'programming', 'language', 'data', 'analysis', 'beautiful', 'quickly']

    print("测试词汇:")
    print(test_words)
    print(f"\n词性过滤器状态: {'启用' if pos_filter.is_enabled() else '禁用'}")

    # 测试禁用状态下的过滤
    filtered_words = pos_filter.filter_by_pos(test_words)
    print(f"\n过滤后的词汇: {filtered_words}")

    # 如果要测试启用状态，可以取消下面的注释
    """
    print("\n" + "="*50)
    print("测试启用词性过滤器:")
    
    pos_filter.enable_filter(['NN', 'NNS', 'JJ'])  # 只保留名词和形容词
    print(f"词性过滤器状态: {'启用' if pos_filter.is_enabled() else '禁用'}")
    print(f"允许的词性标签: {pos_filter.get_allowed_pos_tags()}")
    
    # 获取词性标签
    pos_tags = pos_filter.get_pos_tags(test_words)
    print(f"\n词性标注结果:")
    for word, pos in pos_tags:
        print(f"{word}: {pos}")
    
    # 按词性过滤
    filtered_words = pos_filter.filter_by_pos(test_words)
    print(f"\n词性过滤后的词汇: {filtered_words}")
    """


if __name__ == "__main__":
    main()
