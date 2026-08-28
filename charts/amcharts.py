import json
from datetime import date, datetime

import pandas as pd
from streamlit.components.v1 import html as components_html


CDN_CORE = "https://cdn.amcharts.com/lib/5/index.js"
CDN_XY = "https://cdn.amcharts.com/lib/5/xy.js"
CDN_PERCENT = "https://cdn.amcharts.com/lib/5/percent.js"
CDN_ANIMATED = "https://cdn.amcharts.com/lib/5/themes/Animated.js"

BG = "#0B1220"
PANEL = "#111B2E"
GRID = "#334155"
TEXT = "#E2E8F0"
MUTED = "#94A3B8"
GREEN = "#22C55E"
RED = "#EF4444"
CYAN = "#38BDF8"
AMBER = "#F59E0B"


MONTHS_PT = {
    1: "Jan", 2: "Fev", 3: "Mar", 4: "Abr", 5: "Mai", 6: "Jun",
    7: "Jul", 8: "Ago", 9: "Set", 10: "Out", 11: "Nov", 12: "Dez",
}


def _safe_json(value):
    return json.dumps(value, ensure_ascii=False, separators=(",", ":")).replace("</", "<\\/")


def _month_label(value):
    text = str(value)
    try:
        year, month = text.split("-")[:2]
        return f"{MONTHS_PT[int(month)]}/{year[-2:]}"
    except Exception:
        return text


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


def _date_ms(value):
    if isinstance(value, pd.Timestamp):
        value = value.to_pydatetime()
    if isinstance(value, date) and not isinstance(value, datetime):
        value = datetime.combine(value, datetime.min.time())
    if not isinstance(value, datetime):
        value = pd.to_datetime(value).to_pydatetime()
    return int(value.timestamp() * 1000)


def _base_html(chart_js, *, height=390, modules=("xy",)):
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
<meta charset="utf-8" />
<meta name="viewport" content="width=device-width, initial-scale=1" />
<style>
html, body {{ margin: 0; padding: 0; background: transparent; color: {TEXT}; font-family: Inter, ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif; }}
* {{ box-sizing: border-box; }}
.chart-shell {{
  width: 100%; height: {height}px; position: relative; overflow: hidden;
  border: 1px solid rgba(148,163,184,.12); border-radius: 18px;
  background:
    radial-gradient(circle at 85% 10%, rgba(56,189,248,.08), transparent 30%),
    linear-gradient(145deg, rgba(17,27,46,.98), rgba(11,18,32,.98));
  box-shadow: inset 0 1px 0 rgba(255,255,255,.025), 0 12px 32px rgba(2,6,23,.18);
}}
.chart-shell::before {{
  content: ""; position: absolute; inset: 0; pointer-events: none; z-index: 2;
  background-image: linear-gradient(rgba(148,163,184,.025) 1px, transparent 1px), linear-gradient(90deg, rgba(148,163,184,.025) 1px, transparent 1px);
  background-size: 28px 28px; mask-image: linear-gradient(to bottom, rgba(0,0,0,.7), transparent 85%);
}}
#chartdiv {{ width: 100%; height: 100%; position: relative; z-index: 1; }}
.loading {{ position: absolute; inset: 0; display: grid; place-items: center; color: {MUTED}; font-size: 13px; z-index: 0; }}
</style>
{scripts_html}
</head>
<body>
<div class="chart-shell"><div class="loading">Carregando visualização…</div><div id="chartdiv"></div></div>
<script>
am5.ready(function() {{
  {chart_js}
}});
</script>
</body>
</html>
"""


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
var data = {data};
var root = am5.Root.new("chartdiv");
root.setThemes([am5themes_Animated.new(root)]);
root.numberFormatter.set("numberFormat", "#,###.00");

var chart = root.container.children.push(am5xy.XYChart.new(root, {{
  panX: false, panY: false, wheelX: "none", wheelY: "none",
  paddingLeft: 10, paddingRight: 16, paddingTop: 18, paddingBottom: 4,
  layout: root.verticalLayout
}}));

var xRenderer = am5xy.AxisRendererX.new(root, {{ minGridDistance: 32 }});
xRenderer.labels.template.setAll({{ fill: am5.color(0x94A3B8), fontSize: 11, paddingTop: 8 }});
xRenderer.grid.template.setAll({{ stroke: am5.color(0x334155), strokeOpacity: 0.16 }});
var xAxis = chart.xAxes.push(am5xy.CategoryAxis.new(root, {{ categoryField: "period", renderer: xRenderer }}));
xAxis.data.setAll(data);

var yRenderer = am5xy.AxisRendererY.new(root, {{}});
yRenderer.labels.template.setAll({{ fill: am5.color(0x94A3B8), fontSize: 11, paddingRight: 8 }});
yRenderer.grid.template.setAll({{ stroke: am5.color(0x334155), strokeOpacity: 0.22, strokeDasharray: [3,3] }});
var yAxis = chart.yAxes.push(am5xy.ValueAxis.new(root, {{ renderer: yRenderer, extraMax: 0.14, extraMin: 0.08 }}));

function makeColumnSeries(name, field, color) {{
  var series = chart.series.push(am5xy.ColumnSeries.new(root, {{
    name: name, xAxis: xAxis, yAxis: yAxis, valueYField: field, categoryXField: "period",
    clustered: true, tooltip: am5.Tooltip.new(root, {{ labelText: "[bold]{{name}}[/]\n{{categoryX}}\nR$ {{valueY.formatNumber('#,###.00')}}" }})
  }}));
  series.columns.template.setAll({{
    width: am5.percent(72), cornerRadiusTL: 7, cornerRadiusTR: 7,
    fill: am5.color(color), stroke: am5.color(color), strokeOpacity: 0,
    shadowColor: am5.color(color), shadowBlur: 10, shadowOpacity: 0.16
  }});
  series.columns.template.states.create("hover", {{ scale: 1.035, shadowOpacity: 0.34 }});
  series.data.setAll(data);
  series.appear(900);
  return series;
}}

var incomeSeries = makeColumnSeries("Receitas", "income", 0x22C55E);
var expenseSeries = makeColumnSeries("Despesas", "expense", 0xEF4444);

var balanceSeries = chart.series.push(am5xy.LineSeries.new(root, {{
  name: "Saldo", xAxis: xAxis, yAxis: yAxis, valueYField: "balance", categoryXField: "period",
  stroke: am5.color(0x38BDF8), fill: am5.color(0x38BDF8),
  tooltip: am5.Tooltip.new(root, {{ labelText: "[bold]Saldo[/]\n{{categoryX}}\nR$ {{valueY.formatNumber('#,###.00')}}" }})
}}));
balanceSeries.strokes.template.setAll({{ strokeWidth: 3, shadowColor: am5.color(0x38BDF8), shadowBlur: 10, shadowOpacity: 0.35 }});
balanceSeries.bullets.push(function() {{
  return am5.Bullet.new(root, {{ sprite: am5.Circle.new(root, {{ radius: 4.5, fill: am5.color(0x0B1220), stroke: am5.color(0x38BDF8), strokeWidth: 3 }}) }});
}});
balanceSeries.data.setAll(data);
balanceSeries.appear(1100);

var cursor = chart.set("cursor", am5xy.XYCursor.new(root, {{ behavior: "none" }}));
cursor.lineY.set("visible", false);
cursor.lineX.setAll({{ stroke: am5.color(0x38BDF8), strokeOpacity: 0.28, strokeDasharray: [4,4] }});

var legend = chart.children.push(am5.Legend.new(root, {{ centerX: am5.p50, x: am5.p50, marginTop: 4 }}));
legend.labels.template.setAll({{ fill: am5.color(0xCBD5E1), fontSize: 11 }});
legend.valueLabels.template.set("forceHidden", true);
legend.data.setAll([incomeSeries, expenseSeries, balanceSeries]);

chart.appear(700, 80);
"""
    components_html(_base_html(js, height=height, modules=("xy",)), height=height + 8, scrolling=False)


