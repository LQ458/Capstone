#!/bin/bash

# 编译扩展报告脚本
# 包含所有三个游戏的分析

echo "=== 编译扩展游戏分析报告 ==="

# 检查是否安装了LaTeX
if ! command -v pdflatex &> /dev/null; then
    echo "错误: 未找到 pdflatex。请安装 LaTeX 发行版。"
    echo "macOS: brew install --cask mactex"
    echo "Ubuntu: sudo apt-get install texlive-full"
    exit 1
fi

# 生成可视化图表
echo "1. 生成可视化图表..."
python generate_all_visualizations.py

# 检查图表是否生成成功
if [ ! -f "comprehensive_game_comparison.png" ]; then
    echo "警告: 可视化图表生成可能失败，使用现有图表..."
fi

# 编译LaTeX报告
echo "2. 编译LaTeX报告..."
pdflatex -interaction=nonstopmode report_extended.tex

# 检查编译是否成功
if [ $? -eq 0 ]; then
    echo "3. 报告编译成功！"
    echo "生成的文件: report_extended.pdf"
    echo "输出文件位置: output/"
    
    # 清理临时文件
    echo "4. 清理临时文件..."
    rm -f *.aux *.log *.out *.toc *.fdb_latexmk *.fls *.synctex.gz
    
    echo "=== 编译完成 ==="
    echo "最终报告: report_extended.pdf"
else
    echo "错误: LaTeX编译失败。请检查错误信息。"
    exit 1
fi

# 显示文件大小
if [ -f "report_extended.pdf" ]; then
    echo "报告文件大小: $(du -h report_extended.pdf | cut -f1)"
fi

echo "=== 所有任务完成 ===" 