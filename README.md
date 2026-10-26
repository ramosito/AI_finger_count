# AI Finger Count

Détection du **nombre de doigts levés** via la webcam (OpenCV + MediaPipe). Le résultat est envoyé à un **Arduino** par liaison série : il allume autant de LEDs que de doigts levés et joue une note sur un buzzer.

```
Webcam -> OpenCV -> MediaPipe (21 points de la main) -> comptage des doigts
       -> port série (USB) -> Arduino -> LEDs + buzzer
```

---

## 1. Matériel

- 1 Arduino Uno (ou compatible) + câble USB **qui transmet les données** (certains câbles ne font que la charge)
- 1 breadboard
- 5 LEDs
- 5 résistances 220 Ω
- 1 buzzer **passif**
- Fils jumper
- 1 webcam (intégrée ou USB)

## 2. Branchement

| Composant | Broche Arduino |
|---|---|
| LED 1 | 2 |
| LED 2 | 3 |
| LED 3 | 4 |
| LED 4 | 5 |
| LED 5 | 6 |
| Buzzer (patte +) | 7 |
| Tous les − (LEDs et buzzer) | GND |

Pour **chaque LED** :

```
broche Arduino -> résistance 220 Ω -> patte LONGUE (+) -> patte COURTE (−) -> rail GND
```

