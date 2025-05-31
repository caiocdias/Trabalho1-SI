import pandas as pd
import os

def processar_dados_aula_v1(dados_aula_v1: pd.DataFrame) -> pd.DataFrame:
    """
    Recebe o DataFrame original (df lido de dadosAulav1.csv) e retorna um DataFrame
    em que todos os atributos são numéricos e normalizados em [0,1], conforme instruções:
      - Atributos nominais (Nome, Doença) → dummy encoding;
      - Atributos ordinais (Pressão) → mapeamento direto para números inteiros que
        representem a ordem (Baixa=0, Boa=1, Alta=2);
      - Binário nominal Mancha (“Sim”/“Não”) → 1/0;
      - Data de Nascimento → convertido para datetime e, depois, para ordinal (int);
      - ID, Idade, Febre mantidos como numéricos;
      - “Doença” vazia preenchida com “Saudável” antes de dummificar;
      - Linhas com qualquer outro valor faltante são descartadas;
      - Todos os campos (após codificação) são normalizados via min–max para o intervalo [0,1].
    """
    df = dados_aula_v1.copy()

    # 1) Preencher 'Doença' vazia como "Saudável"
    df['Doença'] = df['Doença'].fillna('Saudável')

    # 2) Padronizar / codificar 'Mancha' em 1/0
    #    → Variações de texto ("Sim", "SIM", "S", "sim" etc) devem ser mapeadas para 1
    #      e ("Não", "NÃO", "N", "nao" etc) para 0.
    #    Para simplificar, convertemos tudo para maiúsculas e usamos startswith('S') ou ('N').
    df['Mancha'] = df['Mancha'].astype(str).str.strip().str.upper()
    # Se for algo como 'SIM' ou 'S', mapeamos para 1; se for 'NÃO' ou 'N', mapeamos para 0.
    df['Mancha'] = df['Mancha'].map(lambda x: 1 if x.startswith('S') else (0 if x.startswith('N') else pd.NA))

    # 3) Codificar 'Pressão' (Baixa < Boa < Alta) como ordinal numérico 0, 1, 2
    df['Pressão'] = df['Pressão'].astype(str).str.strip().str.capitalize()
    mapeamento_pressao = {'Baixa': 0, 'Boa': 1, 'Alta': 2}
    df['Pressão'] = df['Pressão'].map(mapeamento_pressao)

    # 4) Converter "Data de Nascimento" para datetime e depois para inteiro ordinal
    #    (número de dias desde o ano 1). Se falhar a conversão, ficará NaT e a linha será descartada.
    df['Data de Nascimento'] = pd.to_datetime(
        df['Data de Nascimento'],
        format='%d/%m/%Y',
        dayfirst=True,
        errors='coerce'
    )
    # Transformar em número (ordinal)
    df['Data de Nascimento'] = df['Data de Nascimento'].map(lambda d: d.toordinal() if pd.notna(d) else pd.NA)

    # 5) Tratar vazios em colunas numéricas e ordinais: descartar linhas que ainda estejam com NA
    #    (já preenchemos "Doença", mas Idade, Febre, Mancha, Pressão e Data podem ter NA)
    colunas_obrigatorias = ['ID', 'Nome', 'Idade', 'Data de Nascimento', 'Mancha', 'Febre', 'Pressão', 'Doença']
    df = df.dropna(subset=colunas_obrigatorias)

    # 6) Converter 'Idade' e 'Febre' para tipo numérico (já eram float), mas garantir dtype correto:
    df['Idade'] = df['Idade'].astype(float)
    df['Febre'] = df['Febre'].astype(float)

    # 7) Dummy-encoding para 'Nome' (nominal) e 'Doença' (nominal)
    #    → Cria colunas “Nome_<categoria>” e “Doenca_<categoria>” (sem acento no prefixo)
    dummies_nome    = pd.get_dummies(df['Nome'],    prefix='Nome')
    dummies_doenca  = pd.get_dummies(df['Doença'], prefix='Doenca')

    # 8) Montar novo DataFrame já sem as colunas originais 'Nome' e 'Doença'
    df_numeric = pd.concat(
        [
            df[['ID', 'Idade', 'Data de Nascimento', 'Mancha', 'Febre', 'Pressão']],
            dummies_nome,
            dummies_doenca
        ],
        axis=1
    )

    # 9) Normalizar cada coluna para [0,1] via min–max
    #    Fórmula: (x - min) / (max - min)
    df_norm = df_numeric.copy().astype(float)
    for col in df_norm.columns:
        min_val = df_norm[col].min()
        max_val = df_norm[col].max()
        # Se max == min, ficará todo zero (ou podemos deixar 0 para evitar divisão por zero)
        if max_val > min_val:
            df_norm[col] = (df_norm[col] - min_val) / (max_val - min_val)
        else:
            df_norm[col] = 0.0

    return df_norm

def processar_dados_titanic(df_titanic: pd.DataFrame) -> pd.DataFrame:
    """
    Realiza pré‐processamento do dataset Titanic:
      1) Remove colunas irrelevantes ou com alto percentual de NA: ['PassengerId', 'Name', 'Ticket', 'Cabin'].
      2) Imputa 'Age' pela mediana e preenche 'Embarked' pela moda.
      3) Transforma 'Sex' em variável binária (male=1, female=0).
      4) Cria variáveis dummy (one‐hot encoding) para 'Embarked'.
      5) Gera nova coluna 'FamilySize' = SibSp + Parch + 1.
      6) Garante que não haja valores ausentes nas colunas de interesse.
      7) Retorna DataFrame limpo, pronto para análise ou modelagem (sem normalização).
    """
    df = df_titanic.copy()

    # 1) Remover colunas com pouco valor analítico ou muitos NAs
    colunas_para_remover = ['PassengerId', 'Name', 'Ticket', 'Cabin']
    df = df.drop(columns=colunas_para_remover)

    # 2) Tratar valores ausentes em 'Age' e 'Embarked'
    #    - 'Age': imputar pela mediana
    mediana_idade = df['Age'].median()
    df['Age'] = df['Age'].fillna(mediana_idade)

    #    - 'Embarked': imputar pela moda (valor mais frequente)
    moda_embarked = df['Embarked'].mode()[0]
    df['Embarked'] = df['Embarked'].fillna(moda_embarked)

    # 3) Codificar 'Sex' em binário
    #    male → 1, female → 0
    df['Sex'] = df['Sex'].map({'male': 1, 'female': 0})

    # 4) One‐hot encoding para 'Embarked'
    #    Cria colunas: Embarked_C, Embarked_Q, Embarked_S
    dummies_embarked = pd.get_dummies(df['Embarked'], prefix='Embarked')
    df = pd.concat([df.drop(columns=['Embarked']), dummies_embarked], axis=1)

    # 5) Criar 'FamilySize' = SibSp + Parch + 1
    df['FamilySize'] = df['SibSp'] + df['Parch'] + 1

    # 6) Remover possíveis linhas restantes com NA (não deverá haver, mas por segurança)
    df = df.dropna()

    # 7) Retornar o DataFrame resultante (sem normalização)
    return df

def main():
    df_dados_aula_v1 = pd.read_csv(r"./Datasets/dadosAulav1.csv", sep=';', encoding='ISO-8859-1')
    df_titanic = pd.read_csv(r"./Datasets/titanic.csv")

    #Criando o repositório de exportação
    if not os.path.exists(r"./Exports"):
        os.mkdir(r"./Exports")

    df_dados_aula_v1 = processar_dados_aula_v1(df_dados_aula_v1)
    df_titanic = processar_dados_titanic(df_titanic)

    df_dados_aula_v1.to_excel(r"./Exports/dados_aula1.xlsx")
    df_titanic.to_excel(r"./Exports/titanic.xlsx")

if __name__ == "__main__":
    main()