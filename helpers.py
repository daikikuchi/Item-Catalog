from werkzeug.utils import secure_filename
import os

# set allowed extensions for upload
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])
UPLOAD_FOLDER = './static/users'


def allowed_file(filename):
    """Check if an uploaded file has allowed filetype.
    Argument: Filename as string.
    Return: Boolean
    """
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


# make sure link is an image
def check_img_link(link):
    """Verify image link.
    Argument: Link as string. Link must end with "jpg", "jpeg", "png" or "gif".
    Return: Link or None.
    """
    allowed_img = ('jpg', 'jpeg', 'png', 'gif')
    if '.' in link:
        splitlink = link.split('.')
        if splitlink[-1].lower() in allowed_img:
            return link
    return None


# Get link/image from form
def getlink(request):
    link=''
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

    return link