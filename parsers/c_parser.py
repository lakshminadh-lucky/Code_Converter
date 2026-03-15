import re

def parse_c(code):
    nodes = []
    stack = [nodes]
    
    for line in code.splitlines():
        line = line.strip()
        if not line or line.startswith("//") or line.startswith("#"):
            continue
            
        current_block = stack[-1]
        
        m = re.match(r'(?:int|void|float|double|bool)\s+(\w+)\s*\((.*?)\)\s*\{', line)
        if m:
            func_node = {"type": "function", "name": m.group(1), "args": m.group(2), "body": []}
            current_block.append(func_node)
            stack.append(func_node["body"])
            continue
            
        m = re.match(r'for\s*\((.*?)\)\s*\{', line)
        if m:
            loop_node = {"type": "loop", "loop_type": "for", "condition": m.group(1), "body": []}
            current_block.append(loop_node)
            stack.append(loop_node["body"])
            continue
            
        m = re.match(r'if\s*\((.*?)\)\s*\{', line)
        if m:
            if_node = {"type": "if", "condition": m.group(1), "body": []}
            current_block.append(if_node)
            stack.append(if_node["body"])
            continue
            
        m = re.match(r'(?:int|float|double|bool|short|long|char)?\s*\*?(\w+)(?:\[.*?\])?\s*=\s*(.+);', line)
        if m:
            val = m.group(2)
            if val.startswith('{'):
                val = '[' + val[1:-1] + ']'
            val = val.replace('sizeof(arr) / sizeof(arr[0])', 'len(arr)')
            val = re.sub(r'\*(?=\w)', '', val)
            val = val.replace('false', 'False').replace('true', 'True')
            var = m.group(1).replace('*', '')
            current_block.append({"type": "assign", "var": var, "value": val})
            continue

        m = re.match(r'\*?(\w+)\s*=\s*(.+);', line)
        if m:
            val = m.group(2)
            val = re.sub(r'\*(?=\w)', '', val)
            val = val.replace('false', 'False').replace('true', 'True')
            var = m.group(1)
            current_block.append({"type": "assign", "var": var, "value": val})
            continue
            
        m = re.match(r'printf\(\s*"(.*?)"\s*(?:,\s*(.+))?\);', line)
        if m:
            val = m.group(2)
            current_block.append({"type": "print", "text": m.group(1), "value": val})
            continue
            
        m = re.match(r'(\w+)\s*\((.*?)\);', line)
        if m and m.group(1) != "printf":
            current_block.append({"type": "call", "func": m.group(1), "args": m.group(2).replace('&', '')})
            continue
            
        if line == "break;":
            current_block.append({"type": "break"})
            continue
            
        m = re.match(r'return\s+(.*?);', line)
        if m:
            current_block.append({"type": "return", "value": m.group(1)})
            continue
            
        if line == "}":
            if len(stack) > 1:
                stack.pop()
            continue

    return nodes
