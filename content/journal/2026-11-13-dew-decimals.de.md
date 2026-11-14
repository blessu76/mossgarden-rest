---
title: "Warum der Tau mit Nachkommastellen angezeigt wird"
description: "Das Moos wächst um 0,1 pro Sekunde, doch der Tauzähler wirkte wie eingefroren. So haben wir das Zahlenformat korrigiert."
---
Moss Garden ist ein Idle-Spiel (Incremental) für iOS, und sein Tauzähler wirkte eingefroren, weil er ab zehn nur ganze Zahlen anzeigte. Jetzt zeigen wir unter 1 zwei Nachkommastellen und unter 1.000 eine, und wir runden ab, damit die Zahl nie mehr verspricht, als Sie haben.

## Warum die Zahl eingefroren wirkte

Das Moos sammelte sich mit 0,1 pro Sekunde an, aber die Tauzahl oben auf dem Bildschirm blieb lange gleich. Eine testende Person sagte uns, sie könne nicht erkennen, ob überhaupt gezählt werde. Die Ursache war simpel: Ab zehn zeigten wir nur ganze Zahlen an.

## Was wir geändert haben

Werte unter 1 zeigen jetzt zwei Nachkommastellen, Werte unter 1.000 eine. Nachgestellte Nullen entfallen, sodass Sie 289 statt 289,0 lesen.

Die einzige echte Entscheidung betraf das Runden. 185,56 als 185,6 anzuzeigen, ließe etwas, das Sie noch nicht kaufen können, erschwinglich aussehen. Deshalb **runden wir ab**: Die Zahl auf dem Bildschirm ist immer höchstens so groß wie das, was Sie tatsächlich besitzen.

Es ist eine winzige Änderung, aber in einem Spiel ums Warten gehört es zur Belohnung, die Zahl sich bewegen zu sehen.

## FAQ

### Warum zeigt Moss Garden den Tau mit Nachkommastellen an?
Weil das Moos um 0,1 pro Sekunde wächst und ganze Zahlen den Zähler wie eingefroren wirken ließen. Mit Nachkommastellen sieht man, dass er zählt.

### Wird die Tauzahl auf- oder abgerundet?
Abgerundet. Die Zahl auf dem Bildschirm ist immer höchstens die Menge, die Sie tatsächlich besitzen, sodass nichts erschwinglich aussieht, bevor es das ist.
