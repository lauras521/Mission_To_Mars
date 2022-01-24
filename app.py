#use Flask to render a template, redirecting to another url, and creating a URL
from flask import Flask, render_template, redirect, url_for
#says we'll use PyMongo to interact with Mongo Database
from flask_pymongo import PyMongo
#will convert from Jupyter notebook to Python
import scraping

app = Flask(__name__)

# Use flask_pymongo to set up mongo connection
#first part tells Python our app will connect to Mongo using URI
#second part is URI well use to connect to Mongo
#this URI is saying the app can reach Mongo at localhost server 
# using port 27017 using a database nammed mars_app
app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_app"
mongo = PyMongo(app)

#define route for html page
@app.route('/')
#This function is what links our visual representation of our work, 
# our web app, to the code that powers it.
def index():
    #uses PyMongo to find the "mars"
    mars=mongo.db.mars.find_one()
    #tells Flask to return an HTML template using an index.html file, 
    #,mars=mars tells python to use the "mars" collection in MongoDB
    return render_template('index.html',mars=mars)

#will be the button to scrape and update the data
@app.route("/scrape")
#access database, scrape new data using scraping.py, update db, 
# return a message that it is successful
def scrape():
    #points to mongo db
    mars=mongo.db.mars
    #variable to jold scraped data
    mars_data=scraping.scrape_all()
    #update database
    mars.update_one({},{'$set':mars_data},upsert=True)
    #navitage page back to where we can see updated content
    return redirect('/',code=302)
#needed for Flask to tell it to run
if __name__ == "__main__":
   app.run()

