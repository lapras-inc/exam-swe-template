import datetime
import json

from flask import Flask, render_template, request, redirect, url_for, make_response, jsonify
from flask_login import LoginManager, login_required, login_user, logout_user, current_user

import models
import payment_service
from admin.create_db import init_db
from forms import UserLoginForm
from settings import DATABASE


app = Flask(__name__)
app.config['TEMPLATES_AUTO_RELOAD'] = True
app.secret_key = 'refactea'

login_manager = LoginManager()
login_manager.init_app(app)


#  init data
with app.app_context():
    init_db()


@login_manager.user_loader
def load_user(user_id):
    user_cls = models.User
    users = models.User.select().where(
        user_cls.id == user_id
    )
    if users:
        return users[0]
    return None


@login_manager.unauthorized_handler
def unauthorized_callback():
    return redirect('/login')


@app.route('/login', methods=['GET', 'POST'])
def login_view():
    form = UserLoginForm(request.form)
    error = None
    if request.method == 'POST' and form.validate():
        user_cls = models.User
        hashed_password = user_cls.get_hashed_password(form.password.data)
        users = list(user_cls.select().where(
            user_cls.name == form.username.data,
            user_cls.password == hashed_password,
        ))
        print(users)
        if users:
            login_user(users[0])
            return redirect(url_for('index_view'))
        else:
            error = 'Invalid username or password.'
    return render_template('login.html', form=form, error=error)


@app.route('/logout')
def logout_view():
    logout_user()
    return redirect(url_for('index_view'))


@app.route('/signup', methods=['GET', 'POST'])
def signup_view():
    form = UserLoginForm(request.form)
    error = None
    if request.method == 'POST':
        if form.validate():
            user_cls = models.User
            user = user_cls.create(
                name=form.username.data,
                password=form.password.data,
            )
            if user:
                print(user.name)
                login_user(user)
                return redirect(url_for('index_view'))
        else:
            error = 'Invalid username or password.'
    return render_template('signup.html', form=form, error=error)


@app.route('/')
@app.route('/index')
def index_view():
    cart_cls = models.Cart
    tea_cls = models.Tea
    if current_user.is_authenticated:
        cart, created = cart_cls.get_or_create(user=current_user.id)
        teas = cart.teas_dict
    else:
        teas = {}
    query = request.args.get('q', '')
    tea_list = []
    if query != '':
        query_str = '%{}%'.format(query)
        query_set = tea_cls.select().where(
            (tea_cls.name ** query_str) |
            (tea_cls.description ** query_str)
        ).order_by('id')
    else:
        query_set = tea_cls.select().order_by('id')
    for tea in query_set:
        tea_list.append({
            'id': tea.id,
            'name': tea.name,
            'price': tea.price,
            'stock_amount': tea.stock_amount - teas.get(str(tea.id), 0),  # 自分でカートに入れている分は除く
        })

    return render_template('index.html', tea_list=tea_list, query=query)


@app.route('/tea/<int:tea_id>')
def tea_view(tea_id):
    tea_cls = models.Tea
    tea = tea_cls.get(id=tea_id)
    return render_template('tea.html', tea=tea)


@app.route('/cart', methods=['POST', 'GET'])
@login_required
def cart_view():
    cart_cls = models.Cart
    cart, created = cart_cls.get_or_create(user=current_user.id)
    if request.method == 'POST':
        teas = cart.teas_dict
        tea_id = request.form['teaId']
        tea_amount = int(request.form['teaAmount'])
        if tea_id not in teas:
            teas[tea_id] = 0
        teas[tea_id] += tea_amount
        cart.update_teas_data(teas)
        return redirect(url_for('index_view'))
    else:
        tea_cls = models.Tea
        teas = cart.teas_dict
        cart_data = []
        for tea_id, amount in teas.items():
            cart_data.append({
                'tea': tea_cls.get(id=int(tea_id)),
                'amount': amount,
            })
        return render_template('cart.html', cart_data=cart_data)


