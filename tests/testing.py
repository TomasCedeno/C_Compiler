# pylint: disable=line-too-long

"""
Each test case has an accompanying class.
Each have methods such as: test_lexer, test_parser & test_symbolTable
"""

import unittest
from src.main import Compiler


class ArgumentsTestCase(unittest.TestCase):
    """Test case for arguments.c"""

    @classmethod
    def setUpClass(cls):
        filename = "samples/arguments.c"
        cls.compiler = Compiler({"filename": filename})

    def test_lexer(self):
        """Test the result of the lexer."""

        self.compiler.tokenize()
        result = "[int, sum, (, int, a, ,, int, b, ), {, return, a, +, b, ;, }, int, main, (, ), {, int, i, =, sum, (, 4, ,, 2, ), ;, i, =, sum, (, 2, ,, 4, ), ;, i, =, 2, ;, sum, (, 5, ,, i, ), ;, i, =, sum, (, 1, ,, 2, ), +, sum, (, 3, ,, 4, ), ;, return, i, ;, }, $]"
        self.assertEqual(str(self.compiler.tokens), result)

    def test_parser(self):
        """Test if the tokens were parsed succesfully."""

        self.compiler.parse()
        self.assertTrue(self.compiler.parseTree)

    def test_symbolTable(self):
        """Test the result of the symbol table"""

        self.compiler.buildSymbolTable()
        result = "{'name': 'global', 'variables': {}, 'labels': {}, 'sum': {'name': 'sum', '..': {...}, 'variables': {'a': 'int', 'b': 'int'}, 'labels': {}}, 'main': {'name': 'main', '..': {...}, 'variables': {'i': 'int'}, 'labels': {}}}"
        self.assertEqual(str(self.compiler.symbolTable), result)


class AssignmentTestCase(unittest.TestCase):
    """Test case for assignment.c"""

    @classmethod
    def setUpClass(cls):
        filename = "samples/assignment.c"
        cls.compiler = Compiler({"filename": filename})

    def test_lexer(self):
        """Test the result of the lexer."""

        self.compiler.tokenize()
        result = "[int, main, (, ), {, int, x, =, 2, +, 2, ;, int, y, =, 5, ;, int, z, =, y, ;, x, =, y, ;, }, $]"
        self.assertEqual(str(self.compiler.tokens), result)

    def test_parser(self):
        """Test if the tokens were parsed succesfully."""

        self.compiler.parse()
        self.assertTrue(self.compiler.parseTree)

    def test_symbolTable(self):
        """Test the result of the symbol table"""

        self.compiler.buildSymbolTable()
        result = "{'name': 'global', 'variables': {}, 'labels': {}, 'main': {'name': 'main', '..': {...}, 'variables': {'x': 'int', 'y': 'int', 'z': 'int'}, 'labels': {}}}"
        self.assertEqual(str(self.compiler.symbolTable), result)


class AssignmentsTestCase(unittest.TestCase):
    """Test case for assignments.c"""

    @classmethod
    def setUpClass(cls):
        filename = "samples/assignments.c"
        cls.compiler = Compiler({"filename": filename})

    def test_lexer(self):
        """Test the result of the lexer."""

        self.compiler.tokenize()
        result = "[int, main, (, ), {, int, i, =, 0, ;, i, ++, ;, i, --, ;, i, +=, 2, ;, i, -=, 2, ;, i, +=, i, ;, return, i, ;, }, $]"
        self.assertEqual(str(self.compiler.tokens), result)

    def test_parser(self):
        """Test if the tokens were parsed succesfully."""

        self.compiler.parse()
        self.assertTrue(self.compiler.parseTree)

    def test_symbolTable(self):
        """Test the result of the symbol table"""

        self.compiler.buildSymbolTable()
        result = "{'name': 'global', 'variables': {}, 'labels': {}, 'main': {'name': 'main', '..': {...}, 'variables': {'i': 'int'}, 'labels': {}}}"
        self.assertEqual(str(self.compiler.symbolTable), result)


class BasicMathTestCase(unittest.TestCase):
    """Test case for basic_math.c"""

    @classmethod
    def setUpClass(cls):
        filename = "samples/basic_math.c"
        cls.compiler = Compiler({"filename": filename})

    def test_lexer(self):
        """Test the result of the lexer."""

        self.compiler.tokenize()
        result = "[int, main, (, ), {, return, 2, +, 2, ;, }, $]"
        self.assertEqual(str(self.compiler.tokens), result)

    def test_parser(self):
        """Test if the tokens were parsed succesfully."""

        self.compiler.parse()
        self.assertTrue(self.compiler.parseTree)

    def test_symbolTable(self):
        """Test the result of the symbol table"""

        self.compiler.buildSymbolTable()
        result = "{'name': 'global', 'variables': {}, 'labels': {}, 'main': {'name': 'main', '..': {...}, 'variables': {}, 'labels': {}}}"
        self.assertEqual(str(self.compiler.symbolTable), result)