def render_expense_donut(cat, total=None, height=390):
    records = []
    for _, row in cat.iterrows():
        records.append({"category": str(row.get("category", "Outros")), "value": round(_to_float(row.get("amount", 0)), 2)})
    total_value = _to_float(total) if total is not None else sum(item["value"] for item in records)
    data = _safe_json(records)

    js = f"""
var data = {data};
var root = am5.Root.new("chartdiv");
root.setThemes([am5themes_Animated.new(root)]);
root.numberFormatter.set("numberFormat", "#,###.00");
var chart = root.container.children.push(am5percent.PieChart.new(root, {{
  innerRadius: am5.percent(64), layout: root.horizontalLayout,
  paddingTop: 12, paddingBottom: 10, paddingLeft: 4, paddingRight: 4
}}));

var series = chart.series.push(am5percent.PieSeries.new(root, {{
  valueField: "value", categoryField: "category", alignLabels: false,
  tooltip: am5.Tooltip.new(root, {{ labelText: "[bold]{{category}}[/]\nR$ {{value.formatNumber('#,###.00')}}\n{{valuePercentTotal.formatNumber('0.0')}}% do total" }})
}}));
series.get("colors").set("colors", [
  am5.color(0xEF4444), am5.color(0xF97316), am5.color(0xF59E0B),
  am5.color(0xE11D48), am5.color(0xFB7185), am5.color(0x38BDF8), am5.color(0x8B5CF6)
]);
series.labels.template.set("forceHidden", true);
series.ticks.template.set("forceHidden", true);
series.slices.template.setAll({{
  stroke: am5.color(0x111B2E), strokeWidth: 3, strokeOpacity: 1,
  cornerRadius: 5, toggleKey: "none", shadowBlur: 8, shadowOpacity: 0.12
}});
series.slices.template.states.create("hover", {{ scale: 1.045, shiftRadius: 5, shadowOpacity: 0.30 }});
series.data.setAll(data);

var center = chart.seriesContainer.children.push(am5.Container.new(root, {{
  centerX: am5.p50, centerY: am5.p50, x: am5.p50, y: am5.p50,
  layout: root.verticalLayout
}}));
center.children.push(am5.Label.new(root, {{
  text: "DESPESAS", fill: am5.color(0x94A3B8), fontSize: 11, fontWeight: "600", centerX: am5.p50, x: am5.p50
}}));
center.children.push(am5.Label.new(root, {{
  text: "R$ {total_value:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."),
  fill: am5.color(0xF8FAFC), fontSize: 20, fontWeight: "700", centerX: am5.p50, x: am5.p50, paddingTop: 3
}}));

var legend = chart.children.push(am5.Legend.new(root, {{
  centerY: am5.p50, y: am5.p50, layout: root.verticalLayout, width: am5.percent(38), marginLeft: 8
}}));
legend.labels.template.setAll({{ fill: am5.color(0xCBD5E1), fontSize: 11, maxWidth: 145, oversizedBehavior: "truncate" }});
legend.valueLabels.template.setAll({{ fill: am5.color(0x94A3B8), fontSize: 10 }});
legend.data.setAll(series.dataItems);

series.appear(1000, 80);
"""
    components_html(_base_html(js, height=height, modules=("percent",)), height=height + 8, scrolling=False)


