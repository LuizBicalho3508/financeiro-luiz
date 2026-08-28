from pathlib import Path

app_path = Path("app.py")
ui_path = Path("dashboard_ui.py")
app = app_path.read_text(encoding="utf-8")
ui = ui_path.read_text(encoding="utf-8")


def replace_once(text, old, new, label):
    if old in text:
        return text.replace(old, new, 1)
    if new in text:
        return text
    raise SystemExit(f"Bloco não encontrado: {label}")


# Import do cabeçalho reutilizável.
app = replace_once(
    app,
    "from dashboard_ui import inject_dashboard_theme, render_dashboard_hero, section_title\n",
    "from dashboard_ui import inject_dashboard_theme, render_dashboard_hero, render_page_header, section_title\n",
    "import dashboard_ui",
)

# Tema global em todas as páginas autenticadas.
app = app.replace(
    "def page_dashboard(db, user):\n    inject_dashboard_theme()\n",
    "def page_dashboard(db, user):\n",
    1,
)
app = replace_once(
    app,
    '''    user = current_user(db)
    if not user:
        render_login(db)
        st.stop()

    if user.get("must_change_password"):
''',
    '''    user = current_user(db)
    if not user:
        render_login(db)
        st.stop()

    # Identidade visual global da área autenticada.
    inject_dashboard_theme()

    if user.get("must_change_password"):
''',
    "tema global",
)

# Recalcula o botão ativo imediatamente após navegar.
app = replace_once(
    app,
    '''            if clicked:
                st.session_state["nav"] = page
                selected_page = page
''',
    '''            if clicked:
                st.session_state["nav"] = page
                st.rerun()
''',
    "navegação sidebar",
)

# Cabeçalhos das páginas.
app = replace_once(
    app,
    '''def page_add_expense(db, user):
    st.title("Lançar despesa")
    st.caption("Informe uma compra e o sistema cria automaticamente todas as parcelas.")
''',
    '''def page_add_expense(db, user):
    render_page_header(
        "Lançar despesa",
        "Registre compras, contas e parcelamentos. O sistema distribui automaticamente os vencimentos futuros.",
        "SAÍDAS",
        "−",
        "red",
    )
    section_title("Dados da despesa", "LANÇAMENTO INTELIGENTE")
''',
    "página despesas",
)

app = replace_once(
    app,
    '''def page_add_income(db, user):
    st.title("Lançar receita")
    st.caption("Cadastre uma receita única ou repita automaticamente por vários meses.")
''',
    '''def page_add_income(db, user):
    render_page_header(
        "Lançar receita",
        "Cadastre entradas únicas ou recorrentes e mantenha sua previsão de caixa atualizada automaticamente.",
        "ENTRADAS",
        "+",
        "green",
    )
    section_title("Dados da receita", "RECEBIMENTOS")
''',
    "página receitas",
)

app = replace_once(
    app,
    '''def page_transactions(db, user):
    st.title("Movimentações")
''',
    '''def page_transactions(db, user):
    render_page_header(
        "Movimentações",
        "Consulte, filtre, exporte e gerencie todo o histórico financeiro em um único painel operacional.",
        "HISTÓRICO",
        "⇄",
        "blue",
    )
    section_title("Filtros e período", "CONSULTA")
''',
    "página movimentações",
)

app = replace_once(
    app,
    '''def page_budgets(db, user):
    st.title("Orçamentos")
    st.caption("Defina limites mensais por categoria e acompanhe o consumo no dashboard.")
''',
    '''def page_budgets(db, user):
    render_page_header(
        "Orçamentos",
        "Defina limites mensais por categoria e acompanhe quanto do orçamento já foi comprometido.",
        "PLANEJAMENTO",
        "◎",
        "amber",
    )
    section_title("Configurar orçamento", "LIMITES MENSAIS")
''',
    "página orçamentos",
)

app = replace_once(
    app,
    '''def page_my_account(db, user):
    st.title("Minha conta")
    st.write(f"**Nome:** {user['name']}")
    st.write(f"**E-mail:** {user['email']}")
    st.write(f"**Perfil:** {user['role']}")

    st.subheader("Alterar senha")
''',
    '''def page_my_account(db, user):
    render_page_header(
        "Minha conta",
        "Gerencie seus dados de acesso e mantenha as credenciais da sua conta protegidas.",
        "PERFIL & SEGURANÇA",
        "○",
        "blue",
    )
    safe_profile_name = html.escape(str(user.get("name") or "Usuário"))
    safe_profile_email = html.escape(str(user.get("email") or ""))
    safe_profile_role = html.escape(str(user.get("role") or "user").upper())
    st.markdown(
        f"""<div class="profile-summary-card">
            <div class="profile-summary-avatar">{safe_profile_name[:1].upper()}</div>
            <div class="profile-summary-main">
                <div class="profile-summary-name">{safe_profile_name}</div>
                <div class="profile-summary-email">{safe_profile_email}</div>
            </div>
            <div class="profile-summary-role">{safe_profile_role}</div>
        </div>""",
        unsafe_allow_html=True,
    )

    section_title("Alterar senha", "SEGURANÇA DA CONTA")
''',
    "página minha conta",
)

app = replace_once(
    app,
    '''def page_admin_users(db, user):
    st.title("Administração de usuários")
''',
    '''def page_admin_users(db, user):
    render_page_header(
        "Administração de usuários",
        "Crie acessos, controle perfis e gerencie credenciais dos usuários autorizados no sistema.",
        "ADMINISTRAÇÃO",
        "◇",
        "blue",
    )
    section_title("Usuários do sistema", "ACESSOS & PERMISSÕES")
''',
    "página usuários",
)

app = app.replace(
    '    st.divider()\n    st.subheader("Gerenciar lançamento")\n',
    '    section_title("Gerenciar lançamento", "BAIXA · EDIÇÃO · EXCLUSÃO")\n',
    1,
)
app = app.replace(
    '    with st.expander("Editar este lançamento"):\n',
    '    with st.expander("Editar este lançamento", expanded=False):\n',
    1,
)

# Função de cabeçalho reutilizável.
if "def render_page_header(" not in ui:
    anchor = "\n\ndef render_dashboard_hero(today):\n"
    fn = '''

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
'''
    if anchor not in ui:
        raise SystemExit("Âncora render_dashboard_hero não encontrada")
    ui = ui.replace(anchor, fn + anchor, 1)

# CSS global das páginas e formulários.
if "/* Global module pages */" not in ui:
    anchor = '        /* Sidebar / Control Center navigation */\n'
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

'''
    if anchor not in ui:
        raise SystemExit("Âncora CSS global não encontrada")
    ui = ui.replace(anchor, css + anchor, 1)

app_path.write_text(app, encoding="utf-8")
ui_path.write_text(ui, encoding="utf-8")
print("Identidade visual global aplicada com sucesso.")
