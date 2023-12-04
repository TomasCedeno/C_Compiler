from lexical_analyzer import lexical_analysis, Token
import ast_nodes as ast


TYPE_IDENTIFIER = "Identifier"
TYPE_LITERAL_STRING = "Literal_String"
TYPE_LITERAL_NUMBER = "Literal_Number"
OPERAND_TYPES = [TYPE_IDENTIFIER, TYPE_LITERAL_NUMBER, TYPE_LITERAL_STRING]

OPEN_PARENTHESIS = "("
CLOSE_PARENTHESIS = ")"
OPEN_CURLY_BRACKET = "{"
CLOSE_CURLY_BRACKET = "}"

SEMICOLON = ";"
COMMA = ","

ADD_OPERATOR = 'Addition_Operator'
SUBTRACT_OPERATOR = 'Subtraction_Operator'
MULTIPLY_OPERATOR = 'Multiplication_Operator'
DIVIDE_OPERATOR = 'Division_Operator'
MOD_OPERATOR = 'Modulus_Operator'
ARITHMETIC_OPERATORS = [ADD_OPERATOR, SUBTRACT_OPERATOR, MULTIPLY_OPERATOR, DIVIDE_OPERATOR, MOD_OPERATOR]

DATA_TYPE_SPECIFIERS = ['int', 'float', 'char']

ASSIGN_OPERATOR = 'Assignment_Operator'
ADD_ASSIGN_OPERATOR = 'Addition_Assignment_Operator'
SUBTRACT_ASSIGN_OPERATOR = 'Subtraction_Assignment_Operator'
MULTIPLY_ASSIGN_OPERATOR = 'Multiplication_Assignment_Operator'
DIVIDE_ASSIGN_OPERATOR = 'Division_Assignment_Operator'
MOD_ASSIGN_OPERATOR = 'Modulus_Assignment_Operator'
ASSIGN_OPERATORS = [ASSIGN_OPERATOR, ADD_ASSIGN_OPERATOR, SUBTRACT_ASSIGN_OPERATOR, MULTIPLY_ASSIGN_OPERATOR, DIVIDE_ASSIGN_OPERATOR, MOD_ASSIGN_OPERATOR]

LOGIC_OPERATORS = ['==', '!=', '<=', '>=', '<', '>', '&&', '||']

KEY_WORD_RETURN = "return"

def get_precedence(operator):
    """Retorna el nivel de precedncia para cada operador"""
    if operator in [MULTIPLY_OPERATOR, DIVIDE_OPERATOR, MOD_OPERATOR]:
        return 2

    if operator in [ADD_OPERATOR, SUBTRACT_OPERATOR]:
        return 1

    return 0


def get_logic_precedence(operator):
    """Retorna el nivel de precedncia para cada operador logico"""
    if operator in ['&&', '||']:
        return 3

    if operator in ['<=', '>=', '<', '>']:
        return 2

    if operator in ['==', '!=']:
        return 1

    return 0

class InvalidSyntaxException(Exception):
    """Lanzado cuando hay un error de sintaxis.
    
    Attributes:
        token -- token que generó el error.

        message -- explicacion del error.
    """
    
    def __init__(self, token, message=""):
        self.salary = token
        self.message = message
        super().__init__(f"Error de sintaxis, token: {token.token}, linea: {token.line_number}. \n{message}")



#Retorna el siguiente token de la lista y permite ubicar el iterador en una posición especifica
tokenIndex = 0
tokens = []

def get_next_token(index = None) -> Token:
    """Itera sobre los tokens, retorna el siguiente token en lista."""
    global tokenIndex
    if index != None:
        tokenIndex = index
 
    if tokenIndex < len(tokens):
        token = tokens[tokenIndex]
        tokenIndex += 1
        return token

    return None



def parse_operand(token):
    """Retorna el nodo de un identificador, numero o string en caso de que lo identifique en el token, 
    caso contrario retorna False."""
    if token.token_type == TYPE_IDENTIFIER:
        return ast.Identifier(token.token)

    elif token.token_type == TYPE_LITERAL_STRING:
        return ast.LiteralString(token.token)
    
    elif token.token_type == TYPE_LITERAL_NUMBER:
        return ast.LiteralNumber(token.token)

    else:
        return False


