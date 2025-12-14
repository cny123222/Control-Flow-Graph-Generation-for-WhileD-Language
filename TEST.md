# 测试说明文档

本文档详细说明 WhileD CFG 生成器的测试用例，包括测试目的、输入程序、预期输出和验证方法。

## 运行测试

```bash
# 运行所有测试用例
python main.py

# 生成 Mermaid 可视化文件（main.py 的 10 个测试用例）
python main.py --generate

# 运行演示程序（包含 2 个示例）
python demo.py

# 生成 Mermaid 可视化文件（demo.py 的 6 个测试用例）
python demo.py --generate
```

## 测试用例列表

### 测试 1：表达式拆分（Expression Splitting）

**目的**: 验证复杂表达式的线性化拆分

**输入**:
```python
x = a + b + c
```

**预期行为**:
- 将嵌套的二元运算拆分为多步
- 引入临时变量存储中间结果
- 最终将结果赋值给目标变量

**验证点**:
- ✅ 临时变量正确生成（`#0`, `#1` 等）
- ✅ 运算顺序正确（从左到右或按优先级）
- ✅ 最终结果正确赋值

---

### 测试 2：嵌套表达式（Nested Expressions）

**目的**: 验证多层嵌套表达式的处理

**输入**:
```python
result = (x + y) * (z - 10) < 100
```

**预期行为**:
- 先计算 `(x + y)`，结果存入临时变量
- 再计算 `(z - 10)`，结果存入临时变量
- 计算两个临时变量的乘积
- 最后与 100 比较

**验证点**:
- ✅ 嵌套结构正确展开
- ✅ 运算优先级正确处理
- ✅ 临时变量使用合理

---

### 测试 3：短路求值 AND（Short-circuit AND）

**目的**: 验证 `&&` 运算符的短路求值转换

**输入**:
```python
result = p && (*p != 0)
```

**预期行为**:
- 先计算 `p`，如果为假则直接跳转到 FALSE 分支
- 如果 `p` 为真，继续计算 `*p != 0`
- 保留左操作数的实际值（当 `p` 为假时，`result = p` 而不是 `result = 0`）

**验证点**:
- ✅ 条件跳转正确生成
- ✅ 短路逻辑正确（`p` 为假时不计算右操作数）
- ✅ 结果值正确（保留左操作数实际值）
- ✅ 标签和跳转指令正确

---

### 测试 4：短路求值 OR（Short-circuit OR）

**目的**: 验证 `||` 运算符的短路求值转换

**输入**:
```python
result = p || (*p != 0)
```

**预期行为**:
- 先计算 `p`，如果为真则直接跳转到 TRUE 分支
- 如果 `p` 为假，继续计算 `*p != 0`
- 保留左操作数的实际值

**验证点**:
- ✅ 条件跳转正确生成（与 AND 相反的逻辑）
- ✅ 短路逻辑正确（`p` 为真时不计算右操作数）
- ✅ 结果值正确

---

### 测试 5：While 循环（While Loop）

**目的**: 验证 `while` 循环的控制流转换

**输入**:
```python
while (i < n) do {
    s = s + i;
    i = i + 1
}
```

**预期行为**:
- 生成循环入口标签
- 条件判断转换为条件跳转
- 循环体后添加无条件跳转回入口
- 生成循环退出标签

**验证点**:
- ✅ 循环结构正确（标签、跳转）
- ✅ 条件判断正确
- ✅ 基本块划分正确（条件块、循环体块、退出块）
- ✅ CFG 边正确（循环回边）

---

### 测试 6：If-Else 分支（If-Else Branch）

**目的**: 验证 `if-else` 分支的控制流转换

**输入**:
```python
if (x > 0) then
    y = x
else
    y = -x
```

**预期行为**:
- 条件判断转换为条件跳转
- then 分支和 else 分支分别生成代码块
- 两个分支后都跳转到结束标签

**验证点**:
- ✅ 分支结构正确
- ✅ 条件跳转正确（跳转到 else 分支）
- ✅ 基本块划分正确（条件块、then 块、else 块、结束块）
- ✅ CFG 边正确（两个分支都指向结束块）

---

### 测试 7：指针操作（Pointer Operations）

**目的**: 验证指针相关操作（取址 `&` 和解引用 `*`）

**输入**:
```python
p = &x;
*p = 10
```

**预期行为**:
- `&x` 转换为 `IRAddrOf` 指令
- `*p = 10` 转换为 `IRStoreDeref` 指令
- 简单指针操作直接生成，不引入临时变量

**验证点**:
- ✅ 取址操作正确（`p = &x`）
- ✅ 解引用赋值正确（`*p = 10`）
- ✅ 指针操作 IR 指令正确

---

### 测试 8：复杂 While 循环（带短路求值）

**目的**: 验证循环中嵌套短路求值的处理

