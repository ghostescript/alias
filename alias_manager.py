import os
import subprocess
import sys
import re
import platform # Added for OS detection
from prompt_toolkit import prompt
from prompt_toolkit.completion import WordCompleter
from prompt_toolkit.history import InMemoryHistory
from prompt_toolkit.key_binding import KeyBindings
from prompt_toolkit.keys import Keys

def get_current_aliases():
    """Reads ~/.bash_aliases and returns a list of alias/function names."""
    alias_file_path = os.path.expanduser("~/.bash_aliases")
    aliases = []
    if os.path.exists(alias_file_path):
        with open(alias_file_path, "r") as f:
            for line in f:
                stripped_line = line.strip()
                alias_match = re.match(r"^\s*alias\s+([a-zA-Z0-9_]+)=", stripped_line)
                function_match = re.match(r"^\s*([a-zA-Z0-9_]+)\s*\(\)\s*\{", stripped_line)
                if alias_match:
                    aliases.append(alias_match.group(1))
                elif function_match:
                    aliases.append(function_match.group(1))
    return sorted(list(set(aliases)))

alias_completer = WordCompleter(get_current_aliases(), ignore_case=True)
history = InMemoryHistory()

kb = KeyBindings()

@kb.add(Keys.ControlZ)
def _(event):
    "Pressing Ctrl-Z will exit the tool."
    sys.exit(0)

def create_and_activate_alias():
    """
    Prompts the user for a command and an alias name, then saves and activates the alias.
    """
    try:
        print() # Blank line before prompt
        while True:
            command = prompt("Enter the command you want to alias: ", history=history, key_bindings=kb)
            if command.strip():
                break
            print("Input cannot be empty. Please try again...")
        print() # Blank line before prompt
        while True:
            alias_name = prompt("Enter the alias name: ", history=history, key_bindings=kb)
            if alias_name.strip():
                break
            print("Input cannot be empty. Please try again...")

        # Define the function string
        function_definition = f"""
{alias_name}() {{
  {command}
}}"""

        # Path to the alias file (can be customized)
        alias_file_path = os.path.expanduser("~/.bash_aliases")
        if platform.system() == "Linux" and os.path.exists("/data/data/com.termux"):
            alias_file_path = "/data/data/com.termux/files/home/.bash_aliases"

        # Ensure the alias file exists
        if not os.path.exists(alias_file_path):
            open(alias_file_path, 'a').close() # Create the file if it doesn't exist

        # Add the function to the file
        with open(alias_file_path, "a") as f:
            f.write(f"\n{function_definition}\n")
        print(f"Alias '{alias_name}' for command '{command}' saved to {alias_file_path}")

        print(f"\n--------------------------------------------------------------------")
        print() # Blank line after separator
        # Swapped order: Permanent message first
        print(f"\nTo make the alias permanent for future sessions, ensure that your ~/.bashrc and ~/.zshrc files source ~/.bash_aliases.")
        print(f"You can add the following lines to your ~/.bashrc and ~/.zshrc files if they are not already there:")
        print() # This will print a blank line
        print(f"if [ -f ~/.bash_aliases ]; then")
        print(f"    . ~/.bash_aliases")
        print(f"fi")
        print() # Blank line after the new message block

        # Then the "IMPORTANT" message
        print(f"\nIMPORTANT: To activate this alias in your *current* and *permanent* terminal sessions,")
        print(f"you MUST manually run the following command:")
        print() # This will print a blank line
        print(f"    source {alias_file_path}")
        print() # This will print a blank line
        print(f"--------------------------------------------------------------------")
        return True # Successful completion

    except KeyboardInterrupt:
        print() # Blank line before message
        return False # Interrupted

