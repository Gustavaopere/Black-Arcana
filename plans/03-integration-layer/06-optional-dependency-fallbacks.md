# 03.06 — Optional Dependency & Fallback Matrix

## Objective
Define exactly what happens for every integration combination.

## Implemented matrix
| Provider state | Registry state | Capabilities | Provider-backed content | Startup |
|---|---|---|---|---|
| mod absent | `MISSING_MOD` | none | disabled/hidden | continue safely |
| mod present, API/linkage probe fails | `API_INCOMPATIBLE` | none | disabled | continue with actionable diagnostic |
| mod present, probe succeeds | `AVAILABLE` | adapter-specific only | enabled according to provider contract | continue |

## Rules
- Never crash because an optional mod is absent.
- Never silently make a spell free because its cost provider is absent.
- Disable unavailable content with actionable diagnostics.
- Provider-specific recipe types are guarded by datapack conditions when absence would make deserialization invalid.
- `neoforge.mods.toml` declares integrations optional and `AFTER`; the runtime probe, not a permissive metadata range, is authoritative for API compatibility.
- Mod-bus failures are retained and surfaced as `API_INCOMPATIBLE` when the server runtime is installed.

## Acceptance state
Pure fallback/descriptor tests are prepared. Core-only dedicated-server and installed-provider matrix execution remain blocked on a GitHub Actions job that actually runs steps.
