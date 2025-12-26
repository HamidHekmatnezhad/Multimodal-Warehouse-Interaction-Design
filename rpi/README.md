# Multimodale Interaktion im Lagerhaus (Warehouse Interaction Design)

Dieses Projekt umfasst die Entwicklung eines interaktiven Systems zur Simulation eines Logistik-Sortierprozesses. Es verbindet physische Hardware-Eingaben über einen **Raspberry Pi** mit einer virtuellen Umgebung in **Unity 3D** mittels MQTT-Kommunikation.

## 1. Projektübersicht (Overview)
Das System simuliert eine Kontrollstation in einem Warenlager, an der Pakete auf ihre Korrektheit überprüft werden. Der Benutzer interagiert direkt mit der Hardware, um den Fluss der Pakete in der digitalen Simulation zu steuern.

**Kernkonzept des Szenarios:**
* **Manueller Scan-Vorgang:** Ein Paket wird am Scanner (Lichtsensor) vorbeigeführt, um den Identifikationsprozess auszulösen.
* **Status-Validierung:** Das System prüft basierend auf der Logik (z. B. Paket-Daten oder Bestimmungsort), ob das Paket korrekt ist oder einen Fehler aufweist.
* **Interaktive Sortierung:**
  *  **Korrektes Paket:** Das Paket wird akzeptiert und setzt seinen Weg auf der Hauptschiene (Rail) fort.
  * **Fehlerhaftes Paket:** Erkennt das System einen Fehler, wird dies dem Benutzer signalisiert. Der Benutzer muss daraufhin manuell einen physischen 
  * **Hardware-Button** drücken, um das Paket vom Förderband in eine Aussortierbox (Drop-box) zu verschieben.

Dieses System demonstriert die nahtlose Integration von Sensorik, Benutzerinteraktion und Echtzeit-Visualisierung in einem industriellen Kontext.


## 2. Hardware-Komponenten und Funktionslogik

In diesem Abschnitt wird die detaillierte Konfiguration der Hardware-Module am Raspberry Pi sowie deren Interaktion mit der Unity-Simulation erläutert.

### 2.1 LCD-Display Konfiguration (16x2)
Das LCD dient als zentrale Informationsschnittstelle für den Benutzer. Es zeigt den aktuellen Systemstatus in folgendem Format an:

**Display-Template:**
- **Zeile 1:** `dist: XXX |SV/TH`
- **Zeile 2:** `point: XX |YY/ZZ`

**Erklärung der Werte:**
* **dist (Distance):** Zeigt die vom Ultraschallsensor gemessene Distanz des Pakets an.
* **point (Score):** Der aktuelle Punktestand des Spielers, der in Echtzeit von Unity empfangen wird.
* **SV (Sensor Value):** Der aktuelle Wert des Lichtsensors (dividiert durch 10 zur Optimierung der Anzeigepräzision).
* **TH (Threshold):** Der eingestellte Schwellenwert. Fällt der **SV** unter oder auf den **TH**, wird dies als erfolgreicher Scan-Vorgang interpretiert.

---

### 2.2 Detaillierte Komponentenbeschreibung

#### Sensoren (Input):
* **Ultraschallsensor:** Fungiert als primärer Controller für die Bewegung in Unity. Die gemessene Distanz bestimmt die Position (Annäherung oder Entfernung) des Pakets innerhalb der 3D-Simulation.
* **Lichtsensor (Barcodescanner-Simulation):** Simuliert das Einlesen eines Barcodes. Wenn sich ein Paket dem Sensor nähert, sinkt die Lichtintensität. Sobald der Wert den Schwellenwert erreicht, wird der Scan ausgelöst.
* **Drehpotentiometer:** Dient zur Kalibrierung der Scanner-Empfindlichkeit (Bereich: 40 bis 550). Dies ermöglicht es dem Benutzer, das System an unterschiedliche Lichtverhältnisse im Raum anzupassen.
* **Taster (Button):** Löst den "Drop"-Befehl aus. Dieser Taster hat Vorrang vor der automatischen Logik: Sobald er gedrückt wird, wird das aktuelle Paket aussortiert (gedroppt), unabhängig davon, ob es korrekt oder fehlerhaft war.

