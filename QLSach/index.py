from flask import render_template, request, redirect, session, jsonify
from QLSach import dao, app, admin, login, utils
from flask_login import login_user, logout_user, current_user, login_required
from QLSach.decorators import anonymous_user
from QLSach.models import UserRole
import cloudinary.uploader


@app.route("/")
def index():
    kw = request.args.get('keyword')
    cate_id = request.args.get('category_id')
    products = dao.load_products(cate_id, kw)
    return render_template('index.html', products=products)


@app.route('/api/cart/', methods=['post'])
def add_to_cart():
    key = app.config['CART_KEY']
    cart = session[key] if key in session else {}

    data = request.json
    id = str(data['id'])

    if id in cart:
        cart[id]['quantity'] += 1
    else:
        name = data['name']
        price = data['price']

        cart[id] = {
                       "id": id
                       , "name": name
                       , "price": price
                       , "quantity": 1
                   },
    session[key] = cart

    return jsonify(utils.cart_stats(cart))


@app.route('/cart')
def cart():
    # session['cart'] = {
    #     "1": {
    #         "id": "1"
    #         , "name": "iphone 13"
    #         , "price": 13000
    #         , "quantity": 2
    #     },
    #     "2": {
    #         "id": "2"
    #         , "name": "iphone 14"
    #         , "price": 13000
    #         , "quantity": 2
    #     }
    # }
    return render_template('cart.html')


@app.route('/products/<int:product_id>')
def details(product_id):
    p = dao.get_product_by_id(product_id)
    return render_template('details.html', product=p)


@app.route('/login-admin', methods=['post'])
def login_admin():
    username = request.form['username']
    password = request.form['password']

    user = dao.auth_user(username=username, password=password)
    # if user and user.user_role==UserRole.ADMIN:
    if user:
        login_user(user=user)

    return redirect('/admin')


@app.route('/login', methods=['get', 'post'])
@anonymous_user
def login_my_user():
    # if current_user.is_authenticated:
    #     return redirect('/')
    if request.method.__eq__('POST'):
        username = request.form['username']
        password = request.form['password']

        user = dao.auth_user(username=username, password=password)

        if user:
            login_user(user=user)

            n = request.args.get("next")
            return redirect(n if n else '/')

    return render_template('login.html')


@app.route('/logout')
def logout_my_user():
    logout_user()
    return redirect('/login')


@app.route('/api/cart/<product_id>', methods=['put'])
def update_cart(product_id):
    key = app.config['CART_KEY']
    cart = session.get(key)

    if cart and product_id in cart:
        cart[product_id]['quantity'] = int(request.json['quantity'])

    session[key] = cart

    return jsonify(utils.cart_stats(cart))

@app.context_processor
def common_attr():
    categories = dao.load_categories()

    return {
        'categories': categories,
        'cart': utils.cart_stats(session.get(app.config['CART_KEY']))
    }


@login.user_loader
def load_user(user_id):
    return dao.get_user_by_id(user_id)


@app.route('/register', methods=['get', 'post'])
def register():
    err_mess = ''
    if request.method.__eq__('POST'):
        password = request.form['password']
        confirm = request.form['confirm']
        if password.__eq__(confirm):
            avatar = ''
            if request.files:
                request.files['avatar']
                res = cloudinary.uploader.upload(request.files['avatar'])
                avatar = res['secure_url']
            try:
                dao.register(name=request.form['name'],
                             username=request.form['username'],
                             password=password,
                             avatar=avatar)

                return redirect('/login')

            except:
                err_mess = 'Hệ thống đang có lỗi! vui lòng quay lại sau!'
        else:
            err_mess = "Mật khẩu KHÔNG đúng!!!"

    return render_template('register.html', err_mess=err_mess)



@app.route('/api/pay')
@login_required
def pay():
    key = app.config['CART_KEY']
    cart = session.get(key)

    if cart:
        try:
            dao.save_receipt(cart=cart)
        except Exception as ex:
            print(str(ex))
            return jsonify({"status": 500})
        else:
            del session[key]

    return jsonify({"status": 200})

@app.route('/api/cart/<product_id>', methods=['delete'])
def delete_cart(product_id):
    key = app.config['CART_KEY']
    cart = session.get(key)

    if cart and product_id in cart:
        del cart[product_id]

    session[key] = cart

    return jsonify(utils.cart_stats(cart))


if __name__ == '__main__':
    app.run(debug=True)
