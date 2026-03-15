import re

def generate_python_recursive(ir, indent=0):
    lines = []
    prefix = '    ' * indent
    for n in ir:
        if n["op"] == "function":
            args = n.get("args", "")
            args_clean = re.sub(r'(int|float|double|void|bool|char)\s*\**', '', args)
            args_clean = args_clean.replace('*', '').replace('[]', '')
            args_clean = ', '.join([a.strip() for a in args_clean.split(',') if a.strip()])
            lines.append(f'{prefix}def {n["name"]}({args_clean}):')
            body = generate_python_recursive(n.get("body", []), indent + 1)
            lines.append(body if body else f'{prefix}    pass')
            lines.append("")
        elif n["op"] == "assign":
            lines.append(f'{prefix}{n["target"]} = {n["value"]}')
        elif n["op"] == "print":
            text = n.get("text", "")
            val = n.get("value")
            if text == "%d " and val:
                lines.append(f'{prefix}print({val}, end=" ")')
            elif text == "\\n":
                lines.append(f'{prefix}print()')
            elif text and not val:
                lines.append(f'{prefix}print("{text}", end="")')
            elif val:
                lines.append(f'{prefix}print({val})')
            else:
                lines.append(f'{prefix}print()')
        elif n["op"] == "if":
            lines.append(f'{prefix}if {n["condition"]}:')
            body = generate_python_recursive(n.get("body", []), indent + 1)
            lines.append(body if body else f'{prefix}    pass')
        elif n["op"] == "loop":
            cond = n.get("condition", "")
            m = re.match(r'(\w+)\s*=\s*(.*?);\s*\1\s*<\s*(.*?);\s*\1\+\+', cond)
            if m:
                var, start, end = m.groups()
                if start == "0":
                    lines.append(f'{prefix}for {var} in range({end}):')
                else:
                    lines.append(f'{prefix}for {var} in range({start}, {end}):')
            else:
                fallback_cond = cond if cond else "True"
                lines.append(f'{prefix}while {fallback_cond}:')
            body = generate_python_recursive(n.get("body", []), indent + 1)
            lines.append(body if body else f'{prefix}    pass')
        elif n["op"] == "call":
            lines.append(f'{prefix}{n["func"]}({n["args"]})')
        elif n["op"] == "break":
            lines.append(f'{prefix}break')
        elif n["op"] == "return":
            lines.append(f'{prefix}return {n["value"]}')
    return "\n".join(lines)

def generate_python(ir):
    code = generate_python_recursive(ir, 0)
    has_main = any(x["op"] == "function" and x["name"] == "main" for x in ir)
    if has_main:
        code += "\nif __name__ == '__main__':\n    main()\n"
    return code
