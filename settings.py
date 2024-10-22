import os

DB_CONFIG = {
  'user': 'root',
  'password': 'root',
  'host': 'localhost',
  'port': 3306,
  'database': 'mysql',
  'raise_on_warnings': True,
}

USERPROFILE = os.path.expanduser('~')
 
iCLOUD_PATH = os.path.join(USERPROFILE, 'iCloudDrive') if os.name == 'nt' else "not set"
iCLOUD_REPORTING_PATH = os.path.join(iCLOUD_PATH, 'Documents', '2 Areas ♾️', '💼 Reportings')

SHARED_RESOURCE_FOLDER = 'G:/My Drive/Surgical/3 Resources 📚' if os.name == 'nt' else 'not set'
