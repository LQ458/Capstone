# 项目结构说明

## 📁 目录结构

```
Capstone/
├── README.md                       # 项目说明文档
├── report_extended.tex             # 主要LaTeX报告（包含所有三个游戏）
├── compile_extended_report.sh      # 报告编译脚本
├── generate_all_visualizations.py  # 综合可视化生成脚本
├── create_simple_charts.py         # 简化图表生成（文本格式）
├── requirements.txt                # Python依赖
├── output/                         # 输出文件目录
│   ├── *.png                       # 所有生成的图片
│   └── *.json                      # 所有分析结果数据
└── games/                          # 游戏实现目录
    ├── README.md                   # 游戏说明
    ├── tic_tac_toe.py             # 井字棋实现
    ├── connect4.py                 # Connect4实现
    ├── Halving.py                  # Halving游戏实现
    ├── test.c                      # Connect4 C扩展
    ├── test.pyx                    # Cython接口
    ├── setup.py                    # 编译脚本
    ├── connect4/                   # Connect4分析模块
    │   ├── connect4_simulation.py  # 模拟代码
    │   └── connect4_visualization.py # 可视化代码
    └── halving/                    # Halving分析模块
        ├── halving_simulation.py   # 模拟代码
        └── halving_visualization.py # 可视化代码
```

## 🎯 核心文件说明

### 主要文档
- **README.md**: 完整的项目说明和使用指南
- **report_extended.tex**: 包含所有三个游戏分析的学术报告

### 脚本文件
- **compile_extended_report.sh**: 自动编译LaTeX报告
- **generate_all_visualizations.py**: 生成所有可视化图表
- **create_simple_charts.py**: 生成文本格式的分析图表

### 输出目录
- **output/**: 所有生成的图片和分析结果都保存在这里
  - PNG图片：可视化图表
  - JSON文件：分析数据

## 🚀 快速使用

### 1. 生成分析
```bash
# 生成文本格式分析
python create_simple_charts.py

# 生成可视化图表（需要matplotlib）
python generate_all_visualizations.py
```

### 2. 编译报告
```bash
# 编译LaTeX报告
./compile_extended_report.sh
```

### 3. 运行游戏
```bash
# 井字棋
python games/tic_tac_toe.py

# Connect4
python games/connect4.py

# Halving Game
python games/Halving.py
```

## 📊 输出文件

所有输出文件都保存在 `output/` 目录中：

### 图片文件
- `win_rates.png` - 胜率对比图
- `performance_metrics.png` - 性能指标图
- `move_distribution.png` - 移动分布图
- `comprehensive_game_comparison.png` - 综合游戏对比
- `algorithm_performance_analysis.png` - 算法性能分析
- `strategy_analysis.png` - 策略分析
- `summary_statistics.png` - 总结统计

### 数据文件
- `comprehensive_analysis_results.json` - 综合分析结果
- `simulation_results_*.json` - 模拟结果数据

## 🔧 技术特点

### 组织原则
1. **单一报告**: 只保留一个主要的LaTeX报告
2. **集中输出**: 所有输出文件统一放在output目录
3. **模块化设计**: 每个游戏有独立的分析模块
4. **清晰结构**: 易于理解和维护的项目结构

### 文件管理
- 删除了重复的文档文件
- 统一了输出路径
- 简化了项目结构
- 保持了功能的完整性

## 📝 注意事项

1. 所有图片和JSON文件都保存在 `output/` 目录中
2. 游戏文件夹中的可视化脚本使用相对路径 `../../output/` 访问输出目录
3. 主目录中的脚本直接使用 `output/` 路径
4. LaTeX报告中的图片路径已更新为 `output/` 目录 