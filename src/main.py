import flet as ft

from vat_statement_reader import get_vat_tables, get_company, get_credit_data


def main(page: ft.Page) -> None:
    page.title = "Statement reader"


    files = []


    async def pick_files(e):
        file_picker = ft.FilePicker()
        files_list = await file_picker.pick_files(
            allow_multiple=True,
            file_type=ft.FilePickerFileType.CUSTOM,
            allowed_extensions=['pdf'])
        total_revenue = 0
        for file in files_list:
            revenue = get_credit_data(get_vat_tables(file.path))["Revenue"]
            total_revenue += revenue
        files_list_view.controls.append(ft.Text(f"{total_revenue: ,.2f}"))
        page.update()
        
    files_list_view = ft.ListView(
        
    )

    file_picker_btn = ft.Button(
        "Pick files",
        icon=ft.Icons.FILE_UPLOAD_ROUNDED,
        on_click=pick_files,
    )

    page.add(file_picker_btn, files_list_view)




ft.run(main)