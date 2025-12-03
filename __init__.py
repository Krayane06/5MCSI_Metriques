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

@app.route("/commits-data/")
def commits_data():
    # Appel de l'API GitHub du dépôt d'origine
    response = urlopen("https://api.github.com/repos/OpenRSI/5MCSI_Metriques/commits")
    raw_content = response.read()
    commits = json.loads(raw_content.decode("utf-8"))

    minutes_count = {}

    for commit in commits:
        # Récupérer la date : commit -> author -> date
        date_str = (
            commit.get("commit", {})
                  .get("author", {})
                  .get("date")
        )
        if not date_str:
            continue

        # Exemple de format : "2024-02-11T11:57:27Z"
        date_object = datetime.strptime(date_str, "%Y-%m-%dT%H:%M:%SZ")
        minute = date_object.minute

        # Compter le nombre de commits par minute
        minutes_count[minute] = minutes_count.get(minute, 0) + 1

    # Transformer en liste triée pour le JSON
    results = [
        {"minute": minute, "count": count}
        for minute, count in sorted(minutes_count.items())
    ]

    return jsonify(results=results)



@app.route("/")
def hello_world():
    # Page d'accueil (exercice précédent)
    return render_template("hello.html")


if __name__ == "__main__":
    app.run(debug=True)
