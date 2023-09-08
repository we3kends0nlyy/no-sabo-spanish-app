from flask import Flask, render_template, request
import project4
radio_global = None
dropdown_global = None
app = Flask(__name__)

@app.route("/")
def home():
    return render_template("home.html")


@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/", methods=["GET"])
def show_form():
    return render_template("combined_form.html")

@app.route("/process_form", methods=["POST"])
def process_form():
    radio_option = request.form.get("radio_option")
    dropdown_option = request.form.get("dropdown_option")
    radio_global = radio_option
    dropdown_global = dropdown_option
    return render_template("random_name.html", message = project4.random_name_gen(f"{radio_option}{dropdown_option}"))

if __name__ == "__main__":
    app.run(debug=True)