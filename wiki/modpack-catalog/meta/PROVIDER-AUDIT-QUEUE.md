# Fila operacional de auditoria dos providers mágicos

## Autoridade atual

O snapshot imediatamente anterior está preservado byte-for-byte em [`PROVIDER-AUDIT-QUEUE-PRE-PHASE2AX.md`](./PROVIDER-AUDIT-QUEUE-PRE-PHASE2AX.md).

- Minecraft 1.21.1
- NeoForge `21.1.248`
- modlist física: **595 entradas top-level**
- SHA-1 da modlist: `7aaece7acbfb07ba4d0c66029042f36c50d046f0`
- estado canônico pós-Phase 2BL: `main@43e343dfdfe1119820f05888ebbf79debc3db8da`; esse SHA incorpora o fechamento durável de Phase 2BL e a estabilização de fixture da PR #208, e passou exact-SHA post-merge CI #2540 / run `34709290589`, incluindo 104/104 Foundation GameTests, dedicated-server smoke e canonical QA artifact `10302279485` (`sha256:3398896435975751fec35357fde1e83b76dfa1463cb1e2771756834aec0bdae0`);
- jarjar/internal não conta como provider top-level

## Métricas separadas

### Cobertura semântica de magias — métrica principal para o usuário

A reconstrução canônica após Phase 2BK fecha **1250 objetos mágicos semânticos**. Phase 2BL fecha Goety Iron 3.1 em **+14** e Goety Cataclysm 1.21.1-1.8.2 em **+52**, portanto o mínimo passa a **1316**. O denominador global continua incompleto e nenhuma porcentagem semântica é declarada.

A correção de contagem imediatamente anterior ao fechamento Alshanex continua sendo **Werewolves Leap +1**: a source exata 2.0.3.3 prova `LEAP` como `ActionSkill`, nó `SURVIVAL31` conectado à árvore normal e input dedicado processado pelo servidor/provider. Portanto Leap deixa de ser `CONDITIONAL` e Werewolves passa de 7 para 8 ações semânticas contadas. `hide_name` continua excluído como presentation-only; `no_leap_cooldown` continua sendo uma questão separada de refinement/acquisition.

GTBC's SpellLib 2.2.0 adiciona **0 magias semânticas independentes**. É infraestrutura de biblioteca/API compartilhada; atributos e helpers reutilizáveis não são identidades de spell próprias.

A Phase 2BJ substitui a reconciliação publisher-only anterior: o JAR exato Gaze 1.1.7.1 agora está hash-matched. Soulward Shield adiciona **+1**; os 26 Spirit Rites exatos permanecem `CONDITIONAL` por falta do valor COMMON implantado de `disableGazeRites`; 2 Geas e 8 runes são metric-excluded.

- delta semântico Werewolves: **+1**;
- delta semântico GTBC SpellLib: **+0**;
- delta semântico Ignis Soulfires: Spellbooks 1.1.0 Phase 2BK: **+0** (`ZERO_BRIDGE_INFRA` exact-artifact);
- delta semântico Gaze 1.1.7.1 Phase 2BJ: **+1**;
- delta semântico Alshanex 4.0.3: **+18**;
- delta semântico Cataclysm: Spellbooks 1.1.13: **+59**;
- delta semântico Somake 1.0.8-fix Phase 2BF: **+0** (`67 exact registry`, reachability/config efetivo ainda `CONDITIONAL`);
- delta semântico Leyline Spellbooks 1.0.3 Phase 2BG: **+14** (`14 exact unconditional registry identities`);
- delta semântico Goety 3.1.4 Phase 2BH: **+361** (`123 active Focus + 238 available distinct non-Focus rituals`);
- delta semântico Goety Iron 3.1 Phase 2BL: **+14** (`2 Focus + 12 distinct non-Focus rituals`);
- delta semântico Goety Cataclysm 1.21.1-1.8.2 Phase 2BL: **+52** (`28 Focus + 24 distinct non-Focus rituals`);
- mínimo estrito global após Phase 2BL: **1316**;
- denominador global: ainda incompleto;
- nenhuma porcentagem final de spells/magias é declarada enquanto inventories atuais permanecem abertas.

### Cobertura interna de componentes do catálogo

