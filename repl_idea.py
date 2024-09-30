import sys
import readline

# Example functions for the commands
def list_jobs_function():
    print("Listing jobs...")

def start_job_function(nice=0, max_mem='64k'):
    print(f"Starting job with nice={nice} and max_mem={max_mem}")

def stop_job_function():
    print("Stopping job...")

def add_user_function():
    print("Adding user...")

def remove_user_function():
    print("Removing user...")

def list_users_function():
    print("Listing users...")

# Definition of commands and their hierarchy
commands = {
    'jobs': {
        '_type': 'group',
        'children': {
            'list': {
                '_type': 'command',
                'function': list_jobs_function,
            },
            'start': {
                '_type': 'command',
                'function': start_job_function,
                'options': ['nice', 'max-mem'],
            },
            'stop': {
                '_type': 'command',
                'function': stop_job_function,
            },
        }
    },
    'users': {
        '_type': 'group',
        'children': {
            'add': {
                '_type': 'command',
                'function': add_user_function,
            },
            'remove': {
                '_type': 'command',
                'function': remove_user_function,
            },
            'list': {
                '_type': 'command',
                'function': list_users_function,
            },
        }
    }
}

def completer(text, state):
    # Get the entire input buffer
    line = readline.get_line_buffer()
    # Split the input into tokens
    tokens = line.strip().split()
    # If the cursor is at the end with a space, append an empty token
    if line.endswith(' '):
        tokens.append('')
    # Initialize options
    options = []
    # Start at the root of the command tree
    current_node = commands
    # Traverse the tokens to find the current node
    for i, token in enumerate(tokens[:-1]):
        if token in current_node:
            node = current_node[token]
            if node['_type'] == 'group':
                current_node = node.get('children', {})
            elif node['_type'] == 'command':
                # Command reached, no further subcommands
                current_node = {}
                break
        else:
            current_node = {}
            break
    # The current token is the last in tokens
    if tokens:
        current_token = tokens[-1]
    else:
        current_token = ''
    if current_node:
        # We are in a group node or at the beginning
        matches = [cmd for cmd in current_node.keys() if cmd.startswith(current_token)]
        options.extend(matches)
    else:
        # No more options available
        options = []
    # Sort options for consistent order
    options.sort()
    # Return the option based on the state
    if state < len(options):
        return options[state]
    else:
        return None

readline.set_completer(completer)
readline.parse_and_bind('tab: complete')

def execute_command(tokens):
    current_node = commands
    options = {}
    command_function = None
    i = 0
    while i < len(tokens):
        token = tokens[i]
        if token == '--help':
            show_help(tokens[:i])
            return
        elif token.startswith('--'):
            # Option
            key_value = token.lstrip('-').split('=', 1)
            if len(key_value) == 2:
                options[key_value[0]] = key_value[1]
            else:
                # If no value is given, check the next token
                if i + 1 < len(tokens) and not tokens[i + 1].startswith('--'):
                    options[key_value[0]] = tokens[i + 1]
                    i += 1
                else:
                    options[key_value[0]] = True
        elif token in current_node:
            node = current_node[token]
            if node['_type'] == 'group':
                current_node = node.get('children', {})
            elif node['_type'] == 'command':
                command_function = node.get('function')
                expected_options = node.get('options', [])
                # Collect options
                current_node = {}
            else:
                print(f"Unknown node type for '{token}'.")
                return
        else:
            print(f"Unknown command or option '{token}'.")
            return
        i += 1
    if command_function:
        # Filter options to pass only expected ones
        filtered_options = {k.replace('-', '_'): v for k, v in options.items()}
        try:
            command_function(**filtered_options)
        except TypeError as e:
            print(f"Error executing command: {e}")
    else:
        print("No executable command provided.")

def show_help(tokens=None):
    if tokens is None:
        tokens = []
    current_node = commands
    for token in tokens:
        if token in current_node:
            node = current_node[token]
            if node['_type'] == 'group':
                current_node = node.get('children', {})
            elif node['_type'] == 'command':
                print(f"Help for command '{' '.join(tokens)}':")
                if 'options' in node:
                    print("Options:")
                    for opt in node['options']:
                        print(f"  --{opt}")
                else:
                    print("No options available.")
                return
        else:
            print(f"Unknown command '{' '.join(tokens)}'.")
            return
    # If we are here, we are in a group node
    if tokens:
        print(f"Available commands under '{' '.join(tokens)}':")
    else:
        print("Available commands:")
    for cmd in current_node.keys():
        print(f"  {cmd}")

def run_repl():
    while True:
        try:
            user_input = input('>> ').strip()
            if user_input == 'exit':
                break
            elif not user_input:
                continue
            tokens = user_input.split()
            execute_command(tokens)
        except EOFError:
            break

def main():
    if len(sys.argv) > 1:
        # Commands were provided as arguments
        tokens = sys.argv[1:]
        if '--help' in tokens or '-h' in tokens:
            show_help(tokens[:-1])  # Remove '--help' or '-h'
        else:
            execute_command(tokens)
    else:
        # No arguments provided, start the REPL
        run_repl()

if __name__ == '__main__':
    main()
