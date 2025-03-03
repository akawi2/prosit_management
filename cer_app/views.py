import datetime
import json
import os
from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.views.decorators.csrf import csrf_exempt
import google.generativeai as genai
import docx
import pdfplumber


# Create your views here.
def index(request):
    return render(request, 'prosit_retour_app/index.html')


def readWordFile(file):
    if file.content_type in ['application/msword', 'application/vnd.openxmlformats-officedocument.wordprocessingml.document']:
        
        # Read the content of the Word document
        try:
            doc = docx.Document(file)
            file_content = "\n".join([para.text for para in doc.paragraphs])
            print('content extracted successfully')
            return {'content': file_content.strip()}

        except Exception as e:
            return {'error': str(e)}
    

    else:
        return {'error': 'Invalid file type. Please upload a Word or PDF document.'}
    
    
def readPdfFile(file):
    text = ""
    with pdfplumber.open(file) as pdf:
        for page in pdf.pages:
            text += page.extract_text()
    return {'content': text.strip()}

def prompt(message):
        genai.configure(api_key=os.getenv('API_KEY'))

        # Create the model
        generation_config = {
        "temperature": 1,
        "top_p": 0.95,
        "top_k": 40,
        "max_output_tokens": 8192,
        "response_mime_type": "application/json",
        }

        model = genai.GenerativeModel(
        model_name="gemini-2.0-flash",
        generation_config=generation_config,
        )

        chat_session = model.start_chat(
        history=[
        ]
        )

        response = chat_session.send_message(message)
        
        return response.text

@csrf_exempt
def generateCER(request):


    if request.method == 'POST':
        if 'file' not in request.FILES:
            return JsonResponse({'error': 'No file uploaded.'}, status=400)
            
        uploaded_file = request.FILES['file']
        
        try:
            doc = readWordFile(uploaded_file)
            docContent = doc['content']
        except:
            doc = readPdfFile(uploaded_file)
            docContent = doc['content']
        
        request.session['response'] = prompt("""
        Tu es un étudiant studieux et tu dois réaliser ton Cahier d'étude et de recherche. Tu dois te baser sur un élément appelé « prosit aller », contenant les informations sur le sujet en question. Tu dois réaliser ton cahier d'étude et recherche sous la forme du JSON suivant, en tenant compte de ce qui a été mentionné dans le prosit aller. La forme de réponse est comme suit :
        {
        "cer": {
            titre: "",
            "mots_cles": [
            {
                "mot": "",
                "definition": ""
            }
            ],
            "contexte": "",
            "besoins": [],
            "contraintes": []
            "generalite": "",
            "problematique": "",
            "plan_d_action": [],
            "pistes_de_solutions": [],
        }
        }
        Voici le prosit aller en question : [insérer le prosit aller ici]"""+
        docContent+
        """
        Le titre du Prosit est celui qui est donné qu debut ne l'imagine pas.
        Rassure-toi de maintenir la forme du JSON et de ne pas créer une forme inconnue.
        Lorsque tu definis les mots cles, fais le en fonction du contexte et donne la definition avec un minimum de detail.

        """)
                
        return redirect('cer_presentation')

@csrf_exempt
def generateRetour(request):
    if request.method == 'POST':
        if 'file1' not in request.FILES:
            return JsonResponse({'error': 'No file uploaded.'}, status=400)
        
        uploaded_file = request.FILES['file1']
        
        try:
            doc = readWordFile(uploaded_file)
            docContent = doc['content']
        except:
            doc = readPdfFile(uploaded_file)
            docContent = doc['content']

        
        request.session['response'] = prompt("""
        Tu es un étudiant studieux et tu dois réaliser ton Cahier d'étude et de recherche. Tu dois te baser sur un élément appelé « prosit aller », contenant les informations sur le sujet en question. Tu dois réaliser ton cahier d'étude et recherche sous la forme du JSON suivant, en tenant compte de ce qui a été mentionné dans le prosit aller. La forme de réponse est comme suit :
        {
        "cer": {
            titre: "",
            "mots_cles": [
            {
                "mot": "",
                "definition": ""
            }
            ],
            "contexte": "",
            "besoins": [],
            "contraintes": [],
            "generalite": "",
            "problematique": "",
            "plan_d_action": [],
            "pistes_de_solutions": [],
        }
        }
        Voici le prosit aller en question : [insérer le prosit aller ici]"""+
        docContent+
        """
        Le titre du Prosit est celui qui est donné qu debut ne l'imagine pas.
        Rassure-toi de maintenir la forme du JSON et de ne pas créer une forme inconnue.
        Lorsque tu definis les mots cles, fais le en fonction du contexte et donne la definition avec un minimum de detail.

        """)
                
        return redirect('retour_presentation')
        
def cer_presentation(request):
    data_str = request.session.get('response')
    data = json.loads(data_str) 
    print(data)
    print(type(data))
    titre = data['cer']['titre']
    motCles = data['cer']['mots_cles']
    contexte = data['cer']['contexte']
    besoins = data['cer']['besoins']
    contraintes = data['cer']['contraintes']
    generalite = data['cer']['generalite']
    problematique = data['cer']['problematique']
    pistes_de_solutions = data['cer']['pistes_de_solutions']
    plan_d_action = data['cer']['plan_d_action']
    
    return render(request, 'prosit_retour_app/cer_presentation.html', {'titre': titre,'motCles': motCles, 'contexte':contexte, 'besoins': besoins, 'contraintes': contraintes,'generalite': generalite, 'problematique': problematique, 'piste_de_solution': pistes_de_solutions, 'plan_d_action':plan_d_action})    

    
 
# def cer_presentation(request):
#     data_str = request.session.get('response')
#     data = json.loads(data_str) 
#     print(data)
#     print(type(data))
#     titre = data['cer']['titre']
#     motCles = data['cer']['mots_cles']
#     contexte = data['cer']['contexte']
#     besoins = data['cer']['besoins']
#     generalite = data['cer']['generalite']
#     problematique = data['cer']['problematique']
#     pistes_de_solutions = data['cer']['pistes_de_solutions']
#     plan_d_action = data['cer']['plan_d_action']
    
#     return render(request, 'prosit_retour_app/cer_presentation.html', {'titre': titre,'motCles': motCles, 'contexte':contexte, 'besoins': besoins, 'generalite': generalite, 'problematique': problematique, 'piste_de_solution': pistes_de_solutions, 'plan_d_action':plan_d_action})    

def retour_presentation(request):
    current_date = datetime.datetime.now()
    formatted_date = current_date.strftime("%d/%m/%Y")
    
    data_str = request.session.get('response')
    data = json.loads(data_str) 
    print(data)
    print(type(data))
    titre = data['cer']['titre']
    motCles = data['cer']['mots_cles']
    contexte = data['cer']['contexte']
    besoins = data['cer']['besoins']
    contraintes = data['cer']['contraintes']
    generalite = data['cer']['generalite']
    problematique = data['cer']['problematique']
    pistes_de_solutions = data['cer']['pistes_de_solutions']
    plan_d_action = data['cer']['plan_d_action']
    
    return render(request, 'prosit_retour_app/retour_presentation.html', {'date': formatted_date, 'titre': titre,'motCles': motCles, 'contexte':contexte, 'besoins': besoins, 'contraintes': contraintes,'generalite': generalite, 'problematique': problematique, 'piste_de_solution': pistes_de_solutions, 'plan_d_action':plan_d_action})    
    