# Parent class for all other controllers(functions)
from ..helpers import get_settings, Settings
import os
import random
import string


class BaseController:

    def __init__(self):
        self.app_settings = get_settings()  # type: ignore[call-arg]

        self.base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # Get the base directory of the project which is src
        self.file_dir = os.path.join(
            self.base_dir,
            "assets/files",
        )  # Define the directory to store uploaded files
        
        self.database_dir = os.path.join(
            self.base_dir,
            "assets/database"
        )  # Define the directory to store the database file

    def generate_random_string(self, length: int = 12):
        return ''.join(
            random.choices(
                string.ascii_letters + string.digits,
                k=length,
            )
        )
    
    def get_database_path(self, db_name: str):
        database_path = os.path.join(self.database_dir, db_name)

        if not os.path.exists(self.database_dir):
            os.makedirs(self.database_dir)
        return database_path
    