class BooleanExpressionTestCase(unittest.TestCase):
    """Test case for boolean_expression.c"""

    @classmethod
    def setUpClass(cls):
        filename = "samples/boolean_expression.c"
        cls.compiler = Compiler({"filename": filename})

    def test_lexer(self):
        """Test the result of the lexer."""

        self.compiler.tokenize()
        result = "[int, main, (, ), {, int, a, =, 1, &&, 1, ;, int, b, =, 1, ||, 1, ;, int, c, =, !, 1, ;, }, $]"
        self.assertEqual(str(self.compiler.tokens), result)

    def test_parser(self):
        """Test if the tokens were parsed succesfully."""

        self.compiler.parse()
        self.assertTrue(self.compiler.parseTree)

    def test_symbolTable(self):
        """Test the result of the symbol table"""
        self.compiler.buildSymbolTable()
        result = "{'name': 'global', 'variables': {}, 'labels': {}, 'main': {'name': 'main', '..': {...}, 'variables': {'a': 'int', 'b': 'int', 'c': 'int'}, 'labels': {}}}"
        self.assertEqual(str(self.compiler.symbolTable), result)


class BreakTestCase(unittest.TestCase):
    """Test case for break.c"""

    @classmethod
    def setUpClass(cls):
        filename = "samples/break.c"
        cls.compiler = Compiler({"filename": filename})

    def test_lexer(self):
        """Test the result of the lexer."""

        self.compiler.tokenize()
        result = "[int, main, (, ), {, int, i, =, 10, ;, while, (, i, >, 0, ), {, if, (, i, ==, 2, ), {, break, ;, }, i, --, ;, }, return, i, ;, }, $]"
        self.assertEqual(str(self.compiler.tokens), result)

    def test_parser(self):
        """Test if the tokens were parsed succesfully."""

        self.compiler.parse()
        self.assertTrue(self.compiler.parseTree)

    def test_symbolTable(self):
        """Test the result of the symbol table"""
        self.compiler.buildSymbolTable()
        result = "{'name': 'global', 'variables': {}, 'labels': {}, 'main': {'name': 'main', '..': {...}, 'variables': {'i': 'int'}, 'labels': {}}}"
        self.assertEqual(str(self.compiler.symbolTable), result)


class CallTestCase(unittest.TestCase):
    """Test case for call.c"""

    @classmethod
    def setUpClass(cls):
        filename = "samples/call.c"
        cls.compiler = Compiler({"filename": filename})

    def test_lexer(self):
        """Test the result of the lexer."""

        self.compiler.tokenize()
        result = "[int, sum, (, int, x, ,, int, y, ), {, return, x, +, y, ;, }, int, main, (, ), {, int, a, =, 2, ;, int, b, =, 3, ;, int, c, =, sum, (, a, ,, b, ), ;, return, c, ;, }, $]"
        self.assertEqual(str(self.compiler.tokens), result)

    def test_parser(self):
        """Test if the tokens were parsed succesfully."""

        self.compiler.parse()
        self.assertTrue(self.compiler.parseTree)

    def test_symbolTable(self):
        """Test the result of the symbol table"""

        self.compiler.buildSymbolTable()
        result = "{'name': 'global', 'variables': {}, 'labels': {}, 'sum': {'name': 'sum', '..': {...}, 'variables': {'x': 'int', 'y': 'int'}, 'labels': {}}, 'main': {'name': 'main', '..': {...}, 'variables': {'a': 'int', 'b': 'int', 'c': 'int'}, 'labels': {}}}"
        self.assertEqual(str(self.compiler.symbolTable), result)


class ComparisonTestCase(unittest.TestCase):
    """Test case for comparison.c"""

    @classmethod
    def setUpClass(cls):
        filename = "samples/comparison.c"
        cls.compiler = Compiler({"filename": filename})

    def test_lexer(self):
        """Test the result of the lexer."""

        self.compiler.tokenize()
        result = "[int, main, (, ), {, int, a, =, 0, ;, int, b, =, 1, ;, int, c, =, a, !=, b, ;, return, c, ;, }, $]"
        self.assertEqual(str(self.compiler.tokens), result)

    def test_parser(self):
        """Test if the tokens were parsed succesfully."""

        self.compiler.parse()
        self.assertTrue(self.compiler.parseTree)

    def test_symbolTable(self):
        """Test the result of the symbol table"""
        self.compiler.buildSymbolTable()
        result = "{'name': 'global', 'variables': {}, 'labels': {}, 'main': {'name': 'main', '..': {...}, 'variables': {'a': 'int', 'b': 'int', 'c': 'int'}, 'labels': {}}}"
        self.assertEqual(str(self.compiler.symbolTable), result)


class ContinueTestCase(unittest.TestCase):
    """Test case for continue.c"""

    @classmethod
    def setUpClass(cls):
        filename = "samples/continue.c"
        cls.compiler = Compiler({"filename": filename})

    def test_lexer(self):
        """Test the result of the lexer."""

        self.compiler.tokenize()
        result = "[int, main, (, ), {, int, i, =, 0, ;, int, a, =, 0, ;, while, (, i, <, 10, ), {, if, (, i, ==, 5, ), {, i, =, 11, ;, continue, ;, }, i, ++, ;, }, return, i, ;, }, $]"
        self.assertEqual(str(self.compiler.tokens), result)

    def test_parser(self):
        """Test if the tokens were parsed succesfully."""

        self.compiler.parse()
        self.assertTrue(self.compiler.parseTree)

    def test_symbolTable(self):
        """Test the result of the symbol table"""
        self.compiler.buildSymbolTable()
        result = "{'name': 'global', 'variables': {}, 'labels': {}, 'main': {'name': 'main', '..': {...}, 'variables': {'i': 'int', 'a': 'int'}, 'labels': {}}}"
        self.assertEqual(str(self.compiler.symbolTable), result)


