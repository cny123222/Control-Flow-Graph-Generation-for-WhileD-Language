"""
Main Program: Test Cases for WhileD CFG Generator

This module demonstrates the CFG generator with comprehensive test cases.
"""

from ast_definition import *
from ir_representation import *
from cfg_generator import CFGGenerator


def print_test_header(test_name: str, description: str):
    """Print a formatted test header."""
    print("=" * 70)
    print(f"TEST: {test_name}")
    print(f"Description: {description}")
    print("=" * 70)
    print()


def print_cfg_result(cfg: ControlFlowGraph):
    """Print the CFG in the required format."""
    print("Generated IR:")
    print("-" * 70)
    print(cfg)
    print("-" * 70)
    print()


def test_1_expression_splitting():
    """Test 1: Simple expression splitting (linearization)"""
    print_test_header(
        "Expression Splitting",
        "Input: x = a + b + c\nExpected: Multi-step linearization"
    )
    
    # AST: x = a + b + c
    # Parsed as: x = ((a + b) + c)
    program = CAsgnVar(
        "x",
        EBinop("+",
            EBinop("+", EVar("a"), EVar("b")),
            EVar("c")
        )
    )
    
    generator = CFGGenerator()
    cfg = generator.generate_cfg(program)
    print_cfg_result(cfg)


def test_2_nested_expressions():
    """Test 2: Nested arithmetic and comparison"""
    print_test_header(
        "Nested Expressions",
        "Input: result = (x + y) * (z - 10) < 100\nExpected: Multiple temp variables"
    )
    
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
    
    generator = CFGGenerator()
    cfg = generator.generate_cfg(program)
    print_cfg_result(cfg)


def test_3_short_circuit_and():
    """Test 3: Short-circuit AND evaluation"""
    print_test_header(
        "Short-circuit AND",
        "Input: result = p && (*p != 0)\nExpected: Control flow with jumps"
    )
    
    # AST: result = p && (*p != 0)
    program = CAsgnVar(
        "result",
        EBinop("&&",
            EVar("p"),
            EBinop("!=", EDeref(EVar("p")), EConst(0))
        )
    )
    
    generator = CFGGenerator()
    cfg = generator.generate_cfg(program)
    print_cfg_result(cfg)


def test_4_short_circuit_or():
    """Test 4: Short-circuit OR evaluation"""
    print_test_header(
        "Short-circuit OR",
        "Input: result = (x == 0) || (y > 10)\nExpected: Control flow with jumps"
    )
    
    # AST: result = (x == 0) || (y > 10)
    program = CAsgnVar(
        "result",
        EBinop("||",
            EBinop("==", EVar("x"), EConst(0)),
            EBinop(">", EVar("y"), EConst(10))
        )
    )
    
    generator = CFGGenerator()
    cfg = generator.generate_cfg(program)
    print_cfg_result(cfg)


def test_5_while_loop():
    """Test 5: While loop"""
    print_test_header(
        "While Loop",
        "Input: while (i < n) do { s = s + i; i = i + 1 }\nExpected: Loop with labels and jumps"
    )
    
    # AST: while (i < n) do { s = s + i; i = i + 1 }
    program = CWhile(
        EBinop("<", EVar("i"), EVar("n")),
        CSeq(
            CAsgnVar("s", EBinop("+", EVar("s"), EVar("i"))),
            CAsgnVar("i", EBinop("+", EVar("i"), EConst(1)))
        )
    )
    
    generator = CFGGenerator()
    cfg = generator.generate_cfg(program)
    print_cfg_result(cfg)


def test_6_if_else():
    """Test 6: If-else statement"""
    print_test_header(
        "If-Else Statement",
        "Input: if (x > 0) then y = x else y = -x\nExpected: Branching structure"
    )
    
    # AST: if (x > 0) then y = x else y = -x
    program = CIf(
        EBinop(">", EVar("x"), EConst(0)),
        CAsgnVar("y", EVar("x")),
        CAsgnVar("y", EUnop("-", EVar("x")))
    )
    
    generator = CFGGenerator()
    cfg = generator.generate_cfg(program)
    print_cfg_result(cfg)


def test_7_pointer_operations():
    """Test 7: Pointer operations (address-of and dereference)"""
    print_test_header(
        "Pointer Operations",
        "Input: p = &x; *p = 10\nExpected: Correct IR for pointer ops"
    )
    
    # AST: p = &x; *p = 10
    program = CSeq(
        CAsgnVar("p", EAddrOf(EVar("x"))),
        CAsgnDeref(EVar("p"), EConst(10))
    )
    
    generator = CFGGenerator()
    cfg = generator.generate_cfg(program)
    print_cfg_result(cfg)


def test_8_complex_while_with_shortcircuit():
    """Test 8: While loop with short-circuit condition"""
    print_test_header(
        "Complex While with Short-circuit",
        "Input: while (p != 0 && *p > 0) do { p = p + 1 }\nExpected: Nested control flow"
    )
    
    # AST: while (p != 0 && *p > 0) do { p = p + 1 }
    program = CWhile(
        EBinop("&&",
            EBinop("!=", EVar("p"), EConst(0)),
            EBinop(">", EDeref(EVar("p")), EConst(0))
        ),
        CAsgnVar("p", EBinop("+", EVar("p"), EConst(1)))
    )
    
    generator = CFGGenerator()
    cfg = generator.generate_cfg(program)
    print_cfg_result(cfg)


def test_9_nested_if():
    """Test 9: Nested if-else"""
    print_test_header(
        "Nested If-Else",
        "Input: if (x > 0) then { if (y > 0) then z = 1 else z = 2 } else z = 3"
    )
    
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
    
    generator = CFGGenerator()
    cfg = generator.generate_cfg(program)
    print_cfg_result(cfg)


def test_10_comprehensive():
    """Test 10: Comprehensive test combining multiple features"""
    print_test_header(
        "Comprehensive Test",
        "Complex program with loops, conditionals, and expressions"
    )
    
    # AST: More complex program
    # while (i < n) do {
    #     if (arr[i] > max) then {
    #         max = arr[i]
    #     } else {
    #         skip
    #     }
    #     i = i + 1
    # }
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
    
    generator = CFGGenerator()
    cfg = generator.generate_cfg(program)
    print_cfg_result(cfg)
    
    # Also print graph structure
    print("CFG Structure Information:")
    print("-" * 70)
    cfg.print_graph_info()


def run_all_tests():
    """Run all test cases."""
    print("\n")
    print("#" * 70)
    print("# WhileD CFG Generator - Comprehensive Test Suite")
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

