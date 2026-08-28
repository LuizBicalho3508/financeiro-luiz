from pathlib import Path

path = Path("app.py")
text = path.read_text(encoding="utf-8")

css_anchor = '''        .brand-subtitle { opacity: .72; margin-bottom: 1.4rem; }
'''
css_new = '''        .brand-subtitle { opacity: .72; margin-bottom: 1.4rem; }

        /* Dashboard / KPIs */
        .dashboard-context {
            display: flex;
            align-items: center;
            gap: .55rem;
            margin: -.3rem 0 1rem 0;
            color: rgba(148, 163, 184, .95);
            font-size: .95rem;
            font-weight: 600;
        }
        .dashboard-context::before {
            content: "";
            width: 7px;
            height: 7px;
            border-radius: 50%;
            background: #38bdf8;
            box-shadow: 0 0 16px rgba(56, 189, 248, .65);
        }
        .kpi-card {
            position: relative;
            overflow: hidden;
            min-height: 142px;
            padding: 17px 17px 15px 17px;
            border-radius: 19px;
            border: 1px solid rgba(148, 163, 184, .16);
            background: linear-gradient(145deg, rgba(15, 23, 42, .76), rgba(30, 41, 59, .48));
            box-shadow: 0 10px 30px rgba(2, 6, 23, .16);
            transition: transform .16s ease, border-color .16s ease, box-shadow .16s ease;
        }
        .kpi-card:hover {
            transform: translateY(-2px);
            border-color: rgba(148, 163, 184, .30);
            box-shadow: 0 14px 34px rgba(2, 6, 23, .22);
        }
        .kpi-card::after {
            content: "";
            position: absolute;
            width: 110px;
            height: 110px;
            right: -48px;
            top: -52px;
            border-radius: 999px;
            opacity: .16;
            filter: blur(3px);
            background: var(--kpi-color, #38bdf8);
        }
        .kpi-top {
            display: flex;
            justify-content: space-between;
            align-items: center;
            gap: 8px;
            margin-bottom: 13px;
        }
        .kpi-label {
            color: rgba(203, 213, 225, .86);
            font-size: .78rem;
            font-weight: 750;
            letter-spacing: .045em;
            text-transform: uppercase;
        }
        .kpi-icon {
            display: inline-flex;
            align-items: center;
            justify-content: center;
            width: 31px;
            height: 31px;
            border-radius: 10px;
            color: var(--kpi-color, #38bdf8);
            background: color-mix(in srgb, var(--kpi-color, #38bdf8) 14%, transparent);
            font-size: 1rem;
            font-weight: 800;
        }
        .kpi-value {
            color: var(--kpi-color, #e2e8f0);
            font-size: clamp(1.32rem, 1.65vw, 1.78rem);
            line-height: 1.12;
            font-weight: 850;
            letter-spacing: -.035em;
            margin-bottom: 7px;
            white-space: nowrap;
        }
        .kpi-caption {
            color: rgba(148, 163, 184, .88);
            font-size: .77rem;
            line-height: 1.25;
        }
        .kpi-green { --kpi-color: #22c55e; }
        .kpi-red { --kpi-color: #ef4444; }
        .kpi-blue { --kpi-color: #38bdf8; }
        .kpi-amber { --kpi-color: #f59e0b; }
        .kpi-neutral { --kpi-color: #cbd5e1; }

        div[data-testid="stPlotlyChart"] {
            border: 1px solid rgba(148, 163, 184, .10);
            border-radius: 17px;
            overflow: hidden;
            background: rgba(15, 23, 42, .18);
        }
        div[data-testid="stDataFrame"] {
            border-radius: 14px;
            overflow: hidden;
        }
        @media (max-width: 900px) {
            .kpi-card { min-height: 128px; }
            .kpi-value { white-space: normal; }
        }
'''
if css_anchor not in text:
    raise SystemExit("Âncora CSS não encontrada")
text = text.replace(css_anchor, css_new, 1)

inject_anchor = '''inject_css()\n\n\n# -----------------------------------------------------------------------------\n# Utilidades\n'''
inject_new = '''inject_css()\n\n\ndef render_kpi_card(container, title, value, tone="blue", icon="•", caption=""):\n    allowed = {"green", "red", "blue", "amber", "neutral"}\n    tone = tone if tone in allowed else "blue"\n    container.markdown(\n        f"""\n        <div class="kpi-card kpi-{tone}">\n            <div class="kpi-top">\n                <div class="kpi-label">{title}</div>\n                <div class="kpi-icon">{icon}</div>\n            </div>\n            <div class="kpi-value">{value}</div>\n            <div class="kpi-caption">{caption}</div>\n        </div>\n        """,\n        unsafe_allow_html=True,\n    )\n\n\n# -----------------------------------------------------------------------------\n# Utilidades\n'''
if inject_anchor not in text:
    raise SystemExit("Âncora de helper não encontrada")
text = text.replace(inject_anchor, inject_new, 1)

