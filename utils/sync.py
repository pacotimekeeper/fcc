from os.path import join as joinpath
from settings import SHARED_RESOURCE_FOLDER, iCLOUD_REPORTING_PATH
from shutil import copy as cp

def update_mappings():
    MDT_SUPPORTINGS_PATH = joinpath(iCLOUD_REPORTING_PATH, 'Medtronic DMS Report', 'supporting_files')

    mapping_file = joinpath(MDT_SUPPORTINGS_PATH, 'mappings.xlsx')

    ## copy mapping file (Shared G drive) 3 Resources 📚 to 
    src_file = joinpath(SHARED_RESOURCE_FOLDER, 'mappings', 'cwl_mappings(master).xlsx')
    cp(src_file, mapping_file)