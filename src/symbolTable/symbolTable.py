"""
Contains the Symbol Table class.
"""

import parser.grammar as grammar
from util import CompilerMessage


class SymbolTable:
    """Symbol Table that represents all variables and their scopes in the program."""

    def __init__(self):
        self.table = {}
        self.table["name"] = "global"
        self.table["variables"] = {}
        self.table["labels"] = {}
        self.current = self.table
        self.level = 0

    def startScope(self, name, level):
        """Initialize a new scope."""

        if name in self.current:
            raise CompilerMessage(f"Scope with name {name} already exists.")

        # Add the new scope dict
        self.current[name] = {}
        self.current[name]["name"] = name

        # Initialize the dict with a .. and variables entry
        self.current[name][".."] = self.current
        self.current[name]["variables"] = {}
        self.current[name]["labels"] = {}

        # Update the current pointer
        self.current = self.current[name]

        # Set the current level of scope
        self.level = level

    def declareVariable(self, t, name):
        """Declare a new variable in the current scope."""

        if name in self.current["variables"]:
            raise CompilerMessage(f"Variable with name '{name}' already exists.")

        # Add the variable to the current scope
        self.current["variables"][name] = t

    def useLabel(self, name):
        """Add a new label to the label list as unverified."""

        if name not in self.current["labels"]:
            self.current["labels"][name] = False

    def declareLabel(self, name):
        """Add a new label to the label list as verified."""

        if name in self.current["labels"] and self.current["labels"][name] is True:
            raise CompilerMessage(f"Label with name '{name}' already exists.")

        self.current["labels"][name] = True

    def endScope(self):
        """Finalize a scope and return it's parent scope."""

        # Go back up one scope
        if ".." in self.current:
            self.current = self.current[".."]

    def find(self, name):
        """Find the specified variable in the Symbol Table, starting from the current scope."""

        c = self.current

        # Search the global table first
        if c == self.table:
            if name in c["variables"] or name in c or name in c["labels"]:
                return self.table["name"]

            return None

        # Search up the tree from our current scope
        # as long as there is a parent
        while ".." in c:
            if name in c["variables"] or c["name"] == name or name in c["labels"]:
                return c["name"]

            # Loop will break without checking global scope
            # So check if the parent is global scope before exiting
            if c[".."] == self.table:
                if name in self.table["variables"] or name in self.table:
                    return self.table["name"]

                return None

            c = c[".."]

        # Not found in any scope, return False
        return None

    def print(self, node=None, level=0):
        """Pretty print the symbol table."""

        if not node:
            node = self.table

        grammar.printPrefix(level)
        print(f"{node['name']}: {node['variables']}, {node['labels']}")

        for key in node:
            if key not in ["name", "variables", "..", "labels"]:
                self.print(node[key], level + 1)

    def __str__(self):
        return str(self.table)

    def verifyLabels(self, c=None):
        """Check for used but undeclared labels."""

        if c is None:
            c = self.table

        if c["labels"] is not False:
            for l in c["labels"]:
                if c["labels"][l] is False:
                    raise CompilerMessage(f"The label {l} was used but never declared.")

        for key in c:
            if key not in ["name", "variables", "..", "labels"]:
                self.verifyLabels(c[key])


def flattenTree(root, reducer, seen=False):
    """
    Collapse recursive rules to have a single parent.
    The grammar rule to collapse should be specified in reducer.
    i.e. DeclarationList or StatementList.
    """

    # TODO: fix collapsing nested recursive rules

    if isinstance(root, reducer):
        if not seen:
            seen = True

            if len(root.children) <= 1:
                return root

            c = flattenTree(root.children[0], reducer, seen)

            root.children = [root.children[1]]

            if isinstance(c, list):
                for i in c:
                    root.children.append(i)
            else:
                root.children.append(c)

            root.children.reverse()

            return root

        if len(root.children) == 1:
            # This is a DecList that only has a Dec child, no recurse
            return root.children[0]

        # Save the sibling
        dec = root.children[1]

        # Recurse on the DecList
        children = flattenTree(root.children[0], reducer, seen)

        c = [dec]

        if isinstance(children, list):
            for i in children:
                c.append(i)
        else:
            c.append(children)

        return c

    # Current node is not a DecList,
    # we just want to descend the parse tree
    if isinstance(root, list):
        for item in root:
            flattenTree(item, reducer, seen)

    # Current node is not a DecList,
    # but we will need to update its children reference
    if hasattr(root, "children"):
        children = []
        for item in root.children:
            children.append(flattenTree(item, reducer, seen))

        if isinstance(children, list) and len(children) >= 1:
            if isinstance(children[0], list):
                children = children[0]

        root.children = children
        return root

    # Not a reducer node, not a list, not a "complex" node
    # Just return it to be appended as a child
    return root


def buildSymbolTable(parseTree):
    """Given the parse tree, build a symbol table."""

    # Build the symbol table
    st = SymbolTable()
    visitChildren(parseTree, st)

    # Verify all labels are valid
    st.verifyLabels()

    return st


def visitChildren(node, st, level=0):
    """Visit each node of the parse tree."""

    # Update the symbol table for every visited node
    updateSymbolTable(node, st, level)

    if hasattr(node, "children"):
        for child in node.children:
            visitChildren(child, st, level + 1)
    elif isinstance(node, list):
        for child in node:
            visitChildren(child, st, level + 1)


def updateSymbolTable(node, st, level=0):
    """Check if symbol table should be updated based on node."""

    if isinstance(node, grammar.FunctionDeclaration):
        if st.level == level:
            st.endScope()
        st.startScope(node.name, level)
    elif isinstance(node, grammar.VariableDeclaration):
        st.declareVariable(node.type, node.name)
    elif isinstance(node, grammar.Argument):
        st.declareVariable(node.type, node.name)
    elif isinstance(node, grammar.GotoStatement):
        st.useLabel(node.children[0].value)
    elif isinstance(node, grammar.LabelDeclaration):
        st.declareLabel(node.children[0].value)
    elif isinstance(node, grammar.Identifier):
        if st.find(node.value) is None:
            raise CompilerMessage(f"Identifier {node.value} is undefined.")
