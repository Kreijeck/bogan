# 🎲 BOGAN - Board Game Analytics

Eine Flask-basierte Webanwendung zur Verwaltung und Analyse von Brettspielen und Spielrunden.

## ✨ Features

- 📊 **Spieler-Statistiken** - Verfolge Siege, Niederlagen und Spielverhalten
- 🎮 **Spiel-Management** - Verwalte Brettspiele mit BGG-Integration
- 📅 **Event-Verwaltung** - Organisiere Spieleabende und Turniere
- 📱 **Mobile-optimiert** - Responsive Design für alle Geräte
- 🔐 **Admin-Interface** - Umfassendes Verwaltungssystem

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

# Datenbank erstellen
uv run python -c "from bogan.db.models import db; db.create_all()"

# Anwendung starten
uv run flask run
```

## 🔧 Konfiguration

### Umgebungsvariablen

```bash
# .env Datei erstellen
FLASK_ENV=development
FLASK_DEBUG=True
SECRET_KEY=your-secret-key
DATABASE_URL=sqlite:///instance/bogan_app.db
```

### Admin-Benutzer erstellen

Für den Zugriff auf das Admin-Interface:

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

```
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

1. **Hauptseite**: `http://localhost:5000/`
2. **Login**: `http://localhost:5000/auth/login`
3. **Admin-Panel**: `http://localhost:5000/admin/`

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

```bash
# Alle Tests
uv run pytest

# Spezifische Tests
uv run pytest tests/test_admin.py
```

### Code-Qualität

```bash
# Linting
uv run flake8 bogan/

# Formatierung
uv run black bogan/
```

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
   uv run gunicorn -w 4 -b 0.0.0.0:8000 wsgi:app

   # Oder direkt mit Flask (nur für Entwicklung)
   uv run flask run --host=0.0.0.0 --port=8000
   ```

### Docker (optional)

```dockerfile
FROM python:3.10-slim

WORKDIR /app
COPY . .

RUN pip install uv
RUN uv sync --only-prod

EXPOSE 8000
CMD ["uv", "run", "gunicorn", "-w", "4", "-b", "0.0.0.0:8000", "wsgi:app"]
```

## 🤝 Beitragen

1. Fork das Repository
2. Erstelle einen Feature-Branch
3. Committe deine Änderungen
4. Erstelle einen Pull Request

## 📄 Lizenz

Siehe [LICENSE](LICENSE) Datei für Details.

## 🆘 Support

Bei Problemen oder Fragen:

- 📝 Erstelle ein Issue im Repository
- 📧 Kontaktiere den Entwickler

---

Erstellt mit ❤️ für die Brettspiel-Community
