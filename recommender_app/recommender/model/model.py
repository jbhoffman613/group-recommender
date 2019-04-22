from mysql.connector import (connection)
from recommender.model.config_flask import Config


class Model:

    def __init__(self):
        config = Config()
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

        if (len(results) > 1) and not (results[0]['grade'] > (results[1]['grade'] - 5) and (results[0]['grade'] < (results[1]['grade'] + 5))):
            return grade_weight
        return 0

    def getClassGradeGroup(self, id0, id1, id2, id3):
        total_weight = 0
        list_of_ids = [id0, id1, id2, id3]
        for i in range(0, len(list_of_ids)):
            for j in range(0, len(list_of_ids)):
                if i != j:
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

    def getAvailabilityGroup(self, id0, id1, id2, id3):
        ''' Compute the weight for a group of 4 people on availability'''
        total_weight = 0
        list_of_ids = [id0, id1, id2, id3]
        for i in range(0, len(list_of_ids)):
            for j in range(0, len(list_of_ids)):
                if i != j:
                    total_weight += self.getAvailabilityWeight(list_of_ids[i], list_of_ids[j])
        return total_weight

    def getPrefWeight(self, id0, id1):
        ''' Return the weight if user 1 is not a preference of user 0.
            This only matters if user 0 has at least one preferred partner. '''
        pref_weight = 79
        query = ('''select * from user_preference where user_preference.user_id={};'''.format(id0))
        self.cursor.execute(query)
        resultsBrokenSkills = self.cursor.fetchall()
        if len(resultsBrokenSkills) == 1 and resultsBrokenSkills[0]['user_prefers'] != id1:
            return pref_weight
        elif len(resultsBrokenSkills) == 2 and (resultsBrokenSkills[0]['user_prefers'] != id1 and resultsBrokenSkills[1]['user_prefers'] != id1):
            return pref_weight
        return 0

    def getPrefGroup(self, id0, id1, id2, id3):
        ''' Compute all weight for a proposed group of 4 based on their preferences '''
        total_weight = 0
        list_of_ids = [id0, id1, id2, id3]
        for i in range(0, len(list_of_ids)):
            for j in range(0, len(list_of_ids)):
                if i != j:
                    total_weight += self.getPrefWeight(list_of_ids[i], list_of_ids[j])
        return total_weight

    def getYearfWeight(self, id0, id1):
        ''' Return a weight if the two individuals are more than a year apart '''
        year_weight = 14
        query = ('''select ABS((select year from user where user_id = %s) - (select year from user where user_id = %s)) as diff_year;''')
        self.cursor.execute(query, (id0, id1))
        resultsBrokenSkills = self.cursor.fetchall()
        if resultsBrokenSkills[0]['diff_year'] > 1:
            return year_weight
        return 0

    def getYearGroup(self, id0, id1, id2, id3):
        ''' Return the weight for a proposed group based on their difference in year'''
        total_weight = 0
        list_of_ids = [id0, id1, id2, id3]
        for i in range(0, len(list_of_ids)):
            for j in range(0, len(list_of_ids)):
                if i != j:
                    total_weight += self.getYearfWeight(list_of_ids[i], list_of_ids[j])
        return total_weight

    def getTotalScoreForGroup(self, id0, id1, id2, i3):
        ''' Consume four user IDs and compute the total weight for that proposed group '''
        return (self.getClassGradeGroup(id0, id1, id2, i3)
                + self.getSkillGroup(id0, id1, id2, i3)
                + self.getInterestGroup(id0, id1, id2, i3)
                + self.getAvailabilityGroup(id0, id1, id2, i3)
                + self.getPrefGroup(id0, id1, id2, i3)
                + self.getYearGroup(id0, id1, id2, i3))

    def findIdealGroup(self, searcher):
        ''' Computes the ideal group for a given searcher and returns the list
            of IDs for the best group for that searcher

            searcher - int
            returns [int]'''

        min_score = 1000000
        ideal_group_members = []
        seen_groups = []
        all_user_ids = []
        query = ('''select user_id from user where user_id != {};'''.format(searcher))
        self.cursor.execute(query)
        resultsBrokenSkills = self.cursor.fetchall()
        for x in resultsBrokenSkills:
            all_user_ids.append(x["user_id"])
        for i in range(0, len(all_user_ids)):
            print("hit new i value: {}".format(all_user_ids[i]))
            for j in range(i + 1, len(all_user_ids)):
                for k in range(j + 1, len(all_user_ids)):
                    new_min = self.getTotalScoreForGroup(searcher, all_user_ids[i], all_user_ids[j], all_user_ids[k])
                    if new_min < min_score:
                        min_score = new_min
                        ideal_group_members = [all_user_ids[i], all_user_ids[j], all_user_ids[k]]
                        seen_groups.append({i, j, k})
        return ideal_group_members

    def getGroupMatesData(self, mateID):

        # Get Skill Set infor
        query = ('''SELECT
                        skill_name
                    FROM skillset
                    INNER JOIN skill
                        ON (skillset.skill_id = skill.skill_id)
                    WHERE user_id = {};'''.format(mateID))
        self.cursor.execute(query)
        results = self.cursor.fetchall()
        skillSet = []
        for x in results:
            skillSet.append(x["skill_name"])

        # Get all the other info
        query = ('''select name, email, phone_number from user where user_id = {};'''.format(mateID))
        self.cursor.execute(query)
        results = self.cursor.fetchall()
        mate_name = results[0]["name"]
        mate_email = results[0]["email"]
        mate_number = results[0]["phone_number"]
        return {'username': mate_name,
                'email': mate_email,
                'phonenumber': mate_number,
                'skills': skillSet}

    def getYourGroup(self, email):
        searcherID = self.getIdFromEmail(email)
        searcherID = searcherID['user_id']
        if searcherID not in range(0, 1000):
            return []
        ideal_group_ids = self.findIdealGroup(searcherID)
        group_info = []
        for x in ideal_group_ids:
            group_info.append(self.getGroupMatesData(x))
        return group_info

    def close(self):
        # close all connections
        self.cursor.close()
        self.cnx.close()


# model = Model()
# print("Final weight: {}".format(model.getIdFromEmail("setteducati.s@husky.neu.edu")))
# model.close()


# Close all connections
