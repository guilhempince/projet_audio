# Contrôle audio - Raspberry Pi
Projet Type 2 - UPHF 2025

Guilhem Pince - Mathis Sellier

## Installation

### Création de l'environnement Python Virtuel
```
cd projet_audio/
python3 -m venv venv
source venv/bin/activate
pip install flask gunicorn
```

### Tester Gunicorn manuellement
```
venv/bin/gunicorn -w 2 -b 0.0.0.0:8000 wsgi:app
```

### Créer un service systemd
Créer un fichier :
```
sudo nano /etc/systemd/system/flaskaudio.service
```

Contenu :
```
[Unit]
Description=Flask Audio App with Gunicorn
After=network.target

[Service]
User=username
Group=username
WorkingDirectory=app_folder
Environment="PATH=app_folder/venv/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin"
ExecStart=app_folder/venv/bin/gunicorn -w 2 -b 0.0.0.0:8000 wsgi:app
Restart=always

[Install]
WantedBy=multi-user.target
```
**Attention** : Remplace **username** et **app_folder** par le nom d'utilisateur et le chemin du dossier d'installation de l'application.

Activer le service au démarrage
```
sudo systemctl daemon-reexec
sudo systemctl daemon-reload
sudo systemctl enable flaskaudio
sudo systemctl start flaskaudio
```

Vérification :
```
sudo systemctl status flaskaudio
```
