# Phase 2BH — Goety 3.1.4 exact checkpoint

Status: `DURABLE PROMOTION CANDIDATE — NOT CANONICAL UNTIL MERGE + EXACT POST-MERGE CI`

Base audited: `main@7d14874e7d477c8ae2b3c8643c1519feea5a90cc`.

Exact physical identity: `goety-3.1.4.jar`, `goety` / `3.1.4`, SHA-1 `a0770e180e4e8b1b87d8fa9c8356e9dbf34d82a7`, CurseForge `586095 / 8689429`, modlist 595 / `7aaece7acbfb07ba4d0c66029042f36c50d046f0`.

Evidence: PR #197; `34670150370/10290083272`, `34670458172/10290222369`, `34670556329/10290527131`, `34670758163/10289884505`.

Candidate disposition: 123 active Focus actions + 238 available distinct non-Focus ritual actions = **+361**; strict semantic minimum **888 → 1249**; provider-component coverage **56/100 → 57/100**, candidate component #57.

Numerical balance, Soul Energy settlement APIs, research, servants/Summon Down, Lichdom, ritual completion hooks, full-modpack runtime QA and Black Arcana adapter seams remain separate fail-closed gates. No runtime/Stage authority changes are part of Phase 2BH.

Promotion requires clean reconciled durable HEAD, GREEN PR-head CI, merge against latest main, and GREEN exact-SHA post-merge CI. A final-evidence reconciliation must then promote candidate totals to canonical values.
