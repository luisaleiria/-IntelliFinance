import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(
    page_title="IntelliFinance",
    page_icon="💜",
    layout="wide"
)

def real(v):
    return f"R$ {v:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

def percentual(v):
    return f"{v * 100:.1f}%"

def normalizar_despesas(despesas_dict):
    return {str(cat): float(valor) for cat, valor in despesas_dict.items()}

def normalizar_metas(metas_dict):
    metas_limpas = {}
    for nome, valor in metas_dict.items():
        nome_limpo = str(nome).strip()
        if not nome_limpo:
            continue
        metas_limpas[nome_limpo] = max(float(valor), 0.0)
    return metas_limpas

def simular_patrimonio(renda, despesas, patrimonio, rentabilidade, meses, crescimento_renda, inflacao_despesas):
    dados = []

    for mes in range(1, meses + 1):
        renda_mes = renda * ((1 + crescimento_renda) ** (mes / 12))
        despesas_mes = despesas * ((1 + inflacao_despesas) ** (mes / 12))
        saldo = renda_mes - despesas_mes
        aporte = max(0, saldo)
        patrimonio = patrimonio * (1 + rentabilidade) + aporte

        dados.append({
            "Mês": mes,
            "Renda prevista": renda_mes,
            "Despesas previstas": despesas_mes,
            "Saldo previsto": saldo,
            "Aporte previsto": aporte,
            "Patrimônio previsto": patrimonio
        })

    return pd.DataFrame(dados)

def prazo_meta(df, meta):
    atingiu = df[df["Patrimônio previsto"] >= meta]
    if atingiu.empty:
        return None
    return int(atingiu.iloc[0]["Mês"])

def score_financeiro(taxa_poupanca, reserva_meses, endividamento, variaveis_renda):
    score = 0
    score += min(max(taxa_poupanca, 0) / 0.35, 1) * 35
    score += min(reserva_meses / 6, 1) * 30
    score += max(0, 1 - endividamento) * 20
    score += max(0, 1 - variaveis_renda / 0.35) * 15
    return round(score, 1)

def categorizar_descricao(desc):
    desc = str(desc).lower()

    if any(p in desc for p in ["ifood", "restaurante", "mercado", "padaria", "delivery"]):
        return "Alimentação"
    if any(p in desc for p in ["uber", "99", "gasolina", "posto"]):
        return "Transporte"
    if any(p in desc for p in ["netflix", "spotify", "prime", "assinatura", "vpn"]):
        return "Assinaturas"
    if any(p in desc for p in ["amazon", "shein", "shopping", "loja", "mercado livre"]):
        return "Compras online"
    if any(p in desc for p in ["cinema", "bar", "show", "evento"]):
        return "Lazer"
    if any(p in desc for p in ["academia", "yoga", "pilates"]):
        return "Academia/Yoga"

    return "Outros"

def processar_csv(uploaded_file):
    df = pd.read_csv(uploaded_file)
    df.columns = [c.lower() for c in df.columns]

    desc_col = None
    valor_col = None

    for c in ["descricao", "descrição", "historico", "histórico", "description", "nome"]:
        if c in df.columns:
            desc_col = c

    for c in ["valor", "amount", "preco", "preço"]:
        if c in df.columns:
            valor_col = c

    if desc_col is None or valor_col is None:
        return None, "O CSV precisa ter uma coluna de descrição e uma coluna de valor."

    df["Categoria"] = df[desc_col].apply(categorizar_descricao)
    df["Valor"] = pd.to_numeric(df[valor_col], errors="coerce").abs()
    df = df.dropna(subset=["Valor"])

    resumo = df.groupby("Categoria", as_index=False)["Valor"].sum()
    return resumo, None

st.title("💰 IntelliFinance")
st.caption("Sistema inteligente para diagnóstico financeiro, projeção de fluxo de caixa e acompanhamento de metas")

st.sidebar.title("Configurações")

usar_ana = st.sidebar.toggle("Usar dados-base da Ana Costa", value=True)

if usar_ana:
    renda_default = 6200.0
    patrimonio_default = 4500.0
    dividas_default = 0.0

    despesas_default = {
        "Ajuda aos pais": 800.0,
        "Transporte": 300.0,
        "Alimentação": 600.0,
        "Lazer": 600.0,
        "Compras online": 800.0,
        "Assinaturas": 150.0,
        "Academia/Yoga": 120.0
    }

    metas_default = {
        "Reserva de emergência": 25000.0,
        "Viagem ao Japão": 35000.0,
        "Entrada do apartamento": 100000.0
    }

