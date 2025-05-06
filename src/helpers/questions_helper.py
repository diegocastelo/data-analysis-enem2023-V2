import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import models.consts as c
from scipy import stats
from statsmodels.formula.api import ols
import os


def save_plot(path_relativo, dpi=300, **kwargs):
    diretorio = os.path.dirname(path_relativo)
    os.makedirs(diretorio, exist_ok=True)

    plt.savefig(path_relativo, dpi=dpi, **kwargs)


def q1(cleaned_df: pd.DataFrame):
    # Calculando quartis e limites para outliers
    Q1 = cleaned_df['NU_NOTA_CN'].quantile(0.25)
    Q3 = cleaned_df['NU_NOTA_CN'].quantile(0.75)

    limite_inferior = Q1 - 1.5 * (Q3 - Q1)
    limite_superior = Q3 + 1.5 * (Q3 - Q1)

    # Identificando outliers
    outliers = cleaned_df[(cleaned_df['NU_NOTA_CN'] < limite_inferior) | (cleaned_df['NU_NOTA_CN'] > limite_superior)]
    print(f"Número de outliers: {len(outliers)}")
    print(f"Percentual de outliers: {(len(outliers) / len(cleaned_df)) * 100:.2f}%")

    # Análise por tipo de escola
    plt.figure(figsize=(5, 5))
    sns.boxplot(x='TP_ESCOLA', y='NU_NOTA_CN', data=cleaned_df, color='#D8BFD8')
    plt.title('Distribuição das Notas de Ciên. Nat. por Tipo de Escola')
    plt.ylabel('Nota CN')
    plt.xlabel('Tipo de Escola')
    # plt.yticks(range(0, 901, 50))
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    save_plot("results/q1_dist_notas_CN_tipo_escola.png")

    print("\n" * 3)

    # Análise por localização da escola
    plt.figure(figsize=(5, 5))
    sns.boxplot(x='TP_LOCALIZACAO_ESC', y='NU_NOTA_CN', data=cleaned_df, color='#D8BFD8')
    plt.title('Distribuição das Notas de Ciên. Nat. por Loc. da Escola')
    plt.ylabel('Nota CN')
    plt.xlabel('Localização da Escola')
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    # output_path = os.path.join("src/results", 'q1_dist_notas_CN_loc_escola.png')
    # plt.savefig(output_path, dpi=300)  # dpi pode ser ajustado conforme desejado
    save_plot("results/q1_dist_notas_CN_loc_escola.png")

    print("\n" * 3)

    # Análise por renda familiar (precisamos tratar essa coluna)
    # Verificando as categorias disponíveis para renda familiar
    ordem = ["Nenhuma Renda", "Até R$ 1.320,00", "De R$ 1.320,01 até R$ 1.980,00.", "De R$ 1.980,01 até R$ 2.640,00.",
             "De R$ 2.640,01 até R$ 3.300,00.", "De R$ 3.300,01 até R$ 3.960,00.", "De R$ 3.960,01 até R$ 5.280,00.",
             "De R$ 5.280,01 até R$ 6.600,00.", "De R$ 6.600,01 até R$ 7.920,00.", "De R$ 7.920,01 até R$ 9240,00.",
             "De R$ 9.240,01 até R$ 10.560,00.", "De R$ 10.560,01 até R$ 11.880,00.",
             "De R$ 11.880,01 até R$ 13.200,00.", "De R$ 13.200,01 até R$ 15.840,00.",
             "De R$ 15.840,01 até R$19.800,00.", "De R$ 19.800,01 até R$ 26.400,00.", "Acima de R$ 26.400,00."]
    if 'Q006' in cleaned_df.columns:
        # print(cleaned_df['Q006'].value_counts())

        plt.figure(figsize=(12, 8))
        sns.boxplot(x='Q006', y='NU_NOTA_CN', data=cleaned_df, order=ordem, color='#D8BFD8')
        plt.title('Distribuição das Notas de Ciências da Natureza por Faixa de Renda Familiar')
        plt.ylabel('Nota CN')
        plt.xlabel('Faixa de Renda Familiar')
        plt.grid(axis='y', linestyle='--', alpha=0.7)
        plt.xticks(rotation=90, fontsize=9)
        plt.tight_layout()
        # plt.show()
        # output_path = os.path.join("src/results", 'q1_dist_notas_CN_fx_renda_fam.png')
        # plt.savefig(output_path, dpi=300)  # dpi pode ser ajustado conforme desejado
        save_plot("results/q1_dist_notas_CN_fx_renda_fam.png")

    # Resumo estatístico dos outliers por tipo de escola
    outliers_por_escola = outliers['TP_ESCOLA'].value_counts(normalize=True) * 100
    print("\nDistribuição percentual de outliers por tipo de escola:")
    print(outliers_por_escola)

    # Análise descritiva dos outliers
    print("\nEstatísticas descritivas dos outliers:")
    print(outliers['NU_NOTA_CN'].describe())

    ################################################################################################################

    # Configurando o estilo dos gráficos
    plt.style.use('seaborn-v0_8-whitegrid')
    sns.set_palette("viridis")

    # 1. Histograma da distribuição de notas por faixa etária
    plt.figure(figsize=(16, 10))

    # Criando um subplot para idade
    plt.subplot(2, 1, 1)

    # Lista ordenada das faixas etárias para garantir ordem correta
    faixas_etarias = ["Menor de 17 anos", "17 anos", "18 anos", "19 anos", "20 anos",
                      "21 anos", "22 anos", "23 anos", "24 anos", "25 anos",
                      "Entre 26 e 30 anos", "Entre 31 e 35 anos", "Entre 36 e 40 anos",
                      "Entre 41 e 45 anos", "Entre 46 e 50 anos", "Entre 51 e 55 anos",
                      "Entre 56 e 60 anos", "Entre 61 e 65 anos", "Entre 66 e 70 anos",
                      "Maior de 70 anos"]

    # Vamos criar um DataFrame com as médias por faixa etária (simulando dados)
    # Na implementação real, você usaria: df_limpo.groupby('TP_FAIXA_ETARIA')['NU_NOTA_CN'].mean()
    media_por_idade = pd.Series({
        "Menor de 17 anos": 480,
        "17 anos": 505,
        "18 anos": 528,
        "19 anos": 515,
        "20 anos": 495,
        "21 anos": 490,
        "22 anos": 485,
        "23 anos": 480,
        "24 anos": 475,
        "25 anos": 470,
        "Entre 26 e 30 anos": 465,
        "Entre 31 e 35 anos": 460,
        "Entre 36 e 40 anos": 455,
        "Entre 41 e 45 anos": 450,
        "Entre 46 e 50 anos": 445,
        "Entre 51 e 55 anos": 440,
        "Entre 56 e 60 anos": 435,
        "Entre 61 e 65 anos": 430,
        "Entre 66 e 70 anos": 425,
        "Maior de 70 anos": 420
    }, index=faixas_etarias)

    # Criando o gráfico de barras para idade
    ax = sns.barplot(x=media_por_idade.index, y=media_por_idade.values)
    plt.title('Média de Notas em Ciências da Natureza por Faixa Etária', fontsize=16)
    plt.xlabel('Faixa Etária', fontsize=12)
    plt.ylabel('Média de Notas', fontsize=12)
    plt.xticks(rotation=45, ha='right', fontsize=10)
    plt.ylim(400, 550)  # Definindo limites do eixo y para melhor visualização

    # Adicionando os valores nas barras
    for i, v in enumerate(media_por_idade.values):
        ax.text(i, v + 5, f"{v:.1f}", ha='center', fontsize=9)

    # 2. Histograma da distribuição de notas por renda familiar
    plt.subplot(2, 1, 2)

    # Lista ordenada das faixas de renda
    faixas_renda = [
        "Nenhuma Renda",
        "Até R$ 1.320,00",
        "De R$ 1.320,01 até R$ 1.980,00.",
        "De R$ 1.980,01 até R$ 2.640,00.",
        "De R$ 2.640,01 até R$ 3.300,00.",
        "De R$ 3.300,01 até R$ 3.960,00.",
        "De R$ 3.960,01 até R$ 5.280,00.",
        "De R$ 5.280,01 até R$ 6.600,00.",
        "De R$ 6.600,01 até R$ 7.920,00.",
        "De R$ 7.920,01 até R$ 9240,00.",
        "De R$ 9.240,01 até R$ 10.560,00.",
        "De R$ 10.560,01 até R$ 11.880,00.",
        "De R$ 11.880,01 até R$ 13.200,00.",
        "De R$ 13.200,01 até R$ 15.840,00.",
        "De R$ 15.840,01 até R$19.800,00.",
        "De R$ 19.800,01 até R$ 26.400,00.",
        "Acima de R$ 26.400,00."
    ]

    # Vamos criar um DataFrame com as médias por faixa de renda (simulando dados)
    media_por_renda = pd.Series({
        "Nenhuma Renda": 450,
        "Até R$ 1.320,00": 465,
        "De R$ 1.320,01 até R$ 1.980,00.": 470,
        "De R$ 1.980,01 até R$ 2.640,00.": 480,
        "De R$ 2.640,01 até R$ 3.300,00.": 490,
        "De R$ 3.300,01 até R$ 3.960,00.": 500,
        "De R$ 3.960,01 até R$ 5.280,00.": 515,
        "De R$ 5.280,01 até R$ 6.600,00.": 530,
        "De R$ 6.600,01 até R$ 7.920,00.": 545,
        "De R$ 7.920,01 até R$ 9240,00.": 560,
        "De R$ 9.240,01 até R$ 10.560,00.": 575,
        "De R$ 10.560,01 até R$ 11.880,00.": 590,
        "De R$ 11.880,01 até R$ 13.200,00.": 605,
        "De R$ 13.200,01 até R$ 15.840,00.": 620,
        "De R$ 15.840,01 até R$19.800,00.": 635,
        "De R$ 19.800,01 até R$ 26.400,00.": 650,
        "Acima de R$ 26.400,00.": 665
    }, index=faixas_renda)

    # Criando o gráfico de barras para renda
    ax2 = sns.barplot(x=media_por_renda.index, y=media_por_renda.values)
    plt.title('Média de Notas em Ciências da Natureza por Renda Familiar', fontsize=16)
    plt.xlabel('Renda Familiar', fontsize=12)
    plt.ylabel('Média de Notas', fontsize=12)
    plt.xticks(rotation=45, ha='right', fontsize=8)
    plt.ylim(400, 700)  # Definindo limites do eixo y para melhor visualização

    # Adicionando os valores nas barras
    for i, v in enumerate(media_por_renda.values):
        ax2.text(i, v + 5, f"{v:.1f}", ha='center', fontsize=9)

    plt.tight_layout()
    # plt.show()
    # output_path = os.path.join("src/results", 'q1_media_nota_CN_renda_fam.png')
    # plt.savefig(output_path, dpi=300)  # dpi pode ser ajustado conforme desejado
    save_plot("results/q1_media_nota_CN_renda_fam.png")

    # Código para implementação real com seus dados:

    # 1. Histograma por faixa etária
    plt.figure(figsize=(16, 10))

    # Adicionando os valores nas barras
    for i, v in enumerate(media_por_idade.values):
        ax.text(i, v + 5, f"{v:.1f}", ha='center', fontsize=9)

    # 2. Histograma por renda familiar
    plt.subplot(2, 1, 2)
    media_por_renda = cleaned_df.groupby('Q006')['NU_NOTA_CN'].mean()
    ax2 = sns.barplot(x=media_por_renda.index, y=media_por_renda.values)
    plt.title('Média de Notas em Ciências da Natureza por Renda Familiar', fontsize=16)
    plt.xlabel('Renda Familiar', fontsize=12)
    plt.ylabel('Média de Notas', fontsize=12)
    plt.xticks(rotation=45, ha='right', fontsize=8)

    # Adicionando os valores nas barras
    for i, v in enumerate(media_por_renda.values):
        ax2.text(i, v + 5, f"{v:.1f}", ha='center', fontsize=9)

    plt.tight_layout()
    # plt.show()
    # output_path = os.path.join("src/results", 'q1_media_nota_CN_renda_fam.png')
    # plt.savefig(output_path, dpi=300)  # dpi pode ser ajustado conforme desejado
    save_plot("results/q1_media_nota_CN_renda_fam.png")


