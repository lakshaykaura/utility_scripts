import javalang


def parse_java_code(file_contents):
    tree = javalang.parse.parse(file_contents)
    call_hierarchy = {}

    def get_full_method_name(node):
        param_types = [param.type.name for param in node.parameters]
        return f"{node.name}({', '.join(param_types)})"

    def handle_node(node, parent_method_full_name):
        print(f"Processing node: {type(node)} in method: {parent_method_full_name}")
        if isinstance(node, javalang.tree.MethodInvocation):
            method_call = node.member
            call_signature = (
                f"{method_call}({', '.join([str(arg) for arg in node.arguments])})"
            )
            if node.qualifier:
                call_signature = f"{node.qualifier}.{call_signature}"
            call_hierarchy.setdefault(parent_method_full_name, set()).add(
                call_signature
            )
        elif hasattr(node, "children"):
            for child in node.children:
                if isinstance(child, (javalang.tree.Node, list, tuple)):
                    handle_node(child, parent_method_full_name)

    for _, node in tree.filter(javalang.tree.MethodDeclaration):
        print(f"Processing MethodDeclaration: {node.name}")
        method_full_name = get_full_method_name(node)
        handle_node(node, method_full_name)

    return call_hierarchy


def detect_and_print_cycles(call_hierarchy):
    visited = set()
    path = []

    def is_cyclic(method):
        if method not in visited:
            visited.add(method)
            path.append(method)

            for callee in call_hierarchy.get(method, []):
                if callee not in visited:
                    if is_cyclic(callee):
                        return True
                elif callee in path:
                    cycle_start_index = path.index(callee)
                    print_cycle(path[cycle_start_index:])
                    return True

            path.pop()
        return False

    def print_cycle(cycle_path):
        cycle_str = " --> ".join(cycle_path)
        print(f"Cycle Detected: {cycle_str}")

    for method in call_hierarchy:
        if method not in visited:
            is_cyclic(method)
