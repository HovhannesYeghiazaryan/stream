import os

import dotenv
from dotenv import load_dotenv

load_dotenv(dotenv.find_dotenv('.env'))

CLUSTERS_DIRECTORY = os.getenv('CLUSTERS_DIRECTORY', '/app/all-in-one/clusters')
TEMPLATES_DIRECTORY = os.getenv('TEMPLATES_DIRECTORY', '/app/all-in-one')

files_dir = os.listdir(CLUSTERS_DIRECTORY)
all_files = [
    file_name
    for file_name in files_dir
    if file_name.endswith('yaml') or file_name.endswith('yml')
]
