# WhileD 控制流图生成器 - 详细说明文档

## 目录

1. [项目概述](#项目概述)
2. [系统架构](#系统架构)
3. [核心模块说明](#核心模块说明)
4. [使用指南](#使用指南)
5. [实现原理](#实现原理)
6. [输出格式说明](#输出格式说明)
7. [常见问题](#常见问题)

---

## 项目概述

本项目实现了一个将 WhileD 语言的抽象语法树 (AST) 转换为控制流图 (CFG) 的编译器前端工具。主要功能包括：

- **表达式线性化**: 将嵌套表达式拆分为单操作指令序列
- **短路求值处理**: 将逻辑运算符 `&&` 和 `||` 转换为控制流
- **基本块构建**: 使用 Leader 算法识别和构建基本块
- **可视化输出**: 生成 Mermaid 格式的控制流图

### 支持的 WhileD 语言特性

**表达式 (Expressions)**:
- 整数常量 (`EConst`)
- 变量引用 (`EVar`)
- 二元运算 (`EBinop`): `+`, `-`, `*`, `/`, `%`, `<`, `<=`, `==`, `!=`, `>=`, `>`, `&&`, `||`
- 一元运算 (`EUnop`): `!`, `-`
- 指针解引用 (`EDeref`): `*e`
- 取址运算 (`EAddrOf`): `&e`

**语句 (Commands)**:
- 空语句 (`CSkip`): `skip`
- 变量赋值 (`CAsgnVar`): `x = e`
- 指针赋值 (`CAsgnDeref`): `*e1 = e2`
- 顺序组合 (`CSeq`): `c1; c2`
- 条件语句 (`CIf`): `if (cond) then c1 else c2`
- 循环语句 (`CWhile`): `while (cond) do body`

---

## 系统架构

### 文件结构

```
.
├── ast_definition.py      # AST 节点定义
├── ir_representation.py   # IR 指令和 CFG 结构
├── cfg_generator.py       # 核心转换逻辑
├── demo.py                # 演示程序
├── main.py                # 测试用例
├── README.md              # 项目简介和快速开始
├── DOCUMENTATION.md       # 详细说明文档（本文件）
├── TEST.md                # 测试说明文档
└── mermaid_outputs/       # 生成的流程图
    ├── demo/              # demo.py 生成的测试
    ├── main/              # main.py 生成的测试
    └── custom/            # 用户自定义测试
```

### 数据流

```
WhileD 程序 (AST)
    ↓
[阶段1: 表达式拆分]
    ↓
线性 IR (LABEL_ 标签)
    ↓
[阶段2: 基本块构建]
    ↓
基本块 IR (BB_ 标签)
    ↓
[阶段3: 控制流图]
    ↓
Mermaid 可视化
```

---

## 核心模块说明

### 1. `ast_definition.py`

定义 WhileD 语言的 AST 节点类。

**表达式节点**:
- `EConst(value: int)`: 整数常量
- `EVar(name: str)`: 变量引用
- `EBinop(op: str, left: Expr, right: Expr)`: 二元运算
- `EUnop(op: str, expr: Expr)`: 一元运算
- `EDeref(expr: Expr)`: 指针解引用
- `EAddrOf(expr: Expr)`: 取址运算

**语句节点**:
- `CSkip()`: 空语句
- `CAsgnVar(var: str, expr: Expr)`: 变量赋值
- `CAsgnDeref(addr: Expr, value: Expr)`: 指针赋值
- `CSeq(first: Com, second: Com)`: 顺序组合
- `CIf(cond: Expr, then_branch: Com, else_branch: Com)`: 条件语句
- `CWhile(cond: Expr, body: Com)`: 循环语句

### 2. `ir_representation.py`

定义中间表示 (IR) 指令和 CFG 结构。

**IR 指令类型**:
- `IRAssign(dest, source)`: 简单赋值
- `IRBinOp(dest, left, op, right)`: 二元运算
- `IRUnOp(dest, op, operand)`: 一元运算
- `IRDeref(dest, addr)`: 解引用加载
- `IRAddrOf(dest, var)`: 取址
- `IRStoreDeref(addr, value)`: 解引用存储
- `IRLabel(name)`: 标签标记
- `IRCondJump(cond, label)`: 条件跳转
- `IRJump(label)`: 无条件跳转

**CFG 结构**:
- `BasicBlock`: 基本块（包含指令、前驱、后继）
- `ControlFlowGraph`: 控制流图（包含基本块列表和 IR）

### 3. `cfg_generator.py`

核心转换逻辑，实现 AST 到 CFG 的转换。

**主要方法**:
- `flatten_expr(expr, dest=None)`: 表达式扁平化
- `flatten_shortcircuit(op, left, right, dest=None)`: 短路求值处理
- `process_statement(stmt)`: 语句处理（生成线性 IR）
- `build_cfg(instructions)`: 基本块构建（Leader 算法）
- `generate_cfg(program)`: 完整转换流程

---

## 使用指南

### 基本使用

```python
from ast_definition import *
from cfg_generator import CFGGenerator

# 1. 构建 AST
program = CWhile(
    EBinop("<", EVar("i"), EVar("n")),
    CAsgnVar("i", EBinop("+", EVar("i"), EConst(1)))
)

# 2. 生成 CFG
generator = CFGGenerator()
cfg = generator.generate_cfg(program)

# 3. 查看结果
cfg.print_linear_ir()      # 阶段1: 表达式拆分
cfg.print_blocks_structure() # 阶段2: 基本块
print(cfg.to_mermaid())     # 阶段3: Mermaid 流程图
```

### 命令行使用

```bash
# 运行演示
python demo.py

# 生成 Mermaid 文件（demo 测试用例）
python demo.py --generate

# 运行完整测试套件
python main.py

# 生成 Mermaid 文件（main 测试用例）
python main.py --generate
```

### 自定义测试

参考 `mermaid_outputs/custom/README.md` 和 `mermaid_outputs/custom/example_template.py` 创建自定义测试。

---

## 实现原理

### 表达式扁平化

将嵌套表达式转换为线性指令序列：

**简单表达式优化**:
- 如果表达式是常量或变量，直接使用
- 如果是一元/二元运算且操作数简单，生成单条指令
- 否则，递归拆分并引入临时变量

**示例**:
```python
# 输入: x = a + b + c
# 输出:
#   #0 = a + b
#   x = #0 + c
```

### 短路求值

将 `&&` 和 `||` 转换为控制流：

**`&&` 运算符**:
```
计算左操作数 -> result
if (!result) then jmp FALSE_LABEL
计算右操作数 -> result
jmp END_LABEL
FALSE_LABEL:
result = 左操作数（保留实际值）
END_LABEL:
```

**`||` 运算符**:
```
计算左操作数 -> result
if (result) then jmp TRUE_LABEL
计算右操作数 -> result
jmp END_LABEL
TRUE_LABEL:
result = 左操作数（保留实际值）
END_LABEL:
```

### Leader 算法

识别基本块的入口（Leader）：

1. **第一条指令**是 Leader
2. **跳转目标**是 Leader
3. **跳转后的指令**是 Leader

然后：
- 在 Leader 之间划分指令，形成基本块
- 根据跳转指令连接基本块，建立前驱/后继关系

### 控制流转换

**While 循环**:
```
START_LABEL:
  [条件求值]
  if (!cond) then jmp END_LABEL
  [循环体]
  jmp START_LABEL
END_LABEL:
```

**If-Else 分支**:
```
  [条件求值]
  if (!cond) then jmp ELSE_LABEL
  [then 分支]
  jmp END_LABEL
ELSE_LABEL:
  [else 分支]
END_LABEL:
```

---

## 输出格式说明

### 阶段1: 表达式拆分 (LABEL)

使用 `LABEL_` 前缀的标签：

```
LABEL_1:
    #0 = (i < n)
    if (! #0) then jmp LABEL_2
    i = i + 1
    jmp LABEL_1
LABEL_2:
```

### 阶段2: 基本块 (BB)

使用 `BB_` 前缀的标签：

```
BB_1:
    #0 = (i < n)
    if (! #0) then jmp BB_2
    i = i + 1
    jmp BB_1
BB_2:
```

### 阶段3: 控制流图 (Mermaid)

Mermaid 格式的流程图，包含：
- 基本块节点（矩形）
- 条件判断节点（菱形）
- 控制流边（带 true/false 标签）

查看方法：
- **VSCode**: 打开 `.md` 文件，点击预览图标
- **在线**: 访问 https://mermaid.live/，复制代码查看

---

## 常见问题

### Q: 为什么简单表达式不需要临时变量？

A: 为了优化 IR 代码，简单的一元/二元运算可以直接生成单条指令，避免不必要的临时变量。

### Q: 短路求值的结果值是什么？

A: 短路求值会保留左操作数的实际值。例如 `p && q`，如果 `p` 为假，结果是 `p` 的值（而不是 0）。

### Q: 如何查看生成的流程图？

A: 
1. 在 VSCode 中打开生成的 `.md` 文件，点击预览图标
2. 或访问 https://mermaid.live/，复制 Mermaid 代码查看

### Q: 可以处理数组吗？

A: 当前实现不支持数组语法，但可以通过指针运算模拟（如 `arr + i`）。

### Q: 如何添加自定义测试？

A: 参考 `mermaid_outputs/custom/README.md` 和 `example_template.py` 创建自定义测试脚本。

---

## 参考资料

- 项目 README: `README.md`
- 测试说明: `TEST.md`
- 自定义测试指南: `mermaid_outputs/custom/README.md`

