import os
import pandas as pd
from flask import Flask, request, redirect, url_for, session

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "troque_por_algo_secreto_em_producao")

df = pd.read_excel("alunos_matricula.xlsx")
alunos = df.to_dict(orient="records")


# 🔐 ROTA DE LOGIN
@app.route("/", methods=["GET", "POST"])
def login():
    erro = ""
    if request.method == "POST":
        matricula = request.form.get("matricula", "").strip()
        senha = request.form.get("senha", "").strip()
        for aluno in alunos:
            if str(aluno["Matrícula"]) == matricula and str(aluno["Senha"]) == senha:
                session.clear()
                session["aluno"] = aluno
                return redirect(url_for("boas_vindas"))
        erro = "Matrícula ou senha incorreta. Tente novamente."

    return f"""<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <title>Login</title>
    <style>
        body {
            font-family: Arial;
            background: linear-gradient(to right, #4facfe, #00f2fe);
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
        }

        .login-box {
            background: white;
            padding: 30px;
            border-radius: 10px;
            box-shadow: 0px 0px 10px rgba(0,0,0,0.2);
            text-align: center;
        }

        input {
            width: 80%;
            padding: 10px;
            margin: 10px;
            border-radius: 5px;
            border: 1px solid #ccc;
        }

        button {
            background: #4facfe;
            color: white;
            padding: 10px 20px;
            border: none;
            border-radius: 5px;
            cursor: pointer;
        }

        button:hover {
            background: #00c6ff;
        }
    </style>
</head>
<body>
    <div class="login-box">
        <h2>🎓 Login do Aluno</h2>
        <form method="post">
            <input type="text" name="matricula" placeholder="Matrícula" required><br>
            <input type="password" name="senha" placeholder="Senha" required><br>
            <button type="submit">Entrar</button>
        </form>
    </div>
</body>
</html>"""


# 🤖 ROTA DO CHAT
@app.route("/chat", methods=["GET", "POST"])
def chat():
    if "aluno" not in session:
        return redirect(url_for("login"))
    aluno = session["aluno"]

    if "historico" not in session:
        session["historico"] = []

    if request.method == "POST":
        pergunta = request.form["pergunta"].lower()

        if "pendência" in pergunta:
            resposta = f"Sua pendência é: {aluno['Pendências']}"
        
        elif "sala" in pergunta:
            resposta = f"Sua aula é na sala {aluno['Sala Atual']}"
        
        elif "horário" in pergunta:
            resposta = f"Seu horário de aula é {aluno['Horário Aula']}"
        
        elif "professor" in pergunta:
            resposta = f"Seu professor é {aluno['Professor']}"
        
        elif "mensalidade" in pergunta:
            resposta = f"Status da mensalidade: {aluno['Mensalidade']}"
        
        elif "curso" in pergunta:
            resposta = f"Seu curso é {aluno['Curso']}"

        elif "matrícula ativa" in pergunta or "matricula ativa" in pergunta:
            resposta = f"status da matrícula: {aluno['Matricula Ativa']}"
            
        else:
            resposta = "Desculpe, não entendi sua pergunta."

    return f"""<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <title>Chat do Aluno</title>
    <style>
        body {{
            font-family: Arial;
            background: #f0f2f5;
            display: flex;
            flex-direction: column;
            align-items: center;
        }}

        .chat-container {{
            width: 400px;
            background: white;
            margin-top: 50px;
            border-radius: 10px;
            box-shadow: 0px 0px 10px rgba(0,0,0,0.2);
            padding: 20px;
        }}

        .header {{
            text-align: center;
            margin-bottom: 20px;
        }}

        .messages {{
            height: 200px;
            overflow-y: auto;
            border: 1px solid #ccc;
            padding: 10px;
            border-radius: 5px;
            margin-bottom: 10px;
        }}

        .user {{
            text-align: right;
            margin: 5px;
            color: blue;
        }}

        .bot {{
            text-align: left;
            margin: 5px;
            color: green;
        }}

        input {{
            width: 70%;
            padding: 10px;
        }}

        button {{
            padding: 10px;
            background: #4facfe;
            color: white;
            border: none;
            border-radius: 5px;
        }}

        button:hover {{
            background: #00c6ff;
        }}

        a {{
            display: block;
            text-align: center;
            margin-top: 10px;
        }}
    </style>
</head>
<body>

<div class="chat-container">
    <div class="header">
        <h3>🎓 {aluno["Nome"]}</h3>
    </div>

  <div class="chat-area" id="chat-area">
    {render_msgs()}
  </div>

    <form method="post">
        <input type="text" name="pergunta" placeholder="Digite sua pergunta..." required>
        <button type="submit">Enviar</button>
    </form>
  </div>

</body>
</html>"""


@app.route("/limpar_chat")
def limpar_chat():
    session.pop("historico", None)
    return redirect(url_for("chat"))


# ─── TOUR ─────────────────────────────────────────────────────────────────────
@app.route("/tour")
def tour():
    return open("tour.html", encoding="utf-8").read()


# ─── LOGOUT ───────────────────────────────────────────────────────────────────
@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))


# ─── SERVIDOR ─────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
