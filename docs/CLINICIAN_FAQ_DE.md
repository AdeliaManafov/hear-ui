# HEAR-UI – Mögliche Fragen von Klinikern & Antworten

Vorbereitung für die Präsentation. Antworten sind Vorschläge – bitte an das
eigene Datenmaterial und die Zentrumspolitik anpassen.

---

## A. Modellgüte & Zuverlässigkeit

**F: Wie genau ist das Modell? Kann ich ihm vertrauen?**

> Die Gütemerkmale des Modells – u. a. wie zuverlässig es zwischen Patienten
> mit guten und weniger guten CI-Ergebnissen unterscheidet – sind in der
> Modellkarte dokumentiert (Seitenleiste → „Modellkarte").
> Das Modell schneidet besser ab als eine rein zufällige Entscheidung.
> Die konkreten Kennzahlen (Sensitivität, Spezifität u. a.) finden sich dort.
> Dennoch ist es ein Entscheidungs*unterstützungs*tool – die endgültige Entscheidung
> liegt immer beim Kliniker.

**F: Was ist, wenn das Modell falsch liegt?**

> Kein prädiktives Modell hat 100 % Treffsicherheit. Deshalb zeigt das System
> neben dem Wahrscheinlichkeitswert auch die SHAP-Erklärung: Der Kliniker kann
> sofort sehen, welche Faktoren ausschlaggebend waren, und beurteilen, ob das
> mit der klinischen Realität übereinstimmt. Das Modell ist ein Hilfsmittel,
> kein Ersatz für das ärztliche Urteil.

**F: Auf wie vielen Patienten wurde das Modell trainiert?**

> Die genaue Patientenzahl ist in der Modellkarte des Systems dokumentiert
> (Seitenleiste → „Modellkarte", Abschnitt „Trainingsdaten").
> Die Trainingsdaten stammen ausschließlich aus unserem eigenen Zentrum –
> das ist für die interne Aussagekraft von Vorteil, bedeutet aber auch,
> dass das Modell noch nicht an anderen Häusern validiert wurde.

---

## B. Datenschutz & DSGVO

**F: Wer hat Zugriff auf die eingegebenen Patientendaten?**

> Das hängt davon ab, wie das System in Ihrer Einrichtung eingerichtet ist.
> Bitte klären Sie mit Ihrem IT-Beauftragten, auf welchem Server das System
> läuft, wer Zugriff hat und ob externe Dienste beteiligt sind.
> Standardmäßig sieht das System nur Nutzer vor, die sich mit Zugangsdaten anmelden.

**F: Werden die Daten gespeichert und wie lange?**

> Patientendaten werden in der Datenbank des Systems gespeichert.
> Aufbewahrungsfristen richten sich nach den geltenden Datenschutzrichtlinien
> der Klinik. Das System unterstützt das gezielte Löschen einzelner Patienten
> (Recht auf Vergessenwerden gemäß DSGVO Art. 17).

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
> ca. 3–5 Minuten. Mit den drei Mindestfeldern für die Vorhersage
> (Geschlecht, Alter und Hörminderung operiertes Ohr) ergibt sich
> bereits in unter 1 Minute eine erste Orientierungsvorhersage.
> Fehlende Felder werden vom Modell durch Mittelwerte aus dem Trainingsdatensatz
> ersetzt (Imputation).

**F: Welche Felder sind Pflichtfelder für das Formular?**

> Für eine Vorhersage sind mindestens drei Felder erforderlich:
> **Geschlecht**, **Alter** und **Hörminderung (operiertes Ohr)**.
> Das System meldet einen Fehler, wenn diese fehlen.
>
> Für eine vollständige und klinisch valide Patientenerfassung empfehlen
> wir die folgenden sieben Felder auszufüllen:
> 1. Alter
> 2. Geschlecht
> 3. Hörminderung (operiertes Ohr)
> 4. Beginn der Hörminderung (OP-Ohr)
> 5. Art der Hörstörung
> 6. Bildgebung: Befund (mind. normal/pathologisch)
> 7. Ursache der Hörminderung

**F: Kann das Tool auch für Kinder eingesetzt werden?**

> Das Modell wurde am Erwachsenenkollektiv trainiert. Für Kinder liegen
> keine validierten Daten vor – eine Anwendung in dieser Gruppe ist
> derzeit nicht empfohlen.

**F: Wie sieht die Integration in unser KIS / EMR aus?**

> Aktuell ist HEAR-UI ein eigenständiges Webinterface. Eine technische
> Schnittstelle für die programmatische Integration in bestehende Systeme
> ist vorhanden. Eine HL7-FHIR-Anbindung ist als zukünftiger Entwicklungsschritt geplant.
> Die konkreten Integrationsschritte stimmen Sie bitte mit Ihrer IT-Abteilung ab.

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

**F: Können wir eigene Merkmale hinzufügen?**

> Das Featureset ist grundsätzlich konfigurierbar. Eine Erweiterung um neue
> klinische Merkmale ist möglich, erfordert aber technische Anpassungen und
> ein Neutraining des Modells. Sprechen Sie dazu das Entwicklungsteam an.

**F: Was ist, wenn das System nicht erreichbar ist?**

> Das System ist ein reines Unterstützungstool – ein Ausfall hat keinen
> Einfluss auf die Patientensicherheit. Der klinische Workflow kann ohne
> das System fortgeführt werden. Fragen zur Verfügbarkeit und Ausfallsicherheit
> richten Sie bitte an Ihre IT-Abteilung.

---

## F. Vertrauen & Akzeptanz

**F: Welche Evidenz gibt es, dass KI-Tools die CI-Entscheidung verbessern?**

> Das ist eine aktive Forschungsfrage. Unser System basiert auf
> publizierten Methoden zur CI-Outcome-Vorhersage.
> Die Kennzahlen zur internen Validierung sind in der Modellkarte einsehbar.
> *(Hinweis: Konkrete Literaturangaben bitte vor der Präsentation intern prüfen
> und ergänzen.)*
> Eine prospektive klinische Studie zur Nutzenevaluation ist geplant.

**F: Verändert das Tool unsere Haftung gegenüber Patienten?**

> Das Tool ist als Dokumentations- und Entscheidungsunterstützungssystem
> klassifiziert, nicht als Medizinprodukt (noch kein CE-Kennzeichen).
> Die Verantwortung für die klinische Entscheidung liegt unverändert
> beim behandelnden Arzt. Eine rechtliche Einschätzung durch den
> Datenschutzbeauftragten der Klinik ist empfohlen, bevor das System
> in den regulären Betrieb geht.
