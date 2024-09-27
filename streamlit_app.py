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

# Convertendo a coluna de data para o tipo datetime, especificando que o dia vem primeiro
df['data_coluna'] = pd.to_datetime(df['Data'], dayfirst=True)
# Criando uma nova coluna "mes_ano" com o nome do mês e o ano
df['mes_ano'] = df['data_coluna'].dt.strftime('%B/%Y')

maior_do_mes = df['Glicemia'].max()
menor_do_mes = df['Glicemia'].loc[df['Glicemia'] > 0].min()

st.header("👨🏾‍🦳 Levy Batista - Índice glicêmico", divider="rainbow")

# Obtendo os valores únicos da coluna "mes_ano"
meses_unicos = df['mes_ano'].unique()

filcol1, filcol2, filcol3, filcol4 = st.columns([0.7,0.7,0.7,4])
# Criando um selectbox com os valores únicos de "mes_ano"
with filcol1:
    option = st.selectbox(
        "Selecione o mês e ano:",
        meses_unicos)

col1, col2, col3, col4 = st.columns([0.7,0.7,0.7,4])
with col1:
    with st.container( border=True):
        st.metric(label="⚠️ Maior do mês", value=maior_do_mes, delta="100", delta_color="inverse") 
with col2:
    with st.container( border=True):
        st.metric(label="⚠️ Menor do mês", value=menor_do_mes, delta="100", delta_color="inverse") 
with col3:
    with st.container( border=True):
        df_2 = pd.DataFrame(df)
        # Convertendo a coluna de data para o tipo datetime, especificando que o dia vem primeiro
        df_2['Data'] = pd.to_datetime(df_2['Data'], dayfirst=True)
        # Filtrando para pegar as linhas onde glicemia não é nulo
        df_glicemia_preenchido = df_2.dropna(subset=['Glicemia'])

        # Pegando a última linha com glicemia preenchida
        ultima_linha_glicemia = df_glicemia_preenchido.iloc[-1]

        # Extraindo o valor de glicemia
        valor_glicemia = ultima_linha_glicemia['Glicemia']
        data_glicemia = ultima_linha_glicemia['Data'].strftime('%d/%m/%Y')  # Formata a data como dd/mm/yyyy

        # Exibindo o valor da glicemia e a data no st.metric
        st.metric(label=f"💉 Glicemia em {data_glicemia}", value=valor_glicemia, delta="100", delta_color="inverse")



st.subheader("🔬 Glicemia de {}".format(option), divider="rainbow")
# Criar o gráfico usando Altair
chart = alt.Chart(df).mark_area().encode(
    x=alt.X('Data:O', title='Data'),  # 'O' para ordinal (string)
    y=alt.Y('Glicemia:Q', title='Glicemia'),
    tooltip=['Data:O', 'Glicemia:Q']
).properties(width=600, height=400).interactive() #, title='Glicemia').interactive()

# Adiciona rótulos aos pontos no gráfico
text = chart.mark_text(align='center', baseline='middle', dy=-5,
                       color='black', size=15
                      ).encode(text='Glicemia:Q', x='Data:O', y='Glicemia:Q')

# Exibe o gráfico no Streamlit
st.altair_chart(chart + text, use_container_width=True)


# Exibir o DataFrame no Streamlit
#st.dataframe(df)

