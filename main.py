from flask import Flask, render_template, request, redirect, url_for, jsonify, flash
from bs4 import BeautifulSoup
from flask_sqlalchemy import SQLAlchemy
import project4
import requests
import re
import time
import os

app = Flask(__name__)
app.secret_key = "toptopsecret123"

MERIAM_WEBSTER_API_KEY = 'e659155d-35c4-421f-8e2c-4f58a19f549c'
WORDSAPI_API_KEY = "2c34481877msh7ba15f7575bb54cp159d0fjsn0f2b169556ee"

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///spanish_database.db'
db = SQLAlchemy(app)


class StudyList(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    spanish_word = db.Column(db.String(100), nullable=False, unique=True)
    english_word = db.Column(db.String(100), nullable=False, unique=True)
    spanish_sentence = db.Column(db.String(500), nullable=False, unique=True)
    english_sentence = db.Column(db.String(500), nullable=False, unique=True)
    audio = db.Column(db.String(200), nullable=False, unique=True)


@app.route('/word_detail/<int:word_id>')
def word_detail(word_id):
    # Query the database to retrieve the word's details based on word_id
    word = StudyList.query.get(word_id)

    if word is not None:
        # Render a template to display the word's details
        return render_template('word_detail.html', word=word)
    else:
        # Handle the case where the word_id is not found
        flash('Word not found.', 'danger')
        return redirect(url_for('view_study_list'))

@app.route('/delete-words', methods=['POST'])
def delete_words():
    if request.method == 'POST':
        word_ids_to_delete = request.form.getlist('delete_word_ids')

        # Check if any words were selected for deletion
        if word_ids_to_delete:
            # Loop through the selected word IDs and delete them from the database
            for word_id in word_ids_to_delete:
                word = StudyList.query.get(word_id)
                if word:
                    db.session.delete(word)
            
            # Commit the changes to the database
            db.session.commit()
            flash('Selected words have been deleted successfully!', 'success')

    return redirect(url_for('view_study_list2'))

@app.route('/save-to-study-list', methods=['POST'])
def save_to_study_list():
    spanish_word = request.form.get('spanish_word')
    english_word = request.form.get('english_word')
    spanish_sentence = request.form.get('spanish_sentence')
    english_sentence = request.form.get('english_sentence')
    audio = request.form.get('audio')

    # Check if the word is not already in the study list
    if not StudyList.query.filter_by(spanish_word=spanish_word).first():
        new_word = StudyList(
            spanish_word=spanish_word,
            english_word=english_word,
            spanish_sentence=spanish_sentence,
            english_sentence=english_sentence,
            audio=audio
        )
        db.session.add(new_word)
        db.session.commit()
        flash(f'Word "{spanish_word}" saved successfully!', 'success')

    return redirect(url_for('view_study_list2'))


@app.route('/study-list')
def view_study_list():
    study_list = StudyList.query.all()
    print(study_list, "<<<<<<")
    return render_template('span_study_list.html', study_list=study_list)

@app.route('/study-list2')
def view_study_list2():
    study_list = StudyList.query.all()
    return render_template('study_list_from_home.html', study_list=study_list)


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
    return render_template("random_name.html", message = project4.random_name_gen(f"{radio_option}{dropdown_option}"))


@app.route("/spanish_page")
def spanish_page():
    return render_template("spanish.html")




@app.route("/generate-word", methods=["GET"])
def generate_word():
    print("restart")
    api_url_es = "https://random-word-api.herokuapp.com/word?lang=es"
    try:
        response = requests.get(api_url_es)
        if response.status_code == 200:
            data = response.json()
            random_word = data[0]
            api_url = f"https://www.dictionaryapi.com/api/v3/references/spanish/json/{random_word}?key={MERIAM_WEBSTER_API_KEY}"
            response = requests.get(api_url)
            data = response.json()
            if type(data[0]) is not dict:
                print("11111")
                result = generate_word()
                return result
            else:
                audio = data[0]['hwi']['prs'][0]['sound']['audio']
                if len(data[0]['shortdef']) > 1:
                    translate_word1 = data[0]['shortdef'][0]
                    translate_word2 = data[0]['shortdef'][1]
                    translate_word_final = translate_word1.capitalize() + "/" + translate_word2.capitalize()
                    if ":" in translate_word1:
                        b = translate_word1.split(":")
                        for i in range(len(b)):
                            if b[i][0] == " ":
                                c = b[i:]
                                break
                        translate_word1 = c[0][1:]
                    if ":" in translate_word2:
                        b = translate_word2.split(":")
                        for i in range(len(b)):
                            if b[i][0] == " ":
                                c = b[i:]
                                break
                        translate_word2 = c[0][1:]
                    translate_word_final = translate_word1 + "/" + translate_word2
                else:
                    translate_word_final = data[0]['shortdef'][0].capitalize()
            if random_word[0].islower():
                url = f"https://www.spanishdict.com/translate/{random_word}"
                response = requests.get(url)
                if response.status_code == 200:
                    soup = BeautifulSoup(response.text, "html.parser")
                    all_text = soup.get_text()
                    pattern = r'\b[ab]\.\s+(.*?)\n'
                    examples = re.findall(pattern, all_text, re.DOTALL)
                    x = examples[0]
                    x.split("2.")
                    for i in range(len(x)):
                        if x[i]+x[i+1] == "2.":
                            a = x[0:i]
                            break
                    a = a.split(".") 
                    ###SEPARATE THIS CODE INTO MULTIPLE FUNCTIONS###
                    left_side = a[0]
                    new = left_side.split(" ")
                    new_new = new[1:]
                    newwww = ""
                    for i in range(len(new_new)):
                        if new_new[i].islower():
                            del new_new[i]
                            break
                    for i in new_new:
                        newwww = newwww + " " + i
                    newwww = newwww + "."
                    english_sentence = a[1] + "."
                    response.close()
                    ###PLUS add study list(checks if word is already added, displays info of the word, allow to delete, other things)###
                return render_template("random_spanish.html", random_word=random_word, translate_word=translate_word_final, spanish_sentence=newwww, english_sentence=english_sentence, audio = audio)
            else:
                result = generate_word()
                return result
        else:
            return "Failed to generate a word. Please try again later."
    except Exception as e:
        print(e)
        result = generate_word()
        return result

if __name__ == "__main__":
    app.run(debug=True)