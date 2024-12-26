import math
from itertools import product

from click import confirm
from app import app, Login
from flask import render_template, request, redirect, session,jsonify
import dao
from flask_login import login_user, logout_user, current_user, login_required
import utils
from app.dao import load_book, save_bill, get_bill, load_bill, get_bookname, change_bill, count_book
from app.utils import stats_cart
from decorators import annonymous_user,annonymous_employee
from app.models import UserRole
import admin


@app.route("/")
def index():
    page = request.args.get('page', 1)
    cate_id = request.args.get('category_id')
    kw = request.args.get('kw')
    book = load_book(cate_id=cate_id, kw=kw, page=int(page))

    page_size = app.config["PAGE_SIZE"]
    total = count_book()

    return render_template('index.html',books=book,pages=math.ceil(total/page_size))

@app.route("/login", methods=['get','post'])
@annonymous_user

def login_process():
    if request.method.__eq__('POST'):
        username=request.form.get('username')
        password=request.form.get('password')
        u=dao.auth_user(username=username, password=password)
        if u:
            login_user(u)


            next = request.args.get('next')
            return redirect(next if next else '/')
    return render_template('login.html')

@app.route("/login-admin", methods=['post'])
def login_admin_process():
    username = request.form.get('username')
    password = request.form.get('password')
    u = dao.auth_user(username=username, password=password, role=UserRole.ADMIN)
    if u:
        login_user(u)

    return redirect('/admin')


@Login.user_loader #Nhiem vu,Tacdung ?
def get_user(user_id):
    return dao.get_user_by_ID(user_id)

@app.route("/logout")
def logout_process():
    logout_user()
    return redirect('/login')

@app.route("/register",methods=['get','post'])
@annonymous_user
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

@app.route("/api/carts/<book_id>", methods=['delete'])
def delete_cart(book_id):
    cart = session.get('cart')
    if cart and book_id in cart:
        del cart[book_id]

        session['cart'] = cart

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

@app.route('/api/order')
def order():
    cart=session.get('cart')
    # import pdb
    # pdb.set_trace()
    status=False
    try:
        id=save_bill(cart,status)
    except Exception as ex:
        print(str(ex))
        return jsonify({'status':500})
    else:
        del session['cart']

    return jsonify({'status':200,'id':id})
@app.route("/bill")
@annonymous_employee
def bill():
    id=request.args.get('bill_id')
    bill=get_bill(id)
    bill_details=load_bill(id)
    count=0
    sum=0
    d={}
    for i in bill_details:
        d[count]={
            "name":get_bookname(i.book_id),
            "price":i.price,
            "quantity":i.quantity
        }
        count=count+1
        sum+=i.price*i.quantity
    return render_template('bill_detail.html',bill_details=d,bill=bill,count=count,sum=sum)

@app.route("/api/pay_bill",methods=['post','get'])
def pay_bill():
    id=str(request.json.get('id'))
    try:
        change_bill(id)
    except:
        return jsonify({'status': 500})

    return jsonify({'status': 200})
@app.route("/create_bill")
@login_required
@annonymous_employee
def create_bill():
    bill_stats=utils.stats_cart(session.get('bill'))
    return render_template('create_bill.html',bill_stats=bill_stats)

@app.route("/api/create_bill", methods=['post'])
@login_required
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

    return jsonify(utils.stats_cart(cart=bill))
@app.route('/api/create_bill/<book_id>',methods=['put'])
def update_bill(book_id):
    bill=session.get('bill')
    print(bill)
    if bill and book_id in bill:
        bill[book_id]["quantity"]=int(request.json['quantity'])

    session['bill']=bill
    print(stats_cart(cart=bill))
    return jsonify(stats_cart(cart=bill))

@app.route('/book/<int:book_id>')
def details(book_id):
    return render_template('details.html',
                           book=dao.load_book(book_id),
                           comments=dao.load_commments(book_id))
@app.route('/api/book/<int:book_id>/comments', methods=['post'])
@login_required
def add_comment(book_id):
    content = request.json.get('content')
    c = dao.add_comment(content=content, book_id=book_id)

    return jsonify({
        "content": c.content,
        "created_date": c.created_date,
        "user": {
            "avatar": c.user.avatar
        }
    })
@app.context_processor
def common_response():
    return {
        'categories': dao.load_categories(),
        'cart_stats': utils.stats_cart(session.get('cart')),
        'bill_stats': utils.stats_cart(session.get('bill'))
    }

if __name__=='__main__':
    app.run(debug=True)
