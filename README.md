API-Yahoo-Finance


1. Importação das Bibliotecas


import yfinance as yf
import streamlit as st
import matplotlib.pyplot as plt
from mplfinance.original_flavor import candlestick_ohlc
import pandas as pd
import matplotlib.dates as mdates


Descrição das Bibliotecas

- yfinance: Obtém dados financeiros de ações (preços históricos, informações fundamentalistas, dividendos, etc.)
- streamlit: Framework para construir aplicações web interativas
- matplotlib.pyplot: Cria gráficos em Python
- mplfinance.original_flavor.candlestick_ohlc: Cria gráficos de velas (candlestick)
- pandas: Manipulação de dados em tabelas e séries temporais
- matplotlib.dates: Trabalha com datas em gráficos

2. Interface Gráfica e Inputs


st.title("Dados Históricos de Ações")
ticker = st.text_input("Digite o ticker da ação (ex: BOVA11.SA):")
start = st.date_input("Data de início:", key="start_date", help="Escolha a data de início.")
end = st.date_input("Data de fim:", key="end_date", help="Escolha a data de término.")


Inputs do Usuário

- ticker: Código da ação (ex: BOVA11.SA)
- start e end: Datas de início e fim para coleta de dados históricos

3. Lógica Principal

3.1. Obtenção de Dados Históricos


dados = yf.download(ticker, start=start, end=end)


3.2. Exibição de Dados Fundamentalistas


info = yf.Ticker(ticker).info
st.write("Dados Fundamentalistas:")
st.write("Setor:", info.get('sector', 'N/A'))
st.write("Indústria:", info.get('industry', 'N/A'))


3.3. Pagamentos de Dividendos


dividends = yf.Ticker(ticker).dividends
if not dividends.empty:
    st.write("Tabela de Dividendos Pagos:")
    st.dataframe(dividends_periodo)


3.4. Gráficos Candlestick


def gerar_grafico(periodo, titulo):
    # ...
    st.pyplot(fig)


Passos para Execução

1. Preparação do Ambiente
- Instale o Python (versão 3.8 ou superior)
- Instale dependências: pip install yfinance streamlit matplotlib mplfinance pandas
2. Baixar o Código
- Acesse o GitHub e baixe o repositório (clonando ou baixando como .zip)
- git clone https://github.com/marciosouzagcm/API-Yahoo-Finance.git
3. Executar o Código
- Inicie o Streamlit: streamlit run yahoo_financial.py