class ControlFlowTestCase(unittest.TestCase):
    """Test case for control_flow.c"""

    @classmethod
    def setUpClass(cls):
        filename = "samples/control_flow.c"
        cls.compiler = Compiler({"filename": filename})

    def test_lexer(self):
        """Test the result of the lexer."""

        self.compiler.tokenize()
        result = "[int, main, (, ), {, int, i, =, 0, ;, int, y, =, 0, ;, int, x, =, 0, ;, for, (, i, =, 0, ;, i, <, 10, ;, i, ++, ), {, x, +=, 1, ;, }, while, (, i, >, 0, ), {, y, +=, 2, ;, i, --, ;, }, return, 0, ;, }, $]"
        self.assertEqual(str(self.compiler.tokens), result)

    def test_parser(self):
        """Test if the tokens were parsed succesfully."""

        self.compiler.parse()
        self.assertTrue(self.compiler.parseTree)

    def test_symbolTable(self):
        """Test the result of the symbol table"""

        self.compiler.buildSymbolTable()


class DuplicateFuncTestCase(unittest.TestCase):
    """
    Test case for duplicate_func.c"
    Returns expected error, because of scope checking
    """

    @classmethod
    def setUpClass(cls):
        filename = "samples/duplicate_func.c"
        cls.compiler = Compiler({"filename": filename})

    def test_lexer(self):
        """Test the result of the lexer."""

        self.compiler.tokenize()
        result = "[int, foo, (, ), {, return, 0, ;, }, int, foo, (, ), {, return, 1, ;, }, $]"
        self.assertEqual(str(self.compiler.tokens), result)

    def test_parser(self):
        """Test if the tokens were parsed succesfully."""

        self.compiler.parse()
        self.assertTrue(self.compiler.parseTree)

    @unittest.expectedFailure
    def test_symbolTable(self):
        """Test the result of the symbol table"""

        self.compiler.buildSymbolTable()


class DuplicateLabelTestCase(unittest.TestCase):
    """
    Test case for duplicate_label.c"
    Returns expected error, because of scope checking
    """

    @classmethod
    def setUpClass(cls):
        filename = "samples/duplicate_label.c"
        cls.compiler = Compiler({"filename": filename})

    def test_lexer(self):
        """Test the result of the lexer."""

        self.compiler.tokenize()
        result = "[int, main, (, ), {, goto, label, ;, return, 0, ;, label, return, 1, ;, label, return, 1, ;, }, $]"
        self.assertEqual(str(self.compiler.tokens), result)

    def test_parser(self):
        """Test if the tokens were parsed succesfully."""

        self.compiler.parse()
        self.assertTrue(self.compiler.parseTree)

    @unittest.expectedFailure
    def test_symbolTable(self):
        """Test the result of the symbol table"""

        self.compiler.buildSymbolTable()


class DuplicateVarTestCase(unittest.TestCase):
    """
    Test case for duplicate_var.c
    Returns expected error, because of scope checking
    """

    @classmethod
    def setUpClass(cls):
        filename = "samples/duplicate_var.c"
        cls.compiler = Compiler({"filename": filename})

    def test_lexer(self):
        """Test the result of the lexer."""

        self.compiler.tokenize()
        result = (
            "[int, main, (, ), {, int, i, =, 0, ;, int, i, =, 1, ;, return, 0, ;, }, $]"
        )
        self.assertEqual(str(self.compiler.tokens), result)

    def test_parser(self):
        """Test if the tokens were parsed succesfully."""

        self.compiler.parse()
        self.assertTrue(self.compiler.parseTree)

    @unittest.expectedFailure
    def test_symbolTable(self):
        """Test the result of the symbol table"""

        self.compiler.buildSymbolTable()


class ExpressionTestCase(unittest.TestCase):
    """Test case for expression.c"""

    @classmethod
    def setUpClass(cls):
        filename = "samples/expression.c"
        cls.compiler = Compiler({"filename": filename})

    def test_lexer(self):
        """Test the result of the lexer."""

        self.compiler.tokenize()
        result = "[int, main, (, ), {, int, x, ;, x, =, 2, +, 2, ;, return, 0, ;, }, $]"
        self.assertEqual(str(self.compiler.tokens), result)

    def test_parser(self):
        """Test if the tokens were parsed succesfully."""

        self.compiler.parse()
        self.assertTrue(self.compiler.parseTree)

    def test_symbolTable(self):
        """Test the result of the symbol table"""

        self.compiler.buildSymbolTable()
        result = "{'name': 'global', 'variables': {}, 'labels': {}, 'main': {'name': 'main', '..': {...}, 'variables': {'x': 'int'}, 'labels': {}}}"
        self.assertEqual(str(self.compiler.symbolTable), result)