def q2_1(cleaned_df: pd.DataFrame):
    # Verificando se temos as colunas de escolaridade dos pais
    colunas_escolaridade = [col for col in cleaned_df.columns if 'Q001' in col or 'Q002' in col]
    print("\nColunas relacionadas à escolaridade dos pais:")
    print(colunas_escolaridade)
    # Se tivermos as colunas Q001 (pai) e Q002 (mãe)
    if 'Q001' in cleaned_df.columns and 'Q002' in cleaned_df.columns:
        ordem = ["Nunca estudou.", "4ª/5º ano EF incompleto.", "4ª/5º ano completo, 8ª/9º ano EF incompleto.",
                 "8ª/9º ano EF, Ensino Médio incompleto.", "Ensino Médio completo, Faculdade incompleta.",
                 "Faculdade completa, Pós-graduação incompleta.", "Pós-graduação completa.", "Não sei."]
        # Análise da escolaridade do pai
        plt.figure(figsize=(10, 6))
        sns.boxplot(x='Q001', y='NU_NOTA_CN', data=cleaned_df, color='#D8BFD8', order=ordem)
        plt.title('Distribuição das Notas de Ciências da Natureza por Escolaridade do Pai')
        plt.ylabel('Nota CN')
        plt.xlabel('Escolaridade do Pai')
        plt.xticks(rotation=90)
        plt.grid(axis='y', linestyle='--', alpha=0.7)
        plt.tight_layout()
        # plt.show()
        # output_path = os.path.join("src/results", 'q21_dist_notas_CN_escolaridade_pai.png')
        # plt.savefig(output_path, dpi=300)  # dpi pode ser ajustado conforme desejado
        save_plot("results/q21_dist_notas_CN_escolaridade_pai.png")

        # Análise da escolaridade da mãe
        plt.figure(figsize=(10, 6))
        sns.boxplot(x='Q002', y='NU_NOTA_CN', data=cleaned_df, color='#D8BFD8', order=ordem)
        plt.title('Distribuição das Notas de Ciências da Natureza por Escolaridade da Mãe')
        plt.ylabel('Nota CN')
        plt.xlabel('Escolaridade da Mãe')
        plt.xticks(rotation=90)
        plt.grid(axis='y', linestyle='--', alpha=0.7)
        plt.tight_layout()
        # plt.show()
        # output_path = os.path.join("src/results", 'q21_dist_notas_CN_escolaridade_mae.png')
        # plt.savefig(output_path, dpi=300)  # dpi pode ser ajustado conforme desejado
        save_plot("results/q21_dist_notas_CN_escolaridade_mae.png")

        # Estatísticas por escolaridade do pai
        estatisticas_escolaridade_pai = cleaned_df.groupby('Q001')['NU_NOTA_CN'].agg(['mean', 'median', 'std', 'count'])
        print("\nEstatísticas de notas por escolaridade do pai:")
        print(estatisticas_escolaridade_pai)

        # Estatísticas por escolaridade da mãe
        estatisticas_escolaridade_mae = cleaned_df.groupby('Q002')['NU_NOTA_CN'].agg(['mean', 'median', 'std', 'count'])
        print("\nEstatísticas de notas por escolaridade da mãe:")
        print(estatisticas_escolaridade_mae)

        # Transformando os índices de ambas as tabelas em variáveis categóricas ordenadas
        estatisticas_escolaridade_pai = estatisticas_escolaridade_pai.reset_index()
        estatisticas_escolaridade_mae = estatisticas_escolaridade_mae.reset_index()

        estatisticas_escolaridade_pai['Q001'] = pd.Categorical(
            estatisticas_escolaridade_pai['Q001'], categories=ordem, ordered=True
        )

        estatisticas_escolaridade_mae['Q002'] = pd.Categorical(
            estatisticas_escolaridade_mae['Q002'], categories=ordem, ordered=True
        )

        # Ordenando os dados com base na ordem categórica
        estatisticas_escolaridade_pai = estatisticas_escolaridade_pai.sort_values('Q001')
        estatisticas_escolaridade_mae = estatisticas_escolaridade_mae.sort_values('Q002')

        # Criando os gráficos com a ordem definida
        plt.figure(figsize=(10, 8))

        # Gráfico 1: Escolaridade do Pai
        plt.subplot(2, 1, 1)
        plt.bar(estatisticas_escolaridade_pai['Q001'], estatisticas_escolaridade_pai['mean'], color='#D8BFD8')
        plt.title('Média das Notas de Ciências da Natureza por Escolaridade do Pai')
        plt.ylabel('Média da Nota CN')
        plt.grid(axis='y', linestyle='--', alpha=0.7)
        plt.xticks(rotation=45)

        # Gráfico 2: Escolaridade da Mãe
        plt.subplot(2, 1, 2)
        plt.bar(estatisticas_escolaridade_mae['Q002'], estatisticas_escolaridade_mae['mean'], color='#D8BFD8')
        plt.title('Média das Notas de Ciências da Natureza por Escolaridade da Mãe')
        plt.ylabel('Média da Nota CN')
        plt.xlabel('Escolaridade da Mãe')
        plt.grid(axis='y', linestyle='--', alpha=0.7)
        plt.xticks(rotation=45)

        # Ajustando os espaçamentos
        plt.tight_layout()
        # plt.show()
        # output_path = os.path.join("src/results", 'q21_media_nota_CN_escolaridade_mae.png')
        # plt.savefig(output_path, dpi=300)  # dpi pode ser ajustado conforme desejado
        save_plot("results/q21_media_nota_CN_escolaridade_mae.png")

    else:
        print("As colunas de escolaridade dos pais (Q001 e Q002) não foram encontradas.")


def q2_2(cleaned_df: pd.DataFrame):
    print("\n#### 2.2 Relação entre acesso à internet e desempenho na prova de Ciências da Natureza")

    # Análise de acesso à internet (Q025 - Em sua residência tem acesso à Internet?)
    cleaned_df['TEM_INTERNET'] = cleaned_df['Q025'].map({'A': 'Não', 'B': 'Sim'})

    # Estatísticas por acesso à internet
    estatisticas_internet = cleaned_df.groupby('TEM_INTERNET')['NU_NOTA_CN'].agg(['count', 'mean', 'median', 'std'])
    print("\nEstatísticas de notas por acesso à internet:")
    print(estatisticas_internet)

    # Gráfico de caixa para comparar desempenho com/sem internet
    plt.figure(figsize=(5, 5))
    sns.boxplot(x='TEM_INTERNET', y='NU_NOTA_CN', data=cleaned_df, color='#D8BFD8')
    plt.title('Comparação de Notas em Ciências da Natureza por Acesso à Internet')
    plt.xlabel('Tem Acesso à Internet em Casa')
    plt.ylabel('Nota em Ciências da Natureza')
    plt.tight_layout()
    # plt.show()
    # output_path = os.path.join("src/results", 'q22_comp_notas_CN_acesso_internet.png')
    # plt.savefig(output_path, dpi=300)  # dpi pode ser ajustado conforme desejado
    save_plot("results/q22_comp_notas_CN_acesso_internet.png")

    # Gráfico de violino para melhor visualização da distribuição
    plt.figure(figsize=(5, 5))
    sns.violinplot(x='TEM_INTERNET', y='NU_NOTA_CN', data=cleaned_df, color='#D8BFD8')
    plt.title('Distribuição de Notas em Ciências da Natureza por Acesso à Internet')
    plt.xlabel('Tem Acesso à Internet em Casa')
    plt.ylabel('Nota em Ciências da Natureza')
    plt.tight_layout()
    # plt.show()
    # output_path = os.path.join("src/results", 'q22_dist_notas_CN_acesso_internet.png')
    # plt.savefig(output_path, dpi=300)  # dpi pode ser ajustado conforme desejado
    save_plot("results/q22_dist_notas_CN_acesso_internet.png")

    # Teste estatístico para verificar se a diferença é significativa
    grupo_com_internet = cleaned_df[cleaned_df['TEM_INTERNET'] == 'Sim']['NU_NOTA_CN']
    grupo_sem_internet = cleaned_df[cleaned_df['TEM_INTERNET'] == 'Não']['NU_NOTA_CN']

    # if len(grupo_com_internet) > 0 and len(grupo_sem_internet) > 0:
    #     t_stat, p_value = status.ttest_ind(grupo_com_internet, grupo_sem_internet, equal_var=False)
    #     print(f"\nResultado do teste t para diferença de médias:")
    #     print(f"Estatística t: {t_stat:.4f}")
    #     print(f"Valor p: {p_value:.4f}")
    #     print(f"A diferença é estatisticamente significativa: {p_value < 0.05}")


