"""
Main Program: Test Cases for WhileD CFG Generator

This module demonstrates the CFG generator with comprehensive test cases.
"""

import os
import sys
from ast_definition import *
from ir_representation import *
from cfg_generator import CFGGenerator


def print_test_header(test_num: int, test_name: str, source_program):
    """Print a formatted test header with source program."""
    print("=" * 70)
    print(f"测试 {test_num}: {test_name}")
    print("=" * 70)
    print("源程序:")
    print("-" * 70)
    print(source_program)
    print("-" * 70)
    print()


def print_cfg_result(cfg: ControlFlowGraph):
    """Print the CFG in the required format."""
    print("生成的 IR:")
    print("-" * 70)
    print(cfg)
    print("-" * 70)
    print()


def test_1_expression_splitting():
    """Test 1: Simple expression splitting (linearization)"""
    source = "x = a + b + c"
    
    # AST: x = a + b + c
    # Parsed as: x = ((a + b) + c)
    program = CAsgnVar(
        "x",
        EBinop("+",
            EBinop("+", EVar("a"), EVar("b")),
            EVar("c")
        )
    )
    
    print_test_header(1, "表达式拆分", source)
    
    generator = CFGGenerator()
    cfg = generator.generate_cfg(program)
    print_cfg_result(cfg)


def test_2_nested_expressions():
    """Test 2: Nested arithmetic and comparison"""
    source = "result = (x + y) * (z - 10) < 100"
    
    # AST: result = (x + y) * (z - 10) < 100
    program = CAsgnVar(
        "result",
        EBinop("<",
            EBinop("*",
                EBinop("+", EVar("x"), EVar("y")),
                EBinop("-", EVar("z"), EConst(10))
            ),
            EConst(100)
        )
    )
    
    print_test_header(2, "嵌套表达式", source)
    
    generator = CFGGenerator()
    cfg = generator.generate_cfg(program)
    print_cfg_result(cfg)


def test_3_short_circuit_and():
    """Test 3: Short-circuit AND evaluation"""
    source = "result = p && *p != 0"
    
    # AST: result = p && (*p != 0)
    program = CAsgnVar(
        "result",
        EBinop("&&",
            EVar("p"),
            EBinop("!=", EDeref(EVar("p")), EConst(0))
        )
    )
    
    print_test_header(3, "短路求值 AND", source)
    
    generator = CFGGenerator()
    cfg = generator.generate_cfg(program)
    print_cfg_result(cfg)


def test_4_short_circuit_or():
    """Test 4: Short-circuit OR evaluation"""
    source = "result = x == 0 || y > 10"
    
    # AST: result = (x == 0) || (y > 10)
    program = CAsgnVar(
        "result",
        EBinop("||",
            EBinop("==", EVar("x"), EConst(0)),
            EBinop(">", EVar("y"), EConst(10))
        )
    )
    
    print_test_header(4, "短路求值 OR", source)
    
    generator = CFGGenerator()
    cfg = generator.generate_cfg(program)
    print_cfg_result(cfg)


def test_5_while_loop():
    """Test 5: While loop"""
    source = "while (i < n) do { s = s + i; i = i + 1 }"
    
    # AST: while (i < n) do { s = s + i; i = i + 1 }
    program = CWhile(
        EBinop("<", EVar("i"), EVar("n")),
        CSeq(
            CAsgnVar("s", EBinop("+", EVar("s"), EVar("i"))),
            CAsgnVar("i", EBinop("+", EVar("i"), EConst(1)))
        )
    )
    
    print_test_header(5, "While 循环", source)
    
    generator = CFGGenerator()
    cfg = generator.generate_cfg(program)
    print_cfg_result(cfg)


