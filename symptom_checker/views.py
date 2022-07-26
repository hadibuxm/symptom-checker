from django.shortcuts import render
import pickle
# our home page view
from symptom_checker import predict


def home(request):
    return render(request, 'index.html')



# our result page view
def result(request):

    sym = request.GET['symptoms'].replace(" ", "")
    if ',' in sym:
        sym = sym.split(',')
    else:
        sym = [sym]
    b_part = request.GET['body-part'].replace(" ", "").split(',')
    condition = request.GET['condition'].replace(" ", "").split(',')
    ch_ad = [request.GET['ch-ad'].strip()]
    gender = [request.GET['gender'].strip()]

    result = predict.prediction_function_main(sym, b_part, condition, ch_ad, gender)
    return render(request, 'index.html', {'result': result[0:5]})