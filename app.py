from flask import Flask , render_template, url_for, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, login_manager, login_user, LoginManager, login_required, logout_user
from flask_wtf import  FlaskForm
from selenium.webdriver.chrome import options
from wtforms import StringField , PasswordField, SubmitField
from wtforms.validators import InputRequired, Length, ValidationError
from flask_bcrypt import Bcrypt
import os
import csv
from selenium import webdriver
import time
import numpy as np

from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchElementException        
from flask import Flask , render_template, sessions, url_for, redirect, request, session
from flask_login import UserMixin, login_manager, login_user, LoginManager, login_required, logout_user
from flask_wtf import  FlaskForm
from wtforms import StringField , PasswordField, SubmitField
from wtforms.validators import InputRequired, Length, ValidationError






app = Flask(__name__)


bcrypt=Bcrypt(app)
db=SQLAlchemy(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY']='Thisisasecretkey'

login_manager=LoginManager()
login_manager.init_app(app)
login_manager.login_view="login"

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    id=db.Column(db.Integer, primary_key=True)
    username=db.Column(db.String(20), nullable=False,unique =True)
    password=db.Column(db.String(80), nullable=False)




       


class LoginForm(FlaskForm):
    username= StringField(validators=[InputRequired(), 
    Length( min=4, max=20)], render_kw={"placeholder":"Username"})

    password= PasswordField(validators=[InputRequired(), 
    Length( min=4, max=20)], render_kw={"placeholder":"Password"})
    
    submit= SubmitField("Login")

class RegisterForm(FlaskForm):
    username= StringField(validators=[InputRequired(), 
    Length( min=4, max=20)], render_kw={"placeholder":"Username"})

    password= PasswordField(validators=[InputRequired(), 
    Length( min=4, max=20)], render_kw={"placeholder":"Password"})
    
    submit= SubmitField("Register")

    def validate_username( self, username):
        existing_user_username =User.query.filter_by(
            username=username.data).first()
        if existing_user_username:
            raise ValidationError("That username already exists.Please selec a different one.")

class ScrapingForm(FlaskForm):
    style= StringField(validators=[InputRequired(), 
    Length( min=1, max=30)], render_kw={"placeholder":"Style"})



@app.route('/')
def home():
    return render_template('home.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    form=LoginForm()
    if form.validate_on_submit():
        user=User.query.filter_by(username=form.username.data).first()
        if user:
            if bcrypt.check_password_hash(user.password, form.password.data):
                login_user(user)
                return redirect(url_for('dashboard'))
    return render_template('login.html', form=form)



@app.route('/register', methods=['GET', 'POST'])
def register():
    form=RegisterForm()

    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data)
        new_user =User(username=form.username.data, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('login'))

    return render_template('register.html', form=form)



@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    return render_template('dashboard.html')

@app.route('/tripadvisor', methods=['GET', 'POST'])
def tripadvisor():
    
    if request.method == 'POST':
        session["style"] = request.form["style"]
        session["cities"] = request.form["cities"]
        
    
    return render_template('tripadvisor.html')


def Webscraping(restaurantttype,city,num_page):
    
    
    
    filt=3
    num_page=(int(num_page)/30)
    
    url = "https://www.google.com/"

    # if you pass the inputs in the command line
    path = '/Users/alvarodelamaza/Tripadvisor Web App/env/bin/chromedriver 2'

    # Import the webdriver
    
    
    
    myOptions=webdriver.ChromeOptions()
    myOptions.binary_location = os.getenv('$GOOGLE_CHROME_BIN')
    myOptions.add_argument('--disable-infobars')
    myOptions.add_argument('--disable-extensions')
    myOptions.add_argument('--disable-dev-shm-usage')  
    myOptions.add_argument('--profile-directory=Default')
    myOptions.add_argument('--remote-debugging-port=9222')
    myOptions.add_argument('--disable-plugins-discovery')
    #myOptions.add_argument('--headless')
    
    
    driver = webdriver.Chrome(executable_path=str(os.environ.get('CHROMEDRIVER_PATH')), options=myOptions )

    driver.get(url)

    def check_exists_by_xpath(xpath):
        try:
            driver.find_element_by_xpath(xpath)
        except NoSuchElementException:
            return False
        return True
    
    #cookiesgoo=driver.find_element_by_xpath(".//button[@id='L2AGLb']")
    #driver.execute_script("arguments[0].click();", cookiesgoo)
    #time.sleep(2)


    goo=driver.find_element_by_xpath("//input[@class='gLFyf gsfi']")
    goo.send_keys(restaurantttype+' in '+city+ '  Tripadvisor')
    goo.send_keys(Keys.ENTER)

    tripgo=driver.find_element_by_xpath(".//h3[@class='LC20lb DKV0Md']")
    driver.execute_script("arguments[0].click();", tripgo)
    time.sleep(1)



    # Accept cookies
    
    #cookies=driver.find_element_by_xpath(".//button[@id='_evidon-accept-button']")
    #driver.execute_script("arguments[0].click();", cookies)
    #time.sleep(3)
    

    
    

    #City
    
        
    
    restaurantssss=[]
    prices=[]
    baresT=[]
    prixT=[]
    mailsT=[]
    emailsT=[]
    direccionT=[]
    total=[]
    k=0
    if filt==4:
            
            barico=driver.find_elements_by_xpath("//*[@id='search-filters']/ul/li[4]/a")
            driver.execute_script("arguments[0].click();", barico)
            #barico[0].click()
            
            time.sleep(2)
    while k< num_page:
        if filt==4:
            
            restaurantss=driver.find_elements_by_xpath(".//div[@class='result-title']")
        
        else:
            restaurantss= driver.find_elements_by_xpath(".//a[@class='_15_ydu6b']")
        k=k+1
        
        item=[]
        for l in range(len(restaurantss)):
            item.append('a')
        for i in range(len(restaurantss)):
            
            clicar=restaurantss[i]
            window_before = driver.window_handles[0]
            driver.execute_script("arguments[0].click();", clicar)
            window_after = driver.window_handles[1]
            driver.switch_to.window(window_after)
            time.sleep(1)
            
            email=(driver.find_elements_by_xpath('.//div[@class="_36TL14Jn _3jdfbxG0"]'))
            
                
            try:    
                name=(driver.find_element_by_xpath('.//h1[@class="_3a1XQ88S"]')).text
            except NoSuchElementException:
                name='-'
            try:
                direccion=(driver.find_element_by_xpath('.//span[@class="_2saB_OSe"]')).text
            except NoSuchElementException:
                direccion='-'
            try:
                telefono=(driver.find_element_by_xpath('.//span[@class="_15QfMZ2L"]'))
                telefono=telefono.find_element_by_tag_name('a').text
            except NoSuchElementException:
                telefono='-'
            try:
                barrio=(driver.find_element_by_xpath('.//span[@class="_2saB_OSe _1OBMr94N"]')).text
            except NoSuchElementException:
                barrio='-'
            try:
                precio=(driver.find_elements_by_xpath('.//div[@class="_1XLfiSsv"]'))
                mix=[prc.text for prc in precio]
            except NoSuchElementException:
                precio='-'
            
            datos=['-','-']
            for m in range(len(email)):
                try:
                    emaill=email[m].find_element_by_tag_name('span') 
                except:
                    datos[m]='-'
                    break
                try:
                    emailll=emaill.find_element_by_tag_name('a')
                except NoSuchElementException:
                    datos[m]='-'
                    break
                try:
                    mailss =emailll.get_attribute('href')
                    datos[m]=mailss
                except NoSuchElementException:
                    datos[m]='-'
                    break
            datos[1]=datos[1][:-10]
            datos[1]=datos[1][7:]    
            item=[]
            item.append(name)
            item.append(direccion)
            item.append(datos[0])
            
            item.append((datos[1]))
            item.append(telefono)
            item.append(barrio)
            if len(mix)>0:
                item.append(mix[0])
            if len(mix)>1:
                item.append(mix[1])
            if len(mix)>2:
                item.append(mix[2]) 
            total.append(item)
            
            time.sleep(1)
            driver.close()
            driver.switch_to.window(window_before)
        if filt==4:
            try:

                time.sleep(1)    
                next_pagee=driver.find_element_by_xpath('.//a[@class="ui_button nav next primary "]')
                driver.execute_script("arguments[0].click();", next_pagee)
                time.sleep(2)
            except:
                pass
        else:
            try:

                time.sleep(1)    
                next_page=driver.find_element_by_xpath('.//a[@class="nav next rndBtn ui_button primary taLnk"]')
                driver.execute_script("arguments[0].click();", next_page)
                time.sleep(2)
            except:
                pass


    driver.quit()  

    
    headers = ('Restaurants','Adress', 'Web', 'Email', 'Phone', 'Area','Price','Style','Diets' ) 
    data = total
    return headers , data



@app.route('/tripadvisorweb', methods=['GET', 'POST'])
@login_required
def tripadvisorweb():
    if request.method == 'POST':
        session["style"] = request.form["style"]
        session["cities"] = request.form["cities"]
        session["hmany"] = request.form["hmany"]
    

    headers , data = Webscraping(session["style"],session["cities"],session["hmany"]) 

    
    return render_template('tripadvisorweb.html', data=data, headers=headers)

    


if __name__== '__main__':
    app.run(debug=True)
