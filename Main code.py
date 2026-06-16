#Import
import tkinter as tk
from PIL import Image, ImageTk #para poder utilizar imagenes en el juego
from tkinter import messagebox 


#Constantes
TAM = 40 # tam del pixel 

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
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]         
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
    
    boton_jugar = tk.Button(ventana, text="Jugar")
    boton_jugar.place(x=260, y=210)
    
    boton_top = tk.Button(ventana, text="Top de Jugadores")
    boton_top.place(x=235, y=260)
    
    boton_musica = tk.Button(ventana, text="Música")
    boton_musica.place(x=260, y=310)
    
    

#botones del menu
def abrir_jugar():
    ventana_jugar = tk.Toplevel(ventana)
    ventana_jugar.title("Jugar")
    ventana_jugar.geometry("600x400")
    tk.Label(ventana_jugar, text="Ventana de Juego").pack(pady=20)
    
def abrir_top():
    ventana_top = tk.Toplevel(ventana)
    ventana_top.title("Top de jugadores")
    ventana_top.geometry("600x400")
    tk.Label(ventana_top, text= "Ranking de Jugaores").pack(pady=20)

#Ventana Principal 

ventana = tk.Tk()
menu_principal()

ventana.mainloop()
