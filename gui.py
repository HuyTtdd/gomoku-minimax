from flask import (
    request,
    Flask,
    render_template,
    jsonify
)

import gomoku

app = Flask(__name__)
game = gomoku.Gomoku(0)

bot_turn = False


@app.route('/', methods=["GET", "POST"])
def index():
    return render_template('index.html', sign=game.sign)


@app.route('/play/', methods=["POST"])
def play():
    global bot_turn
    position = request.json
    position = position.split(" ")[-1].split("-")

    position = [int(x) for x in position]
    print(position)

    code, sign = game.move(position)
    bot_turn = True

    if code == 1:
        return jsonify(code=code, row=position[0], column=position[1], sign=sign)
    elif code == -1:
        return jsonify(code=code)
    elif code == 5 or code == 6:
        return jsonify(code=code, row=position[0], column=position[1], sign=sign)


@app.route("/bot/", methods=["POST"])
def bot():
    global bot_turn
    code, sign, position = game.bot()

    if bot_turn:
        bot_turn = False
        return jsonify(code=code, row=position[0], column=position[1], sign=sign)

    return jsonify()


@app.route("/refresh/", methods=["POST"])
def refresh():
    global game
    global bot_turn
    bot_turn = False
    game = gomoku.Gomoku(0)
    return ""


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
