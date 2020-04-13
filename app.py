import pandas as pd
import model
from flask import Flask,render_template,url_for,request
import spacy
import os
from docx import Document

nlp = spacy.load('en_core_web_sm')


from pymongo import MongoClient
client=MongoClient("localhost",27017)
db=client.Projectz
col=db.JD
posts=db.post
skills=[]
for post in posts.find():
    skills.append(post)
app=Flask(__name__)

@app.route('/')
def Resume_parsing():
    return render_template('index.html')
@app.route('/ski', methods = ['POST']) # /ski should navigate to the another page

def results():
        form = request.form  #  from a HTML post form
        if request.method == 'POST':

            fname=request.form.get('firstname') # img is name of Select Job_Description
            lname=request.form.get('lastname')
            country=request.form.get("country")
            filenam=request.form.get("filename")


             # something name of dropdown
            file_extension=os.path.splitext(filenam)
            #file_extension=file_extension.split(".")[-1]

            if filenam.endswith(".txt"):

                with open(filenam) as data:
                    data_res=data.read()
            else:
                document=Document(filenam)
                texts=[]
                for pa in document.paragraphs:
                    texts.append(pa.text)
                    data_res=",".join(texts)
            skills=model.extract_skills(data_res,fname,country)
            return render_template("finalpage1.html",p=skills)


if __name__ == '__main__':
    app.run('localhost','9999', debug = True)
