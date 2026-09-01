import os
import pandas as pd
from flask import Flask, request, redirect, url_for, session

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "troque_por_algo_secreto_em_producao")

df = pd.read_excel("alunos_matricula.xlsx")
alunos = df.to_dict(orient="records")

# ─── Design System — Faculdade de Miguel Pereira ─────────────────────────────
BASE_HEAD = """
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Playfair+Display:wght@600;700&family=DM+Sans:wght@400;500;600&display=swap" rel="stylesheet">
<!-- Biblioteca de ícones profissionais -->
<script src="https://unpkg.com/lucide@latest"></script>
<style>
  *, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

  :root {
    --maroon:    #6d1d20;
    --maroon-dk: #5a1619;
    --maroon-lt: #f5e8e8;
    --gray:      #a59c97;
    --gray-lt:   #e8e4e1;
    --cream:     #f8f9fa;
    --white:     #ffffff;
    --text:      #212529;
    --muted:     #6c757d;
    --danger:    #b91c1c;
    --radius:    8px;
    --shadow:    0 2px 8px rgba(0,0,0,0.05);
    --shadow-lg: 0 8px 24px rgba(0,0,0,0.08);
    --font-heading: 'Playfair Display', Georgia, serif;
    --font-body:    'DM Sans', system-ui, sans-serif;
  }

  body { font-family: var(--font-body); color: var(--text); background: var(--cream); line-height: 1.5; }

  .card {
    background: var(--white);
    border-radius: var(--radius);
    box-shadow: var(--shadow-lg);
    overflow: hidden;
    border: 1px solid #e9ecef;
  }

  .btn {
    display: inline-flex; align-items: center; justify-content: center; gap: 8px;
    padding: 12px 24px; border: none; border-radius: 6px;
    font-family: var(--font-body); font-size: 15px; font-weight: 600;
    cursor: pointer; text-decoration: none; transition: all .2s ease;
    width: 100%;
  }
  .btn-primary { background: var(--maroon); color: var(--white); }
  .btn-primary:hover { background: var(--maroon-dk); }

  input[type="text"], input[type="password"] {
    width: 100%; padding: 12px 16px;
    border: 1px solid #ced4da; border-radius: 6px;
    font-family: var(--font-body); font-size: 15px; color: var(--text);
    background: var(--white); transition: border-color .2s;
    outline: none;
  }
  input:focus { border-color: var(--maroon); box-shadow: 0 0 0 3px rgba(109,29,32,.10); }

  label { display: block; font-size: 12px; font-weight: 600;
          color: var(--muted); text-transform: uppercase; letter-spacing: .05em; margin-bottom: 6px; }

  a { color: var(--maroon); text-decoration: none; }
  a:hover { text-decoration: underline; }
</style>
"""


# ─── LOGIN ────────────────────────────────────────────────────────────────────
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
  <title>Login · Portal do Aluno · FAMIPE</title>
  {BASE_HEAD}
  <style>
    body {{
      min-height: 100vh;
      display: flex; align-items: center; justify-content: center;
      padding: 24px;
      position: relative; overflow: hidden;
    }}
    body::before {{
      content: '';
      position: fixed; inset: 0;
      background: url('/static/famipe_cleanup.png') center center / cover no-repeat;
      filter: blur(4px) brightness(0.3);
      transform: scale(1.05);
      z-index: 0;
    }}
    .login-card {{ width: 100%; max-width: 400px; position: relative; z-index: 1; }}

    .login-header {{
      background: var(--maroon);
      padding: 32px 36px 24px;
      text-align: center; color: var(--white);
    }}
    .logo-wrap {{
      margin-bottom: 12px;
    }}
    .logo-wrap img {{
      height: 48px; width: auto;
      filter: brightness(0) invert(1);
    }}
    .login-header p {{
      margin-top: 8px; color: rgba(255,255,255,.8); font-size: 14px;
    }}
    .login-body {{ padding: 32px 36px; }}
    .field {{ margin-bottom: 20px; }}
    .alert-error {{
      display: flex; align-items: center; gap: 10px;
      background: #fdf6f6; border: 1px solid #f5c2c7;
      color: var(--danger); border-radius: 6px;
      padding: 12px 16px; font-size: 14px; font-weight: 500;
      margin-bottom: 20px;
    }}
    .forgot-link {{
      display: block; text-align: center; margin-top: 24px;
      font-size: 13px; color: var(--muted);
    }}
    .forgot-link a {{ color: var(--maroon); font-weight: 600; }}
  </style>
