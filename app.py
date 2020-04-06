from flask import Flask, render_template, request
import requests

app = Flask(__name__)

r = requests.get('https://rickandmortyapi.com/api/episode/')
#pedir_personajes = requests.get('https://rickandmortyapi.com/api/character/')
#pedir_lugares = requests.get('https://rickandmortyapi.com/api/location/')
r_1 = r.json()
#r_2 = pedir_personajes.json()
#r_3 = pedir_lugares.json()
episodios = r_1["results"]
personajes = []
lugares = []
#personajes.extend(r_2["results"])
#lugares.extend(r_3["results"])
num = int(r_1['info']['pages'])
#num_pages = int(r_2['info']['pages'])
#num_pages_2 = int(r_3['info']['pages'])

r_sanfran = requests.get("https://rickandmortyapi.com/api/episode/", params={'page': 2}).json()
episodios.extend(r_sanfran['results'])

#for page in range(1, num_pages -1):
 #   r_sanfran = requests.get("https://rickandmortyapi.com/api/character/", params={'page': page}).json()
  #  personajes.extend(r_sanfran['results'])

#for page in range(1, num_pages_2 -1):
 #  r_sanfran_2 = requests.get("https://rickandmortyapi.com/api/character/", params={'page': page}).json()
 #   lugares.extend(r_sanfran_2['results'])


def separar_ulr(lista):
    return [int((str(i).split('/'))[-1]) for i in lista]


def manejar_busqueda(palabra, data):
    # episodios con la palabra
    r = requests.get(f'https://rickandmortyapi.com/api/{data}/').json()
    numero = (r["info"])["pages"]
    episodios = []
    for page in range(1, numero + 1):
        r_sanfran_2 = requests.get(f"https://rickandmortyapi.com/api/{data}/",
                                   params={'page': page}).json()
        episodios.extend(r_sanfran_2['results'])
    final = [elemento for elemento in episodios if palabra.lower()
             in elemento['name'].lower()]
    return final


def juntar_busquedas(palabra):
    p = manejar_busqueda(palabra, 'character')
    ep = manejar_busqueda(palabra, 'episode')
    loc = manejar_busqueda(palabra, 'location')
    return p, ep, loc


@app.route('/', methods=['GET', 'POST'])
def hello_world():
    if request.method == 'POST':
        data = request.form["b"]
        listas = juntar_busquedas(data)
        return render_template('busqueda.html', personajes=listas[0],
                               capitulos=listas[1],
                               locaciones=listas[2], data=data)
    else:
        return render_template('home.html', capitulos=episodios)
        

@app.route('/episodio/<string:name>', methods=['POST', 'GET'])
def episodio(name):
    if request.method == 'POST':
        data = request.form["b"]
        listas = juntar_busquedas(data)
        return render_template('busqueda.html', personajes=listas[0],
                               capitulos=listas[1], locaciones=listas[2], data=data)
    else:
        e = requests.get(f'https://rickandmortyapi.com/api/episode/{str(name)}')
        e_1 = e.json()
        personajes_list = e_1['characters']
        par = separar_ulr(personajes_list)
        pedir_personajes = requests.get(f'https://rickandmortyapi.com/api/'
                                        f'character/{par}').json()
        return render_template('episodio.html', episodio=e_1,
                               personajes=pedir_personajes)

@app.route('/personaje/<string:name>', methods=['POST', 'GET'])
def personaje(name):
  if request.method == 'POST':
      data = request.form["b"]
      listas = juntar_busquedas(data)
      return render_template('busqueda.html', personajes=listas[0],
                             capitulos=listas[1], locaciones=listas[2], data=data)
  else:
      p = requests.get(f'https://rickandmortyapi.com/api/character/{str(name)}')
      p_1 = p.json()
      episodes_list = p_1['episode']
      locaciones_actual = p_1['location']
      locaciones_origen = p_1['origin']
      l_a, l_o = (str(locaciones_actual['url']).split('/'))[-1],\
                 (str(locaciones_origen['url']).split('/'))[-1]
      par = separar_ulr(episodes_list)
      #par_2 = separar_ulr(locaciones_list)
      pedir_episodios = requests.get(f'https://rickandmortyapi.com/api/'  
                                        f'episode/{par}').json()
      #pedir_locaciones = requests.get(f'https://rickandmortyapi.com/api/'
       #                                 f'location/{par}')
      return render_template('personaje.html', personaje=p_1,
                               episodios=pedir_episodios, locacion_actual=locaciones_actual,
                             locacion_origen=locaciones_origen, l_a=l_a, l_o=l_o)


@app.route('/locacion/<string:name>', methods=['POST', 'GET'])
def locacion(name):
   if request.method == 'POST':
       data = request.form["b"]
       listas = juntar_busquedas(data)
       return render_template('busqueda.html', personajes=listas[0],
                              capitulos=listas[1], locaiones=listas[2], data=data)

   else:
       l = requests.get(f'https://rickandmortyapi.com/api/location/{str(name)}')
       l_1 = l.json()
       residentes_list = l_1['residents']
       par = separar_ulr(residentes_list)
       pedir_personajes = requests.get(f'https://rickandmortyapi.com/api/'
                                       f'character/{par}').json()
       return render_template('locacion.html', locacion=l_1, residentes=pedir_personajes)

@app.route('/busqueda/<string:name>', methods=['POST', 'GET'])
def busqueda(name):
    if request.method == 'POST':
        data = request.form["b"]
        listas = juntar_busquedas(data)
        return render_template('busqueda.html', personajes=listas[0],
                               capitulos=listas[1], locaciones=listas[2], data=data)
    else:
        return render_template('busqueda.html')




if __name__ == '__main__':
    app.run()