- Phase 2AY / PR #175 foi mergeada como `9a4e1cd6a462a278083ab946b5ed054864c3315e`;
- HEAD auditado `2260c46261ac9ab99d839f307fd7b4519d38eef2` passou Black Arcana CI #2420;
- o merge SHA exato de Phase 2AY passou Black Arcana CI #2421 com unit tests, diff sanity, NeoForge build, built-JAR verification, Foundation GameTest server, dedicated-server smoke e publicação do canonical QA JAR;
- Gaze / PR #180 foi mergeada como `03054438d1f126f48cb0b11b84c5d6589d677666`;
- o merge SHA exato da reconciliação Gaze passou Black Arcana CI #2434 com unit tests, diff sanity, NeoForge build, built-JAR verification, Foundation GameTest server, dedicated-server smoke e publicação do canonical QA JAR;
- a reconciliação Gaze permanece parcial e **não** cria novo componente canônico fechado;
- Phase 2BD / PR #186: HEAD auditado `acfcff0fca09b3c2f7b4fcf082618a970e1d19c0` passou Black Arcana CI #2464;
- PR #186 foi squash-mergeada como `95ec538ff1c34766450393522ce3affe1039d0dd`; o merge SHA exato passou Black Arcana CI #2465 com unit tests, diff sanity, NeoForge build, built-JAR verification, Foundation GameTest server, dedicated-server smoke e publicação do canonical QA JAR;
- cobertura de componentes após o fechamento Phase 2BL: **60/100 = 60%**; `goetyiron` é componente #59 e `goety_cataclysm` é componente #60 por exact-artifact semantic closure.

O valor 60/100 nunca substitui a métrica semântica de magias.

## Phase 2BL — Goety Iron 3.1 + Goety Cataclysm 1.21.1-1.8.2 — componentes #59/#60 / semantic +66

| Mod ID | Artefato físico | Estado |
|---|---|---|
| `goetyiron` | `GoetyIron-1.21.1-NeoForge-3.1.jar` | EXACT HASH-MATCHED / 2 FOCUS + 12 DISTINCT NON-FOCUS RITUALS / UNCONDITIONAL REGISTRATION GATE / +14 / COMPONENT #59 |
| `goety_cataclysm` | `goety_cataclysm-1.21.1-1.8.2.jar` | EXACT HASH-MATCHED / 28 FOCUS + 24 DISTINCT NON-FOCUS RITUALS / UNCONDITIONAL REGISTRATION GATE / +52 / COMPONENT #60 |

Evidence: NON-MERGE PR #205 (Iron) and #206 (Cataclysm). Both audits hard-gate exact physical SHA-1, deduplicate Focus acquisition recipes and compare semantic ownership against base Goety 3.1.4. Runtime mechanics and adapters remain fail-closed.

## Phase 2BK — Ignis Soulfires: Spellbooks 1.1.0 — componente #58 / semantic +0

| Mod ID | Artefato físico | Estado |
|---|---|---|
| `ignissoulfires_spellbooks` | `ignissoulfires_spellbooks-1.1.0.jar` | EXACT HASH-MATCHED ARTIFACT / BRIDGE_COMPAT + GEAR_LOOT_SUPPORT / 11 PROVIDER CLASSES / ARMOR MATERIAL + 5 ITEMS / NO SPELL-RITUAL-ACTION REGISTRY / ZERO_BRIDGE_INFRA / +0 SEMANTIC / COMPONENT #58 |

Evidence: physical/audit SHA-1 `dcde77db35b6de3562b4e6de0025746eaf68f119`; CurseForge project/file `1572171 / 8620663`; NON-MERGE PR #203; audit HEAD `ed807b77345cde1803767d804e26ea972c41d964`; run `34688273425` GREEN; text-only artifact `10296406134`, digest `sha256:5e96a319aea648aadf2c70bdf9b870a26a9503068307befc8a9972bb7b1cd52e`. ARR JAR not redistributed. Runtime gear values/ABI and any Black Arcana adapter remain fail-closed.

## Phase 2BH — Goety 3.1.4 — componente #57 canônico

Exact evidence PR #197 closes **123 Focus + 238 non-Focus rituals = +361 semantic objects**. Accepted run/artifact pairs: `34670150370/10290083272`, `34670458172/10290222369`, `34670556329/10290527131`, `34670758163/10289884505`. Durable PR #198 clean HEAD `d75f82a23b5c977ccc8ec84813bf89c928ffc0ab` passed CI #2523; squash merge `4fcc40aaf8149b5511dbd882a5616ee5240cd640` passed exact-SHA post-merge CI #2524. Canonical QA artifact: `10291461067`, SHA-256 `4f2ccf8be11cdba348c7cd0bdc64e595f6b101257b2b99f80fbe5542fae41ada`. Canonical totals are **1249 / 57/100**.

