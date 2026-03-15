def generate_java_recursive(ir, indent=2):
    code = []
    prefix = '    ' * indent
    for n in ir:
        if n["op"] == "function":
            static_mod = "static " if n["name"] != "main" else ""
            if n["name"] == "main":
                code.append(f'\n{prefix}public static void main(String[] args) {{')
            else:
                code.append(f'\n{prefix}public {static_mod}{n.get("type", "void")} {n["name"]}({n["args"]}) {{')
            body = generate_java_recursive(n.get("body", []), indent + 1)
            if body: code.append(body)
            code.append(f'{prefix}}}')
        elif n["op"] == "assign":
            code.append(f'{prefix}int {n["target"]} = {n["value"]};')
        elif n["op"] == "print":
            text = n.get("text", "")
            val = n.get("value")
            text_cleaned = text.replace("\\n", "")
            if text_cleaned and not val:
                code.append(f'{prefix}System.out.println("{text_cleaned}");')
            elif val:
                code.append(f'{prefix}System.out.println({val});')
            else:
                code.append(f'{prefix}System.out.println();')
        elif n["op"] == "if":
            code.append(f'{prefix}if ({n["condition"]}) {{')
            body = generate_java_recursive(n.get("body", []), indent + 1)
            if body: code.append(body)
            code.append(f'{prefix}}}')
        elif n["op"] == "loop":
            code.append(f'{prefix}while({n.get("condition", "true")}) {{')
            body = generate_java_recursive(n.get("body", []), indent + 1)
            if body: code.append(body)
            code.append(f'{prefix}}}')
        elif n["op"] == "call":
            code.append(f'{prefix}{n["func"]}({n["args"]});')
        elif n["op"] == "break":
            code.append(f'{prefix}break;')
        elif n["op"] == "return":
            code.append(f'{prefix}return {n["value"]};')
    return "\n".join(code)

def generate_java(ir):
    code = ['public class Main {']
    has_func = any(n["op"] == "function" for n in ir)
    if has_func:
        code.append(generate_java_recursive(ir, 1))
    else:
        code.append('    public static void main(String[] args) {')
        code.append(generate_java_recursive(ir, 2))
        code.append('    }')
    code.append('}')
    return "\n".join(code)
