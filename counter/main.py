import flet as ft

def main(page: ft.Page):
    page.title = "Flet counter example"
    # ページのコンポーネント配置方法を指定
    page.vertical_alignment = ft.MainAxisAlignment.CENTER

    # ページに値が0で横幅が100pxのテキストフィールドを追加
    txt_number = ft.TextField(value="0", text_align=ft.TextAlign.RIGHT, width=100)

    # マイナスボタンがクリックされたときの処理
    def minus_click(e):
        txt_number.value = str(int(txt_number.value) - 1)
        page.update()

    # プラスボタンがクリックされたときの処理
    def plus_click(e):
        txt_number.value = str(int(txt_number.value) + 1)
        page.update()

    page.add(
        ft.Row(
            [
                ft.IconButton(ft.icons.REMOVE, on_click=minus_click),
                txt_number,
                ft.IconButton(ft.icons.ADD, on_click=plus_click),
            ],
            alignment=ft.MainAxisAlignment.CENTER,
        )
    )

ft.app(main)