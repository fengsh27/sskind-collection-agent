import yaml

from config.constants import ScopeTypeEnum

def read_config_query(scope_type: ScopeTypeEnum):
    with open("./config/scope_config.yaml", 'r') as file:
        config = yaml.safe_load(file)
        sc_config = config[scope_type.value]
    return sc_config["query"], sc_config["mindate"], sc_config["maxdate"]

def read_config_identify_instructions(scope_type: ScopeTypeEnum):
    with open("./config/scope_config.yaml", 'r') as file:
        config = yaml.safe_load(file)
        sc_config = config[scope_type.value]
    return sc_config.get("identify_instructions", "N/A")

