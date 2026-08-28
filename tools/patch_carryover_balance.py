from pathlib import Path

path = Path("app.py")
text = path.read_text(encoding="utf-8")

anchor = '''    pending_income = current.loc[
        (current["kind"] == "income") & (current["status"] == "pending"), "amount_cents"
    ].sum()

    st.markdown(
'''
insert = '''    pending_income = current.loc[
        (current["kind"] == "income") & (current["status"] == "pending"), "amount_cents"
    ].sum()

    # Saldo transportado: soma todo o histórico anterior ao mês selecionado.
    # Mantemos "resultado do mês" separado para não confundir desempenho mensal
    # com o saldo acumulado disponível/projetado.
    period_start = pd.Timestamp(date(selected_year, selected_month, 1))
    previous = active_df[active_df["due_date"] < period_start]
    previous_income = int(previous.loc[previous["kind"] == "income", "amount_cents"].sum())
    previous_expense = int(previous.loc[previous["kind"] == "expense", "amount_cents"].sum())
    previous_balance = previous_income - previous_expense
    accumulated_balance = previous_balance + result

    st.markdown(
'''
if anchor not in text:
    if "accumulated_balance = previous_balance + result" not in text:
        raise SystemExit("Âncora do cálculo mensal não encontrada.")
else:
    text = text.replace(anchor, insert, 1)

old_result = '''    result_tone = "green" if result > 0 else "red" if result < 0 else "neutral"
    result_caption = "superávit previsto" if result > 0 else "déficit previsto" if result < 0 else "receitas e despesas equilibradas"

    k1, k2, k3, k4, k5 = st.columns([1.28, 1, 1, 1, 1], gap="small")
    render_kpi_card(k1, "Resultado previsto", brl_from_cents(result), result_tone, "◎", result_caption)
    render_kpi_card(k2, "Receitas", brl_from_cents(income), "green", "↑", "total previsto no mês")
    render_kpi_card(k3, "Despesas", brl_from_cents(expense), "red", "↓", "total comprometido")
    render_kpi_card(k4, "A pagar", brl_from_cents(pending_expense), "red", "!", "pendências de saída")
    render_kpi_card(k5, "A receber", brl_from_cents(pending_income), "green", "+", "pendências de entrada")
'''
new_result = '''    result_tone = "green" if result > 0 else "red" if result < 0 else "neutral"
    result_caption = "superávit previsto" if result > 0 else "déficit previsto" if result < 0 else "receitas e despesas equilibradas"
    balance_tone = "green" if accumulated_balance > 0 else "red" if accumulated_balance < 0 else "neutral"
    balance_title = "Saldo atual" if selected_year == today.year and selected_month == today.month else "Saldo acumulado"
    balance_caption = f"inclui {brl_from_cents(previous_balance)} trazidos de meses anteriores"

    k1, k2, k3, k4, k5, k6 = st.columns([1.45, 1.18, 1, 1, 1, 1], gap="small")
    render_kpi_card(k1, balance_title, brl_from_cents(accumulated_balance), balance_tone, "◉", balance_caption)
    render_kpi_card(k2, "Resultado do mês", brl_from_cents(result), result_tone, "◎", result_caption)
    render_kpi_card(k3, "Receitas", brl_from_cents(income), "green", "↑", "total previsto no mês")
    render_kpi_card(k4, "Despesas", brl_from_cents(expense), "red", "↓", "total comprometido")
    render_kpi_card(k5, "A pagar", brl_from_cents(pending_expense), "red", "!", "pendências de saída")
    render_kpi_card(k6, "A receber", brl_from_cents(pending_income), "green", "+", "pendências de entrada")
'''
if old_result in text:
    text = text.replace(old_result, new_result, 1)
elif 'render_kpi_card(k1, balance_title' not in text:
    raise SystemExit("Bloco de KPIs não encontrado.")

old_section = '        section_title("Saldo acumulado", "EVOLUÇÃO DIÁRIA")'
new_section = '        section_title("Saldo acumulado", "EVOLUÇÃO DIÁRIA · INCLUI SALDO ANTERIOR")'
if old_section in text:
    text = text.replace(old_section, new_section, 1)

old_daily = '            daily["acumulado"] = daily["signed"].cumsum()\n'
new_daily = '            daily["acumulado"] = cents_to_money(previous_balance) + daily["signed"].cumsum()\n'
if old_daily in text:
    text = text.replace(old_daily, new_daily, 1)
elif 'cents_to_money(previous_balance) + daily["signed"].cumsum()' not in text:
    raise SystemExit("Cálculo do saldo diário não encontrado.")

path.write_text(text, encoding="utf-8")
print("Saldo acumulado com transporte mensal aplicado.")
