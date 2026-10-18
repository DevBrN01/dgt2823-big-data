"""As cinco microatividades de apoio da disciplina DGT2823."""

from pathlib import Path

import pandas as pd


def main():
    arquivo = Path(__file__).resolve().parent / "dados" / "atividades.csv"

    # 1. O separador do material é ponto e vírgula.
    dados = pd.read_csv(arquivo, sep=";", engine="python", encoding="utf-8")
    print("MICROATIVIDADE 1 - Leitura do CSV")
    print(dados)

    # 2. Uma lista de nomes seleciona três colunas do dataframe original.
    subconjunto = dados[["Duration", "Pulse", "Calories"]].copy()
    print("\nMICROATIVIDADE 2 - Subconjunto de três colunas")
    print(subconjunto)

    # 3. max_rows controla a representação habitual; to_string exibe tudo.
    pd.set_option("display.max_rows", 9999)
    print("\nMICROATIVIDADE 3 - max_rows = 9999 e to_string()")
    print(dados.to_string())

    # 4. head e tail recebem a quantidade de linhas desejada.
    print("\nMICROATIVIDADE 4 - Primeiras 10 linhas")
    print(dados.head(10))
    print("\nÚltimas 10 linhas")
    print(dados.tail(10))

    # 5. info escreve na saída; não é necessário usar print(dados.info()).
    print("\nMICROATIVIDADE 5 - Informações gerais")
    dados.info(memory_usage="deep")
    print(f"\nTotal de linhas: {dados.shape[0]}")
    print(f"Total de colunas: {dados.shape[1]}")
    print("\nValores nulos por coluna:")
    print(dados.isna().sum())
    print(f"Total de células nulas: {dados.isna().sum().sum()}")
    print("\nTipos de dados:")
    print(dados.dtypes)
    print("\nMemória por coluna e índice (bytes):")
    print(dados.memory_usage(index=True, deep=True))
    print(f"Memória total (bytes): {dados.memory_usage(index=True, deep=True).sum()}")


if __name__ == "__main__":
    main()
