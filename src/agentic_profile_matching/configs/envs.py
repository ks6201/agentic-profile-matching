import os
from typing import Any

from dotenv import load_dotenv

class Env:

    def __init__(self):
        load_dotenv()
        self.envs: dict[str, Any] = {}

    def get(self, env: str) -> str:
        if env in self.envs:
            return self.envs[env]
        
        value = os.getenv(env)

        if value is None:
            raise Exception(f"Value for env key '{env}' is missing.")

        self.envs[env] = value

        return value