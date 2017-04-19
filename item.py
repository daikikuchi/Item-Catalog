import os
from helpers import getlink
from flask import Flask, render_template, request, \
    redirect, url_for, flash, jsonify, session as login_session, Blueprint
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, backref
from database_setup import Base, Item, Category
from user import getUserInfo
from helpers import login_required

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
def itemjson(category_id, item_id):
    item = session.query(Item).filter_by(id=item_id).one()
    return jsonify(Item=item.serialize)


# show all items of a category
@item.route('/categories/<int:category_id>/items/')
def categoryitem(category_id):
    category = session.query(Category).filter_by(id=category_id).one()
    if category:
        creator = getUserInfo(category.user_id)
        items = session.query(Item).filter_by(category_id=category.id).all()
    else:
        flash("There is no such category")
        redirect(url_for('category.showcategories'))

    if 'user_id' not in login_session:
        return render_template('categoryitem.html', category=category,
                               items=items, creator=creator, user_id=None)
    else:
        return render_template('categoryitem.html', category=category,
                               items=items, creator=creator,
                               user_id=login_session['user_id'])


# create a new item
@item.route('/categories/<int:category_id>/new/', methods=['GET', 'POST'])
@login_required
def newitem(category_id):
    # if 'username' not in login_session:
    #     return redirect('/login')
    category = session.query(Category).filter_by(id=category_id).one()
    if category:
        if request.method == 'POST':

            link = getlink(request)
            if not link:
                flash("You have to add a link or upload an image")
                return redirect(url_for('item.newitem',
                                        category_id=category_id))
            user_id = login_session['user_id']
            newitem = Item(name=request.form['name'],
                           price=request.form['price'],
                           description=request.form['description'],
                           picture=link, user_id=user_id,
                           category_id=category_id)
            session.add(newitem)
            session.commit()
            flash("New item created!")
            return redirect(url_for('item.categoryitem',
                                    category_id=category_id))
        else:
            return render_template('newitem.html', category_id=category_id,
                                   category=category)

    else:
        flash("There is no such category")
        redirect(url_for('category.showcategories'))

# Edit an item
@item.route('/categories/<int:category_id>/<int:item_id>/edit/',
            methods=['GET', 'POST'])
@login_required
def edititem(category_id, item_id):
    editeditem = session.query(Item).filter_by(id=item_id).one()
    category = session.query(Category).filter_by(id=category_id).one()

    if editeditem and category:
        if request.method == 'POST':
            login_user_id = login_session['user_id']
            if editeditem.user_id != login_user_id:
                flash("You can't delete this item")
                return redirect(url_for('category.showcategories'))
            else:

                link = getlink(request)

                if request.form['name']:
                    editeditem.name = request.form['name']
                if request.form['description']:
                    editeditem.description = request.form['description']
                if request.form['price']:
                    editeditem.price = request.form['price']
                if link:
                    editeditem.picture = link

                session.add(editeditem)
                session.commit()
                flash("The item is editd!")
                return redirect(url_for('item.categoryitem',
                                        category_id=category_id))
        else:
            login_user_id = login_session['user_id']
            if editeditem.user_id != login_user_id:
                flash("You can't edit this item")
                return redirect(url_for('category.showcategories'))
            else:
                return render_template('edititem.html', category=category,
                                   item_id=item_id, item=editeditem)
    else:
        flash("There is no such item and category")
        redirect(url_for('category.showcategories'))


# Delete an item
@item.route('/categories/<int:category_id>/<int:item_id>/delete/')
@login_required
def deleteitem(category_id, item_id):
    deleteditem = session.query(Item).filter_by(id=item_id).one()
    if deleteditem:
        login_user_id = login_session['user_id']
        if deleteditem.user_id != login_user_id:
            flash("You can't delete this item")
            return redirect(url_for('category.showcategories'))
        else:
            session.delete(deleteditem)
            session.commit()
            flash("Menu item is deleted!")
            return redirect(url_for('item.categoryitem', category_id=category_id))
    else:
        flash("There is no such item")
        return redirect(url_for('item.categoryitem', category_id=category_id))

