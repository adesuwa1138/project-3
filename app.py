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

import json
#################################################
# Database Setup
#################################################
engine    = create_engine("sqlite:///data/baby_names.db", echo=False)

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

    conn = engine.connect()
    year_num = int(year)
    baby_names = pd.read_sql("SELECT * FROM baby_names", conn)
    
    baby_names_year = baby_names[baby_names['Year'] == year_num].sort_values(by='Count')

    baby_names_boy = baby_names_year.loc[baby_names_year['Sex'] == 'Male']
    baby_names_girl = baby_names_year.loc[baby_names_year['Sex'] == 'Female']
    

     
    #  = baby_names[baby_names['Year'] == year]

    """Return a list of all passenger names"""
    # Query all passengers
    # results = session.query(nat_names.Count, nat_names.Gender, nat_names.Name, nat_names.Year).\
    #     filter(nat_names.Year == year).limit(25)


    # session.close()
    
   #Create visualizations for YEAR data

    fig1 = px.bar(baby_names_boy, y='Name', x='Count', height=800, orientation='h')
    fig2 = px.bar(baby_names_girl, y='Name', x='Count', height=800,color_discrete_sequence=['pink'], orientation='h')
    fig3 = px.scatter(baby_names_year, x='Count', y='Rank', height=800,  size = 'Count', color='Sex',color_discrete_sequence=['pink','blue'], orientation='h', hover_name="Name")
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

    return render_template("year.html", query = baby_names_year, graphJSON=graphJSON, graphJSON1=graphJSON1, graphJSON2=graphJSON2, year = year_num) 

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
 
# @app.route('/data/', methods = ['POST', 'GET'])
# def data():
#     if request.method == 'GET':
#         return f"The URL /data is accessed directly. Try going to '/form' to submit form"
#     if request.method == 'POST':
#         form_data = request.form


#     conn = engine.connect()
#     year_num = int(year)
#     baby_names = pd.read_sql("SELECT * FROM baby_names", conn)
    
#     baby_names_year = baby_names[baby_names['Year'] == year_num].sort_values(by='Count')

#     baby_names_boy = baby_names_year.loc[baby_names_year['Sex'] == 'Male']
#     baby_names_girl = baby_names_year.loc[baby_names_year['Sex'] == 'Female']
    

     
#     #  = baby_names[baby_names['Year'] == year]

#     """Return a list of all passenger names"""
#     # Query all passengers
#     # results = session.query(nat_names.Count, nat_names.Gender, nat_names.Name, nat_names.Year).\
#     #     filter(nat_names.Year == year).limit(25)


#     # session.close()
    
#    #Create visualizations for YEAR data

#     fig1 = px.bar(baby_names_boy, y='Name', x='Count', height=800, orientation='h')
#     fig2 = px.bar(baby_names_girl, y='Name', x='Count', height=800,color_discrete_sequence=['pink'], orientation='h')
#     fig3 = px.scatter(baby_names_year, x='Count', y='Rank', height=800,  size = 'Count', color='Sex',color_discrete_sequence=['pink','blue'], orientation='h', hover_name="Name")
#     fig1.update_layout(template='simple_white', xaxis_range=[0,10000])
#     fig2.update_layout(template='simple_white',  xaxis_range=[0,10000])
#     fig3.update_layout(yaxis=dict(autorange="reversed"), template='simple_white')
#     graphJSON = json.dumps(fig1, cls=plotly.utils.PlotlyJSONEncoder)
#     graphJSON1 = json.dumps(fig2, cls=plotly.utils.PlotlyJSONEncoder)
#     graphJSON2 = json.dumps(fig3, cls=plotly.utils.PlotlyJSONEncoder)
#     # for name in results:
#     #     # search_term = character["real_name"].replace(" ", "").lower()
#     #     return jsonify(name)
#         # if search_term == canonicalized:
#         #     return jsonify(character)

#     return render_template("year.html", query = baby_names_year, graphJSON=graphJSON, graphJSON1=graphJSON1, graphJSON2=graphJSON2, year = year_num) 
        # return render_template('data.html',form_data = form_data)


if __name__ == "__main__":
    app.run(debug=True)

