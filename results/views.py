from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from . models import Result, Compounda, Compoundb
from django.utils import timezone
import camelot
#from torch import nn
#import torch.nn.functional as F
#from torchvision import datasets, transforms

# Create your views here.

@login_required
def main(request):
    results = Result.objects # this has to be improved to only show results of that user
    return render(request, 'results/main.html', {'results': results})

@login_required
def newhome(request):
    results = Compoundb.objects
    return render(request, 'results/newmain.html', {'results': results})


@login_required
def check(request):
    # this is where you will run the opencv code
    if request.method == 'POST':
        if request.POST['title'] and request.POST['medium'] and request.POST['compound'] and request.FILES['image']:
            result = Result()
            result.title = request.POST['title']
            result.medium = request.POST['medium']
            result.compound = request.POST['compound']
            result.detail = request.POST['detail'] 
            result.image = request.FILES['image']
            result.pub_date = timezone.datetime.now()
            result.uploader = request.user
            result.save()
            result.outputval = opencv(result.image.path)
            result.save()
            return redirect('/result/'+str(result.id))
        else:
            return render(request, 'results/check.html', {'error': 'Please fill in all fields'})
    else:
        return render(request, 'results/compound.html')
        #return render(request, 'results/check.html')

@login_required
def compoundone(request):
    if request.method == 'POST':
        if request.POST['title'] and request.POST['acetone'] and request.POST['compound'] and request.FILES['image']:
            compounda = Compounda()
            result = Result()
            compounda.title = request.POST['title'] #filling up the result as well as the compound db
            result.title = request.POST['title']
            compounda.compound = request.POST['compound']
            
            compounda.acetone = request.POST['acetone']
            aceval = request.POST['acetone']
            compounda.cyclohexane = request.POST['cyclohex']

            cycloval = request.POST['cyclohex']
            compounda.acetate = request.POST['eacetate']
            ethval = request.POST['eacetate']
            compounda.methanol = request.POST['methanol']
            methval = request.POST['methanol']

            compounda.detailcom = request.POST['detail'] 
            result.detail = request.POST['detail'] 
            compounda.image = request.FILES['image']
            result.image = request.FILES['image']
            compounda.pub_date = timezone.datetime.now()
            result.pub_date = timezone.datetime.now()
            compounda.uploader = request.user
            result.uploader = request.user
            compounda.save()
            result.save()
            compounda.outputval = checkCompoundA(aceval, cycloval, ethval, methval)
            result.outputval = checkCompoundA(aceval, cycloval, ethval, methval)
            compounda.save()
            result.save()
            return redirect('/result/'+str(result.id))
        else:
            return render(request, 'results/compoundone.html', {'error': 'Please fill in all fields'})
    else:
        return render(request, 'results/compoundone.html')
        #return render(request, 'results/check.html')


@login_required
def compoundtwo(request):
    if request.method == 'POST':
        if request.FILES['pdf']:
            compoundtwo = Compoundb()
            compoundtwo.pub_date = timezone.datetime.now()
            compoundtwo.uploader = request.user
            compoundtwo.pdf = request.FILES['pdf']
            compoundtwo.save()
            compoundtwo.outputval = camel(compoundtwo.pdf.path)
            compoundtwo.boolval = camel(compoundtwo.pdf.path) == "its working"
            compoundtwo.save()
            return redirect('/result/newresults/'+str(compoundtwo.id))
        else:
            return render(request, 'results/compoundtwo.html', {'error': 'Please fill in all fields'})
    else:
        return render(request, 'results/compoundtwo.html')
        #return render(request, 'results/check.html')


@login_required
def result(request, result_id):
    result = get_object_or_404(Result, pk=result_id)
    return render(request, 'results/result.html', {'result': result})

@login_required
def newresult(request, newresult_id):
    result = get_object_or_404(Compoundb, pk=newresult_id)
    return render(request, 'results/newresult.html', {'result': result})


def opencv(img_path):
    image = cv2.imread(img_path)
    height = image.shape[0]
    width = image.shape[1]
    channels = image.shape[2]
    values = (" the height is %s , width is %s and number of channels is %s" % (height, width, channels)) 
    return values

def checkCompoundA(ace=0, cyclo=0, ethyl=0, meth=0):
    ace = int(ace)
    cyclo = int(cyclo)
    ethyl = int(ethyl)
    meth = int(meth)
    acecheck = ace >= 0 and ace <= 7000
    cyclocheck =  cyclo >=0 and cyclo <=3880
    ethcheck = ethyl >=0 and ethyl <=5000
    methcheck = meth >=0 and meth <=3000
    flag = True
    tup = []
    if acecheck and cyclocheck and ethcheck and methcheck:
        return "Yess all your values are in given range"
    else:
        return "some of the values is out of the range"

def camel(pdf_path):
    tables = camelot.read_pdf(pdf_path)
    if tables:
        return "its working"
    else:
        return "uable to read the pdf"