</head>
<body>
  <div class="card login-card">
    <div class="login-header">
      <div class="logo-wrap">
        <img src="/static/horizontal_branca.png" alt="Faculdade de Miguel Pereira">
      </div>
      <p>Portal do Aluno</p>
    </div>
    <div class="login-body">
      {"<div class='alert-error'><i data-lucide='alert-circle' size='18'></i><span>" + erro + "</span></div>" if erro else ""}
      <form method="post" novalidate>
        <div class="field">
          <label for="matricula">Matrícula</label>
          <input type="text" id="matricula" name="matricula" autocomplete="username" required>
        </div>
        <div class="field">
          <label for="senha">Senha</label>
          <input type="password" id="senha" name="senha" autocomplete="current-password" required>
        </div>
        <button type="submit" class="btn btn-primary">Acessar <i data-lucide="arrow-right" size="18"></i></button>
      </form>
      <p class="forgot-link">Problemas de acesso?
        <a href="mailto:suporte@famipe.edu.br">Contate a secretaria</a>
      </p>
    </div>
  </div>
  <script>lucide.createIcons();</script>
</body>
</html>"""


# ─── BOAS-VINDAS ──────────────────────────────────────────────────────────────
@app.route("/boas_vindas")
def boas_vindas():
    if "aluno" not in session:
        return redirect(url_for("login"))
    aluno = session["aluno"]
    primeiro_nome = aluno["Nome"].split()[0]

    return f"""<!DOCTYPE html>
<html lang="pt-BR">
<head>
  <title>Portal do Aluno · FAMIPE</title>
  {BASE_HEAD}
  <style>
    body {{
      min-height: 100vh;
      display: flex; flex-direction: column; align-items: center;
      background: var(--cream); padding: 0;
    }}
    .page-header {{
      width: 100%; background: var(--maroon);
      padding: 16px 32px;
      display: flex; align-items: center; justify-content: space-between;
    }}
    .page-header img {{ height: 32px; width: auto; filter: brightness(0) invert(1); }}
    .logout-top {{
      display: flex; align-items: center; gap: 6px;
      color: rgba(255,255,255,.8); font-size: 14px; font-weight: 500;
      text-decoration: none; transition: color .15s;
    }}
    .logout-top:hover {{ color: var(--white); text-decoration: none; }}

    .welcome-wrap {{
      flex: 1; display: flex; align-items: center; justify-content: center;
      padding: 40px 24px; width: 100%;
    }}
    .welcome-card {{ width: 100%; max-width: 500px; }}
    .welcome-hero {{
      background: var(--white);
      padding: 32px 32px 24px; border-bottom: 1px solid #e9ecef;
      display: flex; align-items: center; gap: 20px;
    }}
    .avatar {{
      width: 56px; height: 56px; border-radius: 50%;
      background: var(--maroon-lt); color: var(--maroon);
      display: flex; align-items: center; justify-content: center;
      flex-shrink: 0;
    }}
    .welcome-text h1 {{
      font-family: var(--font-heading); font-size: 22px;
      color: var(--text); margin-bottom: 4px;
    }}
    .welcome-text p {{ color: var(--muted); font-size: 14px; }}

    .welcome-body {{ padding: 24px 32px 32px; }}
    .info-grid {{
      display: grid; grid-template-columns: 1fr 1fr; gap: 12px;
      margin-bottom: 32px;
    }}
    .info-item {{
      background: var(--cream); border: 1px solid #e9ecef;
      border-radius: 6px; padding: 12px;
      display: flex; flex-direction: column; gap: 4px;
    }}
    .info-label {{ display: flex; align-items: center; gap: 6px; font-size: 12px; color: var(--muted); text-transform: uppercase; font-weight: 600; }}
    .info-value {{ font-size: 14px; font-weight: 500; color: var(--text); }}

    .section-title {{
      font-size: 12px; font-weight: 600; text-transform: uppercase;
      color: var(--muted); margin-bottom: 16px;
    }}
    .option-card {{
      display: flex; align-items: center; gap: 16px;
      border: 1px solid #e9ecef; border-radius: 8px;
      padding: 16px; margin-bottom: 12px;
      text-decoration: none; color: var(--text);
      transition: all .2s ease; background: var(--white);
    }}
    .option-card:hover {{
      border-color: var(--maroon);
      box-shadow: var(--shadow);
      text-decoration: none;
    }}
    .option-icon {{
      width: 40px; height: 40px; border-radius: 6px;
      display: flex; align-items: center; justify-content: center;
      color: var(--maroon); background: var(--maroon-lt); flex-shrink: 0;
    }}
    .option-title {{ font-size: 15px; font-weight: 600; margin-bottom: 2px; }}
    .option-desc {{ font-size: 13px; color: var(--muted); }}
    .option-arrow {{ margin-left: auto; color: var(--gray); }}
  </style>
