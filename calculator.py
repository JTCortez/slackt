from tkinter import *
from tkinter import messagebox
from ExpressionCalculation import ExpCalc


def buildButton(src, txt, cmd, row, col, rowspan, colspan):
    button = Button(src, text=txt, command=cmd, height=1, width=5*colspan)
    button.grid(row=row, column=col, rowspan=rowspan, columnspan=colspan)


class Window(Frame):
    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.master = master
        self.res, self.dec = None, 0

        # creating text field
        self.textField = Text(master, bg="#FFFFFF", fg="#000000", height=1, width=20)
        self.textField.insert(INSERT, "0")
        self.textField.grid(row=0, columnspan=4)

        # create calculator buttons
        # first row
        # 'clear', '^', 'sqrt', 'del' buttons
        buildButton(master, 'Clear', lambda: self.clear(), 1, 0, 1, 1)
        buildButton(master, '^', lambda: self.notice('^'), 1, 1, 1, 1)
        buildButton(master, 'root', lambda: self.notice("root"), 1, 2, 1, 1)
        buildButton(master, 'Del', lambda: self.delete(), 1, 3, 1, 1)
        # second row (sin, cos, tan, +)
        buildButton(master, 'sin', lambda: self.notice('sin('), 2, 0, 1, 1)
        buildButton(master, 'cos', lambda: self.notice('cos('), 2, 1, 1, 1)
        buildButton(master, 'tan', lambda: self.notice('tan('), 2, 2, 1, 1)
        buildButton(master, '+', lambda: self.notice('+'), 2, 3, 1, 1)
        # third row (7, 8, 9, -)
        buildButton(master, '7', lambda: self.notice('7'), 3, 0, 1, 1)
        buildButton(master, '8', lambda: self.notice('8'), 3, 1, 1, 1)
        buildButton(master, '9', lambda: self.notice('9'), 3, 2, 1, 1)
        buildButton(master, '-', lambda: self.notice('-'), 3, 3, 1, 1)
        # fourth row (4, 5, 6, *)
        buildButton(master, '4', lambda: self.notice('4'), 4, 0, 1, 1)
        buildButton(master, '5', lambda: self.notice('5'), 4, 1, 1, 1)
        buildButton(master, '6', lambda: self.notice('6'), 4, 2, 1, 1)
        buildButton(master, '*', lambda: self.notice('*'), 4, 3, 1, 1)
        # fifth row (7, 8, 9, -)
        buildButton(master, '1', lambda: self.notice('1'), 5, 0, 1, 1)
        buildButton(master, '2', lambda: self.notice('2'), 5, 1, 1, 1)
        buildButton(master, '3', lambda: self.notice('3'), 5, 2, 1, 1)
        buildButton(master, '/', lambda: self.notice('/'), 5, 3, 1, 1)
        # sixth row (0, (, ), .)
        buildButton(master, '0', lambda: self.notice('0'), 6, 0, 1, 1)
        buildButton(master, '(', lambda: self.notice('('), 6, 1, 1, 1)
        buildButton(master, ')', lambda: self.notice(')'), 6, 2, 1, 1)
        buildButton(master, '%', lambda: self.notice('%'), 6, 3, 1, 1)

        # last row ('dec', '.', =)
        buildButton(master, '0/4dec', lambda: self.decimal(), 7, 0, 1, 1)
        buildButton(master, '.', lambda: self.notice('.'), 7, 1, 1, 1)
        buildButton(master, '=', lambda: self.displayRes(None), 7, 2, 1, 2)

        self.textField.bind('<KeyRelease-Return>', self.displayRes)

    # function to notice click on button and display on calc
    def notice(self, symbol):
        if self.textField.get("0.0", END) == "0\n":
            self.textField.delete("0.0", END)
        self.textField.insert(INSERT, str(symbol))

    # function to clear calc
    def clear(self):
        self.textField.delete("0.0", END)
        self.textField.insert(INSERT, "0")

    # delete last char
    def delete(self):
        expr = self.textField.get("0.0", END)
        self.clear()
        if len(expr) <= 2:
            self.clear()
            return

        if expr[-2].isalpha():
            for i in range(len(expr)-3, -1, -1):
                if not expr[i].isalpha():
                    self.notice(expr[:i+1])
                    break
        else:
            self.notice(expr[:-2])

    # toggle decimal place
    def decimal(self):
        if self.res is None:
            return
        self.dec ^= 1
        if not self.dec:
            r = "%.0f" % round(self.res)
        else:
            r = "%.4f" % round(self.res, 4)
        self.clear()
        self.notice(r)

    # function to display result after '=' is register
    def displayRes(self, event):
        self.res = self.calculate(self.textField.get("0.0", END)[:-1])
        if isinstance(self.res, str):
            messagebox.showerror("Error", self.res)
            self.clear()
        else:
            self.textField.delete("0.0", END)
            self.textField.insert(INSERT, self.res)
            if event is not None:
                self.textField.see("0.0")

    # calculate using ExpCalc class
    def calculate(self, expr):
        return ExpCalc(expr).calculate()


if __name__ == "__main__":
    root = Tk()
    calc = Window(root)
    root.wm_title("Calculator")
    root.mainloop()
