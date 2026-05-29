# generate new file for each project id from the uploaded data to store it in assets.files
from .BaseController import BaseController
import os


class ProjectController(BaseController):  # inheritance from BaseController to access common functionalities and configurations

    def __init__(self):
        super().__init__()

    def get_project_path(self, project_id: str):
        project_dir = os.path.join(
            self.file_dir,
            project_id,
        )  # Create a directory path for the project using the base file directory and the project ID

        if not os.path.exists(project_dir):  # Check if the project directory already exists
            os.makedirs(project_dir)  # If it doesn't exist, create the directory

        return project_dir  # Return the path to the project directory
