# alias (v2.0)
A command-line interface (CLI) tool written in Python for easy management of Bash aliases and commands. This tool simplifies the process of creating, listing, and deleting custom commands in your `~/.bash_aliases` file, enhancing your terminal workflow.

## Updates

**Upgrades:** Interactive Input with Autosuggestions and History: Enhanced user experience with `prompt_toolkit` for intelligent input suggestions, navigation, and command history. 

**New** package installation with pip.

## Table of Contents

*   [Features](#features)
*   [Installation](#installation)
    *   [From PyPI](#from-pypi)
    *   [From Git Repository](#from-git-repository)
    *   [Manual Installation (if not using Git)](#manual-installation-if-not-using-git)
*   [Usage](#usage)
    *   [1. Create a new alias](#1-create-a-new-alias)
    *   [2. Alias Manager](#2-alias-manager)
    *   [3. Help message and Exit](#3-help-message-and-exit)
*   [Keyboard Interrupt (Ctrl+C)](#keyboard-interrupt-ctrlc)
*   [Example Workflow](#example-workflow)
    *   [Bonus Example](#bonus-example)
*   [Contributing](#contributing)
*   [License](#license)
*   [Last Updated](#last-updated)
*   [Project Links](#project-links)
*   [Author's Github](#authors-github)

## Features

*   **Interactive Input with Autosuggestions and History:** Enhanced user experience with `prompt_toolkit` for intelligent input suggestions, navigation, and command history.
*   **Plain Text Output:** Clean, unformatted output without ANSI escape codes, ensuring compatibility across various terminal environments.
*   **Create Aliases/Commands:** Define new shortcuts for your frequently used commands.
*   **List Aliases/Commands:** View all currently defined aliases and commands from your `~/.bash_aliases` file.
*   **Delete Aliases/Commands:** Remove specific aliases/commands by name, or delete all of them.
*   **Interactive Menu:** User-friendly menu-driven interface.
*   **Error Handling:** Provides feedback for invalid inputs.
*   **Keyboard Interrupt (Ctrl+C) Handling:** Gracefully returns to the main menu on `Ctrl+C` instead of exiting the script.

## Installation

### From PyPI 

1.  **pip install [aliasman](https://pypi.org/project/aliasman/)**       
    ```bash
    python3 -m pip install aliasman
    ```
    
2.  **Execute Tool**
    ```bash
    aliasman
    ```

### From Git Repository

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/ghostescript/alias 
    cd alias
    ```

2.  **Create virtual environment** 
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```

3.  **Prerequisites**
    ```bash
    python3 -m pip install -r requirements.txt
    ```

4.  **Make the script executable:**
    ```bash
    chmod +x alias_manager.py
    ```

5.  **Run the script:**
    You can now run the script directly from the `alias` directory:

    ```bash
    python3 alias_manager.py
    ```
    Or, if you add the `alias` directory to your system's PATH, you can run it from anywhere:
    ```bash
    alias_manager.py
    ```

### Manual Installation (if not using Git)

1.  **Save the script:**
    Download the `alias_manager.py` file and save it to a convenient location on your system, for example, in your home directory or a `bin` directory within your home directory.

    ```bash
    # Example: Save to your home directory
    mv alias_manager.py ~/alias_manager.py
    ```

2.  **Make it executable:**
    Give execute permissions to the script:

    ```bash
    chmod +x ~/alias_manager.py
    ```

3.  **Run the script:**
    You can now run the script directly:

    ```bash
    python3 ~/alias_manager.py
    ```
    Or, if you added it to your PATH, just:
    ```bash
    alias_manager.py
    ```

## Usage

When you run the script, you will be presented with the main menu:

```
         ###
          ###    #
           ##   ###
           ##    #
           ##
   /###    ##  ###       /###      /###
  / ###  / ##   ###     / ###  /  / #### /
 /   ###/  ##    ##    /   ###/  ##  ###/
##    ##   ##    ##   ##    ##  ####
##    ##   ##    ##   ##    ##    ###
##    ##   ##    ##   ##    ##      ###
##    ##   ##    ##   ##    ##        ###
##    /#   ##    ##   ##    /#   /###  ##
 ####/ ##  ### / ### / ####/ ## / #### /
  ###   ##  ##/   ##/   ###   ##   ###/

          >>> alias v2.0 <<<
< https://github.com/ghostescript/alias >

--- alias v2.0 Menu ---

[1] Create a new alias/command
[2] Aliases/commands (list/delete)
[3] Help message and Exit

Enter your choice (1-3):
```

### 1. Create a new alias

1.  Select option `1` from the main menu.
2.  You will be prompted to "Enter the command you want to alias:". Type your command (e.g., `ls -la`) and press Enter.
3.  You will then be prompted to "Enter the alias name:". Type the desired name for your alias (e.g., `ll`) and press Enter.
4.  The script will confirm that the alias has been saved to `~/.bash_aliases`.
5.  You will then be asked "Create another alias/command? [y/N]:".
    *   Type `y` and press Enter to create another alias/function.
    *   Type `n` or just press Enter to return to the main menu.
    *   If you enter an invalid choice, an error message will be displayed, and you'll be prompted again.
6.  **Important:** For the new alias/command to be active in your *current* terminal session, you **MUST** run:
    ```bash
    source ~/.bash_aliases
    ```
7.  To make the alias permanent for future sessions, ensure that your `~/.bashrc` and `~/.zshrc` files source `~/.bash_aliases`. You can add the following lines to your `~/.bashrc` and `~/.zshrc` files if they are not already there:
    ```bash
    if [ -f ~/.bash_aliases ]; then
        . ~/.bash_aliases
    fi
    ```

### 2. Alias Manager

1.  Select option `2` from the main menu.
2.  The script will display a numbered list of all aliases and commands found in your `~/.bash_aliases` file.
3.  You will then be asked "Do you want to delete an alias/command? [y/N]:".
    *   Type `y` and press Enter to proceed with deletion.
    *   Type `n` or just press Enter to return to the main menu.
    *   If you enter an invalid choice, an error message will be displayed, and you'll be prompted again.
4.  If you chose to delete, you will be prompted: "Enter the name(s) of the alias to delete (comma-separated for multiple, or 'all' to delete everything):".
    *   Enter the exact name(s) of the alias/commands you wish to delete, separated by commas.
    *   Type `all` to delete all aliases and commands.
    *   If you enter names that are not found, the script will inform you.
5.  After deletion, you will be asked "Delete another? [y/N]:".
    *   Type `y` and press Enter to delete more.
    *   Type `n` or just press Enter to return to the main menu.
    *   If you enter an invalid choice, an error message will be displayed, and you'll be prompted again.
6.  **Important:** After deleting aliases/commands, you **MUST** run `source ~/.bash_aliases` in your current terminal session for the changes to take effect.

### 3. Help message and Exit 

1.  Select option `3` from the main menu to exit the Alias Manager.
2.  The script will remind you of the steps to make aliases permanent and activate them in your current session.

### Keyboard Interrupt (Ctrl+C)

*   At any prompt where you are asked for input (e.g., "Enter the command you want to alias:", "Create another alias/function? [y/N]:", "Enter your choice (1-3):"), pressing `Ctrl+C` will gracefully cancel the current operation and return you to the main "--- alias v2.0 Menu ---".

## Example Workflow

1.  Run `python3 alias_manager.py` (assuming you are in the `alias` directory or it's in your PATH)
2.  Select `1` to create a new alias.
3.  Enter `echo "Hello World"` for the command.
4.  Enter `hello` for the alias name.
5.  When asked "Create another alias/function? [y/N]:", press Enter (or type `n`).
6.  You are back at the main menu.
7.  Run `source ~/.bash_aliases` in your terminal.
8.  Now you can type `hello` in your terminal, and it will output "Hello World".
9.  Run `python3 alias_manager.py` again.
10. Select `2` to list/delete aliases.
11. You will see `hello` listed.
12. When asked "Do you want to delete an alias/function? [y/N]:", type `y`.
13. Enter `hello` to delete it.
14. When asked "Delete another? [y/N]:", press Enter (or type `n`).
15. You are back at the main menu.
16. Select `3` to exit.
17. Run `source ~/.bash_aliases` again.
18. Now, typing `hello` will result in a "command not found" error, as it has been deleted.

## Bonus Example 

Display all packages by size in nano. 

**Command:**
```bash
dpkg-query -W -f='${Installed-Size}\t${Package}\n' | sort -nr | awk '{print $1/1024 " MB\t" $2}' > package_sizes.txt ; nano package_sizes.txt # command/function to view package sizes in nano
```
**Alias Name:**
```bash
pac
```

## Contributing

Contributions are welcome! If you have suggestions for improvements, bug fixes, or new features, please open an issue or submit a pull request on the GitHub repository.

## License

This project is open-source and available under the [MIT License](LICENSE).

<br>

## Last Updated 
``Dec 2, 2025``

### Project Links 
[alias v2.0](https://github.com/ghostescript/alias)

[aliasman 0.2.0](https://pypi.org/project/aliasman/)

### Author's Github
[ghostescript](https://github.com/ghostescript)

[ghoste9624](https://github.com/ghoste9624)


<br>
