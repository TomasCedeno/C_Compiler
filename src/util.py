"""
Utility functions to be re-used across modules.
"""

import os


class Unique:
    """Class to contain unique values."""

    def __init__(self):
        self.count = {"none": 0}

    def get(self, k):
        """Get a count for a unique value."""

        try:
            return self.count[k]
        except KeyError:
            return 0

    def new(self, prefix=None):
        """Generate a new unique value."""

        if prefix:
            if prefix not in self.count:
                self.count[prefix] = 0
            self.count[prefix] += 1
            return f"{prefix}{self.count[prefix]}"

        self.count["none"] += 1
        return f"r{self.count['none']}"


unique = Unique()


def readFile(filename):
    """Read the contents of a file, if it exists."""

    try:
        with open(filename) as file:
            messages.add(CompilerMessage(f"Read file: '{filename}'.", "success"))
            return file.read()
    except IOError:
        raise CompilerMessage(f"Cannot read file: {filename}.")


def writeFile(filename, content=None):
    """Write a file with specified content."""

    if not content:
        raise CompilerMessage(f"No content specified to write to file '{filename}'.")

    try:
        with open(filename, "x") as file:
            file.write(str(content))
            messages.add(CompilerMessage(f"Wrote to file: '{filename}'.", "success"))
    except FileExistsError:
        messages.add(
            CompilerMessage(f"The file '{filename}' already exists.", "warning")
        )
        choice = input("Overwrite it? [y/n]: ")
        if choice in ["y", "Y"]:
            try:
                with open(filename, "w") as file:
                    file.write(str(content))
                    messages.add(
                        CompilerMessage(f"Wrote to file: '{filename}'.", "success")
                    )
            except IOError:
                raise CompilerMessage(f"Error overwriting file: '{filename}'.")
        else:
            messages.add(
                CompilerMessage(f"Did not overwrite the file '{filename}'.", "warning")
            )


def ensureDirectory(path):
    """Ensure that a path exists as a directory."""

    # Check if the path is a file instead of directory
    if os.path.exists(path) and not os.path.exists(f"{path}/"):
        raise CompilerMessage(
            f"Path '{path}' is a file instead of a directory. Please remove or rename the file"
            "so that logging output can be saved."
        )

    # Ensure the directory exists.
    if not os.path.exists(f"{path}/"):
        messages.add(
            CompilerMessage(f"No '{path}' directory found, creating one.", "warning")
        )
        os.makedirs(path)


class MessageCollector:
    """A collector class that hold compiler messages."""

    def __init__(self):
        self.messages = []

    def add(self, message):
        """Add a new message to the collector, and print it."""

        self.messages.append(message)
        print(message)

    def print(self):
        """Print all the messages in the collector."""

        for message in self.messages:
            print(message)


class CompilerMessage(Exception):
    """Custom CompilerMessage exception."""

    def __init__(self, message=None, level="error"):
        self.message = message
        self.level = level

    def __str__(self):
        error = "\x1B[31m"
        warn = "\x1B[33m"
        success = "\x1b[32m"
        important = "\x1b[36m"
        reset = "\x1B[0m"
        bold = "\033[1m"

        if self.level == "warning":
            return f"{bold}{warn}⚠  Warning:{reset} {self.message}"
        if self.level == "success":
            return f"{bold}{success}✔ Success:{reset} {self.message}"
        if self.level == "important":
            return f"{bold}{important}✨ {self.message}{reset}"

        return f"{bold}{error}✖ Error:{reset} {self.message}"


messages = MessageCollector()
