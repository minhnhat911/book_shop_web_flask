from sqlalchemy.testing.suite.test_reflection import users

from app import app, db
from sqlalchemy import Column, Integer, String, Enum, ForeignKey, Float, Boolean, Text
from flask_login import current_user
from sqlalchemy.orm import relationship
from enum import  Enum as RoleEnum
from flask_login import UserMixin

class UserRole(RoleEnum):
    ADMIN=1
    CUSTOMER=2
    EMPLOYEE=3

# class User(db.Model, UserMixin):
#     id=Column(Integer,primary_key=True, autoincrement=True)
#     name=Column(String(50),nullable=False)
#     username=Column(String(50),nullable=False, unique=True)
#     password = Column(String(50), nullable=False)
#     avatar=Column(String(100),default='https://res.cloudinary.com/dxxwcby8l/image/upload/v1647248722/r8sjly3st7estapvj19u.jpg')
#     user_role=Column(Enum(UserRole),default=UserRole.USER)



class User(db.Model, UserMixin):
    id=Column(Integer , primary_key=True,autoincrement=True )
    username=Column(String(50),nullable=False, unique=True)
    password = Column(String(50), nullable=False)
    avatar=Column(String(100),default='https://res.cloudinary.com/dxxwcby8l/image/upload/v1647248722/r8sjly3st7estapvj19u.jpg')
    user_role=Column(Enum(UserRole),default=UserRole.CUSTOMER)

class Customer(db.Model):
    id=Column(Integer, ForeignKey(User.id), primary_key=True)
    name = Column(String(50), nullable=False)
    address=Column(String(50))
    bills=relationship('Bill',backref='customer',lazy=True)

class Employee(db.Model):
    id = Column(Integer, ForeignKey(User.id))
    name = Column(String(50), nullable=False,primary_key=True)
    address = Column(String(50))
    bills = relationship('Bill', backref='employee', lazy=True)

class Author(db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False)
    books= relationship('Book', backref='author', lazy=True)


class PublishingHouse(db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False)
    books = relationship('Book', backref='publishinghouse', lazy=True)

class Category(db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False)
    category_book = relationship('Category_Book', backref='category', lazy=True)

class Book(db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False)
    image = Column(String(500), nullable=True)
    description= Column(String(500),nullable=True)
    price=Column(Float,default=0)
    author_id = Column(Integer, ForeignKey(Author.id), nullable=False)#False moi dung
    publishinghouse_id = Column(Integer, ForeignKey(PublishingHouse.id), nullable= False)#False moi dung
    bill_details = relationship('Bill_detail', backref='book', lazy=True)
    category_book=relationship('Category_Book',backref='book', lazy=True)

class Category_Book(db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True)
    category_id = Column(Integer, ForeignKey(Category.id), nullable= False)
    book_id = Column(Integer, ForeignKey(Book.id), nullable=False)


class Bill(db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True)
    status=Column(Boolean,default=False)
    bill_details= relationship('Bill_detail', backref='bill', lazy=True)
    customer_id= Column(Integer, ForeignKey(Customer.id), nullable=False)
    employee_id=Column(Integer, ForeignKey(Employee.id),nullable=False)#lay 1 id default khi khach mua hang online

class Discount(db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True)
    percent = Column(Integer)

class Bill_detail(db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True)
    book_id=Column(Integer, ForeignKey(Book.id), nullable=False)
    bill_id = Column(Integer, ForeignKey(Bill.id), nullable=False)
    quantity = Column(Integer, default=1)
    price=Column(Integer)
class Comment(db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True)
    content=Column(Text)
    customer_id= Column(Integer, ForeignKey(Customer.id), nullable=False)
    book_id=Column(Integer,ForeignKey(Book.id),nullable=False)





