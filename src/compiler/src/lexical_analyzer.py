import re

# Clase Token para representar los tokens
class Token:
    def __init__(self, token, token_type, line_number, start_position, end_position):
        self.token = token
        self.token_type = token_type
        self.line_number = line_number
        self.start_position = start_position
        self.end_position = end_position

# Definir expresiones regulares para tokens
token_patterns = [
    # Palabras clave
    (r'\b(int)\b', 'int'),
    (r'\b(float)\b', 'float'),
    (r'\b(char)\b', 'char'),
    (r'\b(void)\b', 'void'),
    (r'\b(auto)\b', 'auto'),
    (r'\b(else)\b', 'else'),
    (r'\b(long)\b', 'long'),
    (r'\b(switch)\b', 'switch'),
    (r'\b(break)\b', 'break'),
    (r'\b(enum)\b', 'enum'),
    (r'\b(register)\b', 'register'),
    (r'\b(typedef)\b', 'typedef'),
    (r'\b(case)\b', 'case'),
    (r'\b(extern)\b', 'extern'),
    (r'\b(return)\b', 'return'),
    (r'\b(union)\b', 'union'),
    (r'\b(const)\b', 'const'),
    (r'\b(for)\b', 'for'),
    (r'\b(signed)\b', 'signed'),
    (r'\b(continue)\b', 'continue'),
    (r'\b(goto)\b', 'goto'),
    (r'\b(sizeof)\b', 'sizeof'),
    (r'\b(volatile)\b', 'volatile'),
    (r'\b(default)\b', 'default'),
    (r'\b(if)\b', 'if'),
    (r'\b(static)\b', 'static'),
    (r'\b(while)\b', 'while'),
    (r'\b(double)\b', 'double'),
    (r'\b(int)\b', 'int'),
    (r'\b(struct)\b', 'struct'),
    (r'\b(_Packed)\b', '_Packed'),
    (r'\b(do)\b', 'do'),

    # Identificadores (incluyendo guiones bajos)
    (r'[a-zA-Z_][a-zA-Z0-9_]*', 'Identifier'),

    # Literales numéricos con decimales o enteros
    (r'\d+\.\d+|\d+\.\d*|\.\d+|\d+', 'Literal_Number'),

    # Literales de cadena entre comillas
    (r'["\'\u201C\u201D](?:[^"\'\\]|\\.)*["\'\u201C\u201D]', 'Literal_String'),

    # Operadores de incremento y decremento
    (r'\+\+', 'Increment_Operator'),
    (r'\-\-', 'Decrement_Operator'),

    # Operadores relacionales
    (r'==', 'Equal_Operator'),
    (r'!=', 'Not_Equal_Operator'),
    (r'<=', 'Less_Than_Or_Equal_Operator'),
    (r'>=', 'Greater_Than_Or_Equal_Operator'),
    (r'<', 'Less_Than_Operator'),
    (r'>', 'Greater_Than_Operator'),

    # Operador de asignación
    (r'=', 'Assignment_Operator'),
    (r'\+=', 'Addition_Assignment_Operator'),
    (r'-=', 'Subtraction_Assignment_Operator'),
    (r'\*=', 'Multiplication_Assignment_Operator'),
    (r'/=', 'Division_Assignment_Operator'),
    (r'%=', 'Modulus_Assignment_Operator'),

    # Operadores aritméticos
    (r'\+', 'Addition_Operator'),
    (r'\-', 'Subtraction_Operator'),
    (r'\*', 'Multiplication_Operator'),
    (r'/', 'Division_Operator'),
    (r'%', 'Modulus_Operator'),

    # Operadores lógicos
    (r'&&', 'Logical_AND_Operator'),
    (r'\|\|', 'Logical_OR_Operator'),
    (r'!', 'Logical_NOT_Operator'),

    # Símbolos
    (r'\(|\)|\[|\]|\{|\}', 'Symbol'),

    # Signos de puntuación
    (r'[.,;:]', 'Punctuation'),

    # Tipos de variable
    (r'\b(int|float|char|double|short|long|unsigned)\b', 'Variable_Type'),

    # Punteros
    (r'\*|&', 'Pointer'),

    # Directivas de preprocesador
    (r'#define|#elif|#else|#endif|#error|#if|#ifdef|#ifndef|#include|#message|#undef', 'Preprocessor_Directive'),

    # Tokens relacionados con arreglos en C
    (r'\[', 'Left_Bracket'),
    (r'\]', 'Right_Bracket'),
]

# Expresión regular para comentarios de una línea (//...)
line_comment_pattern = r'\/\/.*'

# Expresión regular para comentarios multiline (/* ... */)
multiline_comment_pattern = r'\/\*[\s\S]*?\*\/'

# Expresión regular para espacios en blanco (sin saltos de línea)
whitespace_pattern = r'[ \t]+'


