import pandas as pd

pd.options.mode.chained_assignment = None


def read_csv(csv_file_name):
    file = pd.read_csv(csv_file_name)
    file['user_id'] = file.index
    user = file[['user_id', 'Name', 'Email', 'Phone Number', 'Year (1 through 5)', 'Current grade in class (0-100)']]
    user.rename(columns={'Phone Number': 'phone_number', 'Year (1 through 5)': 'year',
                         'Current grade in class (0-100)': 'grade'}, inplace=True)
    skill_columns = ['Skill set [Non-relational database (neo4J, NoSQL, MongoDB etc...)]',
                     'Skill set [Python]', 'Skill set [Java]',
                     'Skill set [Flask (Python Library)]', 'Skill set [GitHub]',
                     'Skill set [AWS]', 'Skill set [JavaScript]', 'Skill set [Racket]',
                     'Skill set [Scala]', 'Skill set [HTML/CSS]']
    skills = dict(zip(skill_columns, [i for i in range(len(skill_columns))]))
    skill_columns.extend(['user_id'])
    skillset = file[skill_columns]
    skillset = skillset.melt(id_vars='user_id')
    skillset = skillset.loc[skillset['value'] != 'Not known']
    skillset['variable'] = skillset['variable'].map(lambda x: skills[x])
    skillset.rename(columns={'variable': 'skill_id'}, inplace=True)
    skills = pd.DataFrame.from_dict(dict(enumerate(skills.items())), orient='index', columns=['skill_name', 'skill_id'])
    # Creates availability off pivots
    availability_cols = ['What is your availability? [Monday]',
                         'What is your availability? [Tuesday]',
                         'What is your availability? [Wednesday]',
                         'What is your availability? [Thursday]',
                         'What is your availability? [Friday]',
                         'What is your availability? [Saturday]',
                         'What is your availability? [Sunday]']
    # Renames to fit enum
    avail_col_names = dict(zip(availability_cols, ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']))
    availability_cols.extend(['user_id'])
    availability = file[availability_cols]
    availability = availability.rename(columns=avail_col_names)
    # Pivots day availability into column
    availability = availability.melt(id_vars='user_id')
    # Removes unavailable times
    availability = availability.loc[availability['value'] != 'unavailable on that day']
    # Key of timeslot on form to military hour
    timeslots = {'8am - 10am': (8, 10), '10am - 12pm': (10, 12), '12pm - 2pm': (12, 14), '2pm - 4pm': (14, 16),
                 '4pm - 6pm': (16, 18), '6pm - 8pm': (18, 20), '8pm - 10pm': (20, 22), '10pm onward': (22, 24)}
    # makes a column for each timeslot and puts true if in users availability
    for time in timeslots.keys():
        availability[time] = availability['value'].map(lambda x: time in x)
    # Renames for clarity
    availability = availability.rename(columns={'variable': 'day'})
    # Keeps only columns we need
    availability = availability[['user_id', 'day', '8am - 10am', '10am - 12pm', '12pm - 2pm',
                                 '2pm - 4pm', '4pm - 6pm', '6pm - 8pm', '8pm - 10pm', '10pm onward']]
    # Pivots keeping user_id and day
    availability = availability.melt(id_vars=['user_id', 'day'])
    # Removes values where the user is unavailable
    availability = availability[availability['value'] == True]
    # Converts from timeslots to start and end times
    availability['start'] = availability['variable'].map(lambda x: timeslots[x][0])
    availability['end'] = availability['variable'].map(lambda x: timeslots[x][1])
    availability = availability[['user_id', 'day', 'start', 'end']]

    # project interest
    interests_on_form = ['Web App', 'Data Collection', 'Analysis', 'Visualization', 'Non-relational Database']
    interest_ids = dict(zip(interests_on_form, [x for x in range(len(interests_on_form))]))

    # user interests
    user_interest = file[['user_id', 'Project Type Interest (Check all that apply or none)']]
    for int_id in interest_ids.keys():
        user_interest[int_id] = user_interest['Project Type Interest (Check all that apply or none)'].map(
            lambda x: int_id in x)
    # Removes unnecessary column
    user_interest = user_interest[['user_id', 'Web App', 'Data Collection', 'Analysis', 'Visualization',
                                   'Non-relational Database']]
    user_interest = user_interest.melt(id_vars='user_id')
    # Filter out those the user is not interested in
    user_interest = user_interest[user_interest['value'] == True]
    # Map interest name to interest id
    user_interest['interest_id'] = user_interest['variable'].map(lambda x: interest_ids[x])
    # Filter unnecessary columns
    user_interest = user_interest[['user_id', 'interest_id']]

    # Team preferences
    team_preference = file[['user_id', 'Who would you prefer to work with? (email)',
                            'Second person you would prefer to work with? (email) ', ]]
    user_email = dict(zip(file['Email'], file['user_id']))
    # Pivots to have all emails in one column
    team_preference = team_preference.melt(id_vars=['user_id'])
    team_preference = team_preference.dropna()
    team_preference['user_prefers'] = team_preference['value'].map(
        lambda x: user_email[x] if x in user_email.keys() else -1)
    team_preference = team_preference[['user_id', 'user_prefers']]
    # remove preferences where there is no user
    team_preference = team_preference[team_preference['user_prefers'] != -1]

    # Teams
    teams = file[['user_id', 'If you\'re in a group, what is your group name? ']]
    teams = teams.rename(columns={'If you\'re in a group, what is your group name? ': 'group_name'})
    teams = teams.dropna()
    unique_teams = list(teams['group_name'].unique())

    # project_group table
    team_names_to_ids = dict(zip(unique_teams, [x for x in range(len(unique_teams))]))
    # group_member table
    teams['group_id'] = teams['group_name'].map(lambda x: team_names_to_ids[x])
    teams.drop(columns={'group_name'}, inplace=True)
    team_names_to_ids = pd.DataFrame.from_dict(dict(enumerate(team_names_to_ids.items())), orient='index',
                                               columns=['group_name', 'group_id'])
    interest_ids = pd.DataFrame.from_dict(dict(enumerate(interest_ids.items())), orient='index',
                                          columns=['interest_name', 'interest_id'])
    keys = ['user', 'skill', 'skillset', 'availability', 'interest_id', 'user_interest', 'team_preference',
            'project_group', 'team']
    return dict(zip(keys, (user, skills, skillset, availability,
                           interest_ids, user_interest, team_preference, team_names_to_ids, teams)))
