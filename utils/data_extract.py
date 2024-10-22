import requests
from bs4 import BeautifulSoup
import pandas as pd

from .connections import has_permission, login, SESSION

#### Sales orders
#tender_sap_item
def sap_tender_nos(company_code):
    url = "http://fcc/fcc/Tender_v3/tender_sap_item_search.php"
    not has_permission(url) and login()

    data = {"sap_item_code_from" : f"{company_code}1",
        "sap_item_code_to" : f"{company_code}z",
        "submit" : "Search"}

    response = SESSION.post(url, data=data)
    soup = BeautifulSoup(response.content, 'html.parser')
    tables = soup.find_all("table")
    trs = tables[0].find_all('tr')

    sales_orders_nos = []
    for i in range(4,len(trs)-1):
        so = trs[i].find_all("td")[0].get_text().strip()
        if so != '':
            sales_orders_nos.append(so)
    return list(set(sales_orders_nos))

def search_tender(tender_no:str) -> pd.DataFrame:
    url = "http://fcc/fcc/Tender_v2/tender.php"
    not has_permission(url) and login()

    # form data
    data = {"submit" : "SAP+計算數量及差異",
            "act":"load",
            "company": "FCC",
            "action": "sum_qty"}
    data["tender_no"] = tender_no
    
    # request
    response = SESSION.post(url, data=data)
    
    # parseing
    soup = BeautifulSoup(response.content, "lxml")

    table = soup.find_all('table')[0]
    trs = table.find_all('tr')

    # soup into df
    data = []
    for tr in trs:
        if len(list(tr.children)) > 20:
            rows = []
            if len(tr.find_all('td')) != 20:
                continue
            tds = tr.find_all('td')
            for td in tds:
                rows.append(td.get_text().strip())
            data.append(rows)

    tableHeaders = ["序號", "物品編號","SAP Item Code","要求供貨","Missing1","物品名稱","單位", "Missing2","商業名稱",
                    "牌子","型號","生產商","原產地","單價","包","裝","已供","Status","相差","Missing3"]
    df = pd.DataFrame(data= data, columns= tableHeaders)
    return df


def doc_check(so_num):
    url = "http://fcc/fcc/doc_info/doc_info.php"
    
    # Assuming has_permission and login are defined elsewhere
    not has_permission(url) and login()

    response = SESSION.post(url, data={'doc_num': so_num})

    # Parse the HTML response
    doc = BeautifulSoup(response.content.decode('utf-8', 'ignore'), "html.parser")
    table = doc.select_one('table[bgcolor="#CCCCCC"]')

    headers_tr = table.select_one('tr[bgcolor="#DDDDDD"]')
    headers = [td.get_text() for td in headers_tr.find_all('td')]
    
    df = pd.DataFrame(columns=headers)

    trs = table.select('tr[onmouseover="OMOver(this);"]')
    for tr in trs:
        row = []
        tds = tr.find_all('td')
        for td in tds:
            if td.get_text() == "":
                continue
            row.append(td.get_text())
        df.loc[len(df)] = row  # Append the row to the DataFrame

    return df