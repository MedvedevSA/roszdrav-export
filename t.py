import pandas as pd

if __name__ == "__main__":
    file = './uploads/data.xlsx'
    df = pd.read_excel(file)
    c = [c for c in df]
    df_list =[]
    for col in df :

    df = list(df.columns.values)
    print(df)

    print(file)
    #app = App()
    #app.mainloop()