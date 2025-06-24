register_counter = 0
label_counter = 0
variable_values = {}
functions = {}
asm_lines = []  # ✨ Collect all assembly here


def new_register():
    global register_counter
    reg = f"%r{register_counter}"
    register_counter += 1
    return reg


def new_label():
    global label_counter
    label = f"L{label_counter}"
    label_counter += 1
    return label


def emit(line):
    asm_lines.append(line)
    print(line)  # Optional: still print to terminal


def generate_code(node, filename="output.asm"):
    if node.nodetype == 'program':
        emit("section .data")
        for child in node.children:
            if child.nodetype == 'declare':
                emit(f"{child.value} db 0")
        emit("section .text")
        for child in node.children:
            generate_code(child)

        # 📝 Write to .asm file
        with open(filename, 'w') as f:
            f.write("\n".join(asm_lines))
        print(f"\n✅ Assembly code saved to: {filename}")

    elif node.nodetype == 'declare':
        var = node.value
        emit(f"; declare {var}")

    elif node.nodetype == 'declare_assign':
        var = node.value
        if node.children:
            reg = eval_expr(node.children[0])
            emit(f"mov {var}, {reg}")
        else:
            emit(f"{var} db 0")

    elif node.nodetype == 'assign':
        var = node.value
        reg = eval_expr(node.children[0])
        emit(f"mov {var}, {reg}")
        variable_values[var] = reg

    elif node.nodetype == 'if':
        else_label = new_label()
        cond = eval_expr(node.children[0])
        emit(f"cmp {cond}, 0")
        emit(f"je {else_label}")
        generate_code(node.children[1])
        emit(f"{else_label}:")

    elif node.nodetype == 'if_else':
        else_label = new_label()
        end_label = new_label()
        cond = eval_expr(node.children[0])
        emit(f"cmp {cond}, 0")
        emit(f"je {else_label}")
        generate_code(node.children[1])
        emit(f"jmp {end_label}")
        emit(f"{else_label}:")
        generate_code(node.children[2])
        emit(f"{end_label}:")

    elif node.nodetype == 'while':
        start = new_label()
        end = new_label()
        emit(f"{start}:")
        cond = eval_expr(node.children[0])
        emit(f"cmp {cond}, 0")
        emit(f"je {end}")
        generate_code(node.children[1])
        emit(f"jmp {start}")
        emit(f"{end}:")

    elif node.nodetype == 'block':
        for stmt in node.children:
            generate_code(stmt)

    elif node.nodetype == 'func_decl':
        fname = node.value
        functions[fname] = node
        emit(f"\n; Function {fname}")
        emit(f"{fname}:")
        # Skip param node
        if node.children and node.children[1].nodetype == 'block':
            generate_code(node.children[1])
        emit("ret")

    elif node.nodetype == 'func_call':
        fname = node.value
        args = [eval_expr(arg) for arg in node.children]
        for i, reg in enumerate(args):
            emit(f"push {reg} ; arg{i}")
        emit(f"call {fname}")
        emit(f"add esp, {len(args) * 4}")

    elif node.nodetype == 'return':
        val = eval_expr(node.children[0])
        emit(f"mov eax, {val}")
        emit("ret")

    else:
        emit(f"; Unhandled node: {node.nodetype}")


def eval_expr(node):
    if node.nodetype == 'number':
        reg = new_register()
        emit(f"mov {reg}, {node.value}")
        return reg

    elif node.nodetype == 'id':
        return node.value

    elif node.nodetype == 'binop':
        left = eval_expr(node.children[0])
        right = eval_expr(node.children[1])
        result = new_register()
        emit(f"mov {result}, {left}")
        if node.value == '+':
            emit(f"add {result}, {right}")
        elif node.value == '-':
            emit(f"sub {result}, {right}")
        elif node.value == '*':
            emit(f"imul {result}, {right}")
        elif node.value == '/':
            emit(f"mov eax, {left}")
            emit("cdq")
            emit(f"idiv {right}")
            emit(f"mov {result}, eax")
        return result

    elif node.nodetype == 'cmpop':
        left = eval_expr(node.children[0])
        right = eval_expr(node.children[1])
        emit(f"cmp {left}, {right}")
        return left

    return "0"
