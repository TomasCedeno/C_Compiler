"""
Main executable for the compiler.
"""

import sys
import getopt
import logging
import os
from util import readFile, ensureDirectory

from parser.lrParser import LRParser
import lexer.lexer as lexer
from parser.grammar import (
    DeclarationList,
    StatementList,
    Arguments,
    Parameters,
    StatementListNew,
    SwitchCaseList,
    EnumList,
    StructList,
    VarList,
)
from ir.ir import IR, readJson
from symbolTable.symbolTable import buildSymbolTable, flattenTree
from assembler.assembler import Assembler
from util import CompilerMessage, messages


class Compiler:
    """The main compiler class."""

    def __init__(self, options):
        self.filename = options.get("filename")
        self.grammar = options.get("grammar")
        self.flags = options.get("flags")
        self.output = options.get("output")
        self.input = options.get("input")
        self.asmOutput = options.get("asmOutput")
        self.tokens = []
        self.parseTree = None
        self.symbolTable = None
        self.ir = None
        self.asm = None

        # Setup default grammar if none provided
        if self.grammar is None:
            messages.add(
                CompilerMessage("No grammar specified, using default.", "warning")
            )
            self.grammar = "grammars/main_grammar.txt"

        # Setup empty list for flags if none provided
        if self.flags is None:
            self.flags = []

        # Warn if output flag exists but no filename specified
        if "-o" in self.flags and self.output is None:
            messages.add(
                CompilerMessage("No output file specified. Not dumping IR.", "warning")
            )

    def tokenize(self):
        """Tokenize the input file."""

        # Read in the file and tokenize
        code = readFile(self.filename)
        self.tokens = lexer.tokenize(code)

        if self.tokens is None:
            raise CompilerMessage("Failed to tokenize the file.")

        messages.add(CompilerMessage("Tokenized the file successfully.", "success"))

        # Print the tokens
        if "-s" in self.flags:
            messages.add(CompilerMessage("Tokens:", "important"))
            for token in self.tokens:
                print(token)

        return self.tokens

    def parse(self):
        """Parse the tokens using our LR Parser."""

        # Cannot parse until we tokenize
        if not self.tokens:
            raise CompilerMessage("Cannot parse without tokenizing first.")

        parser = LRParser()

        # Check if we should force generate the tables
        if "-f" in self.flags:
            parser.loadParseTables(self.grammar, force=True)
        else:
            parser.loadParseTables(self.grammar, force=False)

        # Parse the tokens and save the parse tree
        self.parseTree = parser.parse(self.tokens)

        if self.parseTree is None:
            messages.add(CompilerMessage("Failed to parse the tokens."))
            return None

        # Change [Program] to Program
        self.parseTree = self.parseTree[0]

        messages.add(CompilerMessage("Successfully parsed the tokens.", "success"))

        # Flatten the parse tree
        for reduce in [
            Arguments,
            Parameters,
            DeclarationList,
            StatementList,
            StatementListNew,
            SwitchCaseList,
            EnumList,
            StructList,
            VarList,
        ]:
            flattenTree(self.parseTree, reducer=reduce)

        # Print the parse tree
        if "-p" in self.flags:
            messages.add(CompilerMessage("Parse Tree:", "important"))
            parser.print()

        return self.parseTree

    def buildSymbolTable(self):
        """Build a symbol table from a parse tree."""

        # Cannot build symbol table without parse tree
        if not self.parseTree:
            raise CompilerMessage("Cannot build symbol table without a parse tree.")

        # Save the symbol table
        self.symbolTable = buildSymbolTable(self.parseTree)

        if self.symbolTable is None:
            messages.add(CompilerMessage("Failed to build the symbol table."))
            return None

        messages.add(CompilerMessage("Successfully built the symbol table.", "success"))

        # Print the symbol table if flag is present
        if "-t" in self.flags:
            messages.add(CompilerMessage("Symbol Table:", "important"))
            self.symbolTable.print()
        return self.symbolTable

    def generateIr(self):
        """Convert a parse tree to the first intermediate representation."""

        # Read in an IR from a file
        if "-i" in self.flags and self.input is not None:
            self.ir = readJson(self.input)
            messages.add(
                CompilerMessage(
                    f"Succesfully parsed the IR in '{self.input}'.", "success"
                )
            )
        else:
            # Cannot convert to IR without parse tree
            if not self.parseTree:
                raise CompilerMessage("Cannot generate an IR without a parse tree.")

            # Cannot convert to IR without symbol table
            if not self.symbolTable:
                raise CompilerMessage("Cannot generate an IR without a symbol table.")

            # Create a new instance of IR
            self.ir = IR(self.parseTree, self.symbolTable)

            # Generate the IR
            output = self.ir.generate()

            if output is None:
                messages.add(CompilerMessage("Failed to generate an IR."))
                return None

            messages.add(CompilerMessage("Successfully generated an IR.", "success"))

        if "-r" in self.flags:
            messages.add(CompilerMessage("Intermediate Representation:", "important"))
            self.ir.print()

        if "-o" in self.flags and self.output is not None:
            self.ir.write(self.output)

        return self.ir

    def assemble(self):
        """Convert the IR to assembly instructions."""

        # Cannot convert to IR without parse tree
        if not self.ir:
            raise CompilerMessage("Cannot generate asm without an IR.")

        assembler = Assembler(self.ir.ir)

        self.asm = assembler.generate()

        if self.asm is None:
            messages.add(CompilerMessage("Failed to generate the ASM."))
            return None

        messages.add(CompilerMessage("Successfully generated ASM.", "success"))

        # Print the ASM if "-a" flag
        if "-a" in self.flags:
            messages.add(CompilerMessage("ASM:", "important"))
            assembler.print()

        if "-n" in self.flags:
            assembler.write(self.asmOutput)

        return 0


