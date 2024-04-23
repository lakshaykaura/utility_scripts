import javalang


def parse_java_code(file_contents):
    """
    Parses Java code and builds a call hierarchy of methods.

    Args:
        file_contents (str): The Java code to parse.

    Returns:
        dict: A dictionary representing the call hierarchy. Each key is a method name, and the value is a set of methods
              that the key method calls.

    This function uses the javalang library to parse the Java code. It then walks the abstract syntax tree (AST) of the
    code, looking for method declarations and invocations. For each method declaration, it records the method's name and
    parameters. For each method invocation, it records the method being called and its arguments. It then adds the
    invocation to the call hierarchy under the method that made the call.
    """
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
    """
    Detects and prints cycles in a call hierarchy of methods.

    Args:
        call_hierarchy (dict): A dictionary representing the call hierarchy. Each key is a method name, and the value is a set of methods
                               that the key method calls.

    This function uses depth-first search to traverse the call hierarchy. It maintains a set of visited methods and a list representing
    the current path from the root of the search to the current method. If it encounters a method that has not been visited, it adds the
    method to the visited set and the path list, and then recursively searches the methods that the current method calls. If it encounters
    a method that is in the path list (indicating a cycle), it prints the cycle and returns True. If it finishes searching all of a method's
    callees without finding a cycle, it removes the method from the path list and returns False. The function starts the search from each
    method in the call hierarchy that has not been visited.
    """
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
