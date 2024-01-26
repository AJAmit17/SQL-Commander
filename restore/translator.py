import deep_translator
import pyttsx3
import os 
import dotenv

dotenv.load_dotenv()

import google.generativeai as genai 

genai.configure(api_key=os.getenv("GOOGLE_GEMINI_API_KEY"))


def test1():
    model = deep_translator.GoogleTranslator(
    source="auto",
    target="en"
    )

    engine = pyttsx3.init()

    ans = model.translate("nima hesarenu")

    ans2 = model.translate("kya hai ye?")

    engine.say(ans)
    
    engine.runAndWait()
    engine.stop()

    print(ans)
    print(ans2)
    

def test2():
    model = deep_translator.GoogleTranslator(
    source="auto",
    target="en"
    )
    
    ans = "kya hai ye?"
    prompt = "Auto detect the lnaguage of input and translate the given language from respective asked language"
    model = genai.GenerativeModel('gemini-pro')
    response = model.generate_content([prompt, ans])
    
    print(response)
test2()