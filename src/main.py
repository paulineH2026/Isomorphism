### Interface Graphique """

import tkinter as tk
from tkinter import Scrollbar
from tkinter import Listbox

from complexite import list_directory_files

# Initialisation de l'interface #

interface = tk.Tk()
interface.title(" TER Signatures - Isomorphismes")
interface.config(bg="skyblue")

# fenêtres principales
left_frame  =  tk.Frame(interface,  width=300,  height= 600,  bg='grey')
left_frame.grid(row=0,  column=0, padx=5,  pady=5)

right_frame  =  tk.Frame(interface,  width=300,  height=600,  bg='grey')
right_frame.grid(row=0,  column=1,  padx=5,  pady=5)

tk.Label(left_frame,  text="Exemples",  relief=tk.RAISED).grid(row=0,  column=0,  padx=5,  pady=5)
tk.Label(right_frame,  text="Applications",  relief=tk.RAISED).grid(row=0,  column=0,  padx=5,  pady=5)

# bouton pour générer des signatures
signature = tk.Button(right_frame, text='Générer des signatures', bg='light gray', fg='#D2691E', font="Helvetica 16 bold italic")
signature.grid(row=1,  column=0,  padx=5,  pady=5,  sticky='w'+'e'+'n'+'s')

# bouton pour faire des test d'isomorphisme
isomorphisme = tk.Button(right_frame, text="Test d'isomorphismes", bg='light gray', fg='#D2691E', font="Helvetica 16 bold italic")
isomorphisme.grid(row=2,  column=0,  padx=5,  pady=5,  sticky='w'+'e'+'n'+'s')

# bouton pour visualiser graphiquement les exemples
dessin = tk.Button(right_frame, text='Visualisation', bg='light gray', fg='#D2691E', font="Helvetica 16 bold italic")
dessin.grid(row=3,  column=0,  padx=5,  pady=5,  sticky='w'+'e'+'n'+'s')

# bouton pour afficher les courbes de complexite
complexite = tk.Button(right_frame, text='Courbes de complexité', bg='light gray', fg='#D2691E', font="Helvetica 16 bold italic")
complexite.grid(row=4,  column=0,  padx=5,  pady=5,  sticky='w'+'e'+'n'+'s')

# pour scroller de manière verticale

scrollbar = Scrollbar(left_frame) 
scrollbar.grid(row=1,  column=1,  padx=5,  pady=5)

scroll = Listbox(left_frame, selectmode = "multiple", yscrollcommand=scrollbar.set, width = 25, height=30, bg="light gray")
scroll.grid(row=1,  column=0,  padx=5,  pady=5)

examples = list_directory_files("plantri_graph")
for example in examples:
    if "ex" in example:
        scroll.insert(tk.END, example)

scrollbar.config(command = scroll.yview)

interface.mainloop()
