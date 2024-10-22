from utils import data_extract as dt
from os.path import join as joinpath
import os
import pandas as pd
import subprocess

dst = r'C:\Users\Paco\Documents\FCC\2 Areas ♾️\💼 Inventory MGMT\cwl_tenders'
dstPath = r'C:\Users\Paco\Documents\FCC\2 Areas ♾️\💼 Inventory MGMT'
file = joinpath(dstPath, "cwl_tenders.xlsx")

def save_tenders():
    tender_nos = dt.sap_tender_nos("cwl")
    if len(tender_nos) == 0:
        print("No sales orders found for cwl")

    for tender_no in tender_nos:
        df = dt.search_tender(tender_no)
        basename = tender_no.replace("/", "&")
        df.to_pickle(joinpath(dst, f"{basename}.pickle"))
        print("...Done")

# def read_pickle_files_to_excel(folder_path, output_file):
    # Create an empty list to hold DataFrames

def export_tenders_to_excel():
    dataframes = []

    # Iterate over all files in the specified folder
    for filename in os.listdir(dst):
        if filename.endswith('.pkl') or filename.endswith('.pickle'):
            # Construct full file path
            file_path = os.path.join(dst, filename)
            # Read the pickle file into a DataFrame
            df = pd.read_pickle(file_path)

            # Insert a new column with the filename (without extension)
            df['Tender_No'] = os.path.splitext(filename)[0].replace("&", "/")
            # Append the DataFrame to the list
            dataframes.append(df)

    # Concatenate all DataFrames into a single DataFrame
    combined_df = pd.concat(dataframes, ignore_index=True)

    combined_df.drop(columns= ['序號', 'Missing1', 'Missing2', 'Missing3'], inplace=True)
    return combined_df
    # Export the combined DataFrame to an Excel file


df = export_tenders_to_excel()
try:
    df.to_excel(joinpath(dstPath, "cwl_tenders.xlsx"), index=False)
except:
    print('Unable to save file')

def kwh_sos_with_tenders()
    from utils import data_extract as dt
    import pandas as pd
    kwh_so_num = "241026076"
    chcsj_so_num = "241030383"
    # dt.doc_check(kwh_so_num)
    # dt.doc_check(chcsj_so_num).to_excel("{}.xlsx".format(chcsj_so_num))

    df = dt.doc_check(kwh_so_num)
    for col in ['貨號', '貨品名稱', '數量']:
        df[col] = df[col].str.strip()

    df.to_excel("{}.xlsx".format(kwh_so_num))


subprocess.Popen(r'explorer /select, "{}"'.format(file))

