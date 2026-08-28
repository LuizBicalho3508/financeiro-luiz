from pathlib import Path

path = Path("app.py")
text = path.read_text(encoding="utf-8")

import_anchor = "from charts import render_balance_chart, render_expense_donut, render_flow_chart\n"
ui_import = "from dashboard_ui import inject_dashboard_theme, render_dashboard_hero, section_title\n"
if ui_import not in text:
    if import_anchor not in text:
        raise SystemExit("Âncora de import não encontrada.")
    text = text.replace(import_anchor, import_anchor + ui_import, 1)

old_start = '''def page_dashboard(db, user):
    st.title("Dashboard")
    rows = transaction_rows(db, user)
    df = to_dataframe(rows)

    today = date.today()
'''
new_start = '''def page_dashboard(db, user):
    inject_dashboard_theme()
    rows = transaction_rows(db, user)
    df = to_dataframe(rows)

    today = date.today()
    render_dashboard_hero(today)
'''
if old_start in text:
    text = text.replace(old_start, new_start, 1)
elif "render_dashboard_hero(today)" not in text:
    raise SystemExit("Início do dashboard não encontrado.")

old_kpis = '''    k1, k2, k3, k4, k5 = st.columns(5, gap="small")
    render_kpi_card(k1, "Receitas", brl_from_cents(income), "green", "↑", "total previsto para o mês")
    render_kpi_card(k2, "Despesas", brl_from_cents(expense), "red", "↓", "compromissos do mês")
    render_kpi_card(k3, "Resultado", brl_from_cents(result), result_tone, "=", result_caption)
    render_kpi_card(k4, "A pagar", brl_from_cents(pending_expense), "red", "!", "pendente de pagamento")
    render_kpi_card(k5, "A receber", brl_from_cents(pending_income), "green", "+", "pendente de recebimento")
'''
new_kpis = '''    k1, k2, k3, k4, k5 = st.columns([1.28, 1, 1, 1, 1], gap="small")
    render_kpi_card(k1, "Resultado previsto", brl_from_cents(result), result_tone, "◎", result_caption)
    render_kpi_card(k2, "Receitas", brl_from_cents(income), "green", "↑", "total previsto no mês")
    render_kpi_card(k3, "Despesas", brl_from_cents(expense), "red", "↓", "total comprometido")
    render_kpi_card(k4, "A pagar", brl_from_cents(pending_expense), "red", "!", "pendências de saída")
    render_kpi_card(k5, "A receber", brl_from_cents(pending_income), "green", "+", "pendências de entrada")
'''
if old_kpis in text:
    text = text.replace(old_kpis, new_kpis, 1)
elif 'render_kpi_card(k1, "Resultado previsto"' not in text:
    raise SystemExit("Bloco de KPIs não encontrado.")

replacements = {
    '        st.subheader("Fluxo mensal")': '        section_title("Fluxo financeiro — 12 meses", "RECEITAS · DESPESAS · SALDO")',
    '        st.subheader("Despesas por categoria")': '        section_title("Despesas por categoria", "COMPOSIÇÃO DO MÊS")',
    '        st.subheader("Saldo acumulado do mês")': '        section_title("Saldo acumulado", "EVOLUÇÃO DIÁRIA")',
    '        st.subheader("Próximos vencimentos")': '        section_title("Próximos vencimentos", "JANELA DE 30 DIAS")',
    '        st.subheader("Orçamento do mês")': '        section_title("Orçamento do mês", "LIMITE POR CATEGORIA")',
    '    chart_left, chart_right = st.columns([1.55, 1])': '    chart_left, chart_right = st.columns([1.65, 1], gap="medium")',
    '    bottom_left, bottom_right = st.columns([1.2, 1])': '    bottom_left, bottom_right = st.columns([1.35, 1], gap="medium")',
}
for old, new in replacements.items():
    if old in text:
        text = text.replace(old, new, 1)

# Streamlit 1.62 remove use_container_width; width é a API atual.
text = text.replace("use_container_width=True", 'width="stretch"')
text = text.replace("use_container_width=False", 'width="content"')

path.write_text(text, encoding="utf-8")
print("Dashboard v2 aplicado com sucesso.")
