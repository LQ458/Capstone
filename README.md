# 井字棋 Minimax 算法分析与报告

这个项目实现了井字棋游戏的Minimax算法，并提供了完整的实验分析和LaTeX报告。

## 项目结构

```
final/
├── tic_tac_toe.py              # 井字棋游戏实现
├── generate_visualizations.py  # 数据可视化脚本
├── report.tex                  # LaTeX报告
├── requirements.txt            # Python依赖包
├── README.md                   # 项目说明
└── ESAP_Capstone_Assignment.pdf # 项目要求文档
```

## 功能特性

### 游戏实现
- ✅ 完整的井字棋游戏逻辑
- ✅ Minimax算法实现
- ✅ Alpha-Beta剪枝优化
- ✅ 人机对战模式
- ✅ AI对战模式
- ✅ 游戏状态验证

### 算法优化
- ✅ 深度考虑（偏好快速胜利）
- ✅ Alpha-Beta剪枝
- ✅ 特殊情况处理（首步优先选择中心）
- ✅ 高效的终端状态检测

### 数据分析
- ✅ 胜率统计
- ✅ 移动次数分析
- ✅ 决策时间测量
- ✅ 性能对比

## 安装和运行

### 1. 安装依赖

```bash
# 创建虚拟环境（推荐）
python3 -m venv venv
source venv/bin/activate  # macOS/Linux
# 或 venv\Scripts\activate  # Windows

# 安装依赖
pip install -r requirements.txt
```

### 2. 运行游戏

```bash
python tic_tac_toe.py
```

选择游戏模式：
- 1: 人机对战
- 2: AI对战

### 3. 生成数据可视化

```bash
# 生成图表
python create_charts.py

# 或者运行详细的数据分析
python simple_visualization.py
```

这将生成以下图表文件：
- `win_rates.png` - 胜率对比图表
- `move_distribution.png` - 移动次数分布
- `performance_metrics.png` - 性能指标图表

### 4. 编译LaTeX报告

```bash
# 编译PDF报告
./compile_report.sh

# 或者手动编译
pdflatex report.tex
pdflatex report.tex  # 第二次编译处理引用
```

## 算法实现细节

### Minimax算法

```python
def minimax(self, depth, is_maximizing, alpha=float('-inf'), beta=float('inf')):
    score = self.evaluate_board()
    
    if score == 10:
        return score - depth  # 偏好快速胜利
    if score == -10:
        return score + depth  # 偏好缓慢失败
    if len(self.get_available_moves()) == 0:
        return 0
    
    # 递归minimax与alpha-beta剪枝
    # ...
```

### 评估函数

- X胜利: +10
- O胜利: -10  
- 平局: 0
- 深度考虑: 偏好快速胜利和缓慢失败

### 人类对手模拟

```python
# 70%概率进行战略性移动，30%概率随机移动
if random.random() < 0.7 and len(moves) > 1:
    # 寻找阻止对手获胜的移动
    for move in moves:
        if is_blocking_move(move):
            return move
    return random.choice(moves)
else:
    return random.choice(moves)  # 30%随机移动
```

**模拟特点**:
- **战略意识 (70%)**: 尝试阻止对手获胜并做出智能移动
- **不完美游戏 (30%)**: 随机移动模拟人类错误或次优决策
- **阻止行为**: 优先选择阻止对手立即获胜的移动

## 实验结果

### 胜率表现
- Minimax vs Random: 96.7% (58/60 wins)
- Minimax vs Human: 92.0% (23/25 wins)
- Minimax vs Minimax: 0.0% (0/15 wins, 100% draws)

### 性能指标
- 平均决策时间: 0.001秒
- 最长决策时间: 0.004秒
- 平均游戏长度: 5.5-9.0步
- 总模拟游戏数: 100局

## 项目要求符合性检查

✅ **游戏选择**: 井字棋 - 确定性双人完美信息游戏
✅ **算法实现**: 完整的Minimax算法
✅ **优化技术**: Alpha-Beta剪枝
✅ **实验设计**: 多种对手类型测试
✅ **数据分析**: 胜率、移动次数、决策时间
✅ **可视化**: 多种图表类型
✅ **报告**: 完整的LaTeX报告

## 技术特点

1. **模块化设计**: 清晰的代码结构，易于扩展
2. **性能优化**: Alpha-Beta剪枝显著提升搜索效率
3. **用户体验**: 友好的命令行界面
4. **数据分析**: 全面的性能指标收集
5. **文档完整**: 详细的代码注释和报告

## 扩展建议

1. **更复杂游戏**: 扩展到四子棋、五子棋等
2. **机器学习**: 结合神经网络评估函数
3. **并行处理**: 实现并行搜索算法
4. **Web界面**: 开发图形化用户界面
5. **多语言支持**: 添加国际化支持

## 贡献

欢迎提交Issue和Pull Request来改进这个项目！

## 许可证

MIT License 