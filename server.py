#!/usr/bin/env python3
"""
server.py — Servidor de datos para la Tabla Periódica Interactiva
=================================================================
Ejecutar:  python3 server.py
Luego abrir:  http://localhost:5000

Provee la API que consume index.html para generar tablas y gráficas.
"""

from flask import Flask, jsonify, request, send_from_directory

app = Flask(__name__, static_folder='.')

_RAW = [
    ("H","Hidrógeno",1,0,1.008),("He","Helio",2,2,4.003),
    ("Li","Litio",3,4,6.94),("Be","Berilio",4,5,9.012),
    ("B","Boro",5,6,10.81),("C","Carbono",6,6,12.011),
    ("N","Nitrógeno",7,7,14.007),("O","Oxígeno",8,8,15.999),
    ("F","Flúor",9,10,18.998),("Ne","Neón",10,10,20.180),
    ("Na","Sodio",11,12,22.990),("Mg","Magnesio",12,12,24.305),
    ("Al","Aluminio",13,14,26.982),("Si","Silicio",14,14,28.085),
    ("P","Fósforo",15,16,30.974),("S","Azufre",16,16,32.060),
    ("Cl","Cloro",17,18,35.450),("Ar","Argón",18,22,39.948),
    ("K","Potasio",19,20,39.098),("Ca","Calcio",20,20,40.078),
    ("Sc","Escandio",21,24,44.956),("Ti","Titanio",22,26,47.867),
    ("V","Vanadio",23,28,50.942),("Cr","Cromo",24,28,51.996),
    ("Mn","Manganeso",25,30,54.938),("Fe","Hierro",26,30,55.845),
    ("Co","Cobalto",27,32,58.933),("Ni","Níquel",28,30,58.693),
    ("Cu","Cobre",29,34,63.546),("Zn","Zinc",30,35,65.380),
    ("Ga","Galio",31,39,69.723),("Ge","Germanio",32,41,72.630),
    ("As","Arsénico",33,42,74.922),("Se","Selenio",34,45,78.971),
    ("Br","Bromo",35,45,79.904),("Kr","Kriptón",36,48,83.798),
    ("Rb","Rubidio",37,48,85.468),("Sr","Estroncio",38,50,87.620),
    ("Y","Itrio",39,50,88.906),("Zr","Circonio",40,51,91.224),
    ("Nb","Niobio",41,52,92.906),("Mo","Molibdeno",42,54,95.950),
    ("Tc","Tecnecio",43,55,98.0),("Ru","Rutenio",44,57,101.07),
    ("Rh","Rodio",45,58,102.91),("Pd","Paladio",46,60,106.42),
    ("Ag","Plata",47,61,107.87),("Cd","Cadmio",48,64,112.41),
    ("In","Indio",49,66,114.82),("Sn","Estaño",50,69,118.71),
    ("Sb","Antimonio",51,71,121.76),("Te","Telurio",52,76,127.60),
    ("I","Yodo",53,74,126.90),("Xe","Xenón",54,77,131.29),
    ("Cs","Cesio",55,78,132.91),("Ba","Bario",56,81,137.33),
    ("La","Lantano",57,82,138.91),("Ce","Cerio",58,82,140.12),
    ("Pr","Praseodimio",59,82,140.91),("Nd","Neodimio",60,84,144.24),
    ("Pm","Prometio",61,84,145.0),("Sm","Samario",62,88,150.36),
    ("Eu","Europio",63,89,151.96),("Gd","Gadolinio",64,93,157.25),
    ("Tb","Terbio",65,94,158.93),("Dy","Disprosio",66,97,162.50),
    ("Ho","Holmio",67,98,164.93),("Er","Erbio",68,100,167.26),
    ("Tm","Tulio",69,99,168.93),("Yb","Iterbio",70,103,173.05),
    ("Lu","Lutecio",71,104,174.97),("Hf","Hafnio",72,106,178.49),
    ("Ta","Tántalo",73,108,180.95),("W","Wolframio",74,110,183.84),
    ("Re","Renio",75,111,186.21),("Os","Osmio",76,114,190.23),
    ("Ir","Iridio",77,115,192.22),("Pt","Platino",78,117,195.08),
    ("Au","Oro",79,118,196.97),("Hg","Mercurio",80,121,200.59),
    ("Tl","Talio",81,123,204.38),("Pb","Plomo",82,125,207.20),
    ("Bi","Bismuto",83,126,208.98),("Po","Polonio",84,125,209.0),
    ("At","Astato",85,125,210.0),("Rn","Radón",86,136,222.0),
    ("Fr","Francio",87,136,223.0),("Ra","Radio",88,138,226.0),
    ("Ac","Actinio",89,138,227.0),("Th","Torio",90,142,232.04),
    ("Pa","Protactinio",91,140,231.04),("U","Uranio",92,146,238.03),
    ("Np","Neptunio",93,144,237.0),("Pu","Plutonio",94,150,244.0),
    ("Am","Americio",95,148,243.0),("Cm","Curio",96,151,247.0),
    ("Bk","Berkelio",97,150,247.0),("Cf","Californio",98,153,251.0),
    ("Es","Einstenio",99,153,252.0),("Fm","Fermio",100,157,257.0),
    ("Md","Mendelevio",101,157,258.0),("No","Nobelio",102,157,259.0),
    ("Lr","Lawrencio",103,163,266.0),("Rf","Rutherfordio",104,163,267.0),
    ("Db","Dubnio",105,163,268.0),("Sg","Seaborgio",106,163,269.0),
    ("Bh","Bohrio",107,163,270.0),("Hs","Hasio",108,169,277.0),
    ("Mt","Meitnerio",109,169,278.0),("Ds","Darmstatio",110,171,281.0),
    ("Rg","Roentgenio",111,171,282.0),("Cn","Copernicio",112,173,285.0),
]

