from graphviz import Digraph
import os
import platform
import subprocess

def visualize_ast(root_node, output_path='ast_output'):
    if root_node is None:
        print("⚠️ No AST to visualize (root_node is None). Skipping visualization.")
        return

    dot = Digraph(comment='AST', format='png')

    def add_nodes_edges(node, parent_id=None):
        node_id = str(id(node))
        label = f"{node.nodetype}"
        if node.value is not None:
            label += f"\n[{node.value}]"
        dot.node(node_id, label, shape='box', style='filled', color='lightblue')
        if parent_id:
            dot.edge(parent_id, node_id)
        for child in node.children:
            add_nodes_edges(child, node_id)

    # 🌳 Build the graph
    add_nodes_edges(root_node)

    # 🖼️ Render as PNG and save
    full_path = os.path.abspath(dot.render(filename=output_path, format='png', cleanup=True))
    print(f"🖼️ AST graph generated and saved to: {full_path}")

    # 📂 Auto-open the image
    try:
        if platform.system() == 'Windows':
            os.startfile(full_path)
        elif platform.system() == 'Darwin':  # macOS
            subprocess.run(['open', full_path])
        else:  # Linux
            subprocess.run(['xdg-open', full_path])
    except Exception as e:
        print(f"⚠️ Failed to auto-open the AST image: {e}")

def print_ast_tree(node, indent=""):
    if node is None:
        print("⚠️ No AST tree to print (node is None).")
        return
    label = f"{node.nodetype}({node.value})" if node.value is not None else node.nodetype
    print(indent + label)
    for child in node.children:
        print_ast_tree(child, indent + "  ")