if __name__=='__main__':
    with app.app_context():
        db.create_all()

        import hashlib
        # u=User(username='admin',password=str(hashlib.md5('admin'.encode('utf-8')).hexdigest()),user_role=UserRole.ADMIN)
        # db.session.add(u)
        # db.session.commit()

        # a1=Author(name='Conan Doyle')
        # a2=Author(name='khong bt')
        # a3=Author(name='Nguyen Nhat Anh')
        #
        # c1=Category(name='Trinh Tham')
        # c2=Category(name='Romance')
        # c3=Category(name='Sport')
        #
        # p1=PublishingHouse(name="Nhi Dong")
        # #
        # b1=Book(name='Be Ready When the Luck Happens: A Memoir', image='https://m.media-amazon.com/images/I/81g+Hs6XF5L._SY425_.jpg',
        #         description='Here, for the first time, Ina Garten presents an intimate, entertaining, and inspiring account of her remarkable journey. Ina’s gift is to make everything look easy, yet all her accomplishments have been the result of hard work,',
        #         price=180000,
        #         author_id='1',
        #         publishinghouse_id='1')
        # b2=Book(name='The Let Them Theory',image='https://m.media-amazon.com/images/I/51wzfAWW1bL._SY445_SX342_.jpg',
        #         description='Sherlock Holmes: The Complete Novels and Stories Volume II ',
        #         price=200000,
        #         author_id='1',
        #         publishinghouse_id='1')
        # b3=Book(name='Murdle: Volume 1 (Murdle, 1)',image='https://m.media-amazon.com/images/I/51FjJsMjY1L._SY445_SX342_.jpg',
        #         description='Join Deductive Logico and investigate murders most foul in Murdle: Volume 1. The first of their kind, these humorous mini-mystery puzzles challenge you to find whodunit, how, where, and why. Examine the clues, interview the ',
        #         price=100000,
        #         author_id='1',
        #         publishinghouse_id='1')
        # b4 = Book(name='Learn A Lot While You Sit On The Pot',
        #           image='https://m.media-amazon.com/images/I/61ofAwaL8oL._SY425_.jpg',
        #           description='On average, humans will spend 92 days sitting on the toilet over their lifetime. To put this in perspective, that’s about one-third of a year in the bathroom relieving yourself. That’s where LEARN A LOT WHILE YOU SIT ON THE POT comes in',
        #           price=100000,
        #           author_id='1',
        #           publishinghouse_id='1')
        # b5 = Book(name='Interesting Facts For Curious Minds',
        #           image='https://m.media-amazon.com/images/I/51XY7fBCqDL._SY445_SX342_.jpg',
        #           description='Want to impress your friends and family with both useful, worthless but undeniably interesting facts Then Interesting Facts For Curious Minds: 1572 Random But Mind Blowing Facts About History, Science, Pop Culture',
        #           price=100000,
        #           author_id='1',
        #           publishinghouse_id='1')
        # b6 = Book(name='How To Draw Everything: 300 Drawings of Cute Stuff',
        #           image='https://m.media-amazon.com/images/I/51FaEQi313L._SX342_SY445_.jpg',
        #           description='Bring the Drawing Magic to Your Kids with this How to Draw Book with 300 Drawings!Introduce your child to the enchanting world of drawing with this easy-to-follow guide that is perfect for helping kids develop sketching, creative and coloring skills.',
        #           price=100000,
        #           author_id='1',
        #           publishinghouse_id='1')
        # b7 = Book(name='Mom, I Want to Hear Your Story)',
        #           image='https://m.media-amazon.com/images/I/41EhSBYl2JL._SY445_SX342_.jpg',
        #           description='Here, for the first time, Ina Garten presents an intimate, entertaining, and inspiring account of her remarkable journey. Ina’s gift is to make everything look easy, yet all her accomplishments have been the result of hard work,',
        #           price=180000,
        #           author_id='1',
        #           publishinghouse_id='1')
        # b8 = Book(name='Dad, I Want to Hear Your Story',
        #           image='https://m.media-amazon.com/images/I/51+ROKEYviL._SY425_.jpg',
        #           description='Here, for the first time, Ina Garten presents an intimate, entertaining, and inspiring account of her remarkable journey. Ina’s gift is to make everything look easy, yet all her accomplishments have been the result of hard work,',
        #           price=180000,
        #           author_id='1',
        #           publishinghouse_id='1')

        # db.session.add(p1)
        # db.session.add_all([a1,a2,a3])
        # db.session.add_all([b1,b2,b3,b4,b5,b7,b8])
        # db.session.commit()
        # c=Customer(diachi='LamDong')
        import hashlib

        # u=User(username='khanhnhat',password=str(hashlib.md5('123456'.encode('utf-8')).hexdigest()),user_role=UserRole.CUSTOMER)
        # # c=Customer(id=5,diachi='daLat')
        # nv = User(username='dinhky', password=str(hashlib.md5('123456'.encode('utf-8')).hexdigest()),user_role=UserRole.EMPLOYEE)
        # db.session.add(nv)
        # id=nv.id
        # e=Employee(id=5,address='lamdong',name='ky')
        # c= Customer(id=1,address='daLat',name='admin')
        # # db.session.add(c)
        # b=Bill(customer=c,employee_id=5)
        # db.session.add(b)
        # db.session.get()
        # db.session.add(e)
        # db.session.add(c)
        # guest=User(username='guest',password=str(hashlib.md5('123456'.encode('utf-8')).hexdigest()),user_role=UserRole.CUSTOMER)
        # db.session.add(guest)
        # c=Category(name='Trinh thám')
        # c1=Category(name='Lãng Mạn')
        # c2=Category(name='Hài Hước')
        # c3=Category(name='Khoa học')
        # db.session.add_all([c1,c2,c3,c])
        # db.session.commit()
        # db.session.add(c)
        # db.session.commit()
