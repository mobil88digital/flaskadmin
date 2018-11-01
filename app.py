#!venv/bin/python
import os
from flask import Flask, url_for, redirect, render_template, request, abort
from flask_sqlalchemy import SQLAlchemy
from flask_security import Security, SQLAlchemyUserDatastore, \
    UserMixin, RoleMixin, login_required, current_user
from flask_security.utils import encrypt_password
import flask_admin
from flask_admin.contrib import sqla
from flask_admin import helpers as admin_helpers
from flask_admin import BaseView, expose


# Create Flask application
app = Flask(__name__)
app.config.from_pyfile('config.py')
db = SQLAlchemy(app)


# Define models
roles_users = db.Table(
    'roles_users',
    db.Column('user_id', db.Integer(), db.ForeignKey('user.id')),
    db.Column('role_id', db.Integer(), db.ForeignKey('role.id'))
)
brand_model = db.Table(
    'brand_model',
    db.Column('brand_id', db.Integer(), db.ForeignKey('brand.id')),
    db.Column('model_id', db.Integer(), db.ForeignKey('model.id'))
)

model_varian = db.Table(
    'model_varian',
    db.Column('model_id', db.Integer(), db.ForeignKey('model.id')),
    db.Column('varian_id', db.Integer(), db.ForeignKey('varian.id'))
)

trans_brand = db.Table(
    'trans_brand',
    db.Column('trans_id', db.Integer(), db.ForeignKey('transaksi.id')),
    db.Column('brand_id', db.Integer(), db.ForeignKey('brand.id'))
)

trans_model = db.Table(
    'trans_model',
    db.Column('trans_id', db.Integer(), db.ForeignKey('transaksi.id')),
    db.Column('model_id', db.Integer(), db.ForeignKey('model.id'))
)

trans_varian = db.Table(
    'trans_varian',
    db.Column('trans_id', db.Integer(), db.ForeignKey('transaksi.id')),
    db.Column('varian_id', db.Integer(), db.ForeignKey('varian.id'))
)

trans_cabang = db.Table(
    'trans_cabang',
    db.Column('trans_id', db.Integer(), db.ForeignKey('transaksi.id')),
    db.Column('cabang_id', db.Integer(), db.ForeignKey('cabang.id'))
)

trans_app = db.Table(
    'trans_app',
    db.Column('trans_id', db.Integer(), db.ForeignKey('transaksi.id')),
    db.Column('app_id', db.Integer(), db.ForeignKey('appraiser.id'))
)


class Role(db.Model, RoleMixin):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(80), unique=True)
    description = db.Column(db.String(255))

    def __str__(self):
        return self.name


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(255))
    last_name = db.Column(db.String(255))
    email = db.Column(db.String(255), unique=True)
    password = db.Column(db.String(255))
    active = db.Column(db.Boolean())
    confirmed_at = db.Column(db.DateTime())
    roles = db.relationship('Role', secondary=roles_users,
                            backref=db.backref('users', lazy='dynamic'))
    
    def __str__(self):
        return self.email

