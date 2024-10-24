from settings import iCLOUD_DRIVE, PARA_FOLDERS
from reportings import medtronic
from os.path import join as joinpath

def run():
    file = joinpath(iCLOUD_DRIVE, PARA_FOLDERS[2], '__FCC__Reportings', 'Medtronic DMS Report', "dms_report_with_offset.xlsx")
    df = medtronic.dms_report_with_offset()
    df.to_excel(file, index=False)
