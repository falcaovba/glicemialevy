import streamlit as st
import pandas as pd
import altair as alt

st.set_page_config(page_title='Acompanhamento de Glicemia - Levy Batista', page_icon='🔬',layout="wide",initial_sidebar_state="collapsed")


# URL do Google Sheets (substitua pelo link da sua planilha)
csv_url = 'https://docs.google.com/spreadsheets/d/1KXgtfKXd1EPWWPSsua-4qS9pUOoflczrnIrmCU4dwTo/pub?output=csv'
# Ler os dados diretamente do Google Sheets
df = pd.read_csv(csv_url)
df['Data'] = pd.to_datetime(df['Data'], dayfirst=True)
df = df.sort_values(by='Data')
# Formata a coluna 'Data' de volta para string no formato desejado (por exemplo, 'dd/mm/yyyy')
df['Data'] = df['Data'].dt.strftime('%d/%m/%Y')


st.header("👨🏾‍🦳 Levy Batista - Índice glicêmico", divider="rainbow")


# Criar o gráfico usando Altair
chart = alt.Chart(df).mark_area().encode(
    x=alt.X('Data:O', title='Data'),  # 'O' para ordinal (string)
    y=alt.Y('Glicemia:Q', title='Glicemia'),
    tooltip=['Data:O', 'Glicemia:Q']
).properties(width=600, height=400, title='Glicemia').interactive()

# Adiciona rótulos aos pontos no gráfico
text = chart.mark_text(align='center', baseline='middle', dy=-5,
                       color='black', size=15
                      ).encode(text='Glicemia:Q', x='Data:O', y='Glicemia:Q')

# Exibe o gráfico no Streamlit
st.altair_chart(chart + text, use_container_width=True)


# Exibir o DataFrame no Streamlit
#st.dataframe(df)