def manage_aliases():
    alias_file_path = os.path.expanduser("~/.bash_aliases")
    if platform.system() == "Linux" and os.path.exists("/data/data/com.termux"):
        alias_file_path = "/data/data/com.termux/files/home/.bash_aliases"

    try:
        if not os.path.exists(alias_file_path) or os.stat(alias_file_path).st_size == 0:
            print(f"\nNo aliases or functions found in {alias_file_path}.")
            return False # Return False to continue to main menu

        with open(alias_file_path, "r") as f:
            lines = f.readlines()

        # Initial alias listing
        print(f"\n--- Current Aliases/Commands in {alias_file_path} ---")
        display_count = 0 # New counter for displayed lines
        for i, line in enumerate(lines):
            stripped_line = line.strip()
            if stripped_line: # Only process non-empty lines
                display_count += 1

                alias_match = re.match(r"^\s*alias\s+([a-zA-Z0-9_]+)=", stripped_line)
                function_match = re.match(r"^\s*([a-zA-Z0-9_]+)\s*\(\)\s*\{", stripped_line)

                if alias_match:
                    print(f"{display_count}: {stripped_line}")
                elif function_match:
                    # The original formatting logic, now safely applied only to functions
                    name = function_match.group(1)
                    name_start_index = stripped_line.find(name)
                    name_end_index = name_start_index + len(name)

                    prefix = stripped_line[:name_start_index]
                    suffix = stripped_line[name_end_index:]

                    command_start_marker = "() {"
                    command_start_index_in_suffix = suffix.find(command_start_marker)

                    if command_start_index_in_suffix != -1:
                        function_declaration_part = suffix[:command_start_index_in_suffix + len(command_start_marker)]
                        command_part = suffix[command_start_index_in_suffix + len(command_start_marker):]

                        formatted_line = (
                            f"{display_count}: {prefix}"
                            f"{name}"
                            f"{function_declaration_part}"
                            f"{command_part}"
                        )
                    else:
                        formatted_line = (
                            f"{display_count}: {prefix}"
                            f"{name}"
                            f"{suffix}"
                        )
                    print(formatted_line)
                else:
                    # For other lines like comments or lines inside a function
                    print(f"{display_count}: {stripped_line}")
        print("----------------------------------------------------")
        try:
            print() # Blank line before prompt

            while True: # Loop for initial delete choice
                delete_choice = prompt("Delete an alias/command? [y/N]: ", history=history, completer=WordCompleter(['y', 'n'], ignore_case=True), key_bindings=kb)
                delete_choice_lower = delete_choice.lower()
                if delete_choice_lower == 'y':
                    break # Exit the loop to proceed with deletion
                elif delete_choice_lower == 'n' or not delete_choice.strip(): # Empty input or 'n' returns to main menu
                    return False # User wants to return to main menu
                else:
                    print("Invalid choice. Please input 'y', 'n', or press Enter to return to the main menu. Try again...")
                    continue # Continue the loop to re-prompt

            # Deletion loop
            while True: # Loop for deleting aliases until user says 'n'
                # Update completer and get latest lines in each iteration
                alias_completer.words = get_current_aliases()
                with open(alias_file_path, "r") as f:
                    lines = f.readlines()

                # If no lines left, exit deletion mode
                if not lines or not any(line.strip() for line in lines):
                    print(f"\nNo aliases or functions left in {alias_file_path}.")
                    return False # Go to main menu

                print() # Blank line before prompt
                name_input = prompt("Enter the name(s) of the alias to delete (comma-separated for multiple, or 'all' to delete everything): ", history=history, completer=alias_completer, key_bindings=kb)

                if not name_input.strip():
                    print("Input cannot be empty. Please try again...")
                    continue

                if name_input.strip().lower() == 'all':
                    names_to_delete = get_current_aliases()
                else:
                    names_to_delete = {name.strip() for name in name_input.split(',') if name.strip()}

                if not names_to_delete:
                    print("No names entered for deletion.")
                    continue

                # --- DELETION LOGIC ---
                to_delete_flags = [False] * len(lines)
                deleted_names = set()
                found_names = set()

                for i, line in enumerate(lines):
                    if to_delete_flags[i]:
                        continue

                    stripped_line = line.strip()

                    alias_match = re.match(r"^\s*alias\s+([a-zA-Z0-9_]+)=", stripped_line)
                    function_match = re.match(r"^\s*([a-zA-Z0-9_]+)\s*\(\)\s*\{", stripped_line)

                    name_on_line = None
                    if alias_match:
                        name_on_line = alias_match.group(1)
                    elif function_match:
                        name_on_line = function_match.group(1)

                    if name_on_line and name_on_line in names_to_delete:
                        found_names.add(name_on_line)
                        deleted_names.add(name_on_line)
                        to_delete_flags[i] = True
                        print(f"Marking for deletion: {stripped_line}")

                        if function_match:
                            # Mark all lines of the function for deletion
                            closing_brace_pattern = re.compile(r"^\s*\}\s*(#.*)?$")
                            for j in range(i + 1, len(lines)):
                                to_delete_flags[j] = True
                                if closing_brace_pattern.match(lines[j].strip()):
                                    break

                # --- END DELETION LOGIC ---

                not_found_names = set(names_to_delete) - found_names

                # If no valid aliases were found to delete, print not found message and re-prompt
                if not found_names:
                    if not_found_names:
                        print(f"\nThe following input was not found: {', '.join(not_found_names)}")
                    # This else handles cases like empty input that somehow passed the initial check
                    else:
                        print("No matching aliases/functions were found.")
                    continue

                # If we get here, at least one valid alias was found.
                # --- CONFIRMATION LOGIC ---
                confirm_delete = ''
                while True:
                    print() # blank line
                    # Format the list of names for the confirmation prompt
                    names_list = sorted(list(found_names)) # Use found_names for confirmation
                    if len(names_list) > 1:
                        names_to_confirm = ", ".join(names_list[:-1]) + " and " + names_list[-1]
                    else:
                        names_to_confirm = names_list[0] if names_list else ""
                    confirmation_prompt = f"Are you sure you want to delete {names_to_confirm}? [Y/n]: "

                    confirm_delete = prompt(confirmation_prompt, history=history, completer=WordCompleter(['y', 'n'], ignore_case=True), key_bindings=kb)
                    confirm_delete_lower = confirm_delete.lower()

                    if confirm_delete_lower in ['y', 'n', '']:
                        break
                    else:
                        print("Invalid choice. Please input 'y', 'n', or press Enter to confirm deletion. Try again...")

                if confirm_delete_lower == 'n':
                    print("Deletion cancelled.")
                    continue # Go back to the top of the deletion loop to ask for names again

                # --- ACTUAL DELETION ---
                new_lines = [line for i, line in enumerate(lines) if not to_delete_flags[i]]
                with open(alias_file_path, "w") as f:
                    f.writelines(new_lines)
                print(f"\nSuccessfully deleted: {', '.join(sorted(list(deleted_names)))}")

                # If some names were not found, report them now
                if not_found_names:
                    print(f"Note: The following input was not found: {', '.join(not_found_names)}")

                print(f"Please run source {alias_file_path} to apply changes to your current session.")
                print("\nNOTE: If you are running multiple shells (e.g., zsh and bash), you may need to run `source ~/.bash_aliases` in each shell to see updates. Alternatively, logging out and back in will apply the changes to all new terminal sessions.")
                # Ask to continue
                while True:
                    print()
                    another_delete = prompt(f"Delete another? [y/N]: ", history=history, completer=WordCompleter(['y', 'n'], ignore_case=True), key_bindings=kb)
                    another_delete_lower = another_delete.lower()
                    if another_delete_lower in ['y', 'n', '']:
                        break
                    else:
                        print(f"\nInvalid choice. Please input 'y', 'n', or press Enter to return to the main menu. Try again...")

                if another_delete_lower == 'y':
                    continue # Go to start of deletion loop
                else:
                    return False # Go to main menu

        except KeyboardInterrupt:
            print() # Blank line before message
            return False # Return False to indicate interruption
    except KeyboardInterrupt:
        print() # Blank line before message
        return False # Return False to indicate interruption
    return False # Return to the main menu after deletion loop finishes
