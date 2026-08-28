from pathlib import Path

app_path = Path('app.py')
ui_path = Path('dashboard_ui.py')
app = app_path.read_text(encoding='utf-8')
ui = ui_path.read_text(encoding='utf-8')

# 1) Importa o novo cabeçalho reutilizável.
old_import = 'from dashboard_ui import inject_dashboard_theme, render_dashboard_hero, section_title\n'
new_import = 'from dashboard_ui import inject_dashboard_theme, render_dashboard_hero, render_page_header, section_title\n'
if old_import in app:
    app = app.replace(old_import, new_import, 1)
elif 'render_page_header' not in app.split('\n', 30)[-1]:
    raise SystemExit('Import do dashboard_ui não encontrado.')

# 2) Tema global: não apenas no Dashboard.
app = app.replace('def page_dashboard(db, user):\n    inject_dashboard_theme()\n', 'def page_dashboard(db, user):\n', 1)
anchor = '''    user = current_user(db)\n    if not user:\n        render_login(db)\n        st.stop()\n\n    if user.get("must_change_password"):\n'''
replacement = '''    user = current_user(db)\n    if not user:\n        render_login(db)\n        st.stop()\n\n    # Identidade visual global da área autenticada.\n    # Mantém sidebar, formulários, tabelas e painéis consistentes em todas as páginas.\n    inject_dashboard_theme()\n\n    if user.get("must_change_password"):\n'''
if anchor in app:
    app = app.replace(anchor, replacement, 1)
elif 'Identidade visual global da área autenticada' not in app:
    raise SystemExit('Âncora para tema global não encontrada.')

# 3) Rerun ao navegar para recalcular imediatamente o estado ativo do botão.
old_click = '''            if clicked:\n                st.session_state["nav"] = page\n                selected_page = page\n'''
new_click = '''            if clicked:\n                st.session_state["nav"] = page\n                st.rerun()\n'''
if old_click in app:
    app = app.replace(old_click, new_click, 1)

# 4) Padroniza cabeçalhos das páginas.
headers = {
'''def page_add_expense(db, user):\n    st.title("Lançar despesa")\n    st.caption("Informe uma compra e o sistema cria automaticamente todas as parcelas.")\n''':
'''def page_add_expense(db, user):\n    render_page_header(\n        "Lançar despesa",\n        "Registre compras, contas e parcelamentos. O sistema distribui automaticamente os vencimentos futuros.",\n        "SAÍDAS",\n        "−",\n        "red",\n    )\n    section_title("Dados da despesa", "LANÇAMENTO INTELIGENTE")\n''',
'''def page_add_income(db, user):\n    st.title("Lançar receita")\n    st.caption("Cadastre uma receita única ou repita automaticamente por vários meses.")\n''':
'''def page_add_income(db, user):\n    render_page_header(\n        "Lançar receita",\n        "Cadastre entradas únicas ou recorrentes e mantenha sua previsão de caixa atualizada automaticamente.",\n        "ENTRADAS",\n        "+",\n        "green",\n    )\n    section_title("Dados da receita", "RECEBIMENTOS")\n''',
'''def page_transactions(db, user):\n    st.title("Movimentações")\n''':
'''def page_transactions(db, user):\n    render_page_header(\n        "Movimentações",\n        "Consulte, filtre, exporte e gerencie todo o histórico financeiro em um único painel operacional.",\n        "HISTÓRICO",\n        "⇄",\n        "blue",\n    )\n    section_title("Filtros e período", "CONSULTA")\n''',
'''def page_budgets(db, user):\n    st.title("Orçamentos")\n    st.caption("Defina limites mensais por categoria e acompanhe o consumo no dashboard.")\n''':
'''def page_budgets(db, user):\n    render_page_header(\n        "Orçamentos",\n        "Defina limites mensais por categoria e acompanhe quanto do orçamento já foi comprometido.",\n        "PLANEJAMENTO",\n        "◎",\n        "amber",\n    )\n    section_title("Configurar orçamento", "LIMITES MENSAIS")\n''',
'''def page_my_account(db, user):\n    st.title("Minha conta")\n    st.write(f"**Nome:** {user['name']}")\n    st.write(f"**E-mail:** {user['email']}")\n    st.write(f"**Perfil:** {user['role']}")\n\n    st.subheader("Alterar senha")\n''':
'''def page_my_account(db, user):\n    render_page_header(\n        "Minha conta",\n        "Gerencie seus dados de acesso e mantenha as credenciais da sua conta protegidas.",\n        "PERFIL & SEGURANÇA",\n        "○",\n        "blue",\n    )\n    safe_profile_name = html.escape(str(user.get("name") or "Usuário"))\n    safe_profile_email = html.escape(str(user.get("email") or ""))\n    safe_profile_role = html.escape(str(user.get("role") or "user").upper())\n    st.markdown(\n        f'''<div class="profile-summary-card">\n            <div class="profile-summary-avatar">{safe_profile_name[:1].upper()}</div>\n            <div class="profile-summary-main">\n                <div class="profile-summary-name">{safe_profile_name}</div>\n                <div class="profile-summary-email">{safe_profile_email}</div>\n            </div>\n            <div class="profile-summary-role">{safe_profile_role}</div>\n        </div>''',\n        unsafe_allow_html=True,\n    )\n\n    section_title("Alterar senha", "SEGURANÇA DA CONTA")\n''',
'''def page_admin_users(db, user):\n    st.title("Administração de usuários")\n''':
'''def page_admin_users(db, user):\n    render_page_header(\n        "Administração de usuários",\n        "Crie acessos, controle perfis e gerencie credenciais dos usuários autorizados no sistema.",\n        "ADMINISTRAÇÃO",\n        "◇",\n        "blue",\n    )\n    section_title("Usuários do sistema", "ACESSOS & PERMISSÕES")\n''',
}
for old, new in headers.items():
    if old in app:
        app = app.replace(old, new, 1)

