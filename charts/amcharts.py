import json
from datetime import date, datetime

import pandas as pd
import streamlit as st


CDN_CORE = "https://cdn.amcharts.com/lib/5/index.js"
CDN_XY = "https://cdn.amcharts.com/lib/5/xy.js"
CDN_PERCENT = "https://cdn.amcharts.com/lib/5/percent.js"
CDN_ANIMATED = "https://cdn.amcharts.com/lib/5/themes/Animated.js"

GREEN = "#16E07A"
RED = "#FF4D67"
CYAN = "#00E7FF"
BLUE = "#4D7CFE"
TEXT = "#F8FAFC"
MUTED = "#8EA3BA"

MONTHS_PT = {
    1: "Jan", 2: "Fev", 3: "Mar", 4: "Abr", 5: "Mai", 6: "Jun",
    7: "Jul", 8: "Ago", 9: "Set", 10: "Out", 11: "Nov", 12: "Dez",
}


def _safe_json(value):
    return json.dumps(value, ensure_ascii=False, separators=(",", ":")).replace("</", "<\\/")


def _to_float(value):
    try:
        if pd.isna(value):
            return 0.0
    except Exception:
        pass
    try:
        return float(value)
    except Exception:
        return 0.0


def _month_label(value):
    text = str(value)
    try:
        year, month = text.split("-")[:2]
        return f"{MONTHS_PT[int(month)]}/{year[-2:]}"
    except Exception:
        return text


def _date_ms(value):
    if isinstance(value, pd.Timestamp):
        value = value.to_pydatetime()
    if isinstance(value, date) and not isinstance(value, datetime):
        value = datetime.combine(value, datetime.min.time())
    if not isinstance(value, datetime):
        value = pd.to_datetime(value).to_pydatetime()
    return int(value.timestamp() * 1000)


def _iframe_document(chart_js, *, height=390, modules=("xy",)):
    scripts = [f'<script src="{CDN_CORE}"></script>']
    if "xy" in modules:
        scripts.append(f'<script src="{CDN_XY}"></script>')
    if "percent" in modules:
        scripts.append(f'<script src="{CDN_PERCENT}"></script>')
    scripts.append(f'<script src="{CDN_ANIMATED}"></script>')
    scripts_html = "\n".join(scripts)

    return f"""
<!doctype html>
<html lang="pt-BR">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<style>
:root {{ color-scheme: dark; --text:{TEXT}; --muted:{MUTED}; --cyan:{CYAN}; }}
html,body {{ margin:0; padding:0; background:transparent; overflow:hidden; font-family:Inter,ui-sans-serif,system-ui,-apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif; }}
* {{ box-sizing:border-box; }}
.shell {{
  position:relative; width:100%; height:{height}px; overflow:hidden; border-radius:20px;
  border:1px solid rgba(0,231,255,.16);
  background:
    radial-gradient(900px 300px at 20% -10%, rgba(0,231,255,.10), transparent 50%),
    radial-gradient(700px 300px at 100% 0%, rgba(77,124,254,.10), transparent 50%),
    linear-gradient(145deg, rgba(14,27,46,.985), rgba(7,16,29,.985));
  box-shadow:inset 0 1px 0 rgba(255,255,255,.035), 0 14px 42px rgba(1,7,18,.24);
}}
.shell::before {{
  content:""; position:absolute; inset:0; pointer-events:none; z-index:0;
  background-image:
    linear-gradient(rgba(96,165,250,.035) 1px, transparent 1px),
    linear-gradient(90deg, rgba(96,165,250,.035) 1px, transparent 1px);
  background-size:28px 28px;
  mask-image:linear-gradient(to bottom, rgba(0,0,0,.72), transparent 92%);
}}
.shell::after {{
  content:""; position:absolute; left:0; right:0; top:0; height:2px; z-index:4;
  background:linear-gradient(90deg, transparent, {CYAN}, {BLUE}, transparent);
  opacity:.72; filter:drop-shadow(0 0 6px {CYAN});
}}
#chartdiv {{ position:absolute; inset:0; z-index:2; }}
.state {{
  position:absolute; inset:0; z-index:5; display:grid; place-items:center; pointer-events:none;
  color:var(--muted); font-size:12px; letter-spacing:.04em;
}}
.state-card {{
  padding:10px 14px; border-radius:12px; border:1px solid rgba(142,163,186,.15);
  background:rgba(8,17,31,.72); backdrop-filter:blur(8px);
}}
.state.error {{ color:#ffc1ca; }}
.state.error .state-card {{ border-color:rgba(255,77,103,.34); background:rgba(61,14,25,.72); }}
.loader-dot {{ display:inline-block; width:7px; height:7px; margin-right:8px; border-radius:50%; background:{CYAN}; box-shadow:0 0 12px {CYAN}; animation:pulse 1s infinite alternate; }}
@keyframes pulse {{ from {{ opacity:.35; transform:scale(.8); }} to {{ opacity:1; transform:scale(1.15); }} }}
</style>
{scripts_html}
</head>
<body>
<div class="shell">
  <div id="chartdiv"></div>
  <div id="chart-state" class="state"><div class="state-card"><span class="loader-dot"></span>Inicializando visualização</div></div>
</div>
<script>
(function() {{
  const state = document.getElementById("chart-state");
  function ready() {{ if (state) state.style.display = "none"; }}
  function fail(message) {{
    if (!state) return;
    state.className = "state error";
    state.innerHTML = '<div class="state-card">Falha ao carregar o gráfico: ' + String(message || "biblioteca indisponível") + '</div>';
  }}
  function boot() {{
    try {{
      if (typeof am5 === "undefined") throw new Error("amCharts Core não carregou");
      {chart_js}
      ready();
    }} catch (err) {{
      console.error("Meu Financeiro / amCharts", err);
      fail(err && err.message ? err.message : err);
    }}
  }}
  if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", boot, {{ once:true }});
  else boot();
  setTimeout(function() {{
    if (state && state.style.display !== "none" && !state.classList.contains("error")) fail("tempo limite ao carregar os scripts externos");
  }}, 8000);
}})();
</script>
</body>
</html>
"""


