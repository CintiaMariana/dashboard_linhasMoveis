import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px

st.set_page_config(
    page_title="Dashboard Linhas Móveis",
    page_icon="📱",
    layout="wide"
)

# --- Carregar dados ---
df = pd.read_excel("TELEFONIA_MOVEL.xlsx")
df_rodovia = pd.read_excel("UNIDADES_RODOVIA_SEM_USO.xlsx")

# --- Sidebar: Filtros ---
st.sidebar.header("🔍 Filtros")

operadoras_disponiveis = sorted(df['OPERADORA'].dropna().astype(str).unique())
operadoras_selecionadas = st.sidebar.multiselect("Operadora", operadoras_disponiveis, default=operadoras_disponiveis)

funcao_disponiveis = sorted(df['FUNCAO'].dropna().astype(str).unique())
funcao_selecionadas = st.sidebar.multiselect("Função", funcao_disponiveis, default=funcao_disponiveis)

grupos_disponiveis = sorted(df['GRUPO'].dropna().astype(str).unique())
grupos_selecionadas = st.sidebar.multiselect("Grupo", grupos_disponiveis, default=grupos_disponiveis)

dadosMoveis_disponiveis = sorted(df['DADOS'].dropna().astype(str).unique())
dadosMoveis_selecionadas = st.sidebar.multiselect("Dados Móveis", dadosMoveis_disponiveis, default=dadosMoveis_disponiveis)

semUso_disponiveis = sorted(df['AGOSTO'].dropna().astype(str).unique())
semUso_selecionadas = st.sidebar.multiselect("Linhas sem uso no mês de Agosto", semUso_disponiveis, default=semUso_disponiveis)

# --- Filtrar DataFrame ---
df_filtrado = df[
    (df['OPERADORA'].astype(str).isin(operadoras_selecionadas)) &
    (df['FUNCAO'].astype(str).isin(funcao_selecionadas)) &
    (df['GRUPO'].astype(str).isin(grupos_selecionadas)) &
    (df['DADOS'].astype(str).isin(dadosMoveis_selecionadas)) &
    (df['AGOSTO'].astype(str).isin(semUso_selecionadas))
]

# --- Título ---
st.title("Dashboard de Análise das Linhas Móveis")
st.markdown("Explore os dados das linhas móveis. Utilize os filtros à esquerda para refinar sua análise.")

# --- Resumo ---
resumo = df.groupby("OPERADORA")['OPERADORA'].count()
st.write("Quantidade de linhas por operadoras:")
st.write(resumo)

# --- Tabela Unidades Rodovia ---
st.subheader("Unidades Rodovia com vendas em até 700.000L em Agosto/2025")
st.dataframe(df_rodovia)

# --- Gráfico de pizza por STATUS abaixo da tabela ---
if 'STATUS' in df_rodovia.columns:
    resumo_status = df_rodovia['STATUS'].value_counts().reset_index()
    resumo_status.columns = ['Status', 'Quantidade']

    grafico_status = px.pie(
        resumo_status,
        names='Status',
        values='Quantidade',
        title='Postos Rodovia com vendas acima de 700.000L',
        hole=0.4
    )
    grafico_status.update_traces(textinfo='percent+label')
    grafico_status.update_layout(title_x=0.5)
    st.plotly_chart(grafico_status, use_container_width=True)
else:
    st.warning("A coluna 'STATUS' não foi encontrada em df_rodovia.")

st.markdown("Sugestão: Remanejar números de unidades urbanas que estão sem uso para as unidades com grandes vendas e estão sem número")

st.markdown("---")
st.subheader("Gráficos")

# --- Primeira linha de gráficos: Operadora e Dados Móveis ---
col_graf1, col_graf2 = st.columns(2)

with col_graf1:
    if not df_filtrado.empty:
        resumo_operadora = df_filtrado['OPERADORA'].value_counts().reset_index()
        resumo_operadora.columns = ['Operadora', 'Quantidade']
        grafico_operadora = px.pie(
            resumo_operadora,
            names='Operadora',
            values='Quantidade',
            title='Linhas por Operadora',
            hole=0.4
        )
        grafico_operadora.update_traces(textinfo='percent+label')
        grafico_operadora.update_layout(title_x=0.5)
        st.plotly_chart(grafico_operadora, use_container_width=True)
    else:
        st.warning("Nenhum dado para exibir o gráfico de operadoras.")

