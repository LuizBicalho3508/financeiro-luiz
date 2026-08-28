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


        /* Global module pages */
        .module-page-hero {
            --module-accent: #00e7ff;
            position: relative;
            overflow: hidden;
            display: flex;
            align-items: center;
            gap: 15px;
            min-height: 112px;
            margin: 0 0 18px 0;
            padding: 18px 20px;
            border: 1px solid color-mix(in srgb, var(--module-accent) 24%, rgba(87,164,220,.14));
            border-radius: 18px;
            background: radial-gradient(420px 145px at 0% 0%, color-mix(in srgb, var(--module-accent) 10%, transparent), transparent 72%), linear-gradient(135deg, rgba(15,30,50,.96), rgba(8,17,31,.98));
            box-shadow: 0 16px 42px rgba(1,7,18,.22), inset 0 1px 0 rgba(255,255,255,.03);
        }
        .module-page-hero::after {
            content: "";
            position: absolute;
            left: 18px;
            right: 18px;
            bottom: 0;
            height: 2px;
            background: linear-gradient(90deg, var(--module-accent), transparent 75%);
            filter: drop-shadow(0 0 6px var(--module-accent));
            opacity: .78;
        }
        .module-page-blue { --module-accent: #00e7ff; }
        .module-page-green { --module-accent: #16e07a; }
        .module-page-red { --module-accent: #ff4d67; }
        .module-page-amber { --module-accent: #ffb020; }
        .module-page-icon {
            display: grid;
            place-items: center;
            width: 54px;
            height: 54px;
            flex: 0 0 54px;
            border-radius: 15px;
            border: 1px solid color-mix(in srgb, var(--module-accent) 34%, transparent);
            background: color-mix(in srgb, var(--module-accent) 9%, rgba(7,16,29,.75));
            color: var(--module-accent);
            font-size: 1.45rem;
            font-weight: 900;
            box-shadow: inset 0 0 20px color-mix(in srgb, var(--module-accent) 8%, transparent), 0 0 20px color-mix(in srgb, var(--module-accent) 6%, transparent);
        }
        .module-page-copy { min-width: 0; flex: 1; }
        .module-page-kicker { margin-bottom: 3px; color: var(--module-accent); font-size: .58rem; font-weight: 850; letter-spacing: .19em; text-transform: uppercase; }
        .module-page-title { color: #f6f9fd; font-size: clamp(1.25rem, 2vw, 1.75rem); font-weight: 850; letter-spacing: -.035em; line-height: 1.1; }
        .module-page-subtitle { max-width: 800px; margin-top: 5px; color: #8297ad; font-size: .78rem; line-height: 1.45; }
        .module-page-status { display: flex; align-items: center; gap: 6px; padding: 7px 9px; border: 1px solid rgba(22,224,122,.22); border-radius: 8px; color: #6ee7a4; background: rgba(22,224,122,.035); font-size: .54rem; font-weight: 850; letter-spacing: .09em; }
        .module-page-status span { width: 6px; height: 6px; border-radius: 50%; background: #16e07a; box-shadow: 0 0 8px rgba(22,224,122,.72); }

        [data-testid="stForm"] {
            padding: 18px 18px 8px 18px;
            border: 1px solid rgba(87,164,220,.14);
            border-radius: 17px;
            background: linear-gradient(145deg, rgba(13,25,42,.82), rgba(8,18,32,.72));
            box-shadow: 0 13px 34px rgba(1,7,18,.14), inset 0 1px 0 rgba(255,255,255,.025);
        }
        [data-testid="stTextInput"] input,
        [data-testid="stNumberInput"] input,
        [data-testid="stTextArea"] textarea,
        [data-testid="stDateInput"] input {
            border-color: rgba(87,164,220,.17) !important;
            border-radius: 10px !important;
            background: rgba(7,16,29,.64) !important;
        }
        [data-testid="stTextInput"] input:focus,
        [data-testid="stNumberInput"] input:focus,
        [data-testid="stTextArea"] textarea:focus,
        [data-testid="stDateInput"] input:focus {
            border-color: rgba(0,231,255,.42) !important;
            box-shadow: 0 0 0 1px rgba(0,231,255,.08), 0 0 16px rgba(0,231,255,.04) !important;
        }
        [data-testid="stExpander"] { border: 1px solid rgba(87,164,220,.14) !important; border-radius: 14px !important; background: rgba(11,22,38,.58) !important; overflow: hidden; }
        [data-testid="stAlert"] { border-radius: 13px; border-width: 1px; }

        .profile-summary-card { display: flex; align-items: center; gap: 14px; margin: 0 0 18px 0; padding: 16px 18px; border: 1px solid rgba(87,164,220,.15); border-radius: 16px; background: linear-gradient(145deg, rgba(15,30,50,.90), rgba(8,18,32,.82)); box-shadow: 0 12px 32px rgba(1,7,18,.16); }
        .profile-summary-avatar { display: grid; place-items: center; width: 46px; height: 46px; flex: 0 0 46px; border-radius: 50%; color: #06111f; background: linear-gradient(135deg, #00e7ff, #6ee7ff); font-size: 1rem; font-weight: 900; box-shadow: 0 0 22px rgba(0,231,255,.14); }
        .profile-summary-main { min-width: 0; flex: 1; }
        .profile-summary-name { color: #f4f8fc; font-size: .92rem; font-weight: 800; }
        .profile-summary-email { color: #8297ad; font-size: .72rem; margin-top: 2px; }
        .profile-summary-role { padding: 6px 9px; border: 1px solid rgba(0,231,255,.18); border-radius: 8px; color: #9defff; background: rgba(0,231,255,.04); font-size: .58rem; font-weight: 850; letter-spacing: .08em; }

        @media (max-width: 720px) {
            .module-page-hero { align-items: flex-start; }
            .module-page-status { display: none; }
            .module-page-icon { width: 45px; height: 45px; flex-basis: 45px; }
        }

        /* Sidebar / Control Center navigation */
        [data-testid="stSidebar"] > div:first-child {
            padding-top: .65rem;
        }

        .sidebar-brand-panel {
            display: flex;
            align-items: center;
            gap: 11px;
            padding: 12px 10px 15px 10px;
            margin: 0 0 10px 0;
            border-bottom: 1px solid rgba(0,231,255,.10);
        }

        .sidebar-brand-mark {
            display: grid;
            place-items: center;
            width: 39px;
            height: 39px;
            flex: 0 0 39px;
            border-radius: 11px;
            border: 1px solid rgba(0,231,255,.38);
            background: linear-gradient(145deg, rgba(0,231,255,.16), rgba(77,124,254,.12));
            color: #c7f8ff;
            font-size: .78rem;
            font-weight: 900;
            letter-spacing: .08em;
            box-shadow: inset 0 0 18px rgba(0,231,255,.08), 0 0 20px rgba(0,231,255,.06);
        }

        .sidebar-brand-title {
            color: #f4f9ff;
            font-size: .82rem;
            font-weight: 850;
            letter-spacing: .055em;
        }

        .sidebar-brand-subtitle {
            margin-top: 2px;
            color: #00e7ff;
            font-size: .55rem;
            font-weight: 800;
            letter-spacing: .19em;
            text-shadow: 0 0 11px rgba(0,231,255,.30);
        }

        .sidebar-user-card {
            display: flex;
            align-items: center;
            gap: 10px;
            margin: 8px 0 20px 0;
            padding: 11px;
            border: 1px solid rgba(87,164,220,.14);
            border-radius: 14px;
            background: linear-gradient(145deg, rgba(16,31,52,.80), rgba(8,18,32,.72));
            box-shadow: inset 0 1px 0 rgba(255,255,255,.025);
        }

        .sidebar-user-avatar {
            display: grid;
            place-items: center;
            width: 35px;
            height: 35px;
            flex: 0 0 35px;
            border-radius: 50%;
            color: #08121f;
            background: linear-gradient(135deg, #00e7ff, #6ee7ff);
            font-weight: 900;
            box-shadow: 0 0 18px rgba(0,231,255,.18);
        }

        .sidebar-user-copy { min-width: 0; }

        .sidebar-user-name {
            overflow: hidden;
            color: #eaf2fb;
            font-size: .75rem;
            font-weight: 750;
            text-overflow: ellipsis;
            white-space: nowrap;
        }

        .sidebar-user-role {
            display: flex;
            align-items: center;
            gap: 5px;
            margin-top: 3px;
            color: #72869b;
            font-size: .52rem;
            font-weight: 800;
            letter-spacing: .08em;
        }

        .sidebar-user-role span {
            width: 6px;
            height: 6px;
            border-radius: 50%;
            background: #16e07a;
            box-shadow: 0 0 8px rgba(22,224,122,.72);
        }

        .sidebar-section-label {
            margin: 0 4px 8px 4px;
            color: #61778d;
            font-size: .56rem;
            font-weight: 850;
            letter-spacing: .18em;
        }

        [data-testid="stSidebar"] div.stButton {
            margin-bottom: .24rem;
        }

        [data-testid="stSidebar"] div.stButton > button {
            min-height: 43px;
            justify-content: flex-start;
            padding: 0 13px;
            border-radius: 11px;
            border: 1px solid rgba(87,164,220,.11);
            background: rgba(10,22,38,.50);
            color: #91a7bd;
            font-size: .72rem;
            font-weight: 700;
            letter-spacing: .01em;
            box-shadow: none;
            transition: transform .15s ease, border-color .15s ease, background .15s ease, box-shadow .15s ease, color .15s ease;
        }

        [data-testid="stSidebar"] div.stButton > button:hover {
            transform: translateX(3px);
            border-color: rgba(0,231,255,.24);
            background: rgba(0,231,255,.055);
            color: #d9f9ff;
        }

        [data-testid="stSidebar"] button[kind="primary"],
        [data-testid="stSidebar"] button[data-testid="stBaseButton-primary"] {
            border-color: rgba(0,231,255,.32) !important;
            background: linear-gradient(90deg, rgba(0,231,255,.14), rgba(77,124,254,.09)) !important;
            color: #e9fcff !important;
            box-shadow: inset 3px 0 0 #00e7ff, 0 0 18px rgba(0,231,255,.055) !important;
        }

        .sidebar-session-divider {
            display: flex;
            align-items: center;
            gap: 8px;
            margin: 17px 3px 9px 3px;
            color: #53687e;
            font-size: .52rem;
            font-weight: 850;
            letter-spacing: .16em;
        }

        .sidebar-session-divider::after {
            content: "";
            height: 1px;
            flex: 1;
            background: linear-gradient(90deg, rgba(87,164,220,.14), transparent);
        }

        [data-testid="stSidebar"] .st-key-logout_btn button {
            border-color: rgba(255,77,103,.16) !important;
            background: rgba(255,77,103,.035) !important;
            color: #b98791 !important;
        }

        [data-testid="stSidebar"] .st-key-logout_btn button:hover {
            border-color: rgba(255,77,103,.34) !important;
            background: rgba(255,77,103,.08) !important;
            color: #ff8091 !important;
            box-shadow: inset 3px 0 0 #ff4d67 !important;
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


def render_page_header(title, subtitle, kicker="MÓDULO", icon="◫", tone="blue"):
    allowed = {"blue", "green", "red", "amber"}
    tone = tone if tone in allowed else "blue"
    st.markdown(
        f"""
        <div class="module-page-hero module-page-{tone}">
            <div class="module-page-icon">{icon}</div>
            <div class="module-page-copy">
                <div class="module-page-kicker">{kicker}</div>
                <div class="module-page-title">{title}</div>
                <div class="module-page-subtitle">{subtitle}</div>
            </div>
            <div class="module-page-status"><span></span> OPERACIONAL</div>
        </div>
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
