# Item Catalog

This is an application that provides a list of items within a variety of categories as well as provide 
a user registration and authentication by google or facebook. Registered users will have the ability to post, edit and delete their own category and items.

## You can view it live here: http://ec2-13-54-55-135.ap-southeast-2.compute.amazonaws.com/

#### Requirements
- Python 2.7
- Facebook or Google account

#### Dependencies
- flask
- SQLAlchemy
- Httplib2

#### To run it locally:

- Clone or download this repository
- Install required modules
- run `python database_setup.py` to initialize the database.
- run `python data_populator.py` to populate the database with restaurants and menu(Optional)
- run `python main.py` to run the Flask web server. 
- Access it at http://localhost:9999/ to view Item Catalog app.



#### Project description
- CRUD
1. Website reads category and item information from a database.
2. It includes a form allowing users to add new items and correctly processes submitted forms.
3. It includes a form to edit/update a current record in the database table and correctly processes submitted forms.
4. It includes a function to delete a current record.
5. It includes functionality for image handling.

- Authentication & Authorization
1. Create, delete and update operations consider authorization status prior to execution: Without logging in, Users can not do any execution. The only user who create a category and an item can edit and delete them.
2. Login and Log out implements third-party authentication & authorization services, such as Facebook and Google.
3. There is a 'Login' and 'Logout' button/link in the project

- API Endpoints
1. This project implements a JSON endpoint that serves the same information as displayed in the HTML endpoints for an arbitrary item in the catalog.



