from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse
from django.shortcuts import render, redirect

from .conexionBD import ConexionBD
from .JsonTweet import JsonTweet
from .extract import Extract
from .models import Neo, Candidato

nn = 0
nc = 0


def index(request):
    conx = ConexionBD()
    conx.crear()

    if nn == 0 and nc == 0:
        setConteo(conx)

    neos = get_neologismos_last()
    if request.method == 'GET':
        neo = request.GET.get('n', None)
        if neo is not None:
            for n in neos:
                if n.lexema == neo:
                    context = {
                        "n": n,
                        "neos": neos,
                        "nc": nc,
                        "nn": nn,
                    }
                    return render(request, 'index.html', context)
    if neos:
        n = neos[0]
        context = {
            "n": n,
            "neos": neos,
            "nc": nc,
            "nn": nn,
        }
    else:
        context = {
            "neos": neos,
            "nc": nc,
            "nn": nn,
        }
    return render(request, 'index.html', context)


def index_by(request):
    letra = request.GET['letter']
    neos = get_neologismos_letter(letra)
    letter = " "
    letter += letra
    letter = letter.upper()
    letter += letra

    if neos:
        n = neos[0]
        context = {
            "letter": letter,
            "neos": neos,
            "n": n,
        }
    else:
        context = {
            "letter": letter,
            "neos": neos,
        }

    return render(request, 'index_byLetter.html', context)


def index_by_neo(request):
    letter = request.GET['letter']
    letra = letter[1]
    neos = get_neologismos_letter(letra)

    if request.method == 'GET':
        neo = request.GET.get('n', None)
        if neo is not None:
            for n in neos:
                if n.lexema == neo:
                    context = {
                        "letter": letter,
                        "neos": neos,
                        "n": n,
                    }
                    return render(request, 'index_byLetter.html', context)

    if neos:
        n = neos[0]
        context = {
            "letter": letter,
            "neos": neos,
            "n": n,
        }
    else:
        context = {
            "letter": letter,
            "neos": neos,
        }

    return render(request, 'index_byLetter.html', context)


def get_neologismos():
    neos = []

    conex = ConexionBD()
    hits = conex.get_ads()

    for hit in hits:
        neo = Neo()
        neo.lexema = hit['_source']['unk'][0]
        tweet = hit['_source']['tweetO']
        if not tweet:
            tweet = " Desconocido "
        bio = hit['_source']['perfil']
        if not bio:
            bio = " Desconocido "
        local = hit['_source']['localizacion']
        if not local:
            local = " Desconocido "
        fecha = hit['_source']['fecha']
        if not fecha:
            fecha = " Desconocido "
        neo.tweet = tweet
        neo.bio = bio
        neo.local = local
        neo.date = fecha
        neos.append(neo)
    return neos


def get_neologismos_last():
    neos = []

    conex = ConexionBD()
    hits = conex.get_ads_lasts()

    for hit in hits:
        neo = Neo()
        neo.lexema = hit['_source']['unk'][0]
        tweet = hit['_source']['tweetO']
        if not tweet:
            tweet = " Desconocido "
        bio = hit['_source']['perfil']
        if not bio:
            bio = " Desconocido "
        local = hit['_source']['localizacion']
        if not local:
            local = " Desconocido "
        fecha = hit['_source']['fecha']
        if not fecha:
            fecha = " Desconocido "
        neo.tweet = tweet
        neo.bio = bio
        neo.local = local
        neo.date = fecha
        neos.append(neo)
    return neos


def get_neologismos_letter(letter):
    neos = []

    conex = ConexionBD()
    hits = conex.get_neo_by_letter(letter)

    for hit in hits:
        neo = Neo()
        neo.lexema = hit['_source']['unk'][0]
        tweet = hit['_source']['tweetO']
        if not tweet:
            tweet = " Desconocido "
        bio = hit['_source']['perfil']
        if not bio:
            bio = " Desconocido "
        local = hit['_source']['localizacion']
        if not local:
            local = " Desconocido "
        fecha = hit['_source']['fecha']
        if not fecha:
            fecha = " Desconocido "
        neo.tweet = tweet
        neo.bio = bio
        neo.local = local
        neo.date = fecha
        neos.append(neo)
    return neos


def admitir(request):
    neo = request.GET.get('cand', None)

    conex = ConexionBD()
    hits = conex.get_cand(neo)

    tweeto = ""
    perfil = ""
    localizacion = ""
    fecha = " "
    flag1 = False

    for hit in hits:
        tweet = hit['_source']['tweetO']
        if not tweet:
            tweet = " Desconocido "
        bio = hit['_source']['perfil']
        if not bio:
            bio = " Desconocido "
        local = hit['_source']['localizacion']
        if not local:
            local = " Desconocido "
        date = hit['_source']['fecha']
        if not date:
            date = " Desconocido "
        if flag1:
            tweeto += "|"
            perfil += "|"
            localizacion += "|"
            fecha += "|"
        tweeto += tweet + " "
        perfil += bio + " "
        localizacion += local + " "
        fecha += date + " "

        flag1 = True

    tj = JsonTweet(tweeto, perfil, localizacion, fecha)
    tj.add_unk(neo)
    tj.put_admitido()

    if conex.exist_disc(neo):
        conex.delete_disc(neo)

    msg = "Neologismo [ " + neo + " ] Aceptado"
    messages.success(request, msg)
    return redirect(request.META['HTTP_REFERER'])