else:
    renda_default = 5000.0
    patrimonio_default = 0.0
    dividas_default = 0.0

    despesas_default = {
        "Moradia": 1200.0,
        "Transporte": 300.0,
        "Alimentação": 800.0,
        "Lazer": 400.0,
        "Compras online": 500.0,
        "Assinaturas": 100.0,
        "Saúde/Educação": 300.0
    }

    metas_default = {
        "Reserva de emergência": 20000.0,
        "Viagem/Projeto pessoal": 30000.0,
        "Entrada de imóvel": 100000.0
    }

if st.session_state.get("perfil_base_ana") != usar_ana:
    st.session_state["perfil_base_ana"] = usar_ana
    st.session_state.pop("despesas_override", None)
    st.session_state.pop("metas_override", None)

if "despesas_override" in st.session_state:
    categorias_override = set(st.session_state["despesas_override"].keys())
    categorias_default = set(despesas_default.keys())
    if categorias_override != categorias_default:
        st.session_state.pop("despesas_override")

renda = st.sidebar.number_input("Renda mensal líquida", min_value=0.0, value=renda_default, step=100.0)
patrimonio = st.sidebar.number_input("Patrimônio inicial", min_value=0.0, value=patrimonio_default, step=500.0)
dividas = st.sidebar.number_input("Dívidas atuais", min_value=0.0, value=dividas_default, step=100.0)

st.sidebar.subheader("Projeção")
meses = st.sidebar.slider("Horizonte de previsão", 12, 120, 60, 12)
rentabilidade = st.sidebar.slider("Rentabilidade mensal estimada (%)", 0.0, 2.0, 0.8, 0.1) / 100
crescimento_renda = st.sidebar.slider("Crescimento anual da renda (%)", 0.0, 20.0, 5.0, 0.5) / 100
inflacao_despesas = st.sidebar.slider("Crescimento anual das despesas (%)", 0.0, 15.0, 3.0, 0.5) / 100

aba1, aba2, aba3, aba4, aba5 = st.tabs([
    "Visão Geral",
    "Entrada de Dados",
    "Análise de Gastos",
    "Projeções",
    "Metas e Relatório"
])

with aba2:
    st.subheader("Entrada manual de despesas")

    despesas = {}
    despesas_override = st.session_state.get("despesas_override")
    col1, col2 = st.columns(2)

    for i, (categoria, valor) in enumerate(despesas_default.items()):
        widget_key = f"despesa_{categoria}"
        if despesas_override and categoria in despesas_override:
            st.session_state[widget_key] = float(despesas_override[categoria])

        with col1 if i % 2 == 0 else col2:
            despesas[categoria] = st.number_input(
                categoria,
                min_value=0.0,
                value=float(valor),
                step=50.0,
                key=widget_key
            )

    despesas = normalizar_despesas(despesas)

    st.subheader("Metas financeiras")

    metas_referencia = normalizar_metas(st.session_state.get("metas_override", metas_default))
    df_metas_base = pd.DataFrame({
        "Meta": list(metas_referencia.keys()),
        "Valor alvo": list(metas_referencia.values())
    })

    df_metas_editado = st.data_editor(
        df_metas_base,
        use_container_width=True,
        hide_index=True,
        key="tabela_metas",
        num_rows="dynamic",
        column_config={
            "Meta": st.column_config.TextColumn("Meta"),
            "Valor alvo": st.column_config.NumberColumn(
                "Valor alvo",
                min_value=0.0,
                step=1000.0,
                format="R$ %.2f"
            )
        }
    )

    df_metas_editado["Meta"] = df_metas_editado["Meta"].astype(str).str.strip()
    df_metas_editado["Valor alvo"] = pd.to_numeric(df_metas_editado["Valor alvo"], errors="coerce").fillna(0.0).clip(lower=0.0)
    df_metas_editado = df_metas_editado[df_metas_editado["Meta"] != ""]
    df_metas_editado = df_metas_editado.drop_duplicates(subset=["Meta"], keep="last")

    metas = normalizar_metas(dict(zip(df_metas_editado["Meta"], df_metas_editado["Valor alvo"])))

    if metas != metas_referencia:
        st.session_state["metas_override"] = metas
        st.rerun()

    st.subheader("Upload opcional de CSV")

    uploaded = st.file_uploader("Enviar CSV de transações", type=["csv"])

    if uploaded is not None:
        resumo_csv, erro = processar_csv(uploaded)

        if erro:
            st.error(erro)
        else:
            st.success("CSV processado com sucesso.")
            st.dataframe(resumo_csv, use_container_width=True)

