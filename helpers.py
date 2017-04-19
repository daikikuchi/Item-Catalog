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
