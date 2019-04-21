from django.shortcuts import  render, get_object_or_404
import random, string, json
from shortenApp.models import Urls
from django.http import HttpResponseRedirect, HttpResponse
from django.conf import settings
#from django.core.context_processor import csrf
#from django.views.decorators import csrf
def index(request):
    c = {}
    #c = RequestContext(request)
    #c.update(csrf(request))
    return render(request, 'shortenApp/index.html', c)
 
def redirect_original(request, short_id):
    url = get_object_or_404(Urls, pk=short_id) # get object, if not        found return 404 error
    url.count += 1
    url.save()
    return HttpResponseRedirect(url.httpurl)

def shortenUrl(request):
    url = request.POST.get("url", "")
    print (url)
    try:
        urll = Urls.objects.get(httpurl=url)
        short_id = urll.short_id
    except (Urls.DoesNotExist):
        print ("Does not exist")
    if not (url == ""):
        print ("URL not empty !")
        short_id = getShortCode()
        print ("Got shortcode")
        b = Urls(httpurl=url, short_id=short_id)
        b.save()
        print ("Saved URL")
        response_data = {}
        response_data['url'] = "/" + short_id
    else:
        return HttpResponse(json.dumps({"error": "error occurs"}),content_type="application/json")
    response_data = {}
    response_data['url'] = "/" + short_id
    return HttpResponse(json.dumps(response_data), content_type="application/json")



def shorten_url(request):
    url = request.POST.get("url",'') 
    #if not Url.objects.filter(pk=short_id).exists(): return short_id
    if not (url == ''):
        short_id = get_short_code()
        b = Urls(httpurl=url, short_id=short_id)
        b.save()
 
        response_data = {}
        response_data['url'] = settings.SITE_URL + "/" + short_id
        return HttpResponse(json.dumps(response_data),  content_type="application/json")
    return HttpResponse(json.dumps({"error": "error occurs"}), content_type="application/json")
 
def get_short_code():
    length = 6
    char = string.ascii_uppercase + string.digits + string.ascii_lowercase
    # if the randomly generated short_id is used then generate next
    while True:
        if not Url.objects.filter(pk=short_id).exists(): return short_id
        short_id = ''.join(random.choice(char) for x in range(length))
        try:
            temp = Urls.objects.get(pk=short_id)
        except:
            return short_id

