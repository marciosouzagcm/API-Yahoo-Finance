import yfinance as yf
import streamlit as st  # type: ignore
import matplotlib.pyplot as plt
from mplfinance.original_flavor import candlestick_ohlc # type: ignore
import pandas as pd
import matplotlib.dates as mdates

# Interface gráfica
st.title("Dados Históricos de Ações")

# Inputs para o usuário
ticker = st.text_input("Digite o ticker da ação (ex: BOVA11.SA):")
start = st.date_input("Data de início:", key="start_date", help="Escolha a data de início.")
end = st.date_input("Data de fim:", key="end_date", help="Escolha a data de término.")

if st.button("Buscar"):
    try:
        # Obtendo dados históricos
        dados = yf.download(ticker, start=start, end=end)

        # Exibindo dados históricos (sem a coluna de dias da semana)
        st.write("Dados históricos de", ticker)
        st.write(dados[['Open', 'High', 'Low', 'Close', 'Volume']])

        # Dados fundamentalistas
        info = yf.Ticker(ticker).info
        st.write("Dados Fundamentalistas:")
        st.write("Setor:", info.get('sector', 'N/A'))
        st.write("Indústria:", info.get('industry', 'N/A'))

        # Capitalização de mercado formatada
        market_cap = info.get('marketCap', None)
        if market_cap:
            market_cap_formatado = f"{market_cap:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
            st.write("Capitalização de Mercado:", market_cap_formatado)
        else:
            st.write("Capitalização de Mercado: N/A")

        # Informações sobre Dividend Yield
        dividend_yield = info.get('dividendYield', None)
        if dividend_yield:
            dividend_yield_formatado = f"{dividend_yield * 100:.2f}%"
            st.write("Dividend Yield:", dividend_yield_formatado)
        else:
            st.write("Dividend Yield: N/A")

        # Pagamentos de dividendos no período
        st.write("**Pagamentos de Dividendos no Período:**")
        dividends = yf.Ticker(ticker).dividends
        if not dividends.empty:
            # Garantir que as datas dos dividendos estejam sem fuso horário
            dividends.index = dividends.index.tz_localize(None)

            # Filtrar dividendos no período selecionado
            dividends_periodo = dividends[(dividends.index >= pd.to_datetime(start)) & (dividends.index <= pd.to_datetime(end))]
            
            if not dividends_periodo.empty:
                # Exibir dividendos pagos no período
                st.write("Tabela de Dividendos Pagos:")
                st.dataframe(dividends_periodo)

                # Soma total de dividendos pagos no período
                soma_dividendos = dividends_periodo.sum()
                st.write(f"**Soma total de dividendos pagos no período:** {soma_dividendos:.2f}")
            else:
                st.write("Nenhum dividendo foi pago no período selecionado.")
        else:
            st.write("Nenhum dividendo disponível para este ativo.")

        # Gráficos candlestick
        def gerar_grafico(periodo, titulo):
            dados_periodo = dados.resample(periodo).agg({
                'Open': 'first',
                'High': 'max',
                'Low': 'min',
                'Close': 'last',
                'Volume': 'sum'
            }).dropna()

            fig, ax = plt.subplots(figsize=(12, 6))
            dados_periodo['DataNum'] = mdates.date2num(dados_periodo.index)
            ohlc = dados_periodo[['DataNum', 'Open', 'High', 'Low', 'Close']].values
            candlestick_ohlc(ax, ohlc, colorup='green', colordown='red', width=0.6)

            ax.xaxis.set_major_locator(mdates.MonthLocator())
            ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m'))
            ax.xaxis.set_tick_params(labelsize=10)

            plt.title(f'Gráfico Candlestick {titulo}')
            plt.xlabel('Data')
            plt.ylabel('Preço')
            plt.grid(alpha=0.3)
            st.pyplot(fig)

        # Gerar gráficos para diferentes períodos
        gerar_grafico('D', 'Diário')
        gerar_grafico('W', 'Semanal')
        gerar_grafico('M', 'Mensal')

    except Exception as e:
        st.write("Erro:", str(e))
