# Simple Calculator Interpreter

A lexical analyzer and parser that tokenizes and interprets simple arithmetic expressions in Python.

## Description

A calculator that reads user input (e.g., "3+5") and uses lexical analysis and parsing to evaluate the expression and return the result.

## Features

- Lexical analyzer (scanner/tokenizer) to break input into tokens
- Token class to represent INTEGER, PLUS, and EOF token types
- Recursive descent parser using the `expr()` method
- Error handling for malformed input
- Interactive command-line interface with `calc>` prompt

## How It Works

1. **Lexical Analysis** - Input string is converted into tokens (INTEGER, PLUS, EOF)
2. **Parsing** - Tokens are validated to match the grammar: `INTEGER PLUS INTEGER`
3. **Interpretation** - The parser evaluates and returns the sum of the two integers

## How to Run

```bash
python calculator.py
```

Enter expressions at the `calc>` prompt:
