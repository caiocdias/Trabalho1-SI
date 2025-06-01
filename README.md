# Projeto de Pré-processamento de Dados - Trabalho 1
## Alunos:

- ### Caio Cezar Dias
- ### Isabely Toledo de Melo
## Descrição do Projeto

Este repositório contém a implementação das funções de pré-processamento dos seguintes datasets:
- **dadosAulav1**: dataset didático fornecido pelo professor, no qual todos os atributos são convertidos em valores numéricos e normalizados no intervalo [0,1].
- **Titanic**: dataset do Titanic, processado de forma a tratar valores ausentes, criar novas features e codificar variáveis categóricas, sem normalização obrigatória.

O objetivo deste trabalho é demonstrar as etapas de limpeza e transformação de dados, utilizando Python e pandas.

## Estrutura de Arquivos

```
├── main.py
├── requirements.txt
├── Datasets
│   ├── dadosAulav1.csv
│   └── titanic.csv
├── Exports
│   ├── dados_aula1.xlsx
│   └── titanic.xlsx
└── README.md
```

- **main.py**: contém as funções `processar_dados_aula_v1` e `processar_dados_titanic`, além do script principal que lê os datasets, aplica o pré-processamento e exporta os resultados para a pasta `Exports`.
- **requirements.txt**: lista de dependências necessárias (pandas, openpyxl).
- **Datasets/**: pasta que armazena os arquivos de entrada (`dadosAulav1.csv` e `titanic.csv`).
- **Exports/**: pasta gerada pelo `main.py` contendo os arquivos Excel resultantes após o pré-processamento.
- **README.md**: este arquivo, que descreve o projeto e instruções de uso.

## Instruções de Instalação

1. Clone este repositório em sua máquina:
   ```bash
   git clone https://github.com/caiocdias/Trabalho1-SI
   cd Trabalho1-SI
   ```
2. Crie e ative um ambiente virtual (opcional, porém recomendado):
   ```bash
   python3 -m venv venv
   source venv/bin/activate   # Linux/macOS
   venv\Scripts\activate    # Windows
   ```
3. Instale as dependências listadas em `requirements.txt`:
   ```bash
   pip install -r requirements.txt
   ```

## Uso

Para executar o pré-processamento, basta rodar o script principal:
```bash
python main.py
```

Isso irá:
1. Ler `dadosAulav1.csv` e `titanic.csv` da pasta `Datasets/`.
2. Aplicar as funções `processar_dados_aula_v1` e `processar_dados_titanic`.
3. Criar a pasta `Exports/` (caso não exista) e salvar os arquivos processados:
   - `Exports/dados_aula1.xlsx`
   - `Exports/titanic.xlsx`

## Descrição das Funções

- **processar_dados_aula_v1(dados_aula_v1: DataFrame) -> DataFrame**  
  - Converte todos os atributos do dataset `dadosAulav1` em valores numéricos:
    - Preenche valores faltantes em “Doença” como “Saudável”.
    - Codifica “Mancha” (Sim/Não) como 1/0.
    - Mapeia “Pressão” (Baixa, Boa, Alta) para 0,1,2.
    - Converte “Data de Nascimento” para valor ordinal (número de dias).
    - Realiza dummy encoding para “Nome” e “Doença”.
    - Normaliza todas as colunas no intervalo [0,1].
  - Retorna um DataFrame totalmente numérico.

- **processar_dados_titanic(df_titanic: DataFrame) -> DataFrame**  
  - Remove colunas irrelevantes ou com alto percentual de valores faltantes (e.g., “Cabin”).
  - Imputa valores faltantes em “Age” pela mediana e em “Embarked” pela moda.
  - Codifica “Sex” como variável binária (male=1, female=0).
  - Cria dummy variables para “Embarked”.
  - Gera nova feature “FamilySize” = `SibSp + Parch + 1`.
  - Remove linhas restantes com valores faltantes.
  - Retorna um DataFrame pronto para análise.

## Considerações Finais

- O arquivo de saída para `dadosAulav1` é um Excel com todos os atributos numéricos e normalizados.
- O arquivo de saída para o dataset Titanic é um Excel limpo, sem normalização, pronto para análises exploratórias ou modelos preditivos.
- Sinta-se à vontade para explorar o código, adaptar ou estender as funções de pré-processamento conforme necessário.
