from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.template.loader import get_template
from django.core.files.storage import FileSystemStorage
from django.views.decorators.csrf import csrf_exempt
import base64, json
import datetime, pandas as pd

# Create your views here.

def index(request):
    print('Inside GET')
    html = get_template('upload.html')
    return HttpResponse(html.render({}))

def report(request):
    print('Inside GET')
    html = get_template('report.html')
    return HttpResponse(html.render({}))

@csrf_exempt
def upload(request):
    print('inside upload')
    data = {'success': False}
    if request.method=='POST':
        file = request.FILES['file']
        team = request.POST.get('team')
        file_name = file.name
        print(file_name)
        print(team)
        try:
            handle_uploaded_file(file, team)
            data.update({"success": True})
        except Exception as e:
            print(str(e))
            # data.update({"success": True})

    return JsonResponse(data)

def handle_uploaded_file(f, team):
    with open('static/files/'+ team+'_'+f.name, 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)

    # create log
    with open("static/files/logfile.csv", "a") as myfile:
        myfile.write("%s,%s,%s\n"%(str(datetime.datetime.now().strftime("%I:%M%p, %B %d, %Y")), str(team), str(f.name)))

    destination.close()
    myfile.close()


@csrf_exempt
def get_report(request):
    df = pd.read_csv('static/files/logfile.csv')
    # df.index.name = 'Sr No.'
    # df.index.set_names(names= 'Sr No', level=0, inplace=True)
    table = df.to_html(classes='table table-stripped', index=True, border=1,
    justify='center')
    data = {"success":True, "table":table}
    return JsonResponse(data)





