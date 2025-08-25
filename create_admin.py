#!/usr/bin/env python3
"""
Script zum Erstellen eines Admin-Benutzers für das Produktivsystem
Verwendung: python create_admin.py
"""

import getpass
from sqlalchemy.orm import Session
from werkzeug.security import generate_password_hash

# Import der App-Module
from bogan.db.models import User
from bogan.utils import get_db_engine

def create_admin_user():
    """Erstellt einen neuen Admin-Benutzer interaktiv"""
    
    print("=" * 50)
    print("BOGAN - Admin-Benutzer erstellen")
    print("=" * 50)
    
    # Benutzername eingeben
    while True:
        username = input("Admin-Benutzername: ").strip()
        if username:
            break
        print("❌ Benutzername darf nicht leer sein!")
    
    # Email eingeben (optional)
    email = input("Email (optional): ").strip()
    if not email:
        email = None
    
    # Passwort eingeben (sicher ohne Echo)
    while True:
        password = getpass.getpass("Passwort: ")
        if len(password) < 6:
            print("❌ Passwort muss mindestens 6 Zeichen lang sein!")
            continue
        
        password_confirm = getpass.getpass("Passwort bestätigen: ")
        if password != password_confirm:
            print("❌ Passwörter stimmen nicht überein!")
            continue
        break
    
    # Datenbank-Verbindung
    try:
        with Session(get_db_engine()) as session:
            # Prüfen ob Benutzer bereits existiert
            existing_user = session.query(User).filter(User.name == username).first()
            if existing_user:
                print(f"❌ Benutzer '{username}' existiert bereits!")
                return False
            
            # Neuen Admin-Benutzer erstellen
            admin_user = User(
                name=username,
                email=email,
                password=generate_password_hash(password),
                role='admin'
            )
            
            session.add(admin_user)
            session.commit()
            
            print(f"✅ Admin-Benutzer '{username}' erfolgreich erstellt!")
            print(f"   - Benutzername: {username}")
            print(f"   - Email: {email or 'Keine'}")
            print("   - Rolle: admin")
            print(f"   - ID: {admin_user.id}")
            
            return True
            
    except Exception as e:
        print(f"❌ Fehler beim Erstellen des Admin-Benutzers: {e}")
        return False

def list_admins():
    """Zeigt alle existierenden Admin-Benutzer an"""
    try:
        with Session(get_db_engine()) as session:
            admins = session.query(User).filter(User.role == 'admin').all()
            
            if not admins:
                print("ℹ️ Keine Admin-Benutzer gefunden.")
                return
            
            print("\n📋 Existierende Admin-Benutzer:")
            print("-" * 40)
            for admin in admins:
                print(f"   ID: {admin.id} | Name: {admin.name} | Email: {admin.email or 'Keine'}")
                
    except Exception as e:
        print(f"❌ Fehler beim Abrufen der Admin-Benutzer: {e}")

if __name__ == "__main__":
    print("Was möchten Sie tun?")
    print("1. Neuen Admin-Benutzer erstellen")
    print("2. Existierende Admin-Benutzer anzeigen")
    print("3. Beenden")
    
    while True:
        choice = input("\nWählen Sie eine Option (1-3): ").strip()
        
        if choice == "1":
            create_admin_user()
            break
        elif choice == "2":
            list_admins()
            break
        elif choice == "3":
            print("👋 Auf Wiedersehen!")
            break
        else:
            print("❌ Ungültige Auswahl! Bitte 1, 2 oder 3 eingeben.")
