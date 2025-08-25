# 🎲 BOGAN - Board Game Analytics

Eine Flask-basierte Webanwendung zur Verwaltung und Analyse von Brettspielen und Spielrunden.

## ✨ Features

- 📊 **Spieler-Statistiken** - Verfolge Siege, Niederlagen und Spielverhalten
- 🎮 **Spiel-Management** - Verwalte Brettspiele mit BGG-Integration
- 📅 **Event-Verwaltung** - Organisiere Spieleabende
- 📱 **Mobile-optimiert** - Responsive Design für alle Geräte
- 🔐 **Admin-Interface** - Verwaltungssystem auf Webinterface

## 🚀 Installation

### Voraussetzungen

- Python 3.10+
- UV (Python Package Manager)

### Setup

```bash
# Repository klonen
git clone <repository-url>
cd bogan

# Dependencies installieren
uv sync

# virtual environment aktivieren
Windows: 
```bash
.venv\Scripts\activate
```

Linux

```bash
source .venv/bin/activate
```

### Datenbank erstellen

```bash
uv run ".\bogan\db\update_db.py"
```

### Anwendung starten

```bash
uv run flask run
```

## 🔧 Konfiguration

### Umgebungsvariablen

```bash
# .env Datei aus .env_template erstellen
FLASK_DEBUG=False
SECRET_KEY=your-secret-key
# aktuell wird eine lokale DB verwendet, dann sind nur diese Felder nötig
DB2USE='local'
DB_URL=sqlite:///instance/bogan_app.db
# servereitige DB bitte restl. Felder ausfüllen
```

### Admin-Benutzer erstellen

Für den Zugriff auf das Admin-Interface über ssh:

```bash
# Interaktives Script ausführen
uv run python create_admin.py

# Folge den Anweisungen:
# 1. Benutzername eingeben
# 2. Email eingeben (optional)
# 3. Passwort eingeben und bestätigen
```

Das Script bietet folgende Optionen:

- ✅ Neuen Admin-Benutzer erstellen
- ✅ Existierende Admin-Benutzer anzeigen
- ✅ Sichere Passworteingabe
- ✅ Benutzervalidierung

### Admin-Benutzer verwalten

```bash
# Alle Admin-Benutzer anzeigen
uv run python create_admin.py
# Dann Option 2 wählen
```

### Troubleshooting

#### Problem: "Flask app not found"

```bash
# Stelle sicher, dass du im richtigen Verzeichnis bist
cd /pfad/zu/deiner/bogan-app
```

#### Problem: "Database not found"

```bash
# Erstelle die Datenbank zuerst
uv run python -c "from bogan.db.models import db; db.create_all()"
```

## 📁 Projektstruktur

```tree
bogan/
├── bogan/                  # Hauptanwendung
│   ├── admin/             # Admin-Interface
│   ├── auth/              # Authentifizierung
│   ├── db/                # Datenbankmodelle
│   ├── main/              # Hauptrouten
│   ├── static/            # CSS, JS, Bilder
│   └── tools/             # Hilfswerkzeuge
├── instance/              # Datenbankdateien
├── logs/                  # Log-Dateien
├── tests/                 # Tests
├── create_admin.py        # Admin-Benutzer erstellen
└── wsgi.py               # WSGI Entry Point
```

## 🎯 Verwendung

### Web-Interface

1. **Hauptseite**: `http://localhost:3181/`
2. **Login**: `http://localhost:3181/auth/login`
3. **Admin-Panel**: `http://localhost:3181/admin/`

### Admin-Features

Das Admin-Interface bietet:

- 📊 **Dashboard** - Systemstatistiken und Übersicht
- 👥 **Benutzer-Verwaltung** - Benutzerrollen verwalten
- 📅 **Event-Management** - Events erstellen, bearbeiten, löschen
- 💾 **Datenbank-Übersicht** - Tabelleninhalt anzeigen

### Benutzer-Features

- 🔐 **Registrierung/Login** - Sichere Benutzeranmeldung
- 👤 **Profil-Management** - Persönliche Daten verwalten
- 🎲 **Spiele-Browser** - Brettspiele durchsuchen
- 📈 **Statistiken** - Persönliche Spielstatistiken

## 🛠️ Entwicklung

### Tests ausführen

- aktuell noch nicht implementiert

## 📦 Deployment

### Produktionssetup

1. **Umgebung vorbereiten**:

   ```bash
   # Produktions-Dependencies
   uv sync --only-prod

   # Umgebungsvariablen setzen
   export FLASK_ENV=production
   export SECRET_KEY=your-production-secret
   ```

2. **Admin-Benutzer erstellen**:

   ```bash
   uv run python create_admin.py
   ```

3. **Webserver starten**:

   ```bash
   # Mit Gunicorn
   uv run gunicorn -w 4 -b 0.0.0.0:<port> wsgi:app

   # Oder direkt mit Flask (nur für Entwicklung)
   uv run flask run --host=0.0.0.0 --port=8000
   ```

## 📄 Lizenz

Siehe [LICENSE](LICENSE) Datei für Details.

## 🆘 Support

Bei Problemen oder Fragen:

- 📝 Erstelle ein Issue im Repository
- 📧 Kontaktiere den Entwickler
