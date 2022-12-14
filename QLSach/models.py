from sqlalchemy import Column, Integer, String, Float, ForeignKey, Boolean, Text, Enum, DateTime
from QLSach import db, app
from sqlalchemy.orm import relationship, backref
from enum import Enum as UserEnum
from flask_login import UserMixin
from datetime import datetime


class UserRole(UserEnum):
    USER = 1
    ADMIN = 2
    EMPLOYEE = 3


class BaseModel(db.Model):
    __abstract__ = True
    id = Column(Integer, primary_key=True, autoincrement=True)


class Category(BaseModel):
    __tablename__ = 'category'

    name = Column(String(50), nullable=False)
    products = relationship('Product', backref='category', lazy=True)
    chitietphieunhaps= relationship('ChiTietPhieuNhap', backref='category', lazy=True)


    def __str__(self):
        return self.name


prod_tag = db.Table('prod_tag',
                    Column('product_id', Integer, ForeignKey('product.id'), primary_key=True),
                    Column('tag_id', Integer, ForeignKey('tag.id'), primary_key=True))


class Product(BaseModel):
    name = Column(String(50), nullable=False)
    description = Column(Text)
    price = Column(Float, default=0)
    image = Column(String(100))
    active = Column(Boolean, default=True)
    category_id = Column(Integer, ForeignKey(Category.id), nullable=False)
    receipt_details = relationship('ReceiptDetails', backref='product', lazy=True)
    tags = relationship('Tag', secondary='prod_tag', lazy='subquery',
                        backref=backref('products', lazy=True))
    tacgias = relationship('Author', backref='product', lazy=True)
    chitiets = relationship('ChiTietPhieuNhap', backref='product', lazy=True)


    def __str__(self):
        return self.name


class Tag(BaseModel):
    name = Column(String(50), nullable=False, unique=True)

    def __str__(self):
        return self.name


class User(BaseModel, UserMixin):
    name = Column(String(50), nullable=False)
    username = Column(String(50), nullable=False)
    password = Column(String(50), nullable=False)
    image = Column(String(100), nullable=False)
    active = Column(Boolean, default=True)
    user_role = Column(Enum(UserRole), default=UserRole.USER)
    receipts = relationship('Receipt', backref='user', lazy=True)
    phieunhaps = relationship('PhieuNhap', backref='user', lazy=True)


    def __str__(self):
        return self.name


class Receipt(BaseModel):
    created_date = Column(DateTime, default=datetime.now())
    user_id = Column(Integer, ForeignKey(User.id), nullable=False)
    details = relationship('ReceiptDetails', backref='receipt', lazy=True)


class ReceiptDetails(BaseModel):
    quantity = Column(Integer, default=0)
    price = Column(Float, default=0)
    receipt_id = Column(Integer, ForeignKey(Receipt.id), nullable=False)
    product_id = Column(Integer, ForeignKey(Product.id), nullable=False)


class Author(BaseModel):
    name = Column(String(50), nullable=False)
    product_id = Column(Integer, ForeignKey(Product.id), nullable=False)
    chitietphieunhaps= relationship('ChiTietPhieuNhap', backref='author', lazy=True)

    def __str__(self):
        return self.name


class PhieuNhap(BaseModel):
    chitiets = relationship('ChiTietPhieuNhap', backref='PhieuNhap', lazy=True)
    name = Column(String(50), nullable=False)
    id_tk = Column(Integer, ForeignKey(User.id), nullable=False)
    def __str__(self):
        return self.name

class QuiDinh(BaseModel):
    soLuong=Column(Integer, default=0)
    thoiGian=Column(Integer, default=0)

class ChiTietPhieuNhap(BaseModel):
    Sach_id = Column(Integer, ForeignKey(Product.id), nullable=False)
    category_id = Column(Integer, ForeignKey(Category.id), nullable=False)
    author_id=  Column(Integer, ForeignKey(Author.id), nullable=False)
    soLuong= Column(Integer, default=0)
    PhieuNhap_id = Column(Integer, ForeignKey(PhieuNhap.id), nullable=False)




if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        c1=Category(name='Sách giáo khoa')
        c2=Category(name='Sách lập trình')
        c3=Category(name='Sách kinh tế')

        db.session.add_all([c1,c2,c3])
        db.session.commit()

        p1=Product(name='Sách lập trình cơ bản SQL',price=100000,description='Lập trình',image='https://m.media-amazon.com/images/I/61IvZ9eG91L._AC_UL320_.jpg',category_id=2)
        p2=Product(name='Sách lập trình cơ bản Go',price=150000,description='Lập trình',image='https://m.media-amazon.com/images/I/61UcHo8nstL._AC_UL320_.jpg',category_id=2)
        p3=Product(name='Sách Computer Science',price=800000,description='Giáo khoa',image='https://m.media-amazon.com/images/I/61fFh20AhQL._AC_UL320_.jpg',category_id=1)
        p4=Product(name='Sách dạy con làm giàu',price=1400000,description='Kinh tế',image='https://cdn-amz.woka.io/images/I/91GO13K08eL.jpg',category_id=3)

        db.session.add_all([p1,p2,p3,p4])
        db.session.commit()

        a1=Author(name='Vĩnh thần đá',product_id=1)
        db.session.add_all([a1])
        db.session.commit()



        import hashlib
        password=str(hashlib.md5('123456'.encode('utf-8')).hexdigest())
        u=User(name="Khe",username='admin',password=password,
               user_role=UserRole.ADMIN,
               image='https://m.media-amazon.com/images/I/61UcHo8nstL._AC_UL320_.jpg')

        db.session.add(u)
        db.session.commit()


        # pn1=PhieuNhap(maPN='phiếu 01',id_tk=1)
        # db.session.add_all([pn1])
        # db.session.commit()