# 5) Seções internas mais consistentes.
app = app.replace('    st.divider()\n    st.subheader("Gerenciar lançamento")\n', '    section_title("Gerenciar lançamento", "BAIXA · EDIÇÃO · EXCLUSÃO")\n', 1)
app = app.replace('    with st.expander("Editar este lançamento"):\n', '    with st.expander("Editar este lançamento", expanded=False):\n', 1)

# 6) Cabeçalho genérico e CSS global para páginas/formulários.
if 'def render_page_header(' not in ui:
    function_anchor = '\n\ndef render_dashboard_hero(today):\n'
    page_header_fn = '''\n\ndef render_page_header(title, subtitle, kicker="MÓDULO", icon="◫", tone="blue"):\n    allowed = {"blue", "green", "red", "amber"}\n    tone = tone if tone in allowed else "blue"\n    st.markdown(\n        f"""\n        <div class="module-page-hero module-page-{tone}">\n            <div class="module-page-icon">{icon}</div>\n            <div class="module-page-copy">\n                <div class="module-page-kicker">{kicker}</div>\n                <div class="module-page-title">{title}</div>\n                <div class="module-page-subtitle">{subtitle}</div>\n            </div>\n            <div class="module-page-status"><span></span> OPERACIONAL</div>\n        </div>\n        """,\n        unsafe_allow_html=True,\n    )\n'''
    if function_anchor not in ui:
        raise SystemExit('Âncora render_dashboard_hero não encontrada.')
    ui = ui.replace(function_anchor, page_header_fn + function_anchor, 1)

css_anchor = '        /* Sidebar / Control Center navigation */\n'
if '/* Global module pages */' not in ui:
    css = r'''        /* Global module pages */
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
            background:
                radial-gradient(420px 145px at 0% 0%, color-mix(in srgb, var(--module-accent) 10%, transparent), transparent 72%),
                linear-gradient(135deg, rgba(15,30,50,.96), rgba(8,17,31,.98));
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
        .module-page-kicker {
            margin-bottom: 3px;
            color: var(--module-accent);
            font-size: .58rem;
            font-weight: 850;
            letter-spacing: .19em;
            text-transform: uppercase;
        }
        .module-page-title {
            color: #f6f9fd;
            font-size: clamp(1.25rem, 2vw, 1.75rem);
            font-weight: 850;
            letter-spacing: -.035em;
            line-height: 1.1;
        }
        .module-page-subtitle {
            max-width: 800px;
            margin-top: 5px;
            color: #8297ad;
            font-size: .78rem;
            line-height: 1.45;
        }
        .module-page-status {
            display: flex;
            align-items: center;
            gap: 6px;
            padding: 7px 9px;
            border: 1px solid rgba(22,224,122,.22);
            border-radius: 8px;
            color: #6ee7a4;
            background: rgba(22,224,122,.035);
            font-size: .54rem;
            font-weight: 850;
            letter-spacing: .09em;
        }
        .module-page-status span {
            width: 6px;
            height: 6px;
            border-radius: 50%;
            background: #16e07a;
            box-shadow: 0 0 8px rgba(22,224,122,.72);
        }

        /* Formulários e controles no mesmo acabamento do dashboard */
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

        [data-testid="stExpander"] {
            border: 1px solid rgba(87,164,220,.14) !important;
            border-radius: 14px !important;
            background: rgba(11,22,38,.58) !important;
            overflow: hidden;
        }

        [data-testid="stAlert"] {
            border-radius: 13px;
            border-width: 1px;
        }

        .profile-summary-card {
            display: flex;
            align-items: center;
            gap: 14px;
            margin: 0 0 18px 0;
            padding: 16px 18px;
            border: 1px solid rgba(87,164,220,.15);
            border-radius: 16px;
            background: linear-gradient(145deg, rgba(15,30,50,.90), rgba(8,18,32,.82));
            box-shadow: 0 12px 32px rgba(1,7,18,.16);
        }
        .profile-summary-avatar {
            display: grid;
            place-items: center;
            width: 46px;
            height: 46px;
            flex: 0 0 46px;
            border-radius: 50%;
            color: #06111f;
            background: linear-gradient(135deg, #00e7ff, #6ee7ff);
            font-size: 1rem;
            font-weight: 900;
            box-shadow: 0 0 22px rgba(0,231,255,.14);
        }
        .profile-summary-main { min-width: 0; flex: 1; }
        .profile-summary-name { color: #f4f8fc; font-size: .92rem; font-weight: 800; }
        .profile-summary-email { color: #8297ad; font-size: .72rem; margin-top: 2px; }
        .profile-summary-role {
            padding: 6px 9px;
            border: 1px solid rgba(0,231,255,.18);
            border-radius: 8px;
            color: #9defff;
            background: rgba(0,231,255,.04);
            font-size: .58rem;
            font-weight: 850;
            letter-spacing: .08em;
        }

        @media (max-width: 720px) {
            .module-page-hero { align-items: flex-start; }
            .module-page-status { display: none; }
            .module-page-icon { width: 45px; height: 45px; flex-basis: 45px; }
        }

'''
    if css_anchor not in ui:
        raise SystemExit('Âncora CSS global não encontrada.')
    ui = ui.replace(css_anchor, css + css_anchor, 1)

app_path.write_text(app, encoding='utf-8')
ui_path.write_text(ui, encoding='utf-8')
print('Identidade visual global aplicada.')
