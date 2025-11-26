"""
演示程序：WhileD 控制流图生成

展示从 AST 到 CFG 的完整转换过程
"""

from ast_definition import *
from cfg_generator import CFGGenerator


def print_section(title):
    """打印格式化的标题"""
    print("\n" + "=" * 70)
    print(f"  {title}")
    print("=" * 70 + "\n")


# ============================================================================
# 示例 1：简单 While 循环
# ============================================================================

print("=" * 80)
print("示例 1：简单 While 循环")
print("=" * 80)

print("\n源程序：")
print("-" * 80)
print("""
while (i < n) do {
    s = s + i;
    i = i + 1
}
""")

# 构建 AST
program1 = CWhile(
    EBinop("<", EVar("i"), EVar("n")),
    CSeq(
        CAsgnVar("s", EBinop("+", EVar("s"), EVar("i"))),
        CAsgnVar("i", EBinop("+", EVar("i"), EConst(1)))
    )
)

# 生成 CFG
generator = CFGGenerator()
cfg1 = generator.generate_cfg(program1)

# 阶段 1：表达式拆分
print_section("阶段 1：表达式拆分 (使用 LABEL)")
cfg1.print_linear_ir()

# 阶段 2：基本块
print_section("阶段 2：基本块 (使用 BB)")
cfg1.print_blocks_structure()

# 阶段 3：流程图
print_section("阶段 3：流程图 (Mermaid)")
print("复制以下代码到 https://mermaid.live/ 查看图形化流程图：")
print("-" * 70)
print("```mermaid")
print(cfg1.to_mermaid())
print("```")


# ============================================================================
# 示例 2：复杂程序
# ============================================================================

print("\n\n" + "=" * 80)
print("示例 2：复杂程序（短路求值 + 指针 + 嵌套控制流）")
print("=" * 80)

print("\n源程序：")
print("-" * 80)
print("""
sum = 0
i = 0
while (i < n && arr != 0) do {
    p = arr + i
    if (*p > 0 && *p < 100) then {
        sum = sum + *p
    } else {
        skip
    }
    i = i + 1
}
""")

# 构建 AST
program2 = CSeq(
    CAsgnVar("sum", EConst(0)),
    CSeq(
        CAsgnVar("i", EConst(0)),
        CWhile(
            EBinop("&&",
                EBinop("<", EVar("i"), EVar("n")),
                EBinop("!=", EVar("arr"), EConst(0))
            ),
            CSeq(
                CAsgnVar("p", EBinop("+", EVar("arr"), EVar("i"))),
                CSeq(
                    CIf(
                        EBinop("&&",
                            EBinop(">", EDeref(EVar("p")), EConst(0)),
                            EBinop("<", EDeref(EVar("p")), EConst(100))
                        ),
                        CAsgnVar("sum", EBinop("+", EVar("sum"), EDeref(EVar("p")))),
                        CSkip()
                    ),
                    CAsgnVar("i", EBinop("+", EVar("i"), EConst(1)))
                )
            )
        )
    )
)

generator2 = CFGGenerator()
cfg2 = generator2.generate_cfg(program2)

# 阶段 1：表达式拆分
print_section("阶段 1：表达式拆分 (使用 LABEL)")
cfg2.print_linear_ir()

# 阶段 2：基本块
print_section("阶段 2：基本块 (使用 BB)")
cfg2.print_blocks_structure()

print("\n" + "=" * 80)
print("演示完成")
print("=" * 80)
print("""
转换流程：
1. 源程序 → AST（抽象语法树）
2. AST → 表达式拆分（使用 LABEL，完成表达式线性化和短路求值）
3. 表达式拆分 → 基本块（将 LABEL 转为 BB）
4. 基本块 → 流程图（可视化）
""")

