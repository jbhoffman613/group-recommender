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
        grade_weight = 31

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
                total_weight += self.getClassGradeScore(list_of_ids[i], list_of_ids[j])
        return total_weight

    def getSkillWeight(self, id0, id1):
        ''' Compute the skillset weight between user 1 and user 2
        id0 - int
        id1 - int
        '''

        skill_weight = 27
        level_weight = 3

        # Get weight for broken skills
        query = ('''select count(*) as valuesBroken from skillset where user_id = %s and skill_id not in (select skill_id from skillset where user_id = %s);''')
        self.cursor.execute(query, (id0, id1))
        resultsBrokenSkills = self.cursor.fetchall()
        final_weight = resultsBrokenSkills[0]['valuesBroken'] * skill_weight

        # Get weight when skill level is broken
        query = ('''select count(*) as valuesBroken from skillset as user1
                        join skillset as user2 ON user1.skill_id = user2.skill_id
                    where user1.user_id = %s and user2.user_id = %s and user1.value != user2.value;''')
        self.cursor.execute(query, (id0, id1))
        resultsMatchingSkills = self.cursor.fetchall()
        final_weight += resultsMatchingSkills[0]['valuesBroken'] * level_weight
        print(final_weight)
        return final_weight

    def getSkillGroup(self, id0, id1, id2, id3):
        ''' Compute the weight for a group of 4 people on skillset'''

        total_weight = 0
        list_of_ids = [id0, id1, id2, id3]
        for i in range(0, len(list_of_ids)):
            for j in range(0, len(list_of_ids)):
                if i != j:
                    total_weight += self.getSkillWeight(list_of_ids[i], list_of_ids[j])
        return total_weight

    def getInterestWeight(self, id0, id1):
        ''' Compute weight for interests from a user to another'''
        interest_weight = 13

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
            for j in range(0, len(list_of_ids)):
                if i != j:
                    total_weight += self.getInterestWeight(list_of_ids[i], list_of_ids[j])
        return total_weight

    def getAvailabilityWeight(self, id0, id1):
        ''' Computes weight for user 1 in the context of user 2'''
        availability_weight = 3
        # Get weight for broken availability
        query = ('''select (select count(*) from availability
                    where user_id = %s) -
                    (select count(*)
                    from availability as user1
                    join availability as user2 on user1.day = user2.day and user1.start = user2.start
                    where user1.user_id = %s and user2.user_id = %s) as valuesBroken;''')
        self.cursor.execute(query, (id0, id0, id1))
        resultsBrokenSkills = self.cursor.fetchall()
        final_weight = resultsBrokenSkills[0]['valuesBroken'] * availability_weight
        return final_weight

        return 0

    def getAvailabilityGroup(self, id0, id1, id2, id3):
        ''' Compute the weight for a group of 4 people on availability'''
        total_weight = 0
        list_of_ids = [id0, id1, id2, id3]
        for i in range(0, len(list_of_ids)):
            for j in range(0, len(list_of_ids)):
                if i != j:
                    total_weight += self.getAvailabilityWeight(list_of_ids[i], list_of_ids[j])
        return total_weight
        return 0

    def close(self):
        self.cursor.close()
        self.cnx.close()


model = Model()
print("Final weight: {}".format(model.getAvailabilityGroup(3, 4, 1, 17)))
model.close()


# Close all connections
