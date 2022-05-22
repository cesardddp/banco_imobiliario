from peewee import (
    Model,
    SqliteDatabase,
    CharField,
    BooleanField,
    FloatField
)
    
    
db = SqliteDatabase('players.db')

class Player(Model):
    name = CharField(unique=True)
    cash = FloatField()

    class Meta:
        database = db # This model uses the "people.db" database.

class Config(Model):
    state = BooleanField(choices=[(True,"Playing"),(False,"Stoped")])

    class Meta:
        database = db # This model uses the "people.db" database.
