import os
from flask_script import Manager,Command,Option
from flask_mail import Mail,Message
from test_col_diamon import app,request,render_template,session,User,redirect,url_for
app.config['MAIL_SERVER']='smtp.sina.com'
app.config['MAIL_PORT']=25
app.config['MAIL_USE_TLS']=True
app.config['MAIL_USERNAME']=os.environ.get('mailusername')
app.config['MAIL_PASSWORD']=os.environ.get('mailpassword')
app.config['FLASKY_ADMIN']=os.environ.get('FLASKY_ADMIN')
app.config['FLASKY_MAIL_SUBJECT_PREFIX']='[Flasky]'
app.config['FLASKY_MAIL_SENDER']='Flasky Admin <huangpeng1a@sina.com>'
def send_email(to,subject,template,**kwargs):
    msg=Message(app.config['FLASKY_MAIL_SUBJECT_PREFIX']+subject,\
        sender=app.config['FLASKY_MAIL_SENDER'],recipients=[to])
    msg.body=render_template(template+'.txt',**kwargs)
    msg.html=render_template(template+'.html',**kwargs)
    print 'send mail'
    mail.send(msg)
@app.route('/user/',methods=['GET','POST'])
#@login_required
#@admin_required
def isuser_exist():
    if request.method == 'POST':
        user_record = User.query.filter_by(username=request.form['uname']).first()
        session['known'] = False
        if user_record is None:
            user_record=User(username=request.form['uname'])
            send_email(app.config['FLASKY_ADMIN'],'new user',\
                'mail/welcomenewuser',user=user_record)
        else:
            session['known'] = True
        session['name'] = request.form['uname']
        return redirect(url_for('isuser_exist'))
    return render_template('isuser_exist.html',name=session.get('name'),\
        known=session.get('known',False))   

mail=Mail(app)
manager=Manager(app)

class World(Command):
    'print World lala string'
    option_list=(
        Option('--name','-n',dest='hearttalk',default='see next century'),
    )
    def run(self,hearttalk):
        print 'world lala %s'%hearttalk

@manager.command
def hello(truth='sss'):
    'print hello jj string'
    print "hello jj %s"%truth

@manager.option('-n','--name',help='your namx',default='xiaoming')
#@manager.option('-a','--age',help='your age',default=18)
@manager.option('-a','--age',help='your age')
def printname(name,age):
    'print nihao <name> [age]'
    if age is None:
        print "nihao",name
    else:
        print "nihao %s age is %d"%(name,int(age))

@manager.command
def printbool(booler=False):
    'print nihao xxx'
    print "nihao",'yes' if booler else 'no'
if __name__ == "__main__":
    #manager.add_command('world2',World())
    manager.run({'world2':World()})
