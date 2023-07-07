from __future__ import annotations
from dataclasses import dataclass
from py_ecc import fields
from enum import Enum, auto

F = fields.bn128_FQ

@dataclass
class Expr:
    e: BinOp | UnOp | Var

@dataclass
class BinOp:
    op: BinOperator
    lhs: Expr
    rhs: Expr

class BinOperator(Enum):
    Add = auto()
    Sub = auto()
    Mul = auto()

@dataclass
class UnOp:
    operator: UnOperator
    operand: Expr

class UnOperator(Enum):
    Neg = auto()

@dataclass
class Var:
    name: str

@dataclass
class Statement:
    expr: Expr | Assignment | Assertion | IfElse

@dataclass
class Assignment:
    variable: Var
    value: Expr

@dataclass
class Assertion:
    expression: Expr

@dataclass
class IfElse:
    condition: Expr
    if_body: Block
    else_body: Block

@dataclass
class Block:
    stmts: list[Statement]
