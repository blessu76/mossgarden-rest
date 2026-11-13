---
title: "Why show dew with decimals"
description: "The moss grows 0.1 per second, yet the dew counter looked frozen. This is how we fixed the number format."
---
Moss was piling up at 0.1 per second, but the dew number at the top of the screen stayed the same for a long time. A tester told us they couldn't tell whether it was counting at all. The cause was simple: from ten upward we only showed whole numbers.

So values below 1 now show two decimals, and values below 1,000 show one. Trailing zeros are dropped, so you read 289 instead of 289.0.

The one real decision was rounding. Showing 185.56 as 185.6 would make something you can't buy yet look affordable. So we **round down** instead: the number on screen is always at most what you actually have.

It is a tiny change, but in a game about waiting, watching the number move is part of the reward.
