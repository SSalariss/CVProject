import cv2
import numpy as np

def draw_offside_line(image_path, players, attacking_team='blue'):
    """
    Disegna la linea del fuorigioco sull'immagine.

    Parametri:
        image_path (str): percorso dell'immagine.
        players (list): lista di dizionari con struttura:
            [{'team': 'blue', 'x': 120, 'y': 340}, {'team': 'red', 'x': 250, 'y': 330}, ...]
            dove (x, y) è il punto di riferimento del giocatore (es. centro o fondo del bounding box)
        attacking_team (str): squadra in attacco ('blue' o 'red')

    Output:
        image con la linea del fuorigioco tracciata
    """

    # Carica immagine
    img = cv2.imread(image_path)
    if img is None:
        raise ValueError("Immagine non trovata")

    height, width, _ = img.shape

    # Separiamo giocatori per squadra
    team_attack = [p for p in players if p['team'] == attacking_team]
    team_defend = [p for p in players if p['team'] != attacking_team]

    # Supponiamo che l’attacco vada da sinistra verso destra
    # (quindi i difensori “più arretrati” avranno x più piccolo)
    defending_x_positions = [p['x'] for p in team_defend]
    if not defending_x_positions:
        raise ValueError("Nessun difensore rilevato")

    last_defender_x = min(defending_x_positions)

    # Tracciamo la linea del fuorigioco (parallela alla linea di fondo)
    # Sarà una linea verticale che passa per x = last_defender_x
    cv2.line(img, (last_defender_x, 0), (last_defender_x, height), (0, 255, 255), 2)

    # Disegniamo anche i giocatori per visualizzare meglio
    for p in players:
        color = (255, 0, 0) if p['team'] == 'blue' else (0, 0, 255)
        cv2.circle(img, (p['x'], p['y']), 5, color, -1)

    # Mostra risultato
    cv2.imshow("Offside Line", img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    return img


# Esempio di utilizzo
players = [
    {'team': 'blue', 'x': 100, 'y': 320},
    {'team': 'blue', 'x': 250, 'y': 330},
    {'team': 'red',  'x': 140, 'y': 340},
    {'team': 'red',  'x': 220, 'y': 335},
]

draw_offside_line('campo.jpg', players, attacking_team='blue')
