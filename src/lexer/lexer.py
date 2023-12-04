"""
Lexing phase of the compiler.
Converts a file into a list of identified tokens.
"""

import re
import logging
import lexer.tokens as tokens
from lexer.tokens import Token, symbols, keywords
from util import CompilerMessage

debug = False


def tokenize(code):
    """Parse the file (as a string) into a list of tokens."""

    # Big array of parsed Tokens
    codeTokens = []
    isComment = False

    lines = code.splitlines()
    lines = combineEscapedLines(lines)

    for line in lines:
        # Get the tokens of the current line and add to the big list
        lineTokens, isComment = tokenizeLine(line, isComment)
        codeTokens.extend(lineTokens)

    codeTokens.append(Token(tokens.eof, "$"))

    # Check for floating point numbers
    codeTokens = parseFloats(codeTokens)

    return codeTokens


def tokenizeLine(line, isComment):
    """Parse a line into tokens"""
    lineTokens = []

    # We parse characters in a "chunk" with a start and an end
    # Start both counters at 0 to catch whitespace at beginning of a line
    start = 0
    end = 0

    while end < len(line):
        if debug is True:
            logging.debug("%s:%s = '%s'", start, end, line[start:end])

        symbol = matchSymbol(line, end)

        try:
            nextSymbol = matchSymbol(line, end + 1)
        except IndexError:
            nextSymbol = None

        # Order of searching:
        # 1. Symbols
        # 2. Operators
        # 3. Keywords
        # 4. Identifiers
        # 5. Numbers

        # Check if we are on an include line, if so, then go to the next line
        # NOTE: our subset of C specifies that includes must be on their own line
        if symbol == tokens.pound:
            if debug is True:
                logging.debug("Found include statement.")

            if line[(start + 1) : (start + 8)] == "include":
                previousTokens = parseInclude(line, start + 1)
                lineTokens.append(previousTokens)
                break

        # If we are in a multi-line /* */ comment
        if isComment:
            # If the comment is ending
            if symbol == tokens.star and nextSymbol == tokens.slash:
                if debug is True:
                    logging.debug("Found end of multi-line comment.")

                isComment = False
                start = end + 2
                end = start
            else:
                start += 1
                end = start
            continue

        # If next two symbols begin a multi-line /* */ comment
        if symbol == tokens.slash and nextSymbol == tokens.star:
            if debug is True:
                logging.debug("Found beginning of multi-line comment.")

            # Tokenize whatever we found up to this point
            isComment = True
            if start != end:
                previousTokens = tokenizeChunk(line[start:end])
                lineTokens.append(previousTokens)

            start += 1
            end = start
            continue

        # If next two tokens are //, skip this line, break from while loop, and return
        if symbol == tokens.slash and nextSymbol == tokens.slash:
            if debug is True:
                logging.debug("Found single line comment, skipping line!")
            break

        # If ending character of chunk is whitespace
        if line[end].isspace():
            if debug is True:
                logging.debug("Found whitespace.")

            # Tokenize whatever we found up to this point, and skip whitespace
            if start != end:
                previousTokens = tokenizeChunk(line[start:end])
                lineTokens.append(previousTokens)

            start = end + 1
            end = start
            continue

        # If we see a quote, tokenize the entire quoted value as one token
        if symbol in {tokens.doubleQuote, tokens.singleQuote}:
            if symbol == tokens.doubleQuote:
                delimeter = '"'
            elif symbol == tokens.singleQuote:
                delimeter = "'"

            if debug is True:
                logging.debug("Found a quoted string. Attempting to parse...")

            # Get the token between the quotes and update our chunk end
            token, end = parseQuote(line, start, delimeter)
            lineTokens.append(token)

            start = end
            continue

        if symbol == tokens.minus:
            tmp = start + 1
            tmpe = end + 2

            num = ""

            while line[tmp:tmpe].isdigit():
                num += line[tmp:tmpe]
                tmp += 1
                tmpe += 1

            start = tmp
            end = start

            if num != "":
                lineTokens.append(Token(tokens.number, f"-{num}"))
            else:
                lineTokens.append(Token(tokens.minus, "-"))

            continue

        if symbol == tokens.colon:
            if matchNumber(line[start:end]) is None:
                lineTokens.append(Token(tokens.label, line[start:end]))
                start = end + 1
                end = start

        # If next character is a symbol
        if symbol is not None:
            # Tokenize whatever we found up to this point
            if start != end:
                previousTokens = tokenizeChunk(line[start:end])
                lineTokens.append(previousTokens)

            # Append the next token
            if debug is True:
                logging.debug("Found token %s", symbol)
            lineTokens.append(Token(symbol))

            # Move the chunk forward
            start = end + len(symbol.rep)
            end = start

            continue

        # If none of the above cases have hit, we must increase our search
        # So we increment our chunk end to include an additional character
        end += 1

    # At this point we have parsed the entire line
    # Flush anything left in the chunk
    if start != end:
        previousTokens = tokenizeChunk(line[start:end])
        lineTokens.append(previousTokens)

    # Finally return the list of tokens for this line
    return lineTokens, isComment


