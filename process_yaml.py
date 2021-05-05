import yaml


# Sorry if the code is horrible, i'm just following stackoverflow and a random article about loading yaml files in
# python

class ProcessYaml:
    config = []
    commands_config = []

    with open('config.yml', 'r') as file:
        try:
            config = yaml.safe_load(file)
            commands_config = config['commands']
            print("Config loaded successfully!\nPrinting Config...\n")
            print(config)
        except yaml.YAMLError as exc:
            print(exc)
