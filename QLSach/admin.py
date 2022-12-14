from QLSach.models import Category,Product,User,UserRole,UserEnum,Tag,ChiTietPhieuNhap,PhieuNhap,Author,QuiDinh
from QLSach import db,app,dao
from flask_admin import Admin,BaseView,expose
from flask_admin.contrib.sqla import ModelView
from flask_login import current_user
from flask import abort
from wtforms import TextAreaField
from wtforms.widgets import TextArea
from flask_login import logout_user
from flask import redirect

admin=Admin(app=app,name='QUẢN TRỊ BÁN HÀNG',template_mode='bootstrap4')


class CKTextAreaWidget(TextArea):
    def __call__(self, field, **kwargs):
        if kwargs.get('class'):
            kwargs['class'] += ' ckeditor'
        else:
            kwargs.setdefault('class', 'ckeditor')
        return super(CKTextAreaWidget, self).__call__(field, **kwargs)


class CKTextAreaField(TextAreaField):
    widget = CKTextAreaWidget()


class AuthenticatedModelView(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated and current_user.user_role == UserRole.ADMIN


class ProductView(AuthenticatedModelView):
    column_searchable_list = ['name','description']
    column_filters = ['name','price']
    can_view_details = True
    can_export = True
    column_exclude_list = ['image']
    column_labels = {
        'name':'Tên sản phẩm',
        'description':'Mô tả',
        'price':'Giá'
    }
    extra_js = ['//cdn.ckeditor.com/4.6.0/standard/ckeditor.js']
    form_overrides = {
        'description': CKTextAreaField
    }

    # def is_accessible(self):
    #     return current_user.is_authenticated


class StatsView(BaseView):
    @expose('/')
    def index(self):
        return self.render('admin/stats.html')
    def is_accessible(self):
        return current_user.is_authenticated and current_user.user_role == UserRole.ADMIN


class LogoutView(BaseView):

    @expose('/')
    def index(self):
        logout_user()

        return redirect('/admin')


class PhieuNhapView(AuthenticatedModelView):
    column_exclude_list = ['chitiets']
    form_excluded_columns = ['chitiets']


class ChiTietPhieuNhapView(AuthenticatedModelView):
    column_exclude_list = ['chitiets']
    form_excluded_columns = ['chitiets']
    # column_list = ('Sach_id','category_id','author_id','soLuong','PhieuNhap_id')

class QDView(AuthenticatedModelView):
    can_edit = True
    can_create = None
    can_delete = None



admin.add_view(AuthenticatedModelView(Category,db.session,name='Danh mục'))
admin.add_view(AuthenticatedModelView(Tag,db.session,name='Tag'))
admin.add_view(AuthenticatedModelView(Author,db.session,name='Tác giả'))
admin.add_view(ProductView(Product,db.session,name='Sản Phẩm'))
admin.add_view(PhieuNhapView(PhieuNhap,db.session,name='Phiếu Nhập'))
admin.add_view(ChiTietPhieuNhapView(ChiTietPhieuNhap,db.session,name='Chi Tiết Phiếu Nhập'))
admin.add_view(StatsView(name='Thống kê'))
admin.add_view(QDView(QuiDinh,db.session,name='Qui Định'))
admin.add_view(LogoutView(name='Đăng xuất'))