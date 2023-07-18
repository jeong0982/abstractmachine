from __future__ import annotations
from dataclasses import dataclass
from py_ecc import fields
from enum import Enum, auto
from typing import List, Tuple

F = fields.bn128_FQ

@dataclass
class Expr:
    e: BinOp | UnOp | Var | Num

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
class Num:
    value: F

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

class Undef:
    pass

# This is stack based abstract machine
class SimpleAbstractMachine:
    def __init__(self):
        self.stack = []
        self.variables = {}

    def evaluate_expression(self, expr: Expr) -> F:
        if isinstance(expr, BinOp):
            lhs = self.evaluate_expression(expr.lhs)
            rhs = self.evaluate_expression(expr.rhs)
            if expr.op == BinOperator.Add:
                return lhs + rhs
            elif expr.op == BinOperator.Sub:
                return lhs - rhs
            elif expr.op == BinOperator.Mul:
                return lhs * rhs
            else:
                raise ValueError("Unknown binary operator.")
        elif isinstance(expr, UnOp):
            operand = self.evaluate_expression(expr.operand)
            if expr.operator == UnOperator.Neg:
                return -operand
            else:
                raise ValueError("Unknown unary operator.")
        elif isinstance(expr, Var):
            var_name = expr.name
            if var_name in self.variables:
                return self.variables[var_name]
            else:
                raise ValueError(f"Variable '{var_name}' is not defined.")
        else:
            raise ValueError("Unknown expression type.")

    def execute_block(self, block: Block):
        for statement in block.stmts:
            self.execute_statement(statement)

    def execute_statement(self, statement: Statement):
        if isinstance(statement, Assignment):
            var_name = statement.variable.name
            expr_value = self.evaluate_expression(statement.value)
            self.variables[var_name] = expr_value
        elif isinstance(statement, Assertion):
            expr_value = self.evaluate_expression(statement.expression)
            print(f"Assertion: {expr_value}")
        elif isinstance(statement, IfElse):
            condition = self.evaluate_expression(statement.condition)
            if condition:
                self.execute_block(statement.if_body)
            else:
                self.execute_block(statement.else_body)
        else:
            raise ValueError("Unknown statement type.")

    def execute(self, commands):
        parsed_commands = self.parse(commands)
        for statement in parsed_commands:
            self.execute_statement(statement)

    def evaluate_condition(self, condition):
        return bool(eval(condition.strip(), {}, self.variables))

    def parse(self, commands: List[str]) -> List[Statement]:
        parsed_commands = []
        for command in commands:
            command = command.strip()
            if command.startswith("PRINT"):
                expr = command[6:].strip()
                parsed_commands.append(Statement(self.parse_expression(expr.split())))
            elif "=" in command:
                var_name, expr = command.split("=")
                parsed_commands.append(Statement(Assignment(Var(var_name.strip()), self.parse_expression(expr.split()))))
            elif command.startswith("IF"):
                condition, then_block, else_block = self.parse_if_command(command[2:])
                parsed_commands.append(Statement(IfElse(self.parse_expression(condition.split()), Block(self.parse(then_block)), Block(self.parse(else_block)))))
            else:
                raise ValueError(f"Unknown command: {command}")
        return parsed_commands

    def parse_if_command(self, command: str) -> Tuple[str, List[str], List[str]]:
        parts = command.split("THEN")
        condition = parts[0].strip()
        then_block = parts[1].split("ELSE")[0].strip().split("\n")
        else_block = parts[1].split("ELSE")[1].strip().split("\n")
        return condition, then_block, else_block

    def parse_expression(self, expr: List[str]) -> Expr:
        if len(expr) == 1:
            try:
                return Expr(Num(F(expr[0])))
            except ValueError:
                return Expr(Var(expr[0]))
        elif len(expr) == 2:
            return Expr(UnOp(UnOperator.Neg, self.parse_expression(expr[1:])))
        elif len(expr) == 3:
            return Expr(BinOp(BinOperator[expr[1]], self.parse_expression(expr[:1]), self.parse_expression(expr[2:])))
        else:
            raise ValueError("Invalid expression.")

if __name__ == "__main__":
    machine = SimpleAbstractMachine()
    commands = [
        "x = 10",
        "y = 5",
        "z = x + y",
        "PRINT z",
        "IF z > 15 THEN",
        "    PRINT 'z is greater than 15'",
        "ELSE",
        "    PRINT 'z is less than or equal to 15'",
        "END",
        "i = 0",
        "WHILE i < 5 DO",
        "    PRINT i",
        "    i = i + 1",
        "END"
    ]
    machine.execute(commands)
