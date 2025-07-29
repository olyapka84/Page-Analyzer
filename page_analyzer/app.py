from datetime import datetime
from flask import Flask, render_template, request, flash, redirect, url_for
from dotenv import load_dotenv
import os
import psycopg2
from psycopg2.extras import RealDictCursor
from urllib.parse import urlparse
import validators

load_dotenv()
DATABASE_URL = os.getenv('DATABASE_URL')


def get_connection():
    return psycopg2.connect(DATABASE_URL)


app = Flask(__name__)

app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/urls')
def urls_index():
    with get_connection() as conn:
        with conn.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute('SELECT * FROM urls ORDER BY id DESC;')
            urls = cursor.fetchall()
    return render_template('urls.html', urls=urls)


@app.route('/urls/<int:id>')
def urls_show(id):
    with get_connection() as conn:
        with conn.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute('SELECT * FROM urls WHERE id = %s;', (id,))
            url = cursor.fetchone()
            cursor.execute(
                """
                SELECT * FROM url_checks
                WHERE url_id = %s
                ORDER BY created_at DESC
                """,
                (id,)
            )
            checks = cursor.fetchall()
    return render_template('urls_show.html', url=url, checks=checks)


@app.route('/urls', methods=['POST'])
def urls_add():
    url = request.form.get('url')
    if not validators.url(url) or len(url) > 255:
        flash('Некорректный URL', 'danger')
        return render_template('index.html'), 422

    norm_url = urlparse(url)._replace(path='', query='', fragment='').geturl()

    with get_connection() as conn:
        with conn.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute('SELECT id FROM urls WHERE name = %s;', (norm_url,))
            row = cursor.fetchone()
            if row:
                flash('Страница уже существует', 'info')
                return redirect(url_for('urls_show', id=row["id"]))

            cursor.execute('INSERT INTO urls (name) VALUES (%s) RETURNING id;', (norm_url,))
            new_id = cursor.fetchone()[0]
            conn.commit()
            flash('Страница успешно добавлена', 'success')
            return redirect(url_for('urls_show', id=new_id))


@app.route('/urls/<int:id>/checks', methods=['POST'])
def urls_checks(id):
    with get_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute(
                """
                INSERT INTO url_checks (url_id, created_at)
                VALUES (%s, %s)
                """,
                (id, datetime.now())
            )
    flash("Проверка успешно добавлена", "success")
    return redirect(url_for("urls_show", id=id))
