# ROOSTER

Time management as a coil of gooey tubes. Live at https://pablokm.github.io/ISLANAUT/apps/rooster/

## Sharing (Firebase)

Sign-in, cloud saving, friends and spot requests use the Firebase project `rooster-50ce9`.
The web config in `index.html` is public by design; `firestore.rules` is what protects data.

One-time console setup:
1. Authentication > Sign-in method: Google and Email/Password enabled.
2. Authentication > Settings > Authorized domains: `pablokm.github.io`.
3. Firestore Database > Rules: paste `firestore.rules` and Publish. Re-paste it whenever the file changes.

How it fits together:
- `users/{uid}/days/{date}` holds a day's activities. Friends (listed in your `friends` subcollection) can read them.
- Invites are 6-character codes (`invites/{code}`); joining adds each person to the other's friends list.
- A check-in (`pokes/{id}`) asks a friend what they're doing; their answer (and optionally a timer on their day) comes back.
- A spot request (`requests/{id}`) is pending until the other person accepts (it's added to both days) or declines (the asker is told in the app).
- Without a connection, or in the claude.ai version, the app saves on the device only.

Testing locally: serve this folder and open `index.html?mock=Pablo` and `index.html?mock=Ana` in two tabs of
the same browser. On `localhost` that swaps Firebase for an in-browser stand-in shared by the tabs.

Not yet: push notifications when the app is closed. That needs a small server function
(Firebase Cloud Functions, which requires the pay-as-you-go plan) to send the messages.
