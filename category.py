import os
from helpers import allowed_file, check_img_link, UPLOAD_FOLDER
from flask import Flask, render_template, request, \
    redirect, url_for, flash, jsonify, Blueprint, session as login_session
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, User, Item, Category
from werkzeug.utils import secure_filename

category = Blueprint('category', __name__)

# app = Flask(__name__)

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
    if 'username' not in login_session:
        return render_template('publiccategories.html', c=categories)
    else:
        return render_template('categories.html', c=categories)


# create a new category
@category.route('/categories/new/', methods=['GET', 'POST'])
def newcategory():
    if 'username' not in login_session:
        return redirect('/login')
    if request.method == 'POST':
        link = ''
        file = request.files['image']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            path = os.path.join(UPLOAD_FOLDER)
            save_path = os.path.join(path, filename)
            file.save(save_path)
            link = os.path.join('/',
                                'static',
                                'users',
                                filename)
            # 'link' will be empty if no file was uploaded. In that case, the user
            # should provide an image link.
        if not link:
            link = check_img_link(request.form.get('link'))

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
        link = ''
        file = request.files['picture2']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            path = os.path.join(UPLOAD_FOLDER)
            save_path = os.path.join(path, filename)
            file.save(save_path)
            link = os.path.join('/',
                                'static',
                                'users',
                                filename)
            # 'link' will be empty if no file was uploaded. In that case, the user
            # should provide an image link.
        if not link:
            link = check_img_link(request.form.get('picture1'))

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
    category = session.query(Category).filter_by(id=category_id).one()
    category_name = category.name
    print "category name: " + category_name

    session.delete(category)
    session.commit()
    flash("Category " + category_name + " is deleted!")
    return redirect(url_for('category.showcategories'))
