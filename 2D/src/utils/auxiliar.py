'''
Project: Skelly & Souli
Authors:

Ivan García Quintela
Ismael Míguez Valero
Lola Suárez González

Version: 1.0.0
'''

import json
import os
import sys

"""
Funciones auxiliares para el manejo de los archivos json y los paths."""
# Función para obtener el path de los archivos
def get_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

# Función para cargar un archivo json
def load_json(path):

    try:
        with open(path, "r", encoding="utf-8") as file:
            return json.load(file)
    except FileNotFoundError:
        print(f" Error: File not found {path}.")
        return {}
    except json.JSONDecodeError:
        print(f" Error: File corrupted {path}. ")
        return {}
# Función para guardar un archivo json
def save_json(path, data):
    try:
        with open(path, "w", encoding="utf-8") as file:
            json.dump(data, file, indent=4, ensure_ascii=False)
    except Exception as e:
        print(f" Error: Cannot save {path}: {e}")

# Función para añadir un valor a un archivo json
def update_json(path, key, value):
   
    data = load_json(path)
    data[key] = value 
    save_json(path, data)

def delete_key_json(path, key):
  
    datas = load_json(path)
    if key in datas:
        del datas[key]
        save_json(path, datas)
    else:
        print(f" Warning: the key '{key}' does not exist on  {path}.")