class FloatTestCase(unittest.TestCase):
    """Test case for float.c"""

    @classmethod
    def setUpClass(cls):
        filename = "samples/float.c"
        cls.compiler = Compiler({"filename": filename})

    def test_lexer(self):
        """Test the result of the lexer."""

        self.compiler.tokenize()
        result = "[int, main, (, ), {, float, x, =, 2.5, ;, return, x, ;, }, $]"
        self.assertEqual(str(self.compiler.tokens), result)

    def test_parser(self):
        """Test if the tokens were parsed succesfully."""

        self.compiler.parse()
        self.assertTrue(self.compiler.parseTree)

    def test_symbolTable(self):
        """Test the result of the symbol table"""

        self.compiler.buildSymbolTable()
        result = "{'name': 'global', 'variables': {}, 'labels': {}, 'main': {'name': 'main', '..': {...}, 'variables': {'x': 'float'}, 'labels': {}}}"
        self.assertEqual(str(self.compiler.symbolTable), result)


class ForTestCase(unittest.TestCase):
    """Test case for for.c"""

    @classmethod
    def setUpClass(cls):
        filename = "samples/for.c"
        cls.compiler = Compiler({"filename": filename})

    def test_lexer(self):
        """Test the result of the lexer."""

        self.compiler.tokenize()
        result = "[int, main, (, ), {, int, number, =, 10, ;, int, i, =, 0, ;, int, y, =, 0, ;, for, (, i, =, 0, ;, i, <, number, ;, i, ++, ), {, y, +=, 1, ;, }, return, 0, ;, }, $]"
        self.assertEqual(str(self.compiler.tokens), result)

    def test_parser(self):
        """Test if the tokens were parsed succesfully."""

        self.compiler.parse()
        self.assertTrue(self.compiler.parseTree)

    def test_symbolTable(self):
        """Test the result of the symbol table"""

        self.compiler.buildSymbolTable()
        result = "{'name': 'global', 'variables': {}, 'labels': {}, 'main': {'name': 'main', '..': {...}, 'variables': {'number': 'int', 'i': 'int', 'y': 'int'}, 'labels': {}}}"
        self.assertEqual(str(self.compiler.symbolTable), result)


class FunctionTestCase(unittest.TestCase):
    """Test case for function.c"""

    @classmethod
    def setUpClass(cls):
        filename = "samples/function.c"
        cls.compiler = Compiler({"filename": filename})

    def test_lexer(self):
        """Test the result of the lexer."""

        self.compiler.tokenize()
        result = "[stdio.h, int, sum, (, int, a, ,, int, b, ), {, return, a, +, b, ;, }, int, main, (, void, ), {, int, x, =, 2, ;, int, y, =, 5, ;, int, z, =, sum, (, x, ,, y, ), ;, printf, (, %d, ,, z, ), ;, return, 0, ;, }, $]"
        self.assertEqual(str(self.compiler.tokens), result)

    def test_parser(self):
        """Test if the tokens were parsed succesfully."""

        self.compiler.parse()
        self.assertTrue(self.compiler.parseTree)

    @unittest.expectedFailure
    def test_symbolTable(self):
        """Test the result of the symbol table"""

        self.compiler.buildSymbolTable()


class GotoTestCase(unittest.TestCase):
    """
    Test case for goto.c"
    """

    @classmethod
    def setUpClass(cls):
        filename = "samples/goto.c"
        cls.compiler = Compiler({"filename": filename})

    def test_lexer(self):
        """Test the result of the lexer."""

        self.compiler.tokenize()
        result = "[int, main, (, ), {, int, a, =, 2, ;, if, (, a, %, 2, ==, 0, ), {, goto, even, ;, }, else, {, goto, odd, ;, }, return, 0, ;, even, return, 1, ;, odd, return, 2, ;, }, $]"
        self.assertEqual(str(self.compiler.tokens), result)

    def test_parser(self):

        """Test if the tokens were parsed succesfully."""

        self.compiler.parse()
        self.assertTrue(self.compiler.parseTree)

    def test_symbolTable(self):
        """Test the result of the symbol table"""

        self.compiler.buildSymbolTable()
        result = "{'name': 'global', 'variables': {}, 'labels': {}, 'main': {'name': 'main', '..': {...}, 'variables': {'a': 'int'}, 'labels': {'even': True, 'odd': True}}}"
        self.assertEqual(str(self.compiler.symbolTable), result)


class HelloWorldTestCase(unittest.TestCase):
    """Test case for hello_world.c"""

    @classmethod
    def setUpClass(cls):
        filename = "samples/hello_world.c"
        cls.compiler = Compiler({"filename": filename})

    def test_lexer(self):
        """Test the result of the lexer."""

        self.compiler.tokenize()
        result = "[stdio.h, int, main, (, ), {, printf, (, Hello world!, ), ;, return, 0, ;, }, $]"
        self.assertEqual(str(self.compiler.tokens), result)

    def test_parser(self):
        """Test if the tokens were parsed succesfully."""

        self.compiler.parse()
        self.assertTrue(self.compiler.parseTree)

    @unittest.expectedFailure
    def test_symbolTable(self):
        """Test the result of the symbol table"""

        self.compiler.buildSymbolTable()


