import sqlite3
import pandas as pd 

#Creating Database
def create_connection(db_file = "ca_school.db"):
    conn = "None"
    try:
        conn = sqlite3.connect(db_file)
    except Error as e: print(e)
    return conn

connection = create_connection()

sInfo_stDemo = pd.read_excel('schoolInfo&studentDemo.xlsx')
sInfo_stDemo.drop(columns=['Building Suite',
        'P.O. Box', 'Street','Postal Code', 'Phone Number', 'Fax Number',
        'School Website', 'Board Website', 
        'Change in Grade 3 Reading Achievement Over Three Years',
        'Change in Grade 3 Writing Achievement Over Three Years',
        'Change in Grade 3 Mathematics Achievement Over Three Years',
        'Change in Grade 6 Reading Achievement Over Three Years',
        'Change in Grade 6 Writing Achievement Over Three Years',
        'Change in Grade 6 Mathematics Achievement Over Three Years',
        'Change in Grade 9 Mathematics Achievement Over Three Years',
        'Change in Grade 10 OSSLT Literacy Achievement Over Three Years'
        ], inplace=True)
# print(sInfo_stDemo.columns)

def create_boardDB():
    board_df = sInfo_stDemo[['Board Number', 'Board Name', 'Board Type']]
    board_df.drop_duplicates(ignore_index=True, inplace=True)
    # print(board_df)
    board_df.to_sql('Board', connection, if_exists='replace')
# create_boardDB()

def create_schoolDB():
    school_df = sInfo_stDemo[['School Number',
       'School Name', 'School Type', 'School Special Condition Code',
       'School Level', 'School Language', 'Grade Range', 'Municipality',
       'City', 'Province', 'Enrolment', 'Latitude', 'Longitude']]
    school_df.drop_duplicates(ignore_index=True, inplace=True)
    # print(school_df.info())
    school_df.to_sql('School', connection, if_exists='replace')
# create_schoolDB()

def create_schoolDB():
    school_df = sInfo_stDemo[['School Number',
       'School Name', 'School Type', 'School Special Condition Code',
       'School Level', 'School Language', 'Grade Range', 'Municipality',
       'City', 'Province', 'Enrolment', 'Latitude', 'Longitude']]
    # print(school_df.info())
    school_df.to_sql('School', connection, if_exists='replace')
# create_schoolDB()

def create_studentDemoDB():
    demo_df = sInfo_stDemo[['School Number',
        'Percentage of Students Whose First Language Is Not English',
       'Percentage of Students Whose First Language Is Not French',
       'Percentage of Students Who Are New to Canada from a Non-English Speaking Country',
       'Percentage of Students Who Are New to Canada from a Non-French Speaking Country',
       'Percentage of Students Receiving Special Education Services',
       'Percentage of School-Aged Children Who Live in Low-Income Households',
       'Percentage of Students Whose Parents Have No Degree, Diploma or Certificate',
       'Extract Date']]
    # print(school_df.info())
    demo_df.to_sql('Demographics', connection, if_exists='replace')
# create_studentDemoDB()

def create_achiveDB():
    achieve_df = sInfo_stDemo[['School Number',
            'Percentage of Students Identified as Gifted',
           'Percentage of Grade 3 Students Achieving the Provincial Standard in Reading',
           'Percentage of Grade 3 Students Achieving the Provincial Standard in Writing',
           'Percentage of Grade 3 Students Achieving the Provincial Standard in Mathematics',
           'Percentage of Grade 6 Students Achieving the Provincial Standard in Reading',
           'Percentage of Grade 6 Students Achieving the Provincial Standard in Writing',
           'Percentage of Grade 6 Students Achieving the Provincial Standard in Mathematics',
           'Percentage of Grade 9 Students Achieving the Provincial Standard in Mathematics',
           'Percentage of Students That Passed the Grade 10 OSSLT on Their First Attempt',
           'Extract Date']]
    achieve_df.to_sql('Achievements', connection, if_exists='replace')
create_achiveDB()

boardFinanc = pd.read_csv("boardFinancial.csv")
print(boardFinanc.loc[54])

connection.close()