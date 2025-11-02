"""
柱状图绘制器模块
负责生成词频统计的柱状图
"""

from typing import Dict, Tuple

import matplotlib.pyplot as plt


class BarPlotter:
    """柱状图绘制器类"""

    def __init__(self):
        """初始化柱状图绘制器"""
        # 设置中文字体支持（如果需要）
        plt.rcParams['font.sans-serif'] = ['Arial', 'DejaVu Sans', 'Liberation Sans']
        plt.rcParams['axes.unicode_minus'] = False

        # 默认样式设置
        self.default_figsize = (12, 8)
        self.default_color = 'skyblue'
        self.title_fontsize = 16
        self.label_fontsize = 12

    def create_bar_chart(self, word_counts: Dict[str, int],
                         title: str = "词频统计柱状图",
                         top_n: int = 20,
                         figsize: Tuple[int, int] = None,
                         color: str = None) -> plt.Figure:
        """
        创建基本的词频柱状图
        
        Args:
            word_counts (Dict[str, int]): 词频统计字典
            title (str): 图表标题
            top_n (int): 显示前N个高频词，默认20
            figsize (Tuple[int, int], optional): 图形尺寸
            color (str, optional): 柱状图颜色
            
        Returns:
            plt.Figure: matplotlib图形对象
        """
        if not word_counts:
            raise ValueError("词频数据为空")

        # 获取前N个高频词
        sorted_items = sorted(word_counts.items(), key=lambda x: x[1], reverse=True)
        top_words = sorted_items[:top_n]

        words = [item[0] for item in top_words]
        counts = [item[1] for item in top_words]

        # 设置图形参数
        if figsize is None:
            figsize = self.default_figsize
        if color is None:
            color = self.default_color

        # 创建图形
        fig, ax = plt.subplots(figsize=figsize)

        # 绘制柱状图
        bars = ax.bar(range(len(words)), counts, color=color, alpha=0.7)

        # 设置x轴标签
        ax.set_xticks(range(len(words)))
        ax.set_xticklabels(words, rotation=45, ha='right')

        # 设置标题和标签
        ax.set_title(title, fontsize=self.title_fontsize, fontweight='bold')
        ax.set_xlabel('词汇', fontsize=self.label_fontsize)
        ax.set_ylabel('出现次数', fontsize=self.label_fontsize)

        # 在柱子上显示数值
        for i, bar in enumerate(bars):
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width() / 2., height + 0.1,
                    f'{int(height)}', ha='center', va='bottom')

        # 调整布局
        plt.tight_layout()

        return fig

    def create_horizontal_bar_chart(self, word_counts: Dict[str, int],
                                    title: str = "词频统计水平柱状图",
                                    top_n: int = 15,
                                    figsize: Tuple[int, int] = None,
                                    color: str = None) -> plt.Figure:
        """
        创建水平柱状图
        
        Args:
            word_counts (Dict[str, int]): 词频统计字典
            title (str): 图表标题
            top_n (int): 显示前N个高频词，默认15
            figsize (Tuple[int, int], optional): 图形尺寸
            color (str, optional): 柱状图颜色
            
        Returns:
            plt.Figure: matplotlib图形对象
        """
        if not word_counts:
            raise ValueError("词频数据为空")

        # 获取前N个高频词
        sorted_items = sorted(word_counts.items(), key=lambda x: x[1], reverse=True)
        top_words = sorted_items[:top_n]

        words = [item[0] for item in top_words]
        counts = [item[1] for item in top_words]

        # 反转顺序，使最高频的词在顶部
        words.reverse()
        counts.reverse()

        # 设置图形参数
        if figsize is None:
            figsize = (10, max(6, len(words) * 0.4))
        if color is None:
            color = self.default_color

        # 创建图形
        fig, ax = plt.subplots(figsize=figsize)

        # 绘制水平柱状图
        bars = ax.barh(range(len(words)), counts, color=color, alpha=0.7)

        # 设置y轴标签
        ax.set_yticks(range(len(words)))
        ax.set_yticklabels(words)

        # 设置标题和标签
        ax.set_title(title, fontsize=self.title_fontsize, fontweight='bold')
        ax.set_xlabel('出现次数', fontsize=self.label_fontsize)
        ax.set_ylabel('词汇', fontsize=self.label_fontsize)

        # 在柱子上显示数值
        for i, bar in enumerate(bars):
            width = bar.get_width()
            ax.text(width + max(counts) * 0.01, bar.get_y() + bar.get_height() / 2.,
                    f'{int(width)}', ha='left', va='center')

        # 调整布局
        plt.tight_layout()

        return fig

    def save_chart(self, fig: plt.Figure, filename: str, dpi: int = 300) -> bool:
        """
        保存图表到文件
        
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
            print(f"图表已保存到: {filename}")
            return True
        except Exception as e:
            print(f"保存图表失败: {e}")
            return False

    def show_chart(self, fig: plt.Figure):
        """
        显示图表
        
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
        'artificial': 3
    }

    plotter = BarPlotter()

    print("测试柱状图绘制功能")
    print(f"测试数据: {test_word_counts}")
    print("\n" + "=" * 50 + "\n")

    # 测试垂直柱状图
    fig1 = plotter.create_bar_chart(test_word_counts, top_n=10)
    success = plotter.save_chart(fig1, 'test_output/vertical_bar_chart.png')
    print(f"垂直柱状图保存结果: {'成功' if success else '失败'}")

    # 测试水平柱状图
    fig2 = plotter.create_horizontal_bar_chart(test_word_counts, top_n=8)
    success = plotter.save_chart(fig2, 'test_output/horizontal_bar_chart.png')
    print(f"水平柱状图保存结果: {'成功' if success else '失败'}")

    # 关闭图形以释放内存
    plt.close(fig1)
    plt.close(fig2)


if __name__ == "__main__":
    main()
