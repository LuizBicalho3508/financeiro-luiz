from pathlib import Path

app_path = Path("app.py")
ui_path = Path("dashboard_ui.py")

app = app_path.read_text(encoding="utf-8")
ui = ui_path.read_text(encoding="utf-8")

# -----------------------------------------------------------------------------
# app.py - import para escapar dados exibidos em HTML da sidebar
# -----------------------------------------------------------------------------
if "import html\n" not in app:
    anchor = "import hmac\n"
    if anchor not in app:
        raise SystemExit("Âncora de imports não encontrada.")
    app = app.replace(anchor, anchor + "import html\n", 1)

# -----------------------------------------------------------------------------
# Próximos vencimentos - Valor primeiro, Data por último
# -----------------------------------------------------------------------------
old_table = '''            upcoming_view = view[["Data", "Tipo", "description", "Valor"]].rename(
                columns={"description": "Descrição"}
            )
'''
new_table = '''            upcoming_view = view[["Valor", "Tipo", "description", "Data"]].rename(
                columns={"description": "Descrição"}
            )
'''
if old_table in app:
    app = app.replace(old_table, new_table, 1)
elif 'upcoming_view = view[["Valor", "Tipo", "description", "Data"]]' not in app:
    raise SystemExit("Bloco da tabela de próximos vencimentos não encontrado.")

old_config = '''                column_config={
                    "Data": st.column_config.TextColumn("Data", width="small"),
                    "Tipo": st.column_config.TextColumn("Tipo", width="small"),
                    "Descrição": st.column_config.TextColumn("Descrição", width="large"),
                    "Valor": st.column_config.TextColumn("Valor", width="medium"),
                },
'''
new_config = '''                column_config={
                    "Valor": st.column_config.TextColumn("Valor", width="medium"),
                    "Tipo": st.column_config.TextColumn("Tipo", width="small"),
                    "Descrição": st.column_config.TextColumn("Descrição", width="large"),
                    "Data": st.column_config.TextColumn("Data", width="small"),
                },
'''
if old_config in app:
    app = app.replace(old_config, new_config, 1)

# -----------------------------------------------------------------------------
# Sidebar - troca radio por navegação em botões
# -----------------------------------------------------------------------------
old_sidebar = '''    with st.sidebar:
        st.markdown("## 💰 Meu Financeiro")
        st.caption(f"{user['name']} · {user['role']}")
        pages = ["Dashboard", "Lançar despesa", "Lançar receita", "Movimentações", "Orçamentos", "Minha conta"]
        if user["role"] == "admin":
            pages.append("Usuários")
        selected_page = st.radio("Navegação", pages, key="nav")
        st.divider()
        if st.button("Sair", width="stretch"):
            do_logout()
'''

new_sidebar = '''    with st.sidebar:
        safe_name = html.escape(str(user.get("name") or "Usuário"))
        safe_role = html.escape(str(user.get("role") or "user").upper())
        user_initial = safe_name[:1].upper() if safe_name else "U"

        st.markdown(
            f"""
            <div class="sidebar-brand-panel">
                <div class="sidebar-brand-mark">MF</div>
                <div>
                    <div class="sidebar-brand-title">MEU FINANCEIRO</div>
                    <div class="sidebar-brand-subtitle">CONTROL CENTER</div>
                </div>
            </div>
            <div class="sidebar-user-card">
                <div class="sidebar-user-avatar">{user_initial}</div>
                <div class="sidebar-user-copy">
                    <div class="sidebar-user-name">{safe_name}</div>
                    <div class="sidebar-user-role"><span></span>{safe_role} · ONLINE</div>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        pages = ["Dashboard", "Lançar despesa", "Lançar receita", "Movimentações", "Orçamentos", "Minha conta"]
        if user["role"] == "admin":
            pages.append("Usuários")

        nav_items = [
            ("Dashboard", "◫", "Visão geral das finanças", "dashboard"),
            ("Lançar despesa", "−", "Registrar nova despesa", "expense"),
            ("Lançar receita", "+", "Registrar nova receita", "income"),
            ("Movimentações", "⇄", "Consultar e gerenciar lançamentos", "transactions"),
            ("Orçamentos", "◎", "Definir limites por categoria", "budgets"),
            ("Minha conta", "○", "Perfil e segurança", "account"),
            ("Usuários", "◇", "Administração de usuários", "users"),
        ]

        selected_page = st.session_state.get("nav", "Dashboard")
        if selected_page not in pages:
            selected_page = "Dashboard"
            st.session_state["nav"] = selected_page

        st.markdown('<div class="sidebar-section-label">NAVEGAÇÃO</div>', unsafe_allow_html=True)
        for page, icon, hint, key_name in nav_items:
            if page not in pages:
                continue
            clicked = st.button(
                f"{icon}  {page}",
                key=f"nav_btn_{key_name}",
                type="primary" if selected_page == page else "secondary",
                width="stretch",
                help=hint,
            )
            if clicked:
                st.session_state["nav"] = page
                selected_page = page

        st.markdown(
            '<div class="sidebar-session-divider"><span>SESSÃO</span></div>',
            unsafe_allow_html=True,
        )
        if st.button("⏻  Encerrar sessão", key="logout_btn", width="stretch"):
            do_logout()
'''

if old_sidebar in app:
    app = app.replace(old_sidebar, new_sidebar, 1)
elif "sidebar-brand-panel" not in app:
    raise SystemExit("Bloco antigo da sidebar não encontrado.")

# -----------------------------------------------------------------------------
# dashboard_ui.py - identidade visual da nova sidebar
# -----------------------------------------------------------------------------
css_marker = '''        [data-testid="stProgress"] > div > div { border-radius: 999px; }
'''
sidebar_css = r'''
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
'''

if "sidebar-brand-panel" not in ui:
    if css_marker not in ui:
        raise SystemExit("Âncora CSS da sidebar não encontrada.")
    ui = ui.replace(css_marker, sidebar_css + "\n" + css_marker, 1)

app_path.write_text(app, encoding="utf-8")
ui_path.write_text(ui, encoding="utf-8")
print("Sidebar em botões e reordenação da tabela aplicadas com sucesso.")
