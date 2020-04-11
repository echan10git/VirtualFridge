import os
basedir = os.path.abspath(os.path.dirname(_file_))

class Config(object):
    # ... 
    SQLALCHEMY_DATABASE_URI=os.environ.get('ACCOUNTDATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'account.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False