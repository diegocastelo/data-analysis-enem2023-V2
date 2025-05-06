import pandas as pd


def show_basic_information(df: pd.DataFrame):
    print(f'Registros: {len(df)}\nVariáveis: {len(df.columns)}')

    print(df.head())

    # Verifica as primeiras 5 linhas
    df.head()

    # Verifica as informações do DataFrame, como tipos de dados e valores ausentes
    df.info()

    # Obtém estatísticas descritivas dos dados numéricos
    df.describe()
    print()

    print(f"Existem {df['NU_INSCRICAO'].duplicated().sum()} inscrições duplicadas.")


def show_cleaned_df_infos(cleaned_df: pd.DataFrame):
    print(f"Colunas restantes: {cleaned_df.columns}")

    # Informações básicas - Cópia limpa
    print(f'Registros: {len(cleaned_df)}\nVariáveis: {len(cleaned_df.columns)}')

    print(cleaned_df.head())

    # Verifica as primeiras 5 linhas
    cleaned_df.head()

    # Verifica as informações do DataFrame, como tipos de dados e valores ausentes
    cleaned_df.info()

    # Obtém estatísticas descritivas dos dados numéricos
    cleaned_df.describe()
    print(cleaned_df['TP_PRESENCA_CN'])


def show_disqualified_info(cleaned_df: pd.DataFrame):
    print(cleaned_df['TP_PRESENCA_CN'].value_counts())  # Para conferir os valores restantes
    print(f'Registros após filtro: {len(cleaned_df)}')  # Para ver quantos registros sobraram
    print(cleaned_df.head())


def show_null_columns(cleaned_df: pd.DataFrame):
    nulos = cleaned_df.isnull().sum()
    print([nulos > 0])  # Mostra apenas as colunas com valores ausentes

    print(cleaned_df.isna().sum())