def parse_arithmetic_expression():
    """Retorna un nodo operación, identificador, numero o string.
    \nRetorna False si no identifica una expresion y devuelve el iterador a la psición en la que estaba.
    \nLanza una excepción de sintaxis si la identifica."""
    global tokenIndex
    startIndex = tokenIndex
 
    #Recolecta los tokens correspondientes a la operacion
    operationTokens = []
    while True:
        token = get_next_token()
        if token != None and (token.token_type in (ARITHMETIC_OPERATORS+OPERAND_TYPES) or token.token in [OPEN_PARENTHESIS, CLOSE_PARENTHESIS]):
            operationTokens.append(token)
        else:
            tokenIndex -= 1 #Se deja el iterador en el token despues de la operacion
            break

    #Verifica la sntaxis
    try:
        for i, token in enumerate(operationTokens):
            if (
                token.token_type in ARITHMETIC_OPERATORS 
                and ((operationTokens[i-1].token_type not in OPERAND_TYPES and operationTokens[i-1].token != CLOSE_PARENTHESIS)
                    or (operationTokens[i+1].token_type not in OPERAND_TYPES and operationTokens[i+1].token != OPEN_PARENTHESIS)
                )
            ):
                raise InvalidSyntaxException(token)

            elif (token.token_type in OPERAND_TYPES and (i+1) < len(operationTokens)):
                if (operationTokens[i+1].token_type in OPERAND_TYPES or operationTokens[i+1].token == OPEN_PARENTHESIS):
                    raise InvalidSyntaxException(token)

    except IndexError:
        raise InvalidSyntaxException(token)

    #Identifica de manera recursiva la expresion aritmetica
    def parse_expression(operationTokens):
        if len(operationTokens) == 1:
            if parse_operand(operationTokens[0]):
                return parse_operand(operationTokens[0])
            else:
                raise InvalidSyntaxException(token)

        precedenceLevel = 0
        operatorIndex = -1
        openedParenthesis = 0

        for i, token in enumerate(operationTokens):
            if token.token == "(":
                openedParenthesis += 1
            elif token.token == ")":
                openedParenthesis -= 1

            if token.token_type in ARITHMETIC_OPERATORS and openedParenthesis == 0:
                if get_precedence(token.token) >= precedenceLevel:
                    precedenceLevel = get_precedence(token.token)
                    operatorIndex = i

        if operatorIndex != -1:
            operator = operationTokens[operatorIndex].token
            left = parse_expression(operationTokens[:operatorIndex])
            right = parse_expression(operationTokens[operatorIndex + 1:])
            return ast.Operation(operator, left, right)

        else:
            if operationTokens[0].token == "(" and operationTokens[-1].token == ")":
                return parse_expression(operationTokens[1:-1])
            else:
                print("DONT KNOW WHAT TO DO IN HERE") #Nodo(tokens[0])

    return parse_expression(operationTokens)



def parse_assignment():
    """Retorna nodo asignacion si la identifica y cumple con la sintaxis.
    \nRetorna False si no identifica una asignacion y devuelve el iterador a la posición en la que estaba.
    \nLanza una excepción de sintaxis si la identifica."""
    global tokenIndex
    startIndex = tokenIndex

    #Lado Izquierdo
    token = get_next_token()
    if token.token_type == "Identifier":
        left = ast.Identifier(token.token)
    else:
        tokenIndex = startIndex
        return False

    #Lado Derecho
    operator = get_next_token()
    if operator.token_type == ASSIGN_OPERATOR:
        right = parse_arithmetic_expression()

    elif operator.token_type in ASSIGN_OPERATORS:
        right = ast.Operation(operator.token[0], left, parse_arithmetic_expression())

    else:
        tokenIndex = startIndex
        return False

    #Se reorna el nodo o s elanza excepcion si no hay punto y coma
    token = get_next_token()
    if token.token == SEMICOLON:
        return ast.Assignment(left, right)

    else:
        raise InvalidSyntaxException(token, "Se esperaba punto y coma.")



def parse_increment_decrement():
    """Retorna nodo asiganción con incremente/decremento o si no identifica sintaxis retorna False y devuelve iterador a la posición en la que estaba."""
    global tokenIndex
    startIndex = tokenIndex
    token = get_next_token()

    if token.token_type == TYPE_IDENTIFIER:
        left = ast.Identifier(token.token)
    else:
        tokenIndex = startIndex
        return False

    operator = get_next_token()

    if (operator.token in ["++", "--"]):
        right = ast.Operation(operator.token[0], left, ast.LiteralNumber(1))
    else:
        tokenIndex = startIndex
        return False

    return ast.Assignment(left, right)