ELEMENTS = []
BY_SYM = {}

for sym, nombre, Z, N, masa in _RAW:
    A = Z + N
    d = {"simbolo":sym,"nombre":nombre,"Z":Z,"protones":Z,
         "electrones":Z,"neutrones":N,"masa":masa,"A":A}
    ELEMENTS.append(d)
    BY_SYM[sym.lower()] = d

@app.after_request
def add_cors(r):
    r.headers["Access-Control-Allow-Origin"] = "*"
    return r

@app.route('/')
def index():
    return send_from_directory('.', 'index.html')

@app.route('/api/tabla/<sym>')
def get_tabla(sym):
    el = BY_SYM.get(sym.lower())
    if not el:
        return jsonify({"error":"No encontrado"}), 404
    return jsonify({
        "simbolo": el["simbolo"], "nombre": el["nombre"],
        "filas": [
            {"columna":"# Atómico",       "formula":"Z",        "valor": el["Z"]},
            {"columna":"Protones",        "formula":"e+",       "valor": el["protones"]},
            {"columna":"Electrones",      "formula":"e-",       "valor": el["electrones"]},
            {"columna":"Neutrones",       "formula":"N = A − Z","valor": el["neutrones"]},
            {"columna":"# Másico / Peso", "formula":"A = Z + N","valor": el["A"]},
            {"columna":"Masa Atómica (u)","formula":"—",        "valor": el["masa"]},
        ]
    })

@app.route('/api/grafica/elemento/<sym>')
def grafica_elemento(sym):
    el = BY_SYM.get(sym.lower())
    if not el:
        return jsonify({"error":"No encontrado"}), 404
    return jsonify({
        "simbolo": el["simbolo"], "nombre": el["nombre"],
        "labels": ["Protones (e+)","Electrones (e-)","Neutrones (N)","# Másico (A)"],
        "values": [el["protones"],el["electrones"],el["neutrones"],el["A"]],
        "masa": el["masa"]
    })

@app.route('/api/grafica/todos')
def grafica_todos():
    desde = int(request.args.get('desde', 1))
    hasta  = int(request.args.get('hasta', len(ELEMENTS)))
    subset = [e for e in ELEMENTS if desde <= e["Z"] <= hasta]
    return jsonify({
        "labels":    [e["simbolo"]    for e in subset],
        "protones":  [e["protones"]   for e in subset],
        "electrones":[e["electrones"] for e in subset],
        "neutrones": [e["neutrones"]  for e in subset],
        "masico":    [e["A"]          for e in subset],
    })

if __name__ == '__main__':
    print("\n╔══════════════════════════════════════╗")
    print("║  🔬  TABLA PERIÓDICA · Servidor      ║")
    print("║  Abrir: http://localhost:5000         ║")
    print("╚══════════════════════════════════════╝\n")
    app.run(debug=False, port=5000)