#### Aktoren (Output & Feedback):
* **Blaue LED:** Blinkt (Peak) zusammen mit dem Buzzer auf, sobald ein Paket erfolgreich gescannt wurde, um den Scan-Vorgang zu bestätigen.
* **Grüne LED:** Leuchtet dauerhaft, sobald in Unity ein Paket existiert (`packet_exist`), das zum Scanner bewegt werden kann.
* **Rote LED:** Blinkt in zwei Szenarien:
    1. Wenn das System ein fehlerhaftes Paket erkennt.
    2. Wenn der Benutzer den Button drückt, um ein Paket auszusortieren (Drop-Vorgang).
* **Buzzer (Akustische Signale):**
    * **1 kurzer Beep:** Erfolgreicher Scan eines korrekten Pakets.
    * **2 Beeps:** Bestätigung des manuellen Aussortierens (Drop-Befehl).
    * **3 Beeps:** Warnsignal bei Erkennung eines fehlerhaften Pakets.

---

### 2.3 Datenfluss und MQTT-Kommunikation
Die Synchronisation zwischen Hardware und Software erfolgt über eine robuste MQTT-Architektur:

**Vom Raspberry Pi gesendet (Sending/Publishing):**
1.  **Ultraschall-Daten:** Kontinuierliche Übertragung der Distanzwerte zur Steuerung der Paketbewegung in Unity.
2.  **Scan-Trigger:** Übermittlung des Lichtsensors-Status, sobald der Schwellenwert erreicht ist.
3.  **Drop-Befehl:** Sofortige Übermittlung bei Betätigung des Tasters.

**Vom Raspberry Pi empfangen (Listening/Subscribing):**
1.  **Point-Score:** Aktualisierung des Punktestands auf dem LCD.
2.  **Packet Exist:** Steuerung der grünen LED basierend auf der Paketpräsenz in Unity.
3.  **Packet Corrected:** Information über die Korrektheit des Pakets zur Ansteuerung der roten/blauen LEDs und des Buzzers.
   

## 3. Software-Design und Architektur

Das Softwaresystem wurde nach dem Prinzip der Modularität und Thread-Sicherheit entwickelt, um eine zuverlässige Kommunikation zwischen Hardware und Simulation zu gewährleisten.

### 3.1 Modularer Aufbau (HAL)
Das Projekt implementiert einen **Hardware Abstraction Layer (HAL)**. Jeder Sensor und Aktor wird durch ein dediziertes Modul im Ordner `drivers/` gesteuert (z. B. `lcdHA.py`, `ledsHA.py`).
* **Vorteil:** Die physischen Details der Hardware sind von der Hauptlogik (`main.py`) entkoppelt, was die Wartbarkeit und Testbarkeit des Codes erhöht.

### 3.2 Thread-Sicherheit und Concurrency
Da das System zeitkritische Sensordaten verarbeitet und gleichzeitig visuelles Feedback gibt, wurden folgende Mechanismen implementiert:
* **I2C-Bus-Synchronisation:** Da mehrere Geräte (LCD, Sensoren) den I2C-Bus teilen, verhindert ein `threading.Lock()` Datenkollisionen und den berüchtigten `OSError 121`.
* **Asynchrones Feedback:** Akustische und visuelle Signale (Buzzer-Beeps und LED-Blinken) werden in separaten Threads (`threading.Thread`) gestartet. Dies stellt sicher, dass die Hauptschleife nicht blockiert wird und der Ultraschallsensor weiterhin Daten in Echtzeit an Unity senden kann.

### 3.3 Konfigurationsgesteuerte Logik
Durch die Verwendung der `data.json` ist das System vollständig konfigurierbar.
* Alle MQTT-Topics, Zugangsdaten و Logik-Signale (`SIGNAL_ON/OFF`) sind zentralisiert.
* Dies ermöglicht eine schnelle Anpassung an verschiedene Netzwerkumgebungen (z. B. Wechsel der Broker-IP), ohne den Quellcode modifizieren zu müssen.
* 