def parse_declaration():
    """Retorna nodo declaracion si la identifica y cumple con la sintaxis.
    \nRetorna False si no identifica una declaracion y devuelve el iterador a la psición en la que estaba.
    \nLanza una excepción de sintaxis si la identifica."""
    global tokenIndex
    startIndex = tokenIndex
    token = get_next_token()

    #Tipo de dato
    if token.token_type in DATA_TYPE_SPECIFIERS:
        dataType = ast.TypeSpecifier(token.token)
    else:
        tokenIndex = startIndex
        return False

    #Identificador
    token = get_next_token()
    if token.token_type == TYPE_IDENTIFIER:
        identifier = ast.Identifier(token.token)
    else:
        tokenIndex = startIndex
        return False

    #Se verfica posible asignacion
    tokenIndex -= 1 #Se pone iterador en posicion de identificador
    if assignment := parse_assignment():
        return [ast.Declaration(dataType, identifier), assignment]

    tokenIndex += 1 #Se pone iterador despues de identificador
    token = get_next_token()
    if token.token == SEMICOLON:
        return ast.Declaration(dataType, identifier)
    else:
        raise InvalidSyntaxException(token, "Se es peraba punto y coma.")



def parse_logic_expression():
    """Retorna un nodo condicion, identificador, numero o string.
    \nRetorna False si no identifica una expresion y devuelve el iterador a la psición en la que estaba.
    \nLanza una excepción de sintaxis si la identifica."""
    global tokenIndex
    startIndex = tokenIndex
 
    #Recolecta los tokens correspondientes a la operacion logica
    operationTokens = []
    while True:
        token = get_next_token()
        if token != None and (token.token_type in OPERAND_TYPES or token.token in LOGIC_OPERATORS+[OPEN_PARENTHESIS, CLOSE_PARENTHESIS]):
            operationTokens.append(token)
        else:
            tokenIndex -= 1 #Se deja el iterador en el token despues de la operacion
            break

    #Verifica la sntaxis
    try:
        for i, token in enumerate(operationTokens):
            if (
                token.token in LOGIC_OPERATORS 
                and ((operationTokens[i-1].token_type not in OPERAND_TYPES and operationTokens[i-1].token != CLOSE_PARENTHESIS)
                    or (operationTokens[i+1].token_type not in OPERAND_TYPES and operationTokens[i+1].token != OPEN_PARENTHESIS)
                )
            ):
                raise InvalidSyntaxException(token)

            elif (token.token_type in OPERAND_TYPES and (i+1) < len(operationTokens)):
                if (operationTokens[i+1].token_type in OPERAND_TYPES or operationTokens[i+1].token == OPEN_PARENTHESIS):
                    raise InvalidSyntaxException(token)

    except IndexError:
        raise InvalidSyntaxException(token)

    #Identifica de manera recursiva la expresion logica
    def parse_expression(operationTokens):
        if len(operationTokens) == 1:
            if parse_operand(operationTokens[0]):
                return parse_operand(operationTokens[0])
            else:
                raise InvalidSyntaxException(token)

        precedenceLevel = 0
        operatorIndex = -1
        openedParenthesis = 0

        for i, token in enumerate(operationTokens):
            if token.token == "(":
                openedParenthesis += 1
            elif token.token == ")":
                openedParenthesis -= 1

            if token.token in LOGIC_OPERATORS and openedParenthesis == 0:
                if get_logic_precedence(token.token) >= precedenceLevel:
                    precedenceLevel = get_logic_precedence(token.token)
                    operatorIndex = i

        if operatorIndex != -1:
            operator = operationTokens[operatorIndex].token
            left = parse_expression(operationTokens[:operatorIndex])
            right = parse_expression(operationTokens[operatorIndex + 1:])
            return ast.Condition(operator, left, right)

        else:
            if operationTokens[0].token == "(" and operationTokens[-1].token == ")":
                return parse_expression(operationTokens[1:-1])
            else:
                print("DONT KNOW WHAT TO DO IN HERE") #Nodo(tokens[0])

    return parse_expression(operationTokens)