def render_balance_chart(daily, height=340):
    records = []
    for _, row in daily.iterrows():
        records.append({"date": _date_ms(row.get("date")), "balance": round(_to_float(row.get("acumulado", 0)), 2)})
    final = records[-1]["balance"] if records else 0.0
    color = GREEN if final >= 0 else RED
    color_hex = color.replace("#", "0x")
    rgba = "34,197,94" if final >= 0 else "239,68,68"
    data = _safe_json(records)

    js = f"""
var data = {data};
var root = am5.Root.new("chartdiv");
root.setThemes([am5themes_Animated.new(root)]);
root.numberFormatter.set("numberFormat", "#,###.00");
root.dateFormatter.setAll({{ dateFormat: "dd/MM/yyyy", dateFields: ["valueX"] }});

var chart = root.container.children.push(am5xy.XYChart.new(root, {{
  panX: false, panY: false, wheelX: "none", wheelY: "none",
  paddingLeft: 10, paddingRight: 16, paddingTop: 18, paddingBottom: 5
}}));

var xRenderer = am5xy.AxisRendererX.new(root, {{ minGridDistance: 58 }});
xRenderer.labels.template.setAll({{ fill: am5.color(0x94A3B8), fontSize: 11 }});
xRenderer.grid.template.setAll({{ stroke: am5.color(0x334155), strokeOpacity: 0.12 }});
var xAxis = chart.xAxes.push(am5xy.DateAxis.new(root, {{ baseInterval: {{ timeUnit: "day", count: 1 }}, renderer: xRenderer }}));

var yRenderer = am5xy.AxisRendererY.new(root, {{}});
yRenderer.labels.template.setAll({{ fill: am5.color(0x94A3B8), fontSize: 11, paddingRight: 8 }});
yRenderer.grid.template.setAll({{ stroke: am5.color(0x334155), strokeOpacity: 0.20, strokeDasharray: [3,3] }});
var yAxis = chart.yAxes.push(am5xy.ValueAxis.new(root, {{ renderer: yRenderer, extraMax: 0.16, extraMin: 0.12 }}));

var series = chart.series.push(am5xy.LineSeries.new(root, {{
  xAxis: xAxis, yAxis: yAxis, valueXField: "date", valueYField: "balance",
  stroke: am5.color({color_hex}), fill: am5.color({color_hex}),
  tooltip: am5.Tooltip.new(root, {{ labelText: "{{valueX.formatDate('dd/MM/yyyy')}}\n[bold]Saldo: R$ {{valueY.formatNumber('#,###.00')}}[/]" }})
}}));
series.strokes.template.setAll({{ strokeWidth: 3, shadowColor: am5.color({color_hex}), shadowBlur: 12, shadowOpacity: 0.38 }});
series.fills.template.setAll({{ visible: true, fillOpacity: 1, fillGradient: am5.LinearGradient.new(root, {{
  rotation: 90,
  stops: [{{ color: am5.color({color_hex}), opacity: 0.34 }}, {{ color: am5.color({color_hex}), opacity: 0.02 }}]
}}) }});
series.bullets.push(function() {{ return am5.Bullet.new(root, {{ sprite: am5.Circle.new(root, {{ radius: 4, fill: am5.color(0x0B1220), stroke: am5.color({color_hex}), strokeWidth: 2.5 }}) }}); }});
series.data.setAll(data);

var zeroDataItem = yAxis.makeDataItem({{ value: 0 }});
var zeroRange = yAxis.createAxisRange(zeroDataItem);
zeroRange.get("grid").setAll({{ stroke: am5.color(0x94A3B8), strokeOpacity: 0.55, strokeDasharray: [5,5] }});

var cursor = chart.set("cursor", am5xy.XYCursor.new(root, {{ behavior: "none" }}));
cursor.lineY.set("visible", false);
cursor.lineX.setAll({{ stroke: am5.color({color_hex}), strokeOpacity: 0.30, strokeDasharray: [4,4] }});

series.appear(1200);
chart.appear(700, 80);
"""
    components_html(_base_html(js, height=height, modules=("xy",)), height=height + 8, scrolling=False)