class Brand(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    brand = db.Column(db.String(255))
    description = db.Column(db.String(255))
    
    def __str__(self):
        return self.brand

class Model(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    model = db.Column(db.String(255))
    description = db.Column(db.String(255))
    brand = db.relationship('Brand', secondary=brand_model,
                            backref=db.backref('models'))
    # brand = db.Column(db.String(20))
    
    def __str__(self):
        return self.model

class Varian(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    varian = db.Column(db.String(255))
    description = db.Column(db.String(255))
    model = db.relationship('Model', secondary=model_varian,
                            backref=db.backref('varians', lazy='dynamic'))
    # model = db.Column(db.String(20))

# class Car(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     year = db.Column(db.Integer)
#     transmission = db.Column(db.String(2))
#     recomendation = db.Column(db.String(1))
#     brand = db.relationship('Brand', secondary=brand_car,
#                             backref=db.backref('brands', lazy='dynamic'))
#     model = db.relationship('Model', secondary=model_car,
#                             backref=db.backref('models', lazy='dynamic'))
#     varian = db.relationship('Varian', secondary=varian_car,
#                             backref=db.backref('varians', lazy='dynamic'))

class Cabang(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    kode = db.Column(db.String(50))
    description = db.Column(db.String(50))

class Appraiser(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nama = db.Column(db.String(50))

class Transaksi(db.Model):
    __tablename__ = 'transaksi'
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime)
    cabang = db.relationship('Cabang', secondary=trans_cabang,
                            backref=db.backref('Transaksi_cabang', lazy='dynamic'))
    appraiser = db.relationship('Appraiser', secondary=trans_app,
                            backref=db.backref('Transaksi_app', lazy='dynamic'))
    brand = db.relationship('Brand', secondary=trans_brand,
                            backref=db.backref('Transaksi_brand', lazy='dynamic'))
    model = db.relationship('Model', secondary=trans_model,
                            backref=db.backref('Transaksi_model', lazy='dynamic'))
    varian = db.relationship('Varian', secondary=trans_varian,
                            backref=db.backref('Transaksi_varian', lazy='dynamic'))
    year = db.Column(db.Integer)
    transmission = db.Column(db.String(2))
    nama_stnk = db.Column(db.String(50))
    nama_penjual = db.Column(db.String(50))
    nopol = db.Column(db.String(10))
    mileage = db.Column(db.Integer)
    gtf = db.Column(db.Integer)
    mrp = db.Column(db.Integer)
    total = db.Column(db.Integer)
    rekomen = db.Column(db.String(1))
    spim_id = db.Column(db.Integer)
    rm_id = db.Column(db.Integer)
    # spim = db.relationship('TransaksiSpim', secondary=trans_spim,
    #                         backref=db.backref('Transaksi_spim', lazy='dynamic'))
    # rm = db.relationship('TransaksiRm', secondary=trans_rm,
    #                         backref=db.backref('Transaksi_rm', lazy='dynamic'))

    __mapper_args__ = {
        'polymorphic_identity': 'transaksi',
    }

class TransaksiSpim(Transaksi):
    __tablename__ = 'spim'
    spim_id = db.Column(db.Integer, db.ForeignKey('transaksi.spim_id'), primary_key=True)
    spim = db.Column(db.String(1))

    __mapper_args__ = {
        'polymorphic_identity': 'spim',
    }

# Setup Flask-Security
user_datastore = SQLAlchemyUserDatastore(db, User, Role)
security = Security(app, user_datastore)


# Create customized model view class
class MyModelView(sqla.ModelView):

    def is_accessible(self):
        if not current_user.is_active or not current_user.is_authenticated:
            return False

        if current_user.has_role('superuser'):
            return True

        return False

    def _handle_view(self, name, **kwargs):
        """
        Override builtin _handle_view in order to redirect users when a view is not accessible.
        """
        if not self.is_accessible():
            if current_user.is_authenticated:
                # permission denied
                abort(403)
            else:
                # login
                return redirect(url_for('security.login', next=request.url))


    # can_edit = True
    edit_modal = True
    create_modal = True    
    can_export = True
    can_view_details = True
    details_modal = True

# Create customized model view class
class TransaksiModalView(sqla.ModelView):

    def is_accessible(self):
        if not current_user.is_active or not current_user.is_authenticated:
            return False

        if current_user.has_role('user'):
            return True

        return False

    def _handle_view(self, name, **kwargs):
        """
        Override builtin _handle_view in order to redirect users when a view is not accessible.
        """
        if not self.is_accessible():
            if current_user.is_authenticated:
                # permission denied
                abort(403)
            else:
                # login
                return redirect(url_for('security.login', next=request.url))


    # can_edit = True
    edit_modal = True
    create_modal = True
    can_export = True
    can_view_details = True
    details_modal = True

class TransaksiSpimModalView(sqla.ModelView):

    def is_accessible(self):
        if not current_user.is_active or not current_user.is_authenticated:
            return False

        if current_user.has_role('spim'):
            return True
        
        return False

    def _handle_view(self, name, **kwargs):
        """
        Override builtin _handle_view in order to redirect users when a view is not accessible.
        """
        if not self.is_accessible():
            if current_user.is_authenticated:
                # permission denied
                abort(403)
            else:
                # login
                return redirect(url_for('security.login', next=request.url))

    form_choices = {'spim':[('X','Approve'),('','Decline')]}

    # can_edit = True
    edit_modal = False
    create_modal = False
    can_export = False
    can_view_details = True
    details_modal = False

# class TransaksiRmModalView(sqla.ModelView):

#     def is_accessible(self):
#         if not current_user.is_active or not current_user.is_authenticated:
#             return False

#         if current_user.has_role('rm'):
#             return True

#         return False

#     def _handle_view(self, name, **kwargs):
#         """
#         Override builtin _handle_view in order to redirect users when a view is not accessible.
#         """
#         if not self.is_accessible():
#             if current_user.is_authenticated:
#                 # permission denied
#                 abort(403)
#             else:
#                 # login
#                 return redirect(url_for('security.login', next=request.url))

#     form_choices = {'rm':[('X','Approve'),('','Decline')]}

#     # can_edit = True
#     edit_modal = False
#     create_modal = False
#     can_export = True
#     can_view_details = True
#     details_modal = False

class UserView(MyModelView):
    column_editable_list = ['email', 'first_name', 'last_name']
    column_searchable_list = column_editable_list
    column_exclude_list = ['password']
    # form_excluded_columns = column_exclude_list
    column_details_exclude_list = column_exclude_list
    column_filters = column_editable_list

class BrandView(MyModelView):
    column_editable_list = ['brand', 'description']
    column_searchable_list = column_editable_list
    # column_exclude_list = ['password']
    # form_excluded_columns = column_exclude_list
    # column_details_exclude_list = column_exclude_list
    column_filters = ['brand']

class ModelView(MyModelView):
    column_editable_list = ['model','description']
    column_searchable_list = column_editable_list
    # column_exclude_list = ['password']
    # form_excluded_columns = column_exclude_list
    # column_details_exclude_list = column_exclude_list
    column_filters = ['model']

class VarianView(MyModelView):
    column_editable_list = ['varian']
    column_searchable_list = column_editable_list
    # column_exclude_list = ['password']
    # form_excluded_columns = column_exclude_list
    # column_details_exclude_list = column_exclude_list
    column_filters = ['varian']

class CabangView(MyModelView):
    column_editable_list = ['kode','description']
    column_searchable_list = column_editable_list
    # column_exclude_list = ['password']
    # form_excluded_columns = column_exclude_list
    # column_details_exclude_list = column_exclude_list
    column_filters = ['kode']

class AppraiserView(MyModelView):
    column_editable_list = ['nama']
    column_searchable_list = column_editable_list
    # column_exclude_list = ['password']
    # form_excluded_columns = column_exclude_list
    # column_details_exclude_list = column_exclude_list
    column_filters = ['nama']

class AdhView(TransaksiModalView):
    column_editable_list = ['date','year','nama_stnk','nama_penjual','nopol','mileage']
    column_searchable_list = column_editable_list
    column_exclude_list = ['rekomen','spim_id','gtf','mrp','total']
    form_excluded_columns = column_exclude_list
    column_details_exclude_list = column_exclude_list
    column_filters = ['date']

class SpimView(TransaksiSpimModalView):
    column_editable_list = ['spim']
    column_searchable_list = ['date']
    # column_exclude_list = ['rm_id']
    # column_exclude_list = ['date','year','nama_stnk','nama_penjual','nopol','mileage','rm']
    form_excluded_columns = column_exclude_list
    column_details_exclude_list = column_exclude_list
    column_filters = ['date']

# class RmView(TransaksiRmModalView):
#     column_editable_list = ['rm']
#     column_searchable_list = ['date']
#     # column_exclude_list = ['rm']
#     # form_excluded_columns = column_exclude_list
#     # column_details_exclude_list = column_exclude_list
#     column_filters = ['date']

class CustomView(BaseView):
    @expose('/')
    def index(self):
        return self.render('admin/custom_index.html')

# Flask views
@app.route('/')
def index():
    return render_template('index.html')

# Create admin
admin = flask_admin.Admin(
    app,
    'My Dashboard',
    base_template='my_master.html',
    template_mode='bootstrap3',
)

# Add model views
admin.add_view(MyModelView(Role, db.session, menu_icon_type='fa', menu_icon_value='fa-server', name="Roles"))
admin.add_view(UserView(User, db.session, menu_icon_type='fa', menu_icon_value='fa-users', name="Users"))
admin.add_view(BrandView(Brand, db.session, menu_icon_type='fa', menu_icon_value='fa-users', name="Brand"))
admin.add_view(ModelView(Model, db.session, menu_icon_type='fa', menu_icon_value='fa-users', name="Model"))
admin.add_view(VarianView(Varian, db.session, menu_icon_type='fa', menu_icon_value='fa-users', name="Varian"))
admin.add_view(CabangView(Cabang, db.session, menu_icon_type='fa', menu_icon_value='fa-users', name="Cabang"))
admin.add_view(AppraiserView(Appraiser, db.session, menu_icon_type='fa', menu_icon_value='fa-users', name="Appraiser"))
admin.add_view(AdhView(Transaksi, db.session, menu_icon_type='fa', menu_icon_value='fa-users', name="Transaksi"))
admin.add_view(SpimView(TransaksiSpim, db.session, menu_icon_type='fa', menu_icon_value='fa-users', name="TransaksiSpim"))
# admin.add_view(RmView(TransaksiRm, db.session, menu_icon_type='fa', menu_icon_value='fa-users', name="TransaksiRm"))
# admin.add_view(CustomView(name="Custom view", endpoint='custom', menu_icon_type='fa', menu_icon_value='fa-connectdevelop',))

# define a context processor for merging flask-admin's template context into the
# flask-security views.
@security.context_processor
def security_context_processor():
    return dict(
        admin_base_template=admin.base_template,
        admin_view=admin.index_view,
        h=admin_helpers,
        get_url=url_for
    )

def build_sample_db():
    """
    Populate a small db with some example entries.
    """

    import string
    import random

    db.drop_all()
    db.create_all()

    with app.app_context():
        user_role = Role(name='user')
        spim_role = Role(name='spim')
        super_user_role = Role(name='superuser')
        db.session.add(user_role)
        db.session.add(spim_role)
        db.session.add(super_user_role)
        db.session.commit()

        test_user = user_datastore.create_user(
            first_name='Admin',
            email='admin',
            password=encrypt_password('admin'),
            roles=[super_user_role]
        )

        user_datastore.create_user(
                first_name='Adh',
                last_name='input',
                email='adh',
                password=encrypt_password('admin'),
                roles=[user_role]
            )

        user_datastore.create_user(
                first_name='spim',
                last_name='admin',
                email='spim',
                password=encrypt_password('admin'),
                roles=[spim_role]
            )
        db.session.commit()
    return

if __name__ == '__main__':
    db.create_all()
    # Build a sample db on the fly, if one does not exist yet.
    app_dir = os.path.realpath(os.path.dirname(__file__))
    database_path = os.path.join(app_dir, app.config['DATABASE_FILE'])
    if not os.path.exists(database_path):
        build_sample_db()

    # Start app
    app.run(debug=True)