import os
import re

def main():
    commands_dir = os.path.join(os.path.dirname(__file__), "commands")
    if not os.path.exists(commands_dir):
        print("Commands dir not found.")
        return

    # To use our new parse logic we need to import it
    import sys
    sys.path.append(os.path.join(os.path.dirname(__file__), "api"))
    try:
        from commands import parse_ps1_content, save_command, CommandConfig
    except ImportError as e:
        print("Error importing from commands:", e)
        return

    bats = [f for f in os.listdir(commands_dir) if f.endswith(".bat")]
    for bat in bats:
        bat_path = os.path.join(commands_dir, bat)
        ps1_filename = bat.replace(".bat", ".ps1")
        ps1_path = os.path.join(commands_dir, ps1_filename)

        with open(bat_path, "r", encoding="utf-8") as f:
            content = f.read()

        try:
            # We can use the parse_ps1_content function since it uses regexes that are mostly the same for bat and ps1 (like -a, -m, etc)
            config = parse_ps1_content(content, ps1_filename)
            
            # The parser might miss port if it's looking for powershell param format. 
            # In bat, it is usually %PORT_ARG%. The default in our config is 8080.
            if not config.alias or not config.model_path:
                print(f"Skipping {bat}: missing alias or model_path")
                continue

            # We don't want raw_content here because we want to generate a fresh PS1 using the backend generator
            config.raw_content = None 
            
            save_command(config)
            print(f"Successfully generated {ps1_filename} from {bat}")
        except Exception as e:
            print(f"Error processing {bat}: {e}")

if __name__ == "__main__":
    main()
