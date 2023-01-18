import numpy as np
import pandas as pd
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
# from flask_bootstrap import Bootstrap5
# from flask_datepicker import datepicker
from flask import Flask, jsonify, render_template, request, redirect, url_for
import plotly
import plotly.express as px
import plotly.io as pio
import csv
import json
#################################################
# Database Setup
#################################################
engine    = create_engine("sqlite:///static/baby_names.db", echo=False)

famous_names = pd.read_csv("static/famous_people.csv", encoding = 'unicode_escape', engine ='python')



#################################################
# Flask Setup
#################################################
app = Flask(__name__)
# bootstrap = Bootstrap5(app)
# date = datepicker(app)

#################################################
# Flask Routes
#################################################

# 3. Define what to do when a user hits the index route
@app.route("/")
def home():
    
    return render_template("index.html")

@app.route("/year_home")
def year_home():
    
    return render_template("year_home.html")

@app.route("/name_home")
def name_home():
    
    return render_template("name_home.html")


@app.route("/year_home/<year>")
def year(year):
    """Fetch the Justice League character whose real_name matches
       the path variable supplied by the user, or a 404 if not."""

    # canonicalized = baby_name.replace(" ", "").lower()
    # famous_names = pd.read_csv("static/famous_people.csv", encoding = 'unicode_escape', engine ='python')
    # col_names = ['Year','Img_url','Full_name', 'First_name']
    #     # Use Pandas to parse the CSV file
    #     # 
    # csvData = pd.read_csv('static/famous_people.csv',names=col_names, header=0, encoding = 'unicode_escape', engine ='python')

    # names1 = []
    # for i,row in csvData.iterrows():

    #     names1.append({
    #             "Name": row['First_name'],
    #             "Year": row['Img_url'],
    #             "img_url": row['Year']
    #             })
        
    #     # print(i,row['Year'],row['Img_url'],row['Full_name'],row['First_name'],)
    
    # with open('static/famous_people.csv') as csv_file:
    #     data = csv.reader(csv_file, delimiter=',')
    #     names = []
    #     for row in data:
    #         names.append({
    #             "Name": row[3],
    #             "Year": row[0],
    #             "img_url": row[1]
    #             })
    conn = engine.connect()
    year_num = int(year)
    baby_names = pd.read_sql("SELECT * FROM baby_names", conn)
    
    baby_names_year = baby_names[baby_names['Year'] == year_num].sort_values(by='Count')
    # top_baby_names = baby_names['Name']str.lower()
    baby_names_boy = baby_names_year.loc[baby_names_year['Sex'] == 'Male']
    baby_names_girl = baby_names_year.loc[baby_names_year['Sex'] == 'Female']
    conn.close()
    
    col_names = ['Year','Img_url','Full_name','Name', 'First_name']
    csvData = pd.read_csv('static/famous_people.csv',names=col_names, header=0, encoding = 'unicode_escape', engine ='python')
    names_from_csv =  csvData[csvData['Year'] == year_num]
    top_names = names_from_csv[names_from_csv['Name'].isin(baby_names_year['Name'].str.lower())]
    names1 = []
    for i,row in top_names.iterrows():

        names1.append({
                "Name": row['First_name'],
                "Year": row['Year'],
                "img_url": row['Img_url']
                })
        
    year_celebs = famous_names[famous_names['Year'] == year_num]

    fig1 = px.bar(baby_names_boy, y='Name', x='Count', height=800,color_discrete_sequence=['#0180CB'], orientation='h')
    fig2 = px.bar(baby_names_girl, y='Name', x='Count', height=800,color_discrete_sequence=['#FFC310'], orientation='h')
    fig3 = px.scatter(baby_names_year, x='Count', y='Rank', height=800,  size = 'Count', color='Sex',color_discrete_sequence=['#FFC310','#0180CB'], orientation='h', hover_name="Name")
    fig1.update_layout(template='simple_white', xaxis_range=[0,10000])
    fig2.update_layout(template='simple_white',  xaxis_range=[0,10000])
    fig3.update_layout(yaxis=dict(autorange="reversed"), template='simple_white')
    graphJSON = json.dumps(fig1, cls=plotly.utils.PlotlyJSONEncoder)
    graphJSON1 = json.dumps(fig2, cls=plotly.utils.PlotlyJSONEncoder)
    graphJSON2 = json.dumps(fig3, cls=plotly.utils.PlotlyJSONEncoder)
    # for name in results:
    #     # search_term = character["real_name"].replace(" ", "").lower()
    #     return jsonify(name)
        # if search_term == canonicalized:
        #     return jsonify(character)

    return render_template("year.html", data = names1, graphJSON=graphJSON, graphJSON1=graphJSON1, graphJSON2=graphJSON2, year = year_num) 

#Create page for Name queries
@app.route("/name_home/ADESUWA")
def not_found():
    return render_template("name_not_found.html")

@app.route("/name_home/ANNA")
def not_found_1():
    return render_template("name_not_found_1.html")

@app.route("/name_home/<name>")
def name(name):
   conn = engine.connect()
   baby_names = pd.read_sql("SELECT * FROM baby_names", conn)
   
   baby_names_names = baby_names[baby_names['Name'] == name]

   if baby_names_names['Sex'].loc[baby_names_names.index[0]] == "Male":
    sex_color = '#0180CB'
   else:
    sex_color = '#FFC310'


# Create visualization for name entry
   
   fig = px.line(baby_names_names, y='Count', x='Year', color='Sex',color_discrete_sequence=[sex_color], orientation='h', title = (f'Hello, my name is {name}'))
   
   fig.update_layout(title_font_family="Times New Roman",
                     title_font_color="#FFC310",
                     title_font_size=70,
                     title_x=0.5,
                     template='simple_white')
                     

   graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)

   return render_template("names.html", query = baby_names, graphJSON=graphJSON) 

 
@app.route('/form')
def form():
    return render_template('form.html')
 


if __name__ == "__main__":
    app.run(debug=True)

