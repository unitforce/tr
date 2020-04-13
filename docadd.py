import pandas
import json
from bs4 import BeautifulSoup
import requests
import pandas as pd
import datetime
import spacy
unique=0
upload=0
posts=6
ids=[]
response=requests.get("https://unitforce.talentrecruit.com/API/SearchJobs?")
data=response.json()
from pymongo import MongoClient
client=MongoClient("localhost",27017)
db=client.Project
posts=db.post
from rank_bm25 import BM25Okapi
def extract_skills(resume_text):
    nlp=spacy.load("en_core_web_sm")
    nlp_text = nlp(resume_text)

    # removing stop words and implementing word tokenization
    tokens = [token.text for token in nlp_text if not token.is_stop]

    # reading the csv file
    data = pd.read_csv("F:\skills_talentrecruit.csv")

    # extract values
    skills = list(data.columns.values)

    skillset = []

    # check for one-grams (example: python)
    for token in tokens:
        if token.lower() in skills:
            skillset.append(token)

    # check for bi-grams and tri-grams (example: machine learning)
    for token in nlp_text.noun_chunks:
        token = token.text.lower().strip()
        if token in skills:
            skillset.append(token)
    return [i.capitalize() for i in set([i.lower() for i in skillset])]
inf=[]
for i in data["Details"]:
    e=i["ID"]
    response1=requests.get("https://unitforce.talentrecruit.com/Search/Jobs/"+"?"+e)
    html_a=BeautifulSoup(response1.content,"html.parser")
    a=html_a.find(id="MainContent_divRolesAndResponsibilityRow")
    words=""

    for ments in a.find_all(text=True):
        words+=ments
        extra=words.replace("\n"," ")
        aa=extra.replace("\t"," ")
    i["Date"]=datetime.datetime.utcnow()
    job=i["JobTitle"]
    aaa=job.replace("||"," ")
    i.pop("JobTitle")
    jo_inf=i.pop("$id")
    job_inf=i
    job_inf["description"]=aa
    job_inf.pop("ShortDescription")
    i["skils"]=extract_skills(aa)
    job_inf["JobTitle"]=aaa
    #print(aaa)
    inf.append(job_inf)
#print(inf)
import datetime
for data in inf:
    dataDescip=data["description"].replace("?",".")
    data.pop("description")
    data["description"]=dataDescip
jd_information=inf

for unique_id_jd in posts.find():

    ids.append(unique_id_jd["ID"])


for jd in jd_information:
    if jd["ID"] not in ids:
        posts.insert(jd)
        upload+=1
    else:
        posts.update_one({"ID":jd["ID"]},{"$set":jd})
        unique+=1
print("the total number of document that were uploaded were ",upload)
print("the total number of document that were updated were ",unique)
