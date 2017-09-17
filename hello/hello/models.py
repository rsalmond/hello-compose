import os
import logging
import pickle
from flask import jsonify
from datetime import datetime as dt
from hello.errors import APIInvalidData, APIAlreadyExists
from hello.common.database import db

class ModelBase(db.Model):
    """ provide some useful common functions for db models """
    __abstract__ = True

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    def __eq__(self, other):
        """ compare class type and (non sqlalchemy) columns for equality """
        if not isinstance(other, self.__class__):
            return False

        for k, v in self.__dict__.iteritems():
            if not k.startswith('_'):
                if getattr(self, k) != getattr(other, k):
                    return False

        return True

    @classmethod
    def by_id(cls, id):
        return db.session.query(cls).filter_by(id=id).first()

    @classmethod
    def all(cls):
        return db.session.query(cls).all()

    @classmethod
    def count(cls):
        return db.session.query(cls).count()

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

class Greeting(ModelBase):
    __tablename__ = 'greetings'

    name = db.Column(db.String(255), default=None, nullable=False, unique=True)
    adjective = db.Column(db.String(255), default=None, nullable=False)
    adverb = db.Column(db.String(255), default=None, nullable=False)

    def __init__(self, name, adjective=None, adverb=None):
        self.name = name.lower()
        if adjective:
            self.adjective = adjective.lower()
        if adverb:
            self.adverb = adverb.lower()
        self.save()

    def to_json(self, status=None):
        data = {
            'Greeting': str(self),
            'Id': self.id
            }

        if status:
            data['Status'] = status

        return jsonify(data)

    def update_from_api(self, payload):
        """ update a greeting with data from an API payload """

        updated = False
        params = ('name', 'adjective', 'adverb')

        for param in params:
            value = payload.get(param)
            if value:
                if isinstance(param, basestring):
                    if getattr(self, param) != value:
                        setattr(self, param, value)
                        updated = True
                else:
                    raise APIInvalidData('Invalid data: `{param}` parameter must be a string.'.format(param=param))

        self.save()

        return updated

    @classmethod
    def all_to_json(cls):
        data = {}
        data['count'] = cls.count()
        data['greetings'] = {greeting.id: str(greeting) for greeting in cls.all()}
        return jsonify(data)

    @classmethod
    def fetch_by_name(cls, name):
        return db.session.query(cls).filter_by(name=name.lower()).first()

    @classmethod
    def create_from_api(cls, payload):
        """ process a JSON payload from the API and create a new greeting record """

        if 'name' not in payload:
            raise APIInvalidData('Invalid data: `name` parameter is required.')
            if not isinstance(payload.get('name'), basestring):
                raise APIInvalidData('Invalid data: `name` parameter must be a string.')
        else:
            name = payload.get('name').lower()
            adjective = payload.get('adjective', 'great')
            adverb = payload.get('adverb', 'really')

            if adjective:
                adjective = adjective.lower()
            if adverb:
                adverb = adverb.lower()

            current = cls.fetch_by_name(name)

            if current:
                raise APIAlreadyExists('Greeting with the name: {name} already exists. Use PUT to update.'.format(
                    name=name),
                    current.id)
            else:
                return cls(name, adjective, adverb)


    def __str__(self):
        now = dt.now()
        vowels = 'aeiouy'

        if now.hour >= 5 and now.hour < 12:
            interval = 'morning'
        elif now.hour >= 12 and now.hour < 17:
            interval = 'afternoon'
        elif now.hour >= 17 and now.hour < 21:
            interval = 'evening'
        elif (now.hour >= 21 and now.hour <= 23) or (now.hour >= 0 and now.hour < 5):
            interval = 'night'

        if True in [self.adverb.startswith(letter) for letter in vowels]:
            article = 'an'
        else:
            article = 'a'

        return 'Hey {name}, have {article} {adverb} {adjective} {interval}!'.format(
            name=self.name.capitalize(),
            article=article,
            adverb=self.adverb,
            adjective=self.adjective,
            interval=interval)
