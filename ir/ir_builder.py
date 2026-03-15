def build_ir(nodes, src):
    ir = []
    for n in nodes:
        if n["type"] == "function":
            ir.append({
                "op": "function", "name": n["name"], "args": n["args"],
                "body": build_ir(n.get("body", []), src)
            })
        elif n["type"] == "assign":
            ir.append({"op": "assign", "target": n["var"], "value": n["value"]})
        elif n["type"] == "print":
            ir.append({"op": "print", "text": n.get("text", ""), "value": n.get("value")})
        elif n["type"] == "if":
            cond = n["condition"].replace('!', 'not ') if n.get("condition") else "True"
            ir.append({
                "op": "if", "condition": cond,
                "body": build_ir(n.get("body", []), src)
            })
        elif n["type"] == "loop":
            ir.append({
                "op": "loop", "loop_type": n.get("loop_type", "for"), "condition": n.get("condition"),
                "body": build_ir(n.get("body", []), src)
            })
        elif n["type"] == "call":
            ir.append({"op": "call", "func": n["func"], "args": n["args"]})
        elif n["type"] == "break":
            ir.append({"op": "break"})
        elif n["type"] == "return":
            ir.append({"op": "return", "value": n["value"]})
    return ir
