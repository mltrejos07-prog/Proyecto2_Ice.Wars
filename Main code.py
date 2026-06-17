#Import
import tkinter as tk
from PIL import Image, ImageTk #para poder utilizar imagenes en el juego
from tkinter import messagebox 


#Constantes
TAM = 75 # tam del pixel 

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

FILAS =len(matriz)
COLUMNAS = len(matriz[0])


#Funciones
def menu_principal(): #fondo del menu
    ventana.title("menu")
    ventana.geometry("600x400")

    img = Image.open("obj/menu.png")
    img = img.resize((600, 400))

    img_tk = ImageTk.PhotoImage(img)

    fondo = tk.Label(ventana, image=img_tk)
    fondo.image = img_tk
    fondo.place(x=0, y=0)
    
    boton_jugar = tk.Button(ventana, text="Jugar", command=abrir_jugar)
    boton_jugar.place(x=260, y=210)
    
    boton_top = tk.Button(ventana, text="Top de Jugadores")
    boton_top.place(x=235, y=260)
    
    boton_musica = tk.Button(ventana, text="Música")
    boton_musica.place(x=260, y=310)

#botones del menu
def abrir_jugar():
    ventana_jugar = tk.Toplevel(ventana) #ventana principal
    ventana_jugar.title("Inicio de Sesión")
    ventana_jugar.geometry("1000x600")

    img = Image.open("obj/session.png")   #fondo 
    img = img.resize((1000, 600))
    img_tk =ImageTk.PhotoImage(img)
    fondo = tk.Label(ventana_jugar, image=img_tk)
    fondo.image = img_tk
    fondo.place(x=0, y=0)
    
    faccion_atacante = tk.StringVar()    #variables 
    faccion_defensor = tk.StringVar()
  
#facciones del atacante 
    nombre_a  = tk.Entry(ventana_jugar)
    nombre_a.place(x=220, y=200)
    contra_a = tk.Entry(ventana_jugar, show="*") #Para que la contra no sea revelada 
    contra_a.place(x=220, y=250)
    tk.Radiobutton( ventana_jugar, text="Frutas", variable=faccion_atacante, value="Frutas").place(x=95, y=350)
    tk.Radiobutton( ventana_jugar, text="Helados", variable=faccion_atacante, value="Helados").place(x=95, y=375)
    tk.Radiobutton( ventana_jugar, text="Fantasmas", variable=faccion_atacante, value="Fantasmas").place(x=95, y=395)

#facciones del defensor
    nombre_d  = tk.Entry(ventana_jugar)
    nombre_d.place(x=720, y=200)
    contra_d = tk.Entry(ventana_jugar, show="*") 
    contra_d.place(x=720, y=250)
    tk.Radiobutton( ventana_jugar, text="Frutas", variable=faccion_defensor, value="Frutas").place(x=575, y=325)
    tk.Radiobutton( ventana_jugar, text="Helados", variable=faccion_defensor, value="Helados").place(x=575, y=350)
    tk.Radiobutton( ventana_jugar, text="Fantasmas", variable=faccion_defensor, value="Fantasmas").place(x=575, y=375)  

#boton de "comenzar"
    def comenzar():
        if nombre_a.get() == "":
            messagebox.showerror("ERROR", "Ingrese el nombre del atacante")
            return
        if nombre_d.get() == "":
            messagebox.showerror("ERROR", "Ingrese el nombre del defensor")
            return  
        if faccion_atacante.get() == faccion_defensor.get(): 
            messagebox.showerror("Error", "Las facciones deben ser diferentes") 
            return 
     
        abrir_editor_mapa()
    tk.Button(ventana_jugar, text="COMENZAR", command=comenzar).place(x=450, y=500)   
def abrir_editor_mapa():
    editor = tk.Toplevel(ventana)
    editor.title("Editor de Mapa")
    editor.geometry("1000x700")
    
# Canvas donde se dibuja el mapa
    canvas = tk.Canvas(
        editor,
        width=COLUMNAS * TAM,
        height=FILAS * TAM,
        bg="lightblue")

    canvas.pack(pady=20)

    # Dibujar el mapa
    for fila in range(FILAS):

        for col in range(COLUMNAS):

            x1 = col * TAM
            y1 = fila * TAM

            x2 = x1 + TAM
            y2 = y1 + TAM

            canvas.create_rectangle(
                x1,
                y1,
                x2,
                y2,
                outline="black")  

def abrir_top():
    ventana_top = tk.Toplevel(ventana)
    ventana_top.title("Top de jugadores")
    ventana_top.geometry("600x400")
    tk.Label(ventana_top, text= "Ranking de Jugaores").pack(pady=20)

#Ventana Principal 

ventana = tk.Tk()
menu_principal()

ventana.mainloop()
