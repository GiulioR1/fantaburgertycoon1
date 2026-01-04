# fantaburgertycoon1
Descrizione del Progetto: FantaBurger Delivery Tycoon
I fanatici 🔥: Francesco Pio Marasca, Russo Giulio, Avellino Gennaro, Esposito Catello

Il progetto consiste nella simulazione di una paninoteca realizzata in Python e permette di gestire ingredienti, ordini e soldi.

Gli ordini vengono gestiti in modo concorrente usando i thread, così più clienti possono "ordinare" nello stesso momento.
I dati vengono salvati in file JSON (JavaScript Object Notation), ovvero un formato di testo per salvare i dati, simile
a un dizionario Python: coppie chiave-valore

È presente anche un evento casuale di sconto (tramite import random)

Il progetto viene avviato sia da terminale CLI (Command Line Interface) e sia con una interfaccia grafica (GUI) realizzata
con tkinter

Nel file orders.py la funzione process_order prende come parametri il nome del panino, l’inventario, le ricette, lo stato del gioco e un lock per la concorrenza.
 La funzione verifica se ci sono ingredienti sufficienti, applica eventuali sconti casuali, riduce gli ingredienti utilizzati, aumenta i soldi del giocatore e restituisce un messaggio
 con il risultato dell’ordine. Abbiamo usato il lock per proteggere risorse condivise come soldi e ingredienti e impedire conflitti quando più thread eseguono ordini contemporaneamente.

Nel file main.py abbiamo creato un menu testuale per la CLI. L’utente può visualizzare lo stato della paninoteca, fare un ordine selezionando un panino o 
uscire dal programma. Ogni ordine eseguito sia dalla CLI sia dalla GUI aggiorna lo stato e salva i dati nei file JSON.

Nel file gui.py la finestra grafica mostra il titolo del gioco, soldi, ingredienti e un menu a tendina per scegliere il panino. 
Cliccando sul bottone “Fai ordine” parte un thread che esegue la funzione process_order e poi aggiorna la GUI in sicurezza usando root.after(0, ...). Abbiamo usato after 
perché Tkinter non permette di aggiornare i widget da thread diversi dal thread principale. Tutti i dati aggiornati vengono salvati automaticamente nei file JSON.

----------------------------------------------------------------------------------------
Spiegazione di alcune istruzioni nel main:

json.dump() che è una funzione del modulo json
Serve a trasformare un oggetto Python (come un dizionario o una lista) in formato JSON e scriverlo direttamente in un file.

with open("data/inventario.json") as f:
serve per aprire un file in Python e lavorarci dentro un “blocco sicuro”
with crea un blocco di codice sicuro,
f è una variabile temporanea che rappresenta il file aperto. Dentro il blocco puoi leggere o scrivere sul file usando f.

lock = threading.Lock()
crea un oggetto chiamato lock (a volte chiamato anche mutex).
Serve a proteggere risorse condivise quando più thread possono accedervi contemporaneamente.
----------------------------------------------------------------------------------------------
Spiegazione di alcune istruzioni nel gui.py:

root è l’oggetto principale di Tkinter che rappresenta tutta la finestra. 
Tutti i widget (label, bottoni, menu a tendina, ecc.) devono essere “attaccati” a questa finestra.


panino_var = tk.StringVar() 
panino_var.set(list(burgers.keys())[0]) # valore di default 
menu_panini = ttk.Combobox(root, textvariable=panino_var, values=list(burgers.keys()), state="readonly")

La variabile panino_var viene creata con tk.StringVar() e serve a memorizzare il valore selezionato dall’utente nel 
menu a tendina. In pratica è una variabile speciale di Tkinter che si collega al widget e aggiorna automaticamente 
il suo valore quando l’utente sceglie un elemento. Subito dopo impostiamo un valore di default 
con panino_var.set(list(burgers.keys())[0]), cioè scegliamo come primo panino quello che compare 
per primo nell’elenco delle chiavi del dizionario burgers, così quando la GUI si apre il menu non è vuoto 
ma mostra già un panino selezionato. Poi creiamo il menu a tendina vero e proprio
 con ttk.Combobox(root, textvariable=panino_var, values=list(burgers.keys()), state="readonly"). 
Qui passiamo root come finestra principale dove inserire il widget, colleghiamo il menu a panino_var in
 modo che la variabile tenga traccia della scelta dell’utente, impostiamo come valori del menu tutte le 
chiavi del dizionario burgers che corrispondono ai panini disponibili e mettiamo state="readonly" per far
 sì che l’utente possa solo selezionare i panini dall’elenco senza poter scrivere testo libero. 
Alla fine otteniamo un menu a tendina funzionante e collegato a una variabile, pronto a essere usato
 nella funzione che gestisce l’ordine del panino.

---------------------------------------------------------------------------------------------------
CODICE GUI:

Vengono create diverse label per mostrare informazioni nella GUI. La label titolo mostra il nome del gioco in alto con un font grande e in grassetto. 
La label soldi_label mostra i soldi attuali del giocatore mentre la label inv_label mostra l’inventario degli ingredienti. La label risultato_label serve a mostrare messaggi 
di feedback quando viene completato un ordine, ad esempio se è stato applicato uno sconto o se mancano ingredienti. La funzione aggiorna_gui() viene chiamata 
subito all’avvio della finestra per far sì che questi valori vengano visualizzati correttamente fin dall’inizio.

Per permettere all’utente di scegliere quale panino ordinare, viene creata una variabile Tkinter panino_var collegata a un menu a tendina realizzato con ttk.Combobox.
 Il menu mostra tutti i panini presenti nel file burgers.json e imposta automaticamente come selezione iniziale il primo panino. Questo consente all’utente di selezionare facilmente il panino senza dover scrivere nulla.

Il bottone “Fai ordine” viene creato con tk.Button. Quando l’utente clicca sul bottone, viene chiamata la funzione fai_ordine(). Il bottone ha dimensioni impostate e
 margini per apparire ordinato nella finestra. Grazie al thread interno della funzione fai_ordine, l’elaborazione dell’ordine avviene senza bloccare la GUI e gli 
ggiornamenti della finestra vengono gestiti in sicurezza tramite root.after.

Infine, il ciclo principale della finestra viene avviato solo se gui.py viene eseguito direttamente con root.mainloop(). Questo permette di importare il file gui.py in 
main.py senza far partire automaticamente la GUI. In main.py infatti la GUI viene eseguita nel thread principale, mentre la CLI viene eseguita in un thread separato 
per consentire l’interazione simultanea. Tutto questo garantisce che la finestra rimanga responsiva, che i dati siano aggiornati correttamente e che la concorrenza tra GUI e CLI non provochi errori sui soldi o sull’inventario.
