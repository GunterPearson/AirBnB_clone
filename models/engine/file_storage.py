#!/usr/bin/env python3
"""This module creates a FileStorage class"""
from uuid import uuid4
from datetime import datetime
from os.path import isfile
import json


class FileStorage:
    """This is an instance of the FileStorage class"""
    __file_path = "file.json"
    __objects = {}

    def all(self):
        """This function returns the dictionary FileStorage.__objects"""
        self.reload()
        return FileStorage.__objects

    def new(self, obj):
        """This function sets in __objects
        the obj with key <obj class name>.id"""
        key_string = obj.__class__.__name__ + "." + obj.id
        FileStorage.__objects[key_string] = obj

    def save(self):
        """This function serializes __objects to the JSON file"""
        for obj_id in FileStorage.__objects:
            if type(FileStorage.__objects[obj_id]) != dict:
                FileStorage.__objects[obj_id]\
                    = FileStorage.__objects[obj_id].to_dict()
        with open(FileStorage.__file_path, "w") as fp:
            json.dump(FileStorage.__objects, fp)

    def reload(self):
        """This function deserializes the
        JSON file to __objects, if the JSON file exists"""
        from models.base_model import BaseModel
        from models.user import User
        from models.place import Place
        from models.state import State
        from models.city import City
        from models.amenity import Amenity
        from models.review import Review
        if isfile(FileStorage.__file_path):
            with open(FileStorage.__file_path) as fp:
                FileStorage.__objects = json.load(fp)
            for obj_id in FileStorage.__objects:
                class_name = FileStorage.__objects[obj_id].get("__class__")
                FileStorage.__objects.update(
                    {obj_id: eval(class_name)(**FileStorage.__objects[obj_id])}
                )
