#!/usr/bin/env python3


class Controller:

    def get_recommendations(self, email):
        print("The user to match on is: {}".format(email))
        return self.get_ideal()

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