def _render(document, height):
    st.iframe(document, width="stretch", height=height + 4, tab_index=-1)


def render_flow_chart(monthly, height=390):
    records = []
    for _, row in monthly.iterrows():
        records.append({
            "period": _month_label(row.get("period", "")),
            "income": round(_to_float(row.get("income", 0)), 2),
            "expense": round(_to_float(row.get("expense", 0)), 2),
            "balance": round(_to_float(row.get("balance", 0)), 2),
        })
    data = _safe_json(records)
    js = f"""
const data = {data};
const root = am5.Root.new("chartdiv");
root.setThemes([am5themes_Animated.new(root)]);
root.numberFormatter.set("numberFormat", "#,###.00");
const chart = root.container.children.push(am5xy.XYChart.new(root, {{ panX:false, panY:false, wheelX:"none", wheelY:"none", paddingLeft:8, paddingRight:16, paddingTop:22, paddingBottom:6, layout:root.verticalLayout }}));
const xRenderer = am5xy.AxisRendererX.new(root, {{ minGridDistance:32 }});
xRenderer.labels.template.setAll({{ fill:am5.color(0x8EA3BA), fontSize:11, paddingTop:9 }});
xRenderer.grid.template.setAll({{ stroke:am5.color(0x1F3B57), strokeOpacity:.20 }});
const xAxis = chart.xAxes.push(am5xy.CategoryAxis.new(root, {{ categoryField:"period", renderer:xRenderer }}));
xAxis.data.setAll(data);
const yRenderer = am5xy.AxisRendererY.new(root, {{}});
yRenderer.labels.template.setAll({{ fill:am5.color(0x8EA3BA), fontSize:10, paddingRight:7 }});
yRenderer.grid.template.setAll({{ stroke:am5.color(0x244861), strokeOpacity:.24, strokeDasharray:[3,4] }});
const yAxis = chart.yAxes.push(am5xy.ValueAxis.new(root, {{ renderer:yRenderer, extraMax:.15, extraMin:.09 }}));
function column(name, field, color) {{
  const s = chart.series.push(am5xy.ColumnSeries.new(root, {{ name:name, xAxis:xAxis, yAxis:yAxis, valueYField:field, categoryXField:"period", tooltip:am5.Tooltip.new(root, {{ labelText:"[bold]{{name}}[/]\\n{{categoryX}}\\nR$ {{valueY.formatNumber('#,###.00')}}" }}) }}));
  s.columns.template.setAll({{ width:am5.percent(68), cornerRadiusTL:7, cornerRadiusTR:7, fill:am5.color(color), strokeOpacity:0, shadowColor:am5.color(color), shadowBlur:14, shadowOpacity:.20 }});
  s.columns.template.states.create("hover", {{ scale:1.04, shadowOpacity:.45 }});
  s.data.setAll(data); s.appear(900,100); return s;
}}
const receitas = column("Receitas","income",0x16E07A);
const despesas = column("Despesas","expense",0xFF4D67);
const saldo = chart.series.push(am5xy.LineSeries.new(root, {{ name:"Saldo", xAxis:xAxis, yAxis:yAxis, valueYField:"balance", categoryXField:"period", stroke:am5.color(0x00E7FF), fill:am5.color(0x00E7FF), tooltip:am5.Tooltip.new(root, {{ labelText:"[bold]Saldo[/]\\n{{categoryX}}\\nR$ {{valueY.formatNumber('#,###.00')}}" }}) }}));
saldo.strokes.template.setAll({{ strokeWidth:3, shadowColor:am5.color(0x00E7FF), shadowBlur:14, shadowOpacity:.42 }});
saldo.bullets.push(function() {{ return am5.Bullet.new(root, {{ sprite:am5.Circle.new(root, {{ radius:4.5, fill:am5.color(0x08111F), stroke:am5.color(0x00E7FF), strokeWidth:3 }}) }}); }});
saldo.data.setAll(data); saldo.appear(1150,120);
const cursor = chart.set("cursor", am5xy.XYCursor.new(root, {{ behavior:"none" }}));
cursor.lineY.set("visible",false); cursor.lineX.setAll({{ stroke:am5.color(0x00E7FF), strokeOpacity:.28, strokeDasharray:[4,4] }});
const legend = chart.children.push(am5.Legend.new(root, {{ centerX:am5.p50, x:am5.p50, marginTop:4 }}));
legend.labels.template.setAll({{ fill:am5.color(0xC8D6E5), fontSize:11 }}); legend.valueLabels.template.set("forceHidden",true); legend.data.setAll([receitas,despesas,saldo]);
chart.appear(700,80);
"""
    _render(_iframe_document(js, height=height, modules=("xy",)), height)


