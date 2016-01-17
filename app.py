from flask import Flask, render_template, redirect, flash, url_for
from flask.ext.bootstrap import Bootstrap
from flask.ext.wtf import Form
from wtforms import StringField, SubmitField
from wtforms.validators import Required
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.script import Manager
from flask.ext.migrate import Migrate, MigrateCommand
import os

basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.config['SECRET_KEY'] = 'this password is so hard to guess'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'data.sqlite')
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True

bootstrap = Bootstrap(app)
db = SQLAlchemy(app)
migrate = Migrate(app, db)

manager = Manager(app)
manager.add_command('db', MigrateCommand)

class WordForm(Form):
	word = StringField('Enter a slang: ', validators=[Required()])
	submit = SubmitField('Look up')

class Word(db.Model):
	__tablename__ = 'words'
	id = db.Column(db.Integer, primary_key=True)
	word = db.Column(db.String(64), unique=True)
	meaning = db.Column(db.String(64))

@app.route('/', methods=['GET', 'POST'])
def index():
	form = WordForm()
	found = False
	if form.validate_on_submit():
		word = Word.query.filter_by(word=form.word.data.lower().replace(" ", "")).first()
		if word is None:
			flash('Result not found. Try again!!!')
			return redirect(url_for('index', found=found))
		else:
			found = True
			return render_template('index.html', meaning=word.meaning, word=word.word, form=form, found=found)
	return render_template('index.html', form=form, found=found)

@app.errorhandler(404)
def page_not_found(e):
	return render_template('404.html'), 404

@app.errorhandler(500)
def internal_server_error(e):
	return render_template('500.html'), 500

if __name__ == '__main__':
	manager.run()