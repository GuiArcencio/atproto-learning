from os import makedirs, path
from typing import Optional
import json

_folder = "data"
_file = "account.json"
_filepath = f"{_folder}/{_file}"

def get_account_info() -> dict[str, str]:
    if not path.exists(_filepath):
        update_account_info()
    
    with open(_filepath, "r") as f:
        return json.load(f)
        

def update_account_info(**kwargs):
    if not path.exists(_filepath):
        makedirs(_folder)
        with open(_filepath, "w") as f:
            f.write("{}")

    with open(_filepath, "r") as f:
        account_data = json.load(f)

    account_data.update(**kwargs)

    with open(_filepath, "w") as f:
        json.dump(account_data, f)