import subprocess
from settings import iCLOUD_REPORTING_PATH
from reportings import medtronic
from os.path import join as joinpath

from utils import timer

timer.timeit(medtronic.dms_report_with_offset)
# df = medtronic.dms_report_with_offset()
# df.to_excel(joinpath(iCLOUD_REPORTING_PATH, 'Medtronic DMS Report', "dms_report_with_offset.xlsx"), index=False)

# subprocess.Popen(r'explorer /select,"C:\Users\Paco\iCloudDrive\Documents\2 Areas ♾️\💼 Reportings\Medtronic DMS Report\dms_report_with_offset.xlsx')