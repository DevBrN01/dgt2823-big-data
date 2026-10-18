# DGT2823 — Tecnologias para desenvolvimento de soluções de big data

Trabalho prático de leitura e limpeza de dados com Python e Pandas. O projeto utiliza o conjunto obrigatório de atividades físicas fornecido no enunciado, com 32 registros e as colunas `ID`, `Duration`, `Date`, `Pulse`, `Maxpulse` e `Calories`.

## Execução

Requisitos: Python 3.11 ou superior. Versões utilizadas na validação: Python 3.12.14 e Pandas 3.0.1.

Abra o terminal na pasta do projeto e execute:

```bash
python -m pip install -r requirements.txt
python microatividades.py
python trabalho_pratico.py
```

No Windows, se o comando instalado for `py`, substitua `python` por `py`. Os caminhos dos CSVs são calculados a partir da localização dos scripts, permitindo executá-los também a partir de outra pasta.

`trabalho_pratico.py` mostra cada etapa no terminal e grava `resultados/atividades_tratadas.csv`. Os arquivos `resultados/execucao_microatividades.txt` e `resultados/execucao_trabalho_pratico.txt` contêm saídas reais da execução de referência. Para gerar novas evidências em um terminal UTF-8:

```bash
python microatividades.py > resultados/execucao_microatividades.txt
python trabalho_pratico.py > resultados/execucao_trabalho_pratico.txt
```

## Arquivos

| Arquivo | Conteúdo |
| --- | --- |
| `dados/atividades.csv` | Dados de entrada, separados por ponto e vírgula |
| `microatividades.py` | As cinco atividades de apoio, identificadas e comentadas |
| `trabalho_pratico.py` | Os 13 passos do trabalho, incluindo as tentativas de conversão |
| `requirements.txt` | Versão do Pandas utilizada |
| `resultados/atividades_tratadas.csv` | Dados após o tratamento |
| `resultados/execucao_microatividades.txt` | Evidências das microatividades |
| `resultados/execucao_trabalho_pratico.txt` | Evidências da limpeza |
| `resultados/verificacao.txt` | Resumo das conferências do resultado |

## Origem e ajuste de transcrição

A fonte dos dados é o material da disciplina DGT2823 recebido com a atividade. O conjunto Online Retail citado no material é apenas uma sugestão para as microatividades. Este projeto usa o conjunto obrigatório de atividades físicas em todas as etapas.

No texto recebido, os registros de IDs 20 e 21 aparecem quebrados assim:

```text
20;45;'2020/12/20';97;125;2430 2
1;60;'2020/12/21';108;131;3642
```

Foi corrigida apenas essa quebra de transcrição: o valor de Calories do ID 20 é `2430` e o registro seguinte tem ID `21`. A correção se apoia na sequência de IDs de 0 a 31. Os valores ausentes e a data `20201226` foram mantidos no arquivo de entrada para tratamento no código. Os valores de Calories foram preservados na escala fornecida.

## Microatividades

1. **Ler o CSV:** `pd.read_csv(arquivo, sep=";", engine="python", encoding="utf-8")` importa o arquivo. O separador corresponde ao fornecido no material.
2. **Criar um subconjunto:** `dados[["Duration", "Pulse", "Calories"]].copy()` seleciona três colunas e cria uma cópia independente.
3. **Configurar a exibição:** `pd.set_option("display.max_rows", 9999)` altera o limite da representação habitual. `dados.to_string()` exibe todas as linhas por padrão, independentemente desse limite.
4. **Mostrar início e fim:** `dados.head(10)` retorna as primeiras dez linhas e `dados.tail(10)` as últimas dez.
5. **Inspecionar os dados:** `dados.info(memory_usage="deep")` informa colunas, contagens não nulas, tipos e memória. `shape` mostra dimensões; `isna().sum()` conta nulos; `dtypes` mostra os tipos; `memory_usage(index=True, deep=True).sum()` calcula o uso estimado de memória em bytes, incluindo o índice e os valores de texto.

O conjunto inicial contém **32 linhas, 6 colunas e 3 células nulas**: Calories nos IDs 18 e 28 e Date no ID 22. `ID`, `Duration`, `Pulse` e `Maxpulse` são inteiros; `Calories` é ponto flutuante devido aos nulos; `Date` é textual antes da conversão. O nome do tipo textual e a memória estimada podem variar conforme a versão e o ambiente. Consulte a saída real em `resultados/execucao_microatividades.txt`.

Na execução de referência, as quatro colunas inteiras tiveram tipo `int64`, Calories teve tipo `float64` e Date teve tipo `str`. A memória inicial estimada foi de **3.331 bytes**, incluindo o índice. Após a conversão, Date teve tipo `datetime64[us]`.

## Tratamento realizado

