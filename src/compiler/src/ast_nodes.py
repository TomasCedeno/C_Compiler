class Node:
    def __init__(self, node_type):
        self.node_type = node_type
        self.children = []

    def add_child(self, child_node):
        self.children.append(child_node)

    def show_structure(self):
        print(self.node_type)
        for child in self.children:
            if isinstance(child, Node):
                print("\t\t", end="")
                child.show_structure()
            else:
                print("\t\t", end="")
                print(child, end="")
            print("\t")

class Declaration(Node):
    def __init__(self, type_specifier, identifier):
        super().__init__("Declaration")
        self.type_specifier = type_specifier
        self.identifier = identifier
        self.children = [self.type_specifier, self. identifier]

class TypeSpecifier(Node):
    def __init__(self, type_name):
        super().__init__("TypeSpecifier")
        self.type_name = type_name
    
    def show_structure(self):
        print(f"TypeSpecifier ({self.type_name})")

class FunctionDeclaration(Node):
    def __init__(self, return_type, function_name, parameters, body):
        super().__init__("FunctionDeclaration")
        self.return_type = return_type
        self.function_name = function_name
        self.parameters = parameters
        self.body = body
        self.children = [self.return_type, self.function_name, self.parameters, self.body]

class Parameters(Node):
    def __init__(self):
        super().__init__("Parameters")

class Parameter(Node):
    def __init__(self, param_type, param_name):
        super().__init__("Parameter")
        self.param_type = param_type
        self.param_name = param_name
        self.children = [self.param_type, self.param_name]

class Block(Node):
    def __init__(self, statements):
        super().__init__("Block")
        self.statements = statements
        self.children = self.statements

class Assignment(Node):
    def __init__(self, left, right):
        super().__init__("Assignment")
        self.left = left
        self.right = right
        self.children = [self.left, self.right]

class Identifier(Node):
    def __init__(self, name):
        super().__init__("Identifier")
        self.name = name

    def show_structure(self):
        print(f"Identifier ({self.name})")

class LiteralNumber(Node):
    def __init__(self, value):
        super().__init__("IntegerLiteral")
        self.value = value
    
    def show_structure(self):
        print(f"IntegerLiteral ({self.value})")

class LiteralString(Node):
    def __init__(self, value):
        super().__init__("StringLiteral")
        self.value = value

    def show_structure(self):
        print(f"StringLiteral ({self.value})")


class Condition(Node):
    def __init__(self, operator, left, right):
        super().__init__("Condition")
        self.operator = operator
        self.left = left
        self.right = right
        self.children = [self.left, self.right]

    def show_structure(self):
        print(f"Condition ({self.operator})")
        for child in self.children:
            if isinstance(child, Node):
                print("\t\t", end="")
                child.show_structure()
            else:
                print("\t\t", end="")
                print(child, end="")
            print("\t")

class Operation(Node):
    def __init__(self, operator, left, right):
        super().__init__("Operation")
        self.operator = operator
        self.left = left
        self.right = right
        self.children = [self.left, self.right]

    def show_structure(self):
        print(f"Operation ({self.operator})")
        for child in self.children:
            if isinstance(child, Node):
                print("\t\t", end="")
                child.show_structure()
            else:
                print("\t\t", end="")
                print(child, end="")
            print("\t")

class IfConditional(Node):
    def __init__(self, condition, body):
        super().__init__("IfConditional")
        self.condition = condition
        self.body = body
        self.children = [self.condition, self.body]

class WhileLoop(Node):
    def __init__(self, condition, body):
        super().__init__("WhileLoop")
        self.condition = condition
        self.body = body
        self.children = [self.condition, self.body]

class ForLoop(Node):
    def __init__(self, assignment, condition, increment, body):
        super().__init__("ForLoop")
        self.assignment = assignment
        self.condition = condition
        self.increment = increment
        self.body = body
        self.children = [self.assignment, self.condition, self.increment, self.body]

class ReturnStatement(Node):
    def __init__(self, value):
        super().__init__("ReturnStatement")
        self.value = value
        self.children = [self.value]

class FunctionCall(Node):
    def __init__(self, function_name, parameters):
        super().__init__("FunctionCall")
        self.function_name = function_name
        self.parameters = parameters
        self.children = [self.function_name, self.parameters]

class DefinePreDirective(Node):
    def __init__(self, identifier, value):
        super().__init__("DefinePreprocessorDirective")
        self.ididentifier =identifier
        self.vavalue =value
        self.children = [self.ididentifier, self.vavalue]

class IncludePreDirective(Node):
    def __init__(self, value):
        super().__init__("IncludePreDirective")
        self.value = value

    def show_structure(self):
        print(f"IncludePreDirective ({self.value})")