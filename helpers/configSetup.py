import json
import os
from dotenv import load_dotenv

load_dotenv()

# This is held together with sheer will power and sticky tape 
# I dont fully understand how it works but it does

# --------- #

class Config:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super().__new__(cls)
            return cls._instance
        else:
            raise Exception("An instance of Config already exists. Use Config.get_instance() to access it.")

    def __init__(self, path="config.json"):
        if not hasattr(self, "initialized"):
            self.path = path
            self.load()
            self.initialized = True

    @classmethod
    def getMainInstance(cls):
        if not cls._instance:
            cls._instance = cls()
        return cls._instance

    def load(self):
        with open(self.path, "r") as file:
            data = json.load(file)

        self.token = os.getenv("TOKEN")
        self.admin = os.getenv("ADMIN")
        self.docker = os.getenv("DOCKER", "False").lower() in ("true", "1")

        self.enabled = data["enabled"]
        self.firstRun = data["firstRun"]
        self.totalFixed = data["totalFixed"]
        self.timeoutTime = data["timeoutTime"]
        self.nsfwAllowed = data["nsfwAllowed"]

    def save(self):

        with open(".env", "w") as env:
            env.write(f"TOKEN={self.token}\n")
            env.write(f"ADMIN={self.admin}\n")

        data = {
            "enabled": self.enabled,
            "firstRun": self.firstRun,
            "totalFixed": self.totalFixed,
            "timeoutTime": self.timeoutTime,
            "nsfwAllowed": self.nsfwAllowed
        }

        with open(self.path, "w") as file:
            json.dump(data, file, indent=4)

    def update(self, token=None, admin=None, enabled=None, firstRun=None, totalFixed=None, nsfwAllowed=None):
        if token is not None:
            self.token = token
        if admin is not None:
            self.admin = admin
        if enabled is not None:
            self.enabled = enabled
        if firstRun is not None:
            self.firstRun = firstRun
        if totalFixed is not None:
            self.totalFixed = totalFixed
        if nsfwAllowed is not None:
            self.nsfwAllowed = nsfwAllowed

    def toggle(self):
        self.enabled = not self.enabled