def parse_function_call():
    """Retorna un nodo function call si identifica la sintaxis de llamada a una funcion.
    \nRetorna False y devuelve el iterador a la posicion en la que estaba si no identifica la sintaxis.
    \nLanza error de sintaxis si hay."""
    global tokenIndex
    startIndex = tokenIndex
    functionName = get_next_token()

    if functionName.token_type == TYPE_IDENTIFIER:
        parameters = ast.Parameters()
        token = get_next_token()

        if token.token == OPEN_PARENTHESIS:
            while (token := get_next_token()).token != CLOSE_PARENTHESIS:
                if token.token == COMMA:
                    token = get_next_token()

                operand = parse_operand(token)
                if operand:
                    parameters.add_child(operand)
                else:
                    raise InvalidSyntaxException(token, "Error de sintaxis en parametros.")

            if (get_next_token().token == SEMICOLON):
                return ast.FunctionCall(ast.Identifier(functionName.token), parameters)
            else:
                raise InvalidSyntaxException(token, "Se esperaba punto y coma.")

        else:
            tokenIndex = startIndex
            return False

    else:
        tokenIndex = startIndex
        return False



def parse_block():
    """Retorna un nodo bloque si identifica la sintaxis de un bloque.
    \nLanza error de sintaxis si hay."""
    global tokenIndex
    startIndex = tokenIndex

    token = get_next_token()
    statements = []
    if token.token == OPEN_CURLY_BRACKET:
        while (token := get_next_token()).token != CLOSE_CURLY_BRACKET:
            tokenIndex -= 1
            startIndex = tokenIndex

            #Declaraciones
            if (statement := parse_declaration()) != False:      
                if isinstance(statement, list):
                    statements.extend(statement)
                else:
                    statements.append(statement)
                continue

            #Asignaciones
            if (statement := parse_assignment()) != False:
                statements.append(statement)
                continue

            #Incremento o Decremento
            if (statement := parse_increment_decrement()) != False and (get_next_token().token == SEMICOLON):
                statements.append(statement)
                continue

            #Condicional if o bucle while
            if (statement := parse_if_while()) != False:
                statements.append(statement)
                continue

            #Bucle for
            if (statement := parse_for()) != False:
                statements.append(statement)
                continue
            
            #Sentencia return
            if get_next_token().token == KEY_WORD_RETURN:
                if (value := parse_operand(get_next_token())) and (get_next_token().token == SEMICOLON):
                    statements.append(ast.ReturnStatement(value))
                    continue
                else:
                    raise InvalidSyntaxException(token)
            else:
                tokenIndex -= 1

            #Llamado a funcion
            if (statement := parse_function_call()) != False:
                statements.append(statement)
                continue
            
            raise InvalidSyntaxException(token)

    #Si cumple con las reglas gramticales de bloques
    return ast.Block(statements)


def parse_if_while():
    """Retorna nodo if o while si identifica la sintaxis.
    \nRetorna False si no identifca la sintaxis.
    \nLanza exception de sintaxis si la identifica."""
    global tokenIndex
    startIndex = tokenIndex

    token = get_next_token()
    if token.token not in ["if", "while"]:
        tokenIndex = startIndex
        return False

    struct = token.token

    #Condición
    if get_next_token().token == OPEN_PARENTHESIS:
        tokenIndex -= 1
        condition = parse_logic_expression()

    #Contenido del condicional
    body = parse_block()

    return ast.IfConditional(condition, body) if struct == "if" else ast.WhileLoop(condition, body)


def parse_for():
    """Retorna nodo for si identifica la sintaxis.
    \nRetorna False si no identifca la sintaxis.
    \nLanza exception de sintaxis si la identifica."""
    global tokenIndex
    startIndex = tokenIndex

    token = get_next_token()
    if token.token != "for":
        tokenIndex = startIndex
        return False

    #Asignación
    if get_next_token().token != OPEN_PARENTHESIS or ((assignment := parse_declaration())==False and (assignment := parse_assignment())==False):
        raise InvalidSyntaxException(token)
    else:
        if isinstance(assignment, list):
            node = ast.Node("DeclarationAssignmet")
            node.children = assignment
            assignment = node
   
    #Condicion
    if (condition := parse_logic_expression()) == False or get_next_token().token != SEMICOLON:
        raise InvalidSyntaxException(token)

    #Incremento
    if (increment := parse_increment_decrement()) == False or get_next_token().token != CLOSE_PARENTHESIS:
        raise InvalidSyntaxException(token)

    #Bloque
    body = parse_block()

    return ast.ForLoop(assignment, condition, increment, body)



