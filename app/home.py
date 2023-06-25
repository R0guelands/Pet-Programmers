import streamlit as st
import sqlite3
from PIL import Image
from streamlit_extras.metric_cards import style_metric_cards
from streamlit_extras.altex import line_chart, get_stocks_data
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