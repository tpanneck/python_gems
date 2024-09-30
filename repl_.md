# Introduction

The Python script under discussion serves as a versatile tool for
managing jobs and users through both direct command-line inputs and an
interactive REPL environment. Utilizing Python's built-in modules,
namely `sys` and `readline`, the script offers features such as
hierarchical command structures, autocompletion, and a help system to
enhance user experience.

# Features

-   **REPL Mode**: An interactive shell allowing users to input commands
    and options continuously until they choose to exit.

-   **Command-Line Mode**: Enables users to execute commands directly
    from the terminal without entering the REPL.

-   **Autocompletion**: Facilitates command and subcommand suggestions
    as users type, enhancing efficiency.

-   **Help Functionality**: Provides detailed information about
    available commands and their respective options using the `–help`
    flag.

# Command Definitions

At the core of the script lies a nested dictionary structure that
delineates the available commands, subcommands, and their corresponding
functions.

``` {.python language="Python" caption="Command Definitions"}
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
```

-   **Groups**: Represented by keys such as `jobs` and `users`, these
    contain subcommands or other groups.

-   **Commands**: Defined under groups (e.g., `list`, `start`, `add`),
    these are executable actions tied to specific functions.

-   **Options**: Certain commands (like `start`) have associated options
    (e.g., `–nice`, `–max-mem`) that modify their behavior.

# Command Parsing

The function `execute_command()` is pivotal for interpreting user inputs
and executing the appropriate commands based on the parsed tokens.

``` {.python language="Python" caption="Command Parsing"}
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
            # Option handling
            key_value = token.lstrip('-').split('=', 1)
            if len(key_value) == 2:
                options[key_value[0]] = key_value[1]
            else:
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
                current_node = {}
        else:
            print(f"Unknown command or option '{token}'.")
            return
        i += 1
    if command_function:
        # Filter and pass options to the command function
        filtered_options = {k.replace('-', '_'): v for k, v in options.items()}
        try:
            command_function(**filtered_options)
        except TypeError as e:
            print(f"Error executing command: {e}")
    else:
        print("No executable command provided.")
```

-   \*\*Tokenization\*\*: User input is split into tokens (e.g.,
    `jobs start –nice=5` becomes `[’jobs’, ’start’, ’–nice=5’]`).

-   \*\*Traversal\*\*: The function navigates through the `commands`
    dictionary based on the tokens to locate the relevant command.

-   \*\*Option Handling\*\*: Options are parsed and stored as key-value
    pairs, which are then passed as keyword arguments to the associated
    command function.

-   \*\*Error Handling\*\*: The function gracefully handles unknown
    commands or options by informing the user.

# Command-Line Mode

When commands are provided as arguments during script execution, the
script processes them directly without entering the REPL.

``` {.python language="Python" caption="Command-Line Mode"}
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
```

-   \*\*Argument Check\*\*: The script checks if any command-line
    arguments are provided.

-   \*\*Execution\*\*: If arguments are present, they are parsed and
    executed using `execute_command()`. If not, the script initiates the
    REPL.

# REPL Mode

The REPL (Read-Eval-Print Loop) offers an interactive environment where
users can input commands and receive immediate feedback.

``` {.python language="Python" caption="REPL Mode"}
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
```

-   \*\*Looping\*\*: The REPL continuously prompts the user for input
    until the user types `exit` or sends an EOF signal.

-   \*\*Command Execution\*\*: User inputs are tokenized and passed to
    `execute_command()` for processing.

-   \*\*Graceful Exit\*\*: The loop can be exited gracefully by typing
    `exit` or pressing `Ctrl+D`.

# Autocompletion

Autocompletion enhances user experience by providing command and
subcommand suggestions as users type, leveraging Python's `readline`
module.

``` {.python language="Python" caption="Autocompletion"}
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
```

-   \*\*Functionality\*\*: The `completer()` function suggests possible
    commands or subcommands based on the current input context.

-   \*\*Integration\*\*: `readline.set_completer(completer)` sets the
    completer function, and `readline.parse_and_bind(’tab: complete’)`
    binds the Tab key to trigger autocompletion.

-   \*\*Context Awareness\*\*: The completer navigates through the
    `commands` hierarchy to provide relevant suggestions.

# Help System

The built-in help system offers users guidance on available commands and
their respective options.

``` {.python language="Python" caption="Help System"}
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
```

-   \*\*Invocation\*\*: Users can trigger the help system by appending
    `–help` to their command (e.g., `jobs start –help`).

-   \*\*Output\*\*: Depending on the context, the help system displays
    available commands or details about specific command options.

-   \*\*User Guidance\*\*: Provides clear instructions and available
    options, enhancing usability.

# Usage Examples

## Executing Commands Directly from the Shell

``` {.Shell language="Shell" caption="Command-Line Execution"}
$ python script.py jobs list
Listing jobs...

$ python script.py jobs start --nice=5 --max-mem=128k
Starting job with nice=5 and max_mem=128k

$ python script.py users add
Adding user...
```

## Starting the REPL

``` {.Shell language="Shell" caption="REPL Mode"}
$ python script.py
>> jobs list
Listing jobs...
>> jobs start --nice=5 --max-mem=128k
Starting job with nice=5 and max_mem=128k
>> exit
```

## Getting Help

``` {.Shell language="Shell" caption="Help Commands"}
$ python script.py --help
Available commands:
  jobs
  users

$ python script.py jobs --help
Available commands under 'jobs':
  list
  start
  stop

$ python script.py jobs start --help
Help for command 'jobs start':
Options:
  --nice
  --max-mem
```

# Conclusion

This Python script exemplifies a straightforward yet effective approach
to building a command-line interface with an integrated REPL. By
leveraging Python's inherent modules, it supports hierarchical commands,
autocompletion, and a robust help system without the need for external
dependencies. This design ensures ease of maintenance, scalability, and
a user-friendly experience.