## Phase 2BG — Leyline Spellbooks 1.0.3 — componente #56 canônico

| Mod ID | Artefato físico | Estado |
|---|---|---|
| `leylines` | `leylines-1.0.3.jar` | EXACT PHYSICAL / EXACT CURSEFORGE FILE / EXACT HASH-MATCHED ARTIFACT AUDIT / 14 UNCONDITIONAL REGISTERED SPELL IDENTITIES / NO PROVIDER-SPECIFIC SPELL LOCK OBSERVED / GENERIC HOST CONFIG QA SEPARATE / +14 SEMANTIC MAGICS / #56 CANONICAL / POST-MERGE CI #2504 GREEN |

Evidence: non-merge PR #194; primary `34666436710 / 10289437099`; reachability `34666652534 / 10289292617`; school/loot gate `34667641655 / 10289184487`; exact Iron's 3.16.3 host source `e4056af90302d37eb1739f5ff05020b020e6e252`; durable PR #195 clean HEAD `a9d7b55044230bbb011f7233ffd75d9a8321489b` / CI #2503 GREEN; squash merge `88f042f68429ff920314a7ec3a6923369edc93fd` / post-merge CI #2504 GREEN. Canonical totals are **888 / 56/100**.

## Phase 2BF — Somake Spells 1.0.8-fix — exact registry, sem novo componente

| Mod ID | Artefato físico | Estado |
|---|---|---|
| `somakespells` | `somakespells-1.0.8-1.21.1-fix.jar` | EXACT PHYSICAL / EXACT CURSEFORGE FILE / EXACT HASH-MATCHED ARTIFACT AUDIT / 67 CURRENT REGISTERED SPELL IDENTITIES UNDER PHYSICAL OPTIONAL SET / EFFECTIVE COMMON CONFIG + SURVIVAL REACHABILITY CONDITIONAL / +0 STRICT SEMANTIC DELTA / 55/100 UNCHANGED |

### Evidence boundary

- physical/audit SHA-1 `b0ad94c1504709662bee2d08700375ccecbb5ec7`;
- CurseForge project/file `1461634 / 8417850`;
- isolated non-merge evidence PR #191; initial exact-registry run `34659320633`, reachability run `34664093646`, targeted gate run `34664411845`;
- durable PR #192: clean HEAD `85b15aec9faf395cef5460d06a17be58ccd16af8` / CI #2490 GREEN; squash merge `cc4cfc1d740f7714188e25a3586d8b43bb5eb969` / post-merge CI #2491 GREEN;
- exact registry: 67 typed fields, 67 unique registration IDs, 67 provider `*Spell` classes;
- 61 unconditional registrations; three require `mowziesmobs`; three require `iss_magicfromtheeast`; both mod IDs are in the physical pack, so all 67 registry identities are current for this provider set;
- `enableSpellLockSystem` is COMMON at `somakespells/general/common.toml`, code-default `false`; actual deployed value is not available in authoritative materials;
- complete per-object survival acquisition/reachability, T.O Aqua runtime ownership and supported adapter/API seams remain open/fail-closed;
- ARR clean-room: no implementation/source reconstruction/assets/text are copied or adapted.

This closes the old `over 50 / registry unknown` blocker but does not satisfy the ledger's player-reachability gate. Somake is not component #56 and contributes +0 until the effective config and survival path are closed strongly enough.

## Phase 2BE — Cataclysm: Spellbooks 1.1.13 — componente #55 canônico

| Mod ID | Artefato físico | Estado |
|---|---|---|
| `cataclysm_spellbooks` | `cataclysm_spellbooks-1.1.13-1.21.jar` | EXACT PHYSICAL / EXACT CURSEFORGE FILE / EXACT HASH-MATCHED ARTIFACT AUDIT / 59 REGISTERED SPELL IDENTITIES / 10 TRANSLATION-ONLY ROOT KEYS EXCLUDED / +59 SEMANTIC MAGICS / #55 CANONICAL / POST-MERGE CI #2484 ATTEMPT 2 GREEN |

### Evidence boundary

