from flask import Flask, render_template, send_file, request, redirect, flash
import subprocess
import os
import re

app = Flask(__name__)
app.secret_key = 'un-secret-tres-long-et-complexe'

AUDIO_FILE = "static/fichier.wav"
RINGTONE = "static/ringtone.wav"

def get_audio_cards():
    try:
        result = subprocess.run(["arecord", "-l"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, check=True)
        cards = []
        pattern = re.compile(r"card (\d+): ([^\s]+) \[([^\]]+)\], device (\d+): ([^\[]+)\[([^\]]+)\]")
        for match in pattern.finditer(result.stdout):
            card_num = match.group(1)
            device_num = match.group(4)
            name = f"{match.group(3)} ({match.group(2)})"
            card_id = f"plughw:{card_num},{device_num}"
            cards.append((card_id, name))
        return cards
    except subprocess.CalledProcessError:
        return []

@app.route('/')
def index():
    cards = get_audio_cards()
    return render_template('index.html', cards=cards)

@app.route('/enregistrer', methods=['POST'])
def enregistrer():
    card = request.form.get('carte', 'plughw:1,0')
    duree = request.form.get('duree', '5')
    if not duree.isdigit() or int(duree) <= 0:
        flash("Durée invalide. Entrez un nombre supérieur à 0.", "warning")
        return redirect('/')

    try:
        duree = int(duree)
        if os.path.exists(AUDIO_FILE):
            os.remove(AUDIO_FILE)
        cmd = ["arecord", "-D", card, "-f", "S24_LE", "-r", "192000", "-c", "1", "-d", str(duree), AUDIO_FILE]
        subprocess.run(cmd, check=True)
        flash(f"Enregistrement de {duree} sec terminé avec succès.", "success")
    except subprocess.CalledProcessError:
        flash("Échec de l'enregistrement. Vérifie la carte son sélectionnée.", "danger")
    return redirect('/')

@app.route('/lire', methods=['POST'])
def lire():
    card = request.form.get('carte', 'plughw:1,0')
    if not os.path.exists(AUDIO_FILE):
        flash("Aucun fichier à lire.", "warning")
        return redirect('/')
    try:
        subprocess.run(["aplay", "-D", card, AUDIO_FILE], check=True)
        flash("Lecture terminée.", "info")
    except subprocess.CalledProcessError:
        flash("Erreur lors de la lecture. Vérifie la carte son.", "danger")
    return redirect('/')

@app.route('/ringtone', methods=['POST'])
def ringtone():
    card = request.form.get('carte', 'plughw:1,0')
    if not os.path.exists(RINGTONE):
        flash("Aucun fichier à lire.", "warning")
        return redirect('/')
    try:
        subprocess.run(["aplay", "-D", card, RINGTONE], check=True)
        flash("Lecture terminée.", "info")
    except subprocess.CalledProcessError:
        flash("Erreur lors de la lecture. Vérifie la carte son.", "danger")
    return redirect('/')

@app.route('/telecharger')
def telecharger():
    if not os.path.exists(AUDIO_FILE):
        flash("Aucun fichier à télécharger.", "warning")
        return redirect('/')
    return send_file(AUDIO_FILE, as_attachment=True)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)