</head>
<body>
  <header class="page-header">
    <img src="/static/horizontal_branca.png" alt="FAMIPE">
    <a href="/logout" class="logout-top">Sair <i data-lucide="log-out" size="16"></i></a>
  </header>

  <div class="welcome-wrap">
    <div class="card welcome-card">
      <div class="welcome-hero">
        <div class="avatar"><i data-lucide="graduation-cap" size="28"></i></div>
        <div class="welcome-text">
          <h1>Olá, {primeiro_nome}.</h1>
          <p>Portal Institucional do Aluno</p>
        </div>
      </div>
      <div class="welcome-body">
        <div class="info-grid">
          <div class="info-item">
            <span class="info-label"><i data-lucide="book" size="14"></i> Curso</span>
            <span class="info-value">{aluno["Curso"]}</span>
          </div>
          <div class="info-item">
            <span class="info-label"><i data-lucide="hash" size="14"></i> Matrícula</span>
            <span class="info-value">{aluno["Matrícula"]}</span>
          </div>
          <div class="info-item">
            <span class="info-label"><i data-lucide="map-pin" size="14"></i> Local</span>
            <span class="info-value">Sala {aluno["Sala Atual"]}</span>
          </div>
          <div class="info-item">
            <span class="info-label"><i data-lucide="clock" size="14"></i> Horário</span>
            <span class="info-value">{aluno["Horário Aula"]}</span>
          </div>
        </div>
        
        <p class="section-title">Serviços Acadêmicos</p>
        <a href="/tour" class="option-card">
          <div class="option-icon"><i data-lucide="map"></i></div>
          <div>
            <div class="option-title">Mapa do Campus</div>
            <div class="option-desc">Explore a infraestrutura da faculdade</div>
          </div>
          <i data-lucide="chevron-right" size="20" class="option-arrow"></i>
        </a>
        <a href="/chat" class="option-card">
          <div class="option-icon" style="background:#e8e4e1; color:#212529;"><i data-lucide="message-square"></i></div>
          <div>
            <div class="option-title">Atendimento Virtual</div>
            <div class="option-desc">Consulte pendências, horários e secretaria</div>
          </div>
          <i data-lucide="chevron-right" size="20" class="option-arrow"></i>
        </a>
      </div>
    </div>
  </div>
  <script>lucide.createIcons();</script>
