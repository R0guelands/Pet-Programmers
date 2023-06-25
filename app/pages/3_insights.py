import sqlite3
import streamlit as st
import base64
def sidebar_bg(side_bg):

   side_bg_ext = 'png'

   st.markdown(
      f"""
      <style>
      [data-testid="stSidebar"] > div:first-child {{
        background: url(data:image/{side_bg_ext};base64,{base64.b64encode(open(side_bg, "rb").read()).decode()});
        background-repeat: no-repeat;
        background-repeat: no-repeat;
        background-size: 131px;
        background-position: 50% 0%;
        padding-top: 0px;
      }}
      [data-testid="stSidebarNav"]::before {{
                content: "";
                margin-left: 20px;
                margin-top: 20px;
                font-size: 30px;
                position: relative;
                top: 100px;
            }}
      </style>
      """,
      unsafe_allow_html=True,
      )
   
side_bg = 'app/img/logo.png'
sidebar_bg(side_bg)

from streamlit_extras.altex import line_chart, get_stocks_data
import streamlit as st

st.title('Previsões futuras')

stocks = get_stocks_data()
line_chart(
    data=stocks.query("symbol == 'GOOG'"),
    x="date",
    y="price",
    title="Animais 2023",
)
line_chart(
    data=stocks.query("symbol == 'AAPL'"),
    x="date",
    y="price",
    title="Ração 2023",
)
line_chart(
    data=stocks.query("symbol == 'AAPL'"),
    x="date",
    y="price",
    title="Gastos gerais 2023",
)
line_chart(
    data=stocks.query("symbol == 'AAPL'"),
    x="date",
    y="price",
    title="Lucro esparado 2023",
)
