import streamlit as st
import sqlite3
from streamlit_extras.metric_cards import style_metric_cards
from streamlit_extras.altex import line_chart, get_stocks_data

st.title('Geral')

st.divider()

col1, col2, col3 = st.columns(3)
col1.metric(label="Total gasto esse mês", value=5000, delta=1000)
col2.metric(label="Total ração esse mês", value=5000, delta=-1000)
col3.metric(label="Total animais esse mês", value=5000, delta=0)
style_metric_cards(background_color="#0E1117", border_color="#0E1117", border_left_color="#0E1117", border_radius_px=0, box_shadow=False)

st.divider()

stocks = get_stocks_data()
line_chart(
    data=stocks.query("symbol == 'GOOG'"),
    x="date",
    y="price",
    title="Animais 2023",
)

stocks = get_stocks_data()
line_chart(
    data=stocks.query("symbol == 'AAPL'"),
    x="date",
    y="price",
    title="Ração 2023",
)