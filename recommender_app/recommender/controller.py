#!/usr/bin/env python3
from recommender.model.model import Model


class Controller:

    def get_recommendations(self, email):
        model = Model()
        toReturn = model.getYourGroup(email)
        model.close()
        print("The user to match on is: {}".format(email))
        return toReturn

    def get_id(self, email):
        model = Model()
        toReturn = model.getIdFromEmail(email)
        model.close()
        return toReturn

    def get_ideal(self):
        ideal_group = [
            {'username': 'Amin Khoury',
             'email': 'amin@northeastern.edu',
             'phonenumber': '999-999-9999',
             'skills': ['Java', 'GitHub', 'Python']},
            {'username': 'Carla Brodley',
             'email': 'carla@northeastern.edu',
             'phonenumber': '888-888-8888',
             'skills': ['Java', 'GitHub', 'Python']},
            {'username': 'Ben Hescott',
             'email': 'ben@northeastern.edu',
             'phonenumber': '777-777-7777',
             'skills': ['Java', 'GitHub', 'Python']},
            {'username': 'Christo Wilson',
             'email': 'christo@northeastern.edu',
             'phonenumber': '666-666-6666',
             'skills': ['Java', 'GitHub', 'Python']}
        ]
        return ideal_group
