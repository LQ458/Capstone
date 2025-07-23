# 游戏模拟项目

本项目包含多个经典游戏的AI实现和模拟分析，使用不同的搜索算法来研究游戏策略和性能表现。

## 项目结构

```
games/
├── README.md                    # 本文件
├── tic_tac_toe.py              # 井字棋游戏实现
├── connect4.py                  # Connect4游戏实现
├── Halving.py                   # Halving游戏实现
├── test.c                       # Connect4的C扩展
├── test.pyx                     # Connect4的Cython接口
├── setup.py                     # 编译脚本
├── test.cpython-313-darwin.so   # 编译后的扩展
├── connect4/                    # Connect4游戏文件夹
│   ├── connect4_simulation.py   # Connect4模拟代码
│   └── connect4_visualization.py # Connect4可视化代码
└── halving/                     # Halving游戏文件夹
    ├── halving_simulation.py    # Halving模拟代码
    └── halving_visualization.py # Halving可视化代码
```

## 游戏介绍

### 1. 井字棋 (Tic-Tac-Toe)
- **算法**: Minimax + Alpha-Beta剪枝
- **特点**: 3x3棋盘，经典的双人零和游戏
- **复杂度**: 状态空间较小，可完全求解

### 2. Connect4 (四子棋)
- **算法**: 位棋盘优化的Minimax
- **特点**: 6x7棋盘，重力规则，需要连成4子
- **复杂度**: 中等复杂度，使用C扩展优化性能

### 3. Halving Game (减半游戏)
- **算法**: Minimax + Alpha-Beta剪枝
- **特点**: 数学游戏，玩家轮流对数字进行减一或减半操作
- **复杂度**: 随初始数字指数增长

## 安装和运行

### 环境要求
```bash
pip install matplotlib numpy pandas seaborn
```

### 编译Connect4扩展
```bash
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

### 运行模拟分析

#### Connect4模拟
```bash
cd games/connect4
python connect4_simulation.py
python connect4_visualization.py
```

#### Halving模拟
```bash
cd games/halving
python halving_simulation.py
python halving_visualization.py
```

## 模拟功能

### Connect4模拟功能
1. **AI对战随机玩家**: 测试AI在不同搜索深度下的表现
2. **AI对战AI**: 比较不同深度AI的性能差异
3. **开局移动分析**: 分析AI的首步策略分布
4. **性能测试**: 测试搜索深度对计算时间和胜率的影响

### Halving模拟功能
1. **多数字测试**: 对不同初始数字进行策略分析
2. **获胜策略分析**: 识别关键决策点和最优策略
3. **性能缩放测试**: 分析算法复杂度随数字大小的变化
4. **策略比较**: 比较Minimax与随机策略的效果

## 可视化输出

每个游戏都会生成以下类型的图表：
- 胜率对比图
- 性能分析图
- 策略分布图
- 游戏长度分布图
- 算法复杂度分析图

## 技术特点

### 算法优化
- **Alpha-Beta剪枝**: 减少搜索空间，提高效率
- **位棋盘**: Connect4使用位操作优化存储和计算
- **启发式评估**: 在有限深度下提供合理的移动选择

### 性能分析
- **时间复杂度分析**: 测量不同参数对计算时间的影响
- **胜率统计**: 通过大量模拟获得可靠的胜率数据
- **策略分析**: 识别最优策略和关键决策点

## 扩展性

项目设计具有良好的扩展性：
- 可以轻松添加新的游戏
- 支持不同的搜索算法
- 模块化的模拟和可视化系统
- 标准化的数据输出格式

## 贡献指南

1. 添加新游戏时，请遵循现有的代码结构
2. 为每个游戏创建独立的文件夹
3. 包含模拟和可视化代码
4. 更新README文档

## 许可证

本项目采用MIT许可证。 