def render_expense_donut(cat, total=None, height=390):
    records = []
    for _, row in cat.iterrows():
        records.append({"category": str(row.get("category", "Outros")), "value": round(_to_float(row.get("amount", 0)), 2)})
    total_value = _to_float(total) if total is not None else sum(item["value"] for item in records)
    total_br = f"{total_value:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
    data = _safe_json(records)
    js = f"""
const data = {data};
const root = am5.Root.new("chartdiv");
root.setThemes([am5themes_Animated.new(root)]);
root.numberFormatter.set("numberFormat","#,###.00");
const chart = root.container.children.push(am5percent.PieChart.new(root, {{ innerRadius:am5.percent(67), layout:root.horizontalLayout, paddingTop:14, paddingBottom:10, paddingLeft:8, paddingRight:8 }}));
const series = chart.series.push(am5percent.PieSeries.new(root, {{ valueField:"value", categoryField:"category", alignLabels:false, tooltip:am5.Tooltip.new(root, {{ labelText:"[bold]{{category}}[/]\\nR$ {{value.formatNumber('#,###.00')}}\\n{{valuePercentTotal.formatNumber('0.0')}}% do total" }}) }}));
series.get("colors").set("colors",[am5.color(0xFF4D67),am5.color(0xFF8A3D),am5.color(0xFFB020),am5.color(0xD946EF),am5.color(0x7C5CFF),am5.color(0x00E7FF),am5.color(0x16E07A)]);
series.labels.template.set("forceHidden",true); series.ticks.template.set("forceHidden",true);
series.slices.template.setAll({{ stroke:am5.color(0x0E1B2E), strokeWidth:3, strokeOpacity:1, cornerRadius:5, toggleKey:"none", shadowBlur:10, shadowOpacity:.16 }});
series.slices.template.states.create("hover",{{ scale:1.05, shiftRadius:6, shadowOpacity:.40 }}); series.data.setAll(data);
const center = chart.seriesContainer.children.push(am5.Container.new(root, {{ centerX:am5.p50, centerY:am5.p50, x:am5.p50, y:am5.p50, layout:root.verticalLayout }}));
center.children.push(am5.Label.new(root, {{ text:"DESPESAS", fill:am5.color(0x8EA3BA), fontSize:10, fontWeight:"600", centerX:am5.p50, x:am5.p50 }}));
center.children.push(am5.Label.new(root, {{ text:"R$ {total_br}", fill:am5.color(0xF8FAFC), fontSize:20, fontWeight:"700", centerX:am5.p50, x:am5.p50, paddingTop:4 }}));
const legend = chart.children.push(am5.Legend.new(root, {{ centerY:am5.p50, y:am5.p50, layout:root.verticalLayout, width:am5.percent(39), marginLeft:10 }}));
legend.labels.template.setAll({{ fill:am5.color(0xC8D6E5), fontSize:11, maxWidth:150, oversizedBehavior:"truncate" }}); legend.valueLabels.template.setAll({{ fill:am5.color(0x8EA3BA), fontSize:10 }}); legend.data.setAll(series.dataItems);
series.appear(1000,80);
"""
    _render(_iframe_document(js, height=height, modules=("percent",)), height)


