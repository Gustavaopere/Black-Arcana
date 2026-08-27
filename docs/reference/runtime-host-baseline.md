# Runtime host baseline — NeoForge 1.21.1

Observed: 2026-08-27.
Installed snapshot source: user-provided `modlist agora atual.txt` uploaded 2026-08-26.
Upstream release status checked against the public project pages on 2026-08-27.

This file is a compatibility baseline for Stage 03. It distinguishes the version actually present in the pack from the newest public 1.21.1 release. Adapter code must target/test the installed baseline first; a newer upstream release is not silently substituted.

| Host | Installed in pack | Latest public 1.21.1 checked | Drift | Stage 03 policy |
| --- | --- | --- | --- | --- |
| Iron's Spells 'n Spellbooks | `1.21.1-3.16.3` | `1.21.1-3.16.3` (2026-08-18) | none | Compile against the documented stable API classifier where sufficient; avoid internal packages. |
| Ars Nouveau | `1.21.1-5.13.0` | `1.21.1-5.13.1` (2026-08-24) | one patch | Treat `5.13.0` as the installed acceptance baseline. Do not assume `5.13.1` binary/API equivalence until tested; add a second compatibility test if the pack updates. |
| Eidolon: Repraised | `1.21.1-0.5.0.2` | `1.21.1-0.5.0.2` (2026-05-09) | none | Inspect supported extension seams before choosing it as a runtime host; theme overlap alone is not an API. |
| Malum | `1.21.1-1.8.2` | `1.21.1-1.8.2` (2025-12-08) | none | Target the current 1.8.x Spirit Rite/registry model; never code against the removed Ritual Plinth-era assumptions. |

## Iron's API boundary

The current public developer guide explicitly documents NeoForge 1.21+ dependency setup using:

- `compileOnly "io.redspace:irons_spellbooks:${irons_spells_version}:api"`;
- `localRuntime "io.redspace:irons_spellbooks:${irons_spells_version}"`.

It states that `io.redspace.ironsspellbooks.api` is the stable API surface, while packages outside it can break between releases. It also documents third-party spell registration through `SpellRegistry`/`DeferredRegister` and config-driven spell values. Black Arcana therefore treats API-only integration as the default and requires an explicit Stage 03 justification for any internal dependency.

## Ars version drift

The installed `5.13.0` remains the compile/runtime truth until the pack changes. Public `5.13.1` is newer, but Black Arcana does not upgrade the user's modpack as a side effect of adapter development. Stage 03 should either:

1. target `5.13.0` exactly; or
2. prove the chosen public extension seam works unchanged on both `5.13.0` and `5.13.1`, then document a compatible range.

Generic Blink/Warp/familiar behavior remains host-owned regardless of the patch version.

## Sources

- Installed versions: user-provided `modlist agora atual.txt`, snapshot 2026-08-26.
- Iron's project: https://www.curseforge.com/minecraft/mc-mods/irons-spells-n-spellbooks
- Iron's developer API: https://iron.wiki/developers/
- Ars release: https://www.curseforge.com/minecraft/mc-mods/ars-nouveau/files/8721482
- Eidolon project: https://www.curseforge.com/minecraft/mc-mods/eidolon-repraised
- Malum files: https://www.curseforge.com/minecraft/mc-mods/malum/files/all?version=1.21.1