class IfElseTestCase(unittest.TestCase):
    """Test case for if_else.c"""

    @classmethod
    def setUpClass(cls):
        filename = "samples/if_else.c"
        cls.compiler = Compiler({"filename": filename})

    def test_lexer(self):
        """Test the result of the lexer."""

        self.compiler.tokenize()
        result = "[int, main, (, ), {, int, number, =, 0, ;, if, (, number, ==, 0, ), {, number, =, 1, ;, }, else, {, number, =, 2, ;, }, return, number, ;, }, $]"
        self.assertEqual(str(self.compiler.tokens), result)

    def test_parser(self):
        """Test if the tokens were parsed succesfully."""

        self.compiler.parse()
        self.assertTrue(self.compiler.parseTree)

    def test_symbolTable(self):
        """Test the result of the symbol table"""

        self.compiler.buildSymbolTable()
        result = "{'name': 'global', 'variables': {}, 'labels': {}, 'main': {'name': 'main', '..': {...}, 'variables': {'number': 'int'}, 'labels': {}}}"
        self.assertEqual(str(self.compiler.symbolTable), result)


class IfTestCase(unittest.TestCase):
    """Test case for if.c"""

    @classmethod
    def setUpClass(cls):
        filename = "samples/if.c"
        cls.compiler = Compiler({"filename": filename})

    def test_lexer(self):
        """Test the result of the lexer."""

        self.compiler.tokenize()
        result = "[int, main, (, ), {, int, number, =, 0, ;, if, (, number, ==, 0, ), {, number, =, 99, ;, }, return, 0, ;, }, $]"
        self.assertEqual(str(self.compiler.tokens), result)

    def test_parser(self):
        """Test if the tokens were parsed succesfully."""

        self.compiler.parse()
        self.assertTrue(self.compiler.parseTree)

    def test_symbolTable(self):
        """Test the result of the symbol table"""

        self.compiler.buildSymbolTable()
        result = "{'name': 'global', 'variables': {}, 'labels': {}, 'main': {'name': 'main', '..': {...}, 'variables': {'number': 'int'}, 'labels': {}}}"
        self.assertEqual(str(self.compiler.symbolTable), result)


class IncludeTestCase(unittest.TestCase):
    """Test case for include.c"""

    @classmethod
    def setUpClass(cls):
        filename = "samples/include.c"
        cls.compiler = Compiler({"filename": filename})

    def test_lexer(self):
        """Test the result of the lexer."""

        self.compiler.tokenize()
        result = "[stdio.h, int, main, (, ), {, return, 0, ;, }, $]"
        self.assertEqual(str(self.compiler.tokens), result)

    def test_parser(self):
        """Test if the tokens were parsed succesfully."""

        self.compiler.parse()
        self.assertTrue(self.compiler.parseTree)

    def test_symbolTable(self):
        """Test the result of the symbol table"""

        self.compiler.buildSymbolTable()
        result = "{'name': 'global', 'variables': {}, 'labels': {}, 'main': {'name': 'main', '..': {...}, 'variables': {}, 'labels': {}}}"
        self.assertEqual(str(self.compiler.symbolTable), result)


class IRFuncTestCase(unittest.TestCase):
    """Test case for ir.c"""

    @classmethod
    def setUpClass(cls):
        filename = "samples/ir.c"
        cls.compiler = Compiler({"filename": filename})

    def test_lexer(self):
        """Test the result of the lexer."""

        self.compiler.tokenize()
        result = "[int, main, (, ), {, int, i, ;, int, j, ;, j, =, i, /, 12, *, 15, ;, return, i, ;, }, $]"
        self.assertEqual(str(self.compiler.tokens), result)

    def test_parser(self):
        """Test if the tokens were parsed succesfully."""

        self.compiler.parse()
        self.assertTrue(self.compiler.parseTree)

    def test_symbolTable(self):
        """Test the result of the symbol table"""

        self.compiler.buildSymbolTable()
        result = "{'name': 'global', 'variables': {}, 'labels': {}, 'main': {'name': 'main', '..': {...}, 'variables': {'i': 'int', 'j': 'int'}, 'labels': {}}}"
        self.assertEqual(str(self.compiler.symbolTable), result)


class LineBreakTestCase(unittest.TestCase):
    """Test case for linebreak.c"""

    @classmethod
    def setUpClass(cls):
        filename = "samples/linebreak.c"
        cls.compiler = Compiler({"filename": filename})

    def test_lexer(self):
        """Test the result of the lexer."""

        self.compiler.tokenize()
        result = "[int, main, (, ), {, char, string, =, Line 1 Line 2, ;, return, string, ;, }, $]"
        self.assertEqual(str(self.compiler.tokens), result)

    def test_parser(self):
        """Test if the tokens were parsed succesfully."""

        self.compiler.parse()
        self.assertTrue(self.compiler.parseTree)

    def test_symbolTable(self):
        """Test the result of the symbol table"""

        self.compiler.buildSymbolTable()
        result = "{'name': 'global', 'variables': {}, 'labels': {}, 'main': {'name': 'main', '..': {...}, 'variables': {'string': 'char'}, 'labels': {}}}"
        self.assertEqual(str(self.compiler.symbolTable), result)


