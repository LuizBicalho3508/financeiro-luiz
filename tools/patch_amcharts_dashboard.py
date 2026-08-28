from pathlib import Path

app_path = Path("app.py")
text = app_path.read_text(encoding="utf-8")

import_anchor = "from pymongo.errors import DuplicateKeyError\n"
import_line = "from charts import render_balance_chart, render_expense_donut, render_flow_chart\n"
if import_line not in text:
    if import_anchor not in text:
        raise SystemExit("Ancora de imports nao encontrada")
    text = text.replace(import_anchor, import_anchor + import_line, 1)

flow_old = '''        fig = go.Figure()
        fig.add_bar(x=monthly["period"], y=monthly["income"], name="Receitas", marker_color="#22c55e")
        fig.add_bar(x=monthly["period"], y=monthly["expense"], name="Despesas", marker_color="#ef4444")
        fig.add_scatter(
            x=monthly["period"],
            y=monthly["balance"],
            name="Saldo",
            mode="lines+markers",
            line=dict(color="#38bdf8", width=3),
            marker=dict(size=7),
        )
        fig.update_layout(
            barmode="group",
            height=380,
            margin=dict(l=10, r=10, t=20, b=10),
            legend_orientation="h",
            legend_y=1.1,
            yaxis_title="R$",
            xaxis_title="",
        )
        st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})
'''
flow_new = '''        render_flow_chart(monthly, height=390)
'''
if flow_old in text:
    text = text.replace(flow_old, flow_new, 1)
elif flow_new.strip() not in text:
    raise SystemExit("Bloco do fluxo mensal nao encontrado")

pie_old = '''            fig = px.pie(
                cat,
                names="category",
                values="amount",
                hole=0.58,
                color_discrete_sequence=px.colors.sequential.Reds_r,
            )
            fig.update_traces(textposition="inside", textinfo="percent", marker=dict(line=dict(color="rgba(15,23,42,.35)", width=1)))
            fig.update_layout(height=380, margin=dict(l=10, r=10, t=20, b=10), legend_orientation="h")
            st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})
'''
pie_new = '''            render_expense_donut(cat, total=float(cat["amount"].sum()), height=390)
'''
if pie_old in text:
    text = text.replace(pie_old, pie_new, 1)
elif pie_new.strip() not in text:
    raise SystemExit("Bloco do donut nao encontrado")

area_old = '''            final_balance = float(daily["acumulado"].iloc[-1])
            balance_color = "#22c55e" if final_balance >= 0 else "#ef4444"
            fill_color = "rgba(34,197,94,.16)" if final_balance >= 0 else "rgba(239,68,68,.16)"
            fig = go.Figure(
                go.Scatter(
                    x=daily["date"],
                    y=daily["acumulado"],
                    mode="lines+markers",
                    line=dict(color=balance_color, width=3),
                    marker=dict(size=7, color=balance_color),
                    fill="tozeroy",
                    fillcolor=fill_color,
                    hovertemplate="%{x|%d/%m/%Y}<br>Saldo: R$ %{y:,.2f}<extra></extra>",
                )
            )
            fig.add_hline(y=0, line_width=1, line_dash="dot", line_color="rgba(148,163,184,.55)")
            fig.update_layout(height=330, margin=dict(l=10, r=10, t=20, b=10), xaxis_title="", yaxis_title="R$", showlegend=False)
            st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})
'''
area_new = '''            render_balance_chart(daily, height=340)
'''
if area_old in text:
    text = text.replace(area_old, area_new, 1)
elif area_new.strip() not in text:
    raise SystemExit("Bloco do saldo acumulado nao encontrado")

app_path.write_text(text, encoding="utf-8")

charts_path = Path("charts/amcharts.py")
charts = charts_path.read_text(encoding="utf-8")
old_colors = '''root.set("colors", am5.ColorSet.new(root, {{
  colors: [am5.color(0xEF4444), am5.color(0xF97316), am5.color(0xF59E0B), am5.color(0xE11D48), am5.color(0xFB7185), am5.color(0x38BDF8), am5.color(0x8B5CF6)]
}}));

var chart = root.container.children.push(am5percent.PieChart.new(root, {{
'''
new_colors = '''var chart = root.container.children.push(am5percent.PieChart.new(root, {{
'''
if old_colors in charts:
    charts = charts.replace(old_colors, new_colors, 1)

series_anchor = '''series.labels.template.set("forceHidden", true);
'''
series_colors = '''series.get("colors").set("colors", [
  am5.color(0xEF4444), am5.color(0xF97316), am5.color(0xF59E0B),
  am5.color(0xE11D48), am5.color(0xFB7185), am5.color(0x38BDF8), am5.color(0x8B5CF6)
]);
series.labels.template.set("forceHidden", true);
'''
if 'series.get("colors").set("colors"' not in charts:
    if series_anchor not in charts:
        raise SystemExit("Ancora das cores do donut nao encontrada")
    charts = charts.replace(series_anchor, series_colors, 1)
charts_path.write_text(charts, encoding="utf-8")

print("Integracao amCharts aplicada ao dashboard.")
