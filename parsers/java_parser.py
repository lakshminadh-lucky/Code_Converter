
import re
def parse_java(code):
    nodes=[]
    for line in code.splitlines():
        line=line.strip()

        m=re.match(r'(int|double|float|String) (\w+) = (.+);',line)
        if m:
            nodes.append({"type":"assign","var":m.group(2),"value":m.group(3)})
            continue

        m=re.match(r'System\.out\.println\((.+)\);',line)
        if m:
            nodes.append({"type":"print","value":m.group(1)})
            continue

        if line.startswith("if"):
            cond=line[line.find("(")+1:line.rfind(")")]
            nodes.append({"type":"if","condition":cond})

        if line.startswith("for"):
            nodes.append({"type":"loop","loop_type":"for"})
    return nodes
