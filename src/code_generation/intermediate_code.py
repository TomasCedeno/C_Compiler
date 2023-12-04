"""
Métodos y clases relacionados con
Generacion de codigo intermedio a partir del ast
"""

import json
from util import unique, writeFile, readFile
import parser.grammar as grammar


class BasicBlock:
    """Define un conjunto de instrucciones y datos que componen un Bloque Básico."""

    def __init__(self, instructions, label=None):
        self.instructions = instructions
        self.label = label
        self.instructions.insert(0, ["label", label])

    def print(self):
        """Imprime este bloque básico."""

        for i in self.instructions:
            print(i)
        print()

class IR:
    """Clase de Representación Intermedia para contener datos de IR."""

    def __init__(self, parseTree, symbolTable):
        self.parseTree = parseTree
        self.symbolTable = symbolTable
        self.stack = []
        self.ir = {}
        self.current = None

    def generate(self):
        """Genera la IR a partir del árbol de análisis sintáctico."""

        self.parseTree.visit()
        self.visit(self.parseTree)

        return self.ir

    def closeBlock(self, force=False):
        """Guarda la pila como un bloque y comienza un nuevo bloque."""

        if self.stack or force is True:
            bb = BasicBlock(self.stack, unique.new("_L"))
            self.ir[self.current]["blocks"].append(bb)

        self.stack = []

    def visit(self, node):
        """Visita un nodo del ast y recursión."""

        # Inicia nuevos bloques básicos cuando encontramos ciertos nodos por primera vez.
        if isinstance(node, grammar.FunctionDeclaration):
            # Inicia una nueva entrada de función
            self.ir[node.name] = {}
            self.ir[node.name]["bloques"] = []
            self.ir[node.name]["declaraciones"] = len(
                self.symbolTable.table[node.name]["variables"]
            )
            self.current = node.name
        elif isinstance(node, grammar.IfStatement):
            self.closeBlock()
            node.savedLabel = unique.get("_L")
        elif isinstance(node, grammar.ElseStatement):
            self.closeBlock()
        elif isinstance(node, grammar.LabelDeclaration):
            self.closeBlock()
        elif isinstance(node, grammar.Condition):
            self.closeBlock()
        elif isinstance(node, grammar.WhileStatement):
            self.closeBlock()
            node.savedLabel = unique.get("_L")
        elif isinstance(node, grammar.WhileCondition):
            self.closeBlock()
        elif isinstance(node, grammar.SwitchCondition):
            self.closeBlock()
        elif isinstance(node, grammar.SwitchStatement):
            self.closeBlock()
            node.savedLabel = unique.get("_L")

        # Recursion
        if hasattr(node, "children"):
            for child in node.children:
                self.visit(child)
        elif isinstance(node, list):
            for child in node:
                self.visit(child)

        if not isinstance(node, list):
            # Finaliza los bloques básicos que creamos anteriormente ahora que todos
            # los nodos internos han sido visitados.
            if isinstance(node, grammar.FunctionDeclaration):
                self.ir[node.name]["arguments"] = node.arguments.value
                self.closeBlock()

                # Agrega un bloque básico adicional para garantizar que los saltos if funcionen correctamente
                self.closeBlock(force=True)
            elif isinstance(node, grammar.IfBody):
                if node.hasElse:
                    self.stack.append(["goto", f"_L{unique.get('_L') + 3}"])
                self.closeBlock()
            elif isinstance(node, grammar.IfStatement):
                self.closeBlock()

                if node.hasElse:
                    elseLabel = f"_L{unique.get('_L')}"
                else:
                    elseLabel = f"_L{unique.get('_L') + 1}"

                # La condición será el bloque después de la condición especificada por savedLabel
                # Pero savedLabel no es relativo a la función actual, mientras que self.ir sí lo es
                firstLabel = int(
                    self.ir[self.current]["blocks"][0].instructions[0][1][2:]
                )
                index = node.savedLabel - firstLabel + 1

                # Reemplaza el marcador de posición de la condición if con la etiqueta else
                x = self.ir[self.current]["blocks"][index].instructions
                for index, ins in enumerate(x):
                    if ins[0] == "REPLACE":
                        ins[-1] = elseLabel
                        x[index] = ins[1:]

            elif isinstance(node, grammar.Condition):
                self.stack.append(
                    [
                        "REPLACE",
                        "if",
                        node.value,
                        "GOTO",
                        f"_L{unique.get('_L') + 2}",
                        "else",
                        "GOTO",
                        "UNKNOWN",
                    ]
                )
                self.closeBlock()
            elif isinstance(node, grammar.ElseStatement):
                self.closeBlock()
            elif isinstance(node, grammar.LabelDeclaration):
                self.stack.insert(0, node.ir())
                self.closeBlock()
            elif isinstance(node, grammar.WhileStatement):
                # Debe haber un goto al final de las declaraciones while para volver a visitar la condición
                # La etiqueta de la condición es una después de lo que se guardó.
                self.stack.append(["goto", f"_L{node.savedLabel + 1}"])
                self.closeBlock()

                # La condición será el bloque después de la condición especificada por savedLabel
                # Pero savedLabel no es relativo a la función actual, mientras que self.ir sí lo es
                firstLabel = int(
                    self.ir[self.current]["blocks"][0].instructions[0][1][2:]
                )
                index = node.savedLabel - firstLabel + 1

                # breakLabel es el bloque básico que viene después de la declaración while
                breakLabel = f"_L{unique.get('_L') + 1}"

                # Reemplaza el marcador de posición de la condición while con la etiqueta de ruptura
                x = self.ir[self.current]["blocks"][index].instructions
                for index, ins in enumerate(x):
                    if ins[0] == "REPLACE":
                        ins[-1] = breakLabel
                        x[index] = ins[1:]

                # Reemplaza cualquier declaración de break con un goto a breakLabel
                for block in self.ir[self.current]["blocks"][index + 1 :]:
                    for index, ins in enumerate(block.instructions):
                        if ins == ["break"]:
                            block.instructions[index] = ["goto", breakLabel]
                        elif ins == ["continue"]:
                            block.instructions[index] = [
                                "goto",
                                f"_L{node.savedLabel + 1}",
                            ]

            elif isinstance(node, grammar.WhileCondition):
                self.stack.append(
                    [
                        "REPLACE",
                        "if",
                        node.value,
                        "GOTO",
                        f"_L{unique.get('_L') + 2}",
                        "else",
                        "GOTO",
                        "UNKNOWN",
                    ]
                )
                self.closeBlock()
            elif isinstance(node, grammar.SwitchCondition):
                self.closeBlock()
            elif isinstance(node, grammar.SwitchCase):
                condition = unique.new()
                self.stack.insert(0, [condition, "=", node.operator, "==", node.value])
                self.stack.insert(
                    1,
                    [
                        "if",
                        condition,
                        "GOTO",
                        f"_L{unique.get('_L') + 2}",
                        "else",
                        "GOTO",
                        f"_L{unique.get('_L') + 2}",
                    ],
                )
                self.closeBlock()
            elif isinstance(node, grammar.SwitchStatement):
                self.closeBlock()

                firstLabel = int(
                    self.ir[self.current]["blocks"][0].instructions[0][1][2:]
                )
                index = node.savedLabel - firstLabel

                breakLabel = f"_L{unique.get('_L') + 1}"

                # Reemplaza cualquier declaración de break con un goto a breakLabel
                for block in self.ir[self.current]["bloques"][index + 1 :]:
                    for index, ins in enumerate(block.instructions):
                        if ins == ["break"]:
                            block.instructions[index] = ["goto", breakLabel]
                        elif ins == ["continue"]:
                            block.instructions[index] = [
                                "goto",
                                f"_L{node.savedLabel + 1}",
                            ]

            else:
                i = node.ir()
                if i is not None:
                    self.stack.append(i)

    def print(self):
        """Imprime la representación intermedia como una cadena."""

        print("```")
        for function in self.ir:
            print(f".{function} {self.ir[function]['argumentos']}")
            print()  # Diferenciar entre bloques básicos
            for block in self.ir[function]["bloques"]:
                block.print()
        print("```")



    def write(self, filename):
        """"""

        s = []
        for function in self.ir:
            s.append(
                [
                    f".{function}",
                    self.ir[function]["argumentos"],
                    len(self.symbolTable.table[function]["variables"]),
                ]
            )
            for block in self.ir[function]["bloques"]:
                for instruction in block.instructions:
                    s.append(instruction)

        writeFile(filename, json.dumps(s))

    def __str__(self):
        s = []

        for function in self.ir:
            s.append(f".{function} ({self.ir[function]['argumentos']})")
            for block in self.ir[function]["bloques"]:
                for line in block:
                    s.append(line)

        return "\n".join(s)