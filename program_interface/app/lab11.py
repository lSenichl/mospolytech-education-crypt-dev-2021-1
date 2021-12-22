from flask import Flask, render_template, Blueprint, redirect, url_for, flash, request
from base import alphabet, input_for_cipher_short, input_for_cipher_long, output_from_decrypted, replace_all_to, clear_text, dict
from math import gcd
from base import dict as dictionary

bp = Blueprint('lab11', __name__, url_prefix='/lab11')


@bp.route('/28', methods=['GET', 'POST'])
def lab11_28():
    if request.method == 'POST':
        Ya = request.form.get('Ya')
        a = request.form.get('a')
        n = request.form.get('n')
        ka = request.form.get('ka')
        Yb = request.form.get('Yb')
        if Ya != None:
            K = (int(a)**(int(Ya)*int(Yb)))%int(n)
            return render_template('lab11_28.html', Ya=Ya, a=a, n=n, ka=ka, Yb=Yb, K=K)
        else:
            Ya = int(a)**int(ka) % int(n)
            return render_template('lab11_28.html', Ya=Ya, a=a, n=n, ka=ka, Yb=20)
    else:
        return render_template('lab11_28.html', a=10, n=30, ka=4, Yb=20)