</body>
</html>"""


# ─── CHAT ─────────────────────────────────────────────────────────────────────
@app.route("/chat", methods=["GET", "POST"])
def chat():
    if "aluno" not in session:
        return redirect(url_for("login"))
    aluno = session["aluno"]

    if "historico" not in session:
        session["historico"] = []

    if request.method == "POST":
        pergunta = request.form.get("pergunta", "").strip()
        if pergunta:
            p = pergunta.lower()
            if "pendência" in p or "pendencia" in p:
                resposta = f"Situação acadêmica: {aluno['Pendências']}."
            elif "sala" in p:
                resposta = f"Sua próxima aula presencial ocorrerá na sala {aluno['Sala Atual']}."
            elif "horário" in p or "horario" in p:
                resposta = f"Seu horário registrado para este semestre é {aluno['Horário Aula']}."
            elif "professor" in p:
                resposta = f"Seu professor orientador/regente é {aluno['Professor']}."
            elif "mensalidade" in p:
                resposta = f"Status do departamento financeiro: {aluno['Mensalidade']}."
            elif "curso" in p:
                resposta = f"Você está regularmente matriculado no curso de {aluno['Curso']}."
            elif "matrícula" in p or "matricula" in p:
                resposta = f"Status da matrícula: {aluno['Matrícula Ativa']}."
            else:
                resposta = "Não compreendi a solicitação. Por favor, consulte informações sobre: sala, horário, professor, financeiro ou pendências."
            session["historico"].append({"role": "user", "content": pergunta})
            session["historico"].append({"role": "assistant", "content": resposta})
            session.modified = True
        return redirect(url_for("chat"))

    historico = session.get("historico", [])

    def render_msgs():
        html = ""
        for msg in historico:
            if msg["role"] == "user":
                html += f'<div class="msg-row user-row"><div class="bubble user-bubble">{msg["content"]}</div></div>'
            else:
                html += f'<div class="msg-row bot-row"><div class="bubble-avatar"><i data-lucide="headphones" size="16"></i></div><div class="bubble bot-bubble">{msg["content"]}</div></div>'
        return html or '<div class="empty-state"><i data-lucide="message-square-text" size="32" style="margin-bottom:12px; color:var(--gray)"></i><br>Central de Atendimento. Como posso ajudar com sua matrícula hoje?</div>'

    return f"""<!DOCTYPE html>
