import os
from flask import Flask, render_template,request, \
     redirect, url_for,flash, jsonify
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, User,Item, Category
from werkzeug.utils import secure_filename
from category import category
from item import item
from authentication import authentication

app = Flask(__name__)

app.register_blueprint(category)
app.register_blueprint(item)
app.register_blueprint(authentication)

# engine = create_engine('sqlite:///itemcategorywithusers.db')
# Base.metadata.bind = engine
#
# DBSession = sessionmaker(bind=engine)
# session = DBSession()

# set allowed extensions for upload
# ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])
# UPLOAD_FOLDER = './static/users'
#
# def allowed_file(filename):
#     """Check if an uploaded file has allowed filetype.
#     Argument: Filename as string.
#     Return: Boolean
#     """
#     return '.' in filename and \
#            filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
# # make sure link is an image
# def check_img_link(link):
#     """Verify image link.
#     Argument: Link as string. Link must end with "jpg", "jpeg", "png" or "gif".
#     Return: Link or None.
#     """
#     allowed_img = ('jpg', 'jpeg', 'png', 'gif')
#     if '.' in link:
#         splitlink = link.split('.')
#         if splitlink[-1].lower() in allowed_img:
#             return link
#     return None


# JSON endpoint for items
#
# @app.route('/categories/<int:category_id>/items/JSON')
# def itemsjson(category_id):
#
#     category = session.query(Category).filter_by(id=category_id).one()
#     items = session.query(Item).filter_by(category_id=category_id).all()
#     return jsonify(Item=[i.serialize for i in items])
#
#
# @app.route('/categories/<int:category_id>/items/<int:item_id>/JSON')
# def itemjson(category_id,item_id):
#     item = session.query(Item).filter_by(id=item_id).one()
#     return jsonify(Item = item.serialize)
#
# @app.route('/categories/JSON')
# def categoryjson():
#     categories = session.query(Category).all()
#     return jsonify(categories=[c.serialize for c in categories ])




# # show all categories
# @app.route('/')
# @app.route('/categories/')
# def showcategories():
#     categories = session.query(Category).order_by(Category.name.asc()).all()
#     # if 'username' not in login_session:
#     #     return render_template('publicrestaurants.html', restaurants=restaurants)
#     # else:
#     return render_template('categories.html', c=categories)




# show all items of a category
# @app.route('/categories/<int:category_id>/items/')
# def categoryitem(category_id):
#
#     category = session.query(Category).filter_by(id=category_id).one()
#     items = session.query(Item).filter_by(category_id=category.id).all()
#     return render_template('categoryitem.html', category=category, items = items)

# # create a new category
# @app.route('/categories/new/', methods=['GET', 'POST'])
# def newcategory():
#     # if 'username' not in login_session:
#     #     return redirect('/login')
#     if request.method == 'POST':
#         newcategory = Category(name=request.form['name'], user_id=1) # After Facebook and Google log in has been introduced, Fix user_id
#         session.add(newcategory)
#         flash('New Category %s Successfully Created' % newcategory.name)
#         session.commit()
#         return redirect(url_for('showcategories'))
#     else:
#         return render_template('newcategory.html')

# # create a new item
# @app.route('/categories/<int:category_id>/new/',methods=['GET','POST'])
# def newitem(category_id):
#     category = session.query(Category).filter_by(id=category_id).one()
#     if request.method == 'POST':
#
#         link = ''
#         file = request.files['picture2']
#         if file and allowed_file(file.filename):
#             filename = secure_filename(file.filename)
#             path = os.path.join(UPLOAD_FOLDER)
#             save_path = os.path.join(path, filename)
#             file.save(save_path)
#             link = os.path.join('/',
#                                 'static',
#                                 'users',
#                                 filename)
#             # 'link' will be empty if no file was uploaded. In that case, the user
#             # should provide an image link.
#         if not link:
#             link = check_img_link(request.form.get('picture1'))
#
#
#         if not link:
#             flash("You have to add a link or upload an image")
#             return redirect(url_for('new_item'))
#
#         newitem = Item(name = request.form['name'],
#                        price=request.form['price'],
#                        description = request.form['description'],
#                        picture = link,
#                        category_id = category_id)
#         session.add(newitem)
#         session.commit()
#         flash("New item created!")
#         return redirect(url_for('categoryitem', category_id =
#         category_id))
#     else:
#         return render_template('newitem.html', category_id
#                              = category_id, category = category)
#
# # Edit an item
#
# @app.route('/categories/<int:category_id>/<int:item_id>/edit/', methods=['GET', 'POST'])
# def edititem(category_id, item_id):
#     editedITEM = session.query(Item).filter_by(id=item_id).one()
#     category = session.query(Category).filter_by(id=category_id).one()
#     if request.method == 'POST':
#         link = ''
#         file = request.files['picture2']
#         if file and allowed_file(file.filename):
#             filename = secure_filename(file.filename)
#             path = os.path.join(UPLOAD_FOLDER)
#             save_path = os.path.join(path, filename)
#             file.save(save_path)
#             link = os.path.join('/',
#                                 'static',
#                                 'users',
#                                 filename)
#             # 'link' will be empty if no file was uploaded. In that case, the user
#             # should provide an image link.
#         if not link:
#             link = check_img_link(request.form.get('picture1'))
#
#
#         if request.form['name']:
#             editedITEM.name = request.form['name']
#         if request.form['description']:
#             editedITEM.description = request.form['description']
#         if request.form['price']:
#             editedITEM.price = request.form['price']
#         if link:
#             editedITEM.picture = link
#
#         session.add(editedITEM)
#         session.commit()
#         flash("The item is editd!")
#         return redirect(url_for('categoryitem', category_id=
#             category_id))
#     else:
#         return render_template('edititem.html', category=category,
#                                 item_id=item_id, item=editedITEM)
#
#
# # Delete an item
#
# @app.route('/categories/<int:category_id>/<int:item_id>/delete/',methods=['GET', 'POST'])
# def deleteitem(category_id, item_id):
#     deletedITEM = session.query(Item).filter_by(id=item_id).one()
#     category = session.query(Category).filter_by(id=category_id).one()
#     if request.method == 'POST':
#         print deletedITEM
#         session.delete(deletedITEM)
#         session.commit()
#         flash("Menu item is deleted!")
#         return redirect(url_for('categoryitem', category_id=
#                 category_id))
#     else:
#         return render_template('deleteitem.html', category_id
#                 =category_id, item_id=item_id, item=deletedITEM,
#                                        category=category)




if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host='0.0.0.0', port=9999)