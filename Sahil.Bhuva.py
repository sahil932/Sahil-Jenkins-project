from flask import Flask, render_template_string, request, redirect, url_for

app = Flask(__name__)

# =====================================================================
#  EDIT HERE FOR YOUR LIVE CI/CD DEMO
#  Example change to show the pipeline working:
#  change Argentina -> Spain  (name "Argentina" -> "Spain",
#  flag "🇦🇷" -> "🇪🇸", player "Messi" -> your choice)
# =====================================================================
QUESTION = "Who will win the 2026 FIFA World Cup?"

TEAM_A = {
    "name": "France",
    "flag": "FR",
    "player": "Mbappé",
    "img": "",              # optional: paste an image URL you have rights to use
    "color": "#2563eb",     # card accent color
}

TEAM_B = {
    "name": "Sapin",
    "flag": "SP",
    "player": "Morata",
    "img": "",              # optional: paste an image URL you have rights to use
    "color": "#38bdf8",
}
# =====================================================================

# Vote counts kept in memory (reset when the app/container restarts).
votes = {"A": 0, "B": 0}

PAGE = """
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>World Cup 2026 Vote</title>
  <style>
    * { margin: 0; padding: 0; box-sizing: border-box; }
    body {
      font-family: -apple-system, "Segoe UI", Roboto, sans-serif;
      min-height: 100vh;
      display: flex; align-items: center; justify-content: center;
      padding: 24px;
      background:
        radial-gradient(circle at 20% 20%, rgba(56,189,248,.25), transparent 40%),
        radial-gradient(circle at 80% 80%, rgba(37,99,235,.25), transparent 40%),
        linear-gradient(135deg, #0f172a 0%, #1e293b 55%, #0f172a 100%);
      color: #f8fafc;
    }
    .wrap { width: 100%; max-width: 760px; text-align: center; }
    .badge {
      display: inline-block; font-size: 13px; letter-spacing: 2px;
      text-transform: uppercase; color: #94a3b8; margin-bottom: 10px;
    }
    h1 { font-size: clamp(24px, 5vw, 38px); line-height: 1.2; margin-bottom: 6px; }
    .total { color: #94a3b8; margin-bottom: 28px; font-size: 15px; }
    .cards { display: grid; grid-template-columns: 1fr 1fr; gap: 20px; }
    @media (max-width: 560px){ .cards { grid-template-columns: 1fr; } }
    .card {
      background: rgba(255,255,255,.06);
      border: 1px solid rgba(255,255,255,.12);
      backdrop-filter: blur(12px);
      border-radius: 22px; padding: 26px 20px;
      transition: transform .15s ease, box-shadow .15s ease;
    }
    .card:hover { transform: translateY(-4px); box-shadow: 0 18px 40px rgba(0,0,0,.35); }
    .flag { font-size: 74px; line-height: 1; }
    .flag img { width: 92px; height: 92px; object-fit: cover; border-radius: 50%;
                border: 3px solid rgba(255,255,255,.3); }
    .team { font-size: 24px; font-weight: 700; margin-top: 10px; }
    .player { color: #cbd5e1; font-size: 14px; margin-top: 2px; }
    .count { font-size: 40px; font-weight: 800; margin: 14px 0 4px; }
    .pct { color: #94a3b8; font-size: 13px; }
    .bar { height: 8px; border-radius: 999px; background: rgba(255,255,255,.12);
           margin: 12px 0 18px; overflow: hidden; }
    .bar > span { display:block; height:100%; border-radius:999px; transition: width .4s ease; }
    button {
      width: 100%; padding: 13px; border: none; border-radius: 12px;
      font-size: 16px; font-weight: 700; color: #0f172a; cursor: pointer;
      transition: filter .15s ease;
    }
    button:hover { filter: brightness(1.08); }
    .foot { margin-top: 26px; }
    .reset { color:#64748b; font-size:12px; text-decoration:none; border-bottom:1px dotted #475569; }
  </style>
</head>
<body>
  <div class="wrap">
    <div class="badge">⚽ FIFA World Cup 2026</div>
    <h1>{{ question }}</h1>
    <p class="total">Total votes: {{ total }}</p>

    <div class="cards">
      {% for key, team, count, pct in rows %}
      <div class="card" style="box-shadow: inset 0 0 0 2px {{ team.color }}33;">
        <div class="flag">
          {% if team.img %}<img src="{{ team.img }}" alt="{{ team.name }}">{% else %}{{ team.flag }}{% endif %}
        </div>
        <div class="team">{{ team.name }}</div>
        <div class="player">★ {{ team.player }}</div>
        <div class="count">{{ count }}</div>
        <div class="pct">{{ pct }}%</div>
        <div class="bar"><span style="width: {{ pct }}%; background: {{ team.color }};"></span></div>
        <form method="POST" action="{{ url_for('vote') }}">
          <input type="hidden" name="choice" value="{{ key }}">
          <button type="submit" style="background: {{ team.color }};">Vote {{ team.name }}</button>
        </form>
      </div>
      {% endfor %}
    </div>

    <div class="foot">
      <a class="reset" href="{{ url_for('reset') }}">reset votes</a>
    </div>
  </div>
</body>
</html>
"""


@app.route("/")
def index():
    total = votes["A"] + votes["B"]
    pct_a = round(votes["A"] / total * 100) if total else 0
    pct_b = round(votes["B"] / total * 100) if total else 0
    rows = [
        ("A", TEAM_A, votes["A"], pct_a),
        ("B", TEAM_B, votes["B"], pct_b),
    ]
    return render_template_string(PAGE, question=QUESTION, total=total, rows=rows)


@app.route("/vote", methods=["POST"])
def vote():
    choice = request.form.get("choice")
    if choice in votes:
        votes[choice] += 1
    return redirect(url_for("index"))


@app.route("/reset")
def reset():
    votes["A"] = 0
    votes["B"] = 0
    return redirect(url_for("index"))


if __name__ == "__main__":
    # host 0.0.0.0 so it works inside a Docker container
    app.run(host="0.0.0.0", port=5000)
