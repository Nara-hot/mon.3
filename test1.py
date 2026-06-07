from datetime import datetime
import flet as ft


def main_page(page: ft.Page):
    page.theme_mode = ft.ThemeMode.LIGHT
    page.title = "Мое первое приложение"

    text_hello = ft.Text(value="Hello world")
    name_input = ft.TextField(hint_text="Введите имя")

    greeting_history = []
    favorites = []
    last_name = [None]

    history_text = ft.Text(value="История приветствий:")
    favorites_text = ft.Text(value="Любимые имена: ЗДЕСЬ ПОКА ПУСТО")

    def on_button_click(_):
        if name_input.value:
            name = name_input.value.strip()
            last_name[0] = name

            now = datetime.now()
            time_str = now.strftime("%Y:%m:%d - %H:%M:%S")

            text_hello.value = f"Hello {name}"
            name_input.value = None
            text_hello.color = None

            full_message = f"{time_str} - Привет, {name}!"
            greeting_history.append((now, full_message))

            render_history(greeting_history)
            page.update()
        else:
            text_hello.value = "Введите имя!"
            text_hello.color = ft.Colors.RED
            page.update()

    def render_history(items_list):
        if not items_list:
            history_text.value = "История приветствий пуста"
        else:
            messages = [element[1] for element in items_list]
            history_text.value = "История приветствий:\n" + "\n".join(messages)

    button_elevated = ft.ElevatedButton(
        "send", icon=ft.Icons.SEND, on_click=on_button_click
    )
    name_input.on_submit = on_button_click

    def add_to_favorites(_):
        if last_name[0] and last_name[0] not in favorites:
            favorites.append(last_name[0])
            favorites_text.value = "Любимые имена:\n" + ", ".join(favorites)
            page.update()

    fav_button = ft.IconButton(
        icon=ft.Icons.STAR_BORDER,
        icon_color=ft.Colors.AMBER,
        on_click=add_to_favorites,
    )

    def show_morning_greetings(_):
        morning_items = [item for item in greeting_history if item[0].hour < 12]
        render_history(morning_items)
        page.update()

    def show_evening_greetings(_):
        evening_items = [item for item in greeting_history if item[0].hour >= 12]
        render_history(evening_items)
        page.update()

    def show_all_greetings(_):
        render_history(greeting_history)
        page.update()

    btn_morning = ft.TextButton("Утренние (до 12:00)", on_click=show_morning_greetings)
    btn_evening = ft.TextButton("Вечерние (после 12:00)", on_click=show_evening_greetings)
    btn_all = ft.TextButton("Показать все", on_click=show_all_greetings)

    def clear_history(_):
        greeting_history.clear()
        history_text.value = "История приветствий:"
        page.update()

    clear_button = ft.IconButton(icon=ft.Icons.DELETE, on_click=clear_history)

    filters_row = ft.Row([btn_all, btn_morning, btn_evening])

    page.add(
        text_hello,
        name_input,
        ft.Row([button_elevated, fav_button, clear_button]),
        filters_row,
        favorites_text,
        ft.Divider(),
        history_text,
    )


ft.app(target=main_page)