metric_old = '''    k1, k2, k3, k4, k5 = st.columns(5)\n    k1.metric("Receitas", brl_from_cents(income))\n    k2.metric("Despesas", brl_from_cents(expense))\n    k3.metric("Resultado previsto", brl_from_cents(result))\n    k4.metric("A pagar", brl_from_cents(pending_expense))\n    k5.metric("A receber", brl_from_cents(pending_income))\n'''
metric_new = '''    st.markdown(\n        f'<div class="dashboard-context">Resumo de {month_names[selected_month - 1]} de {selected_year}</div>',\n        unsafe_allow_html=True,\n    )\n\n    result_tone = "green" if result > 0 else "red" if result < 0 else "neutral"\n    result_caption = "superávit previsto" if result > 0 else "déficit previsto" if result < 0 else "receitas e despesas equilibradas"\n\n    k1, k2, k3, k4, k5 = st.columns(5, gap="small")\n    render_kpi_card(k1, "Receitas", brl_from_cents(income), "green", "↑", "total previsto para o mês")\n    render_kpi_card(k2, "Despesas", brl_from_cents(expense), "red", "↓", "compromissos do mês")\n    render_kpi_card(k3, "Resultado", brl_from_cents(result), result_tone, "=", result_caption)\n    render_kpi_card(k4, "A pagar", brl_from_cents(pending_expense), "red", "!", "pendente de pagamento")\n    render_kpi_card(k5, "A receber", brl_from_cents(pending_income), "green", "+", "pendente de recebimento")\n'''
if metric_old not in text:
    raise SystemExit("Bloco antigo de métricas não encontrado")
text = text.replace(metric_old, metric_new, 1)

chart_old = '''        fig = go.Figure()\n        fig.add_bar(x=monthly["period"], y=monthly["income"], name="Receitas")\n        fig.add_bar(x=monthly["period"], y=monthly["expense"], name="Despesas")\n        fig.add_scatter(x=monthly["period"], y=monthly["balance"], name="Saldo", mode="lines+markers")\n'''
chart_new = '''        fig = go.Figure()\n        fig.add_bar(x=monthly["period"], y=monthly["income"], name="Receitas", marker_color="#22c55e")\n        fig.add_bar(x=monthly["period"], y=monthly["expense"], name="Despesas", marker_color="#ef4444")\n        fig.add_scatter(\n            x=monthly["period"],\n            y=monthly["balance"],\n            name="Saldo",\n            mode="lines+markers",\n            line=dict(color="#38bdf8", width=3),\n            marker=dict(size=7),\n        )\n'''
if chart_old not in text:
    raise SystemExit("Bloco do gráfico mensal não encontrado")
text = text.replace(chart_old, chart_new, 1)

pie_old = '''            fig = px.pie(cat, names="category", values="amount", hole=0.55)\n            fig.update_layout(height=380, margin=dict(l=10, r=10, t=20, b=10), legend_orientation="h")\n'''
pie_new = '''            fig = px.pie(\n                cat,\n                names="category",\n                values="amount",\n                hole=0.58,\n                color_discrete_sequence=px.colors.sequential.Reds_r,\n            )\n            fig.update_traces(textposition="inside", textinfo="percent", marker=dict(line=dict(color="rgba(15,23,42,.35)", width=1)))\n            fig.update_layout(height=380, margin=dict(l=10, r=10, t=20, b=10), legend_orientation="h")\n'''
if pie_old not in text:
    raise SystemExit("Bloco do gráfico por categoria não encontrado")
text = text.replace(pie_old, pie_new, 1)

area_old = '''            daily["acumulado"] = daily["signed"].cumsum()\n            fig = px.area(daily, x="date", y="acumulado", markers=True)\n            fig.update_layout(height=330, margin=dict(l=10, r=10, t=20, b=10), xaxis_title="", yaxis_title="R$")\n'''
area_new = '''            daily["acumulado"] = daily["signed"].cumsum()\n            final_balance = float(daily["acumulado"].iloc[-1])\n            balance_color = "#22c55e" if final_balance >= 0 else "#ef4444"\n            fill_color = "rgba(34,197,94,.16)" if final_balance >= 0 else "rgba(239,68,68,.16)"\n            fig = go.Figure(\n                go.Scatter(\n                    x=daily["date"],\n                    y=daily["acumulado"],\n                    mode="lines+markers",\n                    line=dict(color=balance_color, width=3),\n                    marker=dict(size=7, color=balance_color),\n                    fill="tozeroy",\n                    fillcolor=fill_color,\n                    hovertemplate="%{x|%d/%m/%Y}<br>Saldo: R$ %{y:,.2f}<extra></extra>",\n                )\n            )\n            fig.add_hline(y=0, line_width=1, line_dash="dot", line_color="rgba(148,163,184,.55)")\n            fig.update_layout(height=330, margin=dict(l=10, r=10, t=20, b=10), xaxis_title="", yaxis_title="R$", showlegend=False)\n'''
if area_old not in text:
    raise SystemExit("Bloco do saldo acumulado não encontrado")
text = text.replace(area_old, area_new, 1)

# Deixa os gráficos mais limpos sem barra de ferramentas, sem alterar os dados.
text = text.replace(
    'st.plotly_chart(fig, use_container_width=True)',
    'st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})',
)

path.write_text(text, encoding="utf-8")
print("Patch visual do dashboard aplicado com sucesso.")
