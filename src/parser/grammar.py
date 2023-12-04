# pylint: disable=missing-docstring, attribute-defined-outside-init

"""
Classes that represent grammar rules for our Parse Tree.
"""

from util import unique


def parseToken(desc, content="", children=None):
    """Parse a token into the relevant class."""

    # Check if the node is a terminal
    if desc in terminals:
        return terminals[desc](content)

    # Check if the node exists
    if desc in nodes:
        return nodes[desc](children)

    # Did not match any of the known parse tree nodes.
    # Classify it as a "general"  node
    return None


def printPrefix(level):
    """Print a prefix level deep for pretty printing."""

    for _ in range(level):
        print("  ", end=" ")
    print("| - ", end=" ")


class Node:
    """General parse tree node class"""

    def __init__(self, *children):
        self.value = None

        if len(children) == 1:
            self.children = children[0]
        else:
            self.children = children

    def __str__(self):
        return self.__class__.__name__

    def print(self, level=0):
        """
        General node print method.
        First, print the class name, then print all its children.

        This method is overriden at lower level nodes like ConstNum.
        """

        printPrefix(level)
        print(self.__class__.__name__)

        if isinstance(self.children, list):
            for child in self.children:
                child.print(level + 1)
        else:
            for child in self.children[0]:
                child.print(level + 1)

    # pylint: disable=no-self-use
    def ir(self):
        return None

    def prepare(self):
        return None

    # pylint: enable=no-self-use

    def visit(self):
        if hasattr(self, "children"):
            for child in self.children:
                child.visit()

        self.prepare()


# Parse Tree Node Classes


class Program(Node):
    pass


class DeclarationList(Node):
    pass


class Declaration(Node):
    pass


class FunctionDeclaration(Node):
    def __init__(self, children):
        self.children = children
        self.type = self.children[0].value
        self.name = self.children[1].value
        self.arguments = self.children[2]


class Arguments(Node):
    def prepare(self):
        s = []
        for i in self.children:
            s.append(i.name)

        self.value = s


class Argument(Node):
    def __init__(self, children):
        self.children = children
        self.type = children[0].value
        if len(children) > 1:
            self.name = children[1].value
        # added this for the case "main(void)"
        else:
            self.name = "None"


class Parameters(Node):
    def prepare(self):
        s = []
        for i in self.children:
            s.append(i.value)

        self.value = s


class Parameter(Node):
    def __init__(self, children):
        self.children = children
        self.value = children[0].value


class StatementList(Node):
    pass


class Statement(Node):
    pass


class StatementListNew(Node):
    pass


class StatementNew(Node):
    pass


class ReturnStatement(Node):
    def prepare(self):
        self.expr = self.children[0]

    def ir(self):
        return ["ret", self.expr.value]


class VariableDeclaration(Node):
    def __init__(self, children):
        self.children = children
        self.type = children[0].value
        self.name = children[1].value

        # If this VarDec is also assigned
        if len(self.children) == 3:
            self.expr = self.children[2]

    def ir(self):
        if len(self.children) == 3:
            return [self.name, "=", self.expr.children[0].value]

        return None


class LabelDeclaration(Node):
    def prepare(self):
        self.value = self.children[0].value

    def ir(self):
        return ["label", self.value]


# Assignments


class VariableAssignment(Node):
    def __init__(self, children):
        self.children = children
        self.name = children[0].name

    def ir(self):
        recent = unique.count["none"]
        return [self.name, "=", f"r{recent}"]


class IncrementAssignment(Node):
    def __init__(self, children):
        self.children = children
        self.name = self.children[0].value

    def ir(self):
        self.value = unique.new()
        return [self.value, "=", self.name, "+", "1"]


class DecrementAssignment(Node):
    def __init__(self, children):
        self.children = children
        self.name = self.children[0].value

    def ir(self):
        self.value = unique.new()
        return [self.value, "=", self.name, "-", "1"]


class PlusEqualAssignment(Node):
    def __init__(self, children):
        self.children = children
        self.name = self.children[0].value
        self.expr = self.children[1]

    def ir(self):
        self.value = unique.new()
        return [self.value, "=", self.name, "+", self.expr.value]


class MinusEqualAssignment(Node):
    def __init__(self, children):
        self.children = children
        self.name = self.children[0].value
        self.expr = self.children[1]

    def ir(self):
        self.value = unique.new()
        return [self.value, "=", self.name, "-", self.expr.value]


class MultEqualAssignment(Node):
    def __init__(self, children):
        self.children = children
        self.name = self.children[0].value
        self.expr = self.children[1]

    def ir(self):
        self.value = unique.new()
        return [self.value, "=", self.name, "*", self.expr.value]