total_despesas = sum(despesas.values())
saldo = renda - total_despesas
taxa_poupanca = saldo / renda if renda > 0 else 0
reserva_meses = patrimonio / total_despesas if total_despesas > 0 else 0
endividamento = dividas / renda if renda > 0 else 0

variaveis = ["Alimentação", "Lazer", "Compras online"]
gastos_variaveis = sum(valor for cat, valor in despesas.items() if cat in variaveis)
variaveis_renda = gastos_variaveis / renda if renda > 0 else 0

score = score_financeiro(taxa_poupanca, reserva_meses, endividamento, variaveis_renda)

df_despesas = pd.DataFrame({
    "Categoria": list(despesas.keys()),
    "Valor": list(despesas.values())
})

df_proj = simular_patrimonio(
    renda,
    total_despesas,
    patrimonio,
    rentabilidade,
    meses,
    crescimento_renda,
    inflacao_despesas
)

with aba1:
    st.subheader("Visão geral")

    c1, c2, c3, c4 = st.columns(4)

    c1.metric("Saldo mensal", real(saldo))
    c2.metric("Taxa de poupança", percentual(taxa_poupanca))
    c3.metric("Reserva em meses", f"{reserva_meses:.1f}")
    c4.metric("Score financeiro", f"{score}/100")

    st.subheader("Progresso das metas")

    if metas:
        for nome, meta in metas.items():
            if meta > 0 and patrimonio >= meta:
                progresso = 1.0
            elif meta > 0:
                progresso = max(patrimonio / meta, 0)
            else:
                progresso = 0
            st.write(f"**{nome}** — {real(patrimonio)} de {real(meta)}")
            st.progress(progresso)
    else:
        st.info("Cadastre ao menos uma meta na aba Entrada de Dados.")

    colg1, colg2 = st.columns(2)

    with colg1:
        fig = px.pie(
            df_despesas,
            names="Categoria",
            values="Valor",
            title="Distribuição das despesas"
        )
        st.plotly_chart(fig, use_container_width=True)

    with colg2:
        fig2 = px.line(
            df_proj,
            x="Mês",
            y="Patrimônio previsto",
            title="Evolução patrimonial prevista"
        )

        for nome, meta in metas.items():
            fig2.add_hline(y=meta, line_dash="dash", annotation_text=nome)

        st.plotly_chart(fig2, use_container_width=True)

with aba3:
    st.subheader("Análise detalhada de gastos")

    st.caption("Edite os valores na tabela. Ao mudar qualquer gasto, todo o sistema é atualizado automaticamente.")

    df_editavel = df_despesas[["Categoria", "Valor"]].copy()
    df_editado = st.data_editor(
        df_editavel,
        use_container_width=True,
        hide_index=True,
        key="tabela_analise_gastos",
        disabled=["Categoria"],
        column_config={
            "Categoria": st.column_config.TextColumn("Categoria"),
            "Valor": st.column_config.NumberColumn(
                "Valor",
                min_value=0.0,
                step=10.0,
                format="R$ %.2f"
            )
        }
    )

    df_editado["Valor"] = pd.to_numeric(df_editado["Valor"], errors="coerce").fillna(0.0).clip(lower=0.0)

    despesas_editadas = normalizar_despesas(dict(zip(df_editado["Categoria"], df_editado["Valor"])))

    if despesas_editadas != despesas:
        st.session_state["despesas_override"] = despesas_editadas
        st.rerun()

    c1, c2, c3 = st.columns(3)

    c1.metric("Despesas totais", real(total_despesas))
    c2.metric("Gastos variáveis", real(gastos_variaveis))
    c3.metric("Variáveis/renda", percentual(variaveis_renda))

    fig_bar = px.bar(
        df_despesas.sort_values("Valor", ascending=False),
        x="Categoria",
        y="Valor",
        title="Gastos por categoria"
    )

    st.plotly_chart(fig_bar, use_container_width=True)

    df_visao = df_despesas.copy()
    df_visao["% da renda"] = df_visao["Valor"] / renda if renda > 0 else 0
    st.dataframe(df_visao, use_container_width=True)

