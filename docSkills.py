import pandas as pd
def docSkills(skill):
    from pymongo import MongoClient

    db=MongoClient("localhost",27017)
    skillset=db.skills
    add=skillset.add_skills
    skills={}
    skills["id"]=1
    skills["added_today"]=skill
    skills["total_skills_added"]=0
    add.insert_one(skills)

def skilldoc(skill):

    dataset=pd.read_csv("F:\skills_talentrecruit.csv")
    for i in skill.split():
        dataset[i]=" "
    dataset.to_csv("F:\skills_talentrecruit.csv",index=False)
