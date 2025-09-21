import winsound
from typing import Optional
import os

class SoundManager():
    """
    Classe di supporto per la riproduzione di suoni

    La classe offre funzioni di supporto per riprodurre suoni
    in formato .wav.
    
    """

    @staticmethod
    def reproduce(sound_path: str, loop: Optional[bool] = False):
        """
        Riproduce il suono indicato dal path.

        Riproduce il suono indicato dal path se esiste ed ha
        estensione '.wav'.

        Parameters
        ------------
        sound_path : `str`
            Percorso del suono da riprodurre.

        loop : `bool` | `None`
            Valore booleano che indica se il suono deve andare in loop oppure no,
            il valore di default e' `False`.

        Raises
        ------------
        AttributeError 
            se il file non esiste o non ha estensione '.wav'
        """

        if not os.path.exists(sound_path) or not sound_path.endswith(".wav"):
            raise AttributeError(f"Il file {sound_path} non esiste o non e' supportato, assicurati che sia .wav")
        
        flags = winsound.SND_ASYNC
        if loop: flags |=  winsound.SND_LOOP
        winsound.PlaySound(sound_path, flags)

