# PersonalityDNA AI — mobile

Expo + React Native shell with the same five-tab information architecture as the web app (Home, Discover, AI Coach, Growth, Profile).

Application ID: `com.personalitydna.ai`

## Status

The native screens in this folder are a functional navigation shell. Assessment taking, scoring, and coaching currently run against the FastAPI backend via the Next.js web app, which is the complete client in this increment.

To run locally after installing Expo tooling:

```bash
cd apps/mobile
npx expo start
```

Store credentials, push certificates, and RevenueCat keys are external blockers and are not bundled.
