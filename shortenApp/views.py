from django.shortcuts import  render, get_object_or_404
from django.urls import reverse
import random, string, json
from shortenApp.models import Urls
from django.http import HttpResponseRedirect, HttpResponse
from django.conf import settings
import time
start = time.time()
def index(request):
    c = {}
    #c = RequestContext(request)
    #c.update(csrf(request))
    return render(request, 'shortenApp/index.html', c)
 
def redirect_original(request, short_id):
    end=time.time()
    print("END: ", end)
    expiry = end - start
    print("EXPIRY: ",expiry)
    if expiry>300.0:
        print('link expired')
        url = Urls.objects.filter(pk=short_id).delete()
        expiry = 0.0
        end = 0.0
    url = get_object_or_404(Urls, pk=short_id) # get object, if not found return 404 error
    url.count += 11
    url.save()
    return HttpResponseRedirect(url.httpurl)
def shorten_url(request):
    global start
    url = request.POST.get("url",'') 
    if not (url == ''):
        start = time.time()
        print("START: ", start)
        if  Urls.objects.filter(httpurl=url).exists(): 
            print('URL exists... fetching URl...')
            short_id = Urls.objects.get(httpurl=url).short_id
            response_data = {}
            response_data['url'] = settings.SITE_URL + "/" + short_id
            return HttpResponse(json.dumps(response_data),  content_type="application/json")
        else:
            print('generating URL')
            short_id = get_short_code()
            b = Urls(httpurl=url, short_id=short_id)
            b.save()
            response_data = {}
            response_data['url'] = settings.SITE_URL + "/" + short_id
            return HttpResponse(json.dumps(response_data),  content_type="application/json")
    elif url =='':
        return HttpResponse(json.dumps({"error": "error occurs"}), content_type="application/json")
def get_short_code():
    length = 6 
    char = string.ascii_uppercase + string.digits + string.ascii_lowercase
    # if the randomly generated short_id is used then generate next
    while True:
        #if not Urls.objects.filter(pk=short_id).exists(): return short_id
        short_id = ''.join(random.choice(char) for x in range(length))
        try:
            temp = Urls.objects.get(pk=short_id)
        except:
            return short_id