- physical SHA-1 `4af8348cc77bbff2ab7057c1fac26a5ab0a5b6a2`;
- CurseForge project/file `1099461 / 8792628`;
- isolated non-merge PR #188 primary run/artifact `34656614109 / 10285687158`;
- constructor-ID disambiguation run/artifact `34656814496 / 10285756485`;
- exact registry: 59 `Supplier<AbstractSpell>` fields, 59 `registerSpell` calls, 59 class instantiations, 0 conditional branches;
- exact group distribution: 7 Abyssal, 4 Ender, 1 Evocation, 5 Holy, 11 Fire, 5 Ice, 4 Nature, 22 Technomancy;
- ten extra root localization keys are unregistered and excluded;
- publisher generic/current 65-spell scale is not substituted for physical 1.1.13;
- no upstream implementation/assets copied ou adapted; balance/acquisition/runtime/API seams remain fail-closed where not separately proven.

## Phase 2BD — Alshanex's Familiars 4.0.3 — componente #54

| Mod ID | Artefato físico | Estado |
|---|---|---|
| `alshanex_familiars` | `alshanex_familiars-1.21.1_v4.0.3.jar` | EXACT PHYSICAL / EXACT CURSEFORGE FILE / EXACT HASH-MATCHED ARTIFACT AUDIT / 7 SPELLS + 11 RITUALS / +18 SEMANTIC MAGICS / #54 |

### Evidence boundary

- physical SHA-1 `e5051c2385a426d05bf203ba8081a23d891f6686`;
- CurseForge project/file `1171602 / 8675568`;
- isolated audit run/job `34649305941 / 103427464735` materialized the exact Curse Maven artifact and required hash equality;
- exact spell inventory: 7 unconditional provider registry assignments/calls mapped to current IDs;
- exact ritual inventory: 11 packaged resources of custom type `alshanex_familiars:ritual_recipe`;
- Sound/Melodic ownership stays with Tunes n' Tomes; borrowed Iron's casts/familiar AI do not create duplicate semantic objects;
- no upstream implementation/assets copied or adapted; runtime/API/ownership adapter seams remain fail-closed.

## Phase 2BJ — Gaze 1.1.7.1 — exact artifact, semantic +1, component still open

| Mod ID | Artefato físico | Estado |
|---|---|---|
| `gaze` | `gaze-1.1.7.1.jar` | EXACT HASH-MATCHED ARTIFACT / 1 GAZE-OWNED IRON'S SPELL COUNTED / 26 PLAYER-FACING SPIRIT RITES CONFIG-CONDITIONAL / 2 GEAS + 8 RUNES METRIC-EXCLUDED / +1 SEMANTIC / 57/100 UNCHANGED |

### Evidence boundary

- physical/audit SHA-1 `a8cb3190bde157f78160ce65c202ce2d47fb2041`;
- CurseForge project/file `1273454 / 7261638`;
- Modrinth project/version `NlvaJ5WE / od4ltbRo`;
- isolated NON-MERGE PR #201, exact audit HEAD `2f4ff6536663b1c629a6a5ea92416765bea17b1e`;
- final evidence run `34676660467`, artifact `10292013626`, digest `sha256:fb69f353b672f7c8ec7b470c454d24d1c3110cb996a250076a16d2b053f23f71`;
- exact registry/progression evidence: 26 player-facing Gaze Spirit Rites, 2 Geas effect types, 8 rune items, 1 Gaze-owned Iron's spell (Soulward Shield);
- physical `irons_spellbooks` 3.16.3 satisfies the optional provider gate for Soulward Shield;
- exact COMMON `disableGazeRites` gate suppresses the rite registry when true; deployed value unavailable, so the 26 Rites remain conditional;
- ARR clean-room: no implementation bodies/assets/text copied or adapted.

Gaze therefore contributes **+1** to the strict semantic numerator, producing **1250**, but remains an open provider component and does not create component #58. The next actionable provider with materially new exact evidence should be pursued before repeating config-blocked Gaze/NEG work.

## Phase 2AY — GTBC's SpellLib 2.2.0 — canonical #53

| Mod ID | Artefato físico | Estado |
|---|---|---|
| `gtbcs_spell_lib` | `gtbcs_spell_lib-2.2.0-1.21.1.jar` | EXACT PHYSICAL / EXACT PUBLISHER RELEASE / SHARED LIBRARY+API INFRASTRUCTURE / 0 INDEPENDENT SEMANTIC SPELLS / #53 CANONICAL / POST-MERGE CI GREEN |

### Evidence boundary

- physical version `2.2.0`, SHA-1 `36cce8ab3117e89ae992a84a566d596709db2ffe`;
- CurseForge project/file `1194714 / 8824651`;
- publisher defines SpellLib as shared library/API infrastructure with no standalone gameplay of its own;
- 2.2.0 publisher delta adds Healing Received, Damage Taken and Summon Health attributes;
- reusable `AdvancedSpell`, imbuement, Curio, trade, particle and summon surfaces são infrastructure, not proof of provider-owned spell identities;
- no JAR decompilation or copied implementation/assets; unsupported internal signatures remain fail-closed.

