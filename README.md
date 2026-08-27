# Black Arcana

Black Arcana is a NeoForge 1.21.1 dark-magic framework and content mod built around bounded power, modular casting, ritual depth, and optional integration with the magic/RPG ecosystem.

The project is a clean-room implementation. Mahou Tsukai and other mods may be used only as behavioral/design references through public documentation and observable gameplay; their code, assets, text, models, sounds, particles, and implementation details are not source material for this repository.

## Toolchain

- Minecraft 1.21.1
- NeoForge 21.1.248
- Java 21
- ModDevGradle 2.0.144
- Gradle 9.2.1 bootstrap

## Build

```bash
./gradlew build
```

The repository uses a text bootstrap launcher that downloads the pinned Gradle distribution and verifies it against Gradle's published SHA-256 checksum before execution. This keeps a clean checkout reproducible without committing a binary wrapper JAR.

## Project memory

Read `plans/README.md`, `plans/STATUS.md`, and `plans/DECISIONS.md` before implementation work.
