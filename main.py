from flask import Flask, render_template, request, redirect, url_for, flash
from bs4 import BeautifulSoup
from sqlalchemy.sql import func
from flask_sqlalchemy import SQLAlchemy
import project4
import requests
import re
import random

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
    word = StudyList.query.get(word_id)
    spanish_word = word.spanish_word
    english_word = word.english_word
    spanish_sentence = word.spanish_sentence
    english_sentence = word.english_sentence
    audio = word.audio
    if "None" in audio:
        audio = None
    if word is not None:
        return render_template('word_detail.html', spanish_word=spanish_word, english_word=english_word, spanish_sentence=spanish_sentence, english_sentence=english_sentence, audio=audio)
    else:
        flash('Word not found.', 'danger')
        return redirect(url_for('view_study_list'))

@app.route('/delete-words', methods=['POST'])
def delete_words():
    if request.method == 'POST':
        word_ids_to_delete = request.form.getlist('delete_word_ids')

        if word_ids_to_delete:
            for word_id in word_ids_to_delete:
                word = StudyList.query.get(word_id)
                if word:
                    db.session.delete(word)
            
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

@app.route('/save-to-study-list2', methods=['POST'])
def save_to_study_list2():
    spanish_word = request.form.get('spanish_word')
    english_word = request.form.get('english_word')
    spanish_sentence = request.form.get('spanish_sentence')
    english_sentence = request.form.get('english_sentence')
    audio = request.form.get('audio')

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

    return redirect(url_for('view_study_list3'))



@app.route('/study-list')
def view_study_list():
    study_list = StudyList.query.all()
    return render_template('span_study_list.html', study_list=study_list)

@app.route('/study-list2')
def view_study_list2():
    study_list = StudyList.query.all()
    return render_template('study_list_from_home.html', study_list=study_list)

@app.route('/study-list3')
def view_study_list3():
    study_list = StudyList.query.all()
    return render_template('study_list_back_to_random.html', study_list=study_list)

@app.route('/random-quiz')
def random_quiz():
    part0 = generate_word2()
    spanish_correct_word = part0[0]
    english_correct_word = part0[1]
    spanish_sentence = part0[2]
    english_sentence = part0[3]
    audio = part0[4]
    part1 = generate_word2()
    english_word1 = part1[1]
    part2 = generate_word2()
    english_word2 = part2[1]
    part3 = generate_word2()
    english_word3 = part3[1]
    answer_options = [english_correct_word, english_word1, english_word2, english_word3]
    random.shuffle(answer_options)
    num = None
    if audio is None:
        pass
    else:
        if "None" in audio:
            audio = None
    for i in range(len(answer_options)):
        if answer_options[i] == english_correct_word:
            num = i
            break
    return render_template('random_quiz.html', spanish_correct_word=spanish_correct_word, correct_option_index=num, answer_options=answer_options, english_correct_word=english_correct_word, english_word1=english_word1, english_word2=english_word2, english_word3=english_word3, spanish_sentence=spanish_sentence, english_sentence=english_sentence, audio=audio)

@app.route('/submit-random-quiz', methods=["POST"])
def submit_random_quiz():
    answer = request.form.get("answer")
    spanish_correct = request.form.get("spanish_correct_word")
    english_correct = request.form.get("english_correct_word")
    english_word1 = request.form.get("english_word1")
    english_word2 = request.form.get("english_word2")
    english_word3 = request.form.get("english_word3")
    answer_option = [english_correct, english_word1, english_word2, english_word3]
    spanish_sentence = request.form.get("spanish_sentence")
    english_sentence = request.form.get("english_sentence")
    audio = request.form.get("audio")
    if "None" in audio:
        audio = None
    if answer == english_correct:
        return render_template('correct_answer_random.html', random_word=spanish_correct, answer_options=answer_option, translate_word=english_correct, audio=audio, spanish_sentence=spanish_sentence, english_sentence=english_sentence)
    else:
        flash("Wrong, please try again!", 'danger')
        return render_template('random_quiz.html', spanish_correct_word=spanish_correct, answer_options=answer_option, english_correct_word=english_correct, english_word1=english_word1, english_word2=english_word2, english_word3=english_word3, audio=audio, spanish_sentence=spanish_sentence, english_sentence=english_sentence)

@app.route('/correct-random-answer')
def correct_random_answer():
    return render_template('correct_answer_random.html')


@app.route('/study-list-quiz')
def study_list_quiz():
    random_word = db.session.query(StudyList).order_by(func.random()).first()
    if random_word is None:
        return render_template('spanish.html', message="You must add a word to the study list before starting the quiz!")
    else:
        spanish_correct_word = random_word.spanish_word
        english_correct_word = random_word.english_word
        spanish_sentence = random_word.spanish_sentence
        english_sentence = random_word.english_sentence
        audio = random_word.audio
        part1 = generate_word2()
        english_word1 = part1[1]
        part2 = generate_word2()
        english_word2 = part2[1]
        part3 = generate_word2()
        english_word3 = part3[1]
        answer_options = [english_correct_word, english_word1, english_word2, english_word3]
        random.shuffle(answer_options)
        num = None
        for i in range(len(answer_options)):
            if answer_options[i] == english_correct_word:
                num = i
                break
        if "None" in audio:
            audio = None
        return render_template('study_list_quiz.html', spanish_correct_word=spanish_correct_word, correct_option_index=num, answer_options=answer_options, english_correct_word=english_correct_word, english_word1=english_word1, english_word2=english_word2, english_word3=english_word3, audio=audio, spanish_sentence=spanish_sentence, english_sentence=english_sentence)

