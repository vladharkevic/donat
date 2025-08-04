
from flask import Flask, render_template, request, redirect
from config import DONATION_TIERS
from rcon_utils import give_privilege
from mono_utils import find_payment
from invoice_utils import create_invoice

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html', tiers=DONATION_TIERS)

@app.route('/generate_invoice', methods=['POST'])
def generate_invoice():
    nickname = request.form['nickname']
    amount = int(request.form['amount'])

    link = create_invoice(nickname, amount)
    if link:
        return redirect(link)
    else:
        return "❌ Не вдалося створити рахунок", 500

@app.route('/donate', methods=['POST'])
def donate():
    nickname = request.form['nickname']
    amount = int(request.form['amount'])

    if amount in DONATION_TIERS:
        privilege = DONATION_TIERS[amount]
        if find_payment(amount):
            result = give_privilege(nickname, privilege)
            return f"✅ Оплата {amount} грн підтверджена!<br>Привілей <b>{privilege}</b> видано гравцю <b>{nickname}</b>!<br><br>RCON: {result}"
        else:
            return "❌ Платіж не знайдено. Оплати в Monobank і натисни ще раз.", 400
    else:
        return "❌ Невірна сума!", 400

if __name__ == '__main__':
    app.run(debug=True)
