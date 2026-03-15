def generate_cpp_recursive(ir, indent=1):
    code = []
    prefix = '    ' * indent
    for n in ir:
        if n["op"] == "function":
            code.append(f'\n{n.get("type", "void")} {n["name"]}({n["args"]}) {{')
            body = generate_cpp_recursive(n.get("body", []), indent + 1)
            if body: code.append(body)
            code.append(f'}}')
        elif n["op"] == "assign":
            # primitive fallback
            code.append(f'{prefix}int {n["target"]} = {n["value"]};')
        elif n["op"] == "print":
            text = n.get("text", "")
            val = n.get("value")
            text_cleaned = text.replace("\\n", "")
            if text_cleaned and not val:
                code.append(f'{prefix}cout << "{text_cleaned}" << endl;')
            elif val:
                code.append(f'{prefix}cout << {val} << endl;')
            else:
                code.append(f'{prefix}cout << endl;')
        elif n["op"] == "if":
            code.append(f'{prefix}if ({n["condition"]}) {{')
            body = generate_cpp_recursive(n.get("body", []), indent + 1)
            if body: code.append(body)
            code.append(f'{prefix}}}')
        elif n["op"] == "loop":
            code.append(f'{prefix}while({n.get("condition", "true")}) {{')
            body = generate_cpp_recursive(n.get("body", []), indent + 1)
            if body: code.append(body)
            code.append(f'{prefix}}}')
        elif n["op"] == "call":
            code.append(f'{prefix}{n["func"]}({n["args"]});')
        elif n["op"] == "break":
            code.append(f'{prefix}break;')
        elif n["op"] == "return":
            code.append(f'{prefix}return {n["value"]};')
    return "\n".join(code)

def generate_cpp(ir):
    code = ['#include <iostream>', 'using namespace std;', '']
    has_func = any(n["op"] == "function" for n in ir)
    if has_func:
        code.append(generate_cpp_recursive(ir, 0))
    else:
        code.append('int main() {')
        code.append(generate_cpp_recursive(ir, 1))
        code.append('    return 0;\n}')
    return "\n".join(code)
