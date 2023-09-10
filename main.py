from flask import Flask, render_template, request, redirect, url_for, jsonify
import project4
import requests
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
            api_url = f"https://www.dictionaryapi.com/api/v3/references/spanish/json/{random_word}?key={MERIAM_WEBSTER_API_KEY}"
            response = requests.get(api_url)
            data = response.json()
            print("11111")
            if type(data[0]) is not dict:
                print("2222")
                result = generate_word()
                return result
            else:
                if len(data[0]['shortdef']) > 1:
                    translate_word1 = data[0]['shortdef'][0]
                    #if ":" in translate_word1:
                        #ranslate_word1 = ""
                    print(translate_word1, "33333")
                    translate_word2 = data[0]['shortdef'][1]
                    #if ":" in translate_word2:
                        #translate_word2 = ""
                    translate_word_final = translate_word1.capitalize() + "/" + translate_word2.capitalize()
                    if ":" in translate_word1:
                        translate_word_final = translate_word2
                    if ":" in translate_word2:
                        translate_word_final = translate_word1
                    #if ": " in translate_word_final:
                        #word = translate_word_final
                        #for i in range(len(translate_word_final)):
                            #print(i)
                            #if word[i] != ":":
                                #word = word[:i] + word[i + 1:]
                            #else:
                                #break
                    print(translate_word_final, "444222")
                        #translate_word_final = word
                else:
                    translate_word_final = data[0]['shortdef'][0].capitalize()
                    print(translate_word_final, "4444")
            if random_word[0].islower():
                ###GET THE DEFINITION FROM SPANISH DICTIONARY HERE###
                print("55555")
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