import base64
import calendar
import hashlib
import hmac
import html
import os
import secrets
import uuid
from datetime import date, datetime, timedelta
from decimal import Decimal, ROUND_HALF_UP

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st
from bson import ObjectId
from dateutil.relativedelta import relativedelta
from pymongo import ASCENDING, DESCENDING, MongoClient
from pymongo.errors import DuplicateKeyError
from charts import render_balance_chart, render_expense_donut, render_flow_chart
from dashboard_ui import inject_dashboard_theme, render_dashboard_hero, render_page_header, section_title


APP_NAME = "Meu Financeiro"
ADMIN_EMAIL = "felipe123pvh@gmail.com"
ADMIN_INITIAL_SALT = "IPEm1xjsLMt99DPRyi+Qjw=="
ADMIN_INITIAL_HASH = "WgBO9JU6Q5QE9U1BOrtMkRtjsepUa2Zma2vOWqrIw6M="
PBKDF2_ITERATIONS = 310_000

EXPENSE_CATEGORIES = [
    "Alimentação",
    "Moradia",
    "Transporte",
    "Saúde",
    "Educação",
    "Lazer",
    "Assinaturas",
    "Compras",
    "Impostos",
    "Dívidas",
    "Família",
    "Pets",
    "Viagens",
    "Outros",
]

INCOME_CATEGORIES = [
    "Salário",
    "Pró-labore",
    "Freelance",
    "Comissão",
    "Investimentos",
    "Aluguel",
    "Reembolso",
    "Venda",
    "Outros",
]

PAYMENT_METHODS = [
    "PIX",
    "Cartão de crédito",
    "Cartão de débito",
    "Boleto",
    "Débito automático",
    "Dinheiro",
    "Transferência",
    "Outro",
]

ACCOUNTS = ["Conta principal", "Carteira", "Cartão principal", "Outra"]

st.set_page_config(
    page_title=APP_NAME,
    page_icon="💰",
    layout="wide",
    initial_sidebar_state="expanded",
)


