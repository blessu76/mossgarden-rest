---
title: "How the first TestFlight build went up"
description: "After finishing the MVP, the first internal build went up, but the deploy script stopped us once along the way."
---
The first MVP of Moss Garden, an idle game for iOS, went up to TestFlight as 1.0.0 (1) for internal testing after a deploy script stopped the first attempt. Processing took about three minutes, and the build was not submitted for review or opened to external testers.

## What was in the MVP

The first MVP came together with eight plants, offline settlement, seasons, a collection book, saving and settings. We then uploaded it to TestFlight as 1.0.0 (1) for internal testing. Processing took about three minutes, and we did not submit it for review or open it to external testers.

## The first attempt failed

When the deploy script ran the green gate, an environment variable meaning "don't bump the build number" leaked into the tests and broke them, and the script stopped right there. Thanks to that stop, no bad build was uploaded. We fixed it so child processes no longer inherit the outer environment, then uploaded again.

Deploys can be a hassle, but we keep the rule: if the tests aren't green, nothing ships.

## FAQ

### What was in the first Moss Garden TestFlight build?
Eight plants, offline settlement, seasons, a collection book, saving and settings, uploaded as 1.0.0 (1) for internal testing.

### Has Moss Garden been submitted for App Store review?
No. This build was only uploaded for internal testing, and we did not submit it for review.
