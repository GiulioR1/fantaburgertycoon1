import json
import threading
from ordini import process_order
import gui  # importa gui.py

#CARICA DATI
with open("data/inventario.json") as f: #as f assegna il file appena aperto a una variabile chiamata f
    inventario = json.load(f)

with open("data/burgers.json") as f:
    burgers = json.load(f)

with open("data/state.json") as f:
    state = json.load(f)

lock = threading.Lock()

#CLI
def salva():
    with open("data/inventario.json", "w") as f: #w = write
        json.dump(inventario, f, indent=4)
    with open("data/state.json", "w") as f:
        json.dump(state, f, indent=4)

def mostra_stato():
    print("\n💰 Soldi:", state["soldi"])
    print("📦 Ingredienti:", inventario)

def ordine_cli(panino):
    risultato = process_order(panino, inventario, burgers, state, lock)
    print(risultato)
    salva()

def cli_thread_func():
    while True:
        print("\n--- MENU CLI ---")
        print("1. Mostra stato")
        print("2. Fai ordine")
        print("3. Esci")
        scelta = input("Scegli un’opzione: ")

        if scelta == "1":
            mostra_stato()

        elif scelta == "2":
            print("\nPanini disponibili:")
            for panino in burgers:
                print("-", panino)
            nome = input("Quale panino vuoi ordinare? ")
            if nome not in burgers:
                print("❌ Panino non disponibile")
                continue
            # esegue ordine CLI
            ordine_cli(nome)

        elif scelta == "3":
            print("💾 Salvataggio dati e uscita...")
            salva()
            break

        else:
            print("❌ Scelta non valida")

# --- MAIN ---
if __name__ == "__main__":
    print("🍔 Avvio FantaBurger Delivery Tycoon (CLI + GUI)")

    # Avvia CLI in un thread separato
    cli_thread = threading.Thread(target=cli_thread_func, daemon=True)
    cli_thread.start()

    # Avvia GUI nel thread principale (Windows richiede questo)
    gui.root.mainloop()
