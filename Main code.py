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

    img = Image.open("menu.png")
    img = img.resize((600, 400))

    img_tk = ImageTk.PhotoImage(img)

    label = tk.Label(ventana, image=img_tk)
    label.image = img_tk  # importante
    label.pack()

#botones del menu
    
    


#Ventana Principal 

ventana = tk.Tk()
menu_principal()

ventana.mainloop()
#prueba de commit