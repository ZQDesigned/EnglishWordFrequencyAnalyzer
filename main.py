"""
英文词频统计助手 - 主程序
PyQt5图形界面实现
"""

import os
import sys

from PyQt5.QtCore import QThread, pyqtSignal
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout,
                             QHBoxLayout, QPushButton, QLabel, QTextEdit,
                             QFileDialog, QLineEdit, QTableWidget,
                             QTableWidgetItem, QProgressBar, QMessageBox,
                             QTabWidget, QGroupBox, QGridLayout)

from analyzer.counter import WordCounter
# 导入自定义模块
from analyzer.file_loader import FileLoader
from analyzer.text_processor import TextProcessor
from exporter.csv_exporter import CSVExporter
from visualization.plot_bar import BarPlotter
from visualization.wordcloud_gen import WordCloudGenerator


class WorkerThread(QThread):
    """工作线程，用于处理耗时的文本分析任务"""

    # 定义信号
    progress_updated = pyqtSignal(int)
    status_updated = pyqtSignal(str)
    analysis_completed = pyqtSignal(dict, dict)  # 词频结果, 统计信息

    def __init__(self, directory_path, custom_stopwords_path=None):
        super().__init__()
        self.directory_path = directory_path
        self.custom_stopwords_path = custom_stopwords_path

    def run(self):
        """执行文本分析任务"""
        try:
            # 1. 加载文件
            self.status_updated.emit("正在加载文件...")
            self.progress_updated.emit(10)

            file_loader = FileLoader()
            files = file_loader.load_txt_files(self.directory_path)

            if not files:
                self.status_updated.emit("未找到txt文件")
                return

            self.progress_updated.emit(30)

            # 2. 处理文本
            self.status_updated.emit("正在处理文本...")
            text_processor = TextProcessor(self.custom_stopwords_path)
            all_content = file_loader.get_all_content()
            processed_words = text_processor.process_text(all_content)

            self.progress_updated.emit(60)

            # 3. 统计词频
            self.status_updated.emit("正在统计词频...")
            word_counter = WordCounter()
            word_counts = word_counter.count_words(processed_words)

            self.progress_updated.emit(80)

            # 4. 获取统计信息
            statistics = word_counter.get_statistics()
            statistics['file_count'] = file_loader.get_file_count()

            self.progress_updated.emit(100)
            self.status_updated.emit("分析完成")

            # 发送结果
            self.analysis_completed.emit(word_counter.to_dict(), statistics)

        except Exception as e:
            self.status_updated.emit(f"分析失败: {str(e)}")


