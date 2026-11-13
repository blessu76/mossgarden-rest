---
title: "Why we keep two copies of the save"
description: "Losing a garden you've grown is the worst, so saves are split into a main file and a backup."
---
In an idle game, the most upsetting thing is losing the garden you've been growing. So saving has two safeguards.

The first is a checksum: a check value is written with the save, and if it doesn't match on load, the file is treated as damaged. The second is a backup: the main file and the backup are kept separately, so if the main file breaks we restore from the backup and tell you so. We were careful about the order, too, so a broken main file never overwrites a healthy backup.

We also had to stop the trick of turning the device clock back to collect rewards. When a clock rollback is detected, that stretch is not settled, and the app tells you about it.

When we add features, we keep the save format and only add new fields, so older saves still open in newer versions.