**输入**:
```python
while (i < n && arr[i] > 0) do {
    i = i + 1
}
```

**预期行为**:
- 循环条件包含短路求值
- 短路求值转换为条件跳转
- 循环结构正确

**验证点**:
- ✅ 短路求值在循环条件中正确处理
- ✅ 循环结构完整
- ✅ 控制流正确

---

### 测试 9：嵌套 If（Nested If）

**目的**: 验证嵌套的 `if` 语句处理

**输入**:
```python
if (x > 0) then
    if (y > 0) then
        z = 1
    else
        z = 2
else
    z = 0
```

**预期行为**:
- 外层 if-else 正确转换
- 内层 if-else 在外层 then 分支中正确转换
- 标签和跳转正确嵌套

**验证点**:
- ✅ 嵌套结构正确
- ✅ 标签不冲突
- ✅ 跳转目标正确
- ✅ 基本块划分合理

---

### 测试 10：综合测试（Comprehensive Test）

**目的**: 验证复杂程序（包含循环、分支、指针、短路求值）

**输入**:
```python
while (i < n) do {
    p = arr + i;
    if (*p > max) then
        max = *p
    else
        skip;
    i = i + 1
}
```

**预期行为**:
- 所有特性组合使用
- 控制流结构正确
- 表达式处理正确

**验证点**:
- ✅ 循环结构正确
- ✅ 分支结构正确
- ✅ 指针操作正确
- ✅ 表达式拆分正确
- ✅ CFG 结构完整（基本块、边、前驱/后继关系）

---

## 测试覆盖范围

### 功能覆盖

- ✅ **表达式处理**
  - 简单表达式（一元、二元运算）
  - 复杂嵌套表达式
  - 指针表达式（取址、解引用）

- ✅ **控制流结构**
  - `while` 循环
  - `if-else` 分支
  - 嵌套控制流

- ✅ **短路求值**
  - `&&` 运算符
  - `||` 运算符
  - 在控制流中的短路求值

- ✅ **指针操作**
  - 取址操作 `&`
  - 解引用读取 `*p`
  - 解引用赋值 `*p = value`

### 算法覆盖

- ✅ **Leader 算法**
  - Leader 识别正确
  - 基本块划分正确
  - 基本块连接正确

- ✅ **IR 生成**
  - 表达式线性化
  - 控制流转换
  - 标签和跳转生成

- ✅ **优化**
  - 简单表达式优化（不引入临时变量）
  - 短路求值优化（直接使用条件变量）

## 预期输出格式

每个测试用例的输出包含：

1. **阶段1：表达式拆分 (LABEL)**
   - 线性 IR 指令序列
   - 使用 `LABEL_N` 标签
   - 包含所有指令（赋值、运算、跳转）

2. **阶段2：基本块 (BB)**
   - 基本块列表
   - 使用 `BB_N` 标签
   - 基本块的前驱/后继关系

3. **CFG 结构信息**（部分测试）
   - 基本块 ID
   - 指令数量
   - 后继基本块列表
   - 前驱基本块列表

## 验证方法

1. **手动检查**: 查看输出的 IR 指令，验证逻辑正确性
2. **结构检查**: 验证基本块划分和连接关系
3. **可视化检查**: 使用 Mermaid 流程图验证控制流结构
4. **边界情况**: 测试空循环、空分支等特殊情况

## 已知限制

- 当前实现假设输入 AST 是有效的（不进行语法检查）
- 不支持函数调用（WhileD 语言特性）
- 不支持数组访问（仅支持指针运算）

## 测试结果

运行 `python main.py` 后，所有测试用例应全部通过，输出格式正确，CFG 结构完整。

---

## 自定义测试

### 创建自定义测试

#### 方法 1: 使用模板文件（推荐）

1. **复制模板文件到项目根目录**:
   ```bash
   cp mermaid_outputs/custom/example_template.py my_custom_test.py
   ```
   **注意**: 必须复制到项目根目录，因为需要导入项目模块

2. **编辑测试文件**:
   - 修改 `test_name`: 测试用例名称
   - 修改 `source`: 源程序文本（用于显示）
   - 修改 `program`: 构建 AST 节点

3. **在项目根目录运行测试**:
   ```bash
   python my_custom_test.py
   ```
   **重要**: 必须在项目根目录运行，不能在其他目录运行

4. **查看结果**:
   - 终端会显示生成的 IR 代码
   - Mermaid 文件保存在 `mermaid_outputs/custom/my_test.md`
   - 在 VSCode 中打开 `.md` 文件，点击预览图标查看流程图

#### 方法 2: 从头编写

在项目根目录创建新的 Python 文件，参考以下模板：

**注意**: 文件必须放在项目根目录，因为需要导入项目模块