def parse_function_declaration():
    """Retorna nodo function si identifica la sintaxis.
    \nRetorna False si no identifca la sintaxis y devuelve el iterador a la posicion en la que estaba.
    \nLanza exception de sintaxis si la identifica."""
    global tokenIndex
    startIndex = tokenIndex
    dataTypes = ["int", "float", "char", "void"]

    #Tipo de retorno
    token = get_next_token()
    if token.token in dataTypes:
        returnType = ast.TypeSpecifier(token.token)
    else:
        tokenIndex = startIndex
        return False

    #Nombre de funcion
    token = get_next_token()
    if token.token_type == TYPE_IDENTIFIER:
        functionName = ast.Identifier(token.token)
    else:
        tokenIndex = startIndex
        return False

    #Parametros
    parameters = ast.Parameters()
    token = get_next_token()
    if token.token == OPEN_PARENTHESIS:
        while (token := get_next_token()).token != CLOSE_PARENTHESIS:
            if token.token == COMMA:
                token = get_next_token()

            dataType = token
            identifier = get_next_token()
            if dataType.token in dataTypes and identifier.token_type == TYPE_IDENTIFIER:
                parameters.add_child(ast.Parameter(ast.TypeSpecifier(dataType.token), ast.Identifier(identifier.token)))
            else:
                raise InvalidSyntaxException(token, "Error de sintaxis en parametros.")
    else:
        raise InvalidSyntaxException(token, "Se esperaba parentesis.")

    
    #Contenido de la funcion
    body = parse_block()

    #Si cumplio con las reglas gramaticales de la declaración de función retorna el nodo
    return ast.FunctionDeclaration(returnType, functionName, parameters, body)


def parse_preprocessor_directives():
    """Retorna nodo function si identifica la sintaxis.
    \nRetorna False si no identifca la sintaxis y devuelve el iterador a la posicion en la que estaba.
    \nLanza exception de sintaxis si la identifica."""
    global tokenIndex
    startIndex = tokenIndex
    token = get_next_token()

    if token.token == "#define":
        identifier = get_next_token()
        value = get_next_token()
        if identifier.token_type == TYPE_IDENTIFIER and value.token_type in [TYPE_LITERAL_NUMBER, TYPE_LITERAL_STRING]:
            return ast.DefinePreDirective(ast.Identifier(identifier.token), parse_operand(value))
        else:
            raise InvalidSyntaxException(token)

    elif token.token == "#include":
        value = get_next_token()
        if value.token_type == TYPE_LITERAL_STRING:
            return ast.IncludePreDirective(value.token)
        else:
            raise InvalidSyntaxException(token)

    else:
        tokenIndex = startIndex
        return False



def syntax_analysis(tokensInput):
    global tokens
    global tokenIndex
    tokens = tokensInput
    program = ast.Node("Program")

    try:
        while tokenIndex < len(tokens):
            startIndex = tokenIndex

            #Directivas de preprocesador
            if (directive := parse_preprocessor_directives()) != False:
                program.add_child(directive)
                continue

            #Declaracion de Funcion
            if (function := parse_function_declaration()) != False:
                program.add_child(function)
                continue

            #If o While
            if (struct := parse_if_while()) != False:
                program.add_child(struct)
                continue

            #Bucle For
            if (forLoop := parse_for()) != False:
                program.add_child(forLoop)
                continue

            raise InvalidSyntaxException(tokens[tokenIndex])

        return program

    except:
        token = tokens[tokenIndex]
        return f"Error de sintaxis, en la linea {token.line_number}, posición {token.start_position}."



# Ejemplo de uso:
if __name__ == "__main__":
    print("Ingrese su código:")
    user_code = ""
    try:
        while True:
            line = input() 
            if not line:
                break
            user_code += line + "\n" 
    except EOFError:
        pass

    tokens, lexical_errors = lexical_analysis(user_code)
    syntaxTree = syntax_analysis(tokens)

    if isinstance(syntaxTree, str):
        print(syntaxTree)
    else:
        print("\nAnalisis Sintactico Exitoso, no se encontraron errores.")
        syntaxTree.show_structure()

