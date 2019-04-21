from mysql.connector import (connection)
import config


class Model:

    def __init__(self):
        ''' Sets up basic connection and a cursor that returns each row as a dictioary'''

        self.cnx = connection.MySQLConnection(user=config.MYSQL['user'],
                                              password=config.MYSQL['password'],
                                              host=config.MYSQL['host'],
                                              database='partners')
        self.cursor = self.cnx.cursor(dictionary=True)

    def getIdFromEmail(self, email):
        ''' Consumes a user's email and returns their user_id
            email - String'''

        query = ('select user_id from user where user.email=\'{}\';'.format(email))
        self.cursor.execute(query)
        for user_id in self.cursor:
            return user_id

    def getClassGradeScore(self, id0, id1):
        ''' Calculate the weight if the two people have aligning grades or not
        id0 - int
        id1 - int '''
        grade_weight = 30

        query = ('select user_id, grade from user where user.user_id in (%s, %s) order by user_id;')
        self.cursor.execute(query, (id0, id1))
        results = self.cursor.fetchall()
        final_weight = 0

        if not (results[0]['grade'] > (results[1]['grade'] - 5) and (results[0]['grade'] < (results[1]['grade'] + 5))):
            final_weight = grade_weight
        return final_weight

    def getClassGradeGroup(self, id0, id1, id2, id3):
        total_weight = 0
        list_of_ids = [id0, id1, id2, id3]
        for i in range(0, len(list_of_ids)):
            for j in range(i + 1, len(list_of_ids)):
                total_weight += self.getClassGradeScore(i, j)
        return total_weight

    def getSkillWeight(self, id0, id1):
        ''' Compute the skillset weight between user 1 and user 2
        id0 - int
        id1 - int
        '''

        skill_weight = 25
        level_weight = 2

        # Get weight for broken skills
        query = ('''select count(*) as valuesBroken from skillset where user_id = %s and skill_id not in (select skill_id from skillset where user_id = %s);''')
        self.cursor.execute(query, (id0, id1))
        resultsBrokenSkills = self.cursor.fetchall()
        final_weight = resultsBrokenSkills[0]['valuesBroken'] * skill_weight

        # Get weight when skill level is broken
        query = ('''select
                        user1.skill_id,
                        user1.user_id as user2_id,
                        user1.value as value1,
                        user2.user_id as user2_is,
                        user2.value as value2
                    from skillset as user1
                    join skillset as user2 ON user1.skill_id = user2.skill_id
                    where user1.user_id = %s and user2.user_id = %s;''')
        self.cursor.execute(query, (id0, id1))
        resultsMatchingSkills = self.cursor.fetchall()
        for x in resultsMatchingSkills:
            if x["value1"] != x["value2"]:
                final_weight += level_weight
        return final_weight

    def getSkillGroup(self, id0, id1, id2, id3):
        ''' Compute the weight for a group of 4 people on skillset'''

        total_weight = 0
        list_of_ids = [id0, id1, id2, id3]
        for i in range(0, len(list_of_ids)):
            for j in range(i + 1, len(list_of_ids)):
                total_weight += self.getSkillWeight(i, j)
        return total_weight

    def getInterestWeight(self, id0, id1):
        ''' Compute weight for interests from a user to another'''
        interest_weight = 10

        # Get weight for broken skills
        query = ('''select count(*) as valuesBroken
                    from user_interest
                    where user_id = %s
                    and interest_id not in
                    (select interest_id from user_interest where user_id = %s);''')
        self.cursor.execute(query, (id0, id1))
        resultsBrokenSkills = self.cursor.fetchall()
        final_weight = resultsBrokenSkills[0]['valuesBroken'] * interest_weight

        return final_weight

    def getInterestGroup(self, id0, id1, id2, id3):
        ''' Compute the weight for a group of 4 people on interests'''
        total_weight = 0
        list_of_ids = [id0, id1, id2, id3]
        for i in range(0, len(list_of_ids)):
            for j in range(i + 1, len(list_of_ids)):
                total_weight += self.getInterestWeight(i, j)
        return total_weight

    def close(self):
        self.cursor.close()
        self.cnx.close()


model = Model()
print("Final weight: {}".format(model.getInterestGroup(0, 1, 2, 3)))
model.close()


# Close all connections
