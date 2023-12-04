"""
Returns the number of characters in a file.
"""

import sys


def usage():
    """Print a usage statement."""
    print("\n  Usage:")
    print("    python character_count.py [filename]\n")


# Ensure filename is passed as command line argument
if len(sys.argv) < 2:
    print("Filename not specified.")
    usage()
    sys.exit(-1)

fName = sys.argv[1]

try:
    fileIn = open(fName, "r")
    numChars = 0

    for line in fileIn:
        wordList = line.split()

        # Produces length of each word and appends to sum
        numChars += sum(len(word) for word in wordList)

    print(str(numChars) + " Characters")
except FileNotFoundError:
    print(f"The file {fName} cannot be opened.")