@app.route('/change_cart', methods=['POST'])
@login_required
def change_cart_view():
    cart_cls = models.Cart
    cart = cart_cls.get(user=current_user.id)
    teas = cart.teas_dict
    tea_id = request.form['teaId']
    tea_amount = int(request.form['teaAmount'])
    teas[tea_id] = tea_amount
    if tea_amount == 0:
        del teas[tea_id]
    cart.update_teas_data(teas)
    return redirect(url_for('cart_view'))


@app.route('/checkout', methods=['GET'])
@login_required
def checkout_view():
    cart_cls = models.Cart
    cart = cart_cls.get(user=current_user.id)
    tea_cls = models.Tea
    teas = cart.teas_dict
    cart_data = []
    total_price = 0
    total_amount = 0
    for tea_id, amount in teas.items():
        tea = tea_cls.get(id=int(tea_id))
        cart_data.append({
            'tea': tea,
            'price': amount * tea.price,
        })
        total_price += amount * tea.price
        total_amount += amount

    return render_template('checkout.html', cart_data=cart_data, total_price=total_price, total_amount=total_amount)


@app.route('/buy', methods=['POST'])
@login_required
def buy_view():
    payment_type = request.form['paymentType']
    payment_info_1 = request.form['paymentInfo1']
    # optional
    payment_info_2 = request.form.get('paymentInfo2')

    cart_cls = models.Cart
    tea_cls = models.Tea
    order_cls = models.Order
    cart = cart_cls.get(user=current_user.id)
    teas = cart.teas_dict
    total_price = 0
    total_amount = 0
    with DATABASE.transaction():
        for tea_id, amount in teas.items():
            tea = tea_cls.get(id=int(tea_id))
            if tea.stock_amount < amount:
                raise Exception('not enough amount for {}'.format(tea))
            tea.stock_amount -= amount
            tea.save()
            total_price += amount * tea.price
            total_amount += amount

        total_price += total_price * 1.08 + (total_amount / 100 * 30)
        if payment_type != 'bank':
            order_cls.create(
                user=current_user.id,
                teas_dict=teas,
                payment_type=payment_type,
                payment_info=payment_info_1,
                total_price=total_price,
            )
        else:
            order_cls.create(
                user=current_user.id,
                teas_dict=teas,
                payment_type=payment_type,
                payment_info=json.dumps({
                    'branch_number': payment_info_1,
                    'account_number': payment_info_2,
                }),
                total_price=total_price,
            )
        cart.delete_instance()
    return redirect(url_for('index_view'))


@app.route('/settle', methods=['GET'])
def settle_view():
    """
    定期的にバッチから叩かれ、決済処理をまとめて行う
    :return:
    """
    order_cls = models.Order
    target_orders = order_cls.select().where(
        order_cls.status == 0
    )
    is_success = True
    for order in target_orders:
        print('target order', order)
        if order.payment_type == 'card':
            result = payment_service.card_payment(order.payment_info, order.total_price)
            if result:
                order.status = 1
                order.payment_info = None
                order.updated_at = datetime.datetime.now()
                order.save()
            else:
                is_success = False

        if order.payment_type == 'poyjp':
            result = payment_service.poyjp_payment(order.payment_info, order.total_price)
            if result:
                order.status = 1
                order.payment_info = None
                order.updated_at = datetime.datetime.now()
                order.save()
            else:
                is_success = False

        if order.payment_type == 'bank':
            payment_info = json.loads(order.payment_info)
            result = payment_service.bank_payment(payment_info['branch_number'], payment_info['account_number'], order.total_price)
            if result:
                order.status = 1
                order.payment_info = None
                order.updated_at = datetime.datetime.now()
                order.save()
            else:
                is_success = False

    return make_response(jsonify({'success': is_success}))


if __name__ == "__main__":
    app.run(port=8080)
