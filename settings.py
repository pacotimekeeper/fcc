import os
from os.path import join as joinpath
from pathlib import Path

# # DB Settings
DB_CONFIG = {
  'user': 'root',
  'password': 'root',
  'host': 'localhost',
  'port': 3306,
  'database': 'mysql',
  'raise_on_warnings': True,
}

# # FOLDER Constant
USERPROFILE = str(Path.home()) #os.path.expanduser('~')

# Define the path based on the operating system
match os.name:
    case 'nt':
        FCC_SHARED_FOLDER = r'G:/My Drive/Surgical/'
        iCLOUD_DRIVE = joinpath(USERPROFILE, 'iCloudDrive')
    case 'posix':
        iCLOUD_DRIVE = joinpath(USERPROFILE, 'Documents')
        FCC_SHARED_FOLDER = joinpath(USERPROFILE, 'Library','CloudStorage','GoogleDrive-kaiipho@gmail.com','.shortcut-targets-by-id','1S3ebWPM9oMQBhWznv-0LTz9RqgOMJd6m','Surgical')
    case _:
        pass
        
PARA_FOLDERS = ['0 inbox 📥', '1 Projects ⛳️', '2 Areas ♾️', '3 Resources 📚', '4 Archives 🗂️']
REPORTINGS_DIR = '💼 Reportings'