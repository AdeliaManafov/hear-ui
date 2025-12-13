# Colima Setup & Configuration für HEAR-UI

## Quick Start

### 1. Colima installieren (falls noch nicht vorhanden)
```bash
brew install colima
```

### 2. Aktuelle Version prüfen
```bash
colima version
# Latest stable: 0.9.1 (Stand Dez 2025)

# Update auf neueste Version:
brew upgrade colima
```

### 3. Colima mit optimierter Config starten

**Option A: Neue Installation**
```bash
# Mit empfohlener Konfiguration starten
colima start --cpu 6 --memory 10 --disk 100 --vm-type vz --mount-type virtiofs
```

**Option B: Bestehende Colima-Instanz anpassen**
```bash
# Stoppen
colima stop

# Config bearbeiten (öffnet Editor)
colima start --edit

# Oder Config-Datei direkt kopieren:
cp .colima/colima-optimized.yaml ~/.colima/default/colima.yaml
colima start
```

### 4. Status prüfen
```bash
colima status
# Sollte zeigen:
# - runtime: docker
# - arch: aarch64 (Apple Silicon) oder x86_64 (Intel)
# - vmType: vz (macOS 13+) oder qemu
# - mountType: virtiofs (am schnellsten)
```

---

## Empfohlene Einstellungen für HEAR-UI

| Setting | Wert | Begründung |
|---------|------|------------|
| **CPU** | 6 | Backend + Frontend + DB + pgAdmin parallel |
| **Memory** | 10 GB | ML-Model (2-4 GB) + PostgreSQL + Services |
| **Disk** | 100 GB | Docker Images, Logs, DB-Data, Raum für Wachstum |
| **vmType** | vz | Schneller als qemu (macOS 13+, Apple Silicon) |
| **mountType** | virtiofs | Schnellstes Mounting für File-Watching |
| **mountInotify** | true | Hot-reload im Frontend funktioniert |

---

## Docker Compose mit Colima nutzen

### Services starten
```bash
cd hear-ui
docker compose up -d --build
```

### Services-Übersicht
| Service | Port | URL | Beschreibung |
|---------|------|-----|--------------|
| **Backend** | 8000 | http://localhost:8000 | FastAPI REST API |
| **Frontend** | 5173 | http://localhost:5173 | Vite Dev Server |
| **PostgreSQL** | 5434 | localhost:5434 | Datenbank |
| **pgAdmin** | 5050 | http://localhost:5050 | DB-Admin-GUI |

### pgAdmin Setup (erstmaliger Login)
```bash
# 1. Browser öffnen: http://localhost:5050
# 2. Login:
#    Email:    admin@hear-ui.local
#    Password: admin
#
# 3. Neue Server-Verbindung hinzufügen:
#    General Tab:
#      Name: HEAR-UI Local
#
#    Connection Tab:
#      Host name:   db
#      Port:        5432
#      Database:    app
#      Username:    postgres
#      Password:    change_me
#      (oder Werte aus .env-Datei)
```

---

## Wichtige Colima-Befehle

```bash
# Status anzeigen
colima status

# Stoppen
colima stop

# Neustarten
colima restart

# Colima komplett entfernen (Vorsicht: alle Container/Volumes weg!)
colima delete

# Logs anzeigen
colima logs

# SSH in VM
colima ssh

# Docker-Context prüfen
docker context ls
# Sollte "colima" als aktiven Context zeigen

# Docker-Info
docker info
```

---

## Troubleshooting

### Problem: `Cannot connect to the Docker daemon`
```bash
# Lösung 1: Docker-Context auf Colima setzen
docker context use colima

# Lösung 2: Colima neu starten
colima stop
colima start
```

### Problem: Ports bereits belegt (z.B. 5432, 8000)
```bash
# Lösung: Ports in .env anpassen
# Datei: .env
POSTGRES_HOST_PORT=5434  # statt 5432
# Backend/Frontend nutzen docker-compose.override.yml Defaults
```

### Problem: Langsame Performance / File-Watching funktioniert nicht
```bash
# Lösung: Auf vz + virtiofs wechseln (macOS 13+)
colima stop
colima delete  # Vorsicht: Daten gehen verloren!
colima start --vm-type vz --mount-type virtiofs --mount-inotify
```

### Problem: "Out of disk space"
```bash
# Lösung 1: Alte Images/Container aufräumen
docker system prune -a --volumes

# Lösung 2: Disk vergrößern (nur ERHÖHUNG möglich!)
colima stop
# Editiere ~/.colima/default/colima.yaml
# disk: 100  # von z.B. 60 auf 100
colima start
```

### Problem: Colima startet nicht nach macOS-Update
```bash
# Lösung: Colima + Lima updaten
brew upgrade colima lima
colima delete
colima start
```

---

## Colima vs. Docker Desktop

**Vorteile Colima:**
- ✅ Open Source & kostenlos
- ✅ Leichtgewichtig (weniger RAM/CPU)
- ✅ Schnelleres File-Mounting (virtiofs)
- ✅ Konfigurierbar (YAML)

**Nachteile Colima:**
- ❌ Keine GUI
- ❌ Manual Setup erforderlich
- ❌ Weniger "out-of-the-box" Extensions

---

## Update-Check (Dez 2025)

```bash
# Aktuelle Version prüfen
colima version
# Installiert: 0.9.1

# Neueste Version prüfen
brew info colima
# Latest stable: 0.9.1 (Stand Dez 2025)

# Update durchführen
brew upgrade colima

# Nach Update neu starten
colima stop
colima start
```

**Stand:** Colima 0.9.1 ist aktuell stabil und für HEAR-UI empfohlen.

---

## Weiterführende Links

- [Colima GitHub](https://github.com/abiosoft/colima)
- [Colima Docs](https://github.com/abiosoft/colima/blob/main/docs/README.md)
- [Lima Project](https://github.com/lima-vm/lima)
- [Docker Compose Docs](https://docs.docker.com/compose/)

---

## Nächste Schritte

1. ✅ Colima mit optimierter Config starten
2. ✅ `docker compose up -d` im Projekt ausführen
3. ✅ pgAdmin unter http://localhost:5050 öffnen
4. ✅ Backend-API testen: http://localhost:8000/docs
5. ✅ Frontend öffnen: http://localhost:5173
