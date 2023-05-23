from flask import render_template,request,redirect, flash, url_for
from flask_login import login_user, logout_user, login_required, current_user
from app import app, login_manager,db
from .models import LoginForm, User, is_safe_url, NewUserByAdmin, Registration
from datetime import timedelta
from os.path import exists
from flask_mail import Mail
from itsdangerous import URLSafeTimedSerializer
from config import Config


#login configuration
@login_manager.user_loader
def load_user(id):
   return User.query.filter(User.id == id).first()
login_manager.login_view = 'login'

#mail with token configuration
mail = Mail(app)
serializer = URLSafeTimedSerializer(app.config['SECRET_KEY'])





@app.route('/')
def home():
    path_exist = exists('./app/data/user.db')
    
    if path_exist == False:  
        db.create_all()

        admin = User.query.filter(User.mail == 'admin@admin.com').first()
        if admin == None:
            admin = User(mail='admin@admin.com',password=User.get_hashed_password('Admin'),first_name='Name',last_name='lastname',is_admin = 1,confirmed=1)
            db.session.add(admin)
            db.session.commit()
            
            flash("Initial config done!")
            
            return redirect (url_for('home'))
        
    return render_template('base.html')

  
@app.route('/login', methods=['GET','POST'])
def login():
    form = LoginForm() 
    
    if form.validate_on_submit():
        user = User.query.filter(User.mail == form.mail.data).first()
        
        if user != None and User.verify_password(user.password, form.password.data):
            login_user(user, remember=form.remember.data,duration=timedelta(minutes=5))

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
            new_user = User(mail = form.mail.data, password =(User.get_hashed_password(form.password.default)),first_name=form.first_name.data,last_name= form.last_name.data, is_admin= form.is_admin.data)
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
 
@app.route('/signup', methods=['GET', 'POST'])
def registration():    
    form = Registration()
    new_user = User.query.filter(User.mail == form.mail.data).first()
  
    if request.method == 'POST' and form.validate_on_submit():
        if new_user != None:
            flash('This mail exist in database.')
        
        new_user = User(mail = form.mail.data, password =User.get_hashed_password(form.password.data),first_name=form.first_name.data,last_name= form.last_name.data)
        db.session.add(new_user)
        db.session.commit()
        
        token = serializer.dumps(form.mail.data)
        confirmation_url = url_for('confirm_email', token=token, _external=True)
        
        mail.send_message(
            'Confirm Your Email',
            sender=Config.MAIL_USERNAME,
            recipients=[form.mail.data],
            body=f'Please click the following link to confirm your email: {confirmation_url}'
        )
        
        flash('New user successfully added! Check your mailbox to confirm your e-mail.')
    
            
    return render_template('sign_up.html', form=form)
        
@app.route('/confirm_mail/<token>')
def confirm_email(token):
    try:        
        mail = serializer.loads(token, max_age=300)
        user = User.query.filter(User.mail == mail).first()
        user.confirmed = 1
        db.session.add(user)
        db.session.commit()
        
        flash('E-mail successfully confirmed!')
        
        return redirect(url_for('home'))

    except:
        
        flash('Expired token...')
        return redirect(url_for('home'))
    
@app.route('/send_token/<email>')
def new_token(email):
    
    token = serializer.dumps(email)
    confirmation_url = url_for('confirm_email', token=token, _external=True)
    
    mail.send_message(
        'Confirm Your Email',
        sender=Config.MAIL_USERNAME,
        recipients=[email],
        body=f'Please click the following link to confirm your email: {confirmation_url}'
    )
    
    return redirect(url_for('home'))
    
      
        
    
  
 
@app.route('/docs')
@login_required
def docs():
    return '<h1>Docs </h1>'
 


        
    

