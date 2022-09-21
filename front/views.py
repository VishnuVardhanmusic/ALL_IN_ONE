from django.shortcuts import render

def get_html_content(request):
    import requests
    name = request.GET.get('name')
    name = name.replace(" ", "+")
    USER_AGENT = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36"
    LANGUAGE = "en-US,en;q=0.5"
    session = requests.Session()
    session.headers['User-Agent'] = USER_AGENT
    session.headers['Accept-Language'] = LANGUAGE
    session.headers['Content-Language'] = LANGUAGE
    html_content = session.get(f'https://www.google.com/search?q=+{name}').text
    return html_content


def home(request):
    result = None
    re=None
    if 'name' in request.GET:
        # fetch the data from Google.
        html_content = get_html_content(request)
        from bs4 import BeautifulSoup
        soup = BeautifulSoup(html_content, 'html.parser')
        result = dict()
        re=dict()
        #extract ans
        a1=soup.find("div", attrs={"class": "BNeawe iBp4i AP7Wnd"})
        # extract desc
        d1=soup.find("div", attrs={"class": "BNeawe s3v9rd AP7Wnd"})
        # extract useful link
        l1=soup.find("div", attrs={"class": "Gx5Zad fP1Qef xpd EtOod pkphOe"})
        if l1 is not None:
            re['vv'] = l1.a['href'][30:].split('&')[0]
        else:
            re['vv']="No suitable link has been found"

        if a1 is not None:
            result['vv']=a1.text
        elif d1 is not None:
            result['vv']=d1.text
        else:
            result['vv']="Sorry!! Entered name do not have any description. Kindly re-enter."


    return render(request, 'front/home.html', {'result': result,'re':re})
