from flask import Flask, render_template, request, redirect, url_for, jsonify
from bs4 import BeautifulSoup
import project4
import requests
import re
import time
app = Flask(__name__)

MERIAM_WEBSTER_API_KEY = 'e659155d-35c4-421f-8e2c-4f58a19f549c'
WORDSAPI_API_KEY = "2c34481877msh7ba15f7575bb54cp159d0fjsn0f2b169556ee"



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
    api_url_es = "https://random-word-api.herokuapp.com/word?lang=es"
    try:
        response = requests.get(api_url_es)
        if response.status_code == 200:
            data = response.json()
            random_word = data[0]
            print(random_word)
            api_url = f"https://www.dictionaryapi.com/api/v3/references/spanish/json/{random_word}?key={MERIAM_WEBSTER_API_KEY}"
            response = requests.get(api_url)
            data = response.json()
            if type(data[0]) is not dict:
                result = generate_word()
                return result
            else:
                if len(data[0]['shortdef']) > 1:
                    translate_word1 = data[0]['shortdef'][0]
                    print(translate_word1, "33333")
                    translate_word2 = data[0]['shortdef'][1]
                    translate_word_final = translate_word1.capitalize() + "/" + translate_word2.capitalize()
                    if ":" in translate_word1:
                        b = translate_word1.split(":")
                        print(b)
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
                ###GET THE DEFINITION FROM SPANISH DICTIONARY HERE###

                url = f"https://www.spanishdict.com/translate/{random_word}"
                response = requests.get(url)

                # Check if the request was successful
                if response.status_code == 200:
                    # Parse the HTML content
                    soup = BeautifulSoup(response.text, "html.parser")

                    # Search for and extract specific data
                    # For example, extract all the links on the page
                    #links = soup.find_all("a")
                    #paragraphs = soup.find_all("p", string=lambda string: string and "http" not in string)
                    all_text = soup.get_text()
                    pattern = r'\b[ab]\.\s+(.*?)\n'
                    examples = re.findall(pattern, all_text, re.DOTALL)

                    #for example in examples:
                        #print(example.strip())
                    # Print the links
                    #for words in paragraphs:
                        #print("Link Text:", words.text)
                        #print("Link URL:", words.get("href"))

                # Close the HTTP connection
                response.close()
                return render_template("random_spanish.html", random_word=random_word, translate_word=translate_word_final)
            else:
                print("444333")
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