def render_balance_chart(daily, height=340):
    records = []
    for _, row in daily.iterrows():
        records.append({"date": _date_ms(row.get("date")), "balance": round(_to_float(row.get("acumulado", 0)), 2)})
    final = records[-1]["balance"] if records else 0.0
    color = 0x16E07A if final >= 0 else 0xFF4D67
    data = _safe_json(records)
    js = f"""
const data = {data};
const root = am5.Root.new("chartdiv");
root.setThemes([am5themes_Animated.new(root)]);
root.numberFormatter.set("numberFormat","#,###.00"); root.dateFormatter.setAll({{ dateFormat:"dd/MM/yyyy", dateFields:["valueX"] }});
const chart = root.container.children.push(am5xy.XYChart.new(root, {{ panX:false, panY:false, wheelX:"none", wheelY:"none", paddingLeft:8, paddingRight:16, paddingTop:22, paddingBottom:8 }}));
const xr = am5xy.AxisRendererX.new(root, {{ minGridDistance:58 }}); xr.labels.template.setAll({{ fill:am5.color(0x8EA3BA), fontSize:10 }}); xr.grid.template.setAll({{ stroke:am5.color(0x1F3B57), strokeOpacity:.16 }});
const xAxis = chart.xAxes.push(am5xy.DateAxis.new(root, {{ baseInterval:{{ timeUnit:"day", count:1 }}, renderer:xr }}));
const yr = am5xy.AxisRendererY.new(root, {{}}); yr.labels.template.setAll({{ fill:am5.color(0x8EA3BA), fontSize:10, paddingRight:7 }}); yr.grid.template.setAll({{ stroke:am5.color(0x244861), strokeOpacity:.24, strokeDasharray:[3,4] }});
const yAxis = chart.yAxes.push(am5xy.ValueAxis.new(root, {{ renderer:yr, extraMax:.16, extraMin:.13 }}));
const series = chart.series.push(am5xy.LineSeries.new(root, {{ xAxis:xAxis, yAxis:yAxis, valueXField:"date", valueYField:"balance", stroke:am5.color({color}), fill:am5.color({color}), tooltip:am5.Tooltip.new(root, {{ labelText:"{{valueX.formatDate('dd/MM/yyyy')}}\\n[bold]Saldo: R$ {{valueY.formatNumber('#,###.00')}}[/]" }}) }}));
series.strokes.template.setAll({{ strokeWidth:3, shadowColor:am5.color({color}), shadowBlur:15, shadowOpacity:.42 }});
series.fills.template.setAll({{ visible:true, fillOpacity:1, fillGradient:am5.LinearGradient.new(root, {{ rotation:90, stops:[{{ color:am5.color({color}), opacity:.32 }},{{ color:am5.color({color}), opacity:.02 }}] }}) }});
series.bullets.push(function() {{ return am5.Bullet.new(root, {{ sprite:am5.Circle.new(root, {{ radius:4.5, fill:am5.color(0x08111F), stroke:am5.color({color}), strokeWidth:3 }}) }}); }}); series.data.setAll(data);
const zero = yAxis.createAxisRange(yAxis.makeDataItem({{ value:0 }})); zero.get("grid").setAll({{ stroke:am5.color(0x8EA3BA), strokeOpacity:.38, strokeDasharray:[5,5], strokeWidth:1 }});
const cursor = chart.set("cursor", am5xy.XYCursor.new(root, {{ behavior:"none" }})); cursor.lineY.set("visible",false); cursor.lineX.setAll({{ stroke:am5.color({color}), strokeOpacity:.30, strokeDasharray:[4,4] }});
series.appear(1050,80); chart.appear(700,50);
"""
    _render(_iframe_document(js, height=height, modules=("xy",)), height)
