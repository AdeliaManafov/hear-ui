# HEAR-UI – Mögliche Fragen von Klinikern & Antworten

Vorbereitung für die Präsentation. Antworten sind Vorschläge – bitte an das
eigene Datenmaterial und die Zentrumspolitik anpassen.

---

## A. Modellgüte & Zuverlässigkeit

**F: Wie genau ist das Modell? Kann ich ihm vertrauen?**

> Das Modell erreicht auf unserem Validierungsdatensatz eine AUC von [Wert einfügen].
> Das bedeutet, es hebt Patienten mit guten CI-Ergebnissen zuverlässiger hervor
> als eine rein zufällige Auswahl. Die Modellkarte zeigt Sensitivität, Spezifität
> und weitere Metriken transparent.
> Dennoch ist es ein Entscheidungs*unterstützungs*tool – die endgültige Entscheidung
> liegt immer beim Kliniker.

**F: Was ist, wenn das Modell falsch liegt?**

> Kein prädiktives Modell hat 100 % Treffsicherheit. Deshalb zeigt das System
> neben dem Wahrscheinlichkeitswert auch die SHAP-Erklärung: Der Kliniker kann
> sofort sehen, welche Faktoren ausschlaggebend waren, und beurteilen, ob das
> mit der klinischen Realität übereinstimmt. Das Modell ist ein Hilfsmittel,
> kein Ersatz für das ärztliche Urteil.

**F: Auf wie vielen Patienten wurde das Modell trainiert?**

> [Zahl einfügen – z. B. „N = 320 CI-Patienten aus unserem Zentrum".]
> Die Trainingsdaten stammen ausschließlich aus unserer eigenen Klinik,
> was für die interne Validität von Vorteil ist, aber die externe
> Übertragbarkeit begrenzt.

---

## B. Datenschutz & DSGVO

**F: Wer hat Zugriff auf die eingegebenen Patientendaten?**

> Die Daten liegen auf einem Server, der ausschließlich innerhalb der
> klinischen IT-Infrastruktur läuft – kein Cloud-Zugriff, keine externen
> Dienste. Zugriff haben nur autorisierte Nutzer mit Login.

**F: Werden die Daten gespeichert und wie lange?**

> Patientendaten werden in der lokalen PostgreSQL-Datenbank gespeichert.
> Aufbewahrungsfristen richten sich nach den geltenden Datenschutzrichtlinien
> der Klinik. Das System unterstützt das gezielte Löschen einzelner Patienten
> (DSGVO Art. 17 – Recht auf Vergessenwerden: DELETE-Endpoint vorhanden).

**F: Enthält das System echte Patientendaten als Trainingsdaten?**

> Das trainierte Modell enthält keine Rohdaten von Patienten – nur die
> gelernten Parameter (Entscheidungsbäume des Random Forest).
> Die Trainingsdaten selbst verbleiben in der klinischen Dateninfrastruktur.

---

## C. Klinischer Workflow

**F: Wann soll ich das Tool nutzen – vor oder nach der Indikationsstellung?**

> Das Tool ist als *Pre-Decision-Support* gedacht: Eingabe der Befunde
> vor dem abschließenden CI-Gespräch. Das Ergebnis kann als zusätzliche
> Informationsgrundlage in die Entscheidungsfindung einbezogen werden,
> nicht als Gatekeeper.

**F: Wie lange dauert die Dateneingabe?**

> Das Formular hat bis zu 21 Felder – eine vollständige Eingabe dauert
> ca. 3–5 Minuten. Mit Pflichtfeldern (Geschlecht, Alter) ergibt sich
> bereits in unter 1 Minute eine erste Vorhersage.
> Fehlende Felder werden vom Modell durch Mittelwerte aus dem Trainingsdatensatz
> ersetzt (Imputation).

**F: Kann das Tool auch für Kinder eingesetzt werden?**

> Das Modell wurde am Erwachsenenkollektiv trainiert. Für Kinder liegen
> keine validierten Daten vor – eine Anwendung in dieser Gruppe ist
> derzeit nicht empfohlen.

**F: Wie sieht die Integration in unser KIS / EMR aus?**

> Aktuell ist HEAR-UI ein eigenständiges Webinterface. Eine REST-API
> (`/api/v1/patients/`) ermöglicht die programmatische Integration in
> bestehende Systeme. Eine HL7-FHIR-Schnittstelle ist in der Roadmap.

---

## D. Erklärbarkeit (SHAP)

**F: Was bedeuten die roten und blauen Balken im Diagramm?**

> Rote Balken = Features, die die Vorhersagewahrscheinlichkeit *erhöhen*.
> Blaue Balken = Features, die sie *senken*.
> Die Länge des Balkens zeigt den Einfluss des jeweiligen Merkmals auf
> genau diesen Patienten.

**F: Warum bekomme ich manchmal einen anderen Wert als beim letzten Mal?**

> Die Vorhersage ist deterministisch – bei gleichen Eingabewerten immer
> gleich. Unterschiede entstehen, wenn Felder geändert wurden (z. B.
> durch Nacherfassung) oder wenn eine neue Modellversion eingespielt wurde.
> Die Modellversionierung in der Modellkarte hilft, das nachzuvollziehen.

---

## E. Technisches / Weiterentwicklung

**F: Was passiert, wenn das Modell nicht aktuell ist?**

> Die Modellkarte dokumentiert Trainings- und Validierungsdatum.
> Für ein Retraining ist eine neue Exportdatei (`.pkl`) nötig,
> die über den Backend-Deployment-Prozess eingespielt wird.
> Das System zeigt in der Statusseite, welche Modellversion geladen ist.

**F: Können wir eigene Features hinzufügen?**

> Ja, über `backend/app/config/feature_definitions.json` können Features
> konfiguriert werden. Eine Änderung des Featuresets erfordert aber ein
> Retraining des Modells.

**F: Was ist, wenn der Server ausfällt?**

> Das System ist so ausgelegt, dass ein Ausfall keine Patientensicherheit
> gefährdet – es ist ein Unterstützungstool. Für Hochverfügbarkeit kann
> das Docker-Setup auf einem redundanten Server deployt werden.

---

## F. Vertrauen & Akzeptanz

**F: Welche Evidenz gibt es, dass KI-Tools die CI-Entscheidung verbessern?**

> Das ist eine aktive Forschungsfrage. Unser System basiert auf
> publizierten Methoden zur CI-Outcome-Prediction (z. B. [Referenz einfügen]).
> Die interne Validierung zeigt [Metriken]. Eine prospektive klinische
> Studie zur Nutzenevaluation ist geplant.

**F: Verändert das Tool unsere Haftung gegenüber Patienten?**

> Das Tool ist als Dokumentations- und Entscheidungsunterstützungssystem
> klassifiziert, nicht als Medizinprodukt (noch kein CE-Kennzeichen).
> Die Verantwortung für die klinische Entscheidung liegt unverändert
> beim behandelnden Arzt. Eine rechtliche Einschätzung durch den
> Datenschutzbeauftragten der Klinik ist empfohlen, bevor das System
> in den regulären Betrieb geht.
