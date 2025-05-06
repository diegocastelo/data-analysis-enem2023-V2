
csv_microdados_path = "data/MICRODADOS_ENEM_2023.csv"

columns_to_remove = ['TP_PRESENCA_CH', 'TP_PRESENCA_LC', 'TP_PRESENCA_MT',
                             'CO_PROVA_CH', 'CO_PROVA_LC', 'CO_PROVA_MT',
                             'NU_NOTA_CH', 'NU_NOTA_LC', 'NU_NOTA_MT',
                             'TX_RESPOSTAS_CH', 'TX_RESPOSTAS_LC', 'TX_RESPOSTAS_MT',
                             'TP_LINGUA',
                             'TX_GABARITO_CH', 'TX_GABARITO_LC', 'TX_GABARITO_MT',
                            'NU_NOTA_COMP1', 'NU_NOTA_COMP2', 'NU_NOTA_COMP3', 'NU_NOTA_COMP4',
                             'NU_NOTA_COMP5', 'NU_NOTA_REDACAO']

columns_to_remove_redacao = ['TP_PRESENCA_CH', 'TP_PRESENCA_LC', 'TP_PRESENCA_MT',
                             'CO_PROVA_CH', 'CO_PROVA_LC', 'CO_PROVA_MT',
                             'TX_RESPOSTAS_CH', 'TX_RESPOSTAS_LC', 'TX_RESPOSTAS_MT',
                             'TP_LINGUA',
                             'TX_GABARITO_CH', 'TX_GABARITO_LC', 'TX_GABARITO_MT',
                             'NU_NOTA_COMP1', 'NU_NOTA_COMP2', 'NU_NOTA_COMP3', 'NU_NOTA_COMP4',
                             'NU_NOTA_COMP5']
regioes = {
        'Norte': ['AC', 'AM', 'AP', 'PA', 'RO', 'RR', 'TO'],
        'Nordeste': ['AL', 'BA', 'CE', 'MA', 'PB', 'PE', 'PI', 'RN', 'SE'],
        'Centro-Oeste': ['DF', 'GO', 'MS', 'MT'],
        'Sudeste': ['ES', 'MG', 'RJ', 'SP'],
        'Sul': ['PR', 'RS', 'SC']
}

mapeamento_idade = {
        "Menor de 17 anos": 16,
        "17 anos": 17,
        "18 anos": 18,
        "19 anos": 19,
        "20 anos": 20,
        "21 anos": 21,
        "22 anos": 22,
        "23 anos": 23,
        "24 anos": 24,
        "25 anos": 25,
        "Entre 26 e 30 anos": 28,
        "Entre 31 e 35 anos": 33,
        "Entre 36 e 40 anos": 38,
        "Entre 41 e 45 anos": 43,
        "Entre 46 e 50 anos": 48,
        "Entre 51 e 55 anos": 53,
        "Entre 56 e 60 anos": 58,
        "Entre 61 e 65 anos": 63,
        "Entre 66 e 70 anos": 68,
        "Maior de 70 anos": 75
    }

