import os
import speech_recognition as sr
import dialogflow
from pydub import AudioSegment
from pydub.playback import play


from google.api_core.exceptions import InvalidArgument

DIALOGFLOW_PROJECT_ID = 'medibot-vdkbdh'
DIALOGFLOW_LANGUAGE_CODE = 'en-US'
GOOGLE_APPLICATION_CREDENTIALS = 'medibot-vdkbdh-066528734230.json'
SESSION_ID = 'dadc1'
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] ="D:\\Python Projects\\Jenny\\medibot-vdkbdh-066528734230.json"





def takeCommand():
    #It takes microphone input from the user and returns string output

    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.adjust_for_ambient_noise(source)
        
        r.pause_threshold = 1
        audio = r.listen(source)

    try:
        print("Recognizing...")    

        query = r.recognize_google(audio, language='en-in')
        print(f"User said: {query}\n")

    except Exception as e:
        # print(e)    
        print("Say that again please...")  
        return "None"
    return query



while True:


    query = takeCommand().lower()
    

    

    text_to_be_analyzed = query
    session_client = dialogflow.SessionsClient()
    session = session_client.session_path(DIALOGFLOW_PROJECT_ID, SESSION_ID)
    text_input = dialogflow.types.TextInput(text=text_to_be_analyzed, language_code=DIALOGFLOW_LANGUAGE_CODE)
    query_input = dialogflow.types.QueryInput(text=text_input)
    try:
        response = session_client.detect_intent(session=session, query_input=query_input)
    except InvalidArgument:
        raise
    print("Query text:", response.query_result.query_text)
    print("Detected intent:", response.query_result.intent.display_name)
    print("Detected intent confidence:", response.query_result.intent_detection_confidence)
    print("Fulfillment text:", response.query_result.fulfillment_text)



    with open('speak.wav' , 'wb') as out:
        out.write(response.output_audio)
        print('Audio content written to file "speak.wav"')

    #os.system("cvlc --play-and-exit C:\\Users\\Rajesh\\Desktop\\jenny\\speak.wav")
        
    song=AudioSegment.from_wav("speak.wav")
    play(song)
