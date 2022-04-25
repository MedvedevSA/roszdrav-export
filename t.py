import tkinter as tk
import tkinter.filedialog as fd


if __name__ == "__main__":

    root = tk.Tk()
    root.withdraw()
    file = fd.askopenfilename(title="Выбрать файл", initialdir="/", filetypes=[('CSV','*.csv')])
    print(file)
    #app = App()
    #app.mainloop()