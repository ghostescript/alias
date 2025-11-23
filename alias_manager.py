import os
import subprocess
import sys
import re

# ANSI escape codes for colors and styles
COLOR_RESET = "\033[0m"
COLOR_BOLD = "\033[1m"
COLOR_WHITE = "\033[97m"
COLOR_CYAN = "\033[96m"
COLOR_YELLOW = "\033[93m"
COLOR_GREEN = "\033[92m"

def create_and_activate_alias():
    """
    Prompts the user for a command and an alias name, then saves and activates the alias.
    """
    try:
        print() # Blank line before prompt
        command = input("\033[1m\033[92mEnter the command you want to alias: \033[0m")
        print() # Blank line before prompt
        alias_name = input("\033[1m\033[92mEnter the alias name: \033[0m")

        # Define the function string
        function_definition = f"""
{alias_name}() {{
  {command}
}} """

        # Path to the alias file (can be customized)
        alias_file_path = os.path.expanduser("~/.bash_aliases")

        # Ensure the alias file exists
        if not os.path.exists(alias_file_path):
            open(alias_file_path, 'a').close() # Create the file if it doesn't exist

        # Add the function to the file
        with open(alias_file_path, "a") as f:
            f.write(f"\n{function_definition}\n")
        print(f"{COLOR_BOLD}{COLOR_GREEN}Function '{COLOR_CYAN}{alias_name}{COLOR_GREEN}' for command '{COLOR_WHITE}{command}{COLOR_GREEN}' saved to {COLOR_CYAN}{alias_file_path}{COLOR_GREEN}{COLOR_RESET}")

        print(f"\n{COLOR_BOLD}{COLOR_WHITE}--------------------------------------------------------------------{COLOR_RESET}")
        print() # Blank line after separator
        # Swapped order: Permanent message first
        print(f"\n{COLOR_BOLD}{COLOR_WHITE}To make the alias permanent for future sessions, ensure that your ~/.bashrc and ~/.zshrc files source ~/.bash_aliases.{COLOR_RESET}")
        print(f"{COLOR_BOLD}{COLOR_WHITE}You can add the following lines to the bottom of your ~/.bashrc and ~/.zshrc files if they are not already there:{COLOR_RESET}")
        print() # This will print a blank line
        print(f"\033[92mif [ \033[95m-f \033[0m~/.bash_aliases\033[92m ]; \033[92mthen\033[0m")
        print(f"    . \033[0m~/.bash_aliases\033[0m")
        print(f"\033[92mfi\033[0m")
        print() # Blank line after the new message block

        # Then the "IMPORTANT" message
        print(f"\n{COLOR_BOLD}{COLOR_YELLOW}IMPORTANT: To activate this alias in your *current* and *permanent* terminal sessions,{COLOR_RESET}")
        print(f"{COLOR_BOLD}{COLOR_YELLOW}you MUST manually run the following command:{COLOR_RESET}")
        print() # This will print a blank line
        print(f"\033[1m\033[92m    source {alias_file_path}\033[0m")
        print() # This will print a blank line
        print(f"{COLOR_BOLD}{COLOR_WHITE}--------------------------------------------------------------------{COLOR_RESET}")
        return True # Successful completion

    except KeyboardInterrupt:
        print() # Blank line before message
        print("\n\033[91mOperation cancelled. Returning to main menu.\033[0m")
        return False # Interrupted

