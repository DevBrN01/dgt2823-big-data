"""Limpeza do conjunto obrigatório, seguindo os passos 1 a 13 do roteiro."""

from pathlib import Path

import pandas as pd


def main():
    pasta = Path(__file__).resolve().parent

    # Passos 1 a 4: importar o CSV fornecido pela disciplina.
    dados_originais = pd.read_csv(
        pasta / "dados" / "atividades.csv",
        sep=";",
        engine="python",
        encoding="utf-8",
    )

    # Passo 5: verificar a importação, usando N = 10.
    print("PASSO 5 - Informações dos dados originais")
    dados_originais.info(memory_usage="deep")
    print("\nPrimeiras 10 linhas:")
    print(dados_originais.head(10))
    print("\nÚltimas 10 linhas:")
    print(dados_originais.tail(10))
    print("\nValores nulos por coluna:")
    print(dados_originais.isna().sum())

    # Passo 6: tratar uma cópia, preservando os dados importados.
    dados_tratados = dados_originais.copy(deep=True)

    # Passo 7: preencher as calorias ausentes dos IDs 18 e 28 com zero.
    dados_tratados["Calories"] = dados_tratados["Calories"].fillna(0)
    print("\nPASSO 7 - Calories com nulos substituídos por zero")
    print(dados_tratados.to_string(index=False))

    # Passo 8: preencher a data ausente com o marcador exigido no roteiro.
    dados_tratados["Date"] = dados_tratados["Date"].fillna("1900/01/01")
    print("\nPASSO 8 - Date com o marcador 1900/01/01")
    print(dados_tratados.to_string(index=False))

    # As aspas simples fazem parte dos valores do CSV original.
    # Esse formato explícito reproduz os erros didáticos do enunciado.
    formato_original = "'%Y/%m/%d'"
    print("\nPASSO 8 - Primeira tentativa de conversão de Date")
    try:
        dados_tratados["Date"] = pd.to_datetime(
            dados_tratados["Date"], format=formato_original, errors="raise"
        )
    except ValueError as erro:
        print(f"Erro de conversão previsto pelo roteiro: {erro}")

    # Passo 9: devolver o marcador a um nulo real, e tentar novamente.
    # float('nan') é NaN; a string literal 'NaN' não é usada como substituto.
    dados_tratados["Date"] = dados_tratados["Date"].replace(
        "1900/01/01", float("nan")
    )
    print("\nPASSO 9 - Marcador substituído por NaN")
    print(dados_tratados.to_string(index=False))
    try:
        dados_tratados["Date"] = pd.to_datetime(
            dados_tratados["Date"], format=formato_original, errors="raise"
        )
    except ValueError as erro:
        print(f"Segundo erro de conversão previsto pelo roteiro: {erro}")

    # Passo 10: combinar replace e to_datetime para corrigir só 20201226.
    # Primeiro, interpretar a data compacta. Depois, padronizar a sua escrita
    # com as mesmas aspas dos demais valores, para a conversão da coluna.
    data_corrigida = pd.to_datetime("20201226", format="%Y%m%d")
    dados_tratados["Date"] = dados_tratados["Date"].replace(
        "20201226", data_corrigida.strftime(formato_original)
    )
    print("\nPASSO 10 - Data do ID 26 padronizada")
    print(dados_tratados.to_string(index=False))

    # Passo 11: agora todos os valores não nulos seguem o mesmo formato.
    # NaN é convertido em NaT, o marcador de data ausente do Pandas.
    dados_tratados["Date"] = pd.to_datetime(
        dados_tratados["Date"], format=formato_original, errors="raise"
    )
    print("\nPASSO 11 - Coluna Date convertida para datetime")
    print(dados_tratados.to_string(index=False))
    print(f"Tipo de Date: {dados_tratados['Date'].dtype}")

    # Passo 12: remover apenas registros sem data. O ID 22 será removido.
    dados_tratados = dados_tratados.dropna(subset=["Date"])

    # Passo 13: exibir o resultado e comprovar a ausência de nulos.
    print("\nPASSO 13 - Dataframe final")
    print(dados_tratados.to_string(index=False))
    print("\nInformações finais:")
    dados_tratados.info(memory_usage="deep")
    print("\nValores nulos após a limpeza:")
    print(dados_tratados.isna().sum())
    print(f"\nLinhas: {len(dados_originais)} originais; {len(dados_tratados)} finais.")

    # Salvar também o resultado para consulta. CSV não armazena tipos:
    # uma leitura posterior precisa de parse_dates=['Date'].
    saida = pasta / "resultados" / "atividades_tratadas.csv"
    saida.parent.mkdir(parents=True, exist_ok=True)
    dados_tratados.to_csv(
        saida, sep=";", index=False, encoding="utf-8", date_format="%Y-%m-%d"
    )
    print("Arquivo gerado: resultados/atividades_tratadas.csv")
    return dados_originais, dados_tratados


if __name__ == "__main__":
    main()
