
import flet as ft
from config import APP_TITLE, WINDOW_WIDTH, WINDOW_HEIGHT, PRIMARY_COLOR
from db.main_db import init_db
from db.queries import add_item, get_all_items, get_bought_items, get_not_bought_items, toggle_bought, delete_item, get_bought_count

def main(page: ft.Page):
    page.title = APP_TITLE
    page.window.width = WINDOW_WIDTH
    page.window.height = WINDOW_HEIGHT
    page.padding = 20
    page.theme_mode = ft.ThemeMode.LIGHT
    init_db()

    new_item = ft.TextField(label="Название товара", hint_text="Например: Молоко", expand=True, border_radius=8, on_submit=lambda e: add_click(e))
    quantity_field = ft.TextField(label="Количество", hint_text="Например: 2", width=150, border_radius=8, value="")

    items_list = ft.ListView(expand=True, spacing=8)
    counter = ft.Text(size=16, weight=ft.FontWeight.BOLD)
    current_filter = 0

    def update_list():
        items_list.controls.clear()
        if current_filter == 0:
            items = get_all_items()
        elif current_filter == 1:
            items = get_not_bought_items()
        else:
            items = get_bought_items()

        for item in items:
            item_id = item["id"]
            qty = f" ({item['quantity']})" if item.get('quantity') and item['quantity'].strip() else ""
            checkbox = ft.Checkbox(label=f"{item['name']}{qty}", value=bool(item['is_bought']), on_change=lambda e, iid=item_id: toggle_item(e, iid))
            delete_btn = ft.IconButton(icon=ft.Icons.DELETE, icon_color="red400", on_click=lambda e, iid=item_id: delete_item_click(iid))
            row = ft.Row(controls=[checkbox, delete_btn], alignment=ft.MainAxisAlignment.SPACE_BETWEEN)
            items_list.controls.append(row)

        bought = get_bought_count()
        total = len(get_all_items())
        counter.value = f"Куплено: {bought} из {total}"
        page.update()

    def toggle_item(e, item_id):
        toggle_bought(item_id, e.control.value)
        update_list()

    def delete_item_click(item_id):
        delete_item(item_id)
        update_list()

    def add_click(e):
        if new_item.value and new_item.value.strip():
            add_item(new_item.value.strip(), quantity_field.value or "")
            new_item.value = ""
            quantity_field.value = ""
            update_list()

    def filter_all(e):
        nonlocal current_filter
        current_filter = 0
        update_list()

    def filter_not_bought(e):
        nonlocal current_filter
        current_filter = 1
        update_list()

    def filter_bought(e):
        nonlocal current_filter
        current_filter = 2
        update_list()

    filter_row = ft.Row(controls=[
        ft.ElevatedButton("Все", on_click=filter_all),
        ft.ElevatedButton("Не куплено", on_click=filter_not_bought),
        ft.ElevatedButton("Куплено", on_click=filter_bought),
    ], alignment=ft.MainAxisAlignment.CENTER, spacing=8)

    add_button = ft.FloatingActionButton(icon=ft.Icons.ADD, bgcolor=PRIMARY_COLOR, on_click=add_click)

    page.add(
        ft.Text(APP_TITLE, size=28, weight=ft.FontWeight.BOLD),
        ft.Row([new_item, quantity_field]),
        filter_row,
        items_list,
        counter
    )
    page.floating_action_button = add_button
    update_list()

ft.app(target=main)