def test_6_if_else():
    """Test 6: If-else statement"""
    source = "if (x > 0) then y = x else y = -x"
    
    # AST: if (x > 0) then y = x else y = -x
    program = CIf(
        EBinop(">", EVar("x"), EConst(0)),
        CAsgnVar("y", EVar("x")),
        CAsgnVar("y", EUnop("-", EVar("x")))
    )
    
    print_test_header(6, "If-Else 分支", source)
    
    generator = CFGGenerator()
    cfg = generator.generate_cfg(program)
    print_cfg_result(cfg)


def test_7_pointer_operations():
    """Test 7: Pointer operations (address-of and dereference)"""
    source = "p = &x; *p = 10"
    
    # AST: p = &x; *p = 10
    program = CSeq(
        CAsgnVar("p", EAddrOf(EVar("x"))),
        CAsgnDeref(EVar("p"), EConst(10))
    )
    
    print_test_header(7, "指针操作", source)
    
    generator = CFGGenerator()
    cfg = generator.generate_cfg(program)
    print_cfg_result(cfg)


def test_8_complex_while_with_shortcircuit():
    """Test 8: While loop with short-circuit condition"""
    source = "while (p != 0 && *p > 0) do { p = p + 1 }"
    
    # AST: while (p != 0 && *p > 0) do { p = p + 1 }
    program = CWhile(
        EBinop("&&",
            EBinop("!=", EVar("p"), EConst(0)),
            EBinop(">", EDeref(EVar("p")), EConst(0))
        ),
        CAsgnVar("p", EBinop("+", EVar("p"), EConst(1)))
    )
    
    print_test_header(8, "While 循环（带短路求值）", source)
    
    generator = CFGGenerator()
    cfg = generator.generate_cfg(program)
    print_cfg_result(cfg)


def test_9_nested_if():
    """Test 9: Nested if-else"""
    source = "if (x > 0) then { if (y > 0) then z = 1 else z = 2 } else z = 3"
    
    # AST: if (x > 0) then { if (y > 0) then z = 1 else z = 2 } else z = 3
    program = CIf(
        EBinop(">", EVar("x"), EConst(0)),
        CIf(
            EBinop(">", EVar("y"), EConst(0)),
            CAsgnVar("z", EConst(1)),
            CAsgnVar("z", EConst(2))
        ),
        CAsgnVar("z", EConst(3))
    )
    
    print_test_header(9, "嵌套 If-Else", source)
    
    generator = CFGGenerator()
    cfg = generator.generate_cfg(program)
    print_cfg_result(cfg)


def test_10_comprehensive():
    """Test 10: Comprehensive test combining multiple features"""
    source = "while (i < n) do { p = arr + i; if (*p > max) then max = *p else skip; i = i + 1 }"
    
    # AST: More complex program
    # Simplified without array indexing (use pointer arithmetic):
    # while (i < n) do {
    #     p = arr + i;
    #     if (*p > max) then max = *p else skip;
    #     i = i + 1
    # }
    
    program = CWhile(
        EBinop("<", EVar("i"), EVar("n")),
        CSeq(
            CSeq(
                CAsgnVar("p", EBinop("+", EVar("arr"), EVar("i"))),
                CIf(
                    EBinop(">", EDeref(EVar("p")), EVar("max")),
                    CAsgnVar("max", EDeref(EVar("p"))),
                    CSkip()
                )
            ),
            CAsgnVar("i", EBinop("+", EVar("i"), EConst(1)))
        )
    )
    
    print_test_header(10, "综合测试", source)
    
    generator = CFGGenerator()
    cfg = generator.generate_cfg(program)
    print_cfg_result(cfg)


def run_all_tests():
    """Run all test cases."""
    print("\n")
    print("#" * 70)
    print("# WhileD 控制流图生成器 - 测试用例")
    print("#" * 70)
    print("\n")
    
    test_1_expression_splitting()
    test_2_nested_expressions()
    test_3_short_circuit_and()
    test_4_short_circuit_or()
    test_5_while_loop()
    test_6_if_else()
    test_7_pointer_operations()
    test_8_complex_while_with_shortcircuit()
    test_9_nested_if()
    test_10_comprehensive()
    
    print("\n")
    print("#" * 70)
    print("# All tests completed!")
    print("#" * 70)