class MathTestCase(unittest.TestCase):
    """Test case for math.c"""

    @classmethod
    def setUpClass(cls):
        filename = "samples/math.c"
        cls.compiler = Compiler({"filename": filename})

    def test_lexer(self):
        """Test the result of the lexer."""

        self.compiler.tokenize()
        result = "[int, main, (, ), {, int, i, =, 0, ;, i, +=, 25, ;, i, ++, ;, float, y, =, 2.5, ;, return, i, ;, }, $]"
        self.assertEqual(str(self.compiler.tokens), result)

    def test_parser(self):
        """Test if the tokens were parsed succesfully."""

        self.compiler.parse()
        self.assertTrue(self.compiler.parseTree)

    def test_symbolTable(self):
        """Test the result of the symbol table"""

        self.compiler.buildSymbolTable()
        result = "{'name': 'global', 'variables': {}, 'labels': {}, 'main': {'name': 'main', '..': {...}, 'variables': {'i': 'int', 'y': 'float'}, 'labels': {}}}"
        self.assertEqual(str(self.compiler.symbolTable), result)


class ModuloTestCase(unittest.TestCase):
    """Test case for modulo.c"""

    @classmethod
    def setUpClass(cls):
        filename = "samples/modulo.c"
        cls.compiler = Compiler({"filename": filename})

    def test_lexer(self):
        """Test the result of the lexer."""

        self.compiler.tokenize()
        result = "[int, main, (, ), {, int, i, =, 32, %, 3, ;, return, i, ;, }, $]"
        self.assertEqual(str(self.compiler.tokens), result)

    def test_parser(self):
        """Test if the tokens were parsed succesfully."""

        self.compiler.parse()
        self.assertTrue(self.compiler.parseTree)

    def test_symbolTable(self):
        """Test the result of the symbol table"""

        self.compiler.buildSymbolTable()
        result = "{'name': 'global', 'variables': {}, 'labels': {}, 'main': {'name': 'main', '..': {...}, 'variables': {'i': 'int'}, 'labels': {}}}"
        self.assertEqual(str(self.compiler.symbolTable), result)


class MultiLineCommentTestCase(unittest.TestCase):
    """Test case for multi_line_comment.c"""

    @classmethod
    def setUpClass(cls):
        filename = "samples/multi_line_comment.c"
        cls.compiler = Compiler({"filename": filename})

    def test_lexer(self):
        """Test the result of the lexer."""

        self.compiler.tokenize()
        result = "[int, main, (, ), {, return, 0, ;, }, $]"
        self.assertEqual(str(self.compiler.tokens), result)

    def test_parser(self):
        """Test if the tokens were parsed succesfully."""

        self.compiler.parse()
        self.assertTrue(self.compiler.parseTree)

    def test_symbolTable(self):
        """Test the result of the symbol table."""

        self.compiler.buildSymbolTable()
        result = "{'name': 'global', 'variables': {}, 'labels': {}, 'main': {'name': 'main', '..': {...}, 'variables': {}, 'labels': {}}}"
        self.assertEqual(str(self.compiler.symbolTable), result)


class MultiFunctionsTestCase(unittest.TestCase):
    """Test case for multiple_functions.c"""

    @classmethod
    def setUpClass(cls):
        filename = "samples/multiple_functions.c"
        cls.compiler = Compiler({"filename": filename})

    def test_lexer(self):
        """Test the result of the lexer."""

        self.compiler.tokenize()
        result = "[int, foo, (, ), {, return, 0, ;, }, int, bar, (, ), {, return, 0, ;, }, int, foobar, (, ), {, return, 0, ;, }, int, foobiz, (, ), {, return, 0, ;, }, int, main, (, ), {, return, 0, ;, }, $]"
        self.assertEqual(str(self.compiler.tokens), result)

    def test_parser(self):
        """Test if the tokens were parsed succesfully."""

        self.compiler.parse()
        self.assertTrue(self.compiler.parseTree)

    def test_symbolTable(self):
        """Test the result of the symbol table."""

        self.compiler.buildSymbolTable()
        result = "{'name': 'global', 'variables': {}, 'labels': {}, 'foo': {'name': 'foo', '..': {...}, 'variables': {}, 'labels': {}}, 'bar': {'name': 'bar', '..': {...}, 'variables': {}, 'labels': {}}, 'foobar': {'name': 'foobar', '..': {...}, 'variables': {}, 'labels': {}}, 'foobiz': {'name': 'foobiz', '..': {...}, 'variables': {}, 'labels': {}}, 'main': {'name': 'main', '..': {...}, 'variables': {}, 'labels': {}}}"
        self.assertEqual(str(self.compiler.symbolTable), result)


class MultiStatementsTestCase(unittest.TestCase):
    """Test case for multiple_statements.c"""

    @classmethod
    def setUpClass(cls):
        filename = "samples/multiple_statements.c"
        cls.compiler = Compiler({"filename": filename})

    def test_lexer(self):
        """Test the result of the lexer."""

        self.compiler.tokenize()
        result = "[int, main, (, ), {, int, x, ;, int, y, ;, int, z, ;, x, =, 2, ;, y, =, 2, ;, z, =, 2, ;, x, =, 2, +, 2, ;, }, int, foo, (, ), {, return, 0, ;, }, int, bar, (, ), {, return, 0, ;, }, $]"
        self.assertEqual(str(self.compiler.tokens), result)

    def test_parser(self):
        """Test if the tokens were parsed succesfully."""

        self.compiler.parse()
        self.assertTrue(self.compiler.parseTree)

    def test_symbolTable(self):
        """Test the result of the symbol table."""

        self.compiler.buildSymbolTable()
        result = "{'name': 'global', 'variables': {}, 'labels': {}, 'main': {'name': 'main', '..': {...}, 'variables': {'x': 'int', 'y': 'int', 'z': 'int'}, 'labels': {}}, 'foo': {'name': 'foo', '..': {...}, 'variables': {}, 'labels': {}}, 'bar': {'name': 'bar', '..': {...}, 'variables': {}, 'labels': {}}}"
        self.assertEqual(str(self.compiler.symbolTable), result)


