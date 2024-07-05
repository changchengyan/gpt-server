


def openAiKeyConfig():
    return  "OPENAI_API_KEY"

def fileUploadPromotConfig():
    return  '''
            Hi! Could you work for me as an assistant to give me the JSON output? I will give you a PDF, an image or text. You need to extract 4 key information of the PDF, image or text.The 4 key information are: Contract Party (service firm of the Contract), Contract Number , Quitting Party name( name of the people who own the contract, include first name and last name），Quitting Party Birthdate (birthdate of the people who own the contract). If you could not find any kind of key information, give me other information that you get. Bsides, could you identify the language the 
         a PDF, an image or text used is German or English, and give me JSON output in the same language of the input and add a string to the JSON to indicate the language of the contract
        Example JSON output:
            {
              "Contract Party": "Fitness First Germany GmbH",
              "Contract Number": "LFG79-930670021",
              "Quitting Party name": "John Doe",
              "Quitting Party Birthdate": "01-06-2000"
               "lang": "en"
            }
            or
            {
              "Vertragspartner": "Fitness First Germany GmbH",
              "Vertragsnummer": "LFG79-93022011",
              "Kündigende Partei Name": "Mohan Zhu",
              "Geburtsdatum der kündigenden Partei": "23.06.2001"
              "lang": "de"
            }
'''

def  textPromotConfig(text):
    prex_str =   '''
           
                Hi! Could you work for me as an assistant to give me the JSON output? Here is my text:
            '''
            
            
    after = ''',You need to extract 4 key information of the text.The 4 key information are: Contract Party (service firm of the Contract), Contract Number , Quitting Party name( name of the people who own the contract, include first name and last name），Quitting Party Birthdate (birthdate of the people who own the contract). If you could not find any kind of key information, give me other information that you get. Bsides, could you identify the language the 
         the text used is German or English, and give me JSON output in the same language of the input and add a string to the JSON to indicate the language of the contract
        Example JSON output:
            {
            "Contract Party": "Fitness First Germany GmbH",
              "Contract Number": "LFG79-93666",
              "Quitting Party name": "John Doe",
              "Quitting Party Birthdate": "01-06-2000"
               "lang": "en"
            }
            or
            {
            "Vertragspartner": "Fitness First Germany GmbH",
              "Vertragsnummer": "93067999",
              "Kündigende Partei Name": "Mohan Zhu",
              "Geburtsdatum der kündigenden Partei": "23.06.2001"
              "lang": "de"
            }

            '''
    
    return    prex_str+text+after




         

def name2signaturePic(res):

    name = ""

    if res.get('lang') == 'de':
        name = res.get('Kündigende Partei Name')
    else:
        name = res.get("Quitting Party name")? if res.get("Quitting Party name")!=None else res.get('Quitting Party Name')     


    return f"A simple handwritten signature with the name:{name} on a white background, in a clean and legible handwriting style similar to the provided example. The signature should be centered and use the same handwriting style as shown., 'size': '1024x1024', 'n': 1"


def fixedContent(lang="en"):
    if lang == "de":
        return [
        "Hiermit kündige ich meinen Vertrag zum nächstmöglichen Zeitpunkt.",
        "Bitte senden Sie mir eine schriftliche Bestätigung der Kündigung unter Angabe des",
        "Kündigungsdatums.",
        ]
    else:
        return [
        "I hereby give notice of termination of my contract with effect from the next",
        "possible date.Please send me a written confirmation of the termination stating",
        "the date of termination."
        ]


def transGreetings(lang="en"):
    if lang == "de":
        return [
            "Hello", "Hi", "Good morning", "Good afternoon", "Good evening"
        ]
    else:
        return [
            "Hello", "Hi", "Good morning", "Good afternoon", "Good evening"
        ]