### Authority boundary

GTBC's SpellLib owns only its library facilities. Concrete spell identities and cast settlement remain owned by the consuming spell providers/Iron's substrate as applicable. Black Arcana does not create a second spell registry, mana ledger or cast settlement because a library exposes reusable machinery.

## Semantic correction — Werewolves Leap

Exact source authority: `TeamLapen/Werewolves@b72635b3e014e406b25bb79adb9d340f7443660b`.

The earlier ledger exclusion is superseded because source establishes the complete player path:

- `ModSkills.LEAP` is an `ActionSkill` bound to `ModActions.LEAP`;
- `SURVIVAL31` is constructed with `ModSkills.LEAP`;
- `SkillTreeProvider` connects `SURVIVAL31` into `werewolf_level`;
- generated configured tree contains the node;
- client Leap input reaches a dedicated server packet enum/action;
- server delegates to Werewolves/Vampirism action authority.

See [`SEMANTIC-MAGIC-DELTA-WEREWOLVES-LEAP.md`](./SEMANTIC-MAGIC-DELTA-WEREWOLVES-LEAP.md). This changes only the semantic count, not provider-component coverage.

## Phase 2AX — FamiliarsLib 1.7.1 — canonical #52

| Mod ID | Artefato físico | Estado |
|---|---|---|
| `familiarslib` | `familiarslib-1.21.1-1.7.1.jar` | EXACT PHYSICAL / EXACT PUBLISHER FILE / RELEASE-CORRELATED OFFICIAL SOURCE / FAMILIAR FRAMEWORK + ATTACHMENT + NETWORK AUTHORITY / IRON'S SPELL CLASSIFICATION CONSUMER / SOUND CONTENT REMOVED IN 1.7 / 0 INDEPENDENT SEMANTIC SPELLS / #52 CANONICAL / POST-MERGE CI GREEN |

### Evidence boundary

- physical runtime `1.21.1-1.7`, mod id `familiarslib`, SHA-1 `7fa3f3116e35c12456425ae195924ced33fcc2eb`;
- CurseForge project/file `1316458 / 8059464`, 2026-05-08, release, NeoForge / Minecraft 1.21.1;
- official source repository `Alshanex/FamiliarsLib`;
- strongest release-correlated source commit `56561e7fd474fbd5c5166c1ac96f235faae156ab`, same date and matching familiar-bed bug-fix intent;
- correlated source tree `9d39b4751b9e52874f66cf2187afab239d00b251`, recursive `truncated=false`;
- source metadata: MC 1.21.1, NeoForge development baseline 21.1.90, Iron's `1.21.1-3.15.5`, Curios 9.2.2, mod version `1.21.1-1.7`;
- no release tag or reproducible-build proof was established, so source↔installed-JAR exactness remains unproven.

### Runtime and authority boundary

FamiliarsLib demonstrably owns framework surfaces for familiars rather than a standalone player spell catalog:

- serializable `player_familiar_data` attachment;
- familiar data/lifecycle, beds and storage;
- familiar summon/selection/release/movement/storage/sync networking;
- `PayloadHandler` registers 17 optional handlers: 9 play-to-server and 8 play-to-client;
- spellcasting familiar base classes and familiar-spellbook/school interoperability;
- Iron's spell classification tags under `data/familiarslib/tags/irons_spellbooks/spells/**`.

The complete release-correlated tree has no provider-owned spell registry and no `data/familiarslib/spells/**` content. The Iron's tag files reference/classify spells owned by the external spell provider and count as **zero new semantic magics**.

The Modrinth 1.7 changelog explicitly says Sound-school content was removed and moved to Tunes 'n Tomes. Do not count older FamiliarsLib Sound-school prose as current 1.7.x content.

### Black Arcana / Stage 07.07 boundary

No automatic FamiliarsLib bridge is created. The BA noetic runtime remains server-authoritative and revalidates through its canonical familiar-ownership boundary. A FamiliarsLib entity cannot be admitted merely because it is a familiar, tameable, spellcasting pet or nearby entity.

Provider-specific ownership integration remains **fail-closed** until a current exact-version seam is proven and deliberately adapted. The catalog evidence identifies provider-owned familiar state, but source↔physical exactness and a stable ownership contract are not closed strongly enough to promote a runtime adapter.

