#Import
import tkinter as tk
from PIL import Image, ImageTk #para poder utilizar imagenes en el juego
from tkinter import messagebox
from pygame import mixer
import json
import os

mixer.init() #musica de fondo
musica_activa = True
mixer.music.load("obj/music.mp3")
mixer.music.play(-1)

#Constantes
TAM = 60 # tam del pixel 
matriz = [
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],  
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],  
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
]
#variables para guardar la info de los jugadores para el ranking y el registro
jugador1 = {}
jugador2 = {}

FILAS =len(matriz)
COLUMNAS = len(matriz[0])
COL_BASE = 0
MITAD = COLUMNAS //2

FACCIONES = { #info de las facciones en la partida 
    "Esqueleto": {
        "soldado":{
            "nombre":"Soldado Esqueleto",
            "vida": 80, "daño": 15, "velocidad": 2,
            "costo": 8,
            "habilidad": "Ataque doble (3 turnos)"},
        "torre": {
            "nombre": "Torre Esqueleto",
            "vida": 150, "daño": 25, "alcance": 3,
            "costo": 12,
            "habilidad": "Disparo en área (5 turnos)"},
        "muro":{
            "nombre": "Muro Esqueleto",
                "vida": 200,
                "costo": 15,
                "habilidad": "—"
        },
    },
    "Fantasma": { 
        "soldado": {
            "nombre": "Soldado Fantasma",
            "vida": 60, "daño": 20, "velocidad": 3,
            "costo": 9,
            "habilidad": "Escudo temporal (4 turnos)"
        },
        "torre": {
            "nombre": "Torre Fantasma",
            "vida": 120, "daño": 20, "alcance": 4,
            "costo": 11,
            "habilidad": "Ralentiza enemigos (4 turnos)"
        },
        "muro": {
            "nombre": "Muro Fantasma",
            "vida": 150,
            "costo": 14,
            "habilidad": "Revive con 50 HP (1 vez)"
        },
    },
    "Helado": {
        "soldado": {
            "nombre": "Soldado Helado",
            "vida": 100, "daño": 10, "velocidad": 1,
            "costo": 10,
            "habilidad": "Curación +20 HP (c/3 turnos)"
        },
        "torre": {
            "nombre": "Torre Helada",
            "vida": 180, "daño": 15, "alcance": 3,
            "costo": 14,
            "habilidad": "Congela unidad 2 turnos (c/5 turnos)"
        },
        "muro": {
            "nombre": "Muro Helado",
            "vida": 250,
            "costo": 17,
            "habilidad": "Ralentiza al pasar"
        },
    },
}
ARCHIVO_JUGADORES ="Jugadores.json"  #guarda la info de las partidas 

class Unidad:
    def __init__(self, tipo, faccion, fila, col):
        datos = FACCIONES[faccion][tipo]
        self.tipo = tipo
        self.faccion = faccion
        self.fila = fila
        self.col = col
        self.vida = datos["vida"]
        self.vida_max = datos["vida"]
        self.daño = datos["daño"]
        self.velocidad = datos["velocidad"]
        self.habilidad = datos["habilidad"]
        self.turno_hab = 0       #cuenta los turnos para habilidad
        self.escudo = False  
        self.congelada = 0       #turnos que le quedan congelada
        self.imagen_id = None    #id del canvas
        self.barra_id = None    

    def esta_viva(self):
        return self.vida > 0

    def recibir_daño(self, cantidad):
        if self.escudo:
            self.escudo = False  #bloquea un golpe
            return
        self.vida -= cantidad
        if self.vida < 0:
            self.vida = 0

class Defensa:
    def __init__(self, tipo, faccion, fila, col):
        datos = FACCIONES[faccion][tipo]
        self.tipo = tipo
        self.faccion = faccion
        self.fila = fila
        self.col = col
        self.vida = datos["vida"]
        self.vida_max = datos["vida"]
        self.habilidad = datos["habilidad"]
        self.turno_hab = 0
        self.imagen_id = None
        self.barra_id  = None
        if tipo == "torre":
            self.daño = datos["daño"]
            self.alcance = datos["alcance"]
        else:
            self.daño = 0
            self.alcance = 0

    def esta_en_pie(self):
        return self.vida > 0

    def recibir_daño(self, cantidad):
        self.vida -= cantidad
        if self.vida < 0:
            self.vida = 0

