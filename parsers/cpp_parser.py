
import re
def parse_cpp(code):
    nodes=[]
    for line in code.splitlines():
        line=line.strip()

        m=re.match(r'int (\w+) = (.+);',line)
        if m:
            nodes.append({"type":"assign","var":m.group(1),"value":m.group(2)})
            continue

        m=re.match(r'cout << (.+) << endl;',line)
        if m:
            nodes.append({"type":"print","value":m.group(1)})

        if line.startswith("if"):
            cond=line[line.find("(")+1:line.rfind(")")]
            nodes.append({"type":"if","condition":cond})

        if line.startswith("for"):
            nodes.append({"type":"loop","loop_type":"for"})
    return nodes