| Passos do roteiro | Operação |
| --- | --- |
| 1 a 4 | Leitura do CSV obrigatório com `read_csv` |
| 5 | Inspeção com `info`, `head(10)`, `tail(10)` e contagem de nulos |
| 6 | Cópia do dataframe por `copy(deep=True)` |
| 7 | Preenchimento dos dois nulos de Calories com `fillna(0)` |
| 8 | Preenchimento da data ausente com `1900/01/01` e primeira tentativa de conversão |
| 9 | Substituição do marcador por um nulo real e nova tentativa de conversão |
| 10 | Correção específica de `20201226`, combinando `replace` e `to_datetime` |
| 11 | Conversão completa de Date para datetime e exibição do dataframe |
| 12 | Remoção do registro sem data com `dropna(subset=["Date"])` |
| 13 | Exibição e inspeção do resultado final |

### Datas e erros didáticos

As aspas simples das datas, como em `'2020/12/01'`, fazem parte dos valores lidos: o delimitador de campos padrão do leitor CSV é a aspa dupla. Por isso, o código explicita o formato `"'%Y/%m/%d'"`, que inclui as aspas simples.

Com esse formato, o marcador `1900/01/01`, que não tem aspas, causa o primeiro `ValueError`. O erro é capturado e exibido, permitindo continuar a prática. Após substituí-lo por um nulo real com `float("nan")`, a segunda tentativa identifica o valor compacto `20201226`.

Há uma imprecisão no enunciado: `1900/01/01` é uma data válida para o formato `%Y/%m/%d`. Neste CSV, a incompatibilidade ocorre pela diferença nas aspas. A inferência automática e a redação dos erros também podem variar entre versões. O formato explícito torna o comportamento da demonstração verificável.

Para corrigir apenas a data compacta, `pd.to_datetime("20201226", format="%Y%m%d")` cria a data correspondente. `strftime` padroniza temporariamente sua escrita para o formato dos demais registros, e `replace` aplica a substituição. A chamada seguinte de `to_datetime` converte toda a coluna de uma vez, evitando misturar objetos datetime e textos antes dessa conversão.

O nulo da coluna Date passa a ser `NaT`, que representa uma data ausente no Pandas. `dropna(subset=["Date"])` remove esse registro. As outras datas são interpretadas com `errors="raise"`, de modo que uma falha adicional não seja descartada silenciosamente.

### Resultado

| Verificação | Resultado |
| --- | --- |
| Registros iniciais | 32 |
| Registros finais | 31 |
| Colunas finais | 6 |
| Calories do ID 18 | 0 |
| Calories do ID 28 | 0 |
| Date do ID 26 | 2020-12-26 |
| Registro removido | ID 22, por ausência de Date |
| Células nulas no resultado | 0 |
| Tipo de Date em memória | datetime64 |
| Dados originais | Preservados |

O índice interno não é renumerado após a remoção. A coluna ID preserva os identificadores originais. O CSV final é exportado sem o índice adicional e com datas no formato `AAAA-MM-DD`. CSV não armazena tipos de dados. Para recuperar Date como datetime ao reabrir o resultado:

```python
import pandas as pd

resultado = pd.read_csv(
    "resultados/atividades_tratadas.csv",
    sep=";",
    encoding="utf-8",
    parse_dates=["Date"],
)
```

O tratamento segue o escopo do roteiro. O valor `Duration = 450` do ID 7, os registros com medidas repetidas nos IDs 11 e 12 e `Maxpulse < Pulse` no ID 23 são mantidos, pois a atividade não define regras para alterá-los. Esses casos exigiriam avaliação adicional antes de uma análise real. O preenchimento de Calories com zero é uma exigência didática e não comprova ausência de gasto calórico.

## Entrega em repositório público

1. Crie um repositório no GitHub chamado, por exemplo, `dgt2823-big-data`, com visibilidade **Public**.
2. Envie o conteúdo desta pasta, incluindo os scripts, o CSV original, os resultados, este README e o arquivo de dependências. Pelo site, use **Add file → Upload files**. O ZIP deve ser extraído antes do envio para que o tutor possa navegar pelos arquivos.
3. Confira o acesso ao repositório em uma janela sem login.
4. Copie o endereço do repositório e envie-o na aba **Trabalhos** da Sala de Aula Virtual, dentro do prazo informado pela instituição.

O projeto local e os resultados não substituem a publicação nem o envio do link na plataforma da disciplina.

Se usar Git no terminal, depois de criar um repositório público vazio no GitHub, substitua `SEU_USUARIO` pelo seu usuário nos comandos abaixo. Execute-os na pasta deste projeto:

```bash
git remote add origin https://github.com/SEU_USUARIO/dgt2823-big-data.git
git push -u origin main
```

O projeto local já possui um commit inicial na branch `main`. A autenticação no GitHub será solicitada pelo seu ambiente Git quando necessário. Se usar os arquivos extraídos do ZIP em vez da pasta com o histórico Git, inicialize primeiro o repositório:

```bash
git init -b main
git add .
git commit -m "Implementa trabalho pratico DGT2823 com Pandas"
```

## Referências de apoio

- Material do trabalho prático da disciplina DGT2823: roteiro e conjunto de dados fornecidos na atividade.
- [Pandas: read_csv](https://pandas.pydata.org/docs/reference/api/pandas.read_csv.html).
- [Pandas: DataFrame.info](https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.info.html).
- [Pandas: to_datetime](https://pandas.pydata.org/docs/reference/api/pandas.to_datetime.html).
- [Pandas: DataFrame.dropna](https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.dropna.html).
