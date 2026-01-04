import random

def process_order(nome_panino, inventario, burgers, state, lock):
    lock.acquire() #blocca le risorse finché non viene rilasciato

    ricetta = burgers[nome_panino]
    prezzo = ricetta["prezzo"]

    messaggio = "✅ Ordine completato"

    # sconto casuale
    if random.random() < 0.3:
        prezzo = int(prezzo * 0.8)
        messaggio = "🎉 Sconto applicato!"

    # controllo ingredienti
    for ingrediente in ricetta:
        if ingrediente != "prezzo" and inventario[ingrediente] < ricetta[ingrediente]:
            lock.release()
            return f"❌ Ingredienti insufficienti per {nome_panino}"

    # usa ingredienti
    for ingrediente in ricetta:
        if ingrediente != "prezzo":
            inventario[ingrediente] -= ricetta[ingrediente]

    # aggiorna soldi
    state["soldi"] += prezzo

    lock.release()

    return f"{messaggio}: +{prezzo}€"
#la f davanti alle virgolette indica che stiamo usando una f-string, cioè una stringa formattata in Python