<html lang="pt-BR">
<head>
  <title>Atendimento · FAMIPE</title>
  {BASE_HEAD}
  <style>
    body {{
      min-height: 100vh; display: flex; flex-direction: column;
      background: var(--cream); padding: 0;
    }}
    .topbar {{
      background: var(--maroon); color: var(--white);
      display: flex; align-items: center; gap: 16px;
      padding: 12px 24px; flex-shrink: 0;
    }}
    .topbar-back {{
      color: rgba(255,255,255,.8);
      display: flex; align-items: center;
      transition: color .15s;
    }}
    .topbar-back:hover {{ color: var(--white); }}
    .topbar-logo {{ flex: 1; display: flex; align-items: center; }}
    .topbar-logo img {{ height: 26px; width: auto; filter: brightness(0) invert(1); }}
    .topbar-sub {{ font-size: 13px; font-weight: 500; color: rgba(255,255,255,.8); border-left: 1px solid rgba(255,255,255,.2); padding-left: 16px; }}
    .topbar-clear {{
      display: flex; align-items: center; gap: 6px;
      background: transparent; border: 1px solid rgba(255,255,255,.3);
      color: var(--white); border-radius: 6px; padding: 6px 12px;
      font-size: 12px; font-weight: 500; cursor: pointer; text-decoration: none;
      transition: background .15s;
    }}
    .topbar-clear:hover {{ background: rgba(255,255,255,.1); }}

    .chat-area {{
      flex: 1; overflow-y: auto; padding: 24px 16px;
      display: flex; flex-direction: column; gap: 16px;
      max-width: 720px; width: 100%; margin: 0 auto;
    }}
    .msg-row {{ display: flex; align-items: flex-end; gap: 12px; }}
    .user-row {{ justify-content: flex-end; }}
    .bot-row  {{ justify-content: flex-start; }}
    .bubble {{
      max-width: 75%; padding: 12px 16px; border-radius: 8px;
      font-size: 14px; line-height: 1.5;
    }}
    .user-bubble {{
      background: var(--maroon); color: var(--white);
      border-bottom-right-radius: 2px;
    }}
    .bot-bubble {{
      background: var(--white); color: var(--text);
      border: 1px solid #e9ecef; border-bottom-left-radius: 2px;
    }}
    .bubble-avatar {{
      width: 32px; height: 32px; border-radius: 6px;
      background: var(--maroon-lt); color: var(--maroon);
      display: flex; align-items: center; justify-content: center; flex-shrink: 0;
    }}
    .empty-state {{
      text-align: center; color: var(--muted); font-size: 14px;
      padding: 48px 16px;
    }}
    .quick-chips {{
      display: flex; flex-wrap: wrap; gap: 8px;
      max-width: 720px; width: 100%; margin: 0 auto;
      padding: 0 16px 16px;
    }}
    .chip {{
      display: inline-flex; align-items: center; gap: 6px;
      background: var(--white); border: 1px solid #ced4da;
      border-radius: 6px; padding: 8px 12px; font-size: 13px;
      color: var(--text); cursor: pointer;
      transition: all .15s; font-family: var(--font-body);
    }}
    .chip:hover {{ background: var(--cream); border-color: var(--gray); }}
    .chip i {{ color: var(--maroon); }}
    
    .input-bar {{
      background: var(--white); border-top: 1px solid #e9ecef;
      padding: 16px; flex-shrink: 0;
    }}
    .input-row {{
      display: flex; gap: 12px; max-width: 720px; margin: 0 auto;
    }}
    .input-row input {{ flex: 1; padding: 12px 16px; border: 1px solid #ced4da; border-radius: 6px; }}
    .send-btn {{
      background: var(--maroon); color: var(--white); border: none;
      border-radius: 6px; padding: 0 20px;
      cursor: pointer; transition: background .2s; display: flex; align-items: center; justify-content: center;
    }}
    .send-btn:hover {{ background: var(--maroon-dk); }}
  </style>
</head>
<body>
  <div class="topbar">
    <a href="/boas_vindas" class="topbar-back" aria-label="Voltar"><i data-lucide="arrow-left" size="20"></i></a>
    <div class="topbar-logo"><img src="/static/horizontal_branca.png" alt="FAMIPE"></div>
    <span class="topbar-sub">{aluno["Nome"].split()[0]}</span>
    <a href="/limpar_chat" class="topbar-clear"><i data-lucide="rotate-ccw" size="14"></i> Reiniciar</a>
  </div>

  <div class="chat-area" id="chat-area">
    {render_msgs()}
  </div>

  {"" if historico else '''
  <div class="quick-chips" id="chips">
    <button class="chip" onclick="sendChip('Qual meu horário?')"><i data-lucide="calendar" size="14"></i> Horário</button>
    <button class="chip" onclick="sendChip('Qual minha sala?')"><i data-lucide="map-pin" size="14"></i> Localização</button>
    <button class="chip" onclick="sendChip('Tenho pendências?')"><i data-lucide="alert-circle" size="14"></i> Pendências</button>
    <button class="chip" onclick="sendChip('Status da mensalidade')"><i data-lucide="credit-card" size="14"></i> Financeiro</button>
  </div>
  '''}

  <div class="input-bar">
    <form method="post" class="input-row" id="form">
      <input type="text" name="pergunta" id="pergunta"
             placeholder="Descreva sua solicitação..." autocomplete="off" required>
      <button type="submit" class="send-btn" aria-label="Enviar"><i data-lucide="send" size="18"></i></button>
    </form>
  </div>

  <script>
    lucide.createIcons();
    var ca = document.getElementById('chat-area');
    if (ca) ca.scrollTop = ca.scrollHeight;
    function sendChip(text) {{
      document.getElementById('pergunta').value = text;
      var chips = document.getElementById('chips');
      if (chips) chips.style.display = 'none';
      document.getElementById('form').submit();
    }}
  </script>
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
    app.run(host="0.0.0.0", port=port, debug=False)