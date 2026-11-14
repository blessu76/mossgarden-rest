---
title: "Release notes live inside the app"
description: "How we made update notes readable right from the app's settings."
copy_review: iris 2026-11-14
---
Moss Garden, an idle game for iOS, shows its update notes inside the app: settings has a release notes menu with the newest version first. Notes appear in your device language when available, otherwise English, and a build missing either the Korean or the English notes doesn't go out.

## Where updates are read

Where is the most natural place to read about an update? We decided it's inside the app. So settings now has a release notes menu.

## How the notes appear

The newest version's notes come first, with the version, build number and date. If notes exist in your device language you see them, otherwise English. If the notes can't be loaded, we show a short message and leave the rest of the app alone.

## A check before every release

Before each release, a check confirms that this build's notes exist in both Korean and English. A build without notes doesn't go out.

The release notes stay quietly in settings, just something to read.

## FAQ

### Where can I read Moss Garden update notes?
Inside the app, in the settings menu, newest version first with its version, build number and date.

### Which language are the notes shown in?
Your device language if notes exist for it, otherwise English.