def parseQuote(line, start, delimeter):
    """Parse the quote value from the line."""
    characters = []
    i = start + 1

    while True:
        if i >= len(line):
            raise ValueError("Missing terminating quote!")
        if line[i] == delimeter:
            return Token(tokens.string, "".join(characters)), i + 1

        characters.append(line[i])
        i += 1


def parseInclude(text, start):
    """Parse the filename from the include statement line."""
    file = re.split("[<>]", text[(start + 9) :])[0]
    return Token(tokens.filename, file)


def tokenizeChunk(text):
    """Check if the given text is a keyword, number, or identifier"""
    # Check if its a keyword first
    keyword = matchKeyword(text)
    if keyword is not None:
        if debug is True:
            logging.debug("Found keyword: %s", text)
        return Token(keyword, text)

    # Check if it a number second
    number = matchNumber(text)
    if number is not None:
        if debug is True:
            logging.debug("Found number: %s", text)
        return Token(tokens.number, text)

    # Check if it an identifier third
    identifier = matchIdentifier(text)
    if identifier is not None:
        if debug is True:
            logging.debug("Found identifier: %s", text)
        return Token(tokens.identifier, text)

    label = matchLabel(text)
    if label is not None:
        if debug is True:
            logging.debug("Found label: %s", text)
        print(f"Found label: {text}")
        return Token(tokens.label, text[:-1])

    # If it is none of the above, we do not recognize this type
    raise CompilerMessage(f"Unrecogized token: '{text}'")


def matchSymbol(line, start):
    """Check if a string matches a symbol"""
    for symbol in symbols:
        try:
            for i, char in enumerate(symbol.rep):
                if line[start + i] != char:
                    break
            else:
                return symbol
        except IndexError:
            pass

    return None


def matchKeyword(text):
    """Check if string matches a keyword"""
    for keyword in keywords:
        if keyword.rep == text:
            return keyword

    return None


def matchIdentifier(text):
    """Check if string matches an identifier"""
    if re.match(r"[_a-zA-Z][_a-zA-Z0-9]*$", text):
        return text

    return None


def matchLabel(text):
    """Check if string matches a label"""
    if re.match(r"[_a-zA-Z][_a-zA-Z0-9:]*$", text):
        return text

    return None


def matchNumber(text):
    """Check if string matches a number"""
    if text.isdigit():
        return text

    return None


def parseFloats(l):
    """Check for floating point numbers"""

    # Copy the tokens as they change while we iterate
    tokensWithFloats = l.copy()
    index = 0

    while index < len(tokensWithFloats):
        token = tokensWithFloats[index]

        if (
            token.kind == tokens.number
            and tokensWithFloats[index + 1].kind == tokens.period
            and tokensWithFloats[index + 2].kind == tokens.number
        ):
            floatValue = f"{token.content}.{tokensWithFloats[index + 2].content}"
            tokensWithFloats[index] = Token(tokens.number, floatValue)

            # We delete at the same index here because the
            # list will have shifted after first deletion
            del tokensWithFloats[index + 1]
            del tokensWithFloats[index + 1]

        index += 1

    return tokensWithFloats


def combineEscapedLines(lines):
    """Combine escaped lines into a singular line."""

    # Replace any \t characters
    lines = [line.replace("\t", "") for line in lines]

    # Copy the lines because we are changing while we iterate
    combinedLines = lines.copy()

    for i, line in enumerate(lines):
        if str.endswith(line, "\\"):
            escapedLine = combinedLines[i][:-1]
            nextLine = combinedLines[i + 1]
            combinedLines[i] = escapedLine + nextLine
            del combinedLines[i + 1]

    return combinedLines
