from settings import SHARED_RESOURCE_FOLDER, iCLOUD_REPORTING_PATH 

from shutil import copy as cp
import os
from os.path import join as joinpath
import pandas as pd
import numpy as np

def dms_report():
    mapping_file = joinpath(SHARED_RESOURCE_FOLDER, 'mappings.xlsx')
    cp(joinpath(SHARED_RESOURCE_FOLDER, 'mappings', 'cwl_mappings(master).xlsx'), mapping_file)
    SUPPORTING_FILES_PATH = os.path.join(iCLOUD_REPORTING_PATH, 'Medtronic DMS Report', 'supporting_files')
    sales_report_file = [os.path.join(SUPPORTING_FILES_PATH, fname) for fname in os.listdir(SUPPORTING_FILES_PATH) if 'sales report' in fname.lower()][0]
    df = pd.read_excel(sales_report_file)
    mappings = pd.read_excel(mapping_file)

    # print(mappings)


    # Rename columns
    df.rename(columns={
        'Code': '編號',
        'Batch No.': '序號/批號',
        'Invoice No./CreditMemo NO.': '發票號碼',
        'Quantity': '銷售數量',
        'UnitPrice': '銷售單價(含稅)'
    }, inplace=True)

    # # Create 發票日期 column
    df['發票日期'] = df['Year'].astype(str) + '/' + df['Month'].astype(str).str.zfill(2) + '/' + df['Day'].astype(str).str.zfill(2)

    # # Load mappings and perform left join
    # mappings = read_excel('path/to/cwl_mappings.xlsx')[['編號', 'Conv']]
    df = df.merge(mappings, on='編號', how='left')

    convitems = pd.read_excel(joinpath(SUPPORTING_FILES_PATH, 'dms_mappings.xlsx'), sheet_name='dmsconv')['編號']
   
    # # Create NeededConv column
    df['NeededConv'] = ~df['編號'].isin(convitems)
    
    # # Convert 銷售數量 to integer
    df['銷售數量'] = pd.to_numeric(df['銷售數量'], errors='coerce').fillna(0).astype(int)

    # # Update 銷售數量 based on NeededConv
    df['銷售數量'] = np.where(df['NeededConv'], df['銷售數量'] * df['Conv'], df['銷售數量'])

    # # Update 銷售單價(含稅) based on NeededConv
    df['銷售單價(含稅)'] = np.where(df['NeededConv'], df['銷售單價(含稅)'] / df['Conv'], df['銷售單價(含稅)'])

    # # Select relevant columns
    selected_columns = ['編號', 'Customer Code', '序號/批號', '銷售數量', '銷售單價(含稅)', '發票號碼', '發票日期']
    df = df[selected_columns]
    
    # Perform left join with cwlmappings
    df = df.merge(mappings[['編號', 'CFN']], on='編號', how='left')

    dmsmappings = pd.read_excel(joinpath(SUPPORTING_FILES_PATH, 'dms_mappings.xlsx'), sheet_name='Product Category')[['CFN', '銷售團隊', '銷售業務代表']]
    
    # # Left join with dmsmappings
    df = df.merge(dmsmappings, on='CFN', how='left')
    dms_customers = pd.read_excel(joinpath(SUPPORTING_FILES_PATH, 'dms_mappings.xlsx'), sheet_name='dmscustomers')[['Customer Code', '銷售醫院']]
    
    # # Left join with dmscustomers
    df = df.merge(dms_customers, on='Customer Code', how='left')
    # # Rename CFN column
    df.rename(columns={'CFN': '型號(CFN)'}, inplace=True)

    # # Select final columns
    final_columns = ['銷售團隊', '銷售醫院', '型號(CFN)', '序號/批號', '銷售數量', '銷售單價(含稅)', '發票號碼', '發票日期', '銷售業務代表']
    
    df = df[final_columns]

    # # Insert additional columns
    df.insert(3, '分倉庫', "FIRMA CHUN CHEONG PRODUCTOS主倉庫_Z")
    df.insert(7, '幣種', "MOP")
    
    for col in ['次級經銷商', '備註', '科室']:
        df[col] = np.nan  # Insert missing values for new columns

    cols_ordered = ['銷售團隊', '銷售醫院', '分倉庫', 
                    '型號(CFN)', 
                    '序號/批號', 
                    '銷售數量',
                    '銷售單價(含稅)', 
                    '幣種',
                    '發票號碼',
                    '發票日期',
                    '銷售業務代表',
                    '次級經銷商',
                    '備註',
                    '科室']

#     # Sort by 發票日期 in descending order and select columns
    df.sort_values(by='發票日期', ascending=False, inplace=True)
    
    return df[cols_ordered]

# # Function to handle offset logic (similar to cwlDMSReportWithOffset)
def dms_report_with_offset():
    df = dms_report()
    
    # Convert 發票日期 to datetime format
    df['發票日期'] = pd.to_datetime(df['發票日期'], format='%Y/%m/%d')

    # Insert index column at row 1
    df.insert(0, "index", range(1, len(df) + 1))

    cancel_rows = df[df['銷售數量'] < 0]
    search_rows = df[df['銷售數量'] > 0]

    offsetdict = {}

    for _, cancel_row in cancel_rows.iterrows():
        for _, row in search_rows.iterrows():
            if (row['銷售數量'] == abs(cancel_row['銷售數量']) and 
                row['銷售團隊'] == cancel_row['銷售團隊'] and 
                row['銷售醫院'] == cancel_row['銷售醫院'] and 
                row['型號(CFN)'] == cancel_row['型號(CFN)'] and 
                row['序號/批號'] == cancel_row['序號/批號'] and 
                row['發票日期'].month == cancel_row['發票日期'].month and 
                row['發票日期'].year == cancel_row['發票日期'].year and 
                row['發票日期'] < cancel_row['發票日期']):
                
                offsetdict[cancel_row.name] = row.name

    # Combine keys and values of offsetdict into a single array
    offsetlist = list(offsetdict.keys()) + list(offsetdict.values())
    
    # Mark rows to be deleted based on offsetlist
    df['to_be_del'] = np.where(df.index.isin(offsetlist), "Delete?", "")
    
    return df.drop(columns=["index"])  # Drop index column if needed

