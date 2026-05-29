# for logics(functions) related to data management, such as uploading, processing, and storing data.
from .BaseController import BaseController
from fastapi import UploadFile
from ..models import ResponseSignals
from .ProjectController import ProjectController
import re
import os


class DataController(BaseController):  # inheritance from BaseController to access common functionalities and configurations

    def __init__(self):
        super().__init__()  # Call the constructor of the BaseController to initialize settings and other common attributes
        self.size_scale = 1024 * 1024  # Scale for converting file size to MB

    def validate_uploaded_file(self, file: UploadFile):
        if file.content_type not in self.app_settings.FILE_ALLOWED_TYPES:
            return False, ResponseSignals.FILE_TYPE_NOT_SUPPORTED.value

        if file.size is None or file.size > self.app_settings.FILE_MAX_SIZE * self.size_scale:  # Convert MB to bytes
            return False, ResponseSignals.FILE_SIZE_EXCEEDED.value

        return True, ResponseSignals.FILE_VALIDATED_SUCCESS.value

    def generate_unique_filepath(self, orig_file_name: str | None, project_id: str):
        random_key = self.generate_random_string()  # Generate a random string to ensure uniqueness
        project_path = ProjectController().get_project_path(project_id=project_id)  # Get the project path using the ProjectController

        cleaned_file_name = self.get_clean_file_name(orig_file_name=orig_file_name)  # Clean the original filename to remove unwanted characters

        new_file_path = os.path.join(
            project_path,
            random_key + "_" + cleaned_file_name,
        )  # Combine the project path, random string, and cleaned filename to create a unique file path

        while os.path.exists(new_file_path):  # Check if a file with the generated name already exists
            random_key = self.generate_random_string()  # Generate a new random string if there is a collision
            new_file_path = os.path.join(
                project_path,
                random_key + "_" + cleaned_file_name,
            )  # Create a new file path with the new random string

        return new_file_path, random_key + "_" + cleaned_file_name  # Return the unique file path for storing the uploaded file

    def get_clean_file_name(self, orig_file_name: str):
        # Remove any characters that are not alphanumeric, dot, underscore
        cleaned_file_name = re.sub(
            r'[^\w\.-]',
            '',
            orig_file_name.strip(),
        )

        cleaned_file_name = cleaned_file_name.replace(
            " ",
            "_",
        )  # Replace spaces with underscores

        return cleaned_file_name
