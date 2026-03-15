def explain_ir_step_by_step(ir, level=0):
    steps = []
    prefix = ""
    for n in ir:
        if n["op"] == "function":
            steps.append(f'{prefix}Define function {n["name"]}')
            steps.extend(explain_ir_step_by_step(n.get("body", []), level + 1))
        elif n["op"] == "assign":
            steps.append(f'{prefix}Assign value {n["value"]} to variable {n["target"]}')
        elif n["op"] == "print":
            steps.append(f'{prefix}Print the value {n.get("value", "")}')
        elif n["op"] == "if":
            steps.append(f'{prefix}Check condition {n["condition"]}')
            steps.extend(explain_ir_step_by_step(n.get("body", []), level + 1))
        elif n["op"] == "loop":
            steps.append(f'{prefix}Execute loop multiple times while {n.get("condition", "True")}')
            steps.extend(explain_ir_step_by_step(n.get("body", []), level + 1))
        elif n["op"] == "call":
            steps.append(f'{prefix}Call function {n["func"]}')
        elif n["op"] == "break":
            steps.append(f'{prefix}Break out of loop')
        elif n["op"] == "return":
            steps.append(f'{prefix}Return value {n["value"]}')
    return steps