class Ronda:
    def __init__(self, unidades, defensas, canvas, matriz, fila_base, col_base, callback_fin, tam, dinero_def_int, dinero_ata_int, dinero_def, dinero_ata):
        self.unidades = unidades
        self.defensas = defensas
        self.canvas = canvas
        self.matriz = matriz
        self.fila_base = fila_base
        self.col_base = col_base
        self.callback_fin = callback_fin
        self.tam = tam
        self.activa = False
        self.turno = 0
        self.dinero_def_int = dinero_def_int  
        self.dinero_ata_int = dinero_ata_int  
        self.dinero_def = dinero_def        
        self.dinero_ata = dinero_ata          

    def iniciar(self):
        self.activa = True
        self._tick()
    def _tick(self):
        if not self.activa:
            return
        self.turno += 1

        #Mueve y ataca cada unidad
        for u in list(self.unidades):
            if not u.esta_viva():
                continue
            if u.congelada > 0:
                u.congelada -= 1
                continue
            u.turno_hab += 1
            self._activar_habilidad_unidad(u)
            col_destino = u.col - 1
            col_destino = u.col - 1  #avanza hacia la izquierda

            #destino a la base
            if col_destino <= self.col_base:
                self.activa = False
                self.callback_fin("atacante")
                return

            #visualiza que hay en la casilla de destino
            contenido = self.matriz[u.fila][col_destino]
            if contenido == 0:
                #si hay una casilla libre se puede mover
                self.matriz[u.fila][u.col] = 0
                u.col = col_destino
                self.matriz[u.fila][u.col] = 2
                if u.imagen_id:
                    self.canvas.coords(u.imagen_id,
                        u.col * self.tam + self.tam // 2,
                        u.fila * self.tam + self.tam // 2)
            else:
                #si hay una unidad permite atacar
                objetivo = self._buscar_defensa(u.fila, col_destino)
                if objetivo:
                    objetivo.recibir_daño(u.daño) #atacante gana dinero por causar algun dano
                    if objetivo.tipo == "torre":
                        self.dinero_ata_int[0] += 3
                        self.dinero_ata.set(f"${self.dinero_ata_int[0]}")
                    if not objetivo.esta_en_pie():
                        #atacante gana extra por destruir
                        self.dinero_ata_int[0] += FACCIONES[objetivo.faccion][objetivo.tipo]["costo"]
                        self.dinero_ata.set(f"${self.dinero_ata_int[0]}")
                        self._eliminar_defensa(objetivo)
        #torres atacan a las unidades enemigas
        for d in list(self.defensas):
            if d.tipo != "torre":
                continue
            if not d.esta_en_pie():
                continue
            d.turno_hab += 1
            objetivo_encontrado = None
            for u in list(self.unidades):
                if not u.esta_viva():
                    continue
                distancia = abs(u.col - d.col) + abs(u.fila - d.fila)
                if distancia <= d.alcance:
                    objetivo_encontrado = u  #guarda la unidad atacada
                    u.recibir_daño(d.daño)
                    if not u.esta_viva():
                        self.eliminar_unidad(u)
                    break
            self._activar_habilidad_torre(d, objetivo_encontrado)  #llama habilidad
        
        #verificar la condicion de victoria
        self._verificar_victoria()
        if self.activa:
            self.canvas.after(3000, self._tick)

    def _activar_habilidad_unidad(self, u):
        if u.faccion == "Esqueleto":
            #ataque doble cada 3 turnos (su daño se duplica ese turno)
            if u.turno_hab % 3 == 0:
                u.daño *= 2
                self.canvas.after(100, lambda: setattr(u, 'daño', u.daño // 2))

        elif u.faccion == "Fantasma": #escudo temporal q se activa cada 4 turnos
            if u.turno_hab % 4 == 0:
                u.escudo = True

        elif u.faccion == "Helado": #curacion cada 3 turnos
            if u.turno_hab % 3 == 0:
                u.vida = min(u.vida + 20, u.vida_max)
    def _activar_habilidad_torre(self, torre, unidad_objetivo):
        if torre.faccion == "Esqueleto":
            #dispara en la casilla cada 5 turnos (daña a todas las unidades cercanas)
            if torre.turno_hab % 5 == 0:
                for u in list(self.unidades):
                    if u.esta_viva():
                        distancia = abs(u.col - torre.col) + abs(u.fila - torre.fila)
                        if distancia <= torre.alcance:
                            u.recibir_daño(torre.daño)
                            if not u.esta_viva():
                                self.eliminar_unidad(u)

        elif torre.faccion == "Fantasma": #ralentiza (congela 1 turno cada 4 turnos)
            if torre.turno_hab % 4 == 0:
                if unidad_objetivo and unidad_objetivo.esta_viva():
                    unidad_objetivo.congelada = max(unidad_objetivo.congelada, 1)

        elif torre.faccion == "Helado": #congela 2 turnos cada 5 turnos
            if torre.turno_hab % 5 == 0:
                if unidad_objetivo and unidad_objetivo.esta_viva():
                    unidad_objetivo.congelada = max(unidad_objetivo.congelada, 2)
    def _buscar_defensa(self, fila, col):
        for d in self.defensas:
            if d.fila == fila and d.col == col and d.esta_en_pie():
                return d
        return None

    def _eliminar_defensa(self, defensa):
        self.defensas.remove(defensa)
        self.matriz[defensa.fila][defensa.col] = 0
        if defensa.imagen_id:
            self.canvas.delete(defensa.imagen_id)
        if defensa.barra_id:
            self.canvas.delete(defensa.barra_id)
    def eliminar_unidad(self, unidad):
        if unidad in self.unidades:
            self.unidades.remove(unidad)
            self.matriz[unidad.fila][unidad.col] = 0
            if unidad.imagen_id:
                self.canvas.delete(unidad.imagen_id)
            if unidad.barra_id:
                self.canvas.delete(unidad.barra_id)
            #defensor gana dinero por eliminar unidad
            recompensa = FACCIONES[unidad.faccion][unidad.tipo]["costo"]
            self.dinero_def_int[0] += recompensa
            self.dinero_def.set(f"${self.dinero_def_int[0]}")
    def _verificar_victoria(self):
        if not self.unidades:
            self.activa = False
            self.callback_fin("defensor")

#funcion para hacer que el volumen se pause y se reanude
def control_musica():
    global musica_activa
    if musica_activa:
        mixer.music.pause()
        musica_activa = False
    else:
        mixer.music.unpause()
        musica_activa = True

#colores
COLOR_FONDO       = "#1a1a2e"
COLOR_PANEL       = "#16213e"
COLOR_TARJETA     = "#0f3460"
COLOR_BORDE       = "#e94560"
COLOR_TEXTO       = "#eaeaea"
COLOR_SUBTEXTO    = "#a0a0c0"
COLOR_DINERO      = "#f5c518"
COLOR_BTN_COLOCAR = "#e94560"
COLOR_BTN_HOVER   = "#c73652"
COLOR_RONDA       = "#0f3460"
COLOR_CANVAS_BG   = "#1e3a5f"
FUENTE_STAT   = ("Segoe UI", 8)
FUENTE_STAT_B = ("Segoe UI", 8, "bold")
FUENTE_DINERO = ("Segoe UI", 13, "bold")
FUENTE_FACCION= ("Segoe UI", 10, "italic")
FUENTE_RONDA  = ("Segoe UI", 13, "bold")
FUENTE_UNIDAD = ("Segoe UI", 9, "bold") 

#Funciones
def cargar_jugadores(): #Top de jugadores y guardado de registro
    if os.path.exists(ARCHIVO_JUGADORES):
        with open(ARCHIVO_JUGADORES, "r") as f:
            return json.load(f)
    return {}

def guardar_jugadores(datos):
    with open(ARCHIVO_JUGADORES, "w") as f:
        json.dump(datos, f, indent=4)

def registrar_o_login(nombre, contrasena):
    """Devuelve True si el login/registro fue exitoso, False si la contraseña es incorrecta."""
    datos = cargar_jugadores()
    if nombre in datos: #si hay un jugador verifica la contra
        if datos[nombre]["contrasena"] != contrasena:
            return False
    else: #jugador nuevo = registrar
        datos[nombre] = {
            "contrasena": contrasena,
            "victorias_atacante": 0,
            "victorias_defensor": 0
        }
        guardar_jugadores(datos)
    return True

def actualizar_victorias(nombre, rol):
    """rol es 'atacante' o 'defensor'"""
    datos = cargar_jugadores()
    if nombre in datos:
        datos[nombre][f"victorias_{rol}"] += 1
        guardar_jugadores(datos)


_cache_img = {} #logra Cargar imagenes/redimensionarlas 

def cargar_img(ruta, ancho, alto):
    clave = (ruta, ancho, alto)
    if clave not in _cache_img:
        try:
            img = Image.open(ruta).convert("RGBA").resize((ancho, alto), Image.LANCZOS)
            _cache_img[clave] = ImageTk.PhotoImage(img)
        except Exception:
            _cache_img[clave] = None
    return _cache_img[clave]

def boton_colocar(parent, texto, comando): #Boton con hover
    btn = tk.Button(parent, text=texto, command=comando, bg=COLOR_BTN_COLOCAR, fg="white",
        font=("Segoe UI", 8, "bold"), relief="flat", bd=0, padx=6, pady=3, cursor="hand2", activebackground=COLOR_BTN_HOVER, activeforeground="white")
    return btn

#panel lateral 
def crear_panel(parent, faccion, dinero_var, rol, seleccion_var, cmd_accion=None):
    es_defensor = rol == "defensor"
    lado_texto  = "DEFENSOR" if es_defensor else "ATACANTE"

    frame = tk.Frame(parent, bg=COLOR_PANEL, width=200)
    frame.pack_propagate(False)
    frame.pack(side="left" if es_defensor else "right", fill="y")

    #encabezado
    tk.Label(frame, text=lado_texto, bg=COLOR_PANEL, fg=COLOR_BORDE, font=("Segoe UI", 12, "bold"), pady=8).pack(fill="x")
    #dinero
    frame_dinero = tk.Frame(frame, bg=COLOR_PANEL)
    frame_dinero.pack(fill="x", padx=10, pady=(0, 4))
    tk.Label(frame_dinero, text="Dinero:", bg=COLOR_PANEL, fg=COLOR_SUBTEXTO, font=FUENTE_STAT_B).pack(side="left")
    tk.Label(frame_dinero, textvariable=dinero_var, bg=COLOR_PANEL, fg=COLOR_DINERO, font=FUENTE_DINERO).pack(side="left", padx=4)
    #Faccion
    frame_fac = tk.Frame(frame, bg=COLOR_PANEL)
    frame_fac.pack(fill="x", padx=10, pady=(0, 8))
    tk.Label(frame_fac, text="Facción:", bg=COLOR_PANEL, fg=COLOR_SUBTEXTO, font=FUENTE_STAT_B).pack(side="left")
    tk.Label(frame_fac, text=faccion, bg=COLOR_PANEL, fg=COLOR_TEXTO, font=FUENTE_FACCION).pack(side="left", padx=4)
    #separador del mapa
    tk.Frame(frame, bg=COLOR_BORDE, height=2).pack(fill="x", padx=10, pady=4)
    stats = FACCIONES[faccion]
    tipos = [
        ("soldado", "obj/soldado"),
        ("torre", "obj/torre"),
        ("muro", "obj/muro"),
    ]
    sufijo_faccion = {
        "Esqueleto": "esqueleto",
        "Fantasma": "ghost",
        "Helado": "helado",
    }
    sufijo = sufijo_faccion.get(faccion, faccion.lower())
    for tipo, ruta_base in tipos:
        datos = stats[tipo]
        ruta_img = f"{ruta_base}_{sufijo}.png"

        tarjeta = tk.Frame(frame, bg=COLOR_TARJETA, highlightbackground=COLOR_BORDE, highlightthickness=1)
        tarjeta.pack(fill="x", padx=8, pady=4, ipady=4)

        fila_top = tk.Frame(tarjeta, bg=COLOR_TARJETA)
        fila_top.pack(fill="x", padx=6, pady=(4, 2))

        img_tk = cargar_img(ruta_img, 36, 36)
        if img_tk:
            lbl_img = tk.Label(fila_top, image=img_tk, bg=COLOR_TARJETA)
            lbl_img.image = img_tk
            lbl_img.pack(side="left", padx=(0, 6))

        tk.Label(fila_top, text=f"{datos['nombre']}", bg=COLOR_TARJETA, fg=COLOR_TEXTO, font=FUENTE_UNIDAD, wraplength=130, justify="left").pack(side="left")
        #Stats del juego
        lineas_stats = []
        if tipo == "soldado":
            lineas_stats = [
                f"Vida: {datos['vida']} Daño: {datos['daño']}",
                f"Velocidad: {datos['velocidad']} casillas/turno",
            ]
        elif tipo == "torre":
            lineas_stats = [
                f"Vida: {datos['vida']} Daño: {datos['daño']}",
                f"Alcance: {datos['alcance']} casillas",
            ]
        else:
            lineas_stats = [f"Vida: {datos['vida']}"]
        lineas_stats.append(f"{datos['habilidad']}")
        lineas_stats.append(f"Costo: {datos['costo']}")
        for linea in lineas_stats:
            tk.Label(tarjeta, text=linea, bg=COLOR_TARJETA, fg=COLOR_SUBTEXTO, font=FUENTE_STAT, anchor="w").pack(fill="x", padx=10)

        #botón colocar
        def hacer_seleccionar(t=tipo):
            seleccion_var.set(t)
        btn = boton_colocar(tarjeta, f"Colocar {tipo}", hacer_seleccionar)
        btn.pack(pady=(4, 2))
        
    if es_defensor:
        tk.Button(frame, text="Defensor listo", bg="#2ecc71", fg="white", font=("Segoe UI", 10, "bold"), relief="flat", padx=12, pady=6, cursor="hand2", command=cmd_accion).pack(pady=8, padx=10, fill="x")
    else:
        tk.Button(frame, text="Iniciar Combate", bg=COLOR_BTN_COLOCAR, fg="white", font=("Segoe UI", 10, "bold"), relief="flat", padx=12, pady=6, cursor="hand2", command=cmd_accion).pack(pady=8, padx=10, fill="x")
    return frame 

#editor del mapa
def abrir_editor_mapa():
    editor = tk.Toplevel(ventana)
    editor.title("Juegooool")
    editor.configure(bg=COLOR_FONDO)
    editor.resizable(False, False)

#variables de estado
    ronda_actual  = tk.IntVar(value=1)
    victorias_def = tk.IntVar(value=0)
    victorias_ata = tk.IntVar(value=0)
    dinero_def = tk.StringVar(value="$100")
    dinero_ata = tk.StringVar(value="$100")
    seleccion_def = tk.StringVar(value="")
    seleccion_ata = tk.StringVar(value="")
    dinero_def_int = [100]
    dinero_ata_int = [100]
    fase_actual = tk.StringVar(value="defensor")

    faccion_def = jugador2.get("facción", "Esqueleto")
    faccion_ata = jugador1.get("facción", "Fantasma")
    
    contenedor = tk.Frame(editor, bg=COLOR_FONDO)
    contenedor.pack(fill="both", expand=True)

    centro = tk.Frame(contenedor, bg=COLOR_FONDO)
    centro.pack(side="left", fill="both", expand=True)
    
    frame_ronda = tk.Frame(centro, bg=COLOR_RONDA, highlightbackground=COLOR_BORDE, highlightthickness=2)
    frame_ronda.pack(pady=(10, 6), padx=20)

    tk.Label(frame_ronda, text="RONDA", bg=COLOR_RONDA, fg=COLOR_SUBTEXTO, font=("Segoe UI", 9, "bold"), padx=12).pack(side="left")
    tk.Label(frame_ronda, textvariable=ronda_actual, bg=COLOR_RONDA, fg=COLOR_BORDE, font=("Segoe UI", 16, "bold"), width=3).pack(side="left")
    tk.Frame(frame_ronda, bg=COLOR_BORDE, width=2).pack(side="left", fill="y", pady=4)
    tk.Label(frame_ronda, text="Defensor", bg=COLOR_RONDA, fg=COLOR_TEXTO, font=("Segoe UI", 12), padx=6).pack(side="left")
    tk.Label(frame_ronda, textvariable=victorias_def, bg=COLOR_RONDA, fg=COLOR_TEXTO, font=FUENTE_RONDA, width=2).pack(side="left")
    tk.Label(frame_ronda, text="vs", bg=COLOR_RONDA, fg=COLOR_SUBTEXTO, font=("Segoe UI", 10), padx=4).pack(side="left")
    tk.Label(frame_ronda, textvariable=victorias_ata, bg=COLOR_RONDA, fg=COLOR_TEXTO, font=FUENTE_RONDA, width=2).pack(side="left")
    tk.Label(frame_ronda, text="Atacante", bg=COLOR_RONDA, fg=COLOR_TEXTO, font=("Segoe UI", 12), padx=6).pack(side="left")
    
    lbl_fase = tk.Label(centro, bg=COLOR_FONDO, fg=COLOR_DINERO, font=("Segoe UI", 10, "bold"))
    lbl_fase.pack(pady=(0, 2))

    def actualizar_lbl_fase(*_):
        if fase_actual.get() == "defensor":
            lbl_fase.config(text="Turno del DEFENSOR — colocá tus defensas")
        else:
            lbl_fase.config(text="Turno del ATACANTE — colocá tus unidades")
    fase_actual.trace_add("write", actualizar_lbl_fase)
    actualizar_lbl_fase()
    
    canvas = tk.Canvas(centro, width=COLUMNAS*TAM, height=FILAS*TAM, bg=COLOR_CANVAS_BG, 
        highlightthickness=2, highlightbackground=COLOR_BORDE
    )
    canvas.pack(pady=6)  
    #cuadricula
    for fila in range(FILAS):
        for col in range(COLUMNAS):
            x1, y1 = col * TAM, fila * TAM
            x2, y2 = x1 + TAM, y1 + TAM
            if col == COL_BASE:
                relleno = "#1f3a2a"
            elif col < MITAD:
                relleno = "#1f2a4a"
            elif col == MITAD:
                relleno = "#0d1a2e"
            else:
                relleno = COLOR_CANVAS_BG
            canvas.create_line(MITAD * TAM, 0, MITAD * TAM, FILAS * TAM, fill=COLOR_BORDE, width=2, dash=(6, 4))
            canvas.create_rectangle(x1, y1, x2, y2, fill=relleno, outline="#2a4a7f")

    #base central del juego
    fila_base = FILAS // 2
    img_base  = cargar_img("obj/base_central.png", TAM - 4, TAM - 4)
    if img_base:
        bx = COL_BASE * TAM + TAM // 2
        by = fila_base * TAM + TAM // 2
        canvas.create_image(bx, by, image=img_base, anchor="center")
        canvas.image_base = img_base
    canvas.create_text(COL_BASE * TAM + TAM // 2, fila_base * TAM + TAM - 8, text="BASE", fill=COLOR_DINERO, font=("Segoe UI", 7, "bold"))

    #clic en el mapa
    imagenes_canvas = {}
    info_canvas = {}
    def click(event):
        col  = event.x // TAM
        fila = event.y // TAM
        if col < 0 or col >= COLUMNAS or fila < 0 or fila >= FILAS:
            return
        if col == COL_BASE and fila == fila_base:
            return

        fase = fase_actual.get()
        imagenes_sufijo = {"Esqueleto": "esqueleto", "Fantasma": "ghost", "Helado": "helado"}

        if fase == "defensor":
            if col == COL_BASE or col >= MITAD:
                return
            tipo = seleccion_def.get()
            if not tipo:
                return
            costo = FACCIONES[faccion_def][tipo]["costo"]
            if dinero_def_int[0] < costo:
                messagebox.showwarning("Sin dinero", f"No tenés ${costo} para colocar {tipo}")
                return
            dinero_def_int[0] -= costo
            dinero_def.set(f"${dinero_def_int[0]}")
            sufijo = imagenes_sufijo[faccion_def]
        else:
            if col <= MITAD:
                return
            tipo = seleccion_ata.get()
            if not tipo:
                return
            costo = FACCIONES[faccion_ata][tipo]["costo"]
            if dinero_ata_int[0] < costo:
                messagebox.showwarning("Sin dinero", f"No tenés ${costo} para colocar {tipo}")
                return
            dinero_ata_int[0] -= costo
            dinero_ata.set(f"${dinero_ata_int[0]}")
            sufijo = imagenes_sufijo[faccion_ata]

            #logra pintar gris en lugar de imagen (imagen aparece al iniciar combate)
        x1, y1 = col * TAM, fila * TAM
        canvas.create_rectangle(x1, y1, x1 + TAM, y1 + TAM, fill="#374a6e", outline="#2a4a7f")
            #guarda lo hay en cada celda para después pintar imágenes
        imagenes_canvas[(fila, col)] = (tipo, sufijo)
        info_canvas[(fila, col)] = (tipo, sufijo)
        matriz[fila][col] = 1
    canvas.bind("<Button-1>", click)
    frame_botones = tk.Frame(centro, bg=COLOR_FONDO)
    frame_botones.pack(pady=6)

    def defensor_listo():
        if fase_actual.get() == "defensor":
            fase_actual.set("atacante")
            btn_listo.config(state="disabled")
            btn_combate.config(state="normal")

    def iniciar_combate():
        #listas donde se guarda los objetos
        lista_unidades = []
        lista_defensas = []
        sufijo_map = {"Esqueleto": "esqueleto", "Fantasma": "ghost", "Helado": "helado"}

        #convierte imagenes_canvas en objetos Unidad o Defensa
        for (f, c), (tipo, sufijo) in info_canvas.items():
            img = cargar_img(f"obj/{tipo}_{sufijo}.png", TAM - 4, TAM - 4)
            item_id = None 
            if img:
                item_id = canvas.create_image(c * TAM + TAM // 2, f * TAM + TAM // 2, image=img, anchor="center")
                imagenes_canvas[(f, c)] = img
            #determina si es unidad atacante o defensa
            if c > MITAD:
                if tipo == "soldado":
                    obj = Unidad(tipo, faccion_ata, f, c)
                    obj.imagen_id = item_id
                    lista_unidades.append(obj)
                else:
                    obj = Defensa(tipo, faccion_ata, f, c)
                    obj.imagen_id = item_id
                    lista_defensas.append(obj)
                matriz[f][c] = 2
            else:
                obj = Defensa(tipo, faccion_def, f, c)
                obj.imagen_id = item_id
                lista_defensas.append(obj)
                matriz[f][c] = 1
        ronda = Ronda(lista_unidades, lista_defensas, canvas, matriz, fila_base, COL_BASE, fin_ronda, TAM, dinero_def_int, dinero_ata_int, dinero_def, dinero_ata)
        print("Unidades:", len(lista_unidades))
        print("Defensas:", len(lista_defensas))
        ronda.iniciar()

    def fin_ronda(ganador):
        if ganador == "atacante":
            victorias_ata.set(victorias_ata.get() + 1)
            messagebox.showinfo("Fin de ronda", "El ATACANTE gana la ronda")
        else:
            victorias_def.set(victorias_def.get() + 1)
            messagebox.showinfo("Fin de ronda", "El DEFENSOR gana la ronda")

        if victorias_ata.get() == 3:
            actualizar_victorias(jugador1["nombre"], "atacante")
            messagebox.showinfo("Fin del juego", f"{jugador1['nombre']} gana la partida")
            editor.destroy()
            return
        elif victorias_def.get() == 3: #guarda victoria
            actualizar_victorias(jugador2["nombre"], "defensor")
            messagebox.showinfo("Fin del juego", f"{jugador2['nombre']} gana la partida")
            editor.destroy()
            return

        #suma el dinero para la siguiente ronda
        dinero_def_int[0] += 100
        dinero_ata_int[0] += 100
        dinero_def.set(f"${dinero_def_int[0]}")
        dinero_ata.set(f"${dinero_ata_int[0]}")
        ronda_actual.set(ronda_actual.get() + 1)

        for f in range(FILAS):
            for c in range(COLUMNAS):
                matriz[f][c] = 0
        canvas.delete("all") #limpia el mapa
 
        for f in range(FILAS): #redibujar cuadricula
            for c in range(COLUMNAS):
                x1, y1 = c * TAM, f * TAM
                x2, y2 = x1 + TAM, y1 + TAM
                if c == COL_BASE:
                    relleno = "#1f3a2a"
                elif c < MITAD:
                    relleno = "#1f2a4a"
                elif c == MITAD:
                    relleno = "#0d1a2e"
                else:
                    relleno = COLOR_CANVAS_BG
                canvas.create_rectangle(x1, y1, x2, y2, fill=relleno, outline="#2a4a7f")
        canvas.create_line(MITAD * TAM, 0, MITAD * TAM, FILAS * TAM, fill=COLOR_BORDE, width=2, dash=(6, 4))

        if img_base:
            canvas.create_image(COL_BASE * TAM + TAM // 2, fila_base * TAM + TAM // 2, image=img_base, anchor="center")
        canvas.create_text(COL_BASE * TAM + TAM // 2, fila_base * TAM + TAM - 8, text="BASE", fill=COLOR_DINERO, font=("Segoe UI", 7, "bold"))

        #limpia diccionarios y reinicia la fase
        info_canvas.clear()
        imagenes_canvas.clear()
        fase_actual.set("defensor")
        btn_listo.config(state="normal")
        btn_combate.config(state="disabled")

    btn_listo = tk.Button(frame_botones, text="Defensor listo", command=defensor_listo, bg="#2ecc71", fg="white", font=("Segoe UI", 10, "bold"), relief="flat", padx=12, pady=6, cursor="hand2")
    btn_listo.pack(side="left", padx=10)

    btn_combate = tk.Button(frame_botones, text="Iniciar Combate", command=iniciar_combate, bg=COLOR_BTN_COLOCAR, fg="white", font=("Segoe UI", 10, "bold"), relief="flat", padx=12, pady=6, cursor="hand2", state="disabled")
    btn_combate.pack(side="left", padx=10)
    
    panel_izq = crear_panel(contenedor, faccion_def, dinero_def, "defensor", seleccion_def, cmd_accion=defensor_listo)
    panel_der = crear_panel(contenedor, faccion_ata, dinero_ata, "atacante", seleccion_ata, cmd_accion=iniciar_combate)

    ancho_total = 200 + COLUMNAS*TAM + 200
    alto_total  = FILAS * TAM + 220 #no se veia el boton "defensor listo"
    editor.geometry(f"{ancho_total}x{alto_total}")
    
def menu_principal():
    ventana.title("juegooool")
    ventana.geometry("600x400")
    try:
        img = Image.open("obj/menu.png").resize((600, 400))
        img_tk = ImageTk.PhotoImage(img)
        fondo = tk.Label(ventana, image=img_tk)
        fondo.image = img_tk
        fondo.place(x=0, y=0)
    except Exception:
        ventana.configure(bg=COLOR_FONDO)

    tk.Button(ventana, text="Jugar", command=abrir_jugar).place(x=260, y=210)
    tk.Button(ventana, text="Top de Jugadores", command=abrir_top).place(x=235, y=260)    
    img_tk = ImageTk.PhotoImage(img)
    
    boton_musica = tk.Button(ventana, text="Música", command=control_musica)
    boton_musica.place(x=260, y=310)

#botones del menu
def abrir_jugar():
    ventana_jugar = tk.Toplevel(ventana)
    ventana_jugar.title("Inicio de Sesión")
    ventana_jugar.geometry("1000x600")

    try:
        img = Image.open("obj/session.png").resize((1000, 600))
        img_tk = ImageTk.PhotoImage(img)
        fondo = tk.Label(ventana_jugar, image=img_tk)
        fondo.image = img_tk
        fondo.place(x=0, y=0)
    except Exception:
        ventana_jugar.configure(bg=COLOR_FONDO)
    faccion_atacante = tk.StringVar()
    faccion_defensor = tk.StringVar()

    nombre_a = tk.Entry(ventana_jugar); nombre_a.place(x=220, y=200)
    contra_a = tk.Entry(ventana_jugar, show="*"); contra_a.place(x=220, y=250)
    for i, fac in enumerate(["Esqueleto", "Fantasma", "Helado"]):
        tk.Radiobutton(ventana_jugar, text=fac, variable=faccion_atacante, value=fac).place(x=95, y=350 + i*25)

    nombre_d = tk.Entry(ventana_jugar); nombre_d.place(x=720, y=200)
    contra_d = tk.Entry(ventana_jugar, show="*"); contra_d.place(x=720, y=250)
    for i, fac in enumerate(["Esqueleto", "Fantasma", "Helado"]):
        tk.Radiobutton(ventana_jugar, text=fac, variable=faccion_defensor, value=fac).place(x=575, y=325 + i*25)

    def comenzar():
        campos = [
            (nombre_a.get(), "nombre del atacante"),
            (nombre_d.get(), "nombre del defensor"),
            (contra_a.get(), "contraseña del atacante"),
            (contra_d.get(), "contraseña del defensor"),
        ]
        for valor, etiqueta in campos:
            if not valor:
                messagebox.showerror("ERROR", f"Ingrese el {etiqueta}")
                return
        if not faccion_atacante.get():
            messagebox.showerror("ERROR", "Seleccione la facción del atacante"); return
        if not faccion_defensor.get():
            messagebox.showerror("ERROR", "Seleccione la facción del defensor"); return
        if faccion_atacante.get() == faccion_defensor.get():
            messagebox.showerror("ERROR", "Los jugadores no pueden usar la misma facción"); return

        #verifica login/registro
        if not registrar_o_login(nombre_a.get(), contra_a.get()):
            messagebox.showerror("ERROR", "Contraseña incorrecta para el atacante"); return
        if not registrar_o_login(nombre_d.get(), contra_d.get()):
            messagebox.showerror("ERROR", "Contraseña incorrecta para el defensor"); return

        jugador1.update({"nombre": nombre_a.get(), "contraseña": contra_a.get(), "facción": faccion_atacante.get()})
        jugador2.update({"nombre": nombre_d.get(), "contraseña": contra_d.get(), "facción": faccion_defensor.get()})
        ventana_jugar.destroy()
        abrir_editor_mapa()
    tk.Button(ventana_jugar, text="COMENZAR", command=comenzar).place(x=450, y=500)

def abrir_top():
    ventana_top = tk.Toplevel(ventana)
    ventana_top.title("Top de Jugadores")
    ventana_top.geometry("600x450")
    ventana_top.configure(bg=COLOR_FONDO)

    tk.Label(ventana_top, text="TOP DE JUGADORES", bg=COLOR_FONDO,
             fg=COLOR_BORDE, font=("Segoe UI", 16, "bold")).pack(pady=15)

    datos = cargar_jugadores()

    #ordena por victorias atacante y defensor
    top_atacantes = sorted(datos.items(), key=lambda x: x[1]["victorias_atacante"], reverse=True)[:5]
    top_defensores = sorted(datos.items(), key=lambda x: x[1]["victorias_defensor"], reverse=True)[:5]

    frame_tablas = tk.Frame(ventana_top, bg=COLOR_FONDO)
    frame_tablas.pack(fill="both", expand=True, padx=20)
    frame_ata = tk.Frame(frame_tablas, bg=COLOR_PANEL)
    frame_ata.pack(side="left", fill="both", expand=True, padx=10)
    tk.Label(frame_ata, text="Top Atacantes", bg=COLOR_PANEL, fg=COLOR_DINERO, font=("Segoe UI", 11, "bold")).pack(pady=8)

    for i, (nombre, info) in enumerate(top_atacantes, 1):
        texto = f"{i}. {nombre}  —  {info['victorias_atacante']} victorias"
        tk.Label(frame_ata, text=texto, bg=COLOR_PANEL, fg=COLOR_TEXTO,
                 font=("Segoe UI", 10)).pack(anchor="w", padx=10, pady=3)

    frame_def = tk.Frame(frame_tablas, bg=COLOR_PANEL)
    frame_def.pack(side="left", fill="both", expand=True, padx=10)
    tk.Label(frame_def, text="Top Defensores", bg=COLOR_PANEL, fg=COLOR_DINERO, font=("Segoe UI", 11, "bold")).pack(pady=8)

    for i, (nombre, info) in enumerate(top_defensores, 1):
        texto = f"{i}. {nombre}  —  {info['victorias_defensor']} victorias"
        tk.Label(frame_def, text=texto, bg=COLOR_PANEL, fg=COLOR_TEXTO, font=("Segoe UI", 10)).pack(anchor="w", padx=10, pady=3)

#Ventana Principal 
ventana = tk.Tk()
menu_principal()
ventana.mainloop()