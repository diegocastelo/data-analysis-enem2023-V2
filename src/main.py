from controllers.data_controller import DataController
import helpers.data_helper as h
import helpers.questions_helper as qh


if __name__ == '__main__':
    dataController = DataController()

    dataController.handle_df_microdados()
    # Informações básicas
    h.show_basic_information(dataController.df_microdados_enem)

    dataController.clean_columns()
    h.show_cleaned_df_infos(dataController.cleaned_df)

    dataController.filter_disqualified()
    h.show_disqualified_info(dataController.cleaned_df)

    # Valores nulos
    h.show_null_columns(dataController.cleaned_df)

    # Tratamento de Dados Nulos
    dataController.handle_null_data()

    # 1) Distribuição de Notas
    # qh.q1(dataController.cleaned_df)

    # 2)  Fatores Socioeconômicos

    # A escolaridade dos pais impacta as notas de Ciências da Natureza?
    # Existe uma correlação entre a escolaridade dos pais e o desempenho na prova de Ciências da Natureza?
    # Essa relação varia entre diferentes tipos de escola?
    # qh.q2_1(dataController.cleaned_df)

    # Os candidatos que têm acesso diário à internet apresentam um desempenho significativamente superior na prova de
    # Ciências da Natureza em comparação com aqueles que não têm?
    # O acesso à internet influencia no desempenho na prova de Ciências da Natureza?
    # qh.q2_2(dataController.cleaned_df)

    # 3) Características da Escola

    # Existe diferença de desempenho entre alunos de escolas públicas e privadas?
    # O desempenho entre escolas públicas e privadas varia mais em determinadas regiões do país?
    # Como essas diferenças se comparam entre capitais e cidades do interior?
    # qh.q3_1(dataController.cleaned_df)

    # O desempenho na prova de Ciências da Natureza varia conforme a localização da escola (urbana x rural)?
    # qh.q3_2(dataController.cleaned_df)

    # O estado de localização da escola influencia o desempenho dos alunos?
    # Existem estados que apresentam um desempenho consistentemente melhor ou pior?
    # Quais possíveis fatores podem explicar essas diferenças?
    # qh.q3_3(dataController.cleaned_df)

    # 4) Características da Escola

    # Como está distribuída a média das notas de Ciências da Natureza por município de aplicação da prova?
    # Quais municípios apresentam as maiores médias na prova de Ciências da Natureza?
    # Essas médias têm relação com IDH ou nível educacional da população?
    # municipios_relevantes = qh.q4_1(dataController.cleaned_df)

    # Quais municípios apresentam a maior e a menor variação de notas?
    # A variação das notas entre municípios está mais associada a diferenças na estrutura escolar ou a fatores socioeconômicos?
    # qh.q4_2(dataController.cleaned_df, municipios_relevantes)

    # 5) Formulação de Novas Perguntas
    dataController.handle_df_enem()

    # Qual a relação das notas dos candidatos de Santa Catarina que possuem carro em casa e os que não possuem?
    # qh.q5_1(dataController.df_microdados_enem)

    # Qual a relação das 5 notas com a idade do candidato?
    # qh.q5_2(dataController.df_microdados_enem)

    # Existe uma relação entre a situação da redação do participante e o tipo de instituição que concluiu ou concluirá o Ensino Médio?
    # qh.q5_3(dataController.df_microdados_enem)

    # Existe alguma relação entre os candidatos faltantes e a presença de veículos em suas casas?
    qh.q5_4(dataController.df_microdados_enem)

    # Existe alguma relação entre o sexo do participante e a nota geral do enem?
    qh.q5_5(dataController.df_microdados_enem)

    print("Fim")
