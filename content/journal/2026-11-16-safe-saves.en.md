---
title: "Why we keep two copies of the save"
description: "Losing a garden you've grown is the worst, so saves are split into a main file and a backup."
copy_review: iris 2026-11-14
---
Moss Garden, an idle game for iOS, protects your garden with two safeguards: a checksum that detects a damaged save and a separate backup it restores from, with a notice. Turning the device clock back to collect rewards is also caught, and that stretch is not settled.

## Two safeguards for the save

In an idle game, the most upsetting thing is losing the garden you've been growing. So saving has two safeguards.

The first is a checksum: a check value is written with the save, and if it doesn't match on load, the file is treated as damaged. The second is a backup: the main file and the backup are kept separately, so if the main file breaks we restore from the backup and tell you so. We were careful about the order, too, so a broken main file never overwrites a healthy backup.

## Clock rollbacks

We also had to stop the trick of turning the device clock back to collect rewards. When a clock rollback is detected, that stretch is not settled, and the app tells you about it.

## Keeping old saves working

When we add features, we keep the save format and only add new fields, so older saves still open in newer versions.

## FAQ

### What happens if the Moss Garden save file breaks?
The checksum notices the mismatch, the game restores from the separate backup and tells you it did.

### Can I get rewards by changing the device clock?
No. When a clock rollback is detected, that stretch is not settled, and the app tells you about it.