class NegativeNumberTestCase(unittest.TestCase):
    """Test case for negative_number.c"""

    @classmethod
    def setUpClass(cls):
        filename = "samples/negative_number.c"
        cls.compiler = Compiler({"filename": filename})

    def test_lexer(self):
        """Test the result of the lexer."""

        self.compiler.tokenize()
        result = "[int, main, (, ), {, int, i, =, 1, -, 1, ;, i, =, 1, -, -1, ;, int, a, =, -2341, ;, }, $]"
        self.assertEqual(str(self.compiler.tokens), result)

    def test_parser(self):
        """Test if the tokens were parsed succesfully."""

        self.compiler.parse()
        self.assertTrue(self.compiler.parseTree)

    def test_symbolTable(self):
        """Test the result of the symbol table"""

        self.compiler.buildSymbolTable()
        result = "{'name': 'global', 'variables': {}, 'labels': {}, 'main': {'name': 'main', '..': {...}, 'variables': {'i': 'int', 'a': 'int'}, 'labels': {}}}"
        self.assertEqual(str(self.compiler.symbolTable), result)


class ParenthesesTestCase(unittest.TestCase):
    """Test case for parentheses.c"""

    @classmethod
    def setUpClass(cls):
        filename = "samples/parentheses.c"
        cls.compiler = Compiler({"filename": filename})

    def test_lexer(self):
        """Test the result of the lexer."""

        self.compiler.tokenize()
        result = "[int, main, (, ), {, int, i, ;, i, =, (, 2, ), ;, }, $]"
        self.assertEqual(str(self.compiler.tokens), result)

    def test_parser(self):
        """Test if the tokens were parsed succesfully."""

        self.compiler.parse()
        self.assertTrue(self.compiler.parseTree)

    def test_symbolTable(self):
        """Test the result of the symbol table."""

        self.compiler.buildSymbolTable()
        result = "{'name': 'global', 'variables': {}, 'labels': {}, 'main': {'name': 'main', '..': {...}, 'variables': {'i': 'int'}, 'labels': {}}}"
        self.assertEqual(str(self.compiler.symbolTable), result)


class ParseTestCase(unittest.TestCase):
    """Test case for parseTest.c"""

    @classmethod
    def setUpClass(cls):
        filename = "samples/parseTest.c"
        cls.compiler = Compiler({"filename": filename})

    def test_lexer(self):
        """Test the result of the lexer."""

        self.compiler.tokenize()
        result = "[int, main, (, ), {, int, i, =, 10, ;, i, =, (, 4, +, 2, ), *, (, 10, %, 11, ), /, (, 3, +, (, 4, /, 2, ), ), ;, return, i, ;, }, $]"
        self.assertEqual(str(self.compiler.tokens), result)

    def test_parser(self):
        """Test if the tokens were parsed succesfully."""

        self.compiler.parse()
        self.assertTrue(self.compiler.parseTree)

    def test_symbolTable(self):
        """Test the result of the symbol table."""

        self.compiler.buildSymbolTable()
        result = "{'name': 'global', 'variables': {}, 'labels': {}, 'main': {'name': 'main', '..': {...}, 'variables': {'i': 'int'}, 'labels': {}}}"
        self.assertEqual(str(self.compiler.symbolTable), result)


class PlainTestCase(unittest.TestCase):
    """Test case for plain.c"""

    @classmethod
    def setUpClass(cls):
        filename = "samples/plain.c"
        cls.compiler = Compiler({"filename": filename})

    def test_lexer(self):
        """Test the result of the lexer."""

        self.compiler.tokenize()
        result = "[int, main, (, ), {, return, 1, ;, }, $]"
        self.assertEqual(str(self.compiler.tokens), result)

    def test_parser(self):
        """Test if the tokens were parsed succesfully."""

        self.compiler.parse()
        self.assertTrue(self.compiler.parseTree)

    def test_symbolTable(self):
        """Test the result of the symbol table."""

        self.compiler.buildSymbolTable()
        result = "{'name': 'global', 'variables': {}, 'labels': {}, 'main': {'name': 'main', '..': {...}, 'variables': {}, 'labels': {}}}"
        self.assertEqual(str(self.compiler.symbolTable), result)


class PrintTestCase(unittest.TestCase):
    """Test case for print.c"""

    @classmethod
    def setUpClass(cls):
        filename = "samples/print.c"
        cls.compiler = Compiler({"filename": filename})

    def test_lexer(self):
        """Test the result of the lexer."""

        self.compiler.tokenize()
        result = "[stdio.h, int, main, (, ), {, printf, (, Hello, World, ), ;, }, $]"
        self.assertEqual(str(self.compiler.tokens), result)

    def test_parser(self):
        """Test if the tokens were parsed succesfully."""

        self.compiler.parse()
        self.assertTrue(self.compiler.parseTree)

    @unittest.expectedFailure
    def test_symbolTable(self):
        """Test the result of the symbol table."""

        self.compiler.buildSymbolTable()


