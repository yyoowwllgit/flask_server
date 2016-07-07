import os
from flask_script import Manager,Command,Option
from threading import Thread
from flask_mail import Mail,Message
from test_col_diamon import app,request,render_template,session,User,redirect,url_for,db
app.config['MAIL_SERVER']='smtp.sina.com'
app.config['MAIL_PORT']=25
app.config['MAIL_USE_TLS']=True
app.config['MAIL_USERNAME']=os.environ.get('mailusername')
app.config['MAIL_PASSWORD']=os.environ.get('mailpassword')
app.config['FLASKY_ADMIN']=os.environ.get('FLASKY_ADMIN')
app.config['FLASKY_MAIL_SUBJECT_PREFIX']='[Flasky]'
app.config['FLASKY_MAIL_SENDER']='Flasky Admin <huangpeng1a@sina.com>'

mail=Mail(app)
manager=Manager(app)

def async_send(app,msg):
    with app.app_context():
        mail.send(msg)

def send_email(to,subject,template,**kwargs):
    msg=Message(app.config['FLASKY_MAIL_SUBJECT_PREFIX']+subject,\
        sender=app.config['FLASKY_MAIL_SENDER'],recipients=[to])
    msg.body=render_template(template+'.txt',**kwargs)
    msg.html=render_template(template+'.html',**kwargs)
    print 'send mail'
    #mail.send(msg)
    t1=Thread(target=async_send,args=(app,msg))
    t1.start()
    return t1
    

@app.route('/sendmail/',methods=['GET','POST'])
#@login_required
#@admin_required
def sendmail():
    if request.method == 'POST':
        to=request.form['emails']
        subject=request.form['subject']
        content=request.form['sendcontent']
        print repr(to)
        print repr(subject)
        print repr(content)
        #send_email2(to,subject,content)
        return redirect(url_for('sendmail'))
    return render_template('mail/sendmail.html')   


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
