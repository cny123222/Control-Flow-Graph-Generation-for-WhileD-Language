"""
WhileD 语言抽象语法树 (AST) 定义

本模块定义了 WhileD 语言的 AST 节点类，包括表达式 (Expr) 和语句 (Com)
"""

from dataclasses import dataclass
from typing import Union


def indent_lines(text: str, indent: str = "  ") -> str:
    """为多行文本添加缩进"""
    lines = text.split('\n')
    return '\n'.join(indent + line if line.strip() else line for line in lines)


# =======================
# 表达式 AST 节点
# =======================

@dataclass
class EConst:
    """整数常量：5, 10, 等等"""
    value: int
    
    def __str__(self):
        return str(self.value)

@dataclass
class EVar:
    """变量引用：x, y, 等等"""
    name: str
    
    def __str__(self):
        return self.name

@dataclass
class EBinop:
    """二元运算：e1 + e2, e1 && e2, 等等
    
    运算符：
    - 算术运算：+, -, *, /, %
    - 比较运算：<, <=, ==, !=, >=, >
    - 逻辑运算：&&, || (需要短路求值)
    """
    op: str
    left: 'Expr'
    right: 'Expr'
    
    def __str__(self):
        return f"({self.left} {self.op} {self.right})"

@dataclass
class EUnop:
    """一元运算：!e, -e
    
    运算符：
    - ! : 逻辑非
    - - : 算术取反
    """
    op: str
    expr: 'Expr'
    
    def __str__(self):
        return f"({self.op}{self.expr})"

@dataclass
class EDeref:
    """指针解引用：*e
    
    等同于 C 语言中的 *ptr
    """
    expr: 'Expr'
    
    def __str__(self):
        return f"(*{self.expr})"

@dataclass
class EAddrOf:
    """取地址运算符：&e
    
    等同于 C 语言中的 &var
    注意：e 应该是左值（通常是 EVar）
    """
    expr: 'Expr'
    
    def __str__(self):
        return f"(&{self.expr})"


# 表达式类型别名
Expr = Union[EConst, EVar, EBinop, EUnop, EDeref, EAddrOf]


# =======================
# 语句 AST 节点
# =======================

@dataclass
class CSkip:
    """空语句（无操作）"""
    
    def __str__(self):
        return "skip"

@dataclass
class CAsgnVar:
    """变量赋值：x = e"""
    var: str
    expr: Expr
    
    def __str__(self):
        return f"{self.var} = {self.expr}"

@dataclass
class CAsgnDeref:
    """指针赋值：*e1 = e2
    
    将值 e2 存储到地址 e1
    WhileD 语言特有
    """
    addr: Expr
    value: Expr
    
    def __str__(self):
        return f"*{self.addr} = {self.value}"

@dataclass
class CSeq:
    """顺序组合：c1; c2"""
    first: 'Com'
    second: 'Com'
    
    def __str__(self):
        first_str = str(self.first)
        second_str = str(self.second)
        # 如果 second 是多行，需要添加缩进
        if '\n' in second_str:
            second_str = indent_lines(second_str)
        return f"{first_str};\n{second_str}"

@dataclass
class CIf:
    """条件语句：if (cond) then c1 else c2"""
    cond: Expr
    then_branch: 'Com'
    else_branch: 'Com'
    
    def __str__(self):
        then_str = str(self.then_branch)
        else_str = str(self.else_branch)
        # 为分支添加缩进
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
    """循环语句：while (cond) do body"""
    cond: Expr
    body: 'Com'
    
    def __str__(self):
        body_str = str(self.body)
        # 为循环体添加缩进
        if '\n' in body_str:
            body_str = indent_lines(body_str)
        else:
            body_str = "  " + body_str
        return f"while ({self.cond}) do\n{body_str}"


# 语句类型别名
Com = Union[CSkip, CAsgnVar, CAsgnDeref, CSeq, CIf, CWhile]
