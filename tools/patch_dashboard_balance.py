from pathlib import Path

path = Path("app.py")
text = path.read_text(encoding="utf-8")

old_group = '            daily = daily.groupby(daily["due_date"].dt.date, as_index=False)["signed"].sum()'
new_group = '            daily["date"] = daily["due_date"].dt.normalize()\n            daily = daily.groupby("date", as_index=False, sort=True)["signed"].sum()'
old_chart = '            fig = px.area(daily, x="due_date", y="acumulado", markers=True)'
new_chart = '            fig = px.area(daily, x="date", y="acumulado", markers=True)'

if old_group in text:
    text = text.replace(old_group, new_group, 1)
elif 'daily = daily.groupby("date", as_index=False, sort=True)["signed"].sum()' not in text:
    raise SystemExit("Trecho de agrupamento esperado não encontrado.")

if old_chart in text:
    text = text.replace(old_chart, new_chart, 1)
elif new_chart.strip() not in text:
    raise SystemExit("Trecho do gráfico esperado não encontrado.")

path.write_text(text, encoding="utf-8")
print("Patch do saldo acumulado aplicado/verificado.")
