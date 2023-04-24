from flask import render_template,request,redirect, flash, url_for
from flask_login import login_user, logout_user, login_required, current_user
from app import app, login_manager,db
from .models import LoginForm, User, NewUserForm, is_safe_url




@login_manager.user_loader
def load_user(id):
   return User.query.filter(User.id == id).first()

login_manager.login_view = 'login'

@app.route('/init')
def init():   
   db.create_all()
   
   admin = User.query.filter(User.mail == 'admin@admin.com').first()
   if admin == None:
      admin = User(mail='admin@admin.com',password=User.get_hashed_password('Admin'),first_name='Name',last_name='lastname',is_admin = 1)
      db.session.add(admin)
      db.session.commit()
      
      flash("Initial config done!")
      
      return redirect(url_for('dashboard'))

      

@app.route('/login', methods=['GET','POST'])
def login():
    form = LoginForm()
    
    if form.validate_on_submit():
        user = User.query.filter(User.mail == form.mail.data).first()
        if user != None and User.verify_password(user.password, form.password.data):
            login_user(user, remember=form.remember.data)

            next = request.args.get('next')
            if next and is_safe_url(next):
                return redirect(next)
            else:
                flash(f'{form.mail.data}, you are logged in!')
                return redirect (url_for('dashboard'))
        flash('Wrong!, Try again...')

    return render_template('sign_in.html', form=form)


@app.route('/admin', methods=['GET','POST'])
def admin():
    users = User().query.all()
    form = NewUserForm()
    
    if form.validate_on_submit():
        return redirect (url_for('dashboard'))
   
    return render_template('admin.html', users=users, form=form)




@app.route('/logout')
def logout():
   logout_user()
   flash(f'You are logged out!')
   return redirect (url_for('dashboard'))
 
 
@app.route('/docs')
@login_required
def docs():
    return '<h1>Docs </h1>'
 
 
 
 
@app.route('/')
def dashboard():
     return render_template('base.html')

