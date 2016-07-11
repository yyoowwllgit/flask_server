#encoding=utf-8
from datetime import timedelta
from flask import Flask,Blueprint,session,render_template,request,url_for,redirect,abort,flash
from flask_login import LoginManager,login_required,login_user,logout_user,UserMixin,current_user
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps
app = Flask(__name__)
#app.config['SQLALCHEMY_DATABASE_URI']='mysql://root:mysql123@localhost/diamond_agent'
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:////root/test/testgit/flask_server/mydb2.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=True
db= SQLAlchemy(app)

class User(db.Model,UserMixin):
    id=db.Column(db.Integer,primary_key=True)
    username=db.Column(db.String(80),unique=True)
    password_hash=db.Column(db.String(128))
    role_id=db.Column(db.Integer,db.ForeignKey('role.id'))
    def __init__(self,**kwargs):
        super(User,self).__init__(**kwargs)
        if self.role is None:
            if self.username=='admin':
                self.role=Role.query.filter_by(permission=0b111).first()
            if self.role is None:
                self.role=Role.query.filter_by(default=True).first()
    def can(self,permissions):
        return self.role is not None and \
            (self.role.permission&permissions) == permissions
    def is_admin(self):
        return self.can(Permission.delete_able)
    
    @property
    def password(self):
        return self.password_hash
    @password.setter
    def password(self,passwd):
        self.password_hash=generate_password_hash(passwd)
    def verity_password(self,passwd):
        return check_password_hash(self.password_hash,passwd) 
    def get_id(self):
        return unicode(self.id)
    def __repr__(self):
        return '<User>:{0}'.format(self.username)

class Data(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    itempath=db.Column(db.String(180))
    itemvalue=db.Column(db.DECIMAL(10,2))
    #itemvalue=db.Column(db.Integer)
    itemstimestamp=db.Column(db.Integer)
    category_id=db.Column(db.Integer,db.ForeignKey('category.id'))
    category=db.relationship('Category',backref=db.backref('posts',lazy='dynamic'))
    def __init__(self,itempath,itemvalue,itemstimestamp,category):
        self.itempath = itempath
        self.itemvalue = itemvalue
        self.itemstimestamp = itemstimestamp
        self.category = category
    def __repr__(self):
        return '<Data>:{0}'.format(self.itempath)
        
class Category(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    itempath=db.Column(db.String(180))
    def __init__(self,itempath):
        self.itempath=itempath
    def __repr__(self):
        return '<Category>:{0}'.format(self.itempath)
class Permission():
    read_able=0b1
    write_able=0b10
    delete_able=0b100
class Role(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    rolename=db.Column(db.String(80))
    permission=db.Column(db.Integer)
    default=db.Column(db.Boolean,default=True,index=True)
    users=db.relationship('User',backref='role',lazy='dynamic')
    @staticmethod
    def insert_roles():
        roles={
            'user':(Permission.read_able,True),
            'manager':(Permission.read_able|Permission.write_able|\
                Permission.delete_able,False),
                }
        for r in roles:
            role = Role.query.filter_by(rolename=r).first()
            if role is None:
                role=Role(rolename=r)
            role.permission=roles.get(r)[0]
            role.default=roles.get(r)[1]
            db.session.add(role)
        db.session.commit()

def permission_required(permission):
    def decoractor(fun):
        @wraps(fun)
        def decorated_function(*args,**kwargs):
            if not current_user.can(permission):
                abort(403)
            return fun(*args,**kwargs)
        return decorated_function
    return decoractor

def admin_required(fun):
    return permission_required(0b100)(fun)
#new code
app.secret_key='\xe1\x1a\xc7tP'
login_manager=LoginManager()
login_manager.session_protection='strong'
login_manager.login_view='auth.logi'
login_manager.login_message=u'请登录'
login_manager.login_message_category='info'
login_manager.remember_cookie_duration=timedelta(minutes=1)
login_manager.init_app(app)

#@login_manager.unauthorized_handler
#def unauth():
#    return u'请登录'

@login_manager.user_loader
def load_use(uid):
    user = User.query.filter_by(id=int(uid)).first()
    return user
#end new code

auth = Blueprint('auth',__name__)
#@auth.before_request
def before_request():
    return "before_request"


@auth.route('/login/',methods=['GET','POST'])
def logi():
    if request.method=='POST':
        user = User.query.filter_by(username=request.form['uname']).first()
        if user is not None:
            if user.verity_password(request.form['passwd']):
                print session
                login_user(user)
                session.permanent=True
                app.permanent_session_lifetime=timedelta(minutes=1)
                print session
                flash('congratulation %s,you login success'%'daming')
                flash('congratulation %s,you login success'%'xiaoming','error')
                flash('congratulation %s,you login success'%current_user.username,'ok')
                if request.args.get('next'): 
                    return redirect(request.args.get('next'))
                #return '{0} login page'.format(current_user.username)
                return render_template('index.html')
            return render_template('login.html')
        return render_template('login.html')
    else:
        return render_template('login.html')

@auth.route('/signup/',methods=['GET','POST'])
def signu():
    if request.method=='POST':
        user = User.query.filter_by(username=request.form['uname']).first()
        if user:
            return render_template('signup.html',tip='username is used,please use anther name')
        else:
            new_user=User()
            new_user.username=request.form['uname']
            new_user.password=request.form['passwd']
            db.session.add(new_user)
            db.session.commit()
            return 'sign up success'
    else:
        return render_template('signup.html',tip='welcome to sign up')

@auth.route('/logout/',methods=['GET','POST'])
@login_required
def logo():
    logout_user()
    return 'logout page'

@app.route('/')
@app.route('/index/')
@login_required
@admin_required
def test():
    #return 'yes,you are allowed,{0}'.format(current_user.username)
    return render_template('index.html')

@app.route('/test/')
@login_required
#@admin_required
def realtest():
    print repr(render_template('test.html'))
    return 'hehe'

@app.route('/modify_pw/',methods=['GET','POST'])
@login_required
@admin_required
def modify_pw():
    if request.method == 'GET':
        return render_template('modify_pw.html',tip=u"请设置重置用户和密码")
    if request.form['uname'] == 'admin':
        return render_template('modify_pw.html',tip=u"超级管理员不能被修改密码")
    user=User.query.filter_by(username=request.form['uname']).first()
    if not user:
        return render_template('modify_pw.html',tip=u"指定的用户不存在")
    user.password=request.form['passwd']
    db.session.add(user)
    db.session.commit()
    return 'modify success'

@app.route('/data/')
@login_required
def data():
    data_list=Data.query.all()
    return render_template('data.html',data_list=data_list)

@app.route('/insertdb/',methods=['POST'])
#@login_required
def insertdb():
    try:
        item_list = request.get_json()
        for item_dict in item_list:
                itempath = item_dict.get('path')
                if itempath is not None:
                    category = Category.query.filter_by(itempath=itempath).first()
                    if category is None:
                        category = Category(itempath)
                        db.session.add(category)
                        db.session.commit()
                    data_obj=Data(itempath,item_dict.get('value'),item_dict.get('timestamp'),category)
                    db.session.add(data_obj)
                    db.session.commit()
        return 'success insert <{0}> to db'.format(str(item_list))
    except Exception,ex:
        return ex.args
app.register_blueprint(auth,url_prefix='/auth')

if __name__=='__main__':
    app.run(host='0.0.0.0',debug=True)
