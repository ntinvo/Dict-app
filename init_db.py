from app import db, Word

f = open('dict.txt', 'r')

for line in f:
	items = line.split(str("  -   "))
	word = Word.query.filter_by(word=items[0]).first()
	if word is None:
		word = Word(word=items[0], meaning=items[1])
		db.session.add(word)
		db.session.commit()