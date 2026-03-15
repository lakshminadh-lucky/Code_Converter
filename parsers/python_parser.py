
import ast

def parse_python(code):
    tree=ast.parse(code)
    nodes=[]

    for node in ast.walk(tree):

        if isinstance(node,ast.Assign):
            if hasattr(node.targets[0],"id"):
                nodes.append({
                    "type":"assign",
                    "var":node.targets[0].id,
                    "value":ast.unparse(node.value)
                })

        elif isinstance(node,ast.Call):
            if hasattr(node.func,"id") and node.func.id=="print":
                nodes.append({
                    "type":"print",
                    "value":ast.unparse(node.args[0])
                })

        elif isinstance(node,ast.If):
            nodes.append({
                "type":"if",
                "condition":ast.unparse(node.test)
            })

        elif isinstance(node,ast.For):
            nodes.append({
                "type":"loop",
                "loop_type":"for"
            })

    return nodes