with col_graf2:
    if not df_filtrado.empty:
        resumo_dados = df_filtrado['DADOS'].value_counts().reset_index()
        resumo_dados.columns = ['Dados Móveis', 'Quantidade']
        grafico_dados = px.pie(
            resumo_dados,
            names='Dados Móveis',
            values='Quantidade',
            title='Linhas por Tipo de Dados',
            hole=0.4
        )
        grafico_dados.update_traces(textinfo='percent+label')
        grafico_dados.update_layout(title_x=0.5)
        st.plotly_chart(grafico_dados, use_container_width=True)
    else:
        st.warning("Nenhum dado para exibir o gráfico de dados móveis.")

# --- Segunda linha de gráficos: Funções e Grupos ---
col_graf3, col_graf4 = st.columns(2)

with col_graf3:
    if not df_filtrado.empty:
        resumo_funcao = df_filtrado['FUNCAO'].value_counts().nlargest(20).sort_values(ascending=True).reset_index()
        resumo_funcao.columns = ['Função', 'Quantidade']
        grafico_funcao = px.bar(
            resumo_funcao,
            x='Quantidade',
            y='Função',
            orientation='h',
            title='Qtd de Linhas por Função',
            labels={'Quantidade': 'Quantidade de Linhas', 'Função': ''}
        )
        grafico_funcao.update_layout(title_x=0.5)
        st.plotly_chart(grafico_funcao, use_container_width=True)
    else:
        st.warning("Nenhum dado para exibir o gráfico de funções.")

with col_graf4:
    if not df_filtrado.empty:
        resumo_grupo = df_filtrado['GRUPO'].value_counts().nlargest(20).sort_values(ascending=True).reset_index()
        resumo_grupo.columns = ['Grupo', 'Quantidade']
        grafico_grupo = px.bar(
            resumo_grupo,
            x='Quantidade',
            y='Grupo',
            orientation='h',
            title='Qtd de Linhas por Grupo',
            labels={'Quantidade': 'Quantidade de Linhas', 'Grupo': ''}
        )
        grafico_grupo.update_layout(title_x=0.5)
        st.plotly_chart(grafico_grupo, use_container_width=True)
    else:
        st.warning("Nenhum dado para exibir o gráfico de grupos.")

# --- Terceira linha de gráfico: Linhas sem uso ---
col_graf5, col_graf6 = st.columns(2)

with col_graf5:
    if not df_filtrado.empty:
        resumo_sem_uso = df_filtrado['AGOSTO'].value_counts().reset_index()
        resumo_sem_uso.columns = ['Status', 'Quantidade']
        grafico_sem_uso = px.pie(
            resumo_sem_uso,
            names='Status',
            values='Quantidade',
            title='Linhas sem uso no mês de Agosto',
            hole=0.4
        )
        grafico_sem_uso.update_traces(textinfo='percent+label')
        grafico_sem_uso.update_layout(title_x=0.5)
        st.plotly_chart(grafico_sem_uso, use_container_width=True)
    else:
        st.warning("Nenhum dado para exibir o gráfico de Linhas sem uso.")

with col_graf6:
    if not df_filtrado.empty:
        # Filtrar apenas linhas com status "Sem uso"
        df_sem_uso = df_filtrado[df_filtrado['AGOSTO'].astype(str).str.lower() == "sem uso"]

        if not df_sem_uso.empty:
            st.subheader("Linhas com status 'Sem uso'")
            st.dataframe(df_sem_uso[['OPERADORA', 'FUNCAO', 'GRUPO', 'DADOS', 'AGOSTO']])
        else:
            st.info("Nenhuma linha com status 'Sem uso' encontrada.")

st.markdown("---")

# --- Tabela completa ---
st.subheader("Todos os dados")
st.dataframe(df)
