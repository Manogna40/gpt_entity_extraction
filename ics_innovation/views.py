from django.http import FileResponse,JsonResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import render
from .forms import UploadEntityExtractor
from .models import EntityExtractorV1
import requests as req
import json
import openai
import os
os.environ['https_proxy'] = 'http://eu-chst-proxy.eu.novartis.net:2011'


env = "prod"
model_name ='gpt'
@api_view(["GET"])
def get_extracted_data(request):
    json_ = []
    api_response=''

    if env == "dev":
        json_ = [
            {
                'entity': 'BRAND',
                'expected_values': [
                    {'end_pos': 513, 'start_pos': 503, 'type': 'BRAND', 'value': 'Ioana Nita'}, {'end_pos': 594, 'start_pos': 574, 'type': 'BRAND', 'value': 'Grigore Alexandrescu'}]}, {'entity': 'FORM', 'expected_values': [{'end_pos': 68, 'start_pos': 62, 'type': 'FORM', 'value': 'Tablet'}, {'end_pos': 106, 'start_pos': 90, 'type': 'FORM', 'value': 'Powder for fever'}, {'end_pos': 187, 'start_pos': 186, 'type': 'FORM', 'value': '.'}, {'end_pos': 243, 'start_pos': 242, 'type': 'FORM', 'value': '.'}, {'end_pos': 367, 'start_pos': 366, 'type': 'FORM', 'value': '.'}, {'end_pos': 397, 'start_pos': 396, 'type': 'FORM', 'value': '.'}, {'end_pos': 539, 'start_pos': 514, 'type': 'FORM', 'value': 'Senior Regulatory Affairs'}]}, {'entity': 'STRENGTH', 'expected_values': [{'end_pos': 48, 'start_pos': 40, 'type': 'STRENGTH', 'value': '500mg/mL'}, {'end_pos': 61, 'start_pos': 53, 'type': 'STRENGTH', 'value': '100mg/mL'}, {'end_pos': 122, 'start_pos': 121, 'type': 'STRENGTH', 'value': '-'}, {'end_pos': 126, 'start_pos': 122, 'type': 'STRENGTH', 'value': '1000'}, {'end_pos': 127, 'start_pos': 126, 'type': 'STRENGTH', 'value': '-'}, {'end_pos': 131, 'start_pos': 127, 'type': 'STRENGTH', 'value': '1000'}]}, {'entity': 'NAME', 'expected_values': [{'end_pos': 122, 'start_pos': 117, 'type': 'NAME', 'value': 'A200-'}, {'end_pos': 501, 'start_pos': 492, 'type': 'NAME', 'value': 'John Cena'}, {'end_pos': 513, 'start_pos': 503, 'type': 'NAME', 'value': 'Ioana Nita'}]}, {'entity': 'ADDRESS', 'expected_values': [{'end_pos': 573, 'start_pos': 522, 'type': 'ADDRESS', 'value': 'Regulatory Affairs Associate Metropolis Center, Str'}]}, {'entity': 'SUBJID', 'expected_values': [{'end_pos': 131, 'start_pos': 117, 'type': 'SUBJID', 'value': 'A200-1000-1000'}]}, {'entity': 'AGE', 'expected_values': [{'end_pos': 390, 'start_pos': 388, 'type': 'AGE', 'value': '25'}]}, {'entity': 'DATE', 'expected_values': [{'end_pos': 366, 'start_pos': 353, 'type': 'DATE', 'value': '2nd June 2022'}]}, {'entity': 'COUNTRY', 'expected_values': [{'end_pos': 632, 'start_pos': 625, 'type': 'COUNTRY', 'value': 'Romania'}]}, {'entity': 'EMAIL', 'expected_values': [{'end_pos': 286, 'start_pos': 266, 'type': 'EMAIL', 'value': 'patient123@email.com'}]}, {'entity': 'HEIGHT', 'expected_values': [{'end_pos': 242, 'start_pos': 236, 'type': 'HEIGHT', 'value': '182 cm'}]}, {'entity': 'MEDICAL HISTORY', 'expected_values': [{'end_pos': 446, 'start_pos': 441, 'type': 'MEDICAL HISTORY', 'value': 'fever'}, {'end_pos': 463, 'start_pos': 451, 'type': 'MEDICAL HISTORY', 'value': 'hypertension'}, {'end_pos': 439, 'start_pos': 435, 'type': 'MEDICAL HISTORY', 'value': 'cold'}, {'end_pos': 508, 'start_pos': 503, 'type': 'MEDICAL HISTORY', 'value': 'Ioana'}, {'end_pos': 531, 'start_pos': 514, 'type': 'MEDICAL HISTORY', 'value': 'Senior Regulatory'}, {'end_pos': 463, 'start_pos': 451, 'type': 'MEDICAL HISTORY', 'value': 'hypertension'}, {'end_pos': 446, 'start_pos': 441, 'type': 'MEDICAL HISTORY', 'value': 'fever'}]}, {'entity': 'PHONE', 'expected_values': [{'end_pos': 325, 'start_pos': 310, 'type': 'PHONE', 'value': ' +91-8876291892'}, {'end_pos': 677, 'start_pos': 660, 'type': 'PHONE', 'value': ' +40 37 26 22 399'}, {'end_pos': 655, 'start_pos': 638, 'type': 'PHONE', 'value': ' +40 31 22 53 000'}, {'end_pos': 325, 'start_pos': 311, 'type': 'PHONE', 'value': '+91-8876291892'}]},
            {'entity': 'SITEID', 'expected_values': [{'end_pos': 126, 'start_pos': 122, 'type': 'SITEID', 'value': '1000'}, {
                'end_pos': 131, 'start_pos': 127, 'type': 'SITEID', 'value': '1000'}]},
            {
                'entity': 'WEIGHT', 'expected_values': [
                    {'end_pos': 221, 'start_pos': 216,
                    'type': 'WEIGHT', 'value': '23 kg'}
                ]
            },
            {
                "entity": "SUBJID",
                "expected_values": []
            }
        ]
    if env == "vdi":
        latest_doc = EntityExtractorV1.objects.order_by("-pk")[0]
        url = "http://10.185.56.168:8051/entities"
        resp = req.post(url, json={
            "input_text": latest_doc.extracted_text,
            "entity_types": latest_doc.entities
        })
        json_ = resp.json()

    if env == "prod":
        latest_doc = EntityExtractorV1.objects.order_by("-pk")[0]
        if latest_doc.category == 'Custom' and model_name == 'fastchat':
            url = "http://10.185.56.168:8051/fast_chat"
            resp = req.post(url, json={
                "user_inputs": latest_doc.extracted_text,
                "entity_list": latest_doc.entities.split(',')
            })
            try:
                print('resp.text',resp.text)
                resp_js = json.loads(resp.text)
                api_response = resp_js['model_output']
                json_resp = json.loads(resp_js['json_object'])
                # res_json = change_json_format(json.loads(json_resp['outputs']),latest_doc.entities)
                res_json = change_json_format(json_resp,latest_doc.entities)
                json_ = res_json
            except json.JSONDecodeError as e:
                print('in errr')
                return Response({"data": json_,'api_response':resp_js['model_output']})
        if model_name == 'gpt' and latest_doc.category == 'Custom':
            gpt_response = get_response_from_gpt(latest_doc.extracted_text,latest_doc.entities)
            gpt_json = json.loads(gpt_response)
            res_json = change_json_format(gpt_json,latest_doc.entities)
            json_ = res_json
            return Response({"data": json_,'api_response':gpt_response})

        else:
            url = "http://localhost:8051/entities"
            resp = req.post(url, json={
                "input_text": latest_doc.extracted_text,
                "entity_types": latest_doc.entities
            })
            url = "http://10.185.56.168:9991/hunflairentities"
            resp_2 = req.post(url, json={
                "user_inputs": latest_doc.extracted_text
            })
            req_json2 = resp_2.json()
            res_json = change_json_format(req_json2,latest_doc.entities)
            json_ = resp.json()
            json_.extend(res_json)
    return Response({"data": json_,'api_response':api_response})

