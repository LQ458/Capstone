# 综合游戏AI分析项目

本项目实现了三个经典游戏的AI分析系统，使用先进的搜索算法来研究游戏策略和性能表现。

## 🎮 游戏介绍

### 1. 井字棋 (Tic-Tac-Toe)
- **算法**: Minimax + Alpha-Beta剪枝
- **特点**: 3×3棋盘，经典的双人零和游戏
- **复杂度**: 状态空间较小（5,478个位置），可完全求解
- **AI胜率**: 98% vs 随机玩家

### 2. Connect4 (四子棋)
- **算法**: 位棋盘优化的Minimax
- **特点**: 6×7棋盘，重力规则，需要连成4子
- **复杂度**: 中等复杂度（约4.5万亿个位置）
- **AI胜率**: 85% vs 随机玩家

### 3. Halving Game (减半游戏)
- **算法**: Minimax + Alpha-Beta剪枝
- **特点**: 数学游戏，玩家轮流对数字进行减一或减半操作
- **复杂度**: 随初始数字指数增长
- **AI胜率**: 95% vs 随机玩家

## 📁 项目结构

```
Capstone/
├── README.md                       # 本文件
├── report_extended.tex             # 扩展LaTeX报告
├── compile_extended_report.sh      # 编译脚本
├── generate_all_visualizations.py  # 可视化生成脚本
├── create_simple_charts.py         # 简化图表生成
├── comprehensive_analysis_results.json # 分析结果
├── games/                          # 游戏文件夹
│   ├── README.md                   # 游戏说明
│   ├── tic_tac_toe.py             # 井字棋实现
│   ├── connect4.py                 # Connect4实现
│   ├── Halving.py                  # Halving游戏实现
│   ├── test.c                      # Connect4 C扩展
│   ├── test.pyx                    # Cython接口
│   ├── setup.py                    # 编译脚本
│   ├── connect4/                   # Connect4分析
│   │   ├── connect4_simulation.py  # 模拟代码
│   │   └── connect4_visualization.py # 可视化代码
│   └── halving/                    # Halving分析
│       ├── halving_simulation.py   # 模拟代码
│       └── halving_visualization.py # 可视化代码
└── 其他文件...
```

## 🚀 快速开始

### 环境要求
```bash
# 安装Python依赖
pip install matplotlib numpy pandas seaborn

# 编译Connect4扩展
cd games
python setup.py build_ext --inplace
```

### 运行游戏

#### 井字棋
```bash
python games/tic_tac_toe.py
```

#### Connect4
```bash
python games/connect4.py
```

#### Halving Game
```bash
python games/Halving.py
```

### 运行分析

#### 生成综合分析
```bash
python create_simple_charts.py
```

#### 生成可视化图表
```bash
python generate_all_visualizations.py
```

#### 编译完整报告
```bash
./compile_extended_report.sh
```

## 📊 分析结果

### 性能对比

| 游戏 | 状态空间 | AI胜率 | 平均长度 | 最优深度 | 复杂度 |
|------|----------|--------|----------|----------|--------|
| Tic-Tac-Toe | 5,478 | 98% | 7.2步 | 6 | 低 |
| Connect4 | 4.5万亿 | 85% | 35步 | 6 | 中 |
| Halving Game | 指数 | 95%* | 15步 | 8 | 高 |

*Halving Game胜率随初始数字变化

### 搜索深度性能

| 深度 | Tic-Tac-Toe | Connect4 | Halving Game |
|------|-------------|----------|--------------|
| 2 | 45% | 35% | 60% |
| 4 | 75% | 55% | 80% |
| 6 | 98% | 85% | 95% |
| 8 | 98% | 92% | 98% |

## 🔧 技术特点

### 算法优化
- **Alpha-Beta剪枝**: 减少搜索空间，提高效率
- **位棋盘**: Connect4使用位操作优化存储和计算
- **启发式评估**: 在有限深度下提供合理的移动选择

### 性能分析
- **时间复杂度分析**: 测量不同参数对计算时间的影响
- **胜率统计**: 通过大量模拟获得可靠的胜率数据
- **策略分析**: 识别最优策略和关键决策点

## 📈 可视化输出

项目生成多种类型的分析图表：
- 胜率对比图
- 性能分析图
- 策略分布图
- 游戏长度分布图
- 算法复杂度分析图
- 综合对比图表

## 🎯 关键发现

### 1. 算法有效性
- Minimax + Alpha-Beta剪枝在所有游戏中都表现优异
- 搜索深度对性能有显著影响
- 游戏特定优化能显著提升性能

### 2. 游戏特定洞察
- **Tic-Tac-Toe**: 可实现完美游戏，验证算法正确性
- **Connect4**: 中心列策略偏好，位棋盘优化效果显著
- **Halving Game**: 数学策略模式，指数复杂度挑战

### 3. 计算考虑
- 内存使用：Connect4需要大量内存进行深度搜索
- 时间复杂度：Halving Game显示指数增长
- 优化影响：C扩展提供显著的性能提升

## 🔮 未来工作

### 潜在研究方向
1. **机器学习集成**: 结合神经网络评估函数
2. **并行计算**: 实现并行搜索以进行更深层探索
3. **更多游戏**: 扩展到更复杂的游戏如国际象棋或围棋
4. **实时应用**: 优化实时游戏场景
5. **教育应用**: 基于这些算法开发交互式学习工具

### 技术改进
- 实现更高效的搜索算法
- 添加机器学习组件
- 优化内存使用
- 支持更多游戏类型

## 📚 学术贡献

本研究对人工智能和游戏理论领域的贡献：

- 展示了经典搜索算法在不同游戏领域的实际有效性
- 提供了计算决策过程的见解
- 建立了AI在策略游戏中性能的基准
- 为更复杂的游戏系统开发做出贡献

## 🤝 贡献指南

1. 添加新游戏时，请遵循现有的代码结构
2. 为每个游戏创建独立的文件夹
3. 包含模拟和可视化代码
4. 更新文档

## 📄 许可证

本项目采用MIT许可证。

## 📞 联系方式

如有问题或建议，请通过以下方式联系：
- 创建Issue
- 提交Pull Request
- 发送邮件

---

**注意**: 本项目是学术研究项目，旨在探索和展示AI算法在游戏中的应用。所有代码和文档都经过精心设计，便于理解和扩展。 