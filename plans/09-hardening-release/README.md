# 09 — Hardening & Release

Validate the completed system under real modpack conditions before calling it finished.

## Tasks

1. [`01-test-matrix.md`](01-test-matrix.md) — compatibility and gameplay test matrix.
2. [`02-performance.md`](02-performance.md) — profiling and bounded-work budgets.
3. [`03-dedicated-server.md`](03-dedicated-server.md) — multiplayer/dedicated-server abuse and lifecycle tests.
4. [`04-world-upgrade.md`](04-world-upgrade.md) — player/world data migrations and downgrade safety.
5. [`05-release-checklist.md`](05-release-checklist.md) — final exact-head release acceptance.
6. [`06-provenance-license.md`](06-provenance-license.md) — clean-room, third-party source/asset provenance and license/permission gate.

## Exit criteria

CI and selected real-pack smoke profiles are green, persistence upgrades are tested, performance budgets are met, clean-room/provenance state is reproducible, the release JAR carries required notices and no actual third-party derivation remains legally/technically unresolved.