def lexical_analysis(code):
    tokens = []  # Lista para almacenar los tokens encontrados
    open_parentheses_stack = []  # Pila para paréntesis abiertos
    open_brackets_stack = []  # Pila para corchetes abiertos
    open_braces_stack = []  # Pila para llaves abiertas
    errors = []  # Lista para almacenar errores léxicos

    lines = code.split('\n')  # Dividir el código en líneas individuales
    in_multiline_comment = False  # Variable para rastrear si estamos dentro de un comentario multilinea

    for line_number, line in enumerate(lines, start=1):
        # Ignorar líneas en blanco
        if not line.strip():
            continue

        position = 0  # Inicializar la posición en el inicio de la línea

        while position < len(line):
            # Si estamos dentro de un comentario multilinea, buscar el cierre '*/'
            if in_multiline_comment:
                end_multiline_comment = line.find('*/', position)
                if end_multiline_comment != -1:
                    # Se encontró el cierre del comentario multilinea
                    position = end_multiline_comment + 2  # Avanzar la posición más allá del comentario
                    in_multiline_comment = False
                else:
                    # No se encontró el cierre del comentario multilinea en esta línea
                    position = len(line)  # Avanzar al final de la línea
            else:
                # No estamos dentro de un comentario multilinea, continuar con el análisis normal

                # Intentar reconocer espacios en blanco
                whitespace_match = re.match(whitespace_pattern, line[position:])
                if whitespace_match:
                    position += whitespace_match.end()  # Avanzar la posición al final del espacio en blanco
                    continue  # Saltar al siguiente carácter en la línea

                # Intentar reconocer comentarios de una línea
                line_comment_match = re.match(line_comment_pattern, line[position:])
                if line_comment_match:
                    position += line_comment_match.end()  # Avanzar la posición
                    continue

                # Verificar si encontramos el inicio de un comentario multilinea '/*'
                if line.startswith('/*', position):
                    in_multiline_comment = True
                    position += 2  # Avanzar la posición más allá del inicio del comentario multilinea
                else:
                    # No se encontró ningún comentario, continuar con el análisis normal

                    match = None
                    for pattern, token_type in token_patterns:
                        regex = re.compile(pattern)  # Compilar la expresión regular
                        match = regex.match(line, position)  # Intentar hacer coincidir el patrón
                        if match:
                            token_value = match.group(0)  # Obtener el valor del token
                            token_start = position  # Posición de inicio del token
                            token_end = position + len(token_value) - 1  # Posición de fin del token
                            # Verificar el tipo de token para símbolos y realizar seguimiento en las pilas
                            if token_type == 'Symbol':
                                # Verificar el tipo de símbolo y realizar acciones correspondientes
                                if token_value == '(':
                                    # Agregar paréntesis abierto a la pila de paréntesis
                                    open_parentheses_stack.append(token_value)
                                elif token_value == ')':
                                    # Verificar si hay un paréntesis abierto correspondiente en la pila
                                    if not open_parentheses_stack:
                                        errors.append(f"Error léxico en línea {line_number}: Paréntesis cerrado sin paréntesis abierto correspondiente.")
                                    else:
                                        open_parentheses_stack.pop()  # Eliminar el paréntesis abierto correspondiente de la pila
                                elif token_value == '[':
                                    open_brackets_stack.append(token_value)
                                elif token_value == ']':
                                    if not open_brackets_stack:
                                        errors.append(f"Error léxico en línea {line_number}: Corchete cerrado sin corchete abierto correspondiente.")
                                    else:
                                        open_brackets_stack.pop()
                                elif token_value == '{':
                                    open_braces_stack.append(token_value)
                                elif token_value == '}':
                                    if not open_braces_stack:
                                        errors.append(f"Error léxico en línea {line_number}: Llave cerrada sin llave abierta correspondiente.")
                                    else:
                                        open_braces_stack.pop()
                            token = Token(token_value, token_type, line_number, token_start, token_end)
                            tokens.append(token)  # Almacenar el token como un objeto Token
                            position = match.end()  # Avanzar la posición más allá del token encontrado
                            break

                    if not match:
                        # Si no se encontró ninguna coincidencia, hay un error léxico
                        errors.append(f'Error léxico en línea {line_number}, posición {position}: "{line[position]}"')
                        position += 1  # Avanzar posición para evitar bucle infinito

    # Verificar si hay paréntesis, corchetes o llaves sin cerrar
    if open_parentheses_stack:
        for token_value in open_parentheses_stack:
            errors.append("Error léxico: Paréntesis abierto sin paréntesis cerrado correspondiente.")
    if open_brackets_stack:
        for token_value in open_brackets_stack:
            errors.append("Error léxico: Corchete abierto sin corchete cerrado correspondiente.")
    if open_braces_stack:
        for token_value in open_braces_stack:
            errors.append("Error léxico: Llave abierta sin llave cerrada correspondiente.")

    return tokens, errors  # Devolver los tokens encontrados y los errores


# Ejemplo de uso:
if __name__ == "__main__":
    code = """
    int main() {
        int x = 5;
        float y = 3.14;
        if (x == 5) {
            printf("Hello, World!");
        }
    }
    """
    tokens, errors = lexical_analysis(code)
    for token in tokens:
        print(f"Token: {token.token}, Tipo: {token.token_type}, Línea: {token.line_number}, Posición de inicio: {token.start_position}, Posición de fin: {token.end_position}")
    if errors:
        print("\nErrores léxicos:")
        for error in errors:
            print(error)