with aba4:
    st.subheader("Projeção de fluxo de caixa")

    st.dataframe(df_proj, use_container_width=True)

    fig_fluxo = px.line(
        df_proj,
        x="Mês",
        y=[
            "Renda prevista",
            "Despesas previstas",
            "Saldo previsto",
            "Aporte previsto"
        ],
        title="Renda, despesas, saldo e aportes projetados"
    )

    st.plotly_chart(fig_fluxo, use_container_width=True)

    fig_pat = px.line(
        df_proj,
        x="Mês",
        y="Patrimônio previsto",
        title="Evolução patrimonial"
    )

    for nome, meta in metas.items():
        fig_pat.add_hline(y=meta, line_dash="dash", annotation_text=nome)

    st.plotly_chart(fig_pat, use_container_width=True)

    st.download_button(
        "Baixar projeção em CSV",
        data=df_proj.to_csv(index=False).encode("utf-8"),
        file_name="projecao_fluxo_caixa.csv",
        mime="text/csv"
    )

with aba5:
    st.subheader("Metas financeiras")

    resultados = []
    if metas:
        cols = st.columns(len(metas))

        for i, (nome, meta) in enumerate(metas.items()):
            prazo = prazo_meta(df_proj, meta)
            prazo_texto = "Não atingida" if prazo is None else f"{prazo} meses"

            cols[i].metric(nome, prazo_texto)

            resultados.append({
                "Meta": nome,
                "Valor alvo": meta,
                "Prazo estimado": prazo_texto
            })

        st.dataframe(pd.DataFrame(resultados), use_container_width=True)
    else:
        st.info("Nenhuma meta cadastrada.")

    fig_gauge = go.Figure(go.Indicator(
        mode="gauge+number",
        value=score,
        title={"text": "Score financeiro"},
        gauge={"axis": {"range": [0, 100]}}
    ))

    st.plotly_chart(fig_gauge, use_container_width=True)

    st.subheader("Recomendações automáticas")

    if saldo < 0:
        st.write("• O orçamento está deficitário. A prioridade deve ser reduzir despesas.")
    elif taxa_poupanca < 0.15:
        st.write("• A taxa de poupança está baixa. Automatize aportes e reduza gastos variáveis.")
    else:
        st.write("• A taxa de poupança está saudável e favorece o avanço nas metas.")

    if reserva_meses < 3:
        st.write("• Priorize a construção da reserva de emergência.")
    elif reserva_meses < 6:
        st.write("• Continue fortalecendo a reserva até atingir 6 meses de despesas.")
    else:
        st.write("• A reserva está adequada. É possível diversificar investimentos.")

    if variaveis_renda > 0.35:
        st.write("• Os gastos variáveis estão elevados. Defina tetos mensais para lazer, compras e alimentação.")
    else:
        st.write("• Os gastos variáveis estão em nível controlado.")

    resumo = f"""
Foi desenvolvido um sistema interativo de inteligência financeira utilizando Python, Streamlit e Plotly.

A aplicação permite que o usuário insira renda mensal, patrimônio inicial, dívidas, categorias de despesas,
rentabilidade esperada, crescimento de renda, crescimento das despesas e metas financeiras.

O sistema calcula saldo mensal, taxa de poupança, reserva em meses, endividamento relativo à renda,
participação de gastos variáveis e score financeiro. Além disso, gera projeções de fluxo de caixa e evolução
patrimonial, estimando o prazo necessário para atingir metas como reserva de emergência, viagem internacional
e entrada de imóvel.

Resumo do cenário analisado:
- Renda mensal: {real(renda)}
- Despesas mensais: {real(total_despesas)}
- Saldo mensal: {real(saldo)}
- Taxa de poupança: {percentual(taxa_poupanca)}
- Reserva em meses: {reserva_meses:.1f}
- Endividamento/renda: {percentual(endividamento)}
- Gastos variáveis/renda: {percentual(variaveis_renda)}
- Score financeiro: {score}/100
"""

    st.text_area("Texto para inserir no relatório", resumo, height=300)

    st.download_button(
        "Baixar resumo em TXT",
        data=resumo.encode("utf-8"),
        file_name="resumo_sistema_financeiro.txt",
        mime="text/plain"
    )