import os
from helpers import allowed_file, check_img_link,UPLOAD_FOLDER
from flask import Flask, render_template,request, \
     redirect, url_for,flash, jsonify,session as login_session,Blueprint
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, User, Item, Category
from werkzeug.utils import secure_filename
from user import getUserInfo

item = Blueprint('item', __name__)

engine = create_engine('sqlite:///itemcategorywithusers.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

# JSON endpoint for items

@item.route('/categories/<int:category_id>/items/JSON')
def itemsjson(category_id):

    category = session.query(Category).filter_by(id=category_id).one()
    items = session.query(Item).filter_by(category_id=category_id).all()
    return jsonify(Item=[i.serialize for i in items])


@item.route('/categories/<int:category_id>/items/<int:item_id>/JSON')
def itemjson(category_id,item_id):
    item = session.query(Item).filter_by(id=item_id).one()
    return jsonify(Item = item.serialize)



# show all items of a category
@item.route('/categories/<int:category_id>/items/')
def categoryitem(category_id):

    category = session.query(Category).filter_by(id=category_id).one()
    print str(category.id)
    print "user id " + str(category.user_id)
    creator = getUserInfo(category.user_id)
    items = session.query(Item).filter_by(category_id=category.id).all()

    # if 'username' not in login_session or creator.id != login_session['user_id']:
    #     return render_template('publiccategoryitem.html', items=items,
    #                            category=category, creator=creator)
    # else:
    if 'user_id' not in login_session:
        return render_template('categoryitem.html', category=category,
                               items = items, creator=creator, user_id=None)
    else:
        print "login user id "+str(login_session['user_id'])
        return render_template('categoryitem.html', category=category,
                               items=items, creator=creator, user_id=login_session['user_id'])



# create a new item
@item.route('/categories/<int:category_id>/new/',methods=['GET','POST'])
def newitem(category_id):
    if 'username' not in login_session:
        return redirect('/login')

    category = session.query(Category).filter_by(id=category_id).one()
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


        if not link:
            flash("You have to add a link or upload an image")
            return redirect(url_for('item.newitem', category_id = category_id))
        user_id = login_session['user_id']
        newitem = Item(name = request.form['name'],
                       price=request.form['price'],
                       description = request.form['description'],
                       picture = link, user_id = user_id,
                       category_id = category_id)
        session.add(newitem)
        session.commit()
        flash("New item created!")
        return redirect(url_for('item.categoryitem', category_id =
        category_id))
    else:
        return render_template('newitem.html', category_id
                             = category_id, category = category)

# Edit an item

@item.route('/categories/<int:category_id>/<int:item_id>/edit/', methods=['GET', 'POST'])
def edititem(category_id, item_id):
    if 'username' not in login_session:
        return redirect('/login')
    editedITEM = session.query(Item).filter_by(id=item_id).one()
    category = session.query(Category).filter_by(id=category_id).one()
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
            editedITEM.name = request.form['name']
        if request.form['description']:
            editedITEM.description = request.form['description']
        if request.form['price']:
            editedITEM.price = request.form['price']
        if link:
            editedITEM.picture = link

        session.add(editedITEM)
        session.commit()
        flash("The item is editd!")
        return redirect(url_for('item.categoryitem', category_id=
            category_id))
    else:
        return render_template('edititem.html', category=category,
                                item_id=item_id, item=editedITEM)


# Delete an item

@item.route('/categories/<int:category_id>/<int:item_id>/delete/')
def deleteitem(category_id, item_id):
    if 'username' not in login_session:
        return redirect('/login')

    deletedITEM = session.query(Item).filter_by(id=item_id).one()
    category = session.query(Category).filter_by(id=category_id).one()
    session.delete(deletedITEM)
    session.commit()
    flash("Menu item is deleted!")
    return redirect(url_for('item.categoryitem', category_id=
                category_id))

