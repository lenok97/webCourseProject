import codecs
import sadisplay

import db

if __name__ == '__main__':
	desc = sadisplay.describe([getattr(db, attr) for attr in dir(db)])

	with codecs.open('schema.dot', 'w', encoding='utf-8') as f:
		f.write(sadisplay.dot(desc))
