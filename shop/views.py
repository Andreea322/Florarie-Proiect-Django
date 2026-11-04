from django.http import HttpResponse
import datetime
import locale
from django.contrib import messages
from django.shortcuts import render
from django.shortcuts import redirect
from .forms import ContactForm

locale.setlocale(locale.LC_TIME, "ro_RO.UTF-8")

class Accesare:
    contor=1
    accesari=[]
    def __init__(self, id, ip_client, parametrii={}, url=""):
        self.id=Accesare.contor
        Accesare.contor+=1
        self.ip_client=ip_client
        self._url=url
        self.parametrii=parametrii
        self._data=datetime.datetime.now()
        Accesare.accesari.append(self)
        
    def __str__(self):
        return ( f"Accesare. id:{self.id}\n"
                f"ip_client: {self.ip_client}\n"
                f"url: {self.url()}\n"
                f"pagina: {self.pagina()}\n"
                f"data: {self.calculeaza_data()}\n"
                f"lista_parametri: {self.lista_parametri()}"
        )
    def lista_parametri(self):
        return list(self.parametrii.items())
    
    def url(self):
        return self._url
    
    def pagina(self):
        return self._url.split("?")[0]
    
    def calculeaza_data(self,tip=""):
        if tip=="zi":
            return self._data.strftime('%d %B %Y').capitalize()
        elif tip=="timp":
            return self._data.strftime('%H:%M:%S')
        else:
            return self._data.strftime('%d %B %Y, %H:%M:%S').capitalize()      
    

def index(request):
    a=Accesare("",request.ip, request.GET, request.get_full_path())
    print(a.__str__())
    messages.info(request, "Acesta este un mesaj informativ. :) ")
    messages.success(request, "Actiunea a avut succes! :D ")
    messages.warning(request, "Acesta este un avertisment. :| ")
    return render(request, "acasa.html", {"id": a.id})


def info(request):
    a=Accesare("",request.ip, request.GET, request.get_full_path())
    print(a.__str__())
    tip=request.GET.get("data","")
    return render(request, "info.html", {
        "data": a.calculeaza_data(tip)
    })
            
    
def exemplu_template(request):
    return render(request,"exemplu_template.html",
        {
            "titlu_tab":"Titlu fereastra",
            "titlu_articol":"Titlu afisat in template",
            "continut_articol":"Continut text"
        }
    )
    
def exemplu_template2(request):
    return render(request,"template2.html" )