class DivEqualAssignment(Node):
    def __init__(self, children):
        self.children = children
        self.name = self.children[0].value
        self.expr = self.children[1]

    def ir(self):
        self.value = unique.new()
        return [self.value, "=", self.name, "/", self.expr.value]


class CallAssignment(Node):
    def __init__(self, children):
        self.children = children
        self.name = self.children[0].value
        self.expr = self.children[1]

    def ir(self):
        self.value = unique.new()
        return f"{self.value} = call {self.name} - {self.expr.value}"


class ExpressionAssignment(Node):
    def __init__(self, children):
        self.children = children
        self.name = self.children[0].value
        self.expr = self.children[1]

    def ir(self):
        self.value = unique.new()
        return [self.value, "=", self.expr.value]


# Expressions


class Expression(Node):
    def prepare(self):
        self.value = self.children[0].value


class NestedExpression(Node):
    def prepare(self):
        self.value = self.children[0].value


class MathExpression(Node):
    def prepare(self):
        self.value = unique.new()
        self.a = self.children[0].value
        self.b = self.children[1].value


class AdditionExpression(MathExpression):
    def ir(self):
        return [self.value, "=", self.a, "+", self.b]


class SubtractionExpression(MathExpression):
    def ir(self):
        return [self.value, "=", self.a, "-", self.b]


class MultiplicationExpression(MathExpression):
    def ir(self):
        return [self.value, "=", self.a, "*", self.b]


class DivisionExpression(MathExpression):
    def ir(self):
        return [self.value, "=", self.a, "/", self.b]


class ModulusExpression(MathExpression):
    def ir(self):
        return [self.value, "=", self.a, "%", self.b]


class BooleanAnd(MathExpression):
    def ir(self):
        return [self.value, "=", self.a, "&&", self.b]


class BooleanOr(MathExpression):
    def ir(self):
        return [self.value, "=", self.a, "||", self.b]


class BooleanNot(Node):
    def ir(self):
        self.value = unique.new()
        return [self.value, "=", "!", self.children[0].value]


class ComparisonExpression(Node):
    def prepare(self):
        self.value = unique.new()
        self.a = self.children[0].value
        self.b = self.children[1].value


class LTOEExpression(ComparisonExpression):
    def ir(self):
        return [self.value, "=", self.a, "<=", self.b]


class GTOEExpression(ComparisonExpression):
    def ir(self):
        return [self.value, "=", self.a, ">=", self.b]


class LTExpression(ComparisonExpression):
    def ir(self):
        return [self.value, "=", self.a, "<", self.b]


class GTExpression(ComparisonExpression):
    def ir(self):
        return [self.value, "=", self.a, ">", self.b]


class NotEqualExpression(ComparisonExpression):
    def ir(self):
        return [self.value, "=", self.a, "!=", self.b]


class EqualExpression(ComparisonExpression):
    def ir(self):
        return [self.value, "=", self.a, "==", self.b]


# Statements


class ForStatement(Node):
    pass


class WhileStatement(Node):
    def ir(self):
        return ["while", self.children[0].ir()]


class WhileCondition(Node):
    def prepare(self):
        self.value = self.children[0].value


class BreakStatement(Node):
    def ir(self):
        return ["break"]


class ContinueStatement(Node):
    def ir(self):
        return ["continue"]


class IncludeStatement(Node):
    pass


class CallStatement(Node):
    def __init__(self, children):
        self.children = children
        self.name = self.children[0].value
        self.parameters = self.children[1]

    def prepare(self):
        self.value = unique.new()

    def ir(self):
        return ["call", self.value, "=", self.name, self.parameters.value]


class GotoStatement(Node):
    def ir(self):
        self.value = self.children[0].value
        return ["goto", self.value]


class IfStatement(Node):
    def __init__(self, children):
        self.children = children
        self.condition = self.children[0]
        self.body = self.children[1]

        if len(self.children) > 2:
            self.hasElse = True
            self.body.hasElse = True
        else:
            self.hasElse = False
            self.body.hasElse = False


class IfBody(Node):
    pass


class Condition(Node):
    def prepare(self):
        self.value = self.children[0].value


class ElseStatement(Node):
    pass


class SwitchStatement(Node):
    def prepare(self):
        self.value = self.children[0].value

        for case in self.children[1].children:
            case.operator = self.value


class SwitchCaseList(Node):
    pass


class SwitchCase(Node):
    def prepare(self):
        self.value = self.children[0].value


class SwitchCondition(Node):
    def prepare(self):
        self.value = self.children[0].value


class BitAnd(MathExpression):
    def ir(self):
        return [self.value, "=", self.a, "&", self.b]


class BitOr(MathExpression):
    def ir(self):
        return [self.value, "=", self.a, "|", self.b]


class BitXor(MathExpression):
    def ir(self):
        return [self.value, "=", self.a, "^", self.b]