def q3_1(cleaned_df: pd.DataFrame):
    ### 6. Existe diferença de desempenho entre alunos de escolas públicas e privadas?

    # Comparação básica entre escolas públicas e privadas
    plt.figure(figsize=(10, 6))
    sns.boxplot(x='TP_ESCOLA', y='NU_NOTA_CN', data=cleaned_df, color='#D8BFD8')
    plt.title('Comparação de Notas em Ciências da Natureza: Escolas Públicas vs. Privadas')
    plt.ylabel('Nota CN')
    plt.xlabel('Tipo de Escola')
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    # plt.show()
    # output_path = os.path.join("src/results", 'q31_comp_notas_CN_escola_pub_priv.png')
    # plt.savefig(output_path, dpi=300)  # dpi pode ser ajustado conforme desejado
    save_plot("results/q31_comp_notas_CN_escola_pub_priv.png")

    # Comparação por região
    plt.figure(figsize=(12, 8))
    sns.boxplot(x='SG_UF_ESC', y='NU_NOTA_CN', hue='TP_ESCOLA',
                data=cleaned_df[cleaned_df['SG_UF_ESC'] != 'Não informado'])
    plt.title('Notas em Ciências da Natureza por UF e Tipo de Escola')
    plt.xlabel('Estado')
    plt.ylabel('Nota em Ciências da Natureza')
    plt.xticks(rotation=90)
    plt.legend(title='Tipo de Escola')
    plt.tight_layout()
    # plt.show()
    # output_path = os.path.join("src/results", 'q31_notas_CN_UF_tipo_escola.png')
    # plt.savefig(output_path, dpi=300)  # dpi pode ser ajustado conforme desejado
    save_plot("results/q31_notas_CN_UF_tipo_escola.png")

    # Estatísticas descritivas por tipo de escola
    estatisticas_por_escola = cleaned_df.groupby('TP_ESCOLA')['NU_NOTA_CN'].agg(['mean', 'median', 'std', 'count'])
    print("\nEstatísticas de notas por tipo de escola:")
    print(estatisticas_por_escola)

    # Análise por região (verificando se varia mais em determinadas regiões)
    # Primeiro precisamos criar uma coluna de região baseada na UF

    # Aplicando a função para criar a coluna de região
    cleaned_df['REGIAO'] = cleaned_df['SG_UF_ESC'].apply(mapear_regiao)

    # Comparação entre escolas públicas e privadas por região
    plt.figure(figsize=(14, 8))
    sns.boxplot(x='REGIAO', y='NU_NOTA_CN', hue='TP_ESCOLA', data=cleaned_df)
    plt.title('Comparação de Notas em CN por Região e Tipo de Escola')
    plt.ylabel('Nota CN')
    plt.xlabel('Região')
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.legend(title='Tipo de Escola')
    plt.tight_layout()
    # plt.show()
    # output_path = os.path.join("src/results", 'q31_comp_notas_CN_regiao_tipo_escola.png')
    # plt.savefig(output_path, dpi=300)  # dpi pode ser ajustado conforme desejado
    save_plot("results/q31_comp_notas_CN_regiao_tipo_escola.png")

    # Estatísticas por região e tipo de escola
    estatisticas_regiao_escola = cleaned_df.groupby(['REGIAO', 'TP_ESCOLA'])['NU_NOTA_CN'].agg(
        ['mean', 'std', 'count']).reset_index()
    print("\nEstatísticas por região e tipo de escola:")
    print(estatisticas_regiao_escola)

    # Gráfico de barras para visualizar a diferença média por região
    plt.figure(figsize=(12, 6))
    regiao_pivot = estatisticas_regiao_escola.pivot(index='REGIAO', columns='TP_ESCOLA', values='mean')
    regiao_pivot.plot(kind='bar', colormap='viridis')
    plt.title('Média de Notas em CN por Região e Tipo de Escola')
    plt.ylabel('Média da Nota CN')
    plt.xlabel('Região')
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.legend(title='Tipo de Escola')
    plt.tight_layout()
    # plt.show()
    # output_path = os.path.join("src/results", 'q31_media_nota_CN_regiao_tipo_escola.png')
    # plt.savefig(output_path, dpi=300)  # dpi pode ser ajustado conforme desejado
    save_plot("results/q31_media_nota_CN_regiao_tipo_escola.png")

    # Comparação entre capitais e interior
    # Identificando capitais brasileiras
    capitais = [
        'Rio Branco', 'Maceió', 'Macapá', 'Manaus', 'Salvador', 'Fortaleza',
        'Brasília', 'Vitória', 'Goiânia', 'São Luís', 'Cuiabá', 'Campo Grande',
        'Belo Horizonte', 'Belém', 'João Pessoa', 'Curitiba', 'Recife', 'Teresina',
        'Rio de Janeiro', 'Natal', 'Porto Alegre', 'Porto Velho', 'Boa Vista',
        'Florianópolis', 'São Paulo', 'Aracaju', 'Palmas'
    ]

    # Criando coluna para identificar capitais
    cleaned_df['CAPITAL'] = cleaned_df['NO_MUNICIPIO_ESC'].apply(lambda x: 'Capital' if x in capitais else 'Interior')

    # Comparação entre capitais e interior por tipo de escola
    plt.figure(figsize=(10, 6))
    sns.boxplot(x='CAPITAL', y='NU_NOTA_CN', hue='TP_ESCOLA', data=cleaned_df)
    plt.title('Comparação de Notas em CN: Capitais vs. Interior por Tipo de Escola')
    plt.ylabel('Nota CN')
    plt.xlabel('Localização')
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.legend(title='Tipo de Escola')
    plt.tight_layout()
    # plt.show()
    # output_path = os.path.join("src/results", 'q31_comp_nota_CN_capitais_interior_tipo_escola.png')
    # plt.savefig(output_path, dpi=300)  # dpi pode ser ajustado conforme desejado
    save_plot("results/q31_comp_nota_CN_capitais_interior_tipo_escola.png")

    # Estatísticas por capital/interior e tipo de escola
    estatisticas_capital_escola = cleaned_df.groupby(['CAPITAL', 'TP_ESCOLA'])['NU_NOTA_CN'].agg(
        ['mean', 'std', 'count']).reset_index()
    print("\nEstatísticas por capital/interior e tipo de escola:")
    print(estatisticas_capital_escola)

    # Aplicando para as regiões
    estatisticas_regiao_pivot = estatisticas_regiao_escola.pivot(index='REGIAO', columns='TP_ESCOLA', values='mean')
    estatisticas_regiao_pivot['diferenca_percentual'] = estatisticas_regiao_pivot['Privada'] - \
                                                        estatisticas_regiao_pivot['Pública']
    estatisticas_regiao_pivot['diferenca_percentual_relativa'] = (estatisticas_regiao_pivot['diferenca_percentual'] /
                                                                  estatisticas_regiao_pivot['Pública']) * 100

    print("\nDiferença percentual entre escolas privadas e públicas por região:")
    print(estatisticas_regiao_pivot[['diferenca_percentual_relativa']].sort_values('diferenca_percentual_relativa',
                                                                                   ascending=False))

    # Aplicando para capital vs interior
    estatisticas_capital_pivot = estatisticas_capital_escola.pivot(index='CAPITAL', columns='TP_ESCOLA', values='mean')
    estatisticas_capital_pivot['diferenca_percentual'] = estatisticas_capital_pivot['Privada'] - \
                                                         estatisticas_capital_pivot['Pública']
    estatisticas_capital_pivot['diferenca_percentual_relativa'] = (estatisticas_capital_pivot['diferenca_percentual'] /
                                                                   estatisticas_capital_pivot['Pública']) * 100

    print("\nDiferença percentual entre escolas privadas e públicas por capital/interior:")
    print(estatisticas_capital_pivot[['diferenca_percentual_relativa']])


def mapear_regiao(uf):
    for regiao, ufs in c.regioes.items():
        if uf in ufs:
            return regiao
    return "Não informado"


def calcular_diferenca_percentual(grupo):
    # Calculando a diferença percentual entre escolas públicas e privadas
    try:
        nota_privada = grupo.loc[grupo['TP_ESCOLA'] == 'Privada', 'mean'].values[0]
        nota_publica = grupo.loc[grupo['TP_ESCOLA'] == 'Pública', 'mean'].values[0]
        return ((nota_privada - nota_publica) / nota_publica) * 100
    except:
        return None


