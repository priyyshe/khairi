from flask import Flask, render_template_string, request, redirect, url_for, session

app = Flask(__name__)
app.secret_key = "rahasia"  # Ganti dengan secret key yang aman

# Template pertanyaan 1
q1_template = """
<!DOCTYPE html>
<html>
<head>
    <title>Pertanyaan 1</title>
    <style>
        body { background: linear-gradient(135deg, #f9d5ec 0%, #a1c4fd 100%); color: #333; font-family: 'Segoe UI', sans-serif; display: flex; flex-direction: column; align-items: center; justify-content: center; height: 100vh; }
        .form-box { background: #fff8fc; padding: 32px 40px; border-radius: 18px; box-shadow: 0 4px 24px rgba(160, 120, 200, 0.15); text-align: center; }
        input[type="text"] { padding: 8px; border-radius: 6px; border: 1px solid #e0b1cb; margin-top: 6px; width: 220px; }
        input[type="submit"] { background: #e0b1cb; color: #fff; border: none; padding: 10px 28px; border-radius: 8px; font-size: 1em; margin-top: 18px; cursor: pointer; transition: background 0.2s; }
        input[type="submit"]:hover { background: #a1c4fd; }
    </style>
</head>
<body>
    <div class="form-box">
        <h2>aloo khairi! 👋</h2>
        <p> ini ada beberapa pertanyaan buat kamu yaa </p>
        <form method="post">
            <label>Gimana kabarnya hari ini? 😊</label><br>
            <input type="text" name="warna" required><br><br>
            <input type="submit" value="Lanjut ➡️">
        </form>
    </div>
</body>
</html>
"""

# Template pertanyaan 2 (dengan pesan error jika salah)
q2_template = """
<!DOCTYPE html>
<html>
<head>
    <title>Pertanyaan 2</title>
    <style>
        body { background: linear-gradient(135deg, #f9d5ec 0%, #a1c4fd 100%); color: #333; font-family: 'Segoe UI', sans-serif; display: flex; flex-direction: column; align-items: center; justify-content: center; height: 100vh; }
        .form-box { background: #fff8fc; padding: 32px 40px; border-radius: 18px; box-shadow: 0 4px 24px rgba(160, 120, 200, 0.15); text-align: center; }
        input[type="text"] { padding: 8px; border-radius: 6px; border: 1px solid #e0b1cb; margin-top: 6px; width: 220px; }
        input[type="submit"] { background: #e0b1cb; color: #fff; border: none; padding: 10px 28px; border-radius: 8px; font-size: 1em; margin-top: 18px; cursor: pointer; transition: background 0.2s; }
        input[type="submit"]:hover { background: #a1c4fd; }
        .error { color: #e74c3c; margin-bottom: 10px; }
    </style>
</head>
<body>
    <div class="form-box">
        <h2>Pertanyaan 2 🥰</h2>
        {% if error %}
            <div class="error">{{ error }}</div>
        {% endif %}
        <form method="post">
            <label>panggilan atau sebutan yang selalu kmu kasi ke aku apa? </label><br>
            <input type="text" name="sayang" required><br><br>
            <input type="submit" value="Kirim 💖">
        </form>
    </div>
</body>
</html>
"""

# Template terima kasih
thanks_template = """
<!DOCTYPE html>
<html>
<head>
    <title>Terima Kasih!</title>
    <style>
        body { background: linear-gradient(135deg, #a1c4fd 0%, #f9d5ec 100%); color: #333; font-family: 'Segoe UI', sans-serif; display: flex; flex-direction: column; align-items: center; justify-content: center; height: 100vh; overflow: hidden;}
        .thanks-box { background: #fff8fc; padding: 36px 44px; border-radius: 18px; box-shadow: 0 4px 24px rgba(160, 120, 200, 0.15); text-align: center; z-index: 2; }
        h2 { font-size: 2em; }
        p { font-size: 1.2em; }
        .emoji-pop {
            position: fixed;
            bottom: -60px;
            font-size: 2.2em;
            animation: popUp 2.5s linear forwards;
            opacity: 0.85;
            pointer-events: none;
        }
        @keyframes popUp {
            0% { transform: translateY(0) scale(0.7) rotate(-10deg); opacity: 0.7;}
            60% { opacity: 1;}
            100% { transform: translateY(-110vh) scale(1.2) rotate(20deg); opacity: 0;}
        }
    </style>
</head>
<body>
    <div class="thanks-box">
        <h2>Terima kasih sudah jawab pertanyaannya! 🥳</h2>
        <p>wkwk kocak jangan lupa kasi rating nya ya! 💖✨</p>
    </div>
    <script>
        // Array emoji senang
        const emojis = ["🥳","💖","✨","😊","😍","🎉","💝","😻"];
        function randomBetween(a, b) {
            return Math.random() * (b - a) + a;
        }
        function createPopEmoji() {
            const emoji = emojis[Math.floor(Math.random() * emojis.length)];
            const span = document.createElement('span');
            span.className = 'emoji-pop';
            span.textContent = emoji;
            span.style.left = randomBetween(10, 90) + 'vw';
            span.style.fontSize = randomBetween(1.8, 2.8) + 'em';
            document.body.appendChild(span);
            setTimeout(() => { span.remove(); }, 2500);
        }
        // Pop up beberapa emoji secara acak dari bawah
        setInterval(createPopEmoji, 350);
        // Awal-awal langsung muncul beberapa
        for(let i=0;i<7;i++) setTimeout(createPopEmoji, i*200);
    </script>
</body>
</html>
"""

@app.route("/", methods=["GET", "POST"])
def q1():
    if request.method == "POST":
        session["warna"] = request.form["warna"]
        return redirect(url_for("q2"))
    return render_template_string(q1_template)

@app.route("/q2", methods=["GET", "POST"])
def q2():
    if "warna" not in session:
        return redirect(url_for("q1"))
    # Hitung berapa kali salah, simpan di session
    if "salah_count" not in session:
        session["salah_count"] = 0
    error = None
    if request.method == "POST":
        jawaban = request.form["sayang"]
        allowed = ["chupa chups", "Chupa cups", "chupa Chups", "Chupa Chups"]
        if jawaban.strip() in allowed:
            session["sayang"] = jawaban
            session.pop("salah_count", None)  # reset jika sudah benar
            return redirect(url_for("thanks"))
        else:
            session["salah_count"] += 1
            if session["salah_count"] == 1:
                error = "Yah, coba lagi yaa 😢"
            elif session["salah_count"] == 2:
                error = "Masa gitu aja gatau 😅"
            elif session["salah_count"] == 3:
                error = "Ayo semangat, pasti bisa! 💪"
            elif session["salah_count"] == 4:
                error = "Coba diingat-ingat lagi 🧐"
            else:
                error = "Hehe, jangan nyerah yaa 😆"
    return render_template_string(q2_template, error=error)

@app.route("/thanks")
def thanks():
    session.clear()
    return render_template_string(thanks_template)

if __name__ == "__main__":
    app.run(debug=True)