class SimpleGotoTestCase(unittest.TestCase):
    """Test case for simple_goto.c"""

    @classmethod
    def setUpClass(cls):
        filename = "samples/simple_goto.c"
        cls.compiler = Compiler({"filename": filename})

    def test_lexer(self):
        """Test the result of the lexer."""

        self.compiler.tokenize()
        result = "[int, main, (, ), {, goto, label, ;, return, 0, ;, label, return, 1, ;, }, $]"
        self.assertEqual(str(self.compiler.tokens), result)

    def test_parser(self):
        """Test if the tokens were parsed succesfully."""

        self.compiler.parse()
        self.assertTrue(self.compiler.parseTree)

    def test_symbolTable(self):
        """Test the result of the symbol table."""

        self.compiler.buildSymbolTable()
        result = "{'name': 'global', 'variables': {}, 'labels': {}, 'main': {'name': 'main', '..': {...}, 'variables': {}, 'labels': {'label': True}}}"
        self.assertEqual(str(self.compiler.symbolTable), result)


class SimpleIfTestCase(unittest.TestCase):
    """Test case for simple_if.c"""

    @classmethod
    def setUpClass(cls):
        filename = "samples/simple_if.c"
        cls.compiler = Compiler({"filename": filename})

    def test_lexer(self):
        """Test the result of the lexer."""

        self.compiler.tokenize()
        result = "[int, main, (, ), {, if, (, 0, ==, 0, ), {, return, 0, ;, }, else, {, return, 22, ;, }, }, $]"
        self.assertEqual(str(self.compiler.tokens), result)

    def test_parser(self):
        """Test if the tokens were parsed succesfully."""

        self.compiler.parse()
        self.assertTrue(self.compiler.parseTree)

    def test_symbolTable(self):
        """Test the result of the symbol table."""

        self.compiler.buildSymbolTable()
        result = "{'name': 'global', 'variables': {}, 'labels': {}, 'main': {'name': 'main', '..': {...}, 'variables': {}, 'labels': {}}}"
        self.assertEqual(str(self.compiler.symbolTable), result)


class SingleLineCommentTestCase(unittest.TestCase):
    """Test case for single_line_comment.c"""

    @classmethod
    def setUpClass(cls):
        filename = "samples/single_line_comment.c"
        cls.compiler = Compiler({"filename": filename})

    def test_lexer(self):
        """Test the result of the lexer."""

        self.compiler.tokenize()
        result = "[int, main, (, ), {, return, 0, ;, }, $]"
        self.assertEqual(str(self.compiler.tokens), result)

    def test_parser(self):
        """Test if the tokens were parsed succesfully."""

        self.compiler.parse()
        self.assertTrue(self.compiler.parseTree)

    def test_symbolTable(self):
        """Test the result of the symbol table."""

        self.compiler.buildSymbolTable()
        result = "{'name': 'global', 'variables': {}, 'labels': {}, 'main': {'name': 'main', '..': {...}, 'variables': {}, 'labels': {}}}"
        self.assertEqual(str(self.compiler.symbolTable), result)


class UndefinedVarTestCase(unittest.TestCase):
    """
    Test case for undefined_var.c
    Returns expected error, because of scope checking
    """

    @classmethod
    def setUpClass(cls):
        filename = "samples/undefined_var.c"
        cls.compiler = Compiler({"filename": filename})

    def test_lexer(self):
        """Test the result of the lexer."""

        self.compiler.tokenize()
        result = "[int, main, (, ), {, return, x, ;, }, $]"
        self.assertEqual(str(self.compiler.tokens), result)

    def test_parser(self):
        """Test if the tokens were parsed succesfully."""

        self.compiler.parse()
        self.assertTrue(self.compiler.parseTree)

    @unittest.expectedFailure
    def test_symbolTable(self):
        """Test the result of the symbol table."""

        self.compiler.buildSymbolTable()


class WhileTestCase(unittest.TestCase):
    """Test case for while.c"""

    @classmethod
    def setUpClass(cls):
        filename = "samples/while.c"
        cls.compiler = Compiler({"filename": filename})

    def test_lexer(self):
        """Test the result of the lexer."""

        self.compiler.tokenize()
        result = "[int, main, (, ), {, int, i, =, 5, ;, while, (, i, !=, 0, ), {, i, -=, 1, ;, }, return, 0, ;, }, $]"
        self.assertEqual(str(self.compiler.tokens), result)

    def test_parser(self):
        """Test if the tokens were parsed succesfully."""

        self.compiler.parse()
        self.assertTrue(self.compiler.parseTree)

    def test_symbolTable(self):
        """Test the result of the symbol table."""

        self.compiler.buildSymbolTable()
        result = "{'name': 'global', 'variables': {}, 'labels': {}, 'main': {'name': 'main', '..': {...}, 'variables': {'i': 'int'}, 'labels': {}}}"
        self.assertEqual(str(self.compiler.symbolTable), result)


if __name__ == "__main__":
    unittest.main()
