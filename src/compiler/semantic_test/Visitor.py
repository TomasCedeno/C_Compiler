import lark
from .Symtable import Symtable

class Visitor(lark.Visitor):
	
    def __init__(self, symtable, onerr, onwarn, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.symtable = symtable
        self.__onerr = onerr
        self.onwarn = onwarn
        self.ok = True

    def onerr(self, line, msg):
        self.__onerr(line, msg)
        self.ok = False

    def visit_top_down(self, tree):
        for subtree in tree.iter_subtrees_topdown():
            self._call_userfunc(subtree)
        return tree

    def variable_declaration(self, tree):
        type_node = tree.children[0]
        identifier_node = tree.children[1]
        
        name = identifier_node.value
        scope = Symtable.get_scope(tree)
        _type = type_node.children[0].value

        if _type != "int":
            self.onwarn(
                tree.line,
                f"Variable type for {repr(name)} assumed as 'int' because it cannot be {repr(_type)}."
            )
            _type = "int"

        if tree.children[2].type == "END_COMMAND":  # regular variable
            previous = self.symtable.add_variable(
                name=name,
                _type=_type,
                scope=scope,
                line=tree.meta.line
            )
        else:  # vector
            size = int(tree.children[3].value)
            if size == 0:
                self.onerr(
                    tree.line,
                    f"Vector {repr(name)} cannot be defined with size 0."
                )
            previous = self.symtable.add_vector(
                name=name,
                _type=_type,
                scope=scope,
                line=tree.meta.line,
                size=size
            )
        if previous:
            self.onerr(
                tree.meta.line,
                Visitor.__var_already_declared(previous)
            )
            return
        tree.entry = self.symtable.get(scope, name)

    def return_declaration(self, tree):
        scope = Symtable.get_scope(tree)
        is_return_void = (len(tree.children) == 2)

        parent_function = go_up_and_find(tree, "function_declaration")
        if parent_function is None:  
            self.onerr(
                tree.line,
                f"Return declaration outside any function."
            )
            return
        parent_function_var = parent_function.entry
        parent_function_var.does_return = True
        if is_return_void:
            if parent_function_var.type != "void":
                self.onerr(
                    tree.line,
                    f"Void return in a {repr(parent_function_var.type)} function."
                )
            else:
                # ok, void return and function is void as well
                pass
            return
        # return is non-void
        if parent_function_var.type == "void":
            self.onerr(
                tree.line,
                "Non-void return in a 'void' function."
            )
            return
        # return is non-void and function is int
        expression = tree.children[1].expression
        if isinstance(expression, int):  
            return
        # it's fine as well, screwed up expressions are fixed later

    def function_declaration(self, tree):
        type_node = tree.children[0]
        identifier_node = tree.children[1]
        parameters = tree.children[3]
        args = []
        func_scope = Symtable.get_scope(tree.parent)
        func_name = identifier_node.value
        
        # add function to symtable
        previous = self.symtable.add_function(
            name=func_name,
            _type=type_node.children[0].value,
            scope=func_scope,
            line=tree.meta.line,
            args=args
        )
        if previous:
            self.onerr(
                tree.meta.line,
                Visitor.__var_already_declared(previous)
            )
            return
        tree.entry = self.symtable.get(func_scope, func_name)
        if tree.entry.name == "main":
            tree.entry.referenced = True
        
        # get params and add them to symtable
        for param in parameters.find_data("param"):
            param_type = param.children[0]
            param_identifier = param.children[1]
            
            param_name = param_identifier.value
            param_scope = Symtable.get_scope(param)
            _type = param_type.children[0].value
            if _type != "int":
                self.onwarn(
                    tree.line,
                    f"Variable type for {repr(param_name)} assumed as 'int' because it cannot be {repr(_type)}."
                )
                _type = "int"
            if len(param.children) == 2:
                previous = self.symtable.add_variable(
                    name=param_name,
                    _type=_type,
                    scope=param_scope,
                    line=param.meta.line
                )
            else:
                previous = self.symtable.add_vector(
                    name=param_name,
                    _type=_type,
                    scope=param_scope,
                    line=param.meta.line,
                    size=None
                )

            if previous:
                self.onerr(
                    param.meta.line,
                    Visitor.__var_already_declared(previous)
                )
            arg_var = self.symtable.get(param_scope, param_name)
            arg_var.referenced = True
            arg_var.initialized = True
            args.append(arg_var)

    def __var_already_declared(previous):
        f_or_var = 'variable' if previous.is_var() else 'function'
        return f"{f_or_var} {repr(previous.name)} has already been declared as {repr(previous.type)} at line {previous.line}."

    def variable(self, tree):
        identifier = tree.children[0]
        var = self.symtable.get(tree, identifier.value)
        if not var:
            self.onerr(
                tree.line,
                f"Undeclared variable {repr(identifier.value)}."
            )
            return
        if var.is_function():
            self.onerr(
                tree.line,
                f"The function {repr(var.name)} defined at line {var.line} is being referenced as a variable."
            )
            return
        var.referenced = True
        tree.entry = var
        if not var.is_vector() and tree.expression.data == "vector":
            self.onerr(
                tree.line,
                f"{repr(var.name)} was defined as a simple variable at line {var.line}, not as a vector, impossible to index."
            )
            return
        elif var.is_vector() and tree.expression.data != "vector":
            err = False
            for parent in iterate_parents(tree):
                if getattr(parent, "expression", None) == None:
                    break
                exp = parent.expression
                if exp.data == "list":
                    # is being called in an argument
                    break
                if exp.data not in {"variable", "="}:
                    msg = exp.data
                    err = True
                    break
                elif exp.data == "=":
                    l, r = exp.children
                    if l.data == "variable" and r.data == "variable":
                        l_var = self.symtable.get(tree, l.var_name)
                        r_var = self.symtable.get(tree, l.var_name)
                        if l_var != None and r_var != None:
                            if not (l_var.is_vector() and r_var.is_vector()):
                                err = True
                        else:
                            err = True
                    else:
                        err = True
                if err:
                    msg = "="
                    break

            if err:
                self.onerr(
                    tree.line,
                    f"Invalid operation {repr(msg)} for the vector {repr(var.name)} defined at line {var.line}."
                )
                return        
        if tree.expression.data != "vector":
            return

        exp = tree.expression.children[0]
        if isinstance(exp, int):
            if exp < 0:
                self.onerr(
                    tree.line,
                    f"Negative access {repr(str(exp))} to the vector {repr(identifier.value)}."
                )

    def activation(self, tree):
        identifier = tree.children[0]
        arguments = tree.children[2]
        exp = tree.expression

        var = self.symtable.get(tree, identifier.value)
        if not var:
            self.onerr(
                tree.line,
                f"The function {repr(identifier.value)} is not declared."
            )
            return
        tree.entry = var
        var.referenced = True
        if var.type == "void":
            declaration_expression = go_up_and_find(tree, "declaration_expression")
            if declaration_expression.children[0].expression.data != "activation":
                self.onerr(
                    tree.line,
                    f"The void function {repr(var.name)} declared at line {var.line} is being called within an expression."
                )
                return

        # arguments match
        are_args_vars = [not arg.is_vector() for arg in var.args]
        are_exps_vars = []
        for e in exp.children:
            if isinstance(e, int):  # if constant, True
                are_exps_vars.append(True)
            elif len(e.children) == 0:  # if a single variable, and symtable returns vector, then it is false
                this_var = self.symtable.get(tree, e.var_name)
                if not this_var:
                    return
                are_exps_vars.append(not this_var.is_vector())
            else:  # there is a complex expression, false expressions are ignored so this should as well
                are_exps_vars.append(True)
        
        if not (len(var.args) == len(exp.children) and all(x == y for x, y in zip(are_args_vars, are_exps_vars))):
            called_with = ",".join(repr("int" if b else "vector of int") for b in are_exps_vars)
            expected = ",".join(repr("int" if b else "vector of int") for b in are_args_vars)

            self.onerr(
                tree.line,
                f"The function {repr(var.name)} defined at line {var.line} was called with variables {called_with if called_with else 'no variables'}, expected {expected if expected else 'no variables'}."
            )

    def expression(self, tree):
        exp = tree.expression
        if isinstance(exp, lark.Tree) and exp.data == "=":
            l_var = self.symtable.get(tree, exp.children[0].var_name)
            if l_var != None:
                l_var.initialized = True

    def selection_declaration(self, tree):
        parent_function = go_up_and_find(tree, "function_declaration").entry
        scope = Symtable.get_scope(tree)
        tree.label = f"{scope}.if{parent_function.no_ifs}"
        parent_function.no_ifs += 1

    def iteration_declaration(self, tree):
        parent_function = go_up_and_find(tree, "function_declaration").entry
        scope = Symtable.get_scope(tree)
        tree.label = f"{scope}.while{parent_function.no_whiles}"
        parent_function.no_whiles += 1

def iterate_parents(tree):
    while True:
        tree = tree.parent
        if not tree:
            break
        yield tree

def go_up_and_find(tree, rule):
    return next((ans for ans in iterate_parents(tree) if ans.data == rule), None)