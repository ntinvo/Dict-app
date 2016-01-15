from flask import Flask, render_template, redirect
from flask.ext.bootstrap import Bootstrap
from flask.ext.wtf import Form
from wtforms import StringField, SubmitField
from wtforms.validators import Required
from flask.ext.sqlalchemy import SQLAlchemy
import os
from flask.ext.script import Manager
from flask.ext.migrate import Migrate, MigrateCommand


basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.config['SECRET_KEY'] = 'this password is so hard to guess'

# DB Config
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'data.sqlite')
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True

bootstrap = Bootstrap(app)
db = SQLAlchemy(app)
migrate = Migrate(app, db)

manager = Manager(app)
manager.add_command('db', MigrateCommand)

class WordForm(Form):
	word = StringField('Enter a word: ', validators=[Required()])
	submit = SubmitField('Look up')

class Word(db.Model):
	__tablename__ = 'words'
	id = db.Column(db.Integer, primary_key=True)
	word = db.Column(db.String(64), unique=True)
	meaning = db.Column(db.String(64))

@app.route('/', methods=['GET', 'POST'])
def index():
	form = WordForm()
	if form.validate_on_submit():
		word = Word.query.filter_by(word=form.word.data).first()
	return render_template('index.html', form=form)


if __name__ == '__main__':
	manager.run()