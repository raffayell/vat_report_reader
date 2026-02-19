import flet as ft

from vat_statement_reader import (
    get_vat_tables,
    get_company,
    get_credit_data,
    get_period,
)


def main(page: ft.Page) -> None:
    page.title = "Statement reader"
    page.horizontal_alignment = ft.MainAxisAlignment.CENTER
    page.window.width = 800
    page.scroll = ft.ScrollMode.ALWAYS

    files = []

    async def pick_files(e):
        file_picker = ft.FilePicker()
        page.controls.append(progress)
        files_list = await file_picker.pick_files(
            allow_multiple=True,
            file_type=ft.FilePickerFileType.CUSTOM,
            allowed_extensions=["pdf"],
        )

        total_revenue = 0
        for file in files_list:
            tables = get_vat_tables(file.path)
            company = get_company(tables)
            period = get_period(tables)
            revenue = get_credit_data(tables)["Revenue"]
            files_list_view.controls.append(
                ft.ListTile(
                    width=400,
                    leading=ft.Icon(ft.Icons.DASHBOARD_CUSTOMIZE_OUTLINED),
                    title=company["Company"],
                    subtitle=ft.Text(f"{period["Year"]} - {period["Month"]}"),
                    trailing=ft.Text(f"{revenue: ,.2f}", size=20, selectable=True),
                    bgcolor=ft.Colors.SURFACE_CONTAINER_LOW,
                ),
            )
            page.update()
            total_revenue += revenue
        files_list_view.controls.append(ft.Divider())
        files_list_view.controls.append(
            ft.Container(
                ft.Text(
                    f"{total_revenue: ,.2f}",
                    size=20,
                    weight=ft.FontWeight.BOLD,
                    text_align=ft.TextAlign.END,
                    margin=ft.Margin.only(right=12),
                    selectable=True,
                ),
                margin=ft.Margin.only(right=12),
            )
        )
        page.controls.remove(progress)
        page.update()

    files_list_view = ft.ListView(
        width=600,
        spacing=3,
        auto_scroll=True,
    )
    progress = ft.ProgressBar()

    file_picker_btn = ft.Button(
        "Pick files",
        icon=ft.Icons.FILE_UPLOAD_ROUNDED,
        on_click=pick_files,
    )

    page.add(file_picker_btn, files_list_view)


ft.run(main)