# -----------------------------------------------------------------------------
# Visual
# -----------------------------------------------------------------------------
def inject_css():
    st.markdown(
        """
        <style>
        .block-container { padding-top: 1.4rem; padding-bottom: 3rem; }
        [data-testid="stMetric"] {
            border: 1px solid rgba(128,128,128,.18);
            border-radius: 16px;
            padding: 14px 16px;
            background: linear-gradient(135deg, rgba(26, 188, 156, .08), rgba(52, 152, 219, .04));
        }
        .finance-card {
            border: 1px solid rgba(128,128,128,.18);
            border-radius: 18px;
            padding: 18px;
            margin-bottom: 12px;
        }
        .muted { opacity: .72; font-size: .92rem; }
        .login-wrap { max-width: 520px; margin: 5vh auto 0 auto; }
        .brand-title { font-size: 2rem; font-weight: 800; margin-bottom: .2rem; }
        .brand-subtitle { opacity: .72; margin-bottom: 1.4rem; }

        /* Dashboard / KPIs */
        .dashboard-context {
            display: flex;
            align-items: center;
            gap: .55rem;
            margin: -.3rem 0 1rem 0;
            color: rgba(148, 163, 184, .95);
            font-size: .95rem;
            font-weight: 600;
        }
        .dashboard-context::before {
            content: "";
            width: 7px;
            height: 7px;
            border-radius: 50%;
            background: #38bdf8;
            box-shadow: 0 0 16px rgba(56, 189, 248, .65);
        }
        .kpi-card {
            position: relative;
            overflow: hidden;
            min-height: 142px;
            padding: 17px 17px 15px 17px;
            border-radius: 19px;
            border: 1px solid rgba(148, 163, 184, .16);
            background: linear-gradient(145deg, rgba(15, 23, 42, .76), rgba(30, 41, 59, .48));
            box-shadow: 0 10px 30px rgba(2, 6, 23, .16);
            transition: transform .16s ease, border-color .16s ease, box-shadow .16s ease;
        }
        .kpi-card:hover {
            transform: translateY(-2px);
            border-color: rgba(148, 163, 184, .30);
            box-shadow: 0 14px 34px rgba(2, 6, 23, .22);
        }
        .kpi-card::after {
            content: "";
            position: absolute;
            width: 110px;
            height: 110px;
            right: -48px;
            top: -52px;
            border-radius: 999px;
            opacity: .16;
            filter: blur(3px);
            background: var(--kpi-color, #38bdf8);
        }
        .kpi-top {
            display: flex;
            justify-content: space-between;
            align-items: center;
            gap: 8px;
            margin-bottom: 13px;
        }
        .kpi-label {
            color: rgba(203, 213, 225, .86);
            font-size: .78rem;
            font-weight: 750;
            letter-spacing: .045em;
            text-transform: uppercase;
        }
        .kpi-icon {
            display: inline-flex;
            align-items: center;
            justify-content: center;
            width: 31px;
            height: 31px;
            border-radius: 10px;
            color: var(--kpi-color, #38bdf8);
            background: color-mix(in srgb, var(--kpi-color, #38bdf8) 14%, transparent);
            font-size: 1rem;
            font-weight: 800;
        }
        .kpi-value {
            color: var(--kpi-color, #e2e8f0);
            font-size: clamp(1.32rem, 1.65vw, 1.78rem);
            line-height: 1.12;
            font-weight: 850;
            letter-spacing: -.035em;
            margin-bottom: 7px;
            white-space: nowrap;
        }
        .kpi-caption {
            color: rgba(148, 163, 184, .88);
            font-size: .77rem;
            line-height: 1.25;
        }
        .kpi-green { --kpi-color: #22c55e; }
        .kpi-red { --kpi-color: #ef4444; }
        .kpi-blue { --kpi-color: #38bdf8; }
        .kpi-amber { --kpi-color: #f59e0b; }
        .kpi-neutral { --kpi-color: #cbd5e1; }

        div[data-testid="stPlotlyChart"] {
            border: 1px solid rgba(148, 163, 184, .10);
            border-radius: 17px;
            overflow: hidden;
            background: rgba(15, 23, 42, .18);
        }
        div[data-testid="stDataFrame"] {
            border-radius: 14px;
            overflow: hidden;
        }
        @media (max-width: 900px) {
            .kpi-card { min-height: 128px; }
            .kpi-value { white-space: normal; }
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


inject_css()


def render_kpi_card(container, title, value, tone="blue", icon="•", caption=""):
    allowed = {"green", "red", "blue", "amber", "neutral"}
    tone = tone if tone in allowed else "blue"
    container.markdown(
        f"""
        <div class="kpi-card kpi-{tone}">
            <div class="kpi-top">
                <div class="kpi-label">{title}</div>
                <div class="kpi-icon">{icon}</div>
            </div>
            <div class="kpi-value">{value}</div>
            <div class="kpi-caption">{caption}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


# -----------------------------------------------------------------------------
# Utilidades
# -----------------------------------------------------------------------------
def now_utc_naive():
    return datetime.utcnow()


def normalize_email(value):
    return (value or "").strip().lower()


def money_to_cents(value):
    amount = Decimal(str(value)).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
    return int(amount * 100)


def cents_to_money(cents):
    return float(Decimal(int(cents or 0)) / Decimal(100))


def brl_from_cents(cents):
    value = cents_to_money(cents)
    txt = f"{value:,.2f}"
    return "R$ " + txt.replace(",", "X").replace(".", ",").replace("X", ".")


def brl(value):
    return brl_from_cents(money_to_cents(value))


def month_key(value):
    return value.strftime("%Y-%m")


def safe_due_date(year, month, day):
    last_day = calendar.monthrange(year, month)[1]
    return datetime(year, month, min(int(day), last_day))


def split_total_cents(total_cents, count):
    count = max(1, int(count))
    base = total_cents // count
    remainder = total_cents % count
    return [base + (1 if i < remainder else 0) for i in range(count)]


def password_hash(password, salt_b64=None):
    if salt_b64:
        salt = base64.b64decode(salt_b64.encode("utf-8"))
    else:
        salt = secrets.token_bytes(16)
        salt_b64 = base64.b64encode(salt).decode("utf-8")

    derived = hashlib.pbkdf2_hmac(
        "sha256",
        password.encode("utf-8"),
        salt,
        PBKDF2_ITERATIONS,
    )
    return salt_b64, base64.b64encode(derived).decode("utf-8")


def password_verify(password, salt_b64, expected_hash_b64):
    _, candidate = password_hash(password, salt_b64)
    return hmac.compare_digest(candidate, expected_hash_b64)


def get_category(selected, custom):
    if selected == "Outra / personalizada":
        custom = (custom or "").strip()
        return custom if custom else "Outros"
    return selected


def status_label(kind, status):
    mapping = {
        "pending": "Pendente",
        "paid": "Pago",
        "received": "Recebido",
        "canceled": "Cancelado",
    }
    return mapping.get(status, status)


def kind_label(kind):
    return "Despesa" if kind == "expense" else "Receita"


def mongo_date(value):
    if isinstance(value, datetime):
        return value
    return datetime.combine(value, datetime.min.time())


# -----------------------------------------------------------------------------
# Banco
# -----------------------------------------------------------------------------
def mongo_settings():
    uri = os.getenv("MONGODB_URI")
    database = os.getenv("MONGODB_DB", "financeiro_luiz")

    try:
        if "mongo" in st.secrets:
            uri = st.secrets["mongo"].get("uri", uri)
            database = st.secrets["mongo"].get("database", database)
    except Exception:
        pass

    return uri, database


@st.cache_resource(show_spinner=False)
def get_database():
    uri, database_name = mongo_settings()
    if not uri:
        raise RuntimeError("MONGODB_URI_NOT_CONFIGURED")

    client = MongoClient(
        uri,
        serverSelectionTimeoutMS=7000,
        connectTimeoutMS=7000,
        socketTimeoutMS=12000,
        appname="financeiro-luiz-streamlit",
    )
    client.admin.command("ping")
    return client[database_name]


def ensure_database(db):
    db.users.create_index([("email", ASCENDING)], unique=True, name="uq_users_email")
    db.transactions.create_index(
        [("owner_user_id", ASCENDING), ("due_date", DESCENDING)],
        name="idx_transactions_owner_due",
    )
    db.transactions.create_index(
        [("owner_user_id", ASCENDING), ("group_id", ASCENDING)],
        name="idx_transactions_owner_group",
    )
    db.budgets.create_index(
        [("owner_user_id", ASCENDING), ("month", ASCENDING), ("category", ASCENDING)],
        unique=True,
        name="uq_budget_owner_month_category",
    )

    if not db.users.find_one({"email": ADMIN_EMAIL}):
        db.users.insert_one(
            {
                "email": ADMIN_EMAIL,
                "name": "Felipe",
                "role": "admin",
                "active": True,
                "password_salt": ADMIN_INITIAL_SALT,
                "password_hash": ADMIN_INITIAL_HASH,
                "must_change_password": True,
                "created_at": now_utc_naive(),
                "updated_at": now_utc_naive(),
            }
        )


# -----------------------------------------------------------------------------
# Autenticação
# -----------------------------------------------------------------------------
def public_user(user):
    return {
        "id": str(user["_id"]),
        "email": user["email"],
        "name": user.get("name") or user["email"],
        "role": user.get("role", "user"),
        "active": bool(user.get("active", True)),
        "must_change_password": bool(user.get("must_change_password", False)),
    }


def login_user(db, email, password):
    user = db.users.find_one({"email": normalize_email(email)})
    if not user or not user.get("active", True):
        return None
    if not password_verify(password, user["password_salt"], user["password_hash"]):
        return None
    return public_user(user)


def current_user(db):
    session_id = st.session_state.get("user_id")
    if not session_id:
        return None
    try:
        user = db.users.find_one({"_id": ObjectId(session_id), "active": True})
    except Exception:
        user = None
    if not user:
        st.session_state.pop("user_id", None)
        return None
    return public_user(user)


def do_logout():
    for key in ["user_id", "nav"]:
        st.session_state.pop(key, None)
    st.rerun()


def render_login(db):
    st.markdown('<div class="login-wrap">', unsafe_allow_html=True)
    st.markdown('<div class="brand-title">💰 Meu Financeiro</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="brand-subtitle">Controle simples, rápido e visual das suas finanças pessoais.</div>',
        unsafe_allow_html=True,
    )

    with st.form("login_form", clear_on_submit=False):
        email = st.text_input("E-mail", placeholder="voce@email.com")
        password = st.text_input("Senha", type="password")
        submitted = st.form_submit_button("Entrar", type="primary", width="stretch")

    if submitted:
        user = login_user(db, email, password)
        if user:
            st.session_state["user_id"] = user["id"]
            st.rerun()
        else:
            st.error("E-mail ou senha inválidos.")

    st.caption("As credenciais são validadas no MongoDB e a senha não é armazenada em texto puro.")
    st.markdown("</div>", unsafe_allow_html=True)


def render_forced_password_change(db, user):
    st.title("Defina sua nova senha")
    st.info("Por segurança, a senha inicial precisa ser trocada antes do primeiro uso.")

    with st.form("forced_password_change"):
        new_password = st.text_input("Nova senha", type="password")
        confirm = st.text_input("Confirmar nova senha", type="password")
        submitted = st.form_submit_button("Salvar nova senha", type="primary")

    if submitted:
        if len(new_password) < 8:
            st.error("Use uma senha com pelo menos 8 caracteres.")
            return
        if new_password != confirm:
            st.error("As senhas não coincidem.")
            return

        salt, pwd_hash = password_hash(new_password)
        db.users.update_one(
            {"_id": ObjectId(user["id"])},
            {
                "$set": {
                    "password_salt": salt,
                    "password_hash": pwd_hash,
                    "must_change_password": False,
                    "updated_at": now_utc_naive(),
                }
            },
        )
        st.success("Senha alterada com sucesso.")
        st.rerun()


# -----------------------------------------------------------------------------
# Dados financeiros
# -----------------------------------------------------------------------------
def owner_filter(user):
    return {"owner_user_id": user["id"]}


def transaction_rows(db, user, start=None, end=None):
    query = owner_filter(user)
    if start or end:
        due_filter = {}
        if start:
            due_filter["$gte"] = mongo_date(start)
        if end:
            due_filter["$lt"] = mongo_date(end) + timedelta(days=1)
        query["due_date"] = due_filter
    return list(db.transactions.find(query).sort("due_date", ASCENDING))


def to_dataframe(rows):
    if not rows:
        return pd.DataFrame(
            columns=[
                "id",
                "kind",
                "description",
                "category",
                "amount_cents",
                "amount",
                "due_date",
                "status",
                "payment_method",
                "account",
                "installment_no",
                "installment_count",
                "group_id",
                "notes",
            ]
        )

    data = []
    for row in rows:
        data.append(
            {
                "id": str(row["_id"]),
                "kind": row.get("kind", "expense"),
                "description": row.get("description", ""),
                "category": row.get("category", "Outros"),
                "amount_cents": int(row.get("amount_cents", 0)),
                "amount": cents_to_money(row.get("amount_cents", 0)),
                "due_date": pd.to_datetime(row.get("due_date")),
                "status": row.get("status", "pending"),
                "payment_method": row.get("payment_method", ""),
                "account": row.get("account", ""),
                "installment_no": int(row.get("installment_no", 1)),
                "installment_count": int(row.get("installment_count", 1)),
                "group_id": row.get("group_id", ""),
                "notes": row.get("notes", ""),
            }
        )
    return pd.DataFrame(data)


def insert_expense_installments(
    db,
    user,
    description,
    category,
    informed_value,
    value_mode,
    installments,
    first_month,
    due_day,
    payment_method,
    account,
    initially_paid,
    notes,
):
    group_id = str(uuid.uuid4())
    installments = max(1, int(installments))
    informed_cents = money_to_cents(informed_value)

    if value_mode == "Valor total da compra":
        installment_values = split_total_cents(informed_cents, installments)
    else:
        installment_values = [informed_cents] * installments

    documents = []
    base = date(first_month.year, first_month.month, 1)
    for index in range(installments):
        month = base + relativedelta(months=index)
        due = safe_due_date(month.year, month.month, due_day)
        documents.append(
            {
                "owner_user_id": user["id"],
                "kind": "expense",
                "description": description.strip(),
                "category": category,
                "amount_cents": installment_values[index],
                "due_date": due,
                "competence": month_key(due),
                "status": "paid" if initially_paid else "pending",
                "payment_method": payment_method,
                "account": account,
                "installment_no": index + 1,
                "installment_count": installments,
                "group_id": group_id,
                "notes": notes.strip(),
                "paid_at": now_utc_naive() if initially_paid else None,
                "created_at": now_utc_naive(),
                "updated_at": now_utc_naive(),
            }
        )

    db.transactions.insert_many(documents)
    return documents


def insert_income_recurrences(
    db,
    user,
    description,
    category,
    value,
    repetitions,
    first_month,
    due_day,
    account,
    initially_received,
    notes,
):
    group_id = str(uuid.uuid4())
    value_cents = money_to_cents(value)
    repetitions = max(1, int(repetitions))
    base = date(first_month.year, first_month.month, 1)
    documents = []

    for index in range(repetitions):
        month = base + relativedelta(months=index)
        due = safe_due_date(month.year, month.month, due_day)
        documents.append(
            {
                "owner_user_id": user["id"],
                "kind": "income",
                "description": description.strip(),
                "category": category,
                "amount_cents": value_cents,
                "due_date": due,
                "competence": month_key(due),
                "status": "received" if initially_received else "pending",
                "payment_method": "Crédito/recebimento",
                "account": account,
                "installment_no": index + 1,
                "installment_count": repetitions,
                "group_id": group_id,
                "notes": notes.strip(),
                "paid_at": now_utc_naive() if initially_received else None,
                "created_at": now_utc_naive(),
                "updated_at": now_utc_naive(),
            }
        )

    db.transactions.insert_many(documents)
    return documents


# -----------------------------------------------------------------------------
# Páginas
# -----------------------------------------------------------------------------
def page_dashboard(db, user):
    rows = transaction_rows(db, user)
    df = to_dataframe(rows)

    today = date.today()
    render_dashboard_hero(today)
    years = sorted(set(df["due_date"].dt.year.tolist())) if not df.empty else []
    if today.year not in years:
        years.append(today.year)
    years = sorted(years, reverse=True)

    c1, c2 = st.columns([1, 1])
    selected_year = c1.selectbox("Ano", years, index=years.index(today.year) if today.year in years else 0)
    month_names = [
        "Janeiro", "Fevereiro", "Março", "Abril", "Maio", "Junho",
        "Julho", "Agosto", "Setembro", "Outubro", "Novembro", "Dezembro"
    ]
    selected_month = c2.selectbox("Mês", range(1, 13), index=today.month - 1, format_func=lambda x: month_names[x - 1])

    if df.empty:
        st.info("Ainda não há movimentações. Use **Lançar despesa** ou **Lançar receita** para começar.")
        return

    active_df = df[df["status"] != "canceled"].copy()
    current = active_df[
        (active_df["due_date"].dt.year == selected_year)
        & (active_df["due_date"].dt.month == selected_month)
    ].copy()

    income = current.loc[current["kind"] == "income", "amount_cents"].sum()
    expense = current.loc[current["kind"] == "expense", "amount_cents"].sum()
    result = int(income - expense)
    pending_expense = current.loc[
        (current["kind"] == "expense") & (current["status"] == "pending"), "amount_cents"
    ].sum()
    pending_income = current.loc[
        (current["kind"] == "income") & (current["status"] == "pending"), "amount_cents"
    ].sum()

    # Saldo transportado: soma todo o histórico anterior ao mês selecionado.
    # Mantemos "resultado do mês" separado para não confundir desempenho mensal
    # com o saldo acumulado disponível/projetado.
    period_start = pd.Timestamp(date(selected_year, selected_month, 1))
    previous = active_df[active_df["due_date"] < period_start]
    previous_income = int(previous.loc[previous["kind"] == "income", "amount_cents"].sum())
    previous_expense = int(previous.loc[previous["kind"] == "expense", "amount_cents"].sum())
    previous_balance = previous_income - previous_expense
    accumulated_balance = previous_balance + result

    st.markdown(
        f'<div class="dashboard-context">Resumo de {month_names[selected_month - 1]} de {selected_year}</div>',
        unsafe_allow_html=True,
    )

    result_tone = "green" if result > 0 else "red" if result < 0 else "neutral"
    result_caption = "superávit previsto" if result > 0 else "déficit previsto" if result < 0 else "receitas e despesas equilibradas"
    balance_tone = "green" if accumulated_balance > 0 else "red" if accumulated_balance < 0 else "neutral"
    balance_title = "Saldo atual" if selected_year == today.year and selected_month == today.month else "Saldo acumulado"
    balance_caption = f"inclui {brl_from_cents(previous_balance)} trazidos de meses anteriores"

    k1, k2, k3, k4, k5, k6 = st.columns([1.45, 1.18, 1, 1, 1, 1], gap="small")
    render_kpi_card(k1, balance_title, brl_from_cents(accumulated_balance), balance_tone, "◉", balance_caption)
    render_kpi_card(k2, "Resultado do mês", brl_from_cents(result), result_tone, "◎", result_caption)
    render_kpi_card(k3, "Receitas", brl_from_cents(income), "green", "↑", "total previsto no mês")
    render_kpi_card(k4, "Despesas", brl_from_cents(expense), "red", "↓", "total comprometido")
    render_kpi_card(k5, "A pagar", brl_from_cents(pending_expense), "red", "!", "pendências de saída")
    render_kpi_card(k6, "A receber", brl_from_cents(pending_income), "green", "+", "pendências de entrada")

    chart_left, chart_right = st.columns([1.65, 1], gap="medium")

    with chart_left:
        section_title("Fluxo financeiro — 12 meses", "RECEITAS · DESPESAS · SALDO")
        end_period = pd.Period(f"{selected_year}-{selected_month:02d}", freq="M")
        periods = pd.period_range(end=end_period, periods=12, freq="M")
        base = pd.DataFrame({"period": periods.astype(str)})
        tmp = active_df.copy()
        tmp["period"] = tmp["due_date"].dt.to_period("M").astype(str)
        grouped = (
            tmp.groupby(["period", "kind"], as_index=False)["amount"].sum()
            .pivot(index="period", columns="kind", values="amount")
            .fillna(0)
            .reset_index()
        )
        monthly = base.merge(grouped, how="left", on="period").fillna(0)
        if "income" not in monthly:
            monthly["income"] = 0.0
        if "expense" not in monthly:
            monthly["expense"] = 0.0
        monthly["balance"] = monthly["income"] - monthly["expense"]

        render_flow_chart(monthly, height=390)

    with chart_right:
        section_title("Despesas por categoria", "COMPOSIÇÃO DO MÊS")
        exp_cat = current[(current["kind"] == "expense") & (current["status"] != "canceled")]
        if exp_cat.empty:
            st.info("Sem despesas no período selecionado.")
        else:
            cat = exp_cat.groupby("category", as_index=False)["amount"].sum().sort_values("amount", ascending=False)
            render_expense_donut(cat, total=float(cat["amount"].sum()), height=390)

    bottom_left, bottom_right = st.columns([1.35, 1], gap="medium")

    with bottom_left:
        section_title("Saldo acumulado", "EVOLUÇÃO DIÁRIA · INCLUI SALDO ANTERIOR")
        if current.empty:
            st.info("Sem dados para o período.")
        else:
            daily = current.sort_values("due_date").copy()
            daily["signed"] = daily.apply(
                lambda r: r["amount"] if r["kind"] == "income" else -r["amount"], axis=1
            )
            daily["date"] = daily["due_date"].dt.normalize()
            daily = daily.groupby("date", as_index=False, sort=True)["signed"].sum()
            daily["acumulado"] = cents_to_money(previous_balance) + daily["signed"].cumsum()
            render_balance_chart(daily, height=340)

    with bottom_right:
        section_title("Próximos vencimentos", "JANELA DE 30 DIAS")
        start_dt = pd.Timestamp(today)
        end_dt = pd.Timestamp(today + timedelta(days=30))
        upcoming = active_df[
            (active_df["status"] == "pending")
            & (active_df["due_date"] >= start_dt)
            & (active_df["due_date"] <= end_dt)
        ].sort_values("due_date").head(10)
        if upcoming.empty:
            st.success("Nenhum vencimento pendente nos próximos 30 dias.")
        else:
            view = upcoming[["due_date", "kind", "description", "amount"]].copy()
            view["Data"] = view["due_date"].dt.strftime("%d/%m/%Y")
            view["Tipo"] = view["kind"].map({"expense": "Despesa", "income": "Receita"})
            view["Valor"] = view["amount"].map(brl)
            upcoming_view = view[["Valor", "Tipo", "description", "Data"]].rename(
                columns={"description": "Descrição"}
            )

            def style_upcoming_type(value):
                if value == "Despesa":
                    return (
                        "background-color: #35141d; "
                        "color: #ff7083; "
                        "font-weight: 800; "
                        "border-left: 3px solid #ff4d67;"
                    )
                if value == "Receita":
                    return (
                        "background-color: #0d3021; "
                        "color: #52f59c; "
                        "font-weight: 800; "
                        "border-left: 3px solid #16e07a;"
                    )
                return ""

            styled_upcoming = upcoming_view.style.map(style_upcoming_type, subset=["Tipo"])
            st.dataframe(
                styled_upcoming,
                hide_index=True,
                width="stretch",
                column_config={
                    "Valor": st.column_config.TextColumn("Valor", width="medium"),
                    "Tipo": st.column_config.TextColumn("Tipo", width="small"),
                    "Descrição": st.column_config.TextColumn("Descrição", width="large"),
                    "Data": st.column_config.TextColumn("Data", width="small"),
                },
            )

    budgets = list(db.budgets.find({"owner_user_id": user["id"], "month": f"{selected_year}-{selected_month:02d}"}))
    if budgets:
        section_title("Orçamento do mês", "LIMITE POR CATEGORIA")
        budget_rows = []
        for item in budgets:
            spent = int(
                current.loc[
                    (current["kind"] == "expense")
                    & (current["category"] == item["category"])
                    & (current["status"] != "canceled"),
                    "amount_cents",
                ].sum()
            )
            limit_cents = int(item.get("limit_cents", 0))
            pct = (spent / limit_cents * 100) if limit_cents else 0
            budget_rows.append((item["category"], spent, limit_cents, pct))
        for category, spent, limit_cents, pct in sorted(budget_rows):
            st.write(f"**{category}** — {brl_from_cents(spent)} de {brl_from_cents(limit_cents)} ({pct:.0f}%)")
            st.progress(min(max(pct / 100, 0.0), 1.0))


def page_add_expense(db, user):
    render_page_header(
        "Lançar despesa",
        "Registre compras, contas e parcelamentos. O sistema distribui automaticamente os vencimentos futuros.",
        "SAÍDAS",
        "−",
        "red",
    )
    section_title("Dados da despesa", "LANÇAMENTO INTELIGENTE")

    with st.form("expense_form", clear_on_submit=True):
        c1, c2 = st.columns([2, 1])
        description = c1.text_input("Descrição *", placeholder="Ex.: Notebook, aluguel, supermercado")
        value = c2.number_input("Valor (R$) *", min_value=0.01, value=100.00, step=10.00, format="%.2f")

        c3, c4, c5 = st.columns(3)
        value_mode = c3.selectbox("O valor informado representa", ["Valor total da compra", "Valor de cada parcela"])
        installments = c4.number_input("Quantidade de parcelas", min_value=1, max_value=120, value=1, step=1)
        due_day = c5.number_input("Dia do vencimento", min_value=1, max_value=31, value=min(date.today().day, 28), step=1)

        c6, c7, c8 = st.columns(3)
        first_month = c6.date_input("Mês do primeiro vencimento", value=date.today())
        category_choice = c7.selectbox("Categoria", EXPENSE_CATEGORIES + ["Outra / personalizada"])
        payment_method = c8.selectbox("Forma de pagamento", PAYMENT_METHODS)

        custom_category = ""
        if category_choice == "Outra / personalizada":
            custom_category = st.text_input("Categoria personalizada")

        c9, c10 = st.columns(2)
        account = c9.selectbox("Conta / cartão", ACCOUNTS)
        initially_paid = c10.checkbox("Já está pago", value=False)

        notes = st.text_area("Observações", placeholder="Opcional")

        if value_mode == "Valor total da compra":
            preview_values = split_total_cents(money_to_cents(value), int(installments))
            st.caption(
                f"Prévia: {int(installments)} parcela(s). Primeira: {brl_from_cents(preview_values[0])} | "
                f"Total: {brl_from_cents(sum(preview_values))}"
            )
        else:
            total = money_to_cents(value) * int(installments)
            st.caption(f"Prévia: {int(installments)} × {brl(value)} = {brl_from_cents(total)}")

        submitted = st.form_submit_button("Salvar despesa", type="primary", width="stretch")

    if submitted:
        if not description.strip():
            st.error("Informe uma descrição.")
            return

        category = get_category(category_choice, custom_category)
        docs = insert_expense_installments(
            db=db,
            user=user,
            description=description,
            category=category,
            informed_value=value,
            value_mode=value_mode,
            installments=installments,
            first_month=first_month,
            due_day=due_day,
            payment_method=payment_method,
            account=account,
            initially_paid=initially_paid,
            notes=notes,
        )
        total_cents = sum(doc["amount_cents"] for doc in docs)
        st.success(f"Despesa salva: {len(docs)} lançamento(s), total de {brl_from_cents(total_cents)}.")


def page_add_income(db, user):
    render_page_header(
        "Lançar receita",
        "Cadastre entradas únicas ou recorrentes e mantenha sua previsão de caixa atualizada automaticamente.",
        "ENTRADAS",
        "+",
        "green",
    )
    section_title("Dados da receita", "RECEBIMENTOS")

    with st.form("income_form", clear_on_submit=True):
        c1, c2 = st.columns([2, 1])
        description = c1.text_input("Descrição *", placeholder="Ex.: Salário, comissão, aluguel")
        value = c2.number_input("Valor por recebimento (R$) *", min_value=0.01, value=1000.00, step=100.00, format="%.2f")

        c3, c4, c5 = st.columns(3)
        repetitions = c3.number_input("Repetir por quantos meses", min_value=1, max_value=120, value=1, step=1)
        due_day = c4.number_input("Dia previsto", min_value=1, max_value=31, value=min(date.today().day, 28), step=1)
        first_month = c5.date_input("Primeiro mês", value=date.today())

        c6, c7, c8 = st.columns(3)
        category_choice = c6.selectbox("Categoria", INCOME_CATEGORIES + ["Outra / personalizada"])
        account = c7.selectbox("Conta de entrada", ACCOUNTS)
        initially_received = c8.checkbox("Já recebido", value=False)

        custom_category = ""
        if category_choice == "Outra / personalizada":
            custom_category = st.text_input("Categoria personalizada")

        notes = st.text_area("Observações", placeholder="Opcional")
        total = money_to_cents(value) * int(repetitions)
        st.caption(f"Prévia: {int(repetitions)} recebimento(s) × {brl(value)} = {brl_from_cents(total)}")
        submitted = st.form_submit_button("Salvar receita", type="primary", width="stretch")

    if submitted:
        if not description.strip():
            st.error("Informe uma descrição.")
            return
        category = get_category(category_choice, custom_category)
        docs = insert_income_recurrences(
            db=db,
            user=user,
            description=description,
            category=category,
            value=value,
            repetitions=repetitions,
            first_month=first_month,
            due_day=due_day,
            account=account,
            initially_received=initially_received,
            notes=notes,
        )
        st.success(f"Receita salva: {len(docs)} lançamento(s), total de {brl_from_cents(total)}.")


def page_transactions(db, user):
    render_page_header(
        "Movimentações",
        "Consulte, filtre, exporte e gerencie todo o histórico financeiro em um único painel operacional.",
        "HISTÓRICO",
        "⇄",
        "blue",
    )
    section_title("Filtros e período", "CONSULTA")

    c1, c2 = st.columns(2)
    start = c1.date_input("De", value=date.today() - timedelta(days=180), key="mov_start")
    end = c2.date_input("Até", value=date.today() + timedelta(days=365), key="mov_end")

    rows = transaction_rows(db, user, start, end)
    df = to_dataframe(rows)
    if df.empty:
        st.info("Nenhuma movimentação encontrada no período.")
        return

    f1, f2, f3 = st.columns(3)
    type_filter = f1.selectbox("Tipo", ["Todos", "Despesas", "Receitas"])
    statuses = f2.multiselect("Status", ["pending", "paid", "received", "canceled"], default=["pending", "paid", "received"], format_func=lambda s: status_label("expense", s))
    categories = f3.multiselect("Categorias", sorted(df["category"].dropna().unique().tolist()))

    filtered = df.copy()
    if type_filter == "Despesas":
        filtered = filtered[filtered["kind"] == "expense"]
    elif type_filter == "Receitas":
        filtered = filtered[filtered["kind"] == "income"]
    if statuses:
        filtered = filtered[filtered["status"].isin(statuses)]
    if categories:
        filtered = filtered[filtered["category"].isin(categories)]

    view = filtered.copy()
    view["Data"] = view["due_date"].dt.strftime("%d/%m/%Y")
    view["Tipo"] = view["kind"].map({"expense": "Despesa", "income": "Receita"})
    view["Status"] = view.apply(lambda r: status_label(r["kind"], r["status"]), axis=1)
    view["Valor"] = view["amount_cents"].map(brl_from_cents)
    view["Parcela"] = view.apply(lambda r: f"{r['installment_no']}/{r['installment_count']}", axis=1)

    st.dataframe(
        view[["Data", "Tipo", "description", "category", "Valor", "Status", "Parcela", "account"]].rename(
            columns={"description": "Descrição", "category": "Categoria", "account": "Conta"}
        ),
        hide_index=True,
        width="stretch",
        height=430,
    )

    csv_df = view[["Data", "Tipo", "description", "category", "amount", "Status", "Parcela", "account", "notes"]].rename(
        columns={
            "description": "Descrição",
            "category": "Categoria",
            "amount": "Valor",
            "account": "Conta",
            "notes": "Observações",
        }
    )
    st.download_button(
        "Exportar CSV",
        data=csv_df.to_csv(index=False, sep=";", decimal=",").encode("utf-8-sig"),
        file_name=f"movimentacoes_{start}_{end}.csv",
        mime="text/csv",
    )

    section_title("Gerenciar lançamento", "BAIXA · EDIÇÃO · EXCLUSÃO")
    if filtered.empty:
        st.info("Nenhum lançamento corresponde aos filtros.")
        return

    labels = {
        row["id"]: f"{row['due_date'].strftime('%d/%m/%Y')} | {kind_label(row['kind'])} | {row['description']} | {brl_from_cents(row['amount_cents'])} | {row['installment_no']}/{row['installment_count']}"
        for _, row in filtered.iterrows()
    }
    selected_id = st.selectbox("Selecione", list(labels.keys()), format_func=lambda x: labels[x])
    selected = db.transactions.find_one({"_id": ObjectId(selected_id), "owner_user_id": user["id"]})
    if not selected:
        st.warning("Lançamento não encontrado.")
        return

    a1, a2, a3 = st.columns(3)
    if selected["status"] == "pending":
        final_status = "paid" if selected["kind"] == "expense" else "received"
        if a1.button("Dar baixa", type="primary", width="stretch"):
            db.transactions.update_one(
                {"_id": selected["_id"]},
                {"$set": {"status": final_status, "paid_at": now_utc_naive(), "updated_at": now_utc_naive()}},
            )
            st.rerun()
    else:
        if a1.button("Voltar para pendente", width="stretch"):
            db.transactions.update_one(
                {"_id": selected["_id"]},
                {"$set": {"status": "pending", "paid_at": None, "updated_at": now_utc_naive()}},
            )
            st.rerun()

    if a2.button("Cancelar lançamento", width="stretch"):
        db.transactions.update_one(
            {"_id": selected["_id"]},
            {"$set": {"status": "canceled", "updated_at": now_utc_naive()}},
        )
        st.rerun()

    delete_scope = a3.selectbox(
        "Excluir",
        ["Somente este lançamento", "Todo o grupo/parcelamento"] if selected.get("installment_count", 1) > 1 else ["Somente este lançamento"],
        key=f"del_scope_{selected_id}",
    )
    if st.button("Excluir definitivamente", type="secondary"):
        if delete_scope == "Todo o grupo/parcelamento":
            result = db.transactions.delete_many({"owner_user_id": user["id"], "group_id": selected.get("group_id")})
        else:
            result = db.transactions.delete_one({"_id": selected["_id"], "owner_user_id": user["id"]})
        st.success(f"{result.deleted_count} lançamento(s) excluído(s).")
        st.rerun()

    with st.expander("Editar este lançamento", expanded=False):
        with st.form(f"edit_{selected_id}"):
            e1, e2 = st.columns([2, 1])
            edit_description = e1.text_input("Descrição", value=selected.get("description", ""))
            edit_value = e2.number_input(
                "Valor (R$)",
                min_value=0.01,
                value=cents_to_money(selected.get("amount_cents", 0)),
                step=10.0,
                format="%.2f",
            )
            e3, e4 = st.columns(2)
            edit_date = e3.date_input("Vencimento", value=selected.get("due_date", datetime.today()).date())
            edit_category = e4.text_input("Categoria", value=selected.get("category", "Outros"))
            e5, e6 = st.columns(2)
            edit_account = e5.text_input("Conta / cartão", value=selected.get("account", ""))
            edit_method = e6.text_input("Forma", value=selected.get("payment_method", ""))
            edit_notes = st.text_area("Observações", value=selected.get("notes", ""))
            save_edit = st.form_submit_button("Salvar alterações", type="primary")

        if save_edit:
            due = mongo_date(edit_date)
            db.transactions.update_one(
                {"_id": selected["_id"], "owner_user_id": user["id"]},
                {
                    "$set": {
                        "description": edit_description.strip(),
                        "amount_cents": money_to_cents(edit_value),
                        "due_date": due,
                        "competence": month_key(due),
                        "category": edit_category.strip() or "Outros",
                        "account": edit_account.strip(),
                        "payment_method": edit_method.strip(),
                        "notes": edit_notes.strip(),
                        "updated_at": now_utc_naive(),
                    }
                },
            )
            st.success("Lançamento atualizado.")
            st.rerun()


def page_budgets(db, user):
    render_page_header(
        "Orçamentos",
        "Defina limites mensais por categoria e acompanhe quanto do orçamento já foi comprometido.",
        "PLANEJAMENTO",
        "◎",
        "amber",
    )
    section_title("Configurar orçamento", "LIMITES MENSAIS")

    today = date.today()
    c1, c2 = st.columns(2)
    year = c1.number_input("Ano", min_value=2020, max_value=2100, value=today.year, step=1)
    month = c2.selectbox("Mês", range(1, 13), index=today.month - 1)
    key = f"{int(year)}-{int(month):02d}"

    with st.form("budget_form"):
        category = st.selectbox("Categoria", EXPENSE_CATEGORIES)
        limit_value = st.number_input("Limite mensal (R$)", min_value=0.01, value=500.00, step=50.00, format="%.2f")
        submitted = st.form_submit_button("Salvar orçamento", type="primary")

    if submitted:
        db.budgets.update_one(
            {"owner_user_id": user["id"], "month": key, "category": category},
            {
                "$set": {
                    "limit_cents": money_to_cents(limit_value),
                    "updated_at": now_utc_naive(),
                },
                "$setOnInsert": {"created_at": now_utc_naive()},
            },
            upsert=True,
        )
        st.success("Orçamento salvo.")

    budgets = list(db.budgets.find({"owner_user_id": user["id"], "month": key}).sort("category", ASCENDING))
    if not budgets:
        st.info("Nenhum orçamento definido para este mês.")
        return

    rows = transaction_rows(db, user, date(int(year), int(month), 1), date(int(year), int(month), calendar.monthrange(int(year), int(month))[1]))
    df = to_dataframe(rows)
    for item in budgets:
        if df.empty:
            spent = 0
        else:
            spent = int(
                df.loc[
                    (df["kind"] == "expense")
                    & (df["category"] == item["category"])
                    & (df["status"] != "canceled"),
                    "amount_cents",
                ].sum()
            )
        limit_cents = int(item["limit_cents"])
        pct = (spent / limit_cents * 100) if limit_cents else 0
        cols = st.columns([3, 2, 1])
        cols[0].write(f"**{item['category']}**")
        cols[1].write(f"{brl_from_cents(spent)} / {brl_from_cents(limit_cents)} — {pct:.0f}%")
        if cols[2].button("Excluir", key=f"budget_del_{item['_id']}"):
            db.budgets.delete_one({"_id": item["_id"], "owner_user_id": user["id"]})
            st.rerun()
        st.progress(min(max(pct / 100, 0.0), 1.0))


def page_my_account(db, user):
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
    with st.form("self_password_change"):
        current_password = st.text_input("Senha atual", type="password")
        new_password = st.text_input("Nova senha", type="password")
        confirm = st.text_input("Confirmar nova senha", type="password")
        submitted = st.form_submit_button("Alterar senha", type="primary")

    if submitted:
        db_user = db.users.find_one({"_id": ObjectId(user["id"])})
        if not password_verify(current_password, db_user["password_salt"], db_user["password_hash"]):
            st.error("Senha atual incorreta.")
            return
        if len(new_password) < 8:
            st.error("A nova senha precisa ter pelo menos 8 caracteres.")
            return
        if new_password != confirm:
            st.error("As novas senhas não coincidem.")
            return
        salt, pwd_hash = password_hash(new_password)
        db.users.update_one(
            {"_id": ObjectId(user["id"])},
            {"$set": {"password_salt": salt, "password_hash": pwd_hash, "must_change_password": False, "updated_at": now_utc_naive()}},
        )
        st.success("Senha atualizada.")


def page_admin_users(db, user):
    render_page_header(
        "Administração de usuários",
        "Crie acessos, controle perfis e gerencie credenciais dos usuários autorizados no sistema.",
        "ADMINISTRAÇÃO",
        "◇",
        "blue",
    )
    section_title("Usuários do sistema", "ACESSOS & PERMISSÕES")

    with st.expander("Criar novo usuário", expanded=False):
        with st.form("create_user"):
            c1, c2 = st.columns(2)
            name = c1.text_input("Nome")
            email = c2.text_input("E-mail")
            c3, c4 = st.columns(2)
            role = c3.selectbox("Perfil", ["user", "admin"])
            temp_password = c4.text_input("Senha temporária", type="password")
            create = st.form_submit_button("Criar usuário", type="primary")

        if create:
            email_n = normalize_email(email)
            if not name.strip() or "@" not in email_n:
                st.error("Informe nome e e-mail válidos.")
            elif len(temp_password) < 8:
                st.error("A senha temporária precisa ter pelo menos 8 caracteres.")
            else:
                salt, pwd_hash = password_hash(temp_password)
                try:
                    db.users.insert_one(
                        {
                            "name": name.strip(),
                            "email": email_n,
                            "role": role,
                            "active": True,
                            "password_salt": salt,
                            "password_hash": pwd_hash,
                            "must_change_password": True,
                            "created_at": now_utc_naive(),
                            "updated_at": now_utc_naive(),
                        }
                    )
                    st.success("Usuário criado.")
                except DuplicateKeyError:
                    st.error("Já existe um usuário com este e-mail.")

    users = list(db.users.find({}).sort("name", ASCENDING))
    table = pd.DataFrame(
        [
            {
                "Nome": u.get("name", ""),
                "E-mail": u.get("email", ""),
                "Perfil": u.get("role", "user"),
                "Ativo": bool(u.get("active", True)),
                "Troca de senha pendente": bool(u.get("must_change_password", False)),
            }
            for u in users
        ]
    )
    st.dataframe(table, hide_index=True, width="stretch")

    options = {str(u["_id"]): f"{u.get('name', '')} — {u.get('email', '')}" for u in users}
    selected_id = st.selectbox("Gerenciar usuário", list(options.keys()), format_func=lambda x: options[x])
    selected = db.users.find_one({"_id": ObjectId(selected_id)})

    c1, c2 = st.columns(2)
    if selected_id != user["id"]:
        action_label = "Desativar usuário" if selected.get("active", True) else "Reativar usuário"
        if c1.button(action_label, width="stretch"):
            db.users.update_one(
                {"_id": selected["_id"]},
                {"$set": {"active": not selected.get("active", True), "updated_at": now_utc_naive()}},
            )
            st.rerun()
    else:
        c1.info("Sua própria conta não pode ser desativada aqui.")

    with c2.form("reset_password"):
        reset_password = st.text_input("Nova senha temporária", type="password")
        reset = st.form_submit_button("Redefinir senha", width="stretch")
    if reset:
        if len(reset_password) < 8:
            st.error("A senha temporária precisa ter pelo menos 8 caracteres.")
        else:
            salt, pwd_hash = password_hash(reset_password)
            db.users.update_one(
                {"_id": selected["_id"]},
                {
                    "$set": {
                        "password_salt": salt,
                        "password_hash": pwd_hash,
                        "must_change_password": True,
                        "updated_at": now_utc_naive(),
                    }
                },
            )
            st.success("Senha redefinida. O usuário deverá trocá-la no próximo acesso.")


# -----------------------------------------------------------------------------
# App
# -----------------------------------------------------------------------------
def render_db_error(exc):
    st.error("Não foi possível conectar ao MongoDB.")
    if str(exc) == "MONGODB_URI_NOT_CONFIGURED":
        st.code(
            '[mongo]\nuri = "mongodb+srv://USUARIO:SENHA@CLUSTER.mongodb.net/?retryWrites=true&w=majority"\ndatabase = "financeiro_luiz"',
            language="toml",
        )
        st.info("No Streamlit Cloud, adicione esse conteúdo em Settings > Secrets.")
    else:
        st.info("Revise a connection string, usuário/senha do MongoDB Atlas e as regras de Network Access.")
        st.caption(f"Falha técnica: {type(exc).__name__}")


def main():
    try:
        db = get_database()
        ensure_database(db)
    except Exception as exc:
        render_db_error(exc)
        st.stop()

    user = current_user(db)
    if not user:
        render_login(db)
        st.stop()

    # Identidade visual global da área autenticada.
    inject_dashboard_theme()

    if user.get("must_change_password"):
        render_forced_password_change(db, user)
        st.stop()

    with st.sidebar:
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
                st.rerun()

        st.markdown(
            '<div class="sidebar-session-divider"><span>SESSÃO</span></div>',
            unsafe_allow_html=True,
        )
        if st.button("⏻  Encerrar sessão", key="logout_btn", width="stretch"):
            do_logout()

    if selected_page == "Dashboard":
        page_dashboard(db, user)
    elif selected_page == "Lançar despesa":
        page_add_expense(db, user)
    elif selected_page == "Lançar receita":
        page_add_income(db, user)
    elif selected_page == "Movimentações":
        page_transactions(db, user)
    elif selected_page == "Orçamentos":
        page_budgets(db, user)
    elif selected_page == "Minha conta":
        page_my_account(db, user)
    elif selected_page == "Usuários" and user["role"] == "admin":
        page_admin_users(db, user)


if __name__ == "__main__":
    main()
