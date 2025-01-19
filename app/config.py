import os

from dotenv import dotenv_values


def env_variables():
    current_directory = os.path.dirname(os.path.abspath(__file__))
    mode = os.getenv("MODE", "local")
    if mode == "development":
        env_file = os.path.join(current_directory, "../.env.development")
    else:
        env_file = os.path.join(current_directory, "../.env.local")
    env = dotenv_values(env_file)

    return env
