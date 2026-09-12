# Phase 2BH — Goety 3.1.4 exact checkpoint

Status: `CANONICAL — DURABLE PR + EXACT POST-MERGE CI GREEN`

Base audited: `main@7d14874e7d477c8ae2b3c8643c1519feea5a90cc`.

Exact physical identity: `goety-3.1.4.jar`, `goety` / `3.1.4`, SHA-1 `a0770e180e4e8b1b87d8fa9c8356e9dbf34d82a7`, CurseForge `586095 / 8689429`, modlist 595 / `7aaece7acbfb07ba4d0c66029042f36c50d046f0`.

Exact catalog evidence came from isolated non-merge PR #197: `34670150370/10290083272`, `34670458172/10290222369`, `34670556329/10290527131`, `34670758163/10289884505`. Discarded harness-failure runs `34670348040` and `34670400350` are not evidence.

Durable PR #198 clean HEAD `d75f82a23b5c977ccc8ec84813bf89c928ffc0ab` passed Black Arcana CI **#2523** / run `34672038273`. It was squash-merged as `4fcc40aaf8149b5511dbd882a5616ee5240cd640`; that exact merge SHA passed Black Arcana CI **#2524** / run `34672222798`, including unit tests, diff sanity, NeoForge build, built-JAR verification, Foundation GameTest, dedicated-server smoke and canonical QA-JAR publication.

Canonical QA artifact: `black-arcana-4fcc40aaf8149b5511dbd882a5616ee5240cd640`, artifact ID `10291461067`, SHA-256 `4f2ccf8be11cdba348c7cd0bdc64e595f6b101257b2b99f80fbe5542fae41ada`.

Canonical disposition: 123 active Focus actions + 238 available distinct non-Focus ritual actions = **+361**; strict semantic minimum **888 → 1249**; provider-component coverage **56/100 → 57/100**, component #57.

Numerical balance, Soul Energy settlement APIs, research, servants/Summon Down, Lichdom, ritual completion hooks, full-modpack runtime QA and Black Arcana adapter seams remain separate fail-closed gates. No runtime/Stage authority changes are part of Phase 2BH.
