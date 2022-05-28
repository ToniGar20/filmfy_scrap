import requests_html
import csv


YOUTUBE = 'https://www.youtube.com'
YOUTUBE_SEARCH = 'https://www.youtube.com/results?search_query='

MOVIES = [
'Seven',
'El+silencio+de+los+corderos',
'Vengadores+Endgame',
'Gran+Torino',
'El+precio+del+poder',
'12+hombres+sin+piedad',
'Sin+perdón',
'Doctor+Strange+Doctor+Extraño',
'Up',
'Dumbo',
'Senderos+de+gloria',
'Whiplash',
'Toy+Story+Juguetes',
'Memento',
'Salvar+al+soldado+Ryan',
'Harry+Potter+y+el+Misterio+del+Príncipe',
'Un+don+excepcional',
'El+viaje+de+Chihiro',
'Los+intocables+de+Eliot+Ness',
'Creed+II+La+leyenda+de+Rocky',
'Bailando+con+lobos',
'Una+cuestión+de+tiempo',
'Casablanca',
'V+de+Vendetta',
'Frozen+el+reino+del+hielo',
'Uno+más+de+la+familia',
'Deadpool',
'Cantando+bajo+la+lluvia',
'Soy+leyenda',
'Pesadilla+antes+de+Navidad+3D',
'Los+milagros+del+cielo',
'Expediente+Warren+The+Conjuring',
'Star+Wars+Episodio+III++La+venganza+de+los+Sith',
'El+profesional+Léon',
'Diamante+de+sangre',
'Con+la+muerte+en+los+talones',
'Réquiem+por+un+sueño',
'Zootrópolis',
'El+último+mohicano',
'Mary+Poppins',
'Call+Me+By+Your+Name',
'Harry+Potter+y+las+reliquias+de+la+muerte+Parte+1',
'Oceans+Eleven',
'Kill+Bill+Volumen+2',
'Capitán+América+El+soldado+de+invierno',
'Enemigo+a+las+puertas',
'Rain+Man+El+hombre+de+la+lluvia',
'Bajo+cero',
'The+Imitation+Game+Descifrando+Enigma',
'Terminator',
'El+nombre+de+la+rosa',
'La+teoría+del+todo',
'Atrápame+si+puedes',
'Alicia+en+el+País+de+las+Maravillas',
'El+irlandés',
'Princesa+por+sorpresa+2',
'Green+Book',
'Prisioneros',
'El+lobo+de+Wall+Street',
'El+libro+de+la+selva',
'Mi+nombre+es+Khan',
'Guardianes+de+la+galaxia+vol+2',
'Ghost+Más+allá+del+amor',
'Siete+almas',
'El+show+de+Truman+Una+vida+en+directo',
'Capitán+América+Civil+War',
'El+libro+de+la+vida',
'El+castillo+ambulante',
'El+Truco+Final+El+Prestigio',
'Avatar',
'Vaiana',
'Los+puentes+de+Madison',
'La+dama+y+el+vagabundo',
'Cómo+entrenar+a+tu+dragón+2',
'Bajo+la+misma+estrella',
'Regreso+al+futuro+II',
'Qué+bello+es+vivir',
'Harry+Potter+y+la+Orden+del+Fénix',
'Enredados+Rapunzel',
'Los+Diez+Mandamientos',
'Leyendas+de+pasión',
'Tres+anuncios+en+las+afueras',
'Los+mundos+de+Coraline',
'El+último+samurái',
'La+sirenita',
'Guardianes+de+la+galaxia',
'La+princesa+Mononoke',
'Un+ciudadano+ejemplar',
'Shutter+Island',
'El+origen+de+los+Guardianes',
'La+cenicienta',
'Mystic+River',
'El+libro+de+la+selva',
'Hasta+que+llegó+su+hora',
'American+Beauty',
'Apocalypto',
'John+Wick+Pacto+de+sangre',
'Espartaco',
'El+club+de+la+lucha',
'Olvídate+de+mi',
'Cars',
'Wonder+Woman',
'SpiderMan',
'Toy+Story+2+Los+juguetes+vuelven+a+la+carga',
'12+años+de+esclavitud',
'El+curioso+caso+de+Benjamin+Button',
'Slumdog+Millionaire',
'El+mago+de+Oz',
'La+gran+evasión',
'300',
'Harry+Potter+y+la+Cámara+Secreta',
'A+dos+metros+de+ti',
'Snatch+cerdos+y+diamantes',
'En+busca+del+arca+perdida',
'Solo+en+casa',
'John+Wick+Capítulo+3++Parabellum',
'Cómo+entrenar+a+tu+dragón',
'Venganza',
'1917',
'El+club+de+los+poetas+muertos',
'Criadas+y+Señoras+The+Help',
'Los+otros',
'Batman+Begins',
'Piratas+del+Caribe+La+maldición+de+la+Perla+Negra',
'Ice+Age+La+Edad+de+Hielo',
'La+Pasión+de+Cristo',
'Logan',
'El+golpe',
'Titanic',
'El+fuego+de+la+venganza',
'La+novia+cadáver',
'La+chaqueta+metálica',
'Aliens+el+regreso',
'Grease+Brillantina',
'Cómo+entrenar+a+tu+dragón+3',
'La+ciudad+de+las+estrellas+La+La+Land',
'Matilda',
'Lawrence+de+Arabia',
'Iron+Man',
'Los+Increíbles+2',
'Gru+mi+villano+favorito',
'Antes+de+ti',
'El+gran+showman',
'Una+mente+maravillosa',
'El+Secreto+de+Sus+Ojos',
'Drácula+de+Bram+Stoker',
'Toro+salvaje',
'El+indomable+Will+Hunting',
'Los+Increíbles',
'The+Blind+Side+Un+sueño+posible',
'Tu+mejor+amigo',
'Matrix',
'Náufrago',
'Marvel+Los+Vengadores',
'Indiana+Jones+y+el+templo+maldito',
'Wonder',
'Tiempos+modernos',
'Big+Hero+6',
'Mi+vecino+Totoro',
'ET+El+extraterrestre',
'Hasta+el+último+hombre',
'2001+Una+odisea+del+espacio',
'Harry+Potter+y+el+Cáliz+de+Fuego',
'Shrek',
'La+Liga+de+la+Justicia+de+Zack+Snyder',
'Big+Fish',
'El+diario+de+Noa',
'Reservoir+Dogs',
'Star+Wars++Episodio+V++El+imperio+contraataca',
'El+pianista',
'El+Señor+de+los+Anillos+El+retorno+del+Rey',
'Ciudadano+Kane',
'Star+Wars+Episodio+IV++Una+nueva+esperanza+La+guerra+de+las+galaxias',
'Intocable',
'BenHur',
'Coco',
'El+niño+con+el+pijama+de+rayas',
'El+Señor+de+los+Anillos+Las+dos+torres',
'El+caballero+oscuro',
'El+Señor+de+los+Anillos+La+Comunidad+del+Anillo',
'Malditos+bastardos',
'Infiltrados',
'Vengadores+Infinity+War',
'Vértigo+De+entre+los+muertos',
'Hombres+de+honor',
'Alguien+voló+sobre+el+nido+del+cuco',
'La+naranja+mecánica',
'Apocalypse+Now',
'La+ventana+indiscreta',
'Eduardo+Manostijeras',
'Rocky',
'Ciudad+de+Dios',
'Harry+Potter+y+las+reliquias+de+la+muerte+Parte+2',
'Los+Goonies',
'American+History+X',
'Toy+Story+3',
'Blade+Runner',
'Harry+Potter+y+el+Prisionero+de+Azkaban',
'Parásitos',
'Pride+and+Prejudice+Orgullo+y+prejuicio',
'El+resplandor',
'Bohemian+Rhapsody',
'Regreso+al+futuro',
'Jurassic+Park+Parque+Jurásico',
'En+busca+de+la+felicidad',
'Braveheart',
'Star+Wars+Episodio+VI++El+retorno+del+Jedi',
'Interstellar',
'WALL-E+Batallón+de+limpieza',
'Psicosis',
'Cinema+Paradiso',
'Tiburón',
'Alien+el+octavo+pasajero',
'El+sexto+sentido',
'Casino',
'Pesadilla+antes+de+Navidad',
'La+vida+es+bella',
'Forrest+Gump',
'Gladiator+El+gladiador',
'Harry+Potter+y+la+Piedra+Filosofal',
'Django+desencadenado',
'El+Exorcista',
'Pulp+Fiction',
'Uno+de+los+nuestros',
'El+Rey+León',
'Cadena+perpetua',
'El+Padrino+Parte+II',
'La+lista+de+Schindler',
'El+padrino',
'Las+ventajas+de+ser+un+marginado',
'Aladdin',
'Trainspotting',
'Los+Miserables',
'Dunkerque',
'Contratiempo',
'El+ultimátum+de+Bourne',
'Toy+Story+4',
'Entrevista+con+el+vampiro',
'Misión+Imposible++Fallout',
'Billy+Elliot+Quiero+bailar',
'Los+cazafantasmas',
'Vengadores+La+era+de+Ultrón',
'Lion',
'El+Rey+León',
'El+niño+que+domó+el+viento',
'Creed+La+leyenda+de+Rocky',
'Buscando+a+Dory',
'Deadpool+2',
'Cisne+negro',
'SpiderMan+Homecoming',
'Tomates+verdes+fritos',
'Memorias+de+una+geisha',
'La+niñera+mágica',
'Sonrisas+y+lágrimas',
'Philadelphia',
'Argo',
'El+puente+de+los+espías',
'Canta',
'Rompe+Ralph',
'Las+crónicas+de+Narnia+El+león+la+bruja+y+el+armario',
'Aladdin',
'Kingsman+Servicio+secreto',
'Spirit+El+corcel+indomable',
'Fargo',
'Soul',
'Pena+de+muerte',
'El+laberinto+del+fauno',
'Carol',
'Patch+Adams',
'Figuras+ocultas',
'Expediente+Warren+El+caso+Enfield',
'Troya',
'La+habitación',
'Mia+y+el+león+blanco',
'SpiderMan+2',
'Charlie+y+la+fábrica+de+chocolate',
]

def create_csv():
    header = ['q', 'trailer-url']
    new_file = open('youtube-movie-trailers.csv', 'w')
    writer = csv.writer(new_file)
    writer.writerow(header)
    new_file.close()


def write_csv(row):
    with open('youtube-movie-trailers.csv', 'a', encoding='UTF8', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(row)
        file.close()


for movie in MOVIES:
    new_trailer = []

    url_queried = YOUTUBE_SEARCH + movie + '+trailer'
    print(url_queried)

    session = requests_html.HTMLSession()
    r = session.get(url_queried)
    r.html.render(sleep=5, timeout=8)

    movie_trailer = r.html.xpath('(//a[@id="video-title"])[1]/@href')
    print(movie_trailer)
    new_trailer.append(movie)
    new_trailer.append(YOUTUBE + movie_trailer[0])

    write_csv(new_trailer)