def manage_aliases():
    alias_file_path = os.path.expanduser("~/.bash_aliases")

    try:
            if not os.path.exists(alias_file_path) or os.stat(alias_file_path).st_size == 0:
                print(f"\nNo aliases or functions found in {alias_file_path}.")
                return False # Return False to continue to main menu

            with open(alias_file_path, "r") as f:
                lines = f.readlines()

            # Initial alias listing
            print(f"\n\033[1m\033[96m--- Current Aliases/Functions in \033[1m\033[92m{alias_file_path}\033[1m\033[96m ---")
            display_count = 0 # New counter for displayed lines
            for i, line in enumerate(lines):
                stripped_line = line.strip()
                if stripped_line: # Only process non-empty lines
                    display_count += 1
                    formatted_line = f"{COLOR_BOLD}{COLOR_YELLOW}{display_count}: {COLOR_RESET}{COLOR_BOLD}{COLOR_WHITE}{stripped_line}{COLOR_RESET}" # Use display_count

                    # Regex to find alias or function name
                    alias_match = re.match(r"^\s*alias\s+([a-zA-Z0-9_]+)=", stripped_line)
                    function_match = re.match(r"^\s*([a-zA-Z0-9_]+)\s*\(\)\s*\{", stripped_line)

                    if alias_match:
                        name = alias_match.group(1)
                        command_start_index = len(f"alias {name}=")
                        command_part = stripped_line[command_start_index:]
                        formatted_line = (
                            f"{COLOR_BOLD}{COLOR_WHITE}{display_count}: alias {COLOR_CYAN}{name}{COLOR_RESET}"
                            f"{COLOR_BOLD}{COLOR_WHITE}={COLOR_YELLOW}{command_part}{COLOR_RESET}"
                        )
                    elif function_match:
                        name = function_match.group(1)
                        # Find the position of the function name to color only the name
                        name_start_index = stripped_line.find(name)
                        name_end_index = name_start_index + len(name)

                        # The part before the name (e.g., "4: ")
                        prefix = stripped_line[:name_start_index]
                        # The part after the name, including "() {" and the command
                        suffix = stripped_line[name_end_index:]

                        # Find the start of the command part (after "() {")
                        command_start_marker = "() {"
                        command_start_index_in_suffix = suffix.find(command_start_marker)

                        if command_start_index_in_suffix != -1:
                            # Split suffix into "() {" and the command part
                            function_declaration_part = suffix[:command_start_index_in_suffix + len(command_start_marker)]
                            command_part = suffix[command_start_index_in_suffix + len(command_start_marker):]

                            formatted_line = (
                                f"{COLOR_BOLD}{COLOR_WHITE}{display_count}: {prefix}"
                                f"{COLOR_CYAN}{name}{COLOR_RESET}"
                                f"{COLOR_BOLD}{COLOR_WHITE}{function_declaration_part}"
                                f"{COLOR_YELLOW}{command_part}{COLOR_RESET}"
                            )
                        else: # Should not happen for valid function definitions, but as a fallback
                            formatted_line = (
                                f"{COLOR_BOLD}{COLOR_WHITE}{display_count}: {prefix}"
                                f"{COLOR_CYAN}{name}{COLOR_RESET}"
                                f"{COLOR_BOLD}{COLOR_WHITE}{suffix}{COLOR_RESET}"
                            )
                    print(formatted_line)
            print("\033[1m\033[96m----------------------------------------------------\033[0m")
            print() # Blank line before prompt

            while True: # Loop for initial delete choice
                delete_choice = input("\033[1m\033[92mDo you want to delete an alias/function? [y/N]: \033[0m").lower()
                if delete_choice == 'y':
                    break # Exit the loop to proceed with deletion
                elif delete_choice == 'n' or delete_choice == '': # 'n' or empty input means no
                    return False # User wants to return to main menu
                else:
                    print() # Blank line before message
                    print("\033[93mInvalid choice. Please enter 'y' or 'n'. Try again.\033[0m")
                    print()
                    continue # Continue the loop to re-prompt

            # Re-inserted deletion loop
            while True: # Loop for deleting multiple aliases
                print() # Blank line before prompt
                name_input = input("\033[1m\033[92mEnter the name(s) of the alias to delete (comma-separated for multiple, or 'all' to delete everything): \033[0m")

                if name_input.strip().lower() == 'all':
                    all_names = set()
                    for line in lines:
                        stripped_line = line.strip()
                        alias_match = re.match(r"^\s*alias\s+([a-zA-Z0-9_]+)=", stripped_line)
                        function_match = re.match(r"^\s*([a-zA-Z0-9_]+)\s*\(\)\s*\{", stripped_line)
                        if alias_match:
                            all_names.add(alias_match.group(1))
                        elif function_match:
                            all_names.add(function_match.group(1))
                    names_to_delete = all_names
                else:
                    names_to_delete = {name.strip() for name in name_input.split(',') if name.strip()}

                if not names_to_delete:
                    print() # Blank line before message
                    print("\033[93mNo names entered for deletion.\033[0m")
                    continue # Continue the deletion loop

                to_delete_flags = [False] * len(lines)
                deleted_names = set()
                found_names = set()

                for i_orig, line_orig in enumerate(lines): # Iterate through original lines for deletion logic
                    if to_delete_flags[i_orig]: # Already marked for deletion by a previous match
                        continue

                    for name in names_to_delete:
                        # Check for alias definition
                        if line_orig.strip().startswith(f"alias {name}="):
                                        print(f"Marking alias for deletion: {line_orig.strip()}")
                                        to_delete_flags[i_orig] = True
                                        deleted_names.add(name)
                                        found_names.add(name)
                                        break
                        # Check for function definition (using regex for robustness)
                        function_pattern = re.compile(r"^\s*{}\s*\(\)\s*\{{".format(re.escape(name)))
                        if function_pattern.match(line_orig):
                            # Extract the function name from the line for the colored message
                            function_match_for_print = re.match(r"^\s*([a-zA-Z0-9_]+)\s*\(\)\s*\{", line_orig.strip())
                            func_name_for_print = function_match_for_print.group(1) if function_match_for_print else name

                            colored_message = (
                                f"{COLOR_BOLD}{COLOR_YELLOW}Marking function for deletion: {COLOR_RESET}"
                                f"{COLOR_BOLD}{COLOR_CYAN}{func_name_for_print}{COLOR_RESET}"
                                f"{COLOR_BOLD}{COLOR_WHITE}() {{{COLOR_RESET}"
                            )
                            print(colored_message)
                            to_delete_flags[i_orig] = True
                            deleted_names.add(name)
                            found_names.add(name)

                            # Mark all lines of the function for deletion until the closing brace '}'
                            closing_brace_pattern = re.compile(r"^\s*\}\s*(#.*)?$")
                            for j in range(i_orig + 1, len(lines)):
                                if closing_brace_pattern.match(lines[j].strip()):
                                    to_delete_flags[j] = True
                                    break
                                to_delete_flags[j] = True
                            break

                new_lines = [line for i, line in enumerate(lines) if not to_delete_flags[i]]

                if deleted_names:
                    with open(alias_file_path, "w") as f:
                        f.writelines(new_lines)
                    # Reload lines after file write to reflect changes
                    with open(alias_file_path, "r") as f:
                        lines = f.readlines()
                    print(f"\n{COLOR_BOLD}{COLOR_GREEN}Successfully deleted: {COLOR_RESET}{', '.join(deleted_names)}{COLOR_BOLD}{COLOR_GREEN}{COLOR_RESET}")
                    print(f"{COLOR_BOLD}{COLOR_GREEN}Please run {COLOR_CYAN}source {alias_file_path}{COLOR_GREEN} to apply changes to your current session.{COLOR_RESET}")
                else:
                    print() # Blank line before message
                    print(f"{COLOR_BOLD}{COLOR_YELLOW}No matching aliases or functions were deleted.{COLOR_RESET}")
                    print() # Blank line after message

                not_found_names = names_to_delete - found_names
                if not_found_names:
                    print() # Blank line before message
                    print(f"{COLOR_BOLD}{COLOR_YELLOW}The following names were not found: {', '.join(not_found_names)}{COLOR_RESET}")
                    print() # Blank line after message

                while True: # Loop for input validation for "Delete another?"
                    print() # Blank line before prompt
                    another_delete = input(f"{COLOR_BOLD}{COLOR_GREEN}Delete another? [y/N]: {COLOR_RESET}").lower()
                    if another_delete == 'y':
                        break # Exit this inner validation loop, outer loop continues
                    elif another_delete == 'n' or another_delete == '':
                        return False # Exit manage_aliases, go to main menu
                    else:
                        print(f"\n\033[93mInvalid choice. Please enter 'y', 'n', or press Enter. Try again.\033[0m")
                        # No need to set error_message here, just print and re-prompt
                if another_delete == 'y': # Only continue if 'y' was explicitly chosen
                    continue # Continue the deletion loop
                else:
                    break # This break should not be reached if return False is used above
            return False # Return to the main menu after deletion loop finishes
    except KeyboardInterrupt:
        print() # Blank line before message
        print("\n\033[91mProcess Terminated\033[0m")
        return False # Return False to indicate interruption

