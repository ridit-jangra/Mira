# This script downloads the Python 3.11 installer
import os
import requests

url = 'https://www.python.org/ftp/python/3.11.0/python-3.11.0.exe'
file_name = 'python-3.11.0.exe'

if not os.path.exists(file_name):
    response = requests.get(url)
    with open(file_name, 'wb') as f:
        f.write(response.content)
    print(f'Successfully downloaded {file_name}')
else:
    print(f'{file_name} already exists.')