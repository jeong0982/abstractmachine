from syntax import *

class Context:
    def __init__(self):
        self.variables = {}

    def assign_variable(self, variable, value):
        self.variables[variable.name] = value

    def get_variable(self, variable):
        return self.variables.get(variable.name, None)


def evaluate_expr(expr, context):
    if isinstance(expr, BinOp):
        left_value = evaluate_expr(expr.lhs, context)
        right_value = evaluate_expr(expr.rhs, context)
        operator = expr.op

        if operator == BinOperator.Add:
            return left_value + right_value
        elif operator == BinOperator.Sub:
            return left_value - right_value
        elif operator == BinOperator.Mul:
            return left_value * right_value

    elif isinstance(expr, UnOp):
        operand_value = evaluate_expr(expr.operand, context)
        operator = expr.operator

        if operator == UnOperator.Neg:
            return -operand_value

    elif isinstance(expr, Var):
        return context.get_variable(expr)

    return None


def evaluate_statement(statement, context):
    if isinstance(statement.expr, Assignment):
        variable = statement.expr.variable
        value = evaluate_expr(statement.expr.value, context)
        context.assign_variable(variable, value)

    elif isinstance(statement.expr, Assertion):
        expression = statement.expr.expression
        result = evaluate_expr(expression, context)
        # TODO

    elif isinstance(statement.expr, IfElse):
        condition = statement.expr.condition
        if_body = statement.expr.if_body
        else_body = statement.expr.else_body

        condition_result = evaluate_expr(condition, context)
        if condition_result:
            evaluate_block(if_body, context)
        else:
            evaluate_block(else_body, context)

    elif isinstance(statement.expr, Expr):
        evaluate_expr(statement.expr, context)

    else:
        # Handle unsupported statement types
        pass


def evaluate_block(block, context):
    for statement in block.statements:
        evaluate_statement(statement, context)
