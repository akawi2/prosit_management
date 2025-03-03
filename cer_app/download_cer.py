from io import BytesIO
import os
import re

from django.http import HttpResponse, JsonResponse
from pptx import Presentation
from docxtpl import DocxTemplate
from django.views.decorators.csrf import csrf_exempt
from prosit_management import settings

def remove_special_characters(input_string):
    # Regular expression to match non-alphanumeric characters (excluding spaces)
    cleaned_string = re.sub(r'[^a-zA-Z0-9\s]', '', input_string)
    return cleaned_string.strip()

@csrf_exempt
def downloadCER(request):
    if request.method == 'POST':
        template = request.POST.get('template')

        if(template is None):
            print(template)
            return JsonResponse({'error': 'Please select a template.'}, status=400)
        
        titre = request.POST.get('titre')
        name = request.POST.get('name')
        contexte = request.POST.get('contexte')
        problematique = request.POST.get('problematique')
        generalite = request.POST.get('generalite')
        besoins = []
        contraintes = []
        pisteDeSolutions = []
        planDActions = []
        motCles = []
        definitions = []
        
        for key in request.POST:
            if key.startswith('besoin_'):
                besoins.append(request.POST[key])
                
        for key in request.POST:
            if key.startswith('mot_'):
                motCles.append(request.POST[key])
                        
        for key in request.POST:
            if key.startswith('definition_'):
                definitions.append(request.POST[key])
            
        for key in request.POST:
            if key.startswith('contrainte'):
                contraintes.append(request.POST[key])
                    
        for key in request.POST:
            if key.startswith('piste'):
                pisteDeSolutions.append(request.POST[key])
        
        for key in request.POST:
            if key.startswith('plan'):
                planDActions.append(request.POST[key])
        
        
        motDefinitions = [{'mot': motCles[i], 'definition': definitions[i]} for i in range(len(motCles))]
        print(motDefinitions)
        print(motCles)
        print(definitions)
        data = {
            'name': name,
            'titre': titre,
            'TITRE': titre,
            'mot_cles': motDefinitions,
            'contexte': contexte,
            'problematique': problematique,
            'generalite': generalite,
            'besoin': besoins,
            'contrainte': contraintes,
            'piste_de_solution': pisteDeSolutions,
            'plan_d_action': planDActions,
        }
        
        template_path = os.path.join(settings.BASE_DIR, 'prosit_management', 'doc_template', f'{template}.docx')

        doc = DocxTemplate(template_path)
        doc.render(data)
        # Save the document to a response
        response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.wordprocessingml.document')
        response['Content-Disposition'] = f'attachment; filename="CER {remove_special_characters(titre)}.docx"'
        print(response['Content-Disposition'])
        doc.save(response)  
        return response
