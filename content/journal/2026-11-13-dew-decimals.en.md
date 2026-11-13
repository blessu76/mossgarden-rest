---
title: "Why show dew with decimals"
description: "The moss grows 0.1 per second, yet the dew counter looked frozen. This is how we fixed the number format."
---
Moss Garden is an idle (incremental) game for iOS, and its dew counter used to look frozen because it showed only whole numbers from ten upward. We now show two decimals below 1 and one decimal below 1,000, and we round down so the number never promises more than you have.

## Why the number looked frozen

Moss was piling up at 0.1 per second, but the dew number at the top of the screen stayed the same for a long time. A tester told us they couldn't tell whether it was counting at all. The cause was simple: from ten upward we only showed whole numbers.

## What we changed

Values below 1 now show two decimals, and values below 1,000 show one. Trailing zeros are dropped, so you read 289 instead of 289.0.

The one real decision was rounding. Showing 185.56 as 185.6 would make something you can't buy yet look affordable. So we **round down** instead: the number on screen is always at most what you actually have.

It is a tiny change, but in a game about waiting, watching the number move is part of the reward.

## FAQ

### Why does Moss Garden show dew with decimals?
Because the moss grows 0.1 per second, and whole numbers made the counter look frozen. Decimals let you see that it is counting.

### Does the dew number round up or down?
Down. The number on screen is always at most the amount you actually have, so nothing looks affordable before it is.