class MainWindow(QMainWindow):
    """主窗口类"""

    def __init__(self):
        super().__init__()
        self.word_counts = {}
        self.statistics = {}
        self.init_ui()

    def init_ui(self):
        """初始化用户界面"""
        self.setWindowTitle("英文词频统计助手")
        self.setGeometry(100, 100, 1200, 800)

        # 创建中央窗口
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # 创建主布局
        main_layout = QVBoxLayout(central_widget)

        # 创建控制面板
        control_panel = self.create_control_panel()
        main_layout.addWidget(control_panel)

        # 创建选项卡
        self.tab_widget = QTabWidget()
        main_layout.addWidget(self.tab_widget)

        # 添加选项卡页面
        self.create_result_tab()
        self.create_statistics_tab()

        # 创建状态栏
        self.statusBar().showMessage("就绪")

    def create_control_panel(self):
        """创建控制面板"""
        group_box = QGroupBox("控制面板")
        layout = QGridLayout(group_box)

        # 文件夹选择
        layout.addWidget(QLabel("文本文件夹:"), 0, 0)
        self.directory_input = QLineEdit()
        self.directory_input.setPlaceholderText("选择包含txt文件的文件夹...")
        layout.addWidget(self.directory_input, 0, 1)

        self.browse_button = QPushButton("浏览")
        self.browse_button.clicked.connect(self.browse_directory)
        layout.addWidget(self.browse_button, 0, 2)

        # 自定义停用词文件
        layout.addWidget(QLabel("停用词文件 (可选):"), 1, 0)
        self.stopwords_input = QLineEdit()
        self.stopwords_input.setPlaceholderText("选择自定义停用词文件...")
        layout.addWidget(self.stopwords_input, 1, 1)

        self.browse_stopwords_button = QPushButton("浏览")
        self.browse_stopwords_button.clicked.connect(self.browse_stopwords)
        layout.addWidget(self.browse_stopwords_button, 1, 2)

        # 控制按钮
        button_layout = QHBoxLayout()

        self.analyze_button = QPushButton("开始分析")
        self.analyze_button.clicked.connect(self.start_analysis)
        button_layout.addWidget(self.analyze_button)

        self.export_button = QPushButton("导出CSV")
        self.export_button.clicked.connect(self.export_csv)
        self.export_button.setEnabled(False)
        button_layout.addWidget(self.export_button)

        self.plot_button = QPushButton("生成图表")
        self.plot_button.clicked.connect(self.show_plots)
        self.plot_button.setEnabled(False)
        button_layout.addWidget(self.plot_button)

        self.wordcloud_button = QPushButton("生成词云")
        self.wordcloud_button.clicked.connect(self.show_wordcloud)
        self.wordcloud_button.setEnabled(False)
        button_layout.addWidget(self.wordcloud_button)

        layout.addLayout(button_layout, 2, 0, 1, 3)

        # 进度条
        self.progress_bar = QProgressBar()
        layout.addWidget(self.progress_bar, 3, 0, 1, 3)

        return group_box

    def create_result_tab(self):
        """创建结果显示选项卡"""
        result_widget = QWidget()
        layout = QVBoxLayout(result_widget)

        # 词频表格
        self.result_table = QTableWidget()
        self.result_table.setColumnCount(3)
        self.result_table.setHorizontalHeaderLabels(["排名", "词汇", "频次"])
        layout.addWidget(self.result_table)

        self.tab_widget.addTab(result_widget, "词频结果")

    def create_statistics_tab(self):
        """创建统计信息选项卡"""
        stats_widget = QWidget()
        layout = QVBoxLayout(stats_widget)

        # 统计信息文本框
        self.stats_text = QTextEdit()
        self.stats_text.setReadOnly(True)
        layout.addWidget(self.stats_text)

        self.tab_widget.addTab(stats_widget, "统计信息")

    def browse_directory(self):
        """浏览文件夹"""
        directory = QFileDialog.getExistingDirectory(self, "选择包含txt文件的文件夹")
        if directory:
            self.directory_input.setText(directory)

    def browse_stopwords(self):
        """浏览停用词文件"""
        file_path, _ = QFileDialog.getOpenFileName(
            self, "选择停用词文件", "", "文本文件 (*.txt);;所有文件 (*)")
        if file_path:
            self.stopwords_input.setText(file_path)

    def start_analysis(self):
        """开始文本分析"""
        directory = self.directory_input.text().strip()
        if not directory:
            QMessageBox.warning(self, "警告", "请选择文本文件夹")
            return

        if not os.path.exists(directory):
            QMessageBox.warning(self, "警告", "选择的文件夹不存在")
            return

        # 禁用按钮
        self.analyze_button.setEnabled(False)
        self.progress_bar.setValue(0)

        # 创建工作线程
        stopwords_path = self.stopwords_input.text().strip() or None
        self.worker_thread = WorkerThread(directory, stopwords_path)

        # 连接信号
        self.worker_thread.progress_updated.connect(self.progress_bar.setValue)
        self.worker_thread.status_updated.connect(self.statusBar().showMessage)
        self.worker_thread.analysis_completed.connect(self.on_analysis_completed)

        # 启动线程
        self.worker_thread.start()

    def on_analysis_completed(self, word_counts, statistics):
        """分析完成的回调函数"""
        self.word_counts = word_counts
        self.statistics = statistics

        # 更新结果表格
        self.update_result_table()

        # 更新统计信息
        self.update_statistics()

        # 启用按钮
        self.analyze_button.setEnabled(True)
        self.export_button.setEnabled(True)
        self.plot_button.setEnabled(True)
        self.wordcloud_button.setEnabled(True)

    def update_result_table(self):
        """更新结果表格"""
        if not self.word_counts:
            return

        # 按频次排序
        sorted_items = sorted(self.word_counts.items(), key=lambda x: x[1], reverse=True)

        # 设置表格行数
        self.result_table.setRowCount(min(len(sorted_items), 100))  # 最多显示100行

        # 填充表格数据
        for i, (word, count) in enumerate(sorted_items[:100]):
            self.result_table.setItem(i, 0, QTableWidgetItem(str(i + 1)))
            self.result_table.setItem(i, 1, QTableWidgetItem(word))
            self.result_table.setItem(i, 2, QTableWidgetItem(str(count)))

        # 调整列宽
        self.result_table.resizeColumnsToContents()

    def update_statistics(self):
        """更新统计信息"""
        if not self.statistics:
            return

        stats_text = "=== 词频统计概况 ===\n\n"
        stats_text += f"处理文件数: {self.statistics.get('file_count', 0)}\n"
        stats_text += f"总词数: {self.statistics.get('total_words', 0)}\n"
        stats_text += f"不重复词数: {self.statistics.get('unique_words', 0)}\n"
        stats_text += f"平均词频: {self.statistics.get('avg_frequency', 0):.2f}\n"
        stats_text += f"最高词频: {self.statistics.get('max_frequency', 0)}\n"
        stats_text += f"最低词频: {self.statistics.get('min_frequency', 0)}\n"

        most_common = self.statistics.get('most_common_word')
        if most_common:
            stats_text += f"最高频词汇: {most_common[0]} ({most_common[1]}次)\n"

        self.stats_text.setText(stats_text)

    def export_csv(self):
        """导出CSV文件"""
        if not self.word_counts:
            QMessageBox.warning(self, "警告", "没有数据可导出")
            return

        # 选择保存位置
        file_path, _ = QFileDialog.getSaveFileName(
            self, "保存CSV文件", "word_frequency.csv", "CSV文件 (*.csv)")

        if file_path:
            try:
                exporter = CSVExporter()
                success = exporter.export_with_statistics(
                    self.word_counts,
                    file_path,
                    self.statistics.get('total_words', 0),
                    self.statistics.get('unique_words', 0)
                )

                if success:
                    QMessageBox.information(self, "成功", f"数据已导出到: {file_path}")
                else:
                    QMessageBox.warning(self, "失败", "导出CSV文件失败")

            except Exception as e:
                QMessageBox.critical(self, "错误", f"导出失败: {str(e)}")

    def show_plots(self):
        """显示柱状图"""
        if not self.word_counts:
            QMessageBox.warning(self, "警告", "没有数据可显示")
            return

        try:
            plotter = BarPlotter()

            # 生成垂直柱状图
            fig1 = plotter.create_bar_chart(
                self.word_counts,
                title="词频统计柱状图",
                top_n=20
            )
            plotter.show_chart(fig1)

            # 生成水平柱状图
            fig2 = plotter.create_horizontal_bar_chart(
                self.word_counts,
                title="词频统计水平柱状图",
                top_n=15
            )
            plotter.show_chart(fig2)

        except Exception as e:
            QMessageBox.critical(self, "错误", f"生成图表失败: {str(e)}")

    def show_wordcloud(self):
        """显示词云"""
        if not self.word_counts:
            QMessageBox.warning(self, "警告", "没有数据可显示")
            return

        try:
            generator = WordCloudGenerator()

            # 生成词云
            fig, wordcloud = generator.create_wordcloud(
                self.word_counts,
                title="词频词云图",
                colormap='viridis',
                max_words=100
            )
            generator.show_wordcloud(fig)

        except Exception as e:
            QMessageBox.critical(self, "错误", f"生成词云失败: {str(e)}")


def main():
    """主函数"""
    app = QApplication(sys.argv)

    # 设置应用程序信息
    app.setApplicationName("英文词频统计助手")
    app.setApplicationVersion("1.0")
    app.setOrganizationName("WordFrequency Analyzer")

    # 创建主窗口
    window = MainWindow()
    window.show()

    # 运行应用程序
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
