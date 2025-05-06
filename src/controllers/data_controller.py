import pandas as pd
import models.consts as c


class DataController:
    def __init__(self):
        self.df_microdados_enem = pd.read_csv(c.csv_microdados_path, encoding='ISO-8859-1', sep=';')
        self.cleaned_df = pd.DataFrame()

    def handle_df_microdados(self):
        for column, mapping in c.dicionario.items():
            self.df_microdados_enem[column] = self.df_microdados_enem[column].replace(mapping)

    def clean_columns(self):
        self.cleaned_df = self.df_microdados_enem.drop(columns=c.columns_to_remove)

    def handle_df_enem(self):
        self.df_microdados_enem = self.df_microdados_enem.drop(columns=c.columns_to_remove_redacao)
        self.df_microdados_enem = self.df_microdados_enem[self.df_microdados_enem['TP_PRESENCA_CN'] == "Presente na prova"]

    def filter_disqualified(self):
        self.cleaned_df = self.cleaned_df[self.cleaned_df['TP_PRESENCA_CN'] == "Presente na prova"]

    def handle_null_data(self):
        # TRANSFORMAR AS QUANTITATIVAS QUE ESTÃO REPRESENTADAS POR CÓDIGOS
        # ADICIONAR QUALITATIVAS NO DICIONÁRIO

        codificadas = ['TP_ENSINO', 'TP_DEPENDENCIA_ADM_ESC', 'TP_LOCALIZACAO_ESC', 'TP_SIT_FUNC_ESC']
        quantitativas = ['CO_MUNICIPIO_ESC', 'CO_UF_ESC']
        qualitativas = ['NO_MUNICIPIO_ESC', 'SG_UF_ESC']

        for colunas in codificadas:
            print(colunas)
            # Verificando se o 0 já não é um código existente
            print(f"Existem {(self.cleaned_df[colunas] == 0).sum()} ZEROS na coluna.")

            # substituindo campos nulos de TP_ENSINO por 0, que significa "Não informado"
            self.cleaned_df[colunas] = self.cleaned_df[colunas].fillna(0)
            print(f"Quantidade de ZEROS na coluna {(self.cleaned_df[colunas] == 0).sum()}.")
            print(f"Quantidade de campos NULOS na coluna {self.cleaned_df[colunas].isnull().sum()}.")

            # adicionando o código 0 do TP_ENSINO no dicionário
            c.dicionario.setdefault(colunas, {})[0] = "Não informado"

            # print(dicionario)

        for colunas in quantitativas:
            print(colunas)
            # Verificando se o 0 já não é um código existente
            print(f"Existem {(self.cleaned_df[colunas] == 0).sum()} ZEROS na coluna.")

            # substituindo campos nulos de TP_ENSINO por 0, que significa "Não informado"
            self.cleaned_df[colunas] = self.cleaned_df[colunas].fillna(0)
            print(f"Quantidade de ZEROS na coluna {(self.cleaned_df[colunas] == 0).sum()}.")
            print(f"Quantidade de campos NULOS na coluna {self.cleaned_df[colunas].isnull().sum()}.")

        for colunas in qualitativas:
            print(colunas)
            # Verificando se o 0 já não é um código existente
            print(f"Existem {(self.cleaned_df[colunas] == 'Não informado').sum()} 'Não informado' na coluna.")

            # substituindo campos nulos de NO_MUNICIPIO_ESC por "Não informado"
            self.cleaned_df[colunas] = self.cleaned_df[colunas].fillna("Não informado")
            print(f"Quantidade de 'Não informados' na coluna {(self.cleaned_df[colunas] == 'Não informado').sum()}.")
            print(f"Quantidade de campos NULOS na coluna {self.cleaned_df[colunas].isnull().sum()}.")
            # df_limpo[colunas].head()

        for coluna, mapeamento in c.dicionario.items():
            self.cleaned_df[coluna] = self.cleaned_df[coluna].replace(mapeamento)

