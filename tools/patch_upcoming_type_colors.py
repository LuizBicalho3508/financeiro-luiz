from pathlib import Path

path = Path("app.py")
text = path.read_text(encoding="utf-8")

old = '''            view["Valor"] = view["amount"].map(brl)\n            st.dataframe(view[["Data", "Tipo", "description", "Valor"]], hide_index=True, width="stretch")\n'''

new = '''            view["Valor"] = view["amount"].map(brl)\n            upcoming_view = view[["Data", "Tipo", "description", "Valor"]].rename(\n                columns={"description": "Descrição"}\n            )\n\n            def style_upcoming_type(value):\n                if value == "Despesa":\n                    return (\n                        "background-color: #35141d; "\n                        "color: #ff7083; "\n                        "font-weight: 800; "\n                        "border-left: 3px solid #ff4d67;"\n                    )\n                if value == "Receita":\n                    return (\n                        "background-color: #0d3021; "\n                        "color: #52f59c; "\n                        "font-weight: 800; "\n                        "border-left: 3px solid #16e07a;"\n                    )\n                return ""\n\n            styled_upcoming = upcoming_view.style.map(style_upcoming_type, subset=["Tipo"])\n            st.dataframe(\n                styled_upcoming,\n                hide_index=True,\n                width="stretch",\n                column_config={\n                    "Data": st.column_config.TextColumn("Data", width="small"),\n                    "Tipo": st.column_config.TextColumn("Tipo", width="small"),\n                    "Descrição": st.column_config.TextColumn("Descrição", width="large"),\n                    "Valor": st.column_config.TextColumn("Valor", width="medium"),\n                },\n            )\n'''

if old not in text:
    if 'styled_upcoming = upcoming_view.style.map(style_upcoming_type' in text:
        print("Patch já aplicado.")
        raise SystemExit(0)
    raise SystemExit("Bloco de próximos vencimentos não encontrado.")

text = text.replace(old, new, 1)
path.write_text(text, encoding="utf-8")
print("Cores da coluna Tipo aplicadas aos próximos vencimentos.")
