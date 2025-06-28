from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

DATABASE = 'database.db'

def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def index():
    conn = get_db_connection()
    matches = conn.execute('SELECT * FROM matches ORDER BY id DESC').fetchall()
    conn.close()
    return render_template('index.html', matches=matches, active_tab='index')

@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        my_deck = request.form['my_deck']
        opponent_deck = request.form['opponent_deck']
        turn_order = request.form['turn_order']
        result = request.form['result']
        turns = request.form['turns']
        stream_num = request.form['stream_num']
        memo = request.form.get('memo', '')
        youtube_url = request.form.get('youtube_url', '')  # 追加部分

        conn = get_db_connection()
        conn.execute(
            'INSERT INTO matches (my_deck, opponent_deck, turn_order, result, turns, stream_num, memo, youtube_url) VALUES (?, ?, ?, ?, ?, ?, ?, ?)',
            (my_deck, opponent_deck, turn_order, result, turns, stream_num, memo, youtube_url)
        )
        conn.commit()
        conn.close()
        return redirect(url_for('index'))

    return render_template('add.html', active_tab='index')

@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
    conn = get_db_connection()
    match = conn.execute('SELECT * FROM matches WHERE id = ?', (id,)).fetchone()

    if request.method == 'POST':
        my_deck = request.form['my_deck']
        opponent_deck = request.form['opponent_deck']
        turn_order = request.form['turn_order']
        result = request.form['result']
        turns = request.form['turns']
        stream_num = request.form['stream_num']
        memo = request.form.get('memo', '')
        youtube_url = request.form.get('youtube_url', '')  # 追加部分

        conn.execute(
            'UPDATE matches SET my_deck=?, opponent_deck=?, turn_order=?, result=?, turns=?, stream_num=?, memo=?, youtube_url=? WHERE id=?',
            (my_deck, opponent_deck, turn_order, result, turns, stream_num, memo, youtube_url, id)
        )
        conn.commit()
        conn.close()
        return redirect(url_for('index'))

    conn.close()
    return render_template('edit.html', match=match, active_tab='index')

@app.route('/delete/<int:id>', methods=['POST'])
def delete(id):
    conn = get_db_connection()
    conn.execute('DELETE FROM matches WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    return redirect(url_for('index'))

@app.route('/stats', methods=['GET', 'POST'])
def stats():
    classes = ['全部', 'エルフ','ロイヤル','ウィッチ','ドラゴン','ナイトメア','ビショップ','ネメシス']

    my_class = request.values.get('my_class', '全部')
    opp_class = request.values.get('opp_class', '全部')

    conn = get_db_connection()
    query = 'SELECT result FROM matches WHERE 1=1 '
    params = []

    if my_class != '全部':
        query += 'AND my_deck = ? '
        params.append(my_class)
    if opp_class != '全部':
        query += 'AND opponent_deck = ? '
        params.append(opp_class)

    results = conn.execute(query, params).fetchall()
    conn.close()

    total = len(results)
    wins = sum(1 for r in results if r['result'] == '勝ち')
    win_rate = f"{(wins / total * 100):.1f}%" if total > 0 else "データなし"

    return render_template('stats.html', classes=classes, my_class=my_class, opp_class=opp_class,
                           total=total, wins=wins, win_rate=win_rate, active_tab='stats')

if __name__ == '__main__':
    app.run(debug=True)