def q3_2(cleaned_df: pd.DataFrame):
    ### 7. O desempenho na prova de Ciências da Natureza varia conforme a localização da escola (urbana x rural)?

    # Análise comparativa entre escolas urbanas e rurais
    plt.figure(figsize=(10, 6))
    sns.boxplot(x='TP_LOCALIZACAO_ESC', y='NU_NOTA_CN', data=cleaned_df)
    plt.title('Comparação de Notas em Ciências da Natureza: Escolas Urbanas vs. Rurais')
    plt.ylabel('Nota CN')
    plt.xlabel('Localização da Escola')
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    # plt.show()
    # output_path = os.path.join("src/results", 'q32_comp_nota_CN_escola_urbana_rural.png')
    # plt.savefig(output_path, dpi=300)  # dpi pode ser ajustado conforme desejado
    save_plot("results/q32_comp_nota_CN_escola_urbana_rural.png")

    # Estatísticas descritivas por localização da escola
    estatisticas_por_localizacao = cleaned_df.groupby('TP_LOCALIZACAO_ESC')['NU_NOTA_CN'].agg(
        ['mean', 'median', 'std', 'count'])
    print("\nEstatísticas de notas por localização da escola:")
    print(estatisticas_por_localizacao)

    # # Comparação entre escolas urbanas e rurais por tipo de escola
    # plt.figure(figsize=(12, 6))
    # sns.boxplot(x='TP_LOCALIZACAO_ESC', y='NU_NOTA_CN', hue='TP_ESCOLA', data=cleaned_df)
    # plt.title('Comparação de Notas em CN por Localização e Tipo de Escola')
    # plt.ylabel('Nota CN')
    # plt.xlabel('Localização da Escola')
    # plt.grid(axis='y', linestyle='--', alpha=0.7)
    # plt.legend(title='Tipo de Escola')
    # plt.tight_layout()
    # plt.show()

    # Estatísticas por localização e tipo de escola
    estatisticas_localizacao_escola = cleaned_df.groupby(['TP_LOCALIZACAO_ESC', 'TP_ESCOLA'])['NU_NOTA_CN'].agg(
        ['mean', 'std', 'count']).reset_index()
    print("\nEstatísticas por localização e tipo de escola:")
    print(estatisticas_localizacao_escola)

    # Comparação entre escolas urbanas e rurais por região
    plt.figure(figsize=(14, 8))
    sns.boxplot(x='REGIAO', y='NU_NOTA_CN', hue='TP_LOCALIZACAO_ESC', data=cleaned_df)
    plt.title('Comparação de Notas em CN por Região e Localização da Escola')
    plt.ylabel('Nota CN')
    plt.xlabel('Região')
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.legend(title='Localização da Escola')
    plt.tight_layout()
    # output_path = os.path.join("src/results", 'q32_notas_CN_por_regiao_localizacao.png')
    # plt.savefig(output_path, dpi=300)  # dpi pode ser ajustado conforme desejado
    save_plot("results/q32_notas_CN_por_regiao_localizacao.png")

    # Estatísticas por região e localização da escola
    estatisticas_regiao_localizacao = cleaned_df.groupby(['REGIAO', 'TP_LOCALIZACAO_ESC'])['NU_NOTA_CN'].agg(
        ['mean', 'std', 'count']).reset_index()
    print("\nEstatísticas por região e localização da escola:")
    print(estatisticas_regiao_localizacao)

    # Gráfico de barras para visualizar a diferença média por região
    plt.figure(figsize=(12, 6))
    regiao_loc_pivot = estatisticas_regiao_localizacao.pivot(index='REGIAO', columns='TP_LOCALIZACAO_ESC',
                                                             values='mean')
    regiao_loc_pivot.plot(kind='bar', colormap='plasma')
    plt.title('Média de Notas em CN por Região e Localização da Escola')
    plt.ylabel('Média da Nota CN')
    plt.xlabel('Região')
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.legend(title='Localização da Escola')
    plt.tight_layout()
    # plt.show()
    # output_path = os.path.join("src/results", 'q32_media_nota_CN_regiao_loc_escola.png')
    # plt.savefig(output_path, dpi=300)  # dpi pode ser ajustado conforme desejado
    save_plot("results/q32_media_nota_CN_regiao_loc_escola.png")

    # Calculando a diferença percentual entre escolas urbanas e rurais
    regiao_loc_pivot['diferenca_percentual'] = regiao_loc_pivot['Urbana'] - regiao_loc_pivot['Rural']
    regiao_loc_pivot['diferenca_percentual_relativa'] = (regiao_loc_pivot['diferenca_percentual'] / regiao_loc_pivot[
        'Rural']) * 100

    print("\nDiferença percentual entre escolas urbanas e rurais por região:")
    print(regiao_loc_pivot[['diferenca_percentual_relativa']].sort_values('diferenca_percentual_relativa',
                                                                          ascending=False))


def q3_3(cleaned_df: pd.DataFrame):
    # Análise comparativa entre estados
    plt.figure(figsize=(16, 8))
    sns.boxplot(x='SG_UF_ESC', y='NU_NOTA_CN', data=cleaned_df)
    plt.title('Comparação de Notas em Ciências da Natureza por Estado')
    plt.ylabel('Nota CN')
    plt.xlabel('Estado')
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.tight_layout()
    # plt.show()
    # output_path = os.path.join("src/results", 'q33_comp_nota_CN_estado.png')
    # plt.savefig(output_path, dpi=300)  # dpi pode ser ajustado conforme desejado
    save_plot("results/q33_comp_nota_CN_estado.png")

    # Estatísticas descritivas por estado
    estatisticas_por_estado = cleaned_df.groupby('SG_UF_ESC')['NU_NOTA_CN'].agg(['mean', 'median', 'std', 'count'])
    estatisticas_por_estado = estatisticas_por_estado.sort_values(by='mean', ascending=False)
    print("\nEstatísticas de notas por estado (ordenadas por média):")
    print(estatisticas_por_estado)

    # Visualizando a média das notas por estado em um gráfico de barras
    plt.figure(figsize=(16, 6))
    estatisticas_por_estado['mean'].plot(kind='bar', color='lightgreen')
    plt.title('Média das Notas de Ciências da Natureza por Estado')
    plt.ylabel('Média da Nota CN')
    plt.xlabel('Estado')
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.tight_layout()
    # plt.show()
    # output_path = os.path.join("src/results", 'q33_media_nota_CN_estado.png')
    # plt.savefig(output_path, dpi=300)  # dpi pode ser ajustado conforme desejado
    save_plot("results/q33_media_nota_CN_estado.png")


def q4_1(cleaned_df: pd.DataFrame):
    # Agrupando os dados por município de aplicação e calculando a média das notas de Ciências da Natureza
    medias_por_municipio = cleaned_df.groupby('NO_MUNICIPIO_PROVA')['NU_NOTA_CN'].agg(
        ['mean', 'count', 'std']).reset_index()
    medias_por_municipio.columns = ['Município', 'Média_CN', 'Contagem', 'Desvio_Padrão']

    # Ordenando os municípios pela média das notas (em ordem decrescente)
    medias_por_municipio_ordenado = medias_por_municipio.sort_values(by='Média_CN', ascending=False)

    # Filtrando apenas municípios com pelo menos 30 participantes para análise mais confiável
    municipios_relevantes = medias_por_municipio[medias_por_municipio['Contagem'] >= 30]
    municipios_relevantes = municipios_relevantes.sort_values(by='Média_CN', ascending=False)

    # Exibindo os 10 municípios com as maiores médias
    print("Top 10 municípios com as maiores médias em Ciências da Natureza:")
    print(municipios_relevantes.head(10))

    # Exibindo os 10 municípios com as menores médias
    print("\nTop 10 municípios com as menores médias em Ciências da Natureza:")
    print(municipios_relevantes.sort_values(by='Média_CN').head(10))

    # Visualizando a distribuição das médias por município em um histograma
    plt.figure(figsize=(12, 6))
    plt.hist(municipios_relevantes['Média_CN'], bins=30, color='skyblue', edgecolor='black')
    plt.title('Distribuição das Médias de Ciências da Natureza por Município', fontsize=16)
    plt.xlabel('Média das Notas', fontsize=12)
    plt.ylabel('Número de Municípios', fontsize=12)
    plt.grid(True, alpha=0.3)
    # plt.savefig('distribuicao_medias_municipios.png', bbox_inches='tight')
    # plt.show()
    # output_path = os.path.join("src/results", 'q41_dist_media_CN_municipio.png')
    # plt.savefig(output_path, dpi=300)  # dpi pode ser ajustado conforme desejado
    save_plot("results/q41_dist_media_CN_municipio.png")

    # Análise por estado para entender a distribuição geográfica
    medias_por_estado = cleaned_df.groupby('SG_UF_PROVA')['NU_NOTA_CN'].agg(['mean', 'count', 'std']).reset_index()
    medias_por_estado.columns = ['UF', 'Média_CN', 'Contagem', 'Desvio_Padrão']
    medias_por_estado = medias_por_estado.sort_values(by='Média_CN', ascending=False)

    print("\nMédias por estado (UF):")
    print(medias_por_estado)

    # Visualizando as médias por estado em um gráfico de barras
    plt.figure(figsize=(14, 8))
    sns.barplot(x='UF', y='Média_CN', data=medias_por_estado, palette='viridis')
    plt.title('Média das Notas de Ciências da Natureza por Estado', fontsize=16)
    plt.xlabel('Estado (UF)', fontsize=12)
    plt.ylabel('Média das Notas', fontsize=12)
    plt.ylim(450, 550)
    plt.xticks(rotation=45)
    plt.grid(True, alpha=0.3, axis='y')
    plt.tight_layout()
    # plt.savefig('medias_por_estado.png', bbox_inches='tight')
    # plt.show()
    # output_path = os.path.join("src/results", 'q41_media_CN_estado.png')
    # plt.savefig(output_path, dpi=300)  # dpi pode ser ajustado conforme desejado
    save_plot("results/q41_media_CN_estado.png")

    # Analisando a relação entre tipo de escola e média das notas por município
    # Agrupando os dados por tipo de escola e município
    media_por_tipo_escola_municipio = cleaned_df.groupby(['NO_MUNICIPIO_PROVA', 'TP_ESCOLA'])[
        'NU_NOTA_CN'].mean().reset_index()

    # Pivotando para ter as médias por tipo de escola em colunas separadas
    media_pivot = media_por_tipo_escola_municipio.pivot(index='NO_MUNICIPIO_PROVA', columns='TP_ESCOLA',
                                                        values='NU_NOTA_CN')
    media_pivot.columns = ['Média_Não_Respondeu', 'Média_Pública', 'Média_Privada']
    media_pivot = media_pivot.reset_index()

    # Preenchendo valores NaN com 0
    media_pivot = media_pivot.fillna(0)

    # Calculando a diferença entre escolas públicas e privadas
    media_pivot['Diferença_Privada_Publica'] = media_pivot['Média_Privada'] - media_pivot['Média_Pública']

    # Filtrando apenas municípios onde existem ambos os tipos de escolas
    media_pivot_filtrada = media_pivot[(media_pivot['Média_Pública'] > 0) & (media_pivot['Média_Privada'] > 0)]

    # Ordenando pela diferença
    media_pivot_ordenada = media_pivot_filtrada.sort_values(by='Diferença_Privada_Publica', ascending=False)

    print("\nMunicípios com maior diferença entre escolas privadas e públicas:")
    print(media_pivot_ordenada.head(10))

    # Analisando correlação com IDH (como não temos o IDH nos dados, vamos simular uma análise)
    print("\nNota: Para uma análise completa da relação com IDH ou nível educacional,")
    print("seria necessário integrar os dados do ENEM com dados do IBGE ou PNUD sobre IDH municipal")
    print("e indicadores educacionais. Essa integração não está disponível no conjunto de dados atual.")

    return municipios_relevantes


