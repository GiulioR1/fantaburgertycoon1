import tkinter as tk
from tkinter import ttk
import json
import threading
from ordini import process_order  # importa la logica ordini

# --- CARICA DATI ---
with open("data/inventario.json") as f:
    inventario = json.load(f)

with open("data/burgers.json") as f:
    burgers = json.load(f)

with open("data/state.json") as f:
    state = json.load(f)

lock = threading.Lock()

# --- FUNZIONI ---
def salva():
    """Salva soldi e ingredienti su JSON"""
    with open("data/inventario.json", "w") as f:
        json.dump(inventario, f, indent=4)
    with open("data/state.json", "w") as f:
        json.dump(state, f, indent=4)

def aggiorna_gui():
    """Aggiorna soldi e ingredienti nella GUI"""
    soldi_label.config(text="💰 Soldi: " + str(state["soldi"]) + " €") #convertiamo in stringa
     #Perché alcune funzioni per concatenare il testo o etc., non funzionano se provi a concatenare un numero con del testo
    inv_label.config(text="📦 Ingredienti: " + str(inventario))

def fai_ordine():
    """Funzione chiamata dal bottone per fare un ordine"""
    panino_scelto = panino_var.get()
    if panino_scelto not in burgers:
        risultato_label.config(text="❌ Panino non valido")
        return

    def thread_ordine():
        # Esegui la logica dell'ordine (thread)
        risultato = process_order(panino_scelto, inventario, burgers, state, lock)
        salva()
        # Aggiorna GUI in sicurezza nel main thread
        def aggiorna():
            risultato_label.config(text=risultato)
            aggiorna_gui()
        root.after(0, aggiorna)

    t = threading.Thread(target=thread_ordine)
    t.start()

# --- CREAZIONE FINESTRA GUI ---
root = tk.Tk()
root.title("🍔 FantaBurger Delivery Tycoon")
root.geometry("450x300")

# Titolo
titolo = tk.Label(root, text="FantaBurger Delivery Tycoon", font=("Arial", 16, "bold"))
titolo.pack(pady=10)

# Soldi e ingredienti
soldi_label = tk.Label(root, text="") #Qui è vuoto ("") perché non vogliamo mostrare 
#nulla all’apertura della finestra, verrà aggiornato più tardi quando si fa un ordine.
soldi_label.pack()
inv_label = tk.Label(root, text="")
inv_label.pack(pady=5)

# Menu a tendina per scegliere panino
panino_var = tk.StringVar()
panino_var.set(list(burgers.keys())[0])  # valore di default
menu_panini = ttk.Combobox(root, textvariable=panino_var, values=list(burgers.keys()), state="readonly")
menu_panini.pack(pady=10)

# Bottone per fare ordine
bottone = tk.Button(root, text="🍔 Fai ordine", command=fai_ordine, height=2, width=20)
bottone.pack(pady=10)

# Messaggio ordine
risultato_label = tk.Label(root, text="", wraplength=400)
risultato_label.pack(pady=10) #significa padding verticale, cioè spazio sopra e sotto la label.

# Aggiorna GUI iniziale
aggiorna_gui()

# --- PERMETTE IMPORT IN main.py ---
if __name__ == "__main__":
    root.mainloop()
