
# suppose the agent is authorized to get some user info


import yaml
import os


def get_user_profile(args=None):
    with open(os.path.join(os.path.dirname(os.path.realpath(__file__)), "../config.yml")) as file:
        conf = yaml.safe_load(file)

    ret_obj = {
        "name": conf["USER"]["name"],
        "age": conf["USER"]["age"],
        "sex": conf["USER"]["sex"],
        "location": conf["USER"]["location"],
        "language": conf["USER"]["language"],
    }
    return ret_obj