dicionario = {
    "TP_FAIXA_ETARIA": {
        1: "Menor de 17 anos",
        2: "17 anos",
        3: "18 anos",
        4: "19 anos",
        5: "20 anos",
        6: "21 anos",
        7: "22 anos",
        8: "23 anos",
        9: "24 anos",
        10: "25 anos",
        11: "Entre 26 e 30 anos",
        12: "Entre 31 e 35 anos",
        13: "Entre 36 e 40 anos",
        14: "Entre 41 e 45 anos",
        15: "Entre 46 e 50 anos",
        16: "Entre 51 e 55 anos",
        17: "Entre 56 e 60 anos",
        18: "Entre 61 e 65 anos",
        19: "Entre 66 e 70 anos",
        20: "Maior de 70 anos"
    },
    "TP_SEXO": {
        'M': "Masculino",
        'F': "Feminino"
    },
    "TP_ESTADO_CIVIL": {
        0: "Não informado",
        1: "Solteiro(a)",
        2: "Casado(a)/Mora com companheiro(a)",
        3: "Divorciado(a)/Desquitado(a)/Separado(a)",
        4: "Viúvo(a)"
    },
    "TP_STATUS_REDACAO": {
        1: "Sem problemas",
        2: "Anulada",
        3: "Cópia Texto Motivador",
        4: "Em Branco",
        6: "Fuga ao tema",
        7: "Não atendimento ao tipo textual",
        8: "Texto insuficiente",
        9: "Parte desconectada",
    },
    "TP_COR_RACA": {
        0: "Não declarado",
        1: "Branca",
        2: "Preta",
        3: "Parda",
        4: "Amarela",
        5: "Indígena",
        6: "Não dispõe da informação"
    },
    "TP_NACIONALIDADE": {
        0: "Não informado",
        1: "Brasileiro(a)",
        2: "Brasileiro(a) Naturalizado(a)",
        3: "Estrangeiro(a)",
        4: "Brasileiro(a) Nato(a), nascido(a) no exterior"
    },
    "TP_ST_CONCLUSAO": {
        1: "Já concluí o Ensino Médio",
        2: "Estou cursando e concluirei o Ensino Médio em 2023",
        3: "Estou cursando e concluirei o Ensino Médio após 2023",
        4: "Não concluí e não estou cursando o Ensino Médio"
    },
    "TP_ANO_CONCLUIU": {
        0: "Não informado",
        1: "2022",
        2: "2021",
        3: "2020",
        4: "2019",
        5: "2018",
        6: "2017",
        7: "2016",
        8: "2015",
        9: "2014",
        10: "2013",
        11: "2012",
        12: "2011",
        13: "2010",
        14: "2009",
        15: "2008",
        16: "2007",
        17: "Antes de 2007"
    },
    "TP_ESCOLA": {
        1: "Não Respondeu",
        2: "Pública",
        3: "Privada"
    },
    "TP_ENSINO": {
        1: "Ensino Regular",
        2: "Educação Especial - Modalidade Substitutiva"
    },
    "IN_TREINEIRO": {
        1: "Sim",
        0: "Não"
    },
    "TP_DEPENDENCIA_ADM_ESC": {
        1: "Federal",
        2: "Estadual",
        3: "Municipal",
        4: "Privada"

    },
    "TP_LOCALIZACAO_ESC": {
        1: "Urbana",
        2: "Rural"
    },
    "TP_SIT_FUNC_ESC": {
        1: "Em atividade",
        2: "Paralisada",
        3: "Extinta",
        4: "Escola extinta em anos anteriores."

    },
    "TP_PRESENCA_CN": {
        0: "Faltou à prova",
        1: "Presente na prova",
        2: "Eliminado na prova"
    },
    "CO_PROVA_CN": {
        1221: "Azul",
        1222: "Amarela",
        1223: "Rosa",
        1224: "Cinza",
        1225: "Rosa - Ampliada",
        1226: "Rosa - Superampliada",
        1227: "Laranja - Braile",
        1228: "Laranja - Adaptada Ledor",
        1229: "Verde - Videoprova - Libras",
        1301: "Azul (Reaplicação)",
        1302: "Amarela (Reaplicação)",
        1303: "Cinza (Reaplicação)",
        1304: "Rosa (Reaplicação)"
    },
    "Q006": {
        'A': "Nenhuma Renda",
        'B': "Até R$ 1.320,00",
        'C': "De R$ 1.320,01 até R$ 1.980,00.",
        'D': "De R$ 1.980,01 até R$ 2.640,00.",
        'E': "De R$ 2.640,01 até R$ 3.300,00.",
        'F': "De R$ 3.300,01 até R$ 3.960,00.",
        'G': "De R$ 3.960,01 até R$ 5.280,00.",
        'H': "De R$ 5.280,01 até R$ 6.600,00.",
        'I': "De R$ 6.600,01 até R$ 7.920,00.",
        'J': "De R$ 7.920,01 até R$ 9240,00.",
        'K': "De R$ 9.240,01 até R$ 10.560,00.",
        'L': "De R$ 10.560,01 até R$ 11.880,00.",
        'M': "De R$ 11.880,01 até R$ 13.200,00.",
        'N': "De R$ 13.200,01 até R$ 15.840,00.",
        'O': "De R$ 15.840,01 até R$19.800,00.",
        'P': "De R$ 19.800,01 até R$ 26.400,00.",
        'Q': "Acima de R$ 26.400,00."
    },
    "Q001": {
        'A': "Nunca estudou.",
        'B': "4ª/5º ano EF incompleto.",
        'C': "4ª/5º ano completo, 8ª/9º ano EF incompleto.",
        'D': "8ª/9º ano EF, Ensino Médio incompleto.",
        'E': "Ensino Médio completo, Faculdade incompleta.",
        'F': "Faculdade completa, Pós-graduação incompleta.",
        'G': "Pós-graduação completa.",
        'H': "Não sei."
    },
    "Q002": {
        'A': "Nunca estudou.",
        'B': "4ª/5º ano EF incompleto.",
        'C': "4ª/5º ano completo, 8ª/9º ano EF incompleto.",
        'D': "8ª/9º ano EF, Ensino Médio incompleto.",
        'E': "Ensino Médio completo, Faculdade incompleta.",
        'F': "Faculdade completa, Pós-graduação incompleta.",
        'G': "Pós-graduação completa.",
        'H': "Não sei."
    },
    "Q025": {
        'A': "Não.",
        'B': "Sim."
    }
}