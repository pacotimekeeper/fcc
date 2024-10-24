from settings import iCLOUD_DRIVE, PARA_FOLDERS

import os
from os.path import join as joinpath
import pandas as pd
from pathlib import Path
from datetime import datetime
import re

REPORT_PATH = joinpath(iCLOUD_DRIVE, PARA_FOLDERS[2], '__FCC__Reportings', 'CHCSJ Ortho Case Report')
SUPPORTING_FILES_PATH = joinpath(REPORT_PATH, "supporting_files")
os.listdir(SUPPORTING_FILES_PATH)

SUPPLIERS = ['CBT', 'UOC', 'ESN']  # Example suppliers
company_name_map = {"UOC":"United Orthopedic Corporation", 
                    "ESN": "Smith & Nephew", 
                    "CBT":"Baxter"}

def remove_zeros(value):
    pat_no = str(int(value))
    end = len(pat_no) -1
    pat_no = pat_no[:end] + '.' + pat_no[end]
    return pat_no


## Data Integry check
def chcsj_surgery_report(supplier_code):

    pattern = re.compile(f"{supplier_code} Sales report to Z11", re.IGNORECASE)
    file = [joinpath(SUPPORTING_FILES_PATH, file) for file in os.listdir(SUPPORTING_FILES_PATH) if pattern.search(file)][0]

    df = pd.read_excel(file)
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
    mapping = pd.read_excel(joinpath(SUPPORTING_FILES_PATH, "{}_mappings.xlsx").format(supplier_code.lower()))[["編號", "Item Code"]]
    
    # Filter mapping where Item Code is not missing
    mapping = mapping[mapping['Item Code'].notna()]
    mapping['Item Code'] = mapping["Item Code"].astype(str)
    
    # Rename Item Code column
    mapping.rename(columns={"Item Code": "產品型號"}, inplace=True)

    # Left join with mapping
    df = df.merge(mapping, on='編號', how='left')

    # Map manufacturers using company_name_map
    df['製造商'] = df['編號'].apply(lambda x: company_name_map[x[:3]])

    # Remove leading zeros from 金卡編號
    df['金卡編號'] = df['金卡編號'].apply(remove_zeros)
    
    # Replace "/" with "-" in 手術日期 and convert to datetime format
    # df['手術日期'] = pd.to_datetime(df['手術日期'].str.replace('/', '-'), format='%Y-%m-%d')
    df['手術日期'] = pd.to_datetime(df['手術日期'].str.replace('/', '-'))

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