if __name__ == "__main__":
    try:
        while True:
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
            print(f"{COLOR_BOLD}{COLOR_CYAN}{banner}{COLOR_RESET}")
            print(f"{COLOR_RESET}") # This prints a blank line after the banner
            print("< https://github.com/ghostescript/alias >") # Centered message
            print() # Blank line after menu header
            print() # Blank line after menu header
            print("\n\033[1m\033[92m--- Alias Manager Menu ---")
            print() # Blank line after menu header
            print("\033[1m\033[92m[1] Create a new alias/function")
            print("\033[1m\033[92m[2] Aliases/functions (list/delete)")
            print("\033[1m\033[92m[3] Exit")
            print() # Blank line before prompt
            choice = input("\033[1m\033[92mEnter your choice (1-3): \033[0m")

            if choice == '1':
                if not create_and_activate_alias(): # Call it once immediately and check return
                    continue # Go back to main menu if Ctrl+C was pressed

                while True: # Loop for creating additional aliases
                    error_message = ""
                    should_continue_creating = True
                    while True: # Inner loop for input validation
                        prompt = f"\n{COLOR_BOLD}{COLOR_GREEN}Create another alias/function? [y/N]: {COLOR_RESET}"
                        if error_message:
                            prompt = f"\n\033[93m{error_message}\033[0m" + prompt
                        try:
                            another_create = input(prompt).lower()
                        except KeyboardInterrupt:
                            print() # Blank line before message
                            print("\n\033[91mOperation cancelled. Returning to main menu.\033[0m")
                            should_continue_creating = False
                            break # Break inner loop, outer loop will then break

                        if another_create == 'y':
                            error_message = ""
                            if not create_and_activate_alias(): # Call again for another alias and check return
                                should_continue_creating = False
                                break # Break inner loop, outer loop will then break
                            break # Break inner loop, continue outer loop
                        elif another_create == 'n' or another_create == '':
                            error_message = ""
                            should_continue_creating = False
                            break # Break inner loop, then outer loop
                        else:
                            error_message = "Invalid choice. Please enter 'y' or 'n'. Try again."
                    if not should_continue_creating:
                        break # Break outer loop to return to main menu
            elif choice == '2':
                if manage_aliases(): # If manage_aliases returns True, exit the main loop
                    break
            elif choice == '3':
                print() # Blank line before message
                # Swapped order: Permanent message first
                print(f"\n{COLOR_BOLD}{COLOR_WHITE}To make the alias permanent for future sessions, ensure that your ~/.bashrc and ~/.zshrc files source ~/.bash_aliases.{COLOR_RESET}")
                print(f"{COLOR_BOLD}{COLOR_WHITE}You can add the following lines to the bottom of your ~/.bashrc and ~/.zshrc files if they are not already there:{COLOR_RESET}")
                print() # This will print a blank line
                print(f"\033[92mif [ \033[95m-f \033[0m~/.bash_aliases\033[92m ]; \033[92mthen\033[0m")
                print(f"    . \033[0m~/.bash_aliases\033[0m")
                print(f"\033[92mfi\033[0m")
                print() # Blank line after the new message block

                # Then the "IMPORTANT" message
                print(f"\n{COLOR_BOLD}{COLOR_YELLOW}IMPORTANT: To activate this alias in your *current* and *permanent* terminal sessions,{COLOR_RESET}")
                print(f"{COLOR_BOLD}{COLOR_YELLOW}you MUST manually run the following command:{COLOR_RESET}")
                print() # This will print a blank line
                print(f"\033[1m\033[92m    source /home/kali/.bash_aliases\033[0m")
                print() # This will print a blank line

                print("\033[91mExiting Alias Manager.\033[0m")
                sys.exit(0)
            else:
                print() # Blank line before message
                print("\033[93mInvalid choice. Please enter 1, 2, or 3.\033[0m")
    except KeyboardInterrupt:
        print() # Blank line before message
        print("\n\033[91mProcess Terminated\033[0m")
        sys.exit(1)