if __name__ == "__main__":
    try:
        error_message = "" # Initialize error_message outside the loop
        at_main_menu_prompt = True # Flag to track if we are at the main menu prompt

        # Print banner and static menu once
        print()
        banner = '''         ###
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
'''
        print(f"{banner}")
        print(f"") # This prints a blank line after the banner
        print("           >>> alias v2.0 <<<") # Centered message
        print("< https://github.com/ghostescript/alias >") # Centered message
        print() # Blank line after menu header
        print() # Blank line after menu header

        while True:
            # Print menu options in each iteration
            print("\n--- alias v2.0 Menu ---")
            print() # Blank line after menu header
            print("[1] Create a new alias/command")
            print("[2] Aliases/commands (list/delete)")
            print("[3] Help message and Exit")
            print() # Blank line before prompt

            at_main_menu_prompt = True # We are at the main menu prompt
            menu_completer = WordCompleter(['1', '2', '3'], ignore_case=True)

            while True: # Inner loop for input validation
                prompt_to_display = "Enter your choice [1-3]: "
                choice = prompt(prompt_to_display, history=history, completer=menu_completer, key_bindings=kb)
                if choice.strip():
                    break
                print("Input cannot be empty. Please try again...")

            at_main_menu_prompt = False # No longer at the main menu prompt

            if choice == '1':
                if not create_and_activate_alias(): # Call it once immediately and check return
                    continue # Go back to main menu if Ctrl+C was pressed

                while True: # Loop for creating additional aliases
                    error_message = ""
                    should_continue_creating = True
                    while True: # Inner loop for input validation
                        prompt_text = f"\nCreate another alias/command? [y/N]: "
                        if error_message:
                            print(error_message) # Print error message from previous iteration
                            error_message = "" # Clear error message after printing
                        try:
                            another_create = prompt(prompt_text, history=history, completer=WordCompleter(['y', 'n'], ignore_case=True), key_bindings=kb)
                            another_create_lower = another_create.lower()
                        except KeyboardInterrupt:
                            print() # Blank line before message
                            print("\nOperation cancelled. Returning to main menu.")
                            should_continue_creating = False
                            break # Break inner loop, outer loop will then break

                        if another_create_lower == 'y':
                            error_message = ""
                            if not create_and_activate_alias(): # Call again for another alias and check return
                                should_continue_creating = False
                                break # Break inner loop, outer loop will then break
                            break # Break inner loop, continue outer loop
                        elif another_create_lower == 'n' or not another_create.strip(): # Empty input or 'n' returns to main menu
                            error_message = ""
                            should_continue_creating = False
                            break # Break inner loop, then outer loop
                        else:
                            error_message = "Invalid choice. Please input 'y', 'n', or press Enter to return to the main menu. Try again..."
                    if not should_continue_creating:
                        break # Break outer loop to return to main menu
            elif choice == '2':
                if manage_aliases(): # If manage_aliases returns True, exit the main loop
                    break
            elif choice == '3':
                print() # Blank line before message
                # Determine the correct bash_aliases path based on OS
                bash_aliases_path = os.path.expanduser("~/.bash_aliases")
                if platform.system() == "Linux" and os.path.exists("/data/data/com.termux"):
                    bash_aliases_path = "/data/data/com.termux/files/home/.bash_aliases"

                print(f"\nTo make the alias permanent for future sessions, ensure that your ~/.bashrc and ~/.zshrc files source ~/.bash_aliases.")
                print(f"You can add the following lines to your ~/.bashrc and ~/.zshrc files if they are not already there:")
                print() # This will print a blank line
                print(f"if [ -f {bash_aliases_path} ]; then")
                print(f"    . {bash_aliases_path}")
                print(f"fi")
                print() # Blank line after the new message block

                # Then the "IMPORTANT" message
                print(f"\nIMPORTANT: To activate this alias in your *current* and *permanent* terminal sessions,")
                print(f"you MUST manually run the following command:")
                print() # This will print a blank line
                print(f"    source {bash_aliases_path}")
                print() # This will print a blank line

                print() # Add another blank line for spacing
                print("NOTE: If you are running multiple shells (e.g., zsh and bash), you may need to run `source ~/.bash_aliases` in each shell to see updates. Alternatively, logging out and back in will apply the changes to all new terminal sessions.")
                print() # Add a blank line for spacing
                print() # Add another blank line for spacing

                print("Exiting alias v2.0 Menu")
                print() # Add final blank line
                sys.exit(0)
            else:
                print("Invalid choice. Please enter 1, 2, or 3.") # Print error message immediately
                error_message = "" # Clear error message for next iteration
                continue # Continue the main loop to re-prompt
    except KeyboardInterrupt:
        print() # Blank line before message
        if at_main_menu_prompt:
            print("\nExiting alias v2.0 Menu.")
            sys.exit(0)
        else:
            error_message = "\nOperation cancelled. Returning to main menu." # Set error message for next loop iteration
            # The outer while True loop will continue, effectively re-prompting the main menu