@app.route('/submit-quiz', methods=["POST"])
def submit_quiz():
    answer = request.form.get("answer")
    audio = request.form.get("audio")
    spanish_correct = request.form.get("spanish_correct_word")
    english_correct = request.form.get("english_correct_word")
    english_word1 = request.form.get("english_word1")
    english_word2 = request.form.get("english_word2")
    english_word3 = request.form.get("english_word3")
    spanish_sentence = request.form.get("spanish_sentence")
    english_sentence = request.form.get("english_sentence")
    if "None" in audio:
        audio = None
    answer_option = [english_correct, english_word1, english_word2, english_word3]
    if answer == english_correct:
        return render_template('correct_quiz_answer.html', random_word=spanish_correct, answer_options=answer_option, translate_word=english_correct, audio=audio, spanish_sentence=spanish_sentence, english_sentence=english_sentence)
    else:
        flash("Wrong, please try again!", 'danger')
        return render_template('study_list_quiz.html', spanish_correct_word=spanish_correct, answer_options=answer_option, english_correct_word=english_correct, english_word1=english_word1, english_word2=english_word2, english_word3=english_word3, audio=audio, spanish_sentence=spanish_sentence, english_sentence=english_sentence)

@app.route('/correct-quiz-answer')
def correct_quiz_answer():
    return render_template('correct_quiz_answer.html')


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
    try:
        data = get_data()
        random_word = data[0]
        translate_word_final = data[1]
        audio = data[2]
        if random_word[0].islower():
            list_of_sentences = find_sentences(random_word)
            spanish_sentence = list_of_sentences[0]
            english_sentence = list_of_sentences[1]
            return render_template("random_spanish.html", random_word=random_word, translate_word=translate_word_final, spanish_sentence=spanish_sentence, english_sentence=english_sentence, audio = audio)
        else:
            result = generate_word()
            return result
    except Exception as e:
        print(e)
        result = generate_word()
        return result

def generate_word2():
    try:
        data = get_data()
        random_word = data[0]
        translate_word_final = data[1]
        audio = data[2]
        if random_word.islower():
            list_of_sentences = find_sentences(random_word)
            spanish_sentence = list_of_sentences[0]
            english_sentence = list_of_sentences[1]
            return [random_word, translate_word_final, spanish_sentence, english_sentence, audio]
        else:
            result = generate_word2()
            return result
    except Exception as e:
        print(e)
        result = generate_word2()
        return result
    
def get_data():
    api_url_es = "https://random-word-api.herokuapp.com/word?lang=es"
    response = requests.get(api_url_es)
    if response.status_code == 200:
        data = response.json()
        random_word = data[0]
        api_url = f"https://www.dictionaryapi.com/api/v3/references/spanish/json/{random_word}?key={MERIAM_WEBSTER_API_KEY}"
        response = requests.get(api_url)
        data = response.json()
        if type(data[0]) is not dict:
            random_word = data[0]
            api_url = f"https://www.dictionaryapi.com/api/v3/references/spanish/json/{random_word}?key={MERIAM_WEBSTER_API_KEY}"
            response = requests.get(api_url)
            data = response.json()
            random_word = data[0]['meta']['id']
        else:
            random_word = data[0]['meta']['id']
        if ":" in random_word:
            random_word = random_word.split(":")[0]
        if 'hwi' in data[0] and 'prs' in data[0]['hwi'] and data[0]['hwi']['prs'] and 'sound' in data[0]['hwi']['prs'][0]:
            audio = data[0]['hwi']['prs'][0]['sound']['audio']
        else:
            audio = None
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
        return [random_word, translate_word_final, audio]
    else:
        return "Failed to generate a word. Please try again later."

def find_sentences(random_word):
    url = f"https://www.wordreference.com/es/en/translation.asp?spen={random_word}"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    all_text = soup.get_text()
    x = all_text.split("2023:Principal TranslationsSpanishEnglish")[1].split("\n")
    if x[0] == '':
        del x[0]

    for i in range(len(x)):
        if "\xa0" in x[i] and "." in x[i]:
            spanish_sentence = x[i].split(".")[-2] + "."
            english_sentence = x[i+1].split(".")[-2] + "."
            return [spanish_sentence, english_sentence]
    if len(spanish_sentence) == 0 and len(english_sentence) == 0:
        x = generate_word()
        return x
    else:
        spanish_sentence = x[2]
        english_sentence = x[3]
        return [spanish_sentence, english_sentence]


if __name__ == "__main__":
    app.run(debug=True)