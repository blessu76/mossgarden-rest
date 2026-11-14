---
title: "Wie der erste TestFlight-Build hochgeladen wurde"
description: "Nach dem Abschluss des MVP ging der erste interne Build hoch, doch das Deploy-Skript hat uns unterwegs einmal gestoppt."
---
Das erste MVP von Moss Garden, einem Idle-Spiel für iOS, wurde als 1.0.0 (1) für interne Tests zu TestFlight hochgeladen, nachdem ein Deploy-Skript den ersten Versuch gestoppt hatte. Die Verarbeitung dauerte etwa drei Minuten, und der Build wurde weder zur Prüfung eingereicht noch für externe Tester geöffnet.

## Was im MVP steckte

Das erste MVP umfasste acht Pflanzen, Offline-Abrechnung, Jahreszeiten, ein Sammelbuch, Speichern und Einstellungen. Anschließend haben wir es als 1.0.0 (1) für interne Tests zu TestFlight hochgeladen. Die Verarbeitung dauerte etwa drei Minuten, und wir haben es weder zur Prüfung eingereicht noch für externe Tester geöffnet.

## Der erste Versuch scheiterte

Als das Deploy-Skript das Green Gate ausführte, gelangte eine Umgebungsvariable mit der Bedeutung „Build-Nummer nicht erhöhen“ in die Tests und brachte sie zum Scheitern, und das Skript hielt genau dort an. Dank dieses Stopps wurde kein fehlerhafter Build hochgeladen. Wir haben das so behoben, dass Kindprozesse die äußere Umgebung nicht mehr erben, und danach erneut hochgeladen.

Deployments können mühsam sein, aber die Regel bleibt: Sind die Tests nicht grün, wird nichts ausgeliefert.

## FAQ

### Was war im ersten TestFlight-Build von Moss Garden enthalten?
Acht Pflanzen, Offline-Abrechnung, Jahreszeiten, ein Sammelbuch, Speichern und Einstellungen, hochgeladen als 1.0.0 (1) für interne Tests.

### Wurde Moss Garden zur App-Store-Prüfung eingereicht?
Nein. Dieser Build wurde nur für interne Tests hochgeladen, und wir haben ihn nicht zur Prüfung eingereicht.
