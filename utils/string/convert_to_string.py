import os
import re


def __get_env(env_name: str) -> str:
    data = os.environ.get(env_name)
    return str(data)


def convert_to_string(env_name: str) -> list:
    data = __get_env(env_name)
    data_list = [re.sub(r"[' ]", '', d) for d in data.split(',')]
    return data_list
