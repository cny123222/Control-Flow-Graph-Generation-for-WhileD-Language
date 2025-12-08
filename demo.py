"""
WhileD 控制流图生成演示程序

功能:
1. 终端演示：展示 2 个示例程序的完整转换过程
2. 文件生成：生成 6 个测试用例的 Mermaid 流程图并保存到 mermaid_outputs/ 目录

使用方法:
    python demo.py              # 仅终端演示
    python demo.py --generate   # 终端演示 + 生成 Mermaid 文件
"""

from ast_definition import *
from cfg_generator import CFGGenerator
import os
import sys


def print_section(title):
    """打印格式化的标题"""
    print("\n" + "=" * 70)
    print(f"  {title}")
    print("=" * 70 + "\n")


def terminal_demo():
    """终端演示：展示完整转换过程"""
    
    # ========================================================================
    # 示例 1：简单 While 循环
    # ========================================================================
    
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
    
    
    # ========================================================================
    # 示例 2：复杂程序
    # ========================================================================
    
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
    
    # 阶段 3：流程图
    print_section("阶段 3：流程图 (Mermaid)")
    print("复制以下代码到 https://mermaid.live/ 查看图形化流程图：")
    print("-" * 70)
    print("```mermaid")
    print(cfg2.to_mermaid())
    print("```")
    
    print("\n" + "=" * 80)
    print("终端演示完成")
    print("=" * 80)
    print("""
转换流程：
1. 源程序 → AST（抽象语法树）
2. AST → 表达式拆分（使用 LABEL，完成表达式线性化和短路求值）
3. 表达式拆分 → 基本块（将 LABEL 转为 BB）
4. 基本块 → 流程图（可视化）
    """)