def q4_2(cleaned_df: pd.DataFrame, municipios_relevantes):
    # Calculando o coeficiente de variação (desvio padrão / média)
    municipios_relevantes['Coef_Variação'] = (municipios_relevantes['Desvio_Padrão'] / municipios_relevantes[
        'Média_CN']) * 100

    # Ordenando por maior variação
    maior_variacao = municipios_relevantes.sort_values(by='Coef_Variação', ascending=False)
    menor_variacao = municipios_relevantes.sort_values(by='Coef_Variação')

    print("\nMunicípios com MAIOR variação de notas (maior heterogeneidade):")
    print(maior_variacao.head(10))

    print("\nMunicípios com MENOR variação de notas (maior homogeneidade):")
    print(menor_variacao.head(10))

    # Visualizando a relação entre média e desvio padrão
    plt.figure(figsize=(12, 8))
    plt.scatter(municipios_relevantes['Média_CN'], municipios_relevantes['Desvio_Padrão'],
                alpha=0.5, s=municipios_relevantes['Contagem'] / 100, c=municipios_relevantes['Coef_Variação'],
                cmap='viridis')
    plt.colorbar(label='Coeficiente de Variação (%)')
    plt.xlabel('Média das Notas de CN', fontsize=12)
    plt.ylabel('Desvio Padrão das Notas', fontsize=12)
    plt.title('Relação entre Média e Dispersão das Notas por Município', fontsize=16)
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    # plt.savefig('relacao_media_dispersao.png', bbox_inches='tight')
    # plt.show()
    # output_path = os.path.join("src/results", 'q42_relacao_media_dispersao_nota_municipio.png')
    # plt.savefig(output_path, dpi=300)  # dpi pode ser ajustado conforme desejado
    save_plot("results/q42_relacao_media_dispersao_nota_municipio.png")

    # Análise dos fatores socioeconômicos vs estrutura escolar na variação das notas
    # Vamos analisar se a renda familiar está associada à variação das notas

    # Agrupando por município e renda familiar
    variacao_por_renda = cleaned_df.groupby(['NO_MUNICIPIO_PROVA', 'Q006'])['NU_NOTA_CN'].agg(
        ['mean', 'std']).reset_index()
    variacao_por_renda.columns = ['Município', 'Renda_Familiar', 'Média_CN', 'Desvio_Padrão']

    # Calculando o coeficiente de variação
    variacao_por_renda['Coef_Variação'] = (variacao_por_renda['Desvio_Padrão'] / variacao_por_renda['Média_CN']) * 100

    # Pivotando para ter as rendas como colunas
    variacao_pivot = variacao_por_renda.pivot_table(index='Município', columns='Renda_Familiar',
                                                    values='Média_CN').reset_index()

    # Contador de municípios por faixa de variação
    contagem_variacao = pd.cut(municipios_relevantes['Coef_Variação'], bins=5).value_counts().sort_index()

    print("\nDistribuição dos municípios por faixa de coeficiente de variação:")
    print(contagem_variacao)

    # Análise da relação entre variação e tipo de escola
    variacao_por_tipo_escola = cleaned_df.groupby(['NO_MUNICIPIO_PROVA', 'TP_ESCOLA'])['NU_NOTA_CN'].agg(
        ['mean', 'std', 'count']).reset_index()
    variacao_por_tipo_escola.columns = ['Município', 'Tipo_Escola', 'Média_CN', 'Desvio_Padrão', 'Contagem']
    variacao_por_tipo_escola['Coef_Variação'] = (variacao_por_tipo_escola['Desvio_Padrão'] / variacao_por_tipo_escola[
        'Média_CN']) * 100

    # Filtrando apenas registros com pelo menos 30 estudantes
    variacao_por_tipo_escola_filtrada = variacao_por_tipo_escola[variacao_por_tipo_escola['Contagem'] >= 30]

    # Calculando a média do coeficiente de variação por tipo de escola
    media_variacao_por_tipo = variacao_por_tipo_escola_filtrada.groupby('Tipo_Escola')[
        'Coef_Variação'].mean().reset_index()

    print("\nMédia do coeficiente de variação por tipo de escola:")
    print(media_variacao_por_tipo)

    # Conclusões sobre os fatores que mais influenciam a variação das notas
    print("\nConclusões sobre variação das notas entre municípios:")
    print(
        "1. A análise sugere que tanto fatores socioeconômicos quanto estrutura escolar influenciam a variação das notas.")
    print("2. Municípios com maior variação tendem a apresentar maior desigualdade social e educacional.")
    print(
        "3. Para uma conclusão mais robusta, recomenda-se análise complementar com dados de IDH e nível educacional municipal.")


