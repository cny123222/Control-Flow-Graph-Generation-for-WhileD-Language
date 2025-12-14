# 自定义测试用例指南

本目录用于存放您自己编写的测试用例生成的 Mermaid 流程图。

## 如何编写自定义测试

### 步骤 1: 创建测试脚本

创建一个新的 Python 文件，例如 `my_test.py`：

```python
from ast_definition import *
from ir_representation import *
from cfg_generator import CFGGenerator

# 1. 定义源程序（可选，仅用于显示）
source = "x = a + b"

# 2. 构建 AST
program = CAsgnVar(
    "x",
    EBinop("+", EVar("a"), EVar("b"))
)

# 3. 生成 CFG
generator = CFGGenerator()
cfg = generator.generate_cfg(program)

# 4. 打印结果
print("源程序:", source)
print("\n生成的 IR:")
print(cfg)

# 5. 生成 Mermaid 流程图（可选）
print("\nMermaid 流程图:")
print(cfg.to_mermaid())
```

### 步骤 2: 生成 Mermaid 文件（推荐）

要生成完整的 Mermaid 文件（包含流程图和 IR），可以使用以下模板：

```python
from ast_definition import *
from ir_representation import *
from cfg_generator import CFGGenerator

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
source = "x = a + b"
program = CAsgnVar("x", EBinop("+", EVar("a"), EVar("b")))
save_mermaid("我的测试", source, program, "mermaid_outputs/custom/my_test.md")
```

### 步骤 3: 运行测试

```bash
python my_test.py
```

生成的 `.md` 文件可以：
1. 直接查看（包含 IR 文本）
2. 复制 Mermaid 代码块到 https://mermaid.live/ 查看流程图

## AST 节点类型参考

### 表达式（Expression）

- **常量**: `EConst(5)` - 整数常量
- **变量**: `EVar("x")` - 变量引用
- **二元运算**: `EBinop("+", left, right)` 
  - 运算符: `+`, `-`, `*`, `/`, `%`, `<`, `<=`, `==`, `!=`, `>=`, `>`, `&&`, `||`
- **一元运算**: `EUnop("-", expr)` 或 `EUnop("!", expr)`
- **解引用**: `EDeref(expr)` - `*expr`
- **取址**: `EAddrOf(EVar("x"))` - `&x`（只能取变量的地址）

### 语句（Command）

- **空语句**: `CSkip()` - `skip`
- **变量赋值**: `CAsgnVar("x", expr)` - `x = expr`
- **指针赋值**: `CAsgnDeref(addr_expr, value_expr)` - `*addr = value`
- **顺序执行**: `CSeq(stmt1, stmt2)` - `stmt1; stmt2`
- **条件语句**: `CIf(cond, then_branch, else_branch)` - `if (cond) then then_branch else else_branch`
- **循环语句**: `CWhile(cond, body)` - `while (cond) do body`

## 完整示例

### 示例 1: 简单赋值

```python
from ast_definition import *
from cfg_generator import CFGGenerator

source = "y = x + 1"
program = CAsgnVar("y", EBinop("+", EVar("x"), EConst(1)))

generator = CFGGenerator()
cfg = generator.generate_cfg(program)
print(cfg.to_mermaid())
```

### 示例 2: While 循环

```python
source = "while (i < 10) do { i = i + 1 }"
program = CWhile(
    EBinop("<", EVar("i"), EConst(10)),
    CAsgnVar("i", EBinop("+", EVar("i"), EConst(1)))
)

generator = CFGGenerator()
cfg = generator.generate_cfg(program)
print(cfg.to_mermaid())
```

### 示例 3: If-Else 分支

```python
source = "if (x > 0) then y = x else y = -x"
program = CIf(
    EBinop(">", EVar("x"), EConst(0)),
    CAsgnVar("y", EVar("x")),
    CAsgnVar("y", EUnop("-", EVar("x")))
)

generator = CFGGenerator()
cfg = generator.generate_cfg(program)
print(cfg.to_mermaid())
```

### 示例 4: 短路求值

```python
source = "result = x != 0 && y > 10"
program = CAsgnVar(
    "result",
    EBinop("&&",
        EBinop("!=", EVar("x"), EConst(0)),
        EBinop(">", EVar("y"), EConst(10))
    )
)

generator = CFGGenerator()
cfg = generator.generate_cfg(program)
print(cfg.to_mermaid())
```

### 示例 5: 指针操作

```python
source = "p = &x; *p = 42"
program = CSeq(
    CAsgnVar("p", EAddrOf(EVar("x"))),
    CAsgnDeref(EVar("p"), EConst(42))
)

generator = CFGGenerator()
cfg = generator.generate_cfg(program)
print(cfg.to_mermaid())
```

### 示例 6: 复杂嵌套

```python
source = "sum = 0; while (i < n) do { sum = sum + i; i = i + 1 }"
program = CSeq(
    CAsgnVar("sum", EConst(0)),
    CWhile(
        EBinop("<", EVar("i"), EVar("n")),
        CSeq(
            CAsgnVar("sum", EBinop("+", EVar("sum"), EVar("i"))),
            CAsgnVar("i", EBinop("+", EVar("i"), EConst(1)))
        )
    )
)

generator = CFGGenerator()
cfg = generator.generate_cfg(program)
print(cfg.to_mermaid())
```

## 查看流程图

### 方法 1: VSCode 预览（推荐）

1. 在 VSCode 中打开生成的 `.md` 文件
2. 点击右上角的预览图标（或按 `Cmd+Shift+V` / `Ctrl+Shift+V`）
3. 流程图会自动渲染显示

### 方法 2: 在线查看

1. 访问 https://mermaid.live/
2. 复制生成的 Mermaid 代码块（```mermaid ... ```）到编辑器
3. 右侧会自动显示流程图

## 提示

- 生成的 Mermaid 文件保存在 `mermaid_outputs/custom/` 目录
- 文件名建议使用有意义的名称，如 `my_test.md`
- 可以在文件中包含源程序说明和测试目的
- 参考 `demo/` 和 `main/` 目录中的示例文件格式

