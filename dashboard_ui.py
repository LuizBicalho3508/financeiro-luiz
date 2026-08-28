import streamlit as st


def inject_dashboard_theme():
    st.markdown(
        """
        <style>
        :root {
            --fin-bg: #07101d;
            --fin-panel: #0d192a;
            --fin-panel-2: #101f34;
            --fin-border: rgba(87, 164, 220, .18);
            --fin-cyan: #00e7ff;
            --fin-blue: #4d7cfe;
            --fin-green: #16e07a;
            --fin-red: #ff4d67;
            --fin-amber: #ffb020;
            --fin-text: #f8fafc;
            --fin-muted: #8ea3ba;
        }

        .stApp {
            background:
                radial-gradient(1100px 520px at 72% -20%, rgba(77,124,254,.09), transparent 58%),
                radial-gradient(900px 480px at 12% 0%, rgba(0,231,255,.055), transparent 56%),
                #07101d;
        }

        .block-container {
            max-width: 1540px;
            padding-top: 1.05rem;
        }

        [data-testid="stSidebar"] {
            border-right: 1px solid rgba(0,231,255,.10);
            background:
                radial-gradient(480px 300px at 20% 0%, rgba(0,231,255,.055), transparent 65%),
                linear-gradient(180deg, #0b1626 0%, #08111f 100%);
        }

        [data-testid="stSidebar"] [role="radiogroup"] label {
            border-radius: 10px;
            padding: .28rem .45rem;
            transition: background .16s ease, transform .16s ease;
        }

        [data-testid="stSidebar"] [role="radiogroup"] label:hover {
            background: rgba(0,231,255,.055);
            transform: translateX(2px);
        }

        .dashboard-hero {
            position: relative;
            overflow: hidden;
            display: flex;
            align-items: center;
            justify-content: space-between;
            gap: 20px;
            padding: 22px 24px;
            margin: 0 0 18px 0;
            border-radius: 20px;
            border: 1px solid rgba(0,231,255,.16);
            background:
                radial-gradient(540px 180px at 8% 0%, rgba(0,231,255,.14), transparent 72%),
                radial-gradient(440px 190px at 95% 0%, rgba(77,124,254,.13), transparent 72%),
                linear-gradient(135deg, rgba(14,29,49,.98), rgba(8,17,31,.98));
            box-shadow: 0 18px 54px rgba(1,7,18,.28), inset 0 1px 0 rgba(255,255,255,.035);
        }

        .dashboard-hero::after {
            content: "";
            position: absolute;
            left: 22px;
            right: 22px;
            bottom: 0;
            height: 2px;
            background: linear-gradient(90deg, #00e7ff, #4d7cfe, #16e07a, transparent);
            filter: drop-shadow(0 0 7px rgba(0,231,255,.65));
        }

        .dashboard-hero::before {
            content: "";
            position: absolute;
            width: 260px;
            height: 260px;
            right: 15%;
            top: -205px;
            border-radius: 50%;
            border: 1px solid rgba(0,231,255,.14);
            box-shadow: 0 0 80px rgba(0,231,255,.08);
        }

        .hero-kicker {
            font-size: .72rem;
            font-weight: 800;
            letter-spacing: .20em;
            color: #00e7ff;
            text-transform: uppercase;
            text-shadow: 0 0 14px rgba(0,231,255,.30);
            margin-bottom: 5px;
        }

        .hero-title {
            margin: 0;
            color: #f8fafc;
            font-size: clamp(1.55rem, 2.5vw, 2.25rem);
            line-height: 1.08;
            letter-spacing: -.045em;
            font-weight: 850;
        }

        .hero-subtitle {
            margin-top: 7px;
            color: #8ea3ba;
            font-size: .86rem;
            max-width: 680px;
        }

        .hero-status {
            display: flex;
            align-items: center;
            justify-content: flex-end;
            flex-wrap: wrap;
            gap: 8px;
            min-width: 245px;
        }

        .status-chip {
            display: inline-flex;
            align-items: center;
            gap: 7px;
            padding: 8px 11px;
            border-radius: 9px;
            border: 1px solid rgba(0,231,255,.23);
            background: rgba(3,17,29,.68);
            color: #bfeffc;
            font-size: .70rem;
            font-weight: 800;
            letter-spacing: .07em;
            text-transform: uppercase;
        }

        .status-chip.green {
            color: #7fffb7;
            border-color: rgba(22,224,122,.30);
            box-shadow: inset 0 0 18px rgba(22,224,122,.045);
        }

        .status-dot {
            width: 7px;
            height: 7px;
            border-radius: 50%;
            background: #16e07a;
            box-shadow: 0 0 12px rgba(22,224,122,.85);
        }

        .dashboard-context {
            margin: 7px 0 14px 0 !important;
            color: #9fb1c5 !important;
            letter-spacing: .025em;
        }

        .kpi-card {
            min-height: 150px !important;
            padding: 18px !important;
            border-radius: 18px !important;
            border: 1px solid rgba(87,164,220,.17) !important;
            background: linear-gradient(145deg, rgba(16,31,52,.96), rgba(10,21,37,.96)) !important;
            box-shadow: 0 14px 36px rgba(1,7,18,.22), inset 0 1px 0 rgba(255,255,255,.035) !important;
        }

        .kpi-card::before {
            content: "";
            position: absolute;
            top: 0;
            left: 14px;
            right: 14px;
            height: 2px;
            border-radius: 999px;
            background: linear-gradient(90deg, transparent, var(--kpi-color), transparent);
            opacity: .85;
            filter: drop-shadow(0 0 7px var(--kpi-color));
        }

        .kpi-card::after {
            width: 140px !important;
            height: 140px !important;
            right: -70px !important;
            top: -75px !important;
            opacity: .12 !important;
            filter: blur(7px) !important;
        }

        .kpi-card:hover {
            transform: translateY(-3px) !important;
            border-color: color-mix(in srgb, var(--kpi-color) 35%, rgba(148,163,184,.18)) !important;
            box-shadow: 0 18px 42px rgba(1,7,18,.30), 0 0 22px color-mix(in srgb, var(--kpi-color) 8%, transparent) !important;
        }

        .kpi-label {
            color: #aebdd0 !important;
            font-size: .70rem !important;
            letter-spacing: .10em !important;
        }

        .kpi-icon {
            border: 1px solid color-mix(in srgb, var(--kpi-color) 28%, transparent);
            box-shadow: inset 0 0 14px color-mix(in srgb, var(--kpi-color) 8%, transparent);
        }

        .kpi-value {
            font-size: clamp(1.34rem, 1.72vw, 1.88rem) !important;
            text-shadow: 0 0 18px color-mix(in srgb, var(--kpi-color) 18%, transparent);
        }

        .kpi-caption { color: #7f93aa !important; }

        .panel-heading {
            display: flex;
            align-items: center;
            gap: 9px;
            margin: 23px 0 10px 0;
            color: #e7eef8;
            font-size: .78rem;
            font-weight: 800;
            letter-spacing: .075em;
            text-transform: uppercase;
        }

        .panel-heading::before {
            content: "";
            width: 4px;
            height: 17px;
            border-radius: 999px;
            background: linear-gradient(180deg, #00e7ff, #4d7cfe);
            box-shadow: 0 0 11px rgba(0,231,255,.45);
        }

        .panel-heading .panel-meta {
            margin-left: auto;
            color: #71869d;
            font-size: .64rem;
            font-weight: 700;
            letter-spacing: .10em;
        }

        div[data-baseweb="select"] > div {
            border-radius: 11px !important;
            background: rgba(13,25,42,.86) !important;
            border-color: rgba(87,164,220,.20) !important;
        }

        div[data-baseweb="select"] > div:focus-within {
            border-color: rgba(0,231,255,.48) !important;
            box-shadow: 0 0 0 1px rgba(0,231,255,.10), 0 0 20px rgba(0,231,255,.06);
        }

        [data-testid="stDataFrame"] {
            border: 1px solid rgba(87,164,220,.14);
            border-radius: 17px;
            background: rgba(11,22,38,.74);
            box-shadow: 0 12px 34px rgba(1,7,18,.16);
            overflow: hidden;
        }

        [data-testid="stProgress"] > div > div { border-radius: 999px; }

        @media (max-width: 900px) {
            .dashboard-hero { align-items: flex-start; flex-direction: column; padding: 19px; }
            .hero-status { justify-content: flex-start; min-width: 0; }
            .kpi-card { min-height: 132px !important; }
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


def render_dashboard_hero(today):
    st.markdown(
        f"""
        <div class="dashboard-hero">
            <div>
                <div class="hero-kicker">Meu Financeiro // Control Center</div>
                <div class="hero-title">Central de controle financeiro</div>
                <div class="hero-subtitle">Visão consolidada de receitas, despesas, compromissos e evolução do seu saldo.</div>
            </div>
            <div class="hero-status">
                <div class="status-chip green"><span class="status-dot"></span> Operacional</div>
                <div class="status-chip">MongoDB online</div>
                <div class="status-chip">{today.strftime('%d/%m/%Y')}</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def section_title(title, meta=""):
    meta_html = f'<span class="panel-meta">{meta}</span>' if meta else ""
    st.markdown(
        f'<div class="panel-heading">{title}{meta_html}</div>',
        unsafe_allow_html=True,
    )
