from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from random import randint
import subprocess
import os
from django.core.mail import send_mail
from .models import feedbackForm
from django.conf import settings


# Create your views here.
def index(request):
    return render(request,'home/index.html')

def run_program(file_path,file_name, program_type, input_data=None):
    if program_type == 'py':
        process = subprocess.Popen(['python', file_path+file_name], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        output, error = process.communicate(input_data.encode() if input_data else None)
        return output.decode(), error.decode()

    else:
        return "Invalid program type"

@csrf_exempt
def code(request):
    language = request.POST['language']
    code = str(request.POST['code'])
    file_name=""
    file_path = "home/programs/"
    if language == "java":
        num = randint(0,1000000000)
        file_name = "MainClass"+str(num)+"."+language
        if "MainClass" in code:
            code = code.replace("MainClass","MainClass"+str(num),1)
        else:
            return JsonResponse({"output":"Error: Please specify main class name as MainClass","error":""})
    else:
        file_name=language+str(randint(0,1000000000))+"."+language

    with open (file_path+file_name,"w") as file:
        file.write(code)
    input_data = request.POST['input']
    output,error = run_program(file_path,file_name, language,input_data)

    if language == 'java':
        os.remove(file_path+file_name)
        os.remove(file_path+file_name.replace('.java','.class'))
    else:
        os.remove(file_path+file_name)
    return JsonResponse({"output":output,"error":error})

def send_feedback_email(name, email, message):
    pass
    
def send_response(name, email):
    pass

@csrf_exempt
def feedback(request):
    if request.method =='POST':
        pass


