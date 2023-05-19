from flask import render_template,request,redirect, flash, url_for
from flask_login import login_user, logout_user, login_required, current_user
from app import app, login_manager,db
from .models import LoginForm, User, is_safe_url, NewUserByAdmin



@login_manager.user_loader
def load_user(id):
   return User.query.filter(User.id == id).first()

login_manager.login_view = 'login'

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
                return redirect (url_for('home'))
        flash('Wrong!, Try again...')

    return render_template('sign_in.html', form=form)


@app.route('/dashboard', methods=['GET','POST'])
def dashboard():
    users = User().query.all()
    form = NewUserByAdmin()    

    if form.validate_on_submit():
        mail = User.query.filter(User.mail == form.mail.data).first()
        if mail == None:
            new_user = User(mail = form.mail.data, password =(form.password.default),first_name=form.first_name.data,last_name= form.last_name.data, is_admin= form.is_admin.data)
            db.session.add(new_user)
            db.session.commit()    
                
            flash('New user added successfully!')
            return redirect (url_for('dashboard'))
    
        flash('User already exists')
        
    return render_template('admin.html', users=users, form=form)

@app.route('/dashboard/edit/<int:id>', methods=['POST'])
def edit_user(id):
    form = NewUserByAdmin()
    user = User.query.filter(User.id == id).first()
    
    if request.method=='POST' and user != None:        
        user.mail = form.mail.data 
        user.password = form.password.data
        user.first_name = form.first_name.data
        user.last_name = form.last_name.data
        user.is_admin = form.is_admin.data
        
        db.session.add(user)
        db.session.commit()
            
        flash('Update completed!')       
        
    
    return redirect(url_for('dashboard'))

@app.route('/dashboard/delete/<int:id>')
def delete_user(id):
    user_to_del = User.query.filter(User.id == id).first()
    db.session.delete(user_to_del)
    db.session.commit()
    
    return redirect(url_for('dashboard'))




@app.route('/logout')
def logout():
   logout_user()
   flash(f'You are logged out!')
   return redirect (url_for('home'))
 
 
@app.route('/docs')
@login_required
def docs():
    return '<h1>Docs </h1>'
 

@app.route('/')
def home():
    try:
        return render_template('base.html')
    
    except:
        db.create_all()
   
        admin = User.query.filter(User.mail == 'admin@admin.com').first()
        if admin == None:
            admin = User(mail='admin@admin.com',password=User.get_hashed_password('Admin'),first_name='Name',last_name='lastname',is_admin = 1)
            db.session.add(admin)
            db.session.commit()
            
            flash("Initial config done!")
            
            return redirect(url_for('home'))
        
    