### License / clean-room

FamiliarsLib license evidence conflicts across source/publisher surfaces. No reuse conclusion is inferred. GTBC's SpellLib is likewise treated conservatively for factual publisher/physical evidence. Read-only factual audit only; no code/assets/text copied or adapted.

## Immediate predecessors

| Component | Phase / PR | Provider | Estado |
|---:|---|---|---|
| 60 | 2BL / #207 | `goety_cataclysm` | CANÔNICO; +52 semânticos; exact-artifact; fechamento durável em `main@d41fe957...`; validação final preservada por `main@43e343df...` / CI #2540 GREEN |
| 59 | 2BL / #207 | `goetyiron` | CANÔNICO; +14 semânticos; exact-artifact; fechamento durável em `main@d41fe957...`; validação final preservada por `main@43e343df...` / CI #2540 GREEN |
| 58 | 2BK / #204 | `ignissoulfires_spellbooks` | CANÔNICO; `ZERO_BRIDGE_INFRA`; +0 semântico; exact-SHA post-merge CI #2534 GREEN |
| 57 | 2BH / #198 | `goety` | CANÔNICO em `main@4fcc40aa...`; +361 semânticos; CI pós-merge #2524 GREEN |
| 56 | 2BG / #195 | `leylines` | CANÔNICO em `main@88f042f...`; +14 semânticos; CI pós-merge #2504 GREEN |
| 55 | 2BE / #189 | `cataclysm_spellbooks` | CANÔNICO em `main@cce7f517...`; HEAD auditado CI #2483 GREEN; CI pós-merge #2484 attempt 2 GREEN |
| 54 | 2BD / #186 | `alshanex_familiars` | CANÔNICO em `main@95ec538f...`; HEAD auditado CI #2464 GREEN; CI pós-merge #2465 GREEN |
| 53 | 2AY / #175 | `gtbcs_spell_lib` | CANÔNICO em `main@9a4e1cd...`; CI pós-merge #2421 GREEN |
| 52 | 2AX / #166 | `familiarslib` | CANÔNICO em `main@4238275...`; CI pós-merge #2337 GREEN |

## Próxima seleção

Phase 2BF / Somake, Phase 2BG / Leylines, Phase 2BH / Goety e Phase 2BL / Goety addons já foram reconciliadas no nível de evidência descrito acima. Não reiniciar esses fechamentos a partir de branches antigas.

Blockers atualmente **PARKED até existir input novo**:

- Not Enough Glyphs 4.6.1 — 39 registrations source-enabled permanecem `CONDITIONAL`; cada glyph usa config `SERVER` `not_enough_glyphs/<glyph>.toml` / `[general].enabled`, e nenhum conjunto implantado de world/server overrides está presente no repositório ou nos materiais físicos atualmente disponíveis;
- Gaze 1.1.7.1 — o registry exato e Soulward Shield já estão fechados; os 26 Spirit Rites permanecem `CONDITIONAL` somente porque o valor COMMON implantado de `disableGazeRites` não está disponível;
- Somake Spells 1.0.8-fix — o registry exato de 67 identidades está fechado, mas config efetiva de `enableSpellLockSystem` e survival acquisition/reachability completa continuam sem autoridade suficiente.

A próxima seleção deve escolher **outro componente ainda aberto** para o qual exista evidência current/exact capaz de reduzir incerteza de inventário ou de classificação. Defaults de provider, publisher prose ou branches preparatórias não substituem estado implantado. Se um candidato só puder avançar com navegação/material externo indisponível, registrar a pendência e passar ao próximo blocker seguro em vez de fabricar fechamento.

Os estados canônicos permanecem **1316 objetos semânticos mínimos / 60 de 100 componentes** até uma nova promoção sustentada por evidência.

## Regras

- presença/versão vêm da modlist/JAR atual;
- source-version correlation não implica JAR reproducibility;
- framework/library não vira spell provider;
- tag de spell externo não conta como spell novo;
- histórico Sound anterior à linha atual não conta no provider que deixou de possuí-lo;
- componente fechado não altera automaticamente a contagem semântica de magias;
- provider action reachability deve ser provada por registry/tree/input ou mecanismo equivalente, não por aparência de UI;
- familiar ownership precisa de seam provider-native comprovado;
- cliente envia intenção, nunca ownership authority;
- integração sem seam seguro e exato permanece fail-closed;
- Phase 3 permanece bloqueada até o catálogo provar lacunas reais e a cobertura semântica ser reconstruível.
