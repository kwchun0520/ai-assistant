import yaml


def load_yaml(file_path) -> dict[str, str]:
    """Load a YAML file and return its content.
    
    Args:
        file_path (str): The path to the YAML file.
    Returns:
        dict[str, str]: The content of the YAML file as a dictionary.
    """
    with open(file_path, 'r') as file:
        return yaml.safe_load(file)
    