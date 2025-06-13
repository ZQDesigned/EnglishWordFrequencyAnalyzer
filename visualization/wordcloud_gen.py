"""
词云生成器模块
负责生成词频统计的词云图
"""

import matplotlib.pyplot as plt
from wordcloud import WordCloud
from typing import Dict, Tuple, List
import numpy as np
from pathlib import Path


class WordCloudGenerator:
    """词云生成器类"""
    
    def __init__(self):
        """初始化词云生成器"""
        # 默认设置
        self.default_width = 800
        self.default_height = 600
        self.default_background_color = 'white'
        self.default_max_words = 100
        self.default_colormap = 'viridis'
        
    def create_wordcloud(self, word_counts: Dict[str, int],
                        title: str = "词频词云图",
                        width: int = None,
                        height: int = None,
                        background_color: str = None,
                        max_words: int = None,
                        colormap: str = None) -> Tuple[plt.Figure, WordCloud]:
        """
        创建词云图
        
        Args:
            word_counts (Dict[str, int]): 词频统计字典
            title (str): 图表标题
            width (int, optional): 词云宽度
            height (int, optional): 词云高度
            background_color (str, optional): 背景色
            max_words (int, optional): 最大词汇数
            colormap (str, optional): 颜色主题
            
        Returns:
            Tuple[plt.Figure, WordCloud]: matplotlib图形对象和词云对象
        """
        if not word_counts:
            raise ValueError("词频数据为空")
            
        # 设置默认参数
        if width is None:
            width = self.default_width
        if height is None:
            height = self.default_height
        if background_color is None:
            background_color = self.default_background_color
        if max_words is None:
            max_words = self.default_max_words
        if colormap is None:
            colormap = self.default_colormap
            
        # 创建词云对象
        wordcloud = WordCloud(
            width=width,
            height=height,
            background_color=background_color,
            max_words=max_words,
            colormap=colormap,
            relative_scaling=0.5,
            random_state=42
        ).generate_from_frequencies(word_counts)
        
        # 创建matplotlib图形
        fig, ax = plt.subplots(figsize=(12, 8))
        ax.imshow(wordcloud, interpolation='bilinear')
        ax.axis('off')
        ax.set_title(title, fontsize=16, fontweight='bold', pad=20)
        
        plt.tight_layout()
        
        return fig, wordcloud
    
    def create_custom_wordcloud(self, word_counts: Dict[str, int],
                               title: str = "自定义词云图",
                               font_path: str = None,
                               mask_image: np.ndarray = None,
                               **kwargs) -> Tuple[plt.Figure, WordCloud]:
        """
        创建自定义样式的词云图
        
        Args:
            word_counts (Dict[str, int]): 词频统计字典
            title (str): 图表标题
            font_path (str, optional): 自定义字体路径
            mask_image (np.ndarray, optional): 遮罩图像
            **kwargs: 其他WordCloud参数
            
        Returns:
            Tuple[plt.Figure, WordCloud]: matplotlib图形对象和词云对象
        """
        if not word_counts:
            raise ValueError("词频数据为空")
            
        # 设置WordCloud参数
        wordcloud_params = {
            'width': kwargs.get('width', self.default_width),
            'height': kwargs.get('height', self.default_height),
            'background_color': kwargs.get('background_color', self.default_background_color),
            'max_words': kwargs.get('max_words', self.default_max_words),
            'colormap': kwargs.get('colormap', self.default_colormap),
            'relative_scaling': kwargs.get('relative_scaling', 0.5),
            'random_state': kwargs.get('random_state', 42)
        }
        
        # 添加字体路径（如果提供）
        if font_path:
            wordcloud_params['font_path'] = font_path
            
        # 添加遮罩图像（如果提供）
        if mask_image is not None:
            wordcloud_params['mask'] = mask_image
            
        # 创建词云对象
        wordcloud = WordCloud(**wordcloud_params).generate_from_frequencies(word_counts)
        
        # 创建matplotlib图形
        fig, ax = plt.subplots(figsize=(12, 8))
        ax.imshow(wordcloud, interpolation='bilinear')
        ax.axis('off')
        ax.set_title(title, fontsize=16, fontweight='bold', pad=20)
        
        plt.tight_layout()
        
        return fig, wordcloud
    
    def save_wordcloud(self, wordcloud: WordCloud, filename: str) -> bool:
        """
        保存词云图到文件
        
        Args:
            wordcloud (WordCloud): 词云对象
            filename (str): 保存的文件名
            
        Returns:
            bool: 保存是否成功
        """
        try:
            wordcloud.to_file(filename)
            print(f"词云图已保存到: {filename}")
            return True
        except Exception as e:
            print(f"保存词云图失败: {e}")
            return False
    
    def save_figure(self, fig: plt.Figure, filename: str, dpi: int = 300) -> bool:
        """
        保存matplotlib图形到文件
        
        Args:
            fig (plt.Figure): matplotlib图形对象
            filename (str): 保存的文件名
            dpi (int): 图像分辨率，默认300
            
        Returns:
            bool: 保存是否成功
        """
        try:
            fig.savefig(filename, dpi=dpi, bbox_inches='tight', 
                       facecolor='white', edgecolor='none')
            print(f"词云图已保存到: {filename}")
            return True
        except Exception as e:
            print(f"保存词云图失败: {e}")
            return False
    
    def get_available_colormaps(self) -> List[str]:
        """
        获取可用的颜色主题列表
        
        Returns:
            List[str]: 颜色主题名称列表
        """
        return [
            'viridis', 'plasma', 'inferno', 'magma',
            'Blues', 'Greens', 'Oranges', 'Reds',
            'YlOrBr', 'YlOrRd', 'OrRd', 'PuRd',
            'RdPu', 'BuPu', 'GnBu', 'PuBu',
            'YlGnBu', 'PuBuGn', 'BuGn', 'YlGn'
        ]
    
    def show_wordcloud(self, fig: plt.Figure):
        """
        显示词云图
        
        Args:
            fig (plt.Figure): matplotlib图形对象
        """
        plt.show()


def main():
    """测试函数"""
    # 测试数据
    test_word_counts = {
        'python': 25,
        'data': 20,
        'analysis': 15,
        'machine': 12,
        'learning': 12,
        'science': 10,
        'programming': 8,
        'statistics': 6,
        'visualization': 5,
        'algorithm': 4,
        'computer': 3,
        'artificial': 3,
        'intelligence': 2,
        'neural': 2,
        'network': 2
    }
    
    generator = WordCloudGenerator()
    
    print("测试词云生成功能")
    print(f"测试数据: {test_word_counts}")
    print("\n" + "="*50 + "\n")
    
    # 测试基本词云
    fig1, wordcloud1 = generator.create_wordcloud(
        test_word_counts, 
        title="基础词云图",
        colormap='Blues'
    )
    success = generator.save_figure(fig1, 'test_output/basic_wordcloud.png')
    print(f"基础词云保存结果: {'成功' if success else '失败'}")
    
    # 测试自定义词云
    fig2, wordcloud2 = generator.create_custom_wordcloud(
        test_word_counts,
        title="自定义词云图",
        background_color='black',
        colormap='plasma',
        max_words=80
    )
    success = generator.save_figure(fig2, 'test_output/custom_wordcloud.png')
    print(f"自定义词云保存结果: {'成功' if success else '失败'}")
    
    # 显示可用颜色主题
    colormaps = generator.get_available_colormaps()
    print(f"\n可用的颜色主题: {colormaps[:5]}...等{len(colormaps)}种")
    
    # 关闭图形以释放内存
    plt.close(fig1)
    plt.close(fig2)


if __name__ == "__main__":
    main() 