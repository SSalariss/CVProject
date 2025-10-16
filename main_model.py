import os
import cv2
from ultralytics import YOLO
from color_clustering.clustering import team_classification_complete
from analysis.attack_prediction import predictTeamAttacking
from visualization.visualize import draw_boxes, save_image
from offside.homography_calculator import calculateOptimHomography, load_homography, save_homography
from offside.offside_detection import drawOffside

import os
from io import BufferedReader
from numpy import frombuffer, uint8



class ModelManager: 

    _image_path: str
    _image: cv2.typing.MatLike

    _player_classification: dict
    _color_classification: dict
    _percent_team1: float
    _percent_team2: float

    def step_select_image(self, buffered_image: BufferedReader):
        """
        Questa funzione prende il percorso dell'immagine selezionata dalla GUI.
        Ritorna l'immagine caricata o None se impossibile caricarla.
        """
        image_data = buffered_image.read()
        np_arr = frombuffer(image_data, uint8)
        image = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)
        if image is None:
            print("Immagine non trovata.")
            
        self._image_path = buffered_image.name
        self._image = image
        self._results_dir = 'results'


    def step_attack_prediction(self):
        """
        Esegue la detection e la classificazione dei giocatori,
        calcola le percentuali di attacco e ritorna la classificazione
        di giocatori, colori e le percentuali di attacco.
        """
        model_path = "model/teamClassification/weights/best.pt"
        model = YOLO(model_path)
        results = model(self._image_path)
        boxes, classes = results[0].boxes.xyxy.tolist(), results[0].boxes.cls.tolist()

        self._players_classification, self._color_classification = team_classification_complete(boxes, classes, self._image)
        self._percent_team_1, self._percent_team_2 = predictTeamAttacking(self._players_classification, self._image)
                
        results = YOLO("model/teamClassification/weights/best.pt")(self._image_path)[0]
        boxes, classes = results.boxes.xyxy.tolist(), results.boxes.cls.tolist()
        annotated_image = draw_boxes(self._image, boxes, classes, self._players_classification)
        save_image(annotated_image, os.path.join(self._results_dir, 'final_annotated_result.jpg'))

        return os.path.join(self._results_dir, 'final_annotated_result.jpg')

    def step_offside_detection(self, attacking_team):
        """
        Calcola o carica l'omografia, rileva il fuorigioco e salva l'immagine annotata.
        Ritorna il numero di giocatori in fuorigioco.
        """
        homography_path = os.path.join(self._results_dir, 'homography.pt')
        if os.path.exists(homography_path):
            homography = load_homography(homography_path)
        else:
            homography = calculateOptimHomography(self._image_path)
        save_homography(homography, homography_path)

        if not os.path.exists(self._results_dir):
            os.makedirs(self._results_dir)

        if attacking_team == "Team A":
            attacker_boxes = self._players_classification.get(0, [])
            defender_boxes = self._players_classification.get(1, [])
            colors = {'Team A': self._color_classification.get(0, [255,0,0]), 'Team B': self._color_classification.get(1, [0,0,255])}
        else:
            attacker_boxes = self._players_classification.get(1, [])
            defender_boxes = self._players_classification.get(0, [])
            colors = {'Team B': self._color_classification.get(1, [255,0,0]), 'Team A': self._color_classification.get(0, [0,0,255])}

        goalkeeper_boxes = self._players_classification.get('goalkeeper', [])

        drawOffside(self._image_path, attacking_team, colors, homography, defender_boxes, attacker_boxes, goalkeeper_boxes)

        # Salva immagine annotata
        return os.path.join(self._results_dir, 'offside_3D.jpg')