def printUsage():
    """Print a usage statement."""

    bold = "\033[1m"
    end = "\033[0m"

    print(f"\n  {bold}Usage{end}:\n")
    print("    python3 main.py [<flags>] filename\n")
    print(f"  {bold}Flags{end}:\n")
    print("     -h, --help                  Output this usage information.")
    print("     -v, --verbose               Generate a log file with debug info.")
    print("     -s, --scanner               Convert a source file into tokens.")
    print("     -p, --parser                Convert tokens into a parse tree.")
    print("     -g, --grammar <filename>    Provide a grammar file to parse with.")
    print(
        "     -t, --table                 Generate a symbol table from the parse tree."
    )
    print(
        "     -f, --force                 Force the Parser to generate a new parse table."
    )
    print("     -r, --representation        Generate an intermediate representation.")
    print("     -i, --input <filename>      Input an IR file and start from there.")
    print("     -o, --output <filename>     Output the IR to a file.")
    print(
        "     -a, --asm                   Generate assembly instructions from the IR."
    )
    print("     -n, --asmOutput <filename>  Output the assembly to a file.")
    print()


def parseArguments():
    """Parse the command line arguments."""

    try:
        opts, args = getopt.getopt(
            sys.argv[1:],
            "hvsptfrag:o:i:n:",
            [
                "help",
                "verbose",
                "scan",
                "parse",
                "table",
                "force",
                "ir",
                "asm",
                "grammar=",
                "output=",
                "input=",
                "asmOutput=",
            ],
        )
    except getopt.GetoptError as err:
        print(err)
        printUsage()
        sys.exit(2)

    flags = []
    grammar = None
    output = None
    inputFile = None
    asmOutput = None

    for opt, arg in opts:
        if opt in ("-h", "--help"):
            printUsage()
            sys.exit()
        elif opt in ("-s", "--scan"):
            flags.append("-s")
        elif opt in ("-p", "--parse"):
            flags.append("-p")
        elif opt in ("-v", "--verbose"):
            flags.append("-v")
        elif opt in ("-t", "--table"):
            flags.append("-t")
        elif opt in ("-f", "--force"):
            flags.append("-f")
        elif opt in ("-o", "--output"):
            output = arg
            flags.append("-o")
        elif opt in ("-i", "--input"):
            inputFile = arg
            flags.append("-i")
        elif opt in ("-r", "--ir"):
            flags.append("-r")
        elif opt in ("-g", "--grammar"):
            grammar = arg
        elif opt in ("-a", "--asm"):
            flags.append("-a")
        elif opt in ("-n", "--asmOutput"):
            flags.append("-n")
            asmOutput = arg

    try:
        filename = args[0]
    except IndexError:
        filename = None
        if "-i" not in flags:
            print("No filename found.")
            printUsage()
            sys.exit()

    return filename, grammar, flags, output, inputFile, asmOutput


def startLog():
    """Initialize a new log file."""

    # Ensure the logs directory exists
    ensureDirectory("logs")
    logs = os.listdir("logs/")
    biggestLog = 0
    for log in logs:
        if len(log.split(".")) == 3:
            if int(log.split(".")[2]) >= biggestLog:
                biggestLog = int(log.split(".")[2]) + 1

    logging.basicConfig(
        filename="logs/compiler.log.%s" % (biggestLog),
        filemode="w",
        level=logging.DEBUG,
    )


def main():
    """Run the compiler from the command line."""

    filename, grammar, flags, output, inputFile, asmOutput = parseArguments()

    # Define levels for each step of the compiler
    # Run up to max level
    level = 0
    if not flags:
        messages.add(
            CompilerMessage(
                "No flags found! Running the compiler to the ASM stage.", "warning"
            )
        )

        # By default the compiler should output a .s file
        # much like running `gcc -O0 -S <filename>`
        # The output file is the name of the input file
        # with .c replaced with .s in the current working directory.
        flags.append("-n")
        basename = os.path.basename(filename)
        noExtension = basename.rsplit(".", 1)[0]
        asmOutput = f"{noExtension}.s"

    if "-s" in flags:
        level = 1
    if "-p" in flags:
        level = 2
    if "-t" in flags:
        level = 3
    if "-r" in flags:
        level = 4
    if "-o" in flags:
        level = 4
    if "-a" in flags:
        level = 5
    if "-n" in flags:
        level = 5

    options = {
        "filename": filename,
        "grammar": grammar,
        "flags": flags,
        "output": output,
        "input": inputFile,
        "asmOutput": asmOutput,
    }
    compiler = Compiler(options)

    try:
        # Start a log if verbose flag
        if "-v" in flags:
            startLog()

        # If not starting from IR
        if "-i" not in flags:
            for i in range(level + 1):
                if i == 1:
                    compiler.tokenize()
                elif i == 2:
                    compiler.parse()
                elif i == 3:
                    compiler.buildSymbolTable()
                elif i == 4:
                    compiler.generateIr()
                elif i == 5:
                    compiler.assemble()
        else:
            compiler.generateIr()
            if level >= 5:
                compiler.assemble()
    except CompilerMessage as err:
        print(err)
        sys.exit(2)
    except KeyboardInterrupt:
        print()
        messages.add(CompilerMessage("Compiler was interrupted."))
        sys.exit(2)


if __name__ == "__main__":
    main()