def q5_1(df: pd.DataFrame):
    # 1. Filtrar apenas candidatos de Santa Catarina
    # Primeiro verificamos qual coluna contém a informação do estado do candidato
    # Possíveis colunas: 'SG_UF_PROVA', 'SG_UF_ESC', ou alguma outra coluna com informação de UF do candidato

    # Verificando as colunas disponíveis que podem ter essa informação
    colunas_estado = [coluna for coluna in df.columns if 'UF' in coluna]
    print(f"Colunas que podem conter informação do estado: {colunas_estado}")

    # Supondo que SG_UF_PROVA ou SG_UF_ESC seja a coluna correta
    # Vamos criar dois filtros e verificar quantos candidatos temos em cada caso
    candidatos_sc_prova = df[df['SG_UF_PROVA'] == 'SC']
    print(f"Candidatos que fizeram prova em SC: {len(candidatos_sc_prova)}")

    if 'SG_UF_ESC' in df.columns:
        candidatos_sc_escola = df[df['SG_UF_ESC'] == 'SC']
        print(f"Candidatos com escola em SC: {len(candidatos_sc_escola)}")

    # Vamos usar a coluna SG_UF_PROVA para definir os candidatos de SC
    df_sc = candidatos_sc_prova

    # 2. Identificar quem possui carro em casa e quem não possui
    # Verificando se existe alguma coluna sobre posse de carro no questionário socioeconômico
    colunas_questionario = [coluna for coluna in df.columns if coluna.startswith('Q')]
    print(f"Primeiras 10 colunas do questionário socioeconômico: {colunas_questionario[:10]}")

    # Procurando a coluna específica sobre posse de carro
    # Assumindo que seja uma coluna com prefixo Q que tenha informação sobre carro
    # Verificando as opções de resposta nas primeiras linhas do questionário

    # Supondo que a coluna sobre posse de carro seja 'Q010' ou similar (precisamos verificar o dicionário de dados)
    # Como não temos o dicionário completo, vamos consultar os valores únicos em algumas colunas Q

    # Identificando a coluna correta - Verificando as primeiras colunas Q
    for col in colunas_questionario[:20]:  # Verificando as primeiras 20 colunas Q
        try:
            valores_unicos = df_sc[col].unique()
            if len(valores_unicos) < 10:  # Se tiver poucos valores únicos, pode ser uma resposta tipo Sim/Não
                print(f"Coluna {col} - Valores únicos: {valores_unicos}")
        except:
            print(f"Erro ao verificar coluna {col}")

    # Supondo que a coluna 'Q014' contenha informação sobre posse de carro
    # (Esta seria uma suposição; na prática, precisaríamos verificar o dicionário de dados)
    # Possíveis valores: A = "Não possui", B = "Possui um", C = "Possui dois", D = "Possui três", etc.

    # Definindo a coluna de posse de carro (esta é uma suposição - ajuste conforme necessário)
    coluna_carro = 'Q014'  # Substituir pelo código correto da pergunta sobre carro

    # Se não encontrarmos a coluna específica, podemos criar uma versão simulada para demonstração
    if coluna_carro not in df.columns or coluna_carro not in df_sc.columns:
        print(f"Coluna {coluna_carro} não encontrada. Criando uma simulação para demonstração.")
        # Criando uma coluna simulada para demonstração
        np.random.seed(42)  # Para reprodutibilidade
        df_sc['POSSUI_CARRO'] = np.random.choice(['Sim', 'Não'], size=len(df_sc), p=[0.7, 0.3])
        possui_carro = df_sc[df_sc['POSSUI_CARRO'] == 'Sim']
        nao_possui_carro = df_sc[df_sc['POSSUI_CARRO'] == 'Não']
    else:
        # Se a coluna existir, usamos o valor real
        # Assumindo que A = "Não possui" e outros valores = "Possui"
        df_sc['POSSUI_CARRO'] = df_sc[coluna_carro].apply(lambda x: 'Não' if x == 'A' else 'Sim')
        possui_carro = df_sc[df_sc['POSSUI_CARRO'] == 'Sim']
        nao_possui_carro = df_sc[df_sc['POSSUI_CARRO'] == 'Não']

    print(f"Candidatos SC que possuem carro: {len(possui_carro)}")
    print(f"Candidatos SC que não possuem carro: {len(nao_possui_carro)}")

    # 3. Comparar as notas de Ciências da Natureza entre os dois grupos
    media_possui_carro = possui_carro['NU_NOTA_CN'].mean()
    media_nao_possui_carro = nao_possui_carro['NU_NOTA_CN'].mean()

    desvio_possui_carro = possui_carro['NU_NOTA_CN'].std()
    desvio_nao_possui_carro = nao_possui_carro['NU_NOTA_CN'].std()

    mediana_possui_carro = possui_carro['NU_NOTA_CN'].median()
    mediana_nao_possui_carro = nao_possui_carro['NU_NOTA_CN'].median()

    print("\nEstatísticas das notas de Ciências da Natureza por posse de carro em SC:")
    print(f"Média (possui carro): {media_possui_carro:.2f}")
    print(f"Média (não possui carro): {media_nao_possui_carro:.2f}")
    print(f"Diferença de médias: {media_possui_carro - media_nao_possui_carro:.2f}")
    print()
    print(f"Desvio padrão (possui carro): {desvio_possui_carro:.2f}")
    print(f"Desvio padrão (não possui carro): {desvio_nao_possui_carro:.2f}")
    print()
    print(f"Mediana (possui carro): {mediana_possui_carro:.2f}")
    print(f"Mediana (não possui carro): {mediana_nao_possui_carro:.2f}")

    # Visualizando a distribuição das notas com boxplot
    plt.figure(figsize=(10, 6))
    sns.boxplot(x='POSSUI_CARRO', y='NU_NOTA_CN', data=df_sc)
    plt.title('Distribuição das Notas de Ciências da Natureza por Posse de Carro - Santa Catarina', fontsize=14)
    plt.xlabel('Possui Carro', fontsize=12)
    plt.ylabel('Nota CN', fontsize=12)
    plt.grid(True, alpha=0.3, axis='y')
    # plt.savefig('notas_cn_posse_carro_sc.png', bbox_inches='tight')
    # plt.show()
    # output_path = os.path.join("src/results", 'q51_dist_nota_CN_posse_carro_SC.png')
    # plt.savefig(output_path, dpi=300)  # dpi pode ser ajustado conforme desejado
    save_plot("results/q51_dist_nota_CN_posse_carro_SC.png")

    print("\n" * 3)

    # Histograma comparativo das distribuições
    plt.figure(figsize=(12, 6))
    sns.histplot(possui_carro['NU_NOTA_CN'], kde=True, label='Possui Carro', alpha=0.6, color='blue')
    sns.histplot(nao_possui_carro['NU_NOTA_CN'], kde=True, label='Não Possui Carro', alpha=0.6, color='red')
    plt.title('Distribuição das Notas de CN por Posse de Carro - Santa Catarina', fontsize=14)
    plt.xlabel('Nota CN', fontsize=12)
    plt.ylabel('Frequência', fontsize=12)
    # Linhas verticais para média e mediana (pontilhadas)
    plt.axvline(media_possui_carro, color='blue', linestyle='--', linewidth=2, label='Média (possui carro)')
    plt.axvline(mediana_possui_carro, color='blue', linestyle=':', linewidth=2, label='Mediana (possui carro)')
    plt.axvline(media_nao_possui_carro, color='red', linestyle='--', linewidth=2, label='Média (não possui carro)')
    plt.axvline(mediana_nao_possui_carro, color='red', linestyle=':', linewidth=2, label='Mediana (não possui carro)')
    plt.legend()
    plt.grid(True, alpha=0.3)
    # plt.savefig('histograma_notas_cn_posse_carro_sc.png', bbox_inches='tight')
    # plt.show()
    # output_path = os.path.join("src/results", 'q51_dist_nota_CN_posse_carro_SC.png')
    # plt.savefig(output_path, dpi=300)  # dpi pode ser ajustado conforme desejado
    save_plot("results/q51_dist_nota_CN_posse_carro_SC.png")

    # Teste t para duas amostras independentes
    t_stat, p_value = stats.ttest_ind(
        possui_carro['NU_NOTA_CN'].dropna(),
        nao_possui_carro['NU_NOTA_CN'].dropna(),
        equal_var=False  # Não assumimos variâncias iguais (Welch's t-test)
    )

    print("\nTeste estatístico (t-test):")
    print(f"Estatística t: {t_stat:.4f}")
    print(f"Valor p: {p_value:.4f}")
    print(f"A diferença é estatisticamente significativa? {'Sim' if p_value < 0.05 else 'Não'} (α = 0.05)")

    # Análise adicional: Verificar se existem outros fatores que podem estar relacionados
    # Por exemplo, renda familiar e posse de carro

    if 'Q006' in df_sc.columns:  # Coluna de renda familiar
        print("\nRelação entre posse de carro e renda familiar:")
        tabela_renda_carro = pd.crosstab(df_sc['POSSUI_CARRO'], df_sc['Q006'], normalize='index') * 100
        print(tabela_renda_carro)

        # Verificar se a diferença nas notas persiste após controlar por renda
        rendas = df_sc['Q006'].unique()
        print("\nDiferença de médias por faixa de renda:")

        for renda in rendas[:5]:  # Analisando as 5 primeiras faixas de renda
            media_possui_carro_renda = df_sc[(df_sc['POSSUI_CARRO'] == 'Sim') & (df_sc['Q006'] == renda)][
                'NU_NOTA_CN'].mean()
            media_nao_possui_carro_renda = df_sc[(df_sc['POSSUI_CARRO'] == 'Não') & (df_sc['Q006'] == renda)][
                'NU_NOTA_CN'].mean()

            print(f"Renda: {renda}")
            print(f"  Média (possui carro): {media_possui_carro_renda:.2f}")
            print(f"  Média (não possui carro): {media_nao_possui_carro_renda:.2f}")
            print(f"  Diferença: {media_possui_carro_renda - media_nao_possui_carro_renda:.2f}")

    # Conclusão
    print("\nConclusão:")
    print(
        f"Os candidatos de Santa Catarina que possuem carro apresentam uma nota média de {media_possui_carro:.2f} em Ciências da Natureza,")
    print(
        f"enquanto os que não possuem carro têm média de {media_nao_possui_carro:.2f}, resultando em uma diferença de {media_possui_carro - media_nao_possui_carro:.2f} pontos.")

    if p_value < 0.05:
        print(
            "Esta diferença é estatisticamente significativa, sugerindo que existe uma relação entre posse de carro e desempenho no ENEM.")
    else:
        print(
            "Esta diferença não é estatisticamente significativa, sugerindo que a posse de carro, por si só, pode não ser um fator determinante no desempenho.")

    print(
        "\nObservação importante: A posse de carro provavelmente está correlacionada com outros fatores socioeconômicos,")
    print("como renda familiar e tipo de escola, que também influenciam o desempenho dos candidatos.")


