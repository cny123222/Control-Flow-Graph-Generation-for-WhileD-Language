"""
Main Program: Test Cases for WhileD CFG Generator

This module demonstrates the CFG generator with comprehensive test cases.
"""

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


if __name__ == "__main__":
    run_all_tests()

