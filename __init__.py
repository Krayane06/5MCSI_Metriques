from flask import Flask, render_template, jsonify
import json
from urllib.request import urlopen
from datetime import datetime

# sqlite3 et datetime ne sont pas obligatoires pour l'instant
# mais tu peux les remettre si ton prof les avait demandés :
# from datetime import datetime
# import sqlite3

app = Flask(__name__)


@app.route("/contact/")
def contact():
    # Page de contact customisée
    return render_template("contact.html")


@app.route("/tawarano/")
def meteo():
    # Appel de l'API OpenWeatherMap (exercice 3)
    response = urlopen(
        "https://samples.openweathermap.org/data/2.5/forecast?lat=0&lon=0&appid=xxx"
    )
    raw_content = response.read()
    json_content = json.loads(raw_content.decode("utf-8"))

    results = []
    for list_element in json_content.get("list", []):
        dt_value = list_element.get("dt")
        temp_day_value = list_element.get("main", {}).get("temp") - 273.15
        results.append({"Jour": dt_value, "temp": temp_day_value})

    return jsonify(results=results)


@app.route("/rapport/")
def mongraphique():
    # Page avec le graphique en ligne Google Charts
    return render_template("graphique.html")


@app.route("/histogramme/")
def histogramme():
    # Page avec l'histogramme (ColumnChart)
    return render_template("histogramme.html")


@app.route("/")
def hello_world():
    # Page d'accueil (exercice précédent)
    return render_template("hello.html")


if __name__ == "__main__":
    app.run(debug=True)
