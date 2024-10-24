import flet as ft
from gen_report_chcsj import run as generate_report_for_chcsj
from gen_report_dms import run as genearte_report_for_dms

import subprocess

def main(page: ft.Page):
    page.title = "Flet counter example"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER

    txt_number = ft.TextField(value="0", text_align=ft.TextAlign.RIGHT, width=100)

    def gen_report_dms(e):
        genearte_report_for_dms()
        subprocess.Popen(r'explorer /select, "C:\Users\Paco\iCloudDrive\Documents\2 Areas\__FCC__Reportings\Medtronic DMS Report\dms_report_with_offset.xlsx"')
        page.update()
    
    def gen_report_chcsj(e):
        generate_report_for_chcsj()
        subprocess.Popen(r'explorer /select, "G:\My Drive\Surgical\2 Areas\Reportings\CHCSJ Ortho Case Report.xlsx"')
        page.update()

    page.add(
        ft.Row(
            [
                ft.TextButton("CHCSJ Ortho Case Report", on_click=gen_report_chcsj),
                ft.TextButton("Medtronic DMS Report", on_click=gen_report_dms),
            ],
            alignment=ft.MainAxisAlignment.CENTER,
        )
    )

ft.app(main)