@api_view(["GET"])
def get_extracted_text(request):
    latest_doc = EntityExtractorV1.objects.order_by("-pk")[0]
    return Response(latest_doc.extracted_text)


@api_view(["GET", "POST"])
def upload_page(request):
    if request.method == "GET":
        context = {'no_of_inputs':[1,2,3,4]}
        return render(request, 'ui_upload.html', context=context)
    if request.method == "POST":
        request.POST._mutable = True
        category = request.POST.getlist("category")
        request.POST.update(
            {"entities": ",".join(en for en in request.POST.getlist("entities") if len(en) > 1 )})
        form = UploadEntityExtractor(request.POST, request.FILES)
        if form.is_valid():
            form = form.save()
            form.save()
            json = [
                {
                    'entity': 'BRAND',
                    'expected_values': [
                        {'end_pos': 513, 'start_pos': 503, 'type': 'BRAND', 'value': 'Ioana Nita'}, {'end_pos': 594, 'start_pos': 574, 'type': 'BRAND', 'value': 'Grigore Alexandrescu'}]}, {'entity': 'FORM', 'expected_values': [{'end_pos': 68, 'start_pos': 62, 'type': 'FORM', 'value': 'Tablet'}, {'end_pos': 106, 'start_pos': 90, 'type': 'FORM', 'value': 'Powder for fever'}, {'end_pos': 187, 'start_pos': 186, 'type': 'FORM', 'value': '.'}, {'end_pos': 243, 'start_pos': 242, 'type': 'FORM', 'value': '.'}, {'end_pos': 367, 'start_pos': 366, 'type': 'FORM', 'value': '.'}, {'end_pos': 397, 'start_pos': 396, 'type': 'FORM', 'value': '.'}, {'end_pos': 539, 'start_pos': 514, 'type': 'FORM', 'value': 'Senior Regulatory Affairs'}]}, {'entity': 'STRENGTH', 'expected_values': [{'end_pos': 48, 'start_pos': 40, 'type': 'STRENGTH', 'value': '500mg/mL'}, {'end_pos': 61, 'start_pos': 53, 'type': 'STRENGTH', 'value': '100mg/mL'}, {'end_pos': 122, 'start_pos': 121, 'type': 'STRENGTH', 'value': '-'}, {'end_pos': 126, 'start_pos': 122, 'type': 'STRENGTH', 'value': '1000'}, {'end_pos': 127, 'start_pos': 126, 'type': 'STRENGTH', 'value': '-'}, {'end_pos': 131, 'start_pos': 127, 'type': 'STRENGTH', 'value': '1000'}]}, {'entity': 'NAME', 'expected_values': [{'end_pos': 122, 'start_pos': 117, 'type': 'NAME', 'value': 'A200-'}, {'end_pos': 501, 'start_pos': 492, 'type': 'NAME', 'value': 'John Cena'}, {'end_pos': 513, 'start_pos': 503, 'type': 'NAME', 'value': 'Ioana Nita'}]}, {'entity': 'ADDRESS', 'expected_values': [{'end_pos': 573, 'start_pos': 522, 'type': 'ADDRESS', 'value': 'Regulatory Affairs Associate Metropolis Center, Str'}]}, {'entity': 'SUBJID', 'expected_values': [{'end_pos': 131, 'start_pos': 117, 'type': 'SUBJID', 'value': 'A200-1000-1000'}]}, {'entity': 'AGE', 'expected_values': [{'end_pos': 390, 'start_pos': 388, 'type': 'AGE', 'value': '25'}]}, {'entity': 'DATE', 'expected_values': [{'end_pos': 366, 'start_pos': 353, 'type': 'DATE', 'value': '2nd June 2022'}]}, {'entity': 'COUNTRY', 'expected_values': [{'end_pos': 632, 'start_pos': 625, 'type': 'COUNTRY', 'value': 'Romania'}]}, {'entity': 'EMAIL', 'expected_values': [{'end_pos': 286, 'start_pos': 266, 'type': 'EMAIL', 'value': 'patient123@email.com'}]}, {'entity': 'HEIGHT', 'expected_values': [{'end_pos': 242, 'start_pos': 236, 'type': 'HEIGHT', 'value': '182 cm'}]}, {'entity': 'MEDICAL HISTORY', 'expected_values': [{'end_pos': 446, 'start_pos': 441, 'type': 'MEDICAL HISTORY', 'value': 'fever'}, {'end_pos': 463, 'start_pos': 451, 'type': 'MEDICAL HISTORY', 'value': 'hypertension'}, {'end_pos': 439, 'start_pos': 435, 'type': 'MEDICAL HISTORY', 'value': 'cold'}, {'end_pos': 508, 'start_pos': 503, 'type': 'MEDICAL HISTORY', 'value': 'Ioana'}, {'end_pos': 531, 'start_pos': 514, 'type': 'MEDICAL HISTORY', 'value': 'Senior Regulatory'}, {'end_pos': 463, 'start_pos': 451, 'type': 'MEDICAL HISTORY', 'value': 'hypertension'}, {'end_pos': 446, 'start_pos': 441, 'type': 'MEDICAL HISTORY', 'value': 'fever'}]}, {'entity': 'PHONE', 'expected_values': [{'end_pos': 325, 'start_pos': 310, 'type': 'PHONE', 'value': ' +91-8876291892'}, {'end_pos': 677, 'start_pos': 660, 'type': 'PHONE', 'value': ' +40 37 26 22 399'}, {'end_pos': 655, 'start_pos': 638, 'type': 'PHONE', 'value': ' +40 31 22 53 000'}, {'end_pos': 325, 'start_pos': 311, 'type': 'PHONE', 'value': '+91-8876291892'}]},
                {'entity': 'SITEID', 'expected_values': [{'end_pos': 126, 'start_pos': 122, 'type': 'SITEID', 'value': '1000'}, {
                    'end_pos': 131, 'start_pos': 127, 'type': 'SITEID', 'value': '1000'}]},
                {
                    'entity': 'WEIGHT', 'expected_values': [
                        {'end_pos': 221, 'start_pos': 216,
                         'type': 'WEIGHT', 'value': '23 kg'}
                    ]
                },
                {
                    "entity": "SUBJID",
                    "expected_values": []
                }
            ]
            context = {
                "page": "preview",
                "response": json,
                "staticpath": form.staticpath,
                "extracted_text": form.extracted_text

            }
            return render(request, 'ui_review.html', context=context)
    return Response(status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET"])
def review_page(request):
    latest_doc = EntityExtractorV1.objects.order_by("-pk")[0]
    context = {
        "staticpath": latest_doc.staticpath
    }
    return render(request, 'ui_review.html', context=context)


def change_json_format(resp_json,entities):
    print('entities',entities)
    print(resp_json)
    result_json = []
    for ent,values in resp_json.items():
        print("$$$$",entities.lower() +','+entities.lower().replace(' ','_')+','+entities.lower().replace(' ','').lower())
        if ent.lower() in entities.lower() +','+entities.lower().replace(' ','_')+','+entities.lower().replace(' ','').lower() :
            temp_json = {}
            temp_json['entity'] = ent
            if type(values) is list:
                temp_json['expected_values'] =[{'value': val } for val in values ]
            elif isinstance(values, (int, float)):
                temp_json['expected_values'] =[{'value': values }]
            elif ',' in values:
                temp_json['expected_values'] =[{'value': val } for val in values.split(',') ]
            else:
                temp_json['expected_values'] =[{'value': values }]
            result_json.append(temp_json)
    return result_json


def get_response_from_gpt(current_data,selected_entites):
    if env=='prod':
        # prompt = 'Redact {},{} from the following text:{}'.format(selected_entites,custom_entities,current_data)
        prompt = 'extract {} entities from the following text:{} and return output in json'.format(selected_entites,current_data)
        openai.api_key = 'Your_api_key'
        print(prompt)
        messages = []
        messages.append({"role": "system", "content": "You are a helpful assistant."})
        question = {}
        question['role'] = 'user'
        question['content'] = prompt
        messages.append(question)
        response = openai.ChatCompletion.create(model="gpt-3.5-turbo",messages=messages)
        try:
            data = response['choices'] [0] ['message'] ['content']
        except:
            data = 'Oops you beat the AI, try a different question, if the problem persists, come back later.'
        return data