def generate_mermaid_files():
    """生成 Mermaid 流程图文件"""
    
    def save_mermaid(name: str, description: str, program: Com, output_file: str):
        """生成并保存 Mermaid 流程图"""
        generator = CFGGenerator()
        cfg = generator.generate_cfg(program)
        
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(f"# {name}\n\n")
            f.write(f"**描述**: {description}\n\n")
            f.write("## 流程图\n\n")
            f.write("```mermaid\n")
            f.write(cfg.to_mermaid())
            f.write("\n```\n\n")
            
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
            f.write("```\n")
        
        print(f"  ✓ {name}")
    
    # 创建输出目录
    output_dir = "mermaid_outputs"
    os.makedirs(output_dir, exist_ok=True)
    
    print("\n" + "=" * 80)
    print("生成 Mermaid 流程图文件")
    print("=" * 80)
    print()
    
    # 测试 1: 简单 While 循环
    save_mermaid(
        "测试1：简单While循环",
        "while (i < n) do { s = s + i; i = i + 1 }",
        CWhile(
            EBinop("<", EVar("i"), EVar("n")),
            CSeq(
                CAsgnVar("s", EBinop("+", EVar("s"), EVar("i"))),
                CAsgnVar("i", EBinop("+", EVar("i"), EConst(1)))
            )
        ),
        f"{output_dir}/test1_while_loop.md"
    )
    
    # 测试 2: If-Else 分支
    save_mermaid(
        "测试2：If-Else分支",
        "if (x > 0) then y = x else y = -x",
        CIf(
            EBinop(">", EVar("x"), EConst(0)),
            CAsgnVar("y", EVar("x")),
            CAsgnVar("y", EUnop("-", EVar("x")))
        ),
        f"{output_dir}/test2_if_else.md"
    )
    
    # 测试 3: 短路求值 AND
    save_mermaid(
        "测试3：短路求值AND",
        "result = p && (*p != 0)",
        CAsgnVar(
            "result",
            EBinop("&&",
                EVar("p"),
                EBinop("!=", EDeref(EVar("p")), EConst(0))
            )
        ),
        f"{output_dir}/test3_shortcircuit_and.md"
    )
    
    # 测试 4: 短路求值 OR
    save_mermaid(
        "测试4：短路求值OR",
        "result = (x == 0) || (y > 10)",
        CAsgnVar(
            "result",
            EBinop("||",
                EBinop("==", EVar("x"), EConst(0)),
                EBinop(">", EVar("y"), EConst(10))
            )
        ),
        f"{output_dir}/test4_shortcircuit_or.md"
    )
    
    # 测试 5: 嵌套控制流
    save_mermaid(
        "测试5：嵌套控制流",
        "sum = 0; while (i < n) do { if (i > 0) then sum = sum + i else skip }",
        CSeq(
            CAsgnVar("sum", EConst(0)),
            CWhile(
                EBinop("<", EVar("i"), EVar("n")),
                CIf(
                    EBinop(">", EVar("i"), EConst(0)),
                    CAsgnVar("sum", EBinop("+", EVar("sum"), EVar("i"))),
                    CSkip()
                )
            )
        ),
        f"{output_dir}/test5_nested.md"
    )
    
    # 测试 6: 指针操作
    save_mermaid(
        "测试6：指针操作",
        "p = &x; *p = 42",
        CSeq(
            CAsgnVar("p", EAddrOf(EVar("x"))),
            CAsgnDeref(EVar("p"), EConst(42))
        ),
        f"{output_dir}/test6_pointer.md"
    )
    
    # 生成汇总文档
    print()
    print("生成汇总文档...")
    
    with open(f"{output_dir}/README.md", 'w', encoding='utf-8') as f:
        f.write("# Mermaid 流程图测试结果\n\n")
        f.write("本目录包含所有测试用例的 Mermaid 流程图。\n\n")
        f.write("## 如何查看\n\n")
        f.write("1. **在线查看**: 访问 https://mermaid.live/\n")
        f.write("2. **复制代码**: 将 MD 文件中的 Mermaid 代码块复制到编辑器\n")
        f.write("3. **自动渲染**: 右侧会自动显示流程图\n\n")
        f.write("## 测试列表\n\n")
        f.write("| 测试 | 文件 | 描述 |\n")
        f.write("|------|------|------|\n")
        f.write("| 测试1 | [test1_while_loop.md](test1_while_loop.md) | 简单While循环 |\n")
        f.write("| 测试2 | [test2_if_else.md](test2_if_else.md) | If-Else分支 |\n")
        f.write("| 测试3 | [test3_shortcircuit_and.md](test3_shortcircuit_and.md) | 短路求值AND |\n")
        f.write("| 测试4 | [test4_shortcircuit_or.md](test4_shortcircuit_or.md) | 短路求值OR |\n")
        f.write("| 测试5 | [test5_nested.md](test5_nested.md) | 嵌套控制流 |\n")
        f.write("| 测试6 | [test6_pointer.md](test6_pointer.md) | 指针操作 |\n")
        f.write("\n## 文件结构\n\n")
        f.write("每个测试文件包含：\n")
        f.write("- 📊 Mermaid 流程图代码\n")
        f.write("- 📝 阶段1：表达式拆分 (LABEL)\n")
        f.write("- 📦 阶段2：基本块 (BB)\n")
    
    print(f"  ✓ README.md")
    
    print()
    print("=" * 80)
    print("✅ Mermaid 文件生成完成")
    print("=" * 80)
    print(f"""
所有 Mermaid 流程图已保存到 {output_dir}/ 目录

文件列表：
  - test1_while_loop.md        (简单While循环)
  - test2_if_else.md           (If-Else分支)
  - test3_shortcircuit_and.md  (短路求值AND)
  - test4_shortcircuit_or.md   (短路求值OR)
  - test5_nested.md            (嵌套控制流)
  - test6_pointer.md           (指针操作)
  - README.md                  (汇总文档)

查看方法：
1. 打开任意 .md 文件
2. 复制 Mermaid 代码块
3. 访问 https://mermaid.live/
4. 粘贴代码即可看到图形化流程图
    """)


if __name__ == "__main__":
    # 终端演示
    terminal_demo()
    
    # 根据命令行参数决定是否生成文件
    if len(sys.argv) > 1 and sys.argv[1] == "--generate":
        generate_mermaid_files()
    else:
        print("\n" + "=" * 80)
        print("提示：运行 'python demo.py --generate' 可生成 Mermaid 文件到 mermaid_outputs/ 目录")
        print("=" * 80)
