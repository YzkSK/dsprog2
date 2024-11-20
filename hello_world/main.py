import flet as ft


def main(page: ft.Page):
    # titleメゾットでページタイトルを設定
    page.title = "Hello Flet"
    # addメゾットでページに要素を追加
    page.add(ft.SafeArea(ft.Text("Hello, Flet!")))
    page.add(ft.SafeArea(ft.Text("Hello, Flet!")))
    page.add(ft.SafeArea(ft.Text("Hello, Flet!")))

    # FilledButtonでボタンを作成
    page.add(ft.FilledButton("Click me"))


ft.app(main)
