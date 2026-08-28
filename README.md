# Meu Financeiro

Aplicativo de financeiro pessoal em **Streamlit**, com persistência em **MongoDB**, autenticação por usuário, despesas parceladas, receitas recorrentes, dashboard e relatórios.

## Funcionalidades

- Login e senha com hash PBKDF2-SHA256.
- Usuário administrador inicial criado automaticamente no primeiro acesso ao MongoDB.
- Troca obrigatória da senha inicial no primeiro login.
- Isolamento dos dados financeiros por usuário.
- Lançamento de despesas à vista e parceladas.
- Opção para informar o valor total da compra ou o valor de cada parcela.
- Definição da quantidade de parcelas e do dia de vencimento.
- Ajuste automático para o último dia válido do mês.
- Lançamento de receitas únicas ou recorrentes.
- Status de pendente, pago/recebido e cancelado.
- Dashboard com KPIs, fluxo mensal, despesas por categoria, saldo acumulado e próximos vencimentos.
- Orçamento mensal por categoria.
- Consulta, edição, baixa, exclusão e exportação CSV das movimentações.
- Administração de usuários pelo perfil admin.

## Estrutura

```text
.
├── app.py
├── .streamlit/
│   ├── config.toml
│   └── secrets.toml.example
├── .gitignore
├── LICENSE
├── README.md
└── requirements.txt
```

## MongoDB Atlas

1. Crie um cluster no MongoDB Atlas.
2. Crie um usuário de banco.
3. Em **Network Access**, permita o acesso necessário para o Streamlit Cloud. Em um projeto pessoal, `0.0.0.0/0` é a configuração mais simples, desde que o usuário do banco tenha senha forte; restrinja posteriormente se sua arquitetura permitir.
4. Copie a connection string no formato `mongodb+srv://...`.

## Streamlit Cloud

1. No Streamlit Community Cloud, crie um novo app.
2. Selecione este repositório e a branch `main`.
3. Arquivo principal: `app.py`.
4. Em **Settings > Secrets**, configure:

```toml
[mongo]
uri = "mongodb+srv://USUARIO:SENHA@CLUSTER.mongodb.net/?retryWrites=true&w=majority"
database = "financeiro_luiz"
```

Também é possível usar as variáveis de ambiente `MONGODB_URI` e `MONGODB_DB`.

## Primeiro acesso

O aplicativo cria automaticamente o administrador solicitado quando o e-mail ainda não existir na coleção `users`. A senha inicial não fica gravada em texto puro no repositório: apenas salt e hash PBKDF2 são usados para o bootstrap.

No primeiro login, o aplicativo exige a troca da senha inicial antes de liberar o financeiro.

## Execução local

```bash
python -m venv .venv
```

Linux/macOS:

```bash
source .venv/bin/activate
pip install -r requirements.txt
cp .streamlit/secrets.toml.example .streamlit/secrets.toml
streamlit run app.py
```

Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
Copy-Item .streamlit\secrets.toml.example .streamlit\secrets.toml
streamlit run app.py
```

Edite `.streamlit/secrets.toml` antes de iniciar.

## Segurança

- Nunca faça commit de `.streamlit/secrets.toml`.
- A connection string do MongoDB deve ficar somente nos Secrets do Streamlit Cloud ou em variável de ambiente.
- Senhas são armazenadas com PBKDF2-SHA256, 310.000 iterações e salt aleatório.
- O login inicial deve ter a senha alterada no primeiro acesso.
