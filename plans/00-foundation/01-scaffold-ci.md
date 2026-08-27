# 00.01 — Scaffold & CI

## Objective
Create the minimal production-quality NeoForge 1.21.1 / Java 21 project.

## Work
- Pin NeoForge/Gradle/toolchain versions compatible with 1.21.1.
- Establish mod id `black_arcana` unless a conflict is found.
- Add main/client/datagen/test source structure.
- Add JUnit and NeoForge GameTest support.
- Add GitHub Actions for build, unit tests and a dedicated-server smoke path.
- Add formatting/static-analysis only if it is stable for the chosen toolchain.
- Replace the generic `.gitignore` with a Gradle/IDE/run-aware one.

## Acceptance
- `./gradlew build` succeeds from clean checkout.
- Unit test task runs even with zero/placeholder tests.
- Dedicated server reaches a deterministic healthy marker and exits cleanly in CI.
- Client-only classes are never loaded by dedicated server.
- Build artifacts are not committed.