def log(request):
    acc=Accesare("", request.ip, request.GET, request.get_full_path())
    n=request.GET.get("ultimele")
    nr=request.GET.get("accesari")
    d=request.GET.getlist("iduri")
    dbl=request.GET.get("dubluri","false")
    tabel=request.GET.get("tabel")

    nr_accesari={}
    for a in Accesare.accesari:
        pagina=a.pagina()
        if pagina not in nr_accesari:
            nr_accesari[pagina]=0
        nr_accesari[pagina]+=1
    statistica=""
    if nr_accesari:
        pag_min=min(nr_accesari, key=nr_accesari.get)
        pag_max=max(nr_accesari, key=nr_accesari.get)
        statistica = f"<p>Pagina cel mai puțin accesată: {pag_min}</p>"
        statistica += f"<p>Pagina cel mai mult accesată: {pag_max}</p>"
    
    parametri="<h2>Parametri</h2>"
    parametri+=f"<p>Număr de parametri:{len(acc.lista_parametri())}</p>"
    for nume, val in acc.lista_parametri():
        parametri+=f"<span>{nume} </span>"     
    detalii="<ul>"
    if nr=="detalii":
        for acc in Accesare.accesari:
            detalii += f"<li>{acc._data.strftime('%d %B %Y, %H:%M:%S')}</li>"
        detalii+="</ul>"          
    if tabel:
        if tabel=="tot":
            proprietati=["id", "ip_client", "url", "pagina", "data", "parametrii"]
        else:
            proprietati=tabel.split(",")
        tabel_html="<table border='1'><tr>"
        for p in proprietati:
            tabel_html+=f"<th>{p}</th>"
        tabel_html += "</tr>"
        for a in Accesare.accesari:
            tabel_html+="<tr>"
            for p in proprietati:
                if p=="id":
                    valoare=a.id
                elif p=="ip_client":
                    valoare=a.ip_client
                elif p=="url":
                    valoare=a.url()
                elif p=="pagina":
                    valoare=a.pagina()
                elif p == "data":
                    valoare=a._data.strftime("%d %B %Y, %H:%M:%S")
                elif p=="parametrii":
                    valoare=a.lista_parametri()
                tabel_html+=f"<td>{valoare}</td>"
            tabel_html+="</tr>"
        tabel_html+="</table>"
        tabel_html+=statistica
        if nr=="nr":
            tabel_html+=f"<p>Număr total de accesări: {len(Accesare.accesari)}</p>"
        elif nr=="detalii":
            tabel_html+= detalii
        tabel_html+=parametri
        return render(request, "log.html", {
            "continut": tabel_html
        })
        #return HttpResponse(f"<html><body>{tabel_html}</body></html>")

    iduri=[]
    for id in d:
        if dbl=="true":
            iduri+=id.split(",")
        elif dbl=="false":
            for i in id.split(","):
                if i not in iduri:
                    iduri.append(i)
                    
    continutid=""  
    if iduri:
        for id in iduri:
            for r in Accesare.accesari:
                if r.id==int(id):
                    continutid+=f"<p>{r}</p>"
        continutid+=statistica
        if nr=="nr":
            continutid+=f"<p>Număr total de accesări: {len(Accesare.accesari)}</p>"
        elif nr=="detalii":
            continutid+= detalii
        continutid+=parametri
        return render(request, "log.html", {
            "continut": continutid
        })       
        #return HttpResponse(f"<html><body>{continutid}</body></html>")     
    if n is None:
        continut=""
        for a in Accesare.accesari:
            continut+=f"<p>{a}</p>" 
        continut+=statistica
        if nr=="nr":
            continut+=f"<p>Număr total de accesări: {len(Accesare.accesari)}</p>"
        elif nr=="detalii":
            continut+= detalii
        continut+=parametri
        return render(request, "log.html", {
            "continut": continut
        })
        #return HttpResponse(f"""<html><body>{continut}</body></html>""")
    elif n.isdigit():
        n=int(n)
    else:
        continut=""
        continut+=statistica  
        if nr=="nr":
            continut+=f"<p>Număr total de accesări: {len(Accesare.accesari)}</p>"
        elif nr=="detalii":
            continut+= detalii
        continut+=parametri
        return render(request, "log.html", {
            "continut": f"<h1>Eroare: parametrul 'ultimele' trebuie să fie un număr întreg.</h1>{continut}"
        })
        #return HttpResponse(f"""<html><body><h1>Eroare: parametrul 'ultimele' trebuie să fie un număr întreg.</h1>
        #                    {continut}</body></html>""")
    if n==0:
        continut=""
        continut+=statistica 
        if nr == "nr":
            continut += f"<p>Număr total de accesări: {len(Accesare.accesari)}</p>"
        elif nr=="detalii":
            continut+= detalii
        continut+=parametri
        return render(request, "log.html", {
            "continut": continut
        })
        #return HttpResponse(f"""<html><body>
        #                    {continut}</body></html>""")
    elif n<=len(Accesare.accesari):
        continut=""
        for a in Accesare.accesari[-n:]:
            continut+=f"<p>{a}</p>"
        continut+=statistica 
        if nr == "nr":
            continut += f"<p>Număr total de accesări: {len(Accesare.accesari)}</p>"
        elif nr=="detalii":
            continut+= detalii
        continut+=parametri
        return render(request, "log.html", {
            "continut": continut
        })
        #return HttpResponse(f"""<html><body>{continut}</body></html>""")
    elif n>len(Accesare.accesari):
        continut=""
        for a in Accesare.accesari:
            continut+=f"<p>{a}</p>"
        continut+=statistica 
        if nr == "nr":
            continut += f"<p>Număr total de accesări: {len(Accesare.accesari)}</p>"
        elif nr=="detalii":
            continut+= detalii
        continut+=parametri
        return render(request, "log.html", {
            "continut": f"{continut}<p>Exista doar {len(Accesare.accesari)} accesari fata de {n} accesari cerute</p>"
        })
        #return HttpResponse(f"""<html><body>{continut}
        #                   <p>Exista doar {len(Accesare.accesari)} accesari fata de {n} accesari cerute</p></body></html>""")
    
def istoric(request):
    Accesare("",request.ip, request.GET, request.get_full_path())
    return render(request, "istoric.html", {
        "continut": "Istoricul comenzilor."
    })
    #return HttpResponse("<html><body>Istoricul comenzilor.</body></html>")
        
def despre(request):
    Accesare("",request.ip, request.GET, request.get_full_path())
    return render(request, "despre.html", {
        "continut": "Suntem o florărie online care oferă buchete pentru orice ocazie."
    })
    #return HttpResponse("<html><body>Suntem o florărie online care oferă buchete pentru orice ocazie.</body></html>")

def accesare(request,id):
    for a in Accesare.accesari:
        if a.id==int(id):
            return HttpResponse(f"<html><body>{a}</body></html>")      
    return HttpResponse("<html><body>Nu există o accesare cu acest ID.</body></html>")

def in_lucru(request):
    messages.info(request, "Acesta este un mesaj informativ. :) ")
    return render(request, "in_lucru.html")

#def contact_view(request):
#    if request.method == 'POST':
#        form = ContactForm(request.POST)
#        if form.is_valid():  
#            nume = form.cleaned_data['nume']
#            email = form.cleaned_data['email']
#            mesaj = form.cleaned_data['mesaj']
#            return redirect('index')
#    else:
#        form = ContactForm()
#    return render(request, 'formular.html', {'form': form})
