import os
import ast

class CodeMetrics(ast.NodeVisitor):
    def __init__(self):
        self.num_classes = 0
        self.num_methods = 0

    def visit_ClassDef(self, node):
        self.num_classes += 1
        self.num_methods += sum(1 for n in node.body if isinstance(n, ast.FunctionDef))
        self.generic_visit(node)

def analyze_code(base_path):
    metrics = CodeMetrics()
    for root, _, files in os.walk(base_path):
        for file in files:
            if file.endswith(".py"):
                file_path = os.path.join(root, file)
                with open(file_path, "r", encoding="utf-8") as f:
                    try:
                        tree = ast.parse(f.read())
                        metrics.visit(tree)
                    except Exception as e:
                        print(f"Error analyzing {file_path}: {e}")
    return metrics

# Specify the path to your project folder
project_path = "C:/Users/judit/desktop/cs4400"
result = analyze_code(project_path)

print(f"Total Classes: {result.num_classes}")
print(f"Total Methods: {result.num_methods}")
