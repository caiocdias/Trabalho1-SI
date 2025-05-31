import pandas as pd
import os

def main():
    df_dados_aula_v1 = pd.read_csv(r"./Datasets/dadosAulav1.csv", sep=';', encoding='ISO-8859-1')
    df_titanic = pd.read_csv(r"./Datasets/titanic.csv")

    #Criando o repositório de exportação
    if not os.path.exists(r"./Exports"):
        os.mkdir(r"./Exports")

    df_dados_aula_v1.to_excel(r"./Exports/dados_aula1.xlsx")
    df_titanic.to_excel(r"./Exports/titanic.xlsx")

if __name__ == "__main__":
    main()