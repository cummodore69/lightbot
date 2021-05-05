# Sorry if the code is horrible, I'm just following stackoverflow and a random article about loading yaml files in
# Python.
# - E404NNF

# Import the YAML module
import yaml

class ProcessYaml:
    
    # We need to pre-define the commands values list and the value for the config itself
    config = []
    commands_config = []
    
    # Open the config.yml file using open
    with open('config.yml', 'r') as file:
        try:
            # Load config using yaml
            config = yaml.safe_load(file)
            # Grab the commands list from the config file
            commands_config = config['commands']
            # Just printing config as a debug
            print("Config loaded successfully!\nPrinting Config...\n")
            print(config)
        # If an error happens, print the error.
        except yaml.YAMLError as exc:
            print(exc)
