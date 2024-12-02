from flask import Flask, request, jsonify
from flask_cors import CORS
from sqlalchemy import create_engine, Column, Integer, String, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

app = Flask(__name__)
CORS(app)  # Для разрешения запросов с разных источников

# Настройка базы данных SQLite (можно заменить на облачную)
DATABASE_URL = "sqlite:///chat.db"
engine = create_engine(DATABASE_URL)
Base = declarative_base()

# Модель данных для сообщений
class Message(Base):
    __tablename__ = "messages"
    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(50), nullable=False)
    text = Column(Text, nullable=False)

# Создаем таблицы
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()

# Получение всех сообщений
@app.route("/messages", methods=["GET"])
def get_messages():
    messages = session.query(Message).all()
    return jsonify([{"username": m.username, "text": m.text} for m in messages])

# Отправка нового сообщения
@app.route("/messages", methods=["POST"])
def send_message():
    data = request.json
    username = data.get("username")
    text = data.get("text")
    if not username or not text:
        return jsonify({"error": "Invalid data"}), 400

    new_message = Message(username=username, text=text)
    session.add(new_message)
    session.commit()
    return jsonify({"success": True}), 201

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
