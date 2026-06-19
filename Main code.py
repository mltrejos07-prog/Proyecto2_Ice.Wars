#Import
import tkinter as tk
from PIL import Image, ImageTk #para poder utilizar imagenes en el juego
from tkinter import messagebox
from pygame import mixer

#musica de fondo
mixer.init()
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
#Aqui se guardara la info de los jugadores para el ranking y el registro
jugador1 = {}
jugador2 = {}

FILAS =len(matriz)
COLUMNAS = len(matriz[0])
COL_BASE = COLUMNAS-1

FACCIONES = {
    "Esqueleto": {
        "soladado":{
            "nombre":"Soldado Esqueeto",
            "vida": 80, "daño": 15, "velocidad": 2,
            "costo": 50,
            "habilidad": "Ataque doble (3 turnos)"},
        "torre": {
            "nombre": "Torre Esqueleto",
            "vida": 150, "daño": 25, "alcance": 3,
            "costo": 100,
            "habilidad": "Disparo en área (5 turnos)"},
        "muro":{
            "nombre": "Muro Esqueleto",
                "vida": 200,
                "costo": 40,
                "habilidad": "—"
        },
    },
    "Fantasma": {
        "soldado": {
            "nombre": "Soldado Fantasma",
            "vida": 60, "daño": 20, "velocidad": 3,
            "costo": 60,
            "habilidad": "Escudo temporal (c/4 turnos)"
        },
        "torre": {
            "nombre": "Torre Fantasma",
            "vida": 120, "daño": 20, "alcance": 4,
            "costo": 90,
            "habilidad": "Ralentiza enemigos (c/4 turnos)"
        },
        "muro": {
            "nombre": "Muro Fantasma",
            "vida": 150,
            "costo": 35,
            "habilidad": "Revive con 50 HP (1 vez)"
        },
    },
    "Helado": {
        "soldado": {
            "nombre": "Soldado Helado",
            "vida": 100, "daño": 10, "velocidad": 1,
            "costo": 45,
            "habilidad": "Curación +20 HP (c/3 turnos)"
        },
        "torre": {
            "nombre": "Torre Helada",
            "vida": 180, "daño": 15, "alcance": 3,
            "costo": 110,
            "habilidad": "Congela unidad 2 turnos (c/5 turnos)"
        },
        "muro": {
            "nombre": "Muro Helado",
            "vida": 250,
            "costo": 50,
            "habilidad": "Ralentiza al pasar"
        },
    },
}

#color
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
_cache_img = {} #Logra Cargar imagenes/redimensionarlas 

def cargar_img(ruta, ancho, alto):
    clave = (ruta, ancho, alto)
    if clave not in _cache_img:
        try:
            img = Image.open(ruta).convert("RGBA").resize((ancho, alto), Image.LANCZOS)
            _cache_img[clave] = ImageTk.PhotoImage(img)
        except Exception:
            _cache_img[clave] = None
    return _cache_img[clave]

def boton_colocar(parent, texto, comando): #Boton con hover? 
    btn = tk.Button(parent, text=texto, command=comando, bg=COLOR_BTN_COLOCAR, fg="white",
        font=("Segoe UI", 8, "bold"),
        relief="flat", bd=0, padx=6, pady=3, cursor="hand2",
        activebackground=COLOR_BTN_HOVER,
        activeforeground="white")
    return btn

#panel lateral 
def crear_panel(parent, faccion, dinero_var, rol, seleccion_var):
    es_defensor = rol == "defensor"
    lado_texto  = "DEFENSOR" if es_defensor else "ATACANTE"

    frame = tk.Frame(parent, bg=COLOR_PANEL, width=200)
    frame.pack_propagate(False)
    frame.pack(side="left" if es_defensor else "right", fill="y")

    #encabezado
    tk.Label(frame, text=lado_texto, bg=COLOR_PANEL, fg=COLOR_BORDE, font=("Segoe UI", 12, "bold"), pady=8).pack(fill="x")
    #Dinero
    frame_dinero = tk.Frame(frame, bg=COLOR_PANEL)
    frame_dinero.pack(fill="x", padx=10, pady=(0, 4))
    tk.Label(frame_dinero, text="💰 Dinero:", bg=COLOR_PANEL, fg=COLOR_SUBTEXTO, font=FUENTE_STAT_B).pack(side="left")
    tk.Label(frame_dinero, textvariable=dinero_var, bg=COLOR_PANEL, fg=COLOR_DINERO, font=FUENTE_DINERO).pack(side="left", padx=4)
    #Faccion
    frame_fac = tk.Frame(frame, bg=COLOR_PANEL)
    frame_fac.pack(fill="x", padx=10, pady=(0, 8))
    tk.Label(frame_fac, text="🏴 Facción:", bg=COLOR_PANEL, fg=COLOR_SUBTEXTO, font=FUENTE_STAT_B).pack(side="left")
    tk.Label(frame_fac, text=faccion, bg=COLOR_PANEL, fg=COLOR_TEXTO, font=FUENTE_FACCION).pack(side="left", padx=4)
    #Separador 
    tk.Frame(frame, bg=COLOR_BORDE, height=2).pack(fill="x", padx=10, pady=4)
    #Tarjeta de unidades
    stats = FACCIONES[faccion]
    tipos = [
        ("soldado", "obj/soldado"),
        ("torre", "obj/torre"),
        ("muro", "obj/muro"),
    ]
    sufijo_faccion = {
        "Esqueleto": "esqueleto",
        "Fantasma":  "ghost",
        "Helado":    "helado",
    }
    sufijo = sufijo_faccion.get(faccion, faccion.lower())
    
    for tipo, icono, ruta_base in tipos:
        datos = stats[tipo]
        ruta_img = f"{ruta_base}_{sufijo}.png"

        tarjeta = tk.Frame(frame, bg=COLOR_TARJETA, highlightbackground=COLOR_BORDE, highlightthickness=1)
        tarjeta.pack(fill="x", padx=8, pady=4, ipady=4)

        #Imagen + nombre
        fila_top = tk.Frame(tarjeta, bg=COLOR_TARJETA)
        fila_top.pack(fill="x", padx=6, pady=(4, 2))

        img_tk = cargar_img(ruta_img, 36, 36)
        if img_tk:
            lbl_img = tk.Label(fila_top, image=img_tk, bg=COLOR_TARJETA)
            lbl_img.image = img_tk
            lbl_img.pack(side="left", padx=(0, 6))

        tk.Label(fila_top, text=f"{icono} {datos['nombre']}", bg=COLOR_TARJETA, fg=COLOR_TEXTO, font=FUENTE_UNIDAD, wraplength=130, justify="left").pack(side="left")
        #Stats
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

        # Botón colocar
        def hacer_seleccionar(t=tipo):
            seleccion_var.set(t)
            messagebox.showinfo("Unidad seleccionada", f"Haz clic en el mapa para colocar: {t}")

        btn = boton_colocar(tarjeta, f"Colocar {tipo}", hacer_seleccionar)
        btn.pack(pady=(4, 2))
    return frame 
