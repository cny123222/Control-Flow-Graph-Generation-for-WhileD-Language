"""
WhileD Language Abstract Syntax Tree (AST) Definition

This module defines AST node classes for the WhileD language, including expressions (Expr) and commands (Com).
"""

from dataclasses import dataclass
from typing import Union


def indent_lines(text: str, indent: str = "  ") -> str:
    """Add indentation to multi-line text."""
    lines = text.split('\n')
    return '\n'.join(indent + line if line.strip() else line for line in lines)


# =======================
# Expression AST Nodes
# =======================

@dataclass
class EConst:
    """Integer constant: 5, 10, etc."""
    value: int
    
    def __str__(self):
        return str(self.value)

@dataclass
class EVar:
    """Variable reference: x, y, etc."""
    name: str
    
    def __str__(self):
        return self.name

@dataclass
class EBinop:
    """Binary operation: e1 + e2, e1 && e2, etc.
    
    Operators:
    - Arithmetic: +, -, *, /, %
    - Comparison: <, <=, ==, !=, >=, >
    - Logical: &&, || (requires short-circuit evaluation)
    """
    op: str
    left: 'Expr'
    right: 'Expr'
    
    def __str__(self):
        return f"({self.left} {self.op} {self.right})"

@dataclass
class EUnop:
    """Unary operation: !e, -e
    
    Operators:
    - ! : Logical negation
    - - : Arithmetic negation
    """
    op: str
    expr: 'Expr'
    
    def __str__(self):
        return f"({self.op}{self.expr})"

@dataclass
class EDeref:
    """Pointer dereference: *e
    
    Equivalent to *ptr in C language.
    """
    expr: 'Expr'
    
    def __str__(self):
        return f"(*{self.expr})"

@dataclass
class EAddrOf:
    """Address-of operator: &e
    
    Equivalent to &var in C language.
    Note: e should be an L-value (typically EVar).
    """
    expr: 'Expr'
    
    def __str__(self):
        return f"(&{self.expr})"


# Expression type alias
Expr = Union[EConst, EVar, EBinop, EUnop, EDeref, EAddrOf]


# =======================
# Command AST Nodes
# =======================

@dataclass
class CSkip:
    """Skip statement (no-op)"""
    
    def __str__(self):
        return "skip"

@dataclass
class CAsgnVar:
    """Variable assignment: x = e"""
    var: str
    expr: Expr
    
    def __str__(self):
        return f"{self.var} = {self.expr}"

@dataclass
class CAsgnDeref:
    """Pointer assignment: *e1 = e2
    
    Store value e2 to address e1.
    Specific to WhileD language.
    """
    addr: Expr
    value: Expr
    
    def __str__(self):
        return f"*{self.addr} = {self.value}"

@dataclass
class CSeq:
    """Sequential composition: c1; c2"""
    first: 'Com'
    second: 'Com'
    
    def __str__(self):
        first_str = str(self.first)
        second_str = str(self.second)
        # If second is multi-line, add indentation
        if '\n' in second_str:
            second_str = indent_lines(second_str)
        return f"{first_str};\n{second_str}"

@dataclass
class CIf:
    """Conditional statement: if (cond) then c1 else c2"""
    cond: Expr
    then_branch: 'Com'
    else_branch: 'Com'
    
    def __str__(self):
        then_str = str(self.then_branch)
        else_str = str(self.else_branch)
        # Add indentation to branches
        if '\n' in then_str:
            then_str = indent_lines(then_str)
        else:
            then_str = "  " + then_str
        if '\n' in else_str:
            else_str = indent_lines(else_str)
        else:
            else_str = "  " + else_str
        return f"if ({self.cond}) then\n{then_str}\nelse\n{else_str}"

@dataclass
class CWhile:
    """Loop statement: while (cond) do body"""
    cond: Expr
    body: 'Com'
    
    def __str__(self):
        body_str = str(self.body)
        # Add indentation to loop body
        if '\n' in body_str:
            body_str = indent_lines(body_str)
        else:
            body_str = "  " + body_str
        return f"while ({self.cond}) do\n{body_str}"


# Command type alias
Com = Union[CSkip, CAsgnVar, CAsgnDeref, CSeq, CIf, CWhile]
