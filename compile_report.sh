#!/bin/bash

echo "正在编译LaTeX报告..."

# 检查是否安装了pdflatex
if ! command -v pdflatex &> /dev/null; then
    echo "错误: 未找到pdflatex。请安装LaTeX发行版。"
    echo "macOS用户可以使用: brew install --cask mactex"
    echo "或者: brew install basictex"
    exit 1
fi

# 编译LaTeX文档
echo "第一次编译..."
pdflatex -interaction=nonstopmode report.tex

echo "第二次编译（处理引用）..."
pdflatex -interaction=nonstopmode report.tex

# 清理临时文件
echo "清理临时文件..."
rm -f *.aux *.log *.out *.toc *.fdb_latexmk *.fls *.synctex.gz

echo "编译完成！"
echo "生成的PDF文件: report.pdf"

# 检查PDF是否生成成功
if [ -f "report.pdf" ]; then
    echo "✓ 报告生成成功！"
    echo "文件大小: $(du -h report.pdf | cut -f1)"
else
    echo "✗ 报告生成失败，请检查LaTeX错误信息"
fi 