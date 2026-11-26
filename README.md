# meme-typ

Welcher Meme-Typ bist du? Ein Spaß-Persönlichkeitstest: Der Test beginnt direkt auf der Hauptseite: In 4 Runden stehen links je 4 klassische Meme-Vorlagen, die man rechts auf die Plätze 1–4 einordnet (Antippen = nächster freier Platz, Ziehen = gezielt einordnen oder tauschen, Antippen eines Platzes legt zurück). Man bekommt einen von 8 Meme-Typen samt Humor-Profil auf 4 Achsen. Deutsch und Englisch.

- Seite: https://schrauberbits.github.io/meme-typ/ (englisch: `/en/`)
- Typ-Seiten: `/typ/<typ>/` und `/en/type/<type>/`, jeweils mit eigenem Vorschaubild (`og/`)
- Inhalte (Memes, Achsen-Gewichte, Typen, Texte): `_werkzeug/daten.json`; Aufbau der App: `_werkzeug/vorlage.html`. Nach Änderungen `python3 _werkzeug/bau.py` ausführen (mit `--ohne-bilder`, wenn sich nur Texte geändert haben). Das Skript schreibt `index.html`, `en/index.html`, die Typ-Seiten, die Vorschaubilder, `sitemap.xml`, `robots.txt` und `urls.txt`.

## Rechnung

- Platz 1–4 auf einer Seite ergibt 3/2/1/0 Punkte.
- Jedes Meme wirkt mit Gewichten auf die Achsen 🔥 Gelassen im Chaos, 🧠 Ironie & Meta, 🎭 Drama & Selbstironie und 💥 Absurd & schräg. Der Achsenwert ist der gewichtete Durchschnitt der Punkte (0–3, angezeigt in Prozent).
- Der Typ ist der Prototyp mit der größten Übereinstimmung mit der Abweichung vom Mittel. Mischtypen werden mit dem Faktor 1,3 gewichtet, damit bei zufälliger Sortierung jeder Typ etwa gleich oft vorkommt (Simulation: 10–15 % je Typ).
- Die Begründung nennt die Seitensieger, die am besten zum Typ passen.

## Teilen und Zählen

- Das Ergebnis steckt nur im Link (`#r=<16 Ziffern>`). Ein Vergleichslink führt auf die Typ-Seite mit `#vs=<16 Ziffern>`. Wer darüber den Test macht, sieht, wie ähnlich der Humor ist.
- Das Story-Bild (1080×1920) wird im Browser nur aus eigenen Grafiken gezeichnet, ohne fremde Bilder.
- Zählung über GoatCounter (schrauberbits.goatcounter.com):
  - `meme-start--<ref>`: Test begonnen
  - `meme-nutzung--<ref>`: erste eigene Bewegung
  - `meme-fertig--<ref>`: Ergebnis erreicht
  - `meme-teilen--<ref>`: Teilen, Story-Bild oder Link kopiert
  - `meme-vergleich--<ref>`: Test über einen Vergleichslink beendet
- Geteilte Links tragen `?ref=<Kennung>-w` (ohne Kennung: `direkt-w`). Typ-Seiten verlinken den Test mit `?ref=seite-<typ>`.

## Bilder und Rechte

Die Meme-Vorlagen werden von i.imgflip.com geladen (Links, keine Kopien im Repository). Fällt ein Bild aus, erscheint eine neutrale Ersatzkarte mit dem Namen. Aufgenommen sind bewusst nur Vorlagen ohne Fotos von Prominenten und ohne Figuren aus Filmen und Serien.

Die Datei `04fadd290f4b124950e8f09ef381b6ff.txt` ist der öffentliche IndexNow-Nachweis, kein Zugangsschlüssel.

Das Programm ruft keinen KI-Dienst auf und enthält keine Zugangsdaten. Ein Hobbyprojekt, mit KI-Hilfe erstellt.