#editor del mapa
def abrir_editor_mapa():
    editor = tk.Toplevel(ventana)
    editor.title("Defensa y Asalto de Base")
    editor.configure(bg=COLOR_FONDO)
    editor.resizable(False, False)

    # Variables de estado
    ronda_actual  = tk.IntVar(value=1)
    victorias_def = tk.IntVar(value=0)
    victorias_ata = tk.IntVar(value=0)
    dinero_def = tk.StringVar(value="$100")
    dinero_ata = tk.StringVar(value="$100")
    seleccion_def = tk.StringVar(value="")
    seleccion_ata = tk.StringVar(value="")

    faccion_def = jugador2.get("facción", "Esqueleto")
    faccion_ata = jugador1.get("facción", "Fantasma")
    
    contenedor = tk.Frame(editor, bg=COLOR_FONDO)
    contenedor.pack(fill="both", expand=True)

    panel_izq = crear_panel(contenedor, faccion_def, dinero_def, "defensor", seleccion_def)
    panel_der = crear_panel(contenedor, faccion_ata, dinero_ata, "atacante", seleccion_ata)

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
    
    canvas = tk.Canvas(centro, width=COLUMNAS * TAM, height=FILAS * TAM, bg=COLOR_CANVAS_BG, 
        highlightthickness=2, highlightbackground=COLOR_BORDE
    )
    canvas.pack(pady=6)  
    #cuadricula
    for fila in range(FILAS):
        for col in range(COLUMNAS):
            x1, y1 = col * TAM, fila * TAM
            x2, y2 = x1 + TAM, y1 + TAM
            if col == 0:
                relleno = "#1f2a4a"
            elif col == COL_BASE:
                relleno = "#1f3a2a"
            else:
                relleno = COLOR_CANVAS_BG
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
    def click(event):
        col  = event.x // TAM
        fila = event.y // TAM
        if col < 0 or col >= COLUMNAS or fila < 0 or fila >= FILAS:
            return
        if col == COL_BASE and fila == fila_base:
            return
        matriz[fila][col] = 1
        x1, y1 = col * TAM, fila * TAM
        x2, y2 = x1 + TAM, y1 + TAM
        canvas.create_rectangle(x1, y1, x2, y2, fill="#374a6e", outline="#2a4a7f")
    canvas.bind("<Button-1>", click)

    ancho_total = 200 + COLUMNAS * TAM + 200
    alto_total  = FILAS * TAM + 120
    editor.geometry(f"{ancho_total}x{alto_total}")
    
def menu_principal():
    ventana.title("Defensa y Asalto de Base")
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
    tk.Button(ventana, text="Música")
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

        jugador1.update({"nombre": nombre_a.get(), "contraseña": contra_a.get(), "facción": faccion_atacante.get()})
        jugador2.update({"nombre": nombre_d.get(), "contraseña": contra_d.get(), "facción": faccion_defensor.get()})
        ventana_jugar.destroy()
        abrir_editor_mapa()

    tk.Button(ventana_jugar, text="COMENZAR", command=comenzar).place(x=450, y=500)

def abrir_top():
    ventana_top = tk.Toplevel(ventana)
    ventana_top.title("Top de Jugadores")
    ventana_top.geometry("600x400")
    tk.Label(ventana_top, text="Ranking de Jugadores").pack(pady=20)

#Ventana Principal 
ventana = tk.Tk()
menu_principal()
ventana.mainloop()