# Static Class
import os
import platform

class FileDAO:
    
    @staticmethod
    def get_project_list():
        dev_path = "/home/jpires/Dev" if platform.system() == "Linux" else "D:/Dev"
        projects = []
        for entry in os.scandir(dev_path):
            if entry.is_dir():
                for project in os.scandir(entry):
                    if project.is_dir():
                        projects.append(project.name)
        return projects
    
    @staticmethod
    def get_projets_in_folder(folder):
        return os.listdir(folder)

    @staticmethod
    def find_project(project_name):
        dev_path = "/home/jpires/Dev" if platform.system() == "Linux" else "D:/Dev"
        for entry in os.scandir(dev_path):
            if entry.is_dir():
                for project in os.scandir(entry):
                    if project.is_dir() and project.name == project_name:
                        return project.path
        return None
    