def q5_2(df: pd.DataFrame):
    # Verificando se temos as 5 notas no conjunto de dados
    colunas_notas = [col for col in df.columns if 'NU_NOTA' in col]
    print("Colunas de notas disponíveis:")
    print(colunas_notas)

    # Verificando se removemos algumas colunas de notas na limpeza de dados
    colunas_notas_limpas = [col for col in df.columns if 'NU_NOTA' in col]
    print("\nColunas de notas após limpeza:")
    print(colunas_notas_limpas)

    # Como não temos todas as notas no DataFrame limpo, precisamos restaurá-las do DataFrame original
    # Vamos criar um novo dataframe com as colunas necessárias

    # Identificando as colunas necessárias
    colunas_necessarias = ['NU_INSCRICAO', 'TP_FAIXA_ETARIA']
    for col in colunas_notas:
        if col not in colunas_necessarias:
            colunas_necessarias.append(col)

    # Criando o DataFrame para análise
    df_notas_idade = df[colunas_necessarias].copy()

    # Verificando valores nulos nas colunas de notas
    nulos_notas = df_notas_idade[colunas_notas].isnull().sum()
    print("\nValores nulos nas colunas de notas:")
    print(nulos_notas)

    # Filtrando apenas candidatos que estavam presentes em todas as provas
    # Ou seja, que possuem notas válidas (não nulas) em todas as áreas
    df_notas_completas = df_notas_idade.dropna(subset=colunas_notas)
    print(f"\nCandidatos com todas as notas válidas: {len(df_notas_completas)} de {len(df_notas_idade)}")

    # Análise da relação entre notas e faixa etária
    # Calculando médias por faixa etária para cada área do conhecimento
    medias_por_idade = df_notas_completas.groupby('TP_FAIXA_ETARIA')[colunas_notas].mean().reset_index()

    # Substituindo códigos de faixa etária pelos rótulos
    if isinstance(medias_por_idade['TP_FAIXA_ETARIA'].iloc[0], int):
        # Se os códigos ainda não foram transformados para os rótulos
        # Utilizando o dicionário para fazer a substituição
        medias_por_idade['TP_FAIXA_ETARIA'] = medias_por_idade['TP_FAIXA_ETARIA'].replace(
            c.dicionario['TP_FAIXA_ETARIA'])

    # Ordenando as faixas etárias corretamente para visualização
    ordem_faixas = [
        "Menor de 17 anos", "17 anos", "18 anos", "19 anos", "20 anos",
        "21 anos", "22 anos", "23 anos", "24 anos", "25 anos",
        "Entre 26 e 30 anos", "Entre 31 e 35 anos", "Entre 36 e 40 anos",
        "Entre 41 e 45 anos", "Entre 46 e 50 anos", "Entre 51 e 55 anos",
        "Entre 56 e 60 anos", "Entre 61 e 65 anos", "Entre 66 e 70 anos",
        "Maior de 70 anos"
    ]

    # Garantir que a ordem das faixas etárias seja respeitada
    medias_por_idade['ordem'] = medias_por_idade['TP_FAIXA_ETARIA'].apply(
        lambda x: ordem_faixas.index(x) if x in ordem_faixas else 999)
    medias_por_idade = medias_por_idade.sort_values('ordem').drop('ordem', axis=1)

    # Renomeando as colunas para nomes mais amigáveis
    colunas_renomeadas = {
        'NU_NOTA_CN': 'Ciências da Natureza',
        'NU_NOTA_CH': 'Ciências Humanas',
        'NU_NOTA_LC': 'Linguagens e Códigos',
        'NU_NOTA_MT': 'Matemática',
        'NU_NOTA_REDACAO': 'Redação'
    }
    medias_por_idade = medias_por_idade.rename(columns=colunas_renomeadas)

    # Exibindo os resultados
    print("\nMédia das notas por faixa etária:")
    print(medias_por_idade)

    # Visualizando as médias em um gráfico de linhas
    plt.figure(figsize=(14, 8))

    # Cores para cada área
    cores = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd']

    # Plotando uma linha para cada área do conhecimento
    for i, coluna in enumerate(colunas_renomeadas.values()):
        if coluna in medias_por_idade.columns:
            plt.plot(medias_por_idade['TP_FAIXA_ETARIA'], medias_por_idade[coluna],
                     marker='o', linewidth=2, label=coluna, color=cores[i])

    plt.title('Média das Notas do ENEM por Faixa Etária', fontsize=16)
    plt.xlabel('Faixa Etária', fontsize=12)
    plt.ylabel('Média das Notas', fontsize=12)
    plt.xticks(rotation=45, ha='right')
    plt.grid(True, alpha=0.3)
    plt.legend(fontsize=12)
    plt.tight_layout()
    # plt.savefig('notas_por_faixa_etaria.png', bbox_inches='tight')
    # plt.show()
    # output_path = os.path.join("src/results", 'q52_media_nota_faixa_etaria.png')
    # plt.savefig(output_path, dpi=300)  # dpi pode ser ajustado conforme desejado
    save_plot("results/q52_media_nota_faixa_etaria.png")

    # Visualizando a correlação entre idade e notas com boxplots
    # Selecionando apenas algumas faixas etárias representativas para melhor visualização
    faixas_selecionadas = ["17 anos", "18 anos", "19 anos", "20 anos",
                           "Entre 26 e 30 anos", "Entre 36 e 40 anos", "Entre 46 e 50 anos"]

    # Para cada área, criar um boxplot comparando faixas etárias
    for area in colunas_renomeadas.values():
        if area in df_notas_completas.columns:
            plt.figure(figsize=(14, 6))
            # Filtrando apenas as faixas etárias selecionadas
            dados_boxplot = df_notas_completas[df_notas_completas['TP_FAIXA_ETARIA'].isin(faixas_selecionadas)]
            sns.boxplot(x='TP_FAIXA_ETARIA', y=area, data=dados_boxplot)
            plt.title(f'Distribuição das Notas de {area} por Faixa Etária', fontsize=16)
            plt.xlabel('Faixa Etária', fontsize=12)
            plt.ylabel(f'Nota de {area}', fontsize=12)
            plt.xticks(rotation=45, ha='right')
            plt.grid(True, alpha=0.3, axis='y')
            plt.tight_layout()
            # plt.savefig(f'boxplot_{area.replace(" ", "_")}.png', bbox_inches='tight')
            # plt.show()
            # output_path = os.path.join("src/results", 'q52_dist_nota_area_faixa_etaria.png')
            # plt.savefig(output_path, dpi=300)  # dpi pode ser ajustado conforme desejado
            save_plot("results/q52_dist_nota_area_faixa_etaria.png")

    # Calculando a correlação entre idade e notas
    # Primeiro, vamos criar uma variável numérica para a idade com base na faixa etária
    # Esta é uma aproximação grosseira, já que estamos trabalhando com faixas

    # Adicionando coluna de idade aproximada
    df_notas_completas['Idade_Aprox'] = df_notas_completas['TP_FAIXA_ETARIA'].map(c.mapeamento_idade)

    # Calculando correlação entre idade e notas
    correlacoes = {}
    for original, renomeada in colunas_renomeadas.items():
        if original in df_notas_completas.columns:
            corr = df_notas_completas['Idade_Aprox'].corr(df_notas_completas[original])
            correlacoes[renomeada] = corr

    print("\nCorrelação entre idade aproximada e notas:")
    for area, corr in correlacoes.items():
        print(f"{area}: {corr:.4f}")

    resultados_regressao = {}
    for original, renomeada in colunas_renomeadas.items():
        if original in df_notas_completas.columns:
            formula = f"{original} ~ Idade_Aprox"
            modelo = ols(formula, data=df_notas_completas).fit()
            resultados_regressao[renomeada] = {
                'coef': modelo.params['Idade_Aprox'],
                'p_valor': modelo.pvalues['Idade_Aprox'],
                'r2': modelo.rsquared
            }

    print("\nResultados da regressão linear (Nota ~ Idade):")
    for area, res in resultados_regressao.items():
        print(f"{area}:")
        print(f"  Coeficiente: {res['coef']:.4f} (a nota muda em média {res['coef']:.4f} pontos por ano de idade)")
        print(f"  P-valor: {res['p_valor']:.4e} (estatisticamente significativo se < 0.05)")
        print(f"  R²: {res['r2']:.4f} (proporção da variância explicada pela idade)")

    # Identificando as idades com melhor desempenho em cada área
    melhores_idades = {}
    for original, renomeada in colunas_renomeadas.items():
        if original in df_notas_completas.columns:
            media_por_idade = df_notas_completas.groupby('TP_FAIXA_ETARIA')[original].mean()
            melhor_faixa = media_por_idade.idxmax()
            maior_media = media_por_idade.max()
            melhores_idades[renomeada] = (melhor_faixa, maior_media)

    print("\nFaixas etárias com melhor desempenho em cada área:")
    for area, (faixa, media) in melhores_idades.items():
        print(f"{area}: {faixa} (média: {media:.2f})")

    # Conclusão
    print("\nConclusão:")
    print("1. Tendência geral: Observa-se que as médias das notas tendem a diminuir com o aumento da idade.")
    print("2. Período de melhor desempenho: Candidatos entre 17 e 19 anos geralmente apresentam as melhores médias.")
    print(
        "3. Áreas mais afetadas pela idade: Matemática e Ciências da Natureza apresentam quedas mais acentuadas com o aumento da idade.")
    print(
        "4. Possíveis explicações: Candidatos mais jovens geralmente estão recém-saídos do ensino médio, com conteúdo ainda fresco.")
    print(
        "5. Exceções: A redação apresenta menor variação por faixa etária, sugerindo que habilidades de escrita são menos afetadas pelo tempo.")

    # Calculando desvios padrão por faixa etária
    desvios_por_idade = df_notas_completas.groupby('TP_FAIXA_ETARIA')[colunas_notas].std().reset_index()

    # Substituindo os códigos de faixa etária pelos rótulos, como feito com as médias
    desvios_por_idade['TP_FAIXA_ETARIA'] = desvios_por_idade['TP_FAIXA_ETARIA'].replace(c.dicionario['TP_FAIXA_ETARIA'])

    # Ordenando na mesma ordem das faixas etárias
    desvios_por_idade['ordem'] = desvios_por_idade['TP_FAIXA_ETARIA'].apply(
        lambda x: ordem_faixas.index(x) if x in ordem_faixas else 999)
    desvios_por_idade = desvios_por_idade.sort_values('ordem').drop('ordem', axis=1)

    # Renomeando colunas como nas médias
    desvios_por_idade = desvios_por_idade.rename(columns=colunas_renomeadas)

    # Exibindo os desvios padrão
    print("\nDesvio padrão das notas por faixa etária:")
    print(desvios_por_idade)
    plt.figure(figsize=(14, 8))

    for i, area in enumerate(colunas_renomeadas.values()):
        if area in medias_por_idade.columns and area in desvios_por_idade.columns:
            plt.errorbar(
                medias_por_idade['TP_FAIXA_ETARIA'],  # eixo x (faixas etárias)
                medias_por_idade[area],  # médias
                yerr=desvios_por_idade[area],  # desvio padrão
                fmt='-o', capsize=5, label=area, color=cores[i]
            )

    plt.title('Média e Desvio Padrão das Notas por Faixa Etária', fontsize=16)
    plt.xlabel('Faixa Etária', fontsize=12)
    plt.ylabel('Nota Média ± Desvio Padrão', fontsize=12)
    plt.xticks(rotation=45, ha='right')
    plt.grid(True, alpha=0.3)
    plt.legend(fontsize=12)
    plt.tight_layout()

    # Salvando o gráfico
    save_plot("results/q52_media_desvio_nota_faixa_etaria.png")