def generate_mermaid_files():
    """生成所有测试用例的 Mermaid 流程图文件"""
    
    def save_mermaid(test_num: int, test_name: str, source: str, program: Com, output_file: str):
        """生成并保存 Mermaid 流程图"""
        generator = CFGGenerator()
        cfg = generator.generate_cfg(program)
        
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(f"# 测试 {test_num}: {test_name}\n\n")
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
        
        print(f"  ✓ 测试 {test_num}: {test_name}")
    
    # 创建输出目录
    output_dir = "mermaid_outputs/main"
    os.makedirs(output_dir, exist_ok=True)
    
    print("\n" + "=" * 80)
    print("生成 Mermaid 流程图文件 (main.py 测试用例)")
    print("=" * 80)
    print()
    
    # 测试 1
    save_mermaid(
        1, "表达式拆分",
        "x = a + b + c",
        CAsgnVar("x", EBinop("+", EBinop("+", EVar("a"), EVar("b")), EVar("c"))),
        f"{output_dir}/test1_expression_splitting.md"
    )
    
    # 测试 2
    save_mermaid(
        2, "嵌套表达式",
        "result = (x + y) * (z - 10) < 100",
        CAsgnVar("result", EBinop("<", EBinop("*", EBinop("+", EVar("x"), EVar("y")), EBinop("-", EVar("z"), EConst(10))), EConst(100))),
        f"{output_dir}/test2_nested_expressions.md"
    )
    
    # 测试 3
    save_mermaid(
        3, "短路求值 AND",
        "result = p && *p != 0",
        CAsgnVar("result", EBinop("&&", EVar("p"), EBinop("!=", EDeref(EVar("p")), EConst(0)))),
        f"{output_dir}/test3_shortcircuit_and.md"
    )
    
    # 测试 4
    save_mermaid(
        4, "短路求值 OR",
        "result = x == 0 || y > 10",
        CAsgnVar("result", EBinop("||", EBinop("==", EVar("x"), EConst(0)), EBinop(">", EVar("y"), EConst(10)))),
        f"{output_dir}/test4_shortcircuit_or.md"
    )
    
    # 测试 5
    save_mermaid(
        5, "While 循环",
        "while (i < n) do { s = s + i; i = i + 1 }",
        CWhile(EBinop("<", EVar("i"), EVar("n")), CSeq(CAsgnVar("s", EBinop("+", EVar("s"), EVar("i"))), CAsgnVar("i", EBinop("+", EVar("i"), EConst(1))))),
        f"{output_dir}/test5_while_loop.md"
    )
    
    # 测试 6
    save_mermaid(
        6, "If-Else 分支",
        "if (x > 0) then y = x else y = -x",
        CIf(EBinop(">", EVar("x"), EConst(0)), CAsgnVar("y", EVar("x")), CAsgnVar("y", EUnop("-", EVar("x")))),
        f"{output_dir}/test6_if_else.md"
    )
    
    # 测试 7
    save_mermaid(
        7, "指针操作",
        "p = &x; *p = 10",
        CSeq(CAsgnVar("p", EAddrOf(EVar("x"))), CAsgnDeref(EVar("p"), EConst(10))),
        f"{output_dir}/test7_pointer_operations.md"
    )
    
    # 测试 8
    save_mermaid(
        8, "While 循环（带短路求值）",
        "while (p != 0 && *p > 0) do { p = p + 1 }",
        CWhile(EBinop("&&", EBinop("!=", EVar("p"), EConst(0)), EBinop(">", EDeref(EVar("p")), EConst(0))), CAsgnVar("p", EBinop("+", EVar("p"), EConst(1)))),
        f"{output_dir}/test8_complex_while_shortcircuit.md"
    )
    
    # 测试 9
    save_mermaid(
        9, "嵌套 If-Else",
        "if (x > 0) then { if (y > 0) then z = 1 else z = 2 } else z = 3",
        CIf(EBinop(">", EVar("x"), EConst(0)), CIf(EBinop(">", EVar("y"), EConst(0)), CAsgnVar("z", EConst(1)), CAsgnVar("z", EConst(2))), CAsgnVar("z", EConst(3))),
        f"{output_dir}/test9_nested_if.md"
    )
    
    # 测试 10
    save_mermaid(
        10, "综合测试",
        "while (i < n) do { p = arr + i; if (*p > max) then max = *p else skip; i = i + 1 }",
        CWhile(EBinop("<", EVar("i"), EVar("n")), CSeq(CSeq(CAsgnVar("p", EBinop("+", EVar("arr"), EVar("i"))), CIf(EBinop(">", EDeref(EVar("p")), EVar("max")), CAsgnVar("max", EDeref(EVar("p"))), CSkip())), CAsgnVar("i", EBinop("+", EVar("i"), EConst(1))))),
        f"{output_dir}/test10_comprehensive.md"
    )
    
    # 生成汇总文档
    print()
    print("生成汇总文档...")
    with open(f"{output_dir}/README.md", 'w', encoding='utf-8') as f:
        f.write("# main.py 测试用例 Mermaid 流程图\n\n")
        f.write("本目录包含 `main.py` 中所有测试用例的 Mermaid 流程图。\n\n")
        f.write("## 如何查看\n\n")
        f.write("1. **在线查看**: 访问 https://mermaid.live/\n")
        f.write("2. **复制代码**: 将 MD 文件中的 Mermaid 代码块复制到编辑器\n")
        f.write("3. **自动渲染**: 右侧会自动显示流程图\n\n")
        f.write("## 测试列表\n\n")
        f.write("| 测试 | 文件 | 描述 |\n")
        f.write("|------|------|------|\n")
        f.write("| 测试1 | [test1_expression_splitting.md](test1_expression_splitting.md) | 表达式拆分 |\n")
        f.write("| 测试2 | [test2_nested_expressions.md](test2_nested_expressions.md) | 嵌套表达式 |\n")
        f.write("| 测试3 | [test3_shortcircuit_and.md](test3_shortcircuit_and.md) | 短路求值 AND |\n")
        f.write("| 测试4 | [test4_shortcircuit_or.md](test4_shortcircuit_or.md) | 短路求值 OR |\n")
        f.write("| 测试5 | [test5_while_loop.md](test5_while_loop.md) | While 循环 |\n")
        f.write("| 测试6 | [test6_if_else.md](test6_if_else.md) | If-Else 分支 |\n")
        f.write("| 测试7 | [test7_pointer_operations.md](test7_pointer_operations.md) | 指针操作 |\n")
        f.write("| 测试8 | [test8_complex_while_shortcircuit.md](test8_complex_while_shortcircuit.md) | While 循环（带短路求值） |\n")
        f.write("| 测试9 | [test9_nested_if.md](test9_nested_if.md) | 嵌套 If-Else |\n")
        f.write("| 测试10 | [test10_comprehensive.md](test10_comprehensive.md) | 综合测试 |\n")
    
    print(f"  ✓ README.md")
    
    print()
    print("=" * 80)
    print("✅ Mermaid 文件生成完成")
    print("=" * 80)
    print(f"""
所有 Mermaid 流程图已保存到 {output_dir}/ 目录

查看方法：
方法1（推荐）：在 VSCode 中打开 .md 文件，点击预览图标即可查看流程图
方法2：访问 https://mermaid.live/，复制 Mermaid 代码块到编辑器查看
    """)


if __name__ == "__main__":
    # 根据命令行参数决定是否生成文件
    if len(sys.argv) > 1 and sys.argv[1] == "--generate":
        generate_mermaid_files()
    else:
        run_all_tests()
        print("\n" + "=" * 70)
        print("提示：运行 'python main.py --generate' 可生成 Mermaid 文件到 mermaid_outputs/main/ 目录")
        print("=" * 70)

