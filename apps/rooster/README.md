# ROOSTER

Time management as a coil of gooey tubes. Live at https://pablokm.github.io/ISLANAUT/apps/rooster/

## Timeline world (tap the date)

Tapping the date at the top opens a 3D scene in a white void: one line running ahead through your days, one hour per world unit.
Your low-poly rooster (extruded from the traced design pieces) walks it. Drag up, or hold the arrows to run; the double arrows hop a day.
- The line is coloured by your activities and ends at the latest one. Past that it dashes on, so you can keep walking to plan further out.
- The flag button plants a marker where the rooster stands. Set its title, date, time, length and colour. It is saved as a locked
  activity (`ev: 1`) on that day, so it shows in the day view and syncs like any other activity. Tap a flag to edit or delete it.
- Overhead flips to a flat view of the whole line: drag to scroll, pinch to zoom, tap the line to move the rooster, tap a flag to edit.
- The renderer is a small canvas painter in `index.html` (no libraries), so it works offline and in the claude.ai version.

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
- The chicken button sends a check-in (`pokes/{id}`) asking a friend what they're doing, and opens their day. Their answer (and optionally a timer on their day) comes back.
- On a friend's day, tap an open spot to ask for it, or tap one of their activities to suggest something in its place. Requests can carry a note.
- A spot request (`requests/{id}`) is pending until the other person accepts (it's added to both days) or declines (the asker is told in the app).
- Without a connection, or in the claude.ai version, the app saves on the device only.

Testing locally: serve this folder and open `index.html?mock=Pablo` and `index.html?mock=Ana` in two tabs of
the same browser. On `localhost` that swaps Firebase for an in-browser stand-in shared by the tabs.

Not yet: push notifications when the app is closed. That needs a small server function
(Firebase Cloud Functions, which requires the pay-as-you-go plan) to send the messages.
