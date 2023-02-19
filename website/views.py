from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from .models import BudgetItem
from flask_login import login_user, login_required, logout_user, current_user
from .currencyconversionapi import exchange_rates
import json

views = Blueprint('views',__name__) 

@views.route('/', methods=['GET', 'POST']) 
def home():

    with open('./website/exchange.json') as json_file:
        data = json.load(json_file)
        countryMap = data['conversion_rates']
        countries = countryMap.keys()

    if request.method == 'POST':

        try:
            startingamount = float(request.form.get('startingamount'))
            interestrate = float(request.form.get('interestrate')) / 100
            period = float(request.form.get('period')) / 365
            elapsedtime = float(request.form.get('elapsedtime'))

            endamount = startingamount*(1 + (interestrate/period))**(period * elapsedtime)
            return render_template("home.html", baseamount = 1, countries = countries, convertedPrice=1, tocurrency = 'CAD', fromcurrency='CAD', endamount = endamount)
        except:
            pass

        try:
            baseamount = request.form.get('baseamount')
            fromcurrency = request.form.get('fromcurrency')
            tocurrency = request.form.get('tocurrency')
            exchange_rates(float(baseamount),fromcurrency,tocurrency)

            with open('conversions.json') as json_file:
                price_data = json.load(json_file)
                convertedPrice = price_data['conversion_result']

            return render_template("home.html", baseamount = baseamount, countries = countries, convertedPrice=convertedPrice, tocurrency = tocurrency, fromcurrency=fromcurrency, endamount = 0)
        except:
            pass

    return render_template("home.html", baseamount = 1, countries = countries, convertedPrice=1, tocurrency = 'CAD', fromcurrency='CAD', endamount = 0)

@views.route('/budget', methods=['GET', 'POST'])
@login_required
def budget(): 

    budgetsum = 0
    user=current_user

    if request.method == "POST":
        itemname = request.form.get('itemname')
        itemdesc = request.form.get('itemdesc')
        itemtype = request.form.get('itemtype')
        itemvalue = float(request.form.get('itemvalue'))

        if itemtype == 'Expense':
            new_item = BudgetItem(itemname=itemname, itemdesc=itemdesc, itemtype=itemtype, itemvalue=-1*itemvalue, user_id = current_user.id)
        else:
            new_item = BudgetItem(itemname=itemname, itemdesc=itemdesc, itemtype=itemtype, itemvalue=itemvalue, user_id = current_user.id)
        
        db.session.add(new_item)
        db.session.commit()

        print('Item Added')

    for item in user.budgetitem:
        budgetsum += item.itemvalue

    return render_template("budget.html", user=user, budgetsum=budgetsum)

@views.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == "POST": # sending user and password over to different page
        username = request.form.get('username')
        password = request.form.get('password')

        user = User.query.filter_by(username = username).first()
        if user:
            if check_password_hash(user.password, password):
                print('logged in')
                login_user(user, remember=True)
                return redirect(url_for('views.budget')) #redirects user to homepage
        
    return render_template("login.html") 

@views.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        user = User.query.filter_by(username = username).first()
        
        if user:
            print('already exists')
            exists = 'User Already Exists'
            return render_template('register.html', exists = exists)

        new_user = User(username = username, password = generate_password_hash(password, method='sha256')) #creates a new user object, encrypts password
        db.session.add(new_user) #tells database we want to add a new user
        db.session.commit() #tells database to commit the updates

        print('new user added')
        return redirect(url_for('views.home')) #redirects user to homepage
    else:
        exists = ''

    return render_template('register.html', exists = exists)

@views.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('views.login'))


@views.route('/delete-item', methods=['POST'])
def delete_item():
    item = json.loads(request.data)
    itemID = item['itemID']
    item = BudgetItem.query.get(itemID)
    if item:
        if item.user_id == current_user.id:
            db.session.delete(item)
            db.session.commit()
    
    return jsonify({})
