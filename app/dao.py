from app.models import User, Book, Bill, Bill_detail, Customer
from flask_login import current_user
import hashlib
import cloudinary
import cloudinary.uploader
from app import db

def auth_user(username,password):
    password=str(hashlib.md5(password.encode('utf-8')).hexdigest())
    return User.query.filter(User.username.__eq__(username),User.password.__eq__(password)).first()

def get_user_by_ID(id):
    return User.query.get(id)

def add_user(name,username,password,avatar=None):
    password=str(hashlib.md5(password.encode('utf-8')).hexdigest())
    u=User(username=username,password=password)

    if avatar:
        res = cloudinary.uploader.upload(avatar)
        u.avatar=res.get('secure_url')
    db.session.add(u)
    db.session.commit()
    id=u.id
    c = Customer(id=id, name=name, address='dalat')
    db.session.add(c)
    db.session.commit()

def load_book(book_id=None):
    if book_id:
        return Book.query.get(book_id)
    else:
        return Book.query.all()

def save_bill(cart):
    if cart:
        b=Bill(customer_id=current_user.id,employee_id=5,status=True)
        db.session.add(b)

        for c in cart.values():
            d=Bill_detail(quantity=c['quantity'],price=c['price'],bill=b,book_id=c['id'])
            db.session.add(d)
        db.session.commit()

def get_bill(id):
    return Bill.query.get(id)

def load_bill(id=None):
    bill_details=Bill_detail.query.filter(Bill_detail.bill_id==id)
    return bill_details.all()
def get_bookname(book_id):
    book=load_book(book_id)
    return book.name







