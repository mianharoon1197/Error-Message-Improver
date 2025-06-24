errors = []

def record(line, message, err_type, fix):
    errors.append({'line': line, 'message': message, 'type': err_type, 'fix': fix})

def clear():
    errors.clear()

def summary():
    if not errors:
        return "\n✅ No errors detected.\n"

    # Get max column widths
    line_w = max(len("Line"), max(len(str(e['line'])) for e in errors))
    msg_w = max(len("Error"), max(len(e['message']) for e in errors))
    type_w = max(len("Type"), max(len(e['type']) for e in errors))
    fix_w = max(len("Fix"), max(len(e['fix']) for e in errors))

    header = f"{'Line':<{line_w}}  {'Error':<{msg_w}}  {'Type':<{type_w}}  {'Fix':<{fix_w}}"
    divider = "-" * len(header)

    table = "\n🔍 Summary Table\n" + header + "\n" + divider + "\n"
    for e in errors:
        table += f"{e['line']:<{line_w}}  {e['message']:<{msg_w}}  {e['type']:<{type_w}}  {e['fix']:<{fix_w}}\n"

    return table
