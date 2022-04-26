from ctypes import util
import utils
import pandas as pd

if __name__ == "__main__":
    file = './uploads/data.xlsx'
    data = utils.import_1c(file)
    """
    file = './uploads/data.xlsx'
    df = pd.read_excel(file)

    df_list =[]
    for col in df :
        df_list.append(df[col].to_list())
    df_list = list(map(list, zip(*df_list)))

    df = list(df.columns.values)
    print(df)

    print(file)
    #app = App()
    #app.mainloop()

    """