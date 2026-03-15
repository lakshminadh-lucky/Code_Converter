from graphviz import Digraph

def flatten_ir_for_flowchart(ir):
    flat = []
    for n in ir:
        if n["op"] in ["function", "if", "loop"]:
            flat.append(n)
            flat.extend(flatten_ir_for_flowchart(n.get("body", [])))
        else:
            flat.append(n)
    return flat

def generate_flowchart(ir):
    dot = Digraph()
    dot.node("Start")
    prev = "Start"
    
    flat_ir = flatten_ir_for_flowchart(ir)
    for i, n in enumerate(flat_ir):
        cur = f"n{i}"
        label = n["op"]
        if n["op"] == "function":
            label = f'Func: {n.get("name")}'
        elif n["op"] == "assign":
            label = f'{n.get("target")} = {n.get("value")}'
        dot.node(cur, label)
        dot.edge(prev, cur)
        prev = cur
        
    dot.node("End")
    dot.edge(prev, "End")
    return dot
