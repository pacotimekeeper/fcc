from settings import iCLOUD_DRIVE, PARA_FOLDERS, REPORTINGS_DIR

import os
from os.path import join as joinpath
import pandas as pd
from pathlib import Path
from datetime import datetime

REPORT_PATH = joinpath(iCLOUD_DRIVE, PARA_FOLDERS[2], REPORTINGS_DIR, 'CHCSJ Ortho Case Report')
SUPPORTING_FILES_PATH = joinpath(REPORT_PATH, "supporting_files")
os.listdir(SUPPORTING_FILES_PATH)

# Constants (you need to define these based on your context)
SUPPLIERS = ['CBT', 'UOC', 'ESN']  # Example suppliers
CHCSJ_CASE_REPORT_PATH = Path('path/to/report/directory')  # Adjust this path accordingly
SURGICAL_DIR = Path('path/to/surgical/directory')  # Adjust this path accordingly
company_name_map = {"UOC":"United Orthopedic Corporation", 
                    "ESN": "S&N", 
                    "CBT":"Baxter"}

def remove_zeros(value):
    pat_no = str(int(value))
    end = len(pat_no) -1
    pat_no = pat_no[:end] + '.' + pat_no[end]
    return pat_no

# def chcsj_surgery_report(supplier, from_date, to_date):
def chcsj_surgery_report():
   # Load the CBT sales
    # company_name_map = sap_prefix_name_dict(SUPPLIERS)

    files = [joinpath(SUPPORTING_FILES_PATH, file) for file in os.listdir(SUPPORTING_FILES_PATH) if 'Sales report to Z11' in file]

    df = pd.read_excel(files[0])
    # Rename columns
    df.rename(columns={
        "項目號碼": "編號",
        "PATIENT No": "金卡編號",
        "itemanme": "產品描述",
        "OPERATION No": "手術編號",
        "OPERATION DATE": "手術日期",
        "quantity": "數量",
        "Linetotal": "單價"
    }, inplace=True)

    # Filter rows where 手術編號 is not missing
    df = df[df['手術編號'].notna()]

    # Load mapping file    
    mapping = pd.read_excel(joinpath(SUPPORTING_FILES_PATH, "esn_mappings.xlsx"))[["編號", "Item Code"]]
    
    # Filter mapping where Item Code is not missing
    mapping = mapping[mapping['Item Code'].notna()]
    
    # Rename Item Code column
    mapping.rename(columns={"Item Code": "產品型號"}, inplace=True)

    # Left join with mapping
    df = df.merge(mapping, on='編號', how='left')

    # Map manufacturers using company_name_map
    df['製造商'] = df['編號'].apply(lambda x: company_name_map[x[:3]])

    # Remove leading zeros from 金卡編號
    df['金卡編號'] = df['金卡編號'].apply(remove_zeros)
    
    # Replace "/" with "-" in 手術日期 and convert to datetime format
    df['手術日期'] = pd.to_datetime(df['手術日期'].str.replace('/', '-'), format='%Y-%m-%d')

    # Filter by date range
    today = datetime.now()
    
    from_date = datetime(today.year - 1, 1, 1)
    to_date = datetime(today.year, 12, 31)

    df = df[(pd.to_datetime(df['手術日期']) >= from_date) & (pd.to_datetime(df['手術日期']) <= to_date)]

    df['供應商'] = "全昌行"
    
    # Calculate total amount
    df['總金額'] = df['單價'] * df['數量']

    # Add missing columns with missing values
    for col in ["患者姓名", "特別醫療消耗性物品記錄右上角編號", "術式"]:
        df[col] = pd.NA

    cols = ["供應商", "患者姓名", "金卡編號", "手術日期", "手術編號", 
            "製造商", "產品型號", "產品描述", "數量", "單價", 
            "總金額", "特別醫療消耗性物品記錄右上角編號", "術式"]
    
    df.sort_values(by=['手術日期', '金卡編號'], inplace=True)
    df['手術日期'] = df['手術日期'].dt.strftime('%Y-%m-%d')
    return df[cols]
    # df.to_excel("temp.xlsx")

def gen_report_chcsj_surgery(from_date, to_date):
    dfs = []
    
    for supplier in ['CBT', 'UOC', 'ESN']:
        try:
            dfs.append(chcsj_surgery_report(supplier, from_date, to_date))
        except Exception as e:
            print("File not found")
            print(e)

    if dfs:
        combined_df = pd.concat(dfs, ignore_index=True)
        combined_df.sort_values(by=['手術日期', '金卡編號'], inplace=True)
        
        file_path = CHCSJ_CASE_REPORT_PATH / f"chcsj_surgery_report_{from_date}_to_{to_date}.xlsx"
        
        combined_df.to_excel(file_path, index=False)


# Example usage:
chcsj_surgery_report().to_excel("temp.xlsx")