from itertools import product

from click import confirm
from app import app, Login
from flask import render_template, request, redirect, session,jsonify
import dao
from flask_login import login_user, logout_user, current_user, login_required
import utils
from app.dao import load_book, save_bill, get_bill, load_bill, get_bookname
from app.utils import stats_cart, stats_bill
from decorators import annonymous_user


@app.route("/")
def index():
    books=load_book()
    return render_template('index.html',books=books)

@app.route("/login", methods=['get','post'])
@annonymous_user

def login_process():
    if request.method.__eq__('POST'):
        username=request.form.get('username')
        password=request.form.get('password')
        u=dao.auth_user(username=username, password=password)
        if u:
            login_user(u)
            return redirect('/')
    return render_template('login.html')

@Login.user_loader #Nhiem vu,Tacdung ?
def get_user(user_id):
    return dao.get_user_by_ID(user_id)

@app.route("/logout")
def logout_process():
    logout_user()
    return redirect('/login')

@app.route("/register",methods=['get','post'])
def register_process():
    err_msg=None
    if request.method.__eq__('POST'):
        password=request.form.get('password')
        confirm=request.form.get('confirm')
        if password.__eq__(confirm):
            data=request.form.copy()
            del data['confirm']
            avatar=request.files.get('avatar')
            dao.add_user(avatar=avatar, **data)
            return redirect('/login')
        else:
            err_msg='Mat khau khong khop!'
    return render_template('register.html',err_msg=err_msg)

@app.route("/api/carts", methods=['post'])
def add_to_cart():
    cart=session.get('cart')
    if not cart:
        cart={}
    id=str(request.json.get("id"))
    name=request.json.get("name")
    price=request.json.get("price")

    if id in cart:
        cart[id]["quantity"]+=1
    else:
        cart[id]={
            "id": id,
            "name":name,
            "price":price,
            "quantity":1
        }
    session["cart"]=cart
    print(cart)

    return jsonify(utils.stats_cart(cart))

@app.route("/cart")
def cart():
    cart_stats=utils.stats_cart(session.get('cart'))
    return render_template("cart.html",cart_stats=cart_stats)

@app.route('/api/cart/<product_id>', methods=['put'])
def update_cart(product_id):
    cart=session.get('cart')

    if cart and product_id in cart:
        cart[product_id]["quantity"]=int(request.json['quantity'])

    session['cart']=cart
    return jsonify(utils.stats_cart(cart))
@app.route('/api/pay')
def pay():
    cart=session.get('cart')
    # import pdb
    # pdb.set_trace()
    try:
        save_bill(cart)
    except Exception as ex:
        print(str(ex))
        return jsonify({'status':500})
    else:
        del session['cart']

    return jsonify({'status':200})
@app.route("/bill")
def bill():
    id=request.args.get('bill_id')
    bill=get_bill(id)
    bill_details=load_bill(id)
    count=0
    d={}
    for i in bill_details:
        d[count]={
            "name":get_bookname(i.book_id),
            "price":i.price,
            "quantity":i.quantity
        }
        count=count+1
    return render_template('bill_detail.html',bill_details=d,bill=bill)

@app.route("/api/pay_bill",methods=['put'])
def pay_bill():
    # id=request.args.get(3)
    bill=get_bill(3)
    try:
        bill.status=True
    except:
        return jsonify({'status': 500})

    return jsonify({'status': 200})
@app.route("/create_bill")
# @annonymous_employee
def create_bill():
    bill_stats=utils.stats_bill(session.get('bill'))
    return render_template('create_bill.html',bill_stats=bill_stats)

@app.route("/api/create_bill", methods=['post'])
def add_to_bill():
    bill=session.get('bill')
    try:
        if not bill:
            bill={}
        id=str(request.json.get("id"))
        if id in bill:
            bill[id]['quantity']+=1
        else:
            book=load_book(id)
            bill[id]={
                "id": id,
                "name":book.name,
                "price":book.price,
                "quantity":1
            }
    except:
        return jsonify({'status': 500})
    session["bill"]=bill
    print(bill)

    return jsonify(utils.stats_bill(bill=bill))
@app.route("/api/create_bill/<book_id>",methods=['put'])
def update_bill(book_id):
    bill=session.get('bill')

    if bill and book_id in bill:
        bill[book_id]["quantity"]=int(request.json['quantity'])

    session['bill']=bill
    return jsonify(utils.stats_bill(bill))

@app.context_processor
def common_response():
    return {
        'categories': dao.load_book(),
        'cart_stats': utils.stats_cart(session.get('cart')),
        'bill_stats': utils.stats_bill(session.get('bill'))
    }

if __name__=='__main__':
    app.run(debug=True)
