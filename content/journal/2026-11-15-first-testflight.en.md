---
title: "How the first TestFlight build went up"
description: "After finishing the MVP, the first internal build went up, but the deploy script stopped us once along the way."
---
The first MVP came together with eight plants, offline settlement, seasons, a collection book, saving and settings. We then uploaded it to TestFlight as 1.0.0 (1) for internal testing. Processing took about three minutes, and we did not submit it for review or open it to external testers.

Our first attempt actually failed. When the deploy script ran the green gate, an environment variable meaning "don't bump the build number" leaked into the tests and broke them, and the script stopped right there. Thanks to that stop, no bad build was uploaded. We fixed it so child processes no longer inherit the outer environment, then uploaded again.

Deploys can be a hassle, but we keep the rule: if the tests aren't green, nothing ships.
