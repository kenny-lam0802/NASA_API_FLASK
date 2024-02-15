from flask_app import app
from flask import render_template, redirect, request, session,jsonify
import requests, os
from flask_app.models import image


@app.route("/")
def search_page():
    return render_template("img_search.html")


@app.route("/search", methods=["POST"])
def search_api():
    #If API call has been saved to DB call from DB instead of calling from API
    query_data = {
        "date": request.form["date"]
        }
    found_image_or_none = image.Image.select_by_date(query_data)
    if found_image_or_none == None:
        print("Calling on API")
        api_link = f"https://api.nasa.gov/planetary/apod?api_key={os.environ.get('NASA_API_KEY')}&date={request.form['date']}"
        #Get JSON data from link using API
        response = requests.get(api_link)
        raw_data = response.json()
        print(raw_data)
        session["date"] = raw_data["date"]
        session["description"] = raw_data["explanation"]
        session["image_link"] = raw_data["hdurl"]
    else:
        session["date"] = found_image_or_none.date
        session["description"] = found_image_or_none.description
        session["image_link"] = found_image_or_none.image_link
    return redirect("/results")

@app.route("/image/save")
def save_fave():
    data = {
        "date": session['date'],
        "description": session['description'],
        "image_link": session['hdurl'],
    }
    image.Image.save_image(data)
    return redirect("/")

@app.route("/results")
def results_page():
    return render_template("search_results.html")

@app.route("/multiple/images")
def date_range():
    return render_template("multiple_img.html")

@app.route("/search/multiple", methods = ['POST'])
def search_multple():
    api_link = (f"https://api.nasa.gov/planetary/apod?api_key={os.environ.get('NASA_API_KEY')}&start_date={request.form['start_date']}&end_date={request.form['end_date']}")
    response_string = requests.get(api_link)
    raw_data = response_string.json()
    session.modified = True #Allows modification of lists in session
    session["results"] = []
    for each_result in raw_data:
        new_dictionary = {
            "date": each_result["date"],
            "description": each_result["explanation"],
            "image": each_result["hdurl"],
        }
        session["results"].append(new_dictionary)
    return redirect("/results/multiple")

@app.route("/results/multiple")
def multiple_results():

    return render_template("multiple_search_results.html")