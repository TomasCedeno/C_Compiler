"""
Methods and classes related to
Intermediate Representations of the Parse Tree.
"""

import json
from util import unique, writeFile, readFile
import parser.grammar as grammar


def readJson(filename):
    """Read in JSON file"""

    # Read the data into a string and parse the string as JSON
    data = readFile(filename)
    lines = json.loads(data)

    # Setup an empty IR instance that we will populate
    ir = IR(None, None)

    for entry in lines:
        command = entry[0]

        # Start a new function and add it to the IR
        if command.startswith("."):
            name = command[1:]
            ir.ir[name] = {}
            ir.ir[name]["blocks"] = []
            ir.ir[name]["arguments"] = entry[1]
            ir.ir[name]["declarations"] = entry[2]
            currentFunction = ir.ir[name]
        elif command == "label":
            currentBlock = BasicBlock([], entry[1])
            currentFunction["blocks"].append(currentBlock)
        else:
            currentBlock.instructions.append(entry)

    return ir


class BasicBlock:
    """Defines a set of instructions and data that compose a Basic Block."""

    def __init__(self, instructions, label=None):
        self.instructions = instructions
        self.label = label
        self.instructions.insert(0, ["label", label])

    def print(self):
        """Print this basic block."""

        for i in self.instructions:
            print(i)
        print()


class IR:
    """Intermediate Representation class to hold IR data."""

    def __init__(self, parseTree, symbolTable):
        self.parseTree = parseTree
        self.symbolTable = symbolTable
        self.stack = []
        self.ir = {}
        self.current = None

    def generate(self):
        """Generate the IR from the parse tree."""

        self.parseTree.visit()
        self.visit(self.parseTree)

        return self.ir

    def closeBlock(self, force=False):
        """Save the stack as a block and start a new block."""

        if self.stack or force is True:
            bb = BasicBlock(self.stack, unique.new("_L"))
            self.ir[self.current]["blocks"].append(bb)

        self.stack = []

    def visit(self, node):
        """Visit a node of the parse tree and recurse."""

        # Start new basic blocks when we first encounter certain nodes.
        if isinstance(node, grammar.FunctionDeclaration):
            # Start a new function entry
            self.ir[node.name] = {}
            self.ir[node.name]["blocks"] = []
            self.ir[node.name]["declarations"] = len(
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

        # Slide to the left, slide to the right
        # Recurse recurse, recurse recurse!
        # ~ Dj Casper (Cha Cha Slide)
        if hasattr(node, "children"):
            for child in node.children:
                self.visit(child)
        elif isinstance(node, list):
            for child in node:
                self.visit(child)

        if not isinstance(node, list):
            # End the basic blocks we created earlier now that all
            # the node within have been visited.
            if isinstance(node, grammar.FunctionDeclaration):
                self.ir[node.name]["arguments"] = node.arguments.value
                self.closeBlock()

                # Add an extra basic block to ensure if jumps work correctly
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

                # The condition will be the block after the condition specified by savedLabel
                # But savedLabel is not relational to the current function, whereas self.ir is
                firstLabel = int(
                    self.ir[self.current]["blocks"][0].instructions[0][1][2:]
                )
                index = node.savedLabel - firstLabel + 1

                # Replace the placeholder of the if condition with the else label
                x = self.ir[self.current]["blocks"][index].instructions
                for index, ins in enumerate(x):
                    if ins[0] == "REPLACEME":
                        ins[-1] = elseLabel
                        x[index] = ins[1:]

            elif isinstance(node, grammar.Condition):
                self.stack.append(
                    [
                        "REPLACEME",
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
                # Must have a goto at the end of while statements to revisit the condition
                # The label of the condition is one after what was saved.
                self.stack.append(["goto", f"_L{node.savedLabel + 1}"])
                self.closeBlock()

                # The condition will be the block after the condition specified by savedLabel
                # But savedLabel is not relational to the current function, whereas self.ir is
                firstLabel = int(
                    self.ir[self.current]["blocks"][0].instructions[0][1][2:]
                )
                index = node.savedLabel - firstLabel + 1

                # breakLabel is the basic block that comes after the while statement
                breakLabel = f"_L{unique.get('_L') + 1}"

                # Replace the placeholder of the while condition with break label
                x = self.ir[self.current]["blocks"][index].instructions
                for index, ins in enumerate(x):
                    if ins[0] == "REPLACEME":
                        ins[-1] = breakLabel
                        x[index] = ins[1:]

                # Replace any break statements with a goto to the breakLabel
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
                        "REPLACEME",
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

                # Replace any break statements with a goto to the breakLabel
                for block in self.ir[self.current]["blocks"][index + 1 :]:
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
        """Print the intermediate representation as a string."""

        print("```")
        for function in self.ir:
            print(f".{function} {self.ir[function]['arguments']}")
            print()  # Differentiate between basic blocks
            for block in self.ir[function]["blocks"]:
                block.print()
        print("```")

    def write(self, filename):
        """Write the ASM to a JSON file."""

        s = []
        for function in self.ir:
            s.append(
                [
                    f".{function}",
                    self.ir[function]["arguments"],
                    len(self.symbolTable.table[function]["variables"]),
                ]
            )
            for block in self.ir[function]["blocks"]:
                for instruction in block.instructions:
                    s.append(instruction)

        writeFile(filename, json.dumps(s))

    def __str__(self):
        s = []

        for function in self.ir:
            s.append(f".{function} ({self.ir[function]['arguments']})")
            for block in self.ir[function]["blocks"]:
                for line in block:
                    s.append(line)

        return "\n".join(s)
