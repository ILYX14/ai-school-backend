from flask import Flask, request, jsonify
import openai
import os

app = Flask(__name__)

# Убедись, что ты установил переменную среды OPENAI_API_KEY на Render или в .env-файле локально
openai.api_key = os.getenv("OPENAI_API_KEY")

@app.route("/ask", methods=["POST"])
def ask():
    data = request.json
    user_question = data.get("question", "")

    messages = [
        {
            "role": "system",
            "content": "Ты — AI-помощник для школьников. Отвечай только на учебные вопросы по школьным предметам: математика, физика, история, биология, химия, русский язык и др. Если вопрос не связан с учёбой — вежливо откажись. Пиши понятно и кратко."
        },
        {
            "role": "user",
            "content": user_question
        }
    ]

    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=messages
        )
        reply = response.choices[0].message["content"]
        return jsonify({"answer": reply})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