class BitNot(Node):
    def ir(self):
        self.value = unique.new()
        return [self.value, "=", "~", self.children[0].value]


class LeftShift(MathExpression):
    def ir(self):
        return [self.value, "=", self.a, "<<", self.b]


class RightShift(MathExpression):
    def ir(self):
        return [self.value, "=", self.a, ">>", self.b]


class EnumStatement(Node):
    pass


class EnumList(Node):
    pass


class StructStatement(Node):
    pass


class StructList(Node):
    pass


class StructDec(Node):
    pass


class VarList(Node):
    pass


# A dictionary of all the parse tree nodes we recognize
# Key: string of the grammar rule
# Value: the associated class

nodes = {
    "program": Program,
    "declarationList": DeclarationList,
    "declaration": Declaration,
    "varDec": VariableDeclaration,
    "assignment": VariableAssignment,
    "exprAssignment": ExpressionAssignment,
    "callAssignment": CallAssignment,
    "incAssignment": IncrementAssignment,
    "decAssignment": DecrementAssignment,
    "incEqualAssignment": PlusEqualAssignment,
    "decEqualAssignment": MinusEqualAssignment,
    "multEqualAssignment": MultEqualAssignment,
    "divEqualAssignment": DivEqualAssignment,
    "functionDeclaration": FunctionDeclaration,
    "labelDeclaration": LabelDeclaration,
    "argList": Arguments,
    "arg": Argument,
    "statementList": StatementList,
    "statementListNew": StatementList,
    "statement": Statement,
    "statementNew": Statement,
    "returnStatement": ReturnStatement,
    "forStatement": ForStatement,
    "whileStatement": WhileStatement,
    "whileCondition": WhileCondition,
    "includeStatement": IncludeStatement,
    "callStatement": CallStatement,
    "gotoStatement": GotoStatement,
    "paramList": Parameters,
    "param": Parameter,
    "ifStatement": IfStatement,
    "ifBody": IfBody,
    "condition": Condition,
    "elseStatement": ElseStatement,
    "expression": Expression,
    "nestedExpr": NestedExpression,
    "addExpr": AdditionExpression,
    "subExpr": SubtractionExpression,
    "multExpr": MultiplicationExpression,
    "divExpr": DivisionExpression,
    "modExpr": ModulusExpression,
    "boolAnd": BooleanAnd,
    "boolOr": BooleanOr,
    "boolNot": BooleanNot,
    "lteExpr": LTOEExpression,
    "gteExpr": GTOEExpression,
    "ltExpr": LTExpression,
    "gtExpr": GTExpression,
    "neExpr": NotEqualExpression,
    "eExpr": EqualExpression,
    "breakStatement": BreakStatement,
    "continueStatement": ContinueStatement,
    "switchStatement": SwitchStatement,
    "caseList": SwitchCaseList,
    "switchCase": SwitchCase,
    "switchCondition": SwitchCondition,
    "bitAnd": BitAnd,
    "bitOr": BitOr,
    "bitXor": BitXor,
    "bitNot": BitNot,
    "leftShift": LeftShift,
    "rightShift": RightShift,
    "enumStatement": EnumStatement,
    "enumList": EnumList,
    "structStatement": StructStatement,
    "structList": StructList,
    "structDec": StructDec,
    "varList": VarList,
}

# Terminal Nodes


class TypeSpecifier(Node):
    """Type specifier node."""

    def __init__(self, value):
        self.value = value

    def print(self, level=0):
        printPrefix(level)
        print(f"{self.__class__.__name__}: {self.value}")


class ConstNum(Node):
    """Number constant node."""

    def __init__(self, value):
        self.value = value

    def print(self, level=0):
        printPrefix(level)
        print(f"{self.__class__.__name__}: {self.value}")


class Identifier(Node):
    """ID node."""

    def __init__(self, value):
        self.value = value

    def print(self, level=0):
        printPrefix(level)
        print(f"{self.__class__.__name__}: {self.value}")


class Filename(Node):
    """Filename node."""

    def __init__(self, value):
        self.value = value

    def print(self, level=0):
        printPrefix(level)
        print(f"{self.__class__.__name__}: {self.value}")


class String(Node):
    """String node."""

    def __init__(self, value):
        self.value = value

    def print(self, level=0):
        printPrefix(level)
        print(f"{self.__class__.__name__}: {self.value}")


class Label(Node):
    """Label node."""

    def __init__(self, value):
        self.value = value

    def print(self, level=0):
        printPrefix(level)
        print(f"{self.__class__.__name__}: {self.value}")


# A dictionary of all the terminal parse tree nodes we recognize
# Key: string of the grammar rule
# Value: the associated class

terminals = {
    "typeSpecifier": TypeSpecifier,
    "ID": Identifier,
    "constNum": ConstNum,
    "fileName": Filename,
    "str": String,
    "label": Label,
}
