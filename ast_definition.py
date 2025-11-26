"""
WhileD 语言抽象语法树 (AST) 定义

本模块定义了 WhileD 语言的 AST 节点类，包括表达式 (Expr) 和语句 (Com)
"""

from dataclasses import dataclass
from typing import Union


# =======================
# 表达式 AST 节点
# =======================

@dataclass
class EConst:
    """整数常量：5, 10, 等等"""
    value: int

@dataclass
class EVar:
    """变量引用：x, y, 等等"""
    name: str

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

@dataclass
class EUnop:
    """一元运算：!e, -e
    
    运算符：
    - ! : 逻辑非
    - - : 算术取反
    """
    op: str
    expr: 'Expr'

@dataclass
class EDeref:
    """指针解引用：*e
    
    等同于 C 语言中的 *ptr
    """
    expr: 'Expr'

@dataclass
class EAddrOf:
    """取地址运算符：&e
    
    等同于 C 语言中的 &var
    注意：e 应该是左值（通常是 EVar）
    """
    expr: 'Expr'


# 表达式类型别名
Expr = Union[EConst, EVar, EBinop, EUnop, EDeref, EAddrOf]


# =======================
# 语句 AST 节点
# =======================

@dataclass
class CSkip:
    """空语句（无操作）"""
    pass

@dataclass
class CAsgnVar:
    """变量赋值：x = e"""
    var: str
    expr: Expr

@dataclass
class CAsgnDeref:
    """指针赋值：*e1 = e2
    
    将值 e2 存储到地址 e1
    WhileD 语言特有
    """
    addr: Expr
    value: Expr

@dataclass
class CSeq:
    """顺序组合：c1; c2"""
    first: 'Com'
    second: 'Com'

@dataclass
class CIf:
    """条件语句：if (cond) then c1 else c2"""
    cond: Expr
    then_branch: 'Com'
    else_branch: 'Com'

@dataclass
class CWhile:
    """循环语句：while (cond) do body"""
    cond: Expr
    body: 'Com'


# 语句类型别名
Com = Union[CSkip, CAsgnVar, CAsgnDeref, CSeq, CIf, CWhile]