def denegar(request):
    neo = request.GET.get('cand', None)

    conex = ConexionBD()
    hits = conex.get_cand(neo)

    tweeto = ""
    perfil = ""
    localizacion = ""
    fecha = " "
    flag1 = False
    for hit in hits:
        tweet = hit['_source']['tweetO']
        if not tweet:
            tweet = " Desconocido "
        bio = hit['_source']['perfil']
        if not bio:
            bio = " Desconocido "
        local = hit['_source']['localizacion']
        if not local:
            local = " Desconocido "
        date = hit['_source']['fecha']
        if not date:
            date = " Desconocido "
        if flag1:
            tweeto += "|"
            perfil += "|"
            localizacion += "|"
            fecha += "|"
        tweeto += tweet + " "
        perfil += bio + " "
        localizacion += local + " "
        fecha += date + " "
        flag1 = True

    tj = JsonTweet(tweeto, perfil, localizacion, fecha)
    tj.add_unk(neo)
    tj.put_descartado()

    if conex.exist_ad(neo):
        conex.delete_ad(neo)

    msg = "Neologismo [ " + neo + " ] Descartado"
    messages.success(request, msg)
    return redirect(request.META['HTTP_REFERER'])


def get_candidatos():
    candidatos = []

    conex = ConexionBD()
    hits = conex.get_tweet()

    for hit in hits:
        neologismos = hit['_source']['unk']
        tweet = hit['_source']['tweetO']
        if not tweet:
            tweet = " Desconocido "
        bio = hit['_source']['perfil']
        if not bio:
            bio = " Desconocido "
        local = hit['_source']['localizacion']
        if not local:
            local = " Desconocido "
        fecha = hit['_source']['fecha']
        if not fecha:
            fecha = " Desconocido "

        for candidato in neologismos:
            flag = True
            for cand in candidatos:
                if str(cand.lexema) == str(candidato):
                    cand.tweet += "|" + tweet + " "
                    cand.bio += "|" + bio + " "
                    cand.local += "|" + local + " "
                    cand.date += "|" + fecha + " "
                    flag = False

            if flag:
                cand = Candidato()
                cand.lexema = candidato
                cand.tweet = tweet
                cand.date = fecha
                cand.bio = bio
                cand.local = local
                candidatos.append(cand)

    for c in candidatos:
        if conex.exist_ad(c.lexema):
            c.ads = True
        elif conex.exist_disc(c.lexema):
            c.disc = True
    return candidatos


def catalogar(request):
    candidatos = get_candidatos()
    dis = False
    ad = False
    cand = False
    all = True

    if request.method == 'GET':
        filtro = request.GET.get('filter', None)
        if filtro is not None:
            all = False
            if filtro == "cand":
                candidatos = [e for e in candidatos if not (e.ads or e.disc)]
                cand = True
            elif filtro == "ad":
                candidatos = [e for e in candidatos if e.ads]
                ad = True
            elif filtro == "dis":
                candidatos = [e for e in candidatos if e.disc]
                dis = True
    context = {
        "cands": candidatos,
        "dis": dis,
        "ad": ad,
        "cand": cand,
        "all": all,
    }
    return render(request, 'catalogar.html', context)


def buscar(request):
    if request.method == 'GET':
        search = request.GET.get('search', None)

        conex = ConexionBD()
        hits = conex.get_neo(search)

        neo = Neo()
        for hit in hits:
            neo.lexema = hit['_source']['unk'][0]
            tweet = hit['_source']['tweetO']
            if not tweet:
                tweet = " Desconocido "
            bio = hit['_source']['perfil']
            if not bio:
                bio = " Desconocido "
            local = hit['_source']['localizacion']
            if not local:
                local = " Desconocido "
            fecha = hit['_source']['fecha']
            if not fecha:
                fecha = " Desconocido "
            neo.tweet = tweet
            neo.bio = bio
            neo.local = local
            neo.date = fecha
        if not hits:
            context = {
            }
        else:
            context = {
                "n": neo,
            }
        return render(request, 'buscado.html', context)


def loguearse(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return index(request)
        else:
            return HttpResponse("No existe usuario o la password es incorrecta")

    form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})


def desconectarse(request):
    logout(request)
    return index(request)


def about(request):
    return render(request, 'about.html')


def procesar(request):
    if request.method == 'POST' and request.FILES['myfile']:
        myfile = request.FILES['myfile']
        fs = FileSystemStorage()
        filename = fs.save(myfile.name, myfile)
        uploaded_file_url = fs.url(filename)
        return render(request, 'procesar.html', {
            'uploaded_file_url': uploaded_file_url
        })
    return render(request, 'procesar.html')


def proceso(request):
    if request.method == 'GET':
        file = request.GET.get('f', None)
        file = '.' + file
        ex = Extract()
        linea = ex.extraer(file)
        return render(request, 'procesando.html', {'linea': linea})
    return render(request, 'procesar.html')


def setConteo(conx):
    global nc
    global nn
    nc = conx.get_nc()
    nn = conx.get_nn()
