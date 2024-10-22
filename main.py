from settings import iCLOUD_REPORTING_PATH
from reportings import medtronic
from os.path import join as joinpath
df = medtronic.dms_report_with_offset()

df.to_excel(joinpath(iCLOUD_REPORTING_PATH, 'Medtronic DMS Report', "dms_report_with_offset.xlsx"), index=False)
# print(df)

# sys.path.append("utils")
# from viz import chart

# chart.spell()


    # df = pd.read_html(response.content, header=0, dtype_backend="pyarrow")[0]
    
    # print(f"Saving {company_code}'s items...................",end="")
    # df.to_pickle(os.pajoinpath(RAW_ITEMS_PATH, "{}_items.pickle".format(company_code)))
    # print("Done")