## 4. Installation und Inbetriebnahme (Raspberry Pi)

Dieser Abschnitt beschreibt die notwendigen Schritte, um die Hardware-Station und die Software-Umgebung auf dem Raspberry Pi vorzubereiten.

### 4.1 Installation des MQTT-Brokers (Mosquitto)
Das System kommuniziert über den Mosquitto-Broker. Installieren Sie diesen direkt auf dem Raspberry Pi:

1. **Mosquitto installieren:**
   ```bash
   sudo apt update
   sudo apt install mosquitto mosquitto-clients -y
    ```

2. **Status überprüfen:**
    Stellen Sie sicher, dass der Broker aktiv ist:
    ```bash
    sudo systemctl status mosquitto
    ```


### 4.2 Python-Bibliotheken

Für die Ausführung des Skripts wird die MQTT-Bibliothek für Python benötigt. Installieren Sie diese mit dem folgenden Befehl:

```bash
pip3 install paho-mqtt
```

### 4.3 Konfiguration der Zugangsdaten

Bevor Sie das Programm starten, müssen die Verbindungsparameter in der Datei `rpi/data.json` angepasst werden.

Öffnen Sie die Datei und tragen Sie die IP-Adresse Ihres PCs (auf dem Unity läuft) oder des Raspberry Pi als `broker_address` ein:

```json
{
    "username": "IHRE_USERNAME",
    "password": "IHRE_PASSWORT",
    "broker_address": "IHRE_IP_ADRESSE"
}
```

### 4.4 Das System starten

Sobald der Broker läuft und die Bibliotheken installiert sind, kann das Hauptprogramm gestartet werden:

1. Navigieren Sie in das Projektverzeichnis.
2. Führen Sie den folgenden Befehl aus:
```bash
python3 rpi/main.py
```

## 5. MQTT-Kommunikationsschnittstelle

Die Kommunikation zwischen dem Raspberry Pi und Unity basiert auf dem MQTT-Protokoll. Alle Verbindungsparameter und Topic-Definitionen sind zentral in der Datei `data.json` hinterlegt, um eine einfache Konfiguration zu ermöglichen.

### 5.1 Verbindungsparameter
Für den Aufbau der Verbindung zum MQTT-Broker werden folgende Daten aus der Konfigurationsdatei verwendet:
* **Broker-Adresse:** `localhost` (die entsprechende IP-Adresse des Servers)
* **Port:** `1883`
* **Benutzername:** `HA_warehouse`
* **Passwort:** `qweasd`
* **Keepalive:** 60 Sekunden

### 5.2 Signal-Definitionen
Zur Vermeidung von Inkonsistenzen werden binäre Zustände (An/Aus) über vordefinierte Signale gesteuert:
* **SIGNAL_ON:** `"1"`
* **SIGNAL_OFF:** `"0"`

### 5.3 MQTT-Topics und Datenfluss
Die folgende Tabelle gibt eine Übersicht über die verwendeten Kommunikationswege und deren Priorisierung (QoS):

| Funktion | Topic-Pfad | QoS | Richtung | Beschreibung |
| :--- | :--- | :--- | :--- | :--- |
| **Packet Exist** | `warehouse/packet/exist` | 2 | Unity -> RPi | Status, ob ein Paket in der Simulation vorhanden ist. |
| **Corrected** | `warehouse/packet/corrected` | 2 | Unity -> RPi | Info von Unity, ob das aktuelle Paket korrekt ist. |
| **Distance** | `warehouse/sensor/distance` | 0 | RPi -> Unity | Kontinuierliche Übertragung der Distanzwerte vom Ultraschallsensor. |
| **Light Sensor** | `warehouse/sensor/light` | 2 | RPi -> Unity | Trigger-Signal bei Erkennung eines Scan-Vorgangs. |
| **Point/Score** | `warehouse/packet/point` | 0 | Unity -> RPi | Aktueller Punktestand zur Anzeige auf dem LCD-Display. |
| **Drop Command** | `warehouse/packet/drop` | 2 | RPi -> Unity | Befehl zum Aussortieren des Pakets bei Button-Druck. |


## 6. Durchführung und Test (Inbetriebnahme)

Nach der Installation der Abhängigkeiten folgen Sie dieser Schritt-für-Schritt-Anleitung, um das Gesamtsystem in Betrieb zu nehmen und zu testen.

### 6.1 Hardware-Anschlussplan
Stellen Sie sicher, dass die GrovePi-Module an den folgenden Ports angeschlossen sind, wie in den Treibern definiert:

| Modul | Port-Typ | Pin / Port | Datei-Referenz |
| :--- | :--- | :--- | :--- |
| **Ultraschallsensor** | Digital | D3 | `ultraSonicHA.py` |
| **Buzzer** | Digital | D4 | `buzzerHA.py` |
| **LED Blau** | Digital | D5 | `ledsHA.py` |
| **Button (Taster)** | Digital | D6 | `btnHA.py` |
| **LED Rot** | Digital | D7 | `ledsHA.py` |
| **LED Grün** | Digital | D8 | `ledsHA.py` |
| **Lichtsensor** | Analog | A2 | `lightSensorHA.py` |
| **Potentiometer** | Analog | A8 (Pin 8) | `potentiometerHA.py` |
| **LCD Display** | I2C | I2C | `lcdHA.py` |

### 6.2 Start-Reihenfolge
Um eine stabile Kommunikation zwischen Raspberry Pi, Broker und Unity zu gewährleisten, halten Sie die folgende Reihenfolge ein:

1.  **MQTT Broker starten:** Der Mosquitto-Dienst muss aktiv sein.
2.  **Konfiguration prüfen:** Stellen Sie sicher, dass die `broker_address` in der `data.json` der IP-Adresse Ihres PCs entspricht.
3.  **Python-Skript ausführen:**
    ```bash
    python3 rpi/main.py
    ```
    *Nach dem Start sollten Sie die Meldung "Connected with result code 0" im Terminal sehen.*
4.  **Unity-Simulation starten:** Starten Sie die Warehouse-Szene in Unity. Sobald die Verbindung steht, leuchtet die **grüne LED**, wenn ein Paket in der Simulation existiert (`packet_exist = "1"`).

### 6.3 Funktionstest und Validierung
Überprüfen Sie die korrekte Funktion anhand der folgenden Indikatoren:

* **LCD-Anzeige:** Das Display muss das vordefinierte Template zeigen: `dist: XXX |SV/TH` in der ersten Zeile und `point: XX |YY/ZZ` in der zweiten Zeile.
* **Sensor-Kalibrierung:** Drehen Sie am Potentiometer. Der Wert `TH` (Threshold) auf dem LCD muss sich zwischen 04 und 55 ändern.
* **Manueller Test (Mosquitto CLI):**
    Sie können den Status der Simulation manuell testen, indem Sie Befehle über das Terminal senden:
    ```bash
    # Simuliert ein existierendes Paket (Grüne LED an)
    mosquitto_pub -u "HA_warehouse" -P "qweasd" -t "warehouse/packet/exist" -m "1"
    ```


## 7. Unity-Integration und Konfiguration

In diesem Abschnitt wird die Schnittstelle zur Unity-Simulation sowie die notwendigen Netzwerkeinstellungen beschrieben. Damit die Kommunikation zwischen dem Raspberry Pi und Unity reibungslos funktioniert, ist die korrekte IP-Konfiguration entscheidend.

### 7.1 Wichtiger Hinweis zur Broker-Adresse
Die Variable `broker_address` in der Datei `data.json` auf dem Raspberry Pi muss zwingend auf die **IP-Adresse des Systems** zeigen, auf dem der MQTT-Broker (Mosquitto) läuft. 

* **PC als Host:** Wenn Unity und der Mosquitto-Broker auf demselben Computer ausgeführt werden, muss in der `data.json` die **lokale Netzwerk-IP dieses PCs** (z. B. `192.168.178.20`) eingetragen werden. 

### 7.2 Unity-Anbindung (Partner-Bereich)
> **Hinweis für den Unity-Partner:** Bitte ergänzen Sie hier die Details zur technischen Umsetzung in Unity.

Folgende Aufgaben sind für die Unity-Seite vorgesehen:
1.  **MQTT-Framework:** Implementierung eines Clients (z. B. `MQTT4Unity` oder `M2MQTT`), um Nachrichten zu senden und zu empfangen.
2.  **Skript-Synchronisation:**
    * **Subscribing:** Unity muss auf die Topics `warehouse/sensor/distance` (Positionssteuerung) und `warehouse/packet/drop` (Aussortier-Event) reagieren.
    * **Publishing:** Unity sendet Status-Updates an `warehouse/packet/exist` (LED Grün) und `warehouse/packet/corrected` (Scan-Feedback).
3.  **Signal-Verarbeitung:** Die empfangenen Payloads (`1` für ON und `0` für OFF) müssen in der Unity-Logik als Trigger oder Status-Flags verarbeitet werden.

### 7.3 Verbindungstest
Vor dem Start der Simulation sollte die Erreichbarkeit des Ziel-PCs vom Raspberry Pi aus mittels `ping` geprüft werden. Stellen Sie sicher, dass keine Firewall den Port `1883` blockiert.



## 8. Fehlerbehandlung und technische Hinweise

In diesem Abschnitt werden Sicherheitsmechanismen und Lösungen für häufig auftretende Probleme beschrieben.

### 8.1 Thread-Sicherheit (I2C-Lock)

Da mehrere Sensoren und Aktoren gleichzeitig über den I2C-Bus kommunizieren (z. B. LCD und Sensoren), wurde ein `threading.Lock()` implementiert.

* **Zweck:** Dies verhindert den Fehler `OSError 121` (Remote I/O error), der auftritt, wenn zwei Prozesse gleichzeitig auf den I2C-Bus zugreifen.
* **Lösung:** Alle hardwarenahen Funktionen im `main.py` sind durch den `i2c_lock` geschützt.

### 8.2 Fehlertoleranz beim Potentiometer

Die Funktion `watch_potentiometer()` wurde so programmiert, dass sie robust gegenüber Hardware-Fluktuationen ist:

* Falls der Sensor einen ungültigen Wert oder `None` zurückgibt (z. B. bei kurzzeitigen Verbindungsproblemen), ignoriert das System den Fehler und behält den letzten gültigen Schwellenwert bei.
* Dies verhindert einen Absturz des Programms durch `TypeErrors`.

### 8.3 Häufige Probleme (FAQ)

| Problem | Mögliche Ursache | Lösung |
| --- | --- | --- |
| **Connection Refused** | Der Mosquitto-Broker läuft nicht. | Prüfen Sie den Status mit `sudo systemctl status mosquitto`. |
| **IOError in Sensors** | Ein Kabel hat sich gelöst. | Überprüfen Sie die Steckverbindungen am GrovePi gemäß dem Anschlussplan in Sektion 5.1. |
| **LCD zeigt nichts an** | I2C ist nicht aktiviert. | Aktivieren Sie I2C über `sudo raspi-config` und starten Sie den Pi neu. |
| **Keine Reaktion in Unity** | Falsche IP-Adresse. | Stellen Sie sicher, dass die `broker_address` in der `data.json` der IP des Host-PCs entspricht. |

### 8.4 Performance-Optimierung

Um die CPU-Last auf dem Raspberry Pi zu minimieren und den I2C-Bus zu entlasten, wird das LCD-Display nicht in jedem Durchlauf der Hauptschleife aktualisiert. Die Aktualisierung erfolgt ereignisbasiert (bei Statusänderung) oder in festen Intervallen (`lcd_rate_show`).
