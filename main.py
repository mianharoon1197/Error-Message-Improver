# ✅ Final working main.py (fully updated and AST compatible)
from lexer import lexer
from parser import parser
from codegen import generate_code
from semantic import clear_table
from ast_visualizer import visualize_ast, print_ast_tree
from errors import clear as clear_errors, summary as error_summary
import parser as parser_module
import os

print("\U0001F3AF Compiler Error Message Improver\n")

# 📂 Ask for input file
file_path = input("\U0001F4C4 Enter source code file path (e.g., test.txt): ").strip()
if not os.path.exists(file_path):
    print(f"\u274C Error: File '{file_path}' not found.")
    exit(1)

# 📄 Load source code
with open(file_path, 'r') as f:
    code = f.read()

print(f"\n\U0001F4DC Source code loaded from: {file_path}\n")

# Pass source code to parser module (used for context in error reporting)
parser_module.source_code = code

# Reset previous errors and semantic context
clear_errors()
clear_table()

# 🚀 Parse input
ast = None
try:
    ast = parser.parse(code, lexer=lexer)
    if ast is None:
        print("\n\U0001F534 Parsing returned no AST (possibly due to syntax error).")
except Exception as e:
    print(f"\n\u274C Internal Parsing Error: {e}")

# ✅ Output
if ast is not None:
    print("✅ AST successfully constructed.\n")

    print("\U0001F50D AST Tree (Text View):")
    print_ast_tree(ast)

    print("\n\U0001F5BC️ Visualizing AST and saving output...")
    visualize_ast(ast)

    print("\n\u2692️ Code Generation Output:")
    generate_code(ast)

    print("\n✅ Compilation completed successfully.\n")
else:
    print("\n\u274C Compilation failed due to parsing or semantic errors.\n")

# 🔎 Optional token view — enable to debug tokens
DEBUG_TOKENS = True
if DEBUG_TOKENS:
    print("\U0001F50E Tokens from source code:")
    lexer.input(code)
    for token in lexer:
        print(token)

# 🧾 Error Summary
print(error_summary())