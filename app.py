# This script focuses on the backend
# of the Geocoder Web Service i.e. reading the data,
# adding the lat and lon columns.

from flask import Flask, render_template, request, send_file
# Used to prevent \...\...\ from being used to
# access computer files
from werkzeug.utils import secure_filename
from geopy.geocoders import ArcGIS
import pandas

nom = ArcGIS()

app = Flask(__name__)


@app.route("/")
# Shows the main page
def main():
    return render_template("index.html")

# Shows the upload page if user has uploaded a file
@app.route("/upload", methods=['GET', 'POST'])
def upload():
    global filename
    # If file has been uploaded, show upload page
    if request.method == 'POST':
        # Stores uploaded file
        file = request.files["file"]
        # Secures computer and pr
        # events hackers from accessing your directory
        # using bash files
        file.save(secure_filename(
            "uploaded"+file.filename))
        with open("uploaded"+file.filename, "a") as f:
            import pandas
            df = pandas.read_csv("uploaded"+file.filename)
            df["Address"] = df["Address"]+", " + df["City"] + \
                ", " + ["State"] + ", " + ["Country"]
            # Gets lat and long of each address
            df["Coordinates"] = df["Address"].apply(nom.geocode)
            # Adds lat and long column
            df["Latitude"] = df["Coordinates"].apply(lambda x: x.latitude)
            df["Longitude"] = df["Coordinates"].apply(lambda y: y.longitude)
            df.to_csv('updatedsupermarkets.csv',
                      mode='a', header=False)

            return render_template("index.html", btn="download.html")


@app.route("/download")
def download():
    return send_file("updatedsupermarkets.csv", attachment_filename="yourfile.csv", as_attachment=True)


# Runs app if name is equal to main page (always true)
if __name__ == "__main__":
    app.run(debug=True)
