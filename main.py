import telebot
import sqlite3
import csv

TOKEN = '7103782951:AAEdkkP9DlvYBLEN2bc13Z1NCDgtygrFVXM'

bot = telebot.TeleBot(TOKEN)

con = sqlite3.connect('Tatarin.db')
cur = con.cursor()
cur.execute(
    '''CREATE TABLE IF NOT EXISTS students
    (id INTEGER PRIMARY KEY AUTOINCREMENT,
    gruppa integer,
    surname text
    )''')

with open('student.csv', 'r', newline='', encoding='utf-8') as file:
    reader = csv.DictReader(file)
    for row in reader:
        if row['gruppa'] and row['surname']:
            cur.execute('''INSERT INTO students(gruppa, surname) VALUES (?, ?)''',
                        (row['gruppa'], row['surname']))
    con.commit()
def get_db_connection():
    return sqlite3.connect('Tatarin.db')

@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "Для поиска введите фамилию:")
    bot.register_next_step_handler(message, get_student_info)

def get_student_info(message):
    surname = message.text
    with get_db_connection() as con:
        cur = con.cursor()
        try:
            cur.execute("SELECT * FROM students WHERE surname = ?", (surname,))
            student = cur.fetchone()
            if student:
                student_id, gruppa, student_surname = student
                bot.reply_to(message, f"Студент с фамилией {student_surname} находится в группе {gruppa}")
            else:
                bot.reply_to(message, "Студент с такой фамилией не найден")
        finally:
            cur.close()

bot.polling()