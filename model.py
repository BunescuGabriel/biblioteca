from datetime import datetime
from db import db

subs = db.Table('subs',
                db.Column('carte_id', db.Integer, db.ForeignKey('carte.id')),
                db.Column('autor_id', db.Integer, db.ForeignKey('autor.id'))
                )


class Carte(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    titlu = db.Column(db.String(300), nullable=False)
    intro = db.Column(db.String(300), nullable=False)
    # image = db.Column(db.LargeBinary, nullable=True)
    image = db.Column(db.String(255))
    date = db.Column(db.DateTime, default=datetime.utcnow())
    autor_id = db.Column(db.Integer, db.ForeignKey('autor.id'))
    autor = db.relationship('Autor', backref='carti')

    def __repr__(self):
        return '<Carte %r>' % self.id


class Autor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nume = db.Column(db.String(300), nullable=False)
    prenume = db.Column(db.String(300), nullable=True)

    def __repr__(self):
        return '<Autor %r>' % self.id
