from sqlalchemy import Column,Integer,String,Float,ForeignKey,Boolean,Text,Enum
from QLSach import db,app
from sqlalchemy.orm import relationship
from enum import Enum as UserEnum
from flask_login import UserMixin

class UserRole(UserEnum):
    USER=1
    ADMIN=2


class BaseModel(db.Model):
    __abstract__=True
    id=Column(Integer,primary_key=True,autoincrement=True)


class Category(BaseModel):
    __tablename__='category'

    name=Column(String(50),nullable=False)
    products=relationship('Product',backref='category',lazy=True)

    def __str__(self):
        return self.name

class Product(BaseModel):
    name = Column(String(50),nullable=False)
    description=Column(Text)
    price=Column(Float,default=0)
    image=Column(String(100))
    active=Column(Boolean,default=True)
    category_id=Column(Integer,ForeignKey(Category.id),nullable=False)



class User(BaseModel,UserMixin):
    name=Column(String(50),nullable=False)
    username=Column(String(50),nullable=False)
    password=Column(String(50),nullable=False)
    image=Column(String(100),nullable=False)
    active=Column(Boolean,default=True)
    user_role=Column(Enum(UserRole),default=UserRole.USER)

    def __str__(self):
        return self.name


if __name__=='__main__':
    with app.app_context():
        # c1=Category(name='Sách giáo khoa')
        # c2=Category(name='Sách lập trình')
        # c3=Category(name='Sách kinh tế')
        #
        # db.session.add_all([c1,c2,c3])
        # db.session.commit()

        # p1=Product(name='Sách lập trình cơ bản SQL',price=100000,description='Lập trình',image='https://m.media-amazon.com/images/I/61IvZ9eG91L._AC_UL320_.jpg',category_id=2)
        # p2=Product(name='Sách lập trình cơ bản Go',price=150000,description='Lập trình',image='https://m.media-amazon.com/images/I/61UcHo8nstL._AC_UL320_.jpg',category_id=2)
        # p3=Product(name='Sách Computer Science',price=800000,description='Giáo khoa',image='https://m.media-amazon.com/images/I/61fFh20AhQL._AC_UL320_.jpg',category_id=1)
        # p4=Product(name='Sách dạy con làm giàu',price=1400000,description='Kinh tế',image='https://cdn-amz.woka.io/images/I/91GO13K08eL.jpg',category_id=3)
        #
        # db.session.add_all([p1,p2,p3,p4])
        # db.session.commit()

        import hashlib
        password=str(hashlib.md5('123456'.encode('utf-8')).hexdigest())
        u=User(name="Khe",username='admin',password=password,
               user_role=UserRole.ADMIN,
               image='https://m.media-amazon.com/images/I/61UcHo8nstL._AC_UL320_.jpg')

        db.session.add(u)
        db.session.commit()

        db.create_all()