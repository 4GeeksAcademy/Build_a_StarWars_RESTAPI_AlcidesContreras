from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()

class User(db.Model):
    __tablename__ = "user"
    user_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50),  nullable=False)
    fullname = db.Column(db.String(100),  nullable=False)
    phone= db.Column(db.String(15),  nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80),  nullable=False)
    is_active = db.Column(db.Boolean(),  nullable=False)
    relation_favorite_people = db.relationship('Favorite_people', backref='user', lazy=True)
    relation_favorite_planet = db.relationship('Favorite_planet', backref='user', lazy=True)

    def __repr__(self):
        return '<User %r>' % self.username

    def serialize(self):
        return {
            "id": self.user_id,
            "email": self.email,
            "username" : self.username,
            "Fulname" : self.fullname,
            "phone" : self.phone,
            "favorite_people" : [favorite.serialize() for favorite in self.relation_favorite_people],
            "favorite_planet" : [favorite.serialize() for favorite in self.relation_favorite_planet]
            # do not serialize the password, its a security breach
        }

class People(db.Model):
    __tablename__ = 'people'
    people_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    height = db.Column(db.String(20))
    mass = db.Column(db.Integer)
    hair_color = db.Column(db.String(10))
    eye_color = db.Column(db.String(10))
    birth_year = db.Column(db.String(10))
    gender = db.Column(db.String(10))
    homeworld = db.Column(db.Integer, db.ForeignKey('planet.planet_id'))
    url = db.Column(db.String(250))
    
    def __repr__(self):
        return '<People %r>' % self.name

    def serialize(self):
        return {
            "id": self.people_id,
            "name": self.name,
            "height": self.height,
            "mass": self.mass,
            "hair_color" : self.hair_color,
            "eye_color" : self.eye_color,
            "birth_year" : self.birth_year,
            "gender" : self.gender,
            "homeworld" : self.homeworld,
            "url" : self.url
        }



class Planet(db.Model):
    __tablename__ = 'planet'
    planet_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    diameter = db.Column(db.Integer,)
    rotation_period = db.Column(db.Integer)
    orbital_period = db.Column(db.Integer)
    gravity = db.Column(db.String(50))
    population = db.Column(db.String(50))
    climate = db.Column(db.String(50))
    terrain = db.Column(db.String(100))
    url = db.Column(db.String(100))
    relation_people = db.relationship('People', backref='planet')
    
    
    
    def __repr__(self):
        return '<Planet %r>' % self.name


    def serialize(self):
        return {
            "id": self.planet_id,
            "name": self.name,
            "diameter": self.diameter,
            "rotation_period": self.rotation_period,
            "orbital_period" : self.orbital_period,
            "gravity" : self.gravity,
            "population" : self.population,
            "climate" : self.climate,
            "terrain" : self.terrain,
            "url" : self.url
        }


class Favorite_people(db.Model):
    __tablename__ = 'favorite_people'
    id = db.Column(db.Integer, primary_key=True)
    relation_user = db.Column(db.Integer, db.ForeignKey('user.user_id'))
    relation_people = db.Column(db.Integer, db.ForeignKey('people.people_id'))
    people = db.relationship('People', backref='favorite_people', lazy=True)
    

    def __repr__(self):
        return '<Favorite %r>' % self.id
    

    def serialize(self):
        return {
            "id" : self.id,                  
            "id_people": self.relation_people,
            "people" : self.people.serialize()["name"] if self.people else None,
            
        }
    
    
class Favorite_planet(db.Model):
    __tablename__ = 'favorite_planet'
    id = db.Column(db.Integer, primary_key=True)
    relation_user = db.Column(db.Integer, db.ForeignKey('user.user_id'))
    relation_planet = db.Column(db.Integer, db.ForeignKey('planet.planet_id'))
    planet = db.relationship('Planet', backref='favorite_planet', lazy=True)


    def __repr__(self):
        return '<Favorite %r>' % self.id


    def serialize(self):
        return {
            "id" : self.id,                
            "id_planet": self.relation_planet,
            "planet" : self.planet.serialize()["name"] if self.planet else None
        }

   