---
title: "Warum wir den Spielstand zweimal speichern"
description: "Einen selbst gezogenen Garten zu verlieren ist das Schlimmste, deshalb besteht der Spielstand aus einer Hauptdatei und einem Backup."
---
Moss Garden, ein Idle-Spiel für iOS, schützt Ihren Garten mit zwei Sicherungen: einer Prüfsumme, die einen beschädigten Spielstand erkennt, und einem separaten Backup, aus dem das Spiel mit einem Hinweis wiederherstellt. Auch das Zurückstellen der Geräteuhr, um Belohnungen abzuholen, wird erkannt, und dieser Zeitraum wird nicht abgerechnet.

## Zwei Sicherungen für den Spielstand

In einem Idle-Spiel ist es am ärgerlichsten, den Garten zu verlieren, den man gezogen hat. Deshalb hat das Speichern zwei Sicherungen.

Die erste ist eine Prüfsumme: Zusammen mit dem Spielstand wird ein Prüfwert geschrieben, und passt er beim Laden nicht, gilt die Datei als beschädigt. Die zweite ist das Backup: Hauptdatei und Backup werden getrennt aufbewahrt. Geht die Hauptdatei kaputt, stellen wir aus dem Backup wieder her und sagen es Ihnen. Auch auf die Reihenfolge haben wir geachtet, damit eine defekte Hauptdatei nie ein intaktes Backup überschreibt.

## Zurückgestellte Uhr

Wir mussten auch den Trick stoppen, die Geräteuhr zurückzustellen, um Belohnungen abzuholen. Wird ein Zurückstellen der Uhr erkannt, wird dieser Zeitraum nicht abgerechnet, und die App informiert Sie darüber.

## Alte Spielstände weiter nutzbar

Bei neuen Funktionen behalten wir das Speicherformat bei und ergänzen nur neue Felder, damit ältere Spielstände auch in neueren Versionen noch geöffnet werden.

## FAQ

### Was passiert, wenn die Spielstanddatei von Moss Garden kaputtgeht?
Die Prüfsumme bemerkt die Abweichung, das Spiel stellt aus dem separaten Backup wieder her und teilt Ihnen mit, dass es das getan hat.

### Kann ich Belohnungen erhalten, indem ich die Geräteuhr ändere?
Nein. Wird ein Zurückstellen der Uhr erkannt, wird dieser Zeitraum nicht abgerechnet, und die App informiert Sie darüber.
