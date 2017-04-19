from helpers import getlink
from flask import Flask, render_template, request, \
    redirect, url_for, flash, jsonify, Blueprint, session as login_session
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Category


category = Blueprint('category', __name__)
engine = create_engine('sqlite:///itemcategorywithusers.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()


# JSON endpoint for categories
@category.route('/categories/JSON')
def categoryjson():
    categories = session.query(Category).all()
    return jsonify(categories=[c.serialize for c in categories])


# show all categories
@category.route('/')
@category.route('/categories/')
def showcategories():
    categories = session.query(Category).order_by(Category.name.asc()).all()
    if categories:
        return render_template('categories.html', c=categories)
    else:
        flash('There is currently no category to show. '
              'Please add new category!')


# create a new category
@category.route('/categories/new/', methods=['GET', 'POST'])
def newcategory():
    if 'username' not in login_session:
        return redirect('/login')
    if request.method == 'POST':
        link = getlink(request)

        if not link:
            flash("You have to add a link or upload an image")
            return redirect(url_for('newcategory'))

        user_id = login_session['user_id']
        newcategory = Category(name=request.form['name'], user_id=user_id,
                               picture=link)
        session.add(newcategory)
        flash('New Category %s Successfully Created' % newcategory.name)
        session.commit()
        return redirect(url_for('category.showcategories'))
    else:
        return render_template('newcategory.html')


# Edit a category
@category.route('/categories/<int:category_id>/edit/', methods=['GET', 'POST'])
def editcategory(category_id):
    if 'username' not in login_session:
        return redirect('/login')
    editedcategory = session.query(Category).filter_by(id=category_id).one()
    if request.method == 'POST':
        link = getlink(request)

        if request.form['name']:
            editedcategory.name = request.form['name']
        if link:
            editedcategory.picture = link

        user_id = login_session['user_id']
        editedcategory.user_id = user_id
        session.add(editedcategory)
        session.commit()
        return redirect(url_for('category.showcategories'))
    else:
        return render_template('editcategory.html', category=editedcategory)


# Delete a category
@category.route('/categories/<int:category_id>/delete/')
def deletecategory(category_id):
    if 'username' not in login_session:
        return redirect('/login')
    cat = session.query(Category).filter_by(id=category_id).one()
    if cat:
        session.delete(cat)
        session.commit()
        flash("Category " + cat.name + " is deleted!")
    else:
        flash("There is no such category")
        redirect(url_for('category.showcategories'))

    return redirect(url_for('category.showcategories'))
