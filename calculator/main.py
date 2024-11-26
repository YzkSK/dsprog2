import flet as ft
import math
import random

# ボタンクラスを定義
class calcButton(ft.ElevatedButton):
    def __init__(self, text, button_clicked, expand=1):
        super().__init__()
        self.text = text
        self.expand = expand
        self.on_click = button_clicked
        self.data = text
        self.shape=ft.RoundedRectangleBorder(radius=10),

# ボタンクラスを継承した数字ボタンクラスを定義
class digitButton(calcButton):
    def __init__(self, text, button_clicked, expand=1):
        calcButton.__init__(self, text, button_clicked, expand)
        self.bgcolor = ft.colors.WHITE24
        self.color = ft.colors.WHITE

# ボタンクラスを継承したアクションボタンクラスを定義
class actionButton(calcButton):
    def __init__(self, text, button_clicked):
        calcButton.__init__(self, text, button_clicked)
        self.bgcolor = ft.colors.GREY_500
        self.color = ft.colors.BLACK

# アプリケーションクラスを定義
class app(ft.Container):
    def __init__(self):
        super().__init__()
        # calcは計算式を表示するテキスト
        self.debug = ft.Text(value="", color=ft.colors.GREY_700, size=15)
        self.calc = ft.Text(value="", color=ft.colors.GREY_700, size=20)
        # resultは計算結果を表示するテキスト
        self.result = ft.Text(value="0", color=ft.colors.WHITE, size=40)
        # 計算の状態を管理する変数
        self.math_entered = False
        self.num_entered = False
        # 計算式を一時的に保存する変数
        self.temp_num = ""
        self.temp = ""
        self.calc_result = ""

        self.width = 400
        self.height = 450
        self.bgcolor = ft.colors.BLACK
        self.border_radius = ft.border_radius.all(15)
        self.padding = 15
        self.content = ft.Column(
            controls=[
                ft.Row(
                    controls=[
                        self.debug,
                        self.calc
                        ],
                    alignment="end"),
                ft.Row(controls=[self.result], alignment="end"),
                ft.Row(
                    controls=[
                        actionButton(
                            text="x^y", button_clicked=self.button_clicked
                        ),
                        actionButton(
                            text="π", button_clicked=self.button_clicked
                        ),
                        actionButton(
                            text="log10", button_clicked=self.button_clicked
                        ),
                    ]
                ),
                ft.Row(
                    controls=[
                        actionButton(
                            text="√", button_clicked=self.button_clicked
                        ),
                        actionButton(
                            text="n!", button_clicked=self.button_clicked
                        ),
                        actionButton(
                            text="(", button_clicked=self.button_clicked
                        ),
                        actionButton(
                            text=")", button_clicked=self.button_clicked
                        ),
                    ]
                ),
                ft.Row(
                    controls=[
                        actionButton(
                            text="AC", button_clicked=self.button_clicked
                        ),
                        actionButton(
                            text="+/-", button_clicked=self.button_clicked
                        ),
                        actionButton(
                            text="%", button_clicked=self.button_clicked
                        ),
                        actionButton(
                            text="÷", button_clicked=self.button_clicked
                        ),
                    ]
                ),
                ft.Row(
                    controls=[
                        digitButton(
                            text="7", button_clicked=self.button_clicked
                        ),
                        digitButton(
                            text="8", button_clicked=self.button_clicked
                        ),
                        digitButton(
                            text="9", button_clicked=self.button_clicked
                        ),
                        actionButton(
                            text="×", button_clicked=self.button_clicked
                        ),
                    ]
                ),
                ft.Row(
                    controls=[
                        digitButton(
                            text="4", button_clicked=self.button_clicked
                        ),
                        digitButton(
                            text="5", button_clicked=self.button_clicked
                        ),
                        digitButton(
                            text="6", button_clicked=self.button_clicked
                        ),
                        actionButton(
                            text="-", button_clicked=self.button_clicked
                        ),
                    ]
                ),
                ft.Row(
                    controls=[
                        digitButton(
                            text="1", button_clicked=self.button_clicked
                        ),
                        digitButton(
                            text="2", button_clicked=self.button_clicked
                        ),
                        digitButton(
                            text="3", button_clicked=self.button_clicked
                        ),
                        actionButton(
                            text="+", button_clicked=self.button_clicked
                        ),
                    ]
                ),
                ft.Row(
                    controls=[
                        digitButton(
                            text="0", expand=2, button_clicked=self.button_clicked
                        ),
                        digitButton(
                            text=".", button_clicked=self.button_clicked
                        ),
                        actionButton(
                            text="=", button_clicked=self.button_clicked
                        ),
                    ]
                ),

                #デバッグ用ボタン

                ft.Row(
                    controls=[
                        actionButton(
                            text="result", button_clicked=self.button_clicked
                        ),
                        actionButton(
                            text="temp", button_clicked=self.button_clicked
                        ),
                    ]
                )
            ]
        )

    def button_clicked(self, e):
        data = e.control.data
        print(data)
        print(self.num_entered)
        if self.result.value == "Error" or data == "AC":
            self.result.value = "0"
            self.calc.value = ""
            self.calc_result = ""
            self.result_val = ""
            self.math_entered = False
            self.num_entered = False
            self.log_entered = False
            self.rand_entered = False
            self.temp_num = ""
            self.temp = ""

        elif data in "result":
            self.debug.value = self.calc_result

        elif data in "temp":
            self.calc.value = self.temp_num

        elif data in ("1","2","3","4","5","6","7","8","9","0",".","+","-","×","÷","x^y","√","(",")","n!","π","log10"):
            if self.result.value == "0":
                if data in ("1","2","3","4","5","6","7","8","9","0"):
                    self.temp_num = data
                    self.result.value = data
                    self.calc_result += data
                    self.num_entered = True
                    self.rand_entered = False
                    print(f"変更 : {self.num_entered}")
                elif data in ("×"):
                    self.calc_result = "*"
                    self.num_entered = False
                    self.rand_entered = False
                elif data in ("÷"):
                    self.calc_result = "/"
                    self.num_entered = False
                    self.rand_entered = False
                elif data in ("x^y"):
                    self.calc_result = "**"
                    self.num_entered = False
                    self.rand_entered = False
                elif data in "n!":
                    self.result.value = "Error"
                    self.math_entered = True
                    self.num_entered = False
                    self.rand_entered = False
                    self.rand_entered = False
                elif data in ("√"):
                    self.calc_result = "math.sqrt("
                    self.result.value = "√"
                    self.math_entered = True
                    self.num_entered = False
                    self.rand_entered = False
                    print(self.math_entered)
                elif data in ("π"):
                    self.calc_result = "math.pi"
                    self.result.value = "π"
                    self.num_entered = True
                    self.rand_entered = False
                    print(self.math_entered)
                elif data in ("log10"):
                    self.calc_result = "math.log10("
                    self.result.value = "log10("
                    self.math_entered = True
                    self.log_entered = True
                    self.num_entered = False
                    self.rand_entered = False
                    print(self.math_entered)
                else:
                    self.calc_result = data
                    self.result.value = data
                    self.num_entered = True
            else:
                if data in ("1","2","3","4","5","6","7","8","9","0"):
                    self.temp_num += data
                    self.result.value += data
                    self.calc_result += data
                    self.num_entered = True
                elif data in ("+"):
                    if self.math_entered == True:
                        self.calc_result += ")+"
                        if self.log_entered == True:
                            self.result.value += ")+"
                            self.log_entered = False
                        else:
                            self.result.value += "+"
                        self.math_entered = False
                        self.num_entered = False
                        self.rand_entered = False
                        self.temp_num = ""
                    else:
                        self.calc_result += "+"
                        self.result.value += "+"
                        self.num_entered = False
                        self.rand_entered = False
                        self.temp_num = ""
                elif data in ("-"):
                    if self.math_entered:
                        self.calc_result += ")-"
                        if self.log_entered == True:
                            self.result.value += ")-"
                            self.log_entered = False
                        else:
                            self.result.value += "-"
                        self.num_entered = False
                        self.math_entered = False
                        self.rand_entered = False
                        self.temp_num = ""
                    else:
                        self.calc_result += "-"
                        self.result.value += "-"
                        self.num_entered = False
                        self.rand_entered = False
                        self.temp_num = ""
                elif data in ("×"):
                    if self.math_entered:
                        self.calc_result += ")*"
                        if self.log_entered == True:
                            self.result.value += ")×"
                            self.log_entered = False
                        else:
                            self.result.value += "×"
                        self.math_entered = False
                        self.num_entered = False
                        self.rand_entered = False
                        self.temp_num = ""
                    else:
                        self.calc_result += "*"
                        self.result.value += "×"
                        self.num_entered = False
                        self.rand_entered = False
                        self.temp_num = ""
                elif data in ("÷"):
                    if self.math_entered:
                        self.calc_result += ")/"
                        if self.log_entered == True:
                            self.result.value += ")÷"
                            self.log_entered = False
                        else:
                            self.result.value += "÷"
                        self.math_entered = False
                        self.num_entered = False
                        self.rand_entered = False
                        self.temp_num = ""
                    else:
                        self.calc_result += "/"
                        self.result.value += "÷"
                        self.num_entered = False
                        self.rand_entered = False
                        self.temp_num = ""
                elif data in ("x^y"):
                    if self.math_entered:
                        self.calc_result += ")**"
                        if self.log_entered == True:
                            self.result.value += ")^"
                            self.log_entered = False
                        else:
                            self.result.value += "^"
                        self.math_entered = False
                        self.num_entered = False
                        self.rand_entered = False
                        self.temp_num
                    else:
                        self.calc_result += "**"
                        self.result.value += "^"
                        self.num_entered = False
                        self.rand_entered = False
                        self.temp_num = ""
                elif data in ("n!"):
                    self.temp = self.temp_num
                    self.temp_num = ""
                    self.temp_num = "math.factorial(" + self.temp
                    self.calc_result = self.calc_result.replace(self.temp, "")
                    self.calc_result += self.temp_num
                    self.result.value += "!"
                    self.math_entered = True
                    self.num_entered = False
                    self.rand_entered = False
                elif data in (")"):
                    self.calc_result += ")"
                    self.result.value += ")"
                    self.math_entered = False
                    self.log_entered = False
                    self.num_entered = False
                    self.rand_entered = False
                elif data in ("√"):
                    if self.num_entered:
                        self.calc_result += "*math.sqrt("
                        self.result.value += "√"
                    else:
                        self.calc_result += "math.sqrt("
                        self.result.value += "√"
                    self.math_entered = True
                    self.num_entered = False
                    self.rand_entered = False
                elif data in ("π"):
                    if self.num_entered:
                        self.calc_result += "*math.pi"
                        self.result.value += "π"
                    else:
                        self.calc_result += "math.pi"
                        self.result.value += "π"
                    self.num_entered = False
                    self.rand_entered = False
                elif data in ("log10"):
                    if self.num_entered:
                        self.calc_result += "*math.log10("
                        self.result.value += "log10("
                    else:
                        self.calc_result += "math.log10("
                        self.result.value += "log10("
                    self.math_entered = True
                    self.log_entered = True
                    self.rand_entered = False
                    self.num_entered = False
                else:
                    self.calc_result += data
                    self.result.value += data
                    self.num_entered = True

        elif data in "=":
            if self.math_entered:
                if self.log_entered:
                    self.calc_result += ")"
                    self.result.value += ")"
                else:
                    self.calc_result += ")"
                self.math_entered = False
                self.log_entered = False
            self.calc.value = self.result.value
            self.temp = self.calculate(self.calc_result)
            if self.temp == "Error":
                self.result.value = self.temp
            else:
                if self.temp.is_integer():
                    self.result.value = str(int(self.temp))
                else:
                    self.result.value = str(self.temp)

        elif data in "%":
            self.result.value = str(float(self.result.value) / 100)

        elif data in "+/-":
            self.result_val = str(self.result.value)
            self.temp_num = str(self.temp_num)
            self.calc_result = str(self.calc_result)
            self.temp = str(self.temp)
            self.temp = self.temp_num
            if self.temp_num == 0 and self.temp_num == None:
                self.result_val = "0"
                self.result.value = self.result_val
            elif float(self.temp_num) > 0:
                self.temp_num = "-" + self.temp_num
                self.result_val = self.result_val[::-1]
                self.calc_result = self.calc_result[::-1]
                self.temp = self.temp[::-1]
                self.temp_num = self.temp_num[::-1]
                print(self.temp)
                print(self.temp_num)
                print(self.result_val)
                print(self.calc_result)
                self.result_val = self.result_val.replace(self.temp, self.temp_num, 1)
                self.result_val = self.result_val[::-1]
                self.calc_result = self.calc_result.replace(self.temp, self.temp_num, 1)
                self.calc_result = self.calc_result[::-1]
                self.temp_num = self.temp_num[::-1]
                self.temp = self.temp[::-1]
                self.result.value = self.result_val
            elif float(self.temp_num) < 0:
                self.temp_num = str(abs(int(self.temp_num)))
                self.result_val = self.result_val[::-1]
                self.calc_result = self.calc_result[::-1]
                self.temp = self.temp[::-1]
                self.temp_num = self.temp_num[::-1]
                self.result_val = self.result_val.replace(self.temp, self.temp_num, 1)
                self.result_val = self.result_val[::-1]
                self.calc_result = self.calc_result.replace(self.temp, self.temp_num, 1)
                self.calc_result = self.calc_result[::-1]
                self.temp_num = self.temp_num[::-1]
                self.temp = self.temp[::-1]
                self.result.value = self.result_val

        self.update()

    def calculate(self, calc):
        try:
            return float(eval(str(calc)))
        except:
            return "Error"

def main(page: ft.Page):
    page.title = "Calculator App"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    calc = app()
    page.add(calc)


ft.app(main)