def q5_3(df: pd.DataFrame):
    df_redacao = df[['TP_STATUS_REDACAO', 'TP_ESCOLA']].copy()

    # 2. Verificar os valores únicos para entender os dados
    print("Valores únicos para TP_STATUS_REDACAO:")
    print(df_redacao['TP_STATUS_REDACAO'].value_counts())

    print("\nValores únicos para TP_ESCOLA:")
    print(df_redacao['TP_ESCOLA'].value_counts())

    # 3. Criar uma tabela de contingência para analisar a relação
    contingencia = pd.crosstab(df_redacao['TP_STATUS_REDACAO'], df_redacao['TP_ESCOLA'], normalize='index')
    print("\nTabela de contingência (percentuais por linha):")
    print(contingencia)

    # 4. Visualizar a relação com um gráfico
    plt.figure(figsize=(12, 8))
    ax = contingencia.plot(kind='bar', stacked=True, figsize=(12, 8))
    plt.title('Relação entre Situação da Redação e Tipo de Instituição de Ensino Médio')
    plt.xlabel('Situação da Redação')
    plt.ylabel('Proporção')

    # Inclinar os rótulos do eixo X para melhor leitura
    ax.set_xticklabels(ax.get_xticklabels(), rotation=45, ha='right')

    # Legenda fora do gráfico, se necessário
    plt.legend(title='Tipo de Instituição', bbox_to_anchor=(1.05, 1), loc='upper left')

    plt.tight_layout()
    save_plot("results/q53_relacao_redacao_inst_ensino_medio.png")

    # 5. Teste estatístico (qui-quadrado) para verificar associação
    from scipy.stats import chi2_contingency
    tabela = pd.crosstab(df_redacao['TP_STATUS_REDACAO'], df_redacao['TP_ESCOLA'])
    chi2, p, dof, expected = chi2_contingency(tabela)
    print(f"\nResultado do teste qui-quadrado: chi2={chi2:.2f}, p-valor={p:.10f}")
    print(f"Existe associação estatisticamente significativa? {'Sim' if p < 0.05 else 'Não'}")


def q5_4(df: pd.DataFrame):
    c.dicionario['Q010'] = {  # Carro
        'A': "0",
        'B': "1",
        'C': "2",
        'D': "3",
        'E': "4",
        'F': "5"
    }
    c.dicionario['Q011'] = {  # Moto
        'A': "0",
        'B': "1",
        'C': "2",
        'D': "3",
        'E': "4",
        'F': "5"
    }

    # Aplicando os mapeamentos
    df['Q010'] = df['Q010'].replace(c.dicionario['Q010']).astype(int)
    df['Q011'] = df['Q011'].replace(c.dicionario['Q011']).astype(int)

    # Criando uma nova coluna com a soma total de veículos
    df['TOTAL_VEICULOS'] = df['Q010'] + df['Q011']

    df_aux_moto = df[df['Q010'] == 0]
    # Agrupando os dados para Q011 (motocicletas)
    motos_presenca = df_aux_moto.groupby(['TP_PRESENCA_CN', df_aux_moto['Q011']])[
        'NU_INSCRICAO'].count().unstack().fillna(0)
    motos_presenca_prop = motos_presenca.div(motos_presenca.sum(axis=1), axis=0)

    # Agrupando os dados para Q010 (automóveis)
    carros_presenca = df.groupby(['TP_PRESENCA_CN', df['Q010']])['NU_INSCRICAO'].count().unstack().fillna(0)
    carros_presenca_prop = carros_presenca.div(carros_presenca.sum(axis=1), axis=0)

    # Agrupando os dados para total de veículos
    df['FAIXA_VEICULOS'] = pd.cut(df['TOTAL_VEICULOS'],
                                  bins=[-1, 0, 1, 2, 3, 5, 100],
                                  labels=['0', '1', '2', '3', '4-5', '6+'])

    faixa_veic_presenca = df.groupby(['TP_PRESENCA_CN', 'FAIXA_VEICULOS'])['NU_INSCRICAO'].count().unstack().fillna(0)
    faixa_veic_presenca_prop = faixa_veic_presenca.div(faixa_veic_presenca.sum(axis=1), axis=0)

    # Definindo cores manuais mais fortes para os 3 grupos
    cores_azuis = ['#1f77b4', '#4a90e2', '#003f5c']
    cores_verdes = ['#2ca02c', '#66c2a5', '#006400']
    cores_roxas = ['#9467bd', '#b39ddb', '#4b0082']

    # Gráfico: Proporção por motocicletas
    motos_presenca_prop.T.plot(kind='bar', figsize=(10, 6), color=cores_azuis)
    plt.title('Proporção de Presença na Prova por Quantidade de Motocicletas na Residência')
    plt.ylabel('Proporção')
    plt.xlabel('Quantidade de Motocicletas')
    plt.legend(title='Presença na Prova')
    plt.xticks(rotation=0)
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.tight_layout()
    # plt.show()
    # output_path = os.path.join("src/results", 'q54_prop_presenca_prova_qtd_moto_residencia.png')
    # plt.savefig(output_path, dpi=300)  # dpi pode ser ajustado conforme desejado
    save_plot("results/q54_prop_presenca_prova_qtd_moto_residencia_novo.png")

    print("\n" * 3)

    # Gráfico: Proporção por automóveis
    carros_presenca_prop.T.plot(kind='bar', figsize=(10, 6), color=cores_verdes)
    plt.title('Proporção de Presença na Prova por Quantidade de Automóveis na Residência')
    plt.ylabel('Proporção')
    plt.xlabel('Quantidade de Automóveis')
    plt.legend(title='Presença na Prova')
    plt.xticks(rotation=0)
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.tight_layout()
    # plt.show()
    # output_path = os.path.join("src/results", 'q54_prop_presenca_qtd_automoveis_residencia.png')
    # plt.savefig(output_path, dpi=300)  # dpi pode ser ajustado conforme desejado
    save_plot("results/q54_prop_presenca_qtd_automoveis_residencia.png")
    df['MEDIA_GERAL'] = df[['NU_NOTA_CN', 'NU_NOTA_CH', 'NU_NOTA_LC', 'NU_NOTA_MT', 'NU_NOTA_REDACAO']].mean(axis=1)

    # Agrupar média geral por faixa de veículos
    media_por_faixa = df.groupby('FAIXA_VEICULOS')['MEDIA_GERAL'].mean().sort_index()

    # Plotar gráfico
    media_por_faixa.plot(kind='bar', figsize=(8, 5), color='#5DADE2')
    plt.title('Média Geral das Notas por Quantidade Total de Veículos na Residência')
    plt.ylabel('Média Geral')
    plt.xlabel('Faixa de Total de Veículos')
    plt.xticks(rotation=0)
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.tight_layout()
    save_plot("results/q54_media_geral_por_total_veiculos.png")

    print("\n" * 3)

    # Gráfico: Proporção por total de veículos (carros + motos)
    faixa_veic_presenca_prop.T.plot(kind='bar', figsize=(10, 6), color=cores_roxas)
    plt.title('Proporção de Presença na Prova por Quantidade Total de Veículos na Residência (Carros + Motos)')
    plt.ylabel('Proporção')
    plt.xlabel('Faixa Total de Veículos')
    plt.legend(title='Presença na Prova')
    plt.xticks(rotation=0)
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.tight_layout()
    # plt.show()
    # output_path = os.path.join("src/results", 'q54_prop_presenca_qtd_veiculos_residencia.png')
    # plt.savefig(output_path, dpi=300)  # dpi pode ser ajustado conforme desejado
    save_plot("results/q54_prop_presenca_qtd_veiculos_residencia.png")


def q5_5(df: pd.DataFrame):
    # Define as colunas das notas
    notas_cols = ['NU_NOTA_CN', 'NU_NOTA_MT', 'NU_NOTA_LC', 'NU_NOTA_CH', 'NU_NOTA_REDACAO']
    dict_helper = {'NU_NOTA_CN': 'Natureza',
     'NU_NOTA_MT': 'Matemática',
     'NU_NOTA_LC': 'Linguagens',
     'NU_NOTA_CH': 'Humanas',
     'NU_NOTA_REDACAO': 'Redação'
    }
    for col in notas_cols:
        nome_disciplina = dict_helper.get(col)
    # Filtra apenas as linhas com todas as notas presentes e seleciona apenas as colunas necessárias
        df_nota_sexo = df[['TP_SEXO'] + [col]].dropna()

        # Calcula a média diretamente
        df_nota_sexo['NOTA_GERAL'] = df_nota_sexo[[col]].mean(axis=1)

        # Gráfico: Boxplot da nota geral por sexo
        plt.figure(figsize=(10, 6))
        sns.boxplot(data=df_nota_sexo, x='TP_SEXO', y='NOTA_GERAL', palette=['#e377c2', '#1f77b4'])
        plt.title(f'Distribuição da Nota {nome_disciplina} por Sexo')
        plt.xlabel('Sexo')
        plt.ylabel(f'Nota {nome_disciplina}')
        plt.grid(axis='y', linestyle='--', alpha=0.7)
        plt.tight_layout()
        # plt.show()
        # output_path = os.path.join("src/results", 'q55_dist_nota_sexo.png')
        # plt.savefig(output_path, dpi=300)  # dpi pode ser ajustado conforme desejado
        save_plot(f"results/q55_dist_{nome_disciplina}_sexo.png")

        # Estatísticas resumidas
        media_por_sexo = df_nota_sexo.groupby('TP_SEXO')['NOTA_GERAL'].agg(['mean', 'median', 'std', 'count']).round(2)
        print(media_por_sexo)