```python
from ast_definition import *
from cfg_generator import CFGGenerator

# 1. 定义源程序（用于显示）
source = "x = a + b"

# 2. 构建 AST
program = CAsgnVar(
    "x",
    EBinop("+", EVar("a"), EVar("b"))
)

# 3. 生成 CFG
generator = CFGGenerator()
cfg = generator.generate_cfg(program)

# 4. 查看结果
print("源程序:", source)
print("\n阶段1: 表达式拆分 (LABEL)")
cfg.print_linear_ir()

print("\n阶段2: 基本块 (BB)")
cfg.print_blocks_structure()

print("\n阶段3: 控制流图 (Mermaid)")
print(cfg.to_mermaid())
```

### 执行自定义测试

#### 快速测试（仅终端输出）

```bash
python my_custom_test.py
```

输出包括：
- 生成的 IR 代码（阶段1和阶段2）
- Mermaid 流程图代码（阶段3）

#### 生成 Mermaid 文件

如果使用模板文件，运行后会自动生成 `.md` 文件。要手动生成，可以使用以下代码：

```python
def save_mermaid(name: str, source: str, program: Com, output_file: str):
    """生成并保存 Mermaid 流程图"""
    generator = CFGGenerator()
    cfg = generator.generate_cfg(program)
    
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(f"# {name}\n\n")
        f.write(f"**源程序**: `{source}`\n\n")
        
        f.write("## 阶段1：表达式拆分 (LABEL)\n\n")
        f.write("```\n")
        for instr in cfg.linear_ir:
            if hasattr(instr, 'name'):
                f.write(f"{instr.name}:\n")
            else:
                f.write(f"    {instr}\n")
        f.write("```\n\n")
        
        f.write("## 阶段2：基本块 (BB)\n\n")
        f.write("```\n")
        for instr in cfg.bb_ir:
            if hasattr(instr, 'name'):
                f.write(f"{instr.name}:\n")
            else:
                f.write(f"    {instr}\n")
        f.write("```\n\n")
        
        f.write("## 阶段3：控制流图\n\n")
        f.write("```mermaid\n")
        f.write(cfg.to_mermaid())
        f.write("\n```\n")
    
    print(f"✓ 已保存到 {output_file}")

# 使用示例
save_mermaid("我的测试", source, program, "mermaid_outputs/custom/my_test.md")
```

### 查看测试结果

#### 方法 1: VSCode 预览（推荐）

1. 在 VSCode 中打开生成的 `.md` 文件（如 `mermaid_outputs/custom/my_test.md`）
2. 点击右上角的预览图标（或按 `Cmd+Shift+V` / `Ctrl+Shift+V`）
3. 流程图会自动渲染显示

#### 方法 2: 在线查看

1. 访问 https://mermaid.live/
2. 打开生成的 `.md` 文件，复制 Mermaid 代码块（```mermaid ... ```）
3. 粘贴到在线编辑器中
4. 右侧会自动显示流程图

#### 方法 3: 终端查看 IR

运行测试脚本后，终端会直接显示：
- **阶段1**: 表达式拆分（LABEL 格式）
- **阶段2**: 基本块（BB 格式）
- **阶段3**: Mermaid 代码（可复制到在线查看器）

### 自定义测试示例

#### 示例 1: 简单赋值

```python
source = "y = x + 1"
program = CAsgnVar("y", EBinop("+", EVar("x"), EConst(1)))
```

#### 示例 2: While 循环

```python
source = "while (i < 10) do { i = i + 1 }"
program = CWhile(
    EBinop("<", EVar("i"), EConst(10)),
    CAsgnVar("i", EBinop("+", EVar("i"), EConst(1)))
)
```

#### 示例 3: If-Else 分支

```python
source = "if (x > 0) then y = x else y = -x"
program = CIf(
    EBinop(">", EVar("x"), EConst(0)),
    CAsgnVar("y", EVar("x")),
    CAsgnVar("y", EUnop("-", EVar("x")))
)
```

#### 示例 4: 短路求值

```python
source = "result = x != 0 && y > 10"
program = CAsgnVar(
    "result",
    EBinop("&&",
        EBinop("!=", EVar("x"), EConst(0)),
        EBinop(">", EVar("y"), EConst(10))
    )
)
```

#### 示例 5: 指针操作

```python
source = "p = &x; *p = 42"
program = CSeq(
    CAsgnVar("p", EAddrOf(EVar("x"))),
    CAsgnDeref(EVar("p"), EConst(42))
)
```

### 自定义测试目录

所有自定义测试的 Mermaid 文件应保存在 `mermaid_outputs/custom/` 目录下。

**文件命名建议**:
- 使用有意义的名称，如 `my_test.md`, `complex_loop.md`
- 避免与现有测试文件重名

**参考资源**:
- 详细指南: `mermaid_outputs/custom/README.md`
- 模板文件: `mermaid_outputs/custom/example_template.py`
- 示例测试: 查看 `mermaid_outputs/demo/` 和 `mermaid_outputs/main/` 目录

