def generate_c_recursive(ir, indent=1):
    code = []
    prefix = '    ' * indent
    for n in ir:
        if n["op"] == "function":
            code.append(f'\n{n.get("type", "void")} {n["name"]}({n["args"]}) {{')
            body = generate_c_recursive(n.get("body", []), indent + 1)
            if body: code.append(body)
            code.append(f'}}')
        elif n["op"] == "assign":
            # Very primitive typing fallback
            code.append(f'{prefix}int {n["target"]} = {n["value"]};')
        elif n["op"] == "print":
            text = n.get("text", "")
            val = n.get("value")
            if text and not val:
                code.append(f'{prefix}printf("{text}\\n");')
            elif val:
                code.append(f'{prefix}printf("{text}\\n", {val});')
            else:
                code.append(f'{prefix}printf("\\n");')
        elif n["op"] == "if":
            code.append(f'{prefix}if ({n["condition"]}) {{')
            body = generate_c_recursive(n.get("body", []), indent + 1)
            if body: code.append(body)
            code.append(f'{prefix}}}')
        elif n["op"] == "loop":
            code.append(f'{prefix}while({n.get("condition", "1")}) {{')
            body = generate_c_recursive(n.get("body", []), indent + 1)
            if body: code.append(body)
            code.append(f'{prefix}}}')
        elif n["op"] == "call":
            code.append(f'{prefix}{n["func"]}({n["args"]});')
        elif n["op"] == "break":
            code.append(f'{prefix}break;')
        elif n["op"] == "return":
            code.append(f'{prefix}return {n["value"]};')
    return "\n".join(code)

def generate_c(ir):
    code = ['#include <stdio.h>', '#include <stdbool.h>', '']
    # If no functions, wrap in main
    has_func = any(n["op"] == "function" for n in ir)
    if has_func:
        code.append(generate_c_recursive(ir, 0))
    else:
        code.append('int main() {')
        code.append(generate_c_recursive(ir, 1))
        code.append('    return 0;')
        code.append('}')
    return "\n".join(code)
