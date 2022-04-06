import pyttsx3
import speech_recognition as sr
import re
import classCovid

API_KEY = "tTTh-szq1A1e"
PROJECT_TOKEN = "tf8Rk7ipTpvT"
RUN_TOKEN = "tOKHy7yuVCTV"

# read text from the speaker
def speak(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()

# write what u said
def get_audio():
    # setup recogrizer
    talk = sr.Recognizer()

    #setup microphone
    with sr.Microphone() as source:
        print('start... ')
        audio = talk.listen(source)
        said = ""
        try:
            # recognize the record and return it in a text format
            said = talk.recognize_google(audio)

        except Exception as e:
            print("Exception: ",str(e))
    return said.lower()





def main():
    data = classCovid.CovidData(API_KEY,PROJECT_TOKEN)
    print("Started Program")
    END_PHRASE = "stop"
    country_list = data.get_list_of_countries()
    UPDATE_COMMAND = "update"
    TOTAL_PATTERNS = {
                        re.compile("[\w\s]+ total [\w\s]+ cases"):data.get_total_cases,
                        re.compile("[\w\s]+ total cases"): data.get_total_cases,
                        re.compile("[\w\s]+ total [\w\s]+ deaths"): data.get_total_deaths,
                        re.compile("[\w\s]+ total deaths"): data.get_total_deaths
					}
    COUNTRY_PATTERNS = {
                        re.compile("[\w\s]+ cases [\w\s]+"): lambda country: data.get_country_data(country)['total_cases'],
                        re.compile("[\w\s]+ deaths [\w\s]+"): lambda country: data.get_country_data(country)['total_deaths'],
                    }

    while True:
        text = get_audio()
        print(text)
        result = None

        for pattern, func in COUNTRY_PATTERNS.items():
            if pattern.match(text):
                words = set(text.split(" "))
                for country in country_list:
                    if country in words:
                        result = func(country)
                        break

        for pattern, func in TOTAL_PATTERNS.items():
            if pattern.match(text):
                result = func()
                break

        if text == UPDATE_COMMAND:
            result = "Data is being updated. This may take a moment!"
            data.update_data()

        if result:
            speak(result)

        if text.find(END_PHRASE) != -1:  # stop loop
            print("Exit")
            break


main()