Points importants :
- Une broche par LED : ne **pas** relier les 5 LEDs à la même broche.
- La résistance est obligatoire, sinon la LED et la broche risquent de griller.
- Ne rien brancher sur les broches 0 et 1 (réservées à l'USB).
- Toutes les pattes courtes et le − du buzzer vont sur le même rail GND, relié à un GND de l'Arduino.
- Le 5V n'est pas utilisé.

## 3. Code Arduino

1. Installer l'**Arduino IDE 2** : https://www.arduino.cc/en/software
2. Ouvrir `arduino.ino` (fourni dans ce dépôt).
3. *Outils > Carte* : choisir la bonne carte (ex. Arduino Uno).
4. *Outils > Port* : choisir le port de l'Arduino.
   - Windows : `COM3`, `COM4`...
   - Linux : `/dev/ttyACM0` ou `/dev/ttyUSB0`
5. Cliquer sur la flèche **Téléverser**.

**Test sans Python** : ouvrir le moniteur série (9600 bauds, fin de ligne "Nouvelle ligne"), taper `3` puis Entrée : 3 LEDs doivent s'allumer avec une note. `0` éteint tout.

⚠️ **Fermer le moniteur série** avant de lancer le script Python : un seul programme à la fois peut utiliser le port.

---

## 4. Installation Python

> Version de Python : **3.9 à 3.12** (MediaPipe ne supporte pas les versions plus récentes pour l'instant).
> Version de MediaPipe : **0.10.14** (les versions récentes n'ont plus `mp.solutions`).

### Windows

1. Installer Python 3.12 depuis https://www.python.org/downloads/ en cochant **"Add Python to PATH"**.
2. Ouvrir un terminal (PowerShell) dans le dossier du projet :
   ```powershell
   py -3.12 -m venv venv
   venv\Scripts\activate
   ```
   Si PowerShell bloque l'activation :
   ```powershell
   Set-ExecutionPolicy -Scope CurrentUser RemoteSigned
   ```
3. Installer les bibliothèques :
   ```powershell
   pip install opencv-python mediapipe==0.10.14 pyserial
   ```
4. Trouver le port : *Gestionnaire de périphériques > Ports (COM et LPT)*, ou dans l'IDE Arduino (*Outils > Port*). Exemple : `COM3`.

### Linux (Fedora)

1. Installer les paquets système :
   ```bash
   sudo dnf install python3.12 python3-pip mesa-libGL
   ```
2. Créer et activer l'environnement virtuel dans le dossier du projet :
   ```bash
   python3.12 -m venv venv
   source venv/bin/activate
   ```
3. Installer les bibliothèques :
   ```bash
   pip install opencv-python mediapipe==0.10.14 pyserial
   ```
4. Autoriser l'accès au port série (une seule fois) :
   ```bash
   sudo usermod -a -G dialout $USER
   ```
   Puis **se déconnecter et se reconnecter** (ou redémarrer).
5. Trouver le port :
   ```bash
   ls /dev/ttyACM* /dev/ttyUSB*
   ```
6. Vérifier la webcam :
   ```bash
   ls /dev/video*
   ```

### Linux (Ubuntu / Debian)

Même chose que Fedora, avec `apt` :
```bash
sudo apt update
sudo apt install python3 python3-pip python3-venv libgl1
```
Puis suivre les étapes 2 à 6 de Fedora.

### Arduino IDE sous Linux

- Fedora : `flatpak install flathub cc.arduino.IDE2` (si l'IDE ne voit pas le port : `flatpak override --user --device=all cc.arduino.IDE2`).
- Ubuntu / Debian : `sudo apt install arduino`, ou l'AppImage officielle.

---

## 5. Configuration du port série

Dans `main.py`, ligne 6, mettre le port de **ton** Arduino :

```python
PORT_SERIE = "COM3"            # Windows
PORT_SERIE = "/dev/ttyACM0"    # Linux
```

## 6. Lancer le programme

```bash
# Linux
source venv/bin/activate
python main.py
```

```powershell
# Windows
venv\Scripts\activate
python main.py
```

Une fenêtre s'ouvre avec l'image de la webcam. Montrer une main : le nombre de doigts s'affiche à l'écran, les LEDs s'allument en conséquence et le buzzer joue une note.

Appuyer sur **q** dans la fenêtre pour quitter.

---

## 7. Problèmes fréquents

| Erreur | Cause et solution |
|---|---|
| `could not open port 'COM3': No such file or directory` (sous Linux) | `COM3` est un nom Windows. Utiliser `/dev/ttyACM0`. |
| `No such file or directory: '/dev/ttyACM0'` | L'Arduino n'est pas détecté ou le port a changé. Vérifier le câble (données, pas seulement charge), refaire `ls /dev/ttyACM* /dev/ttyUSB*`. |
| `Permission denied: '/dev/ttyACM0'` | Faire le `usermod` de la section 4 puis se reconnecter. Dépannage immédiat : `sudo chmod 666 /dev/ttyACM0` (à refaire à chaque rebranchement). |
| `Device or resource busy` / `Access is denied` | Le moniteur série de l'IDE Arduino est ouvert. Le fermer. |
| `module 'mediapipe' has no attribute 'solutions'` | Mauvaise version de MediaPipe : `pip install mediapipe==0.10.14`. Vérifier aussi qu'aucun fichier `mediapipe.py` n'existe dans le projet. |
| `pip install mediapipe` échoue | Version de Python trop récente. Utiliser Python 3.12 ou moins. |
| `externally-managed-environment` (Linux) | Ne pas installer hors d'un venv. Activer le venv avant `pip install`. |
| La fenêtre ne s'ouvre pas (Linux, erreur Qt / xcb) | Lancer avec `QT_QPA_PLATFORM=xcb python main.py` (Wayland). |
| La webcam ne s'ouvre pas | Essayer `cv2.VideoCapture(1)` à la place de `0`. Sous Linux, vérifier `ls /dev/video*` et que l'utilisateur est dans le groupe `video`. |
| Le pouce est compté à l'envers | Dans `main.py`, inverser les `<` et `>` dans le bloc du pouce. |
| Les LEDs ne s'allument pas | LED à l'envers (retourner), résistance sur la mauvaise colonne, GND non relié au rail −, ou broche différente de celle du code. |
| Pas de son | Vérifier que le buzzer est **passif** et que son + est sur la broche 7. |

## 8. Figer les versions (bonne pratique)

Une fois que tout fonctionne :

```bash
pip freeze > requirements.txt
```

Quelqu'un qui clone le dépôt pourra alors tout installer avec :

```bash
pip install -r requirements.txt
```

Ajouter `venv/` au fichier `.gitignore` pour ne pas envoyer l'environnement virtuel sur GitHub.
