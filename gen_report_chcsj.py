from reportings.chcsj_ortho_case_report import chcsj_surgery_report
import pandas as pd
from settings import FCC_SHARED_FOLDER, PARA_FOLDERS
from os.path import join as joinpath


def run():
    dfs = []
    for supplier in ['CBT', 'UOC', 'ESN']:
        try:
            df = chcsj_surgery_report(supplier)
            dfs.append(df)
        except Exception as e:
            print("File not found")
            print(e)


    combined_df = pd.concat(dfs, ignore_index=True)
    combined_df.sort_values(by=['手術日期', '金卡編號'], inplace=True)

    combined_df.to_excel(joinpath(FCC_SHARED_FOLDER, PARA_FOLDERS[2], 'Reportings', "CHCSJ Ortho Case Report.xlsx"), index=False)


