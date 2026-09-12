# Fila operacional de auditoria dos providers mágicos

## Autoridade atual

O snapshot imediatamente anterior está preservado byte-for-byte em [`PROVIDER-AUDIT-QUEUE-PRE-PHASE2AX.md`](./PROVIDER-AUDIT-QUEUE-PRE-PHASE2AX.md).

- Minecraft 1.21.1
- NeoForge `21.1.248`
- modlist física: **595 entradas top-level**
- SHA-1 da modlist: `7aaece7acbfb07ba4d0c66029042f36c50d046f0`
- `main` canônica após Phase 2BF final evidence / PR #193: `91fe79e8479f7c82a7e922f64d4806a3e7abafe1`; durable PR #192 HEAD `85b15aec9faf395cef5460d06a17be58ccd16af8` passou CI #2490 e merge `cc4cfc1d740f7714188e25a3586d8b43bb5eb969` passou CI #2491; final-evidence PR #193 foi mergeado como `91fe79e8479f7c82a7e922f64d4806a3e7abafe1` e o exact-SHA post-merge CI #2493 ficou GREEN;
- jarjar/internal não conta como provider top-level

## Métricas separadas

### Cobertura semântica de magias — métrica principal para o usuário

A reconstrução canônica após Phase 2BE fecha **874 objetos mágicos semânticos** com o inventário exato Cataclysm 1.1.13. O denominador global continua incompleto e nenhuma porcentagem semântica é declarada.

A correção de contagem imediatamente anterior ao fechamento Alshanex continua sendo **Werewolves Leap +1**: a source exata 2.0.3.3 prova `LEAP` como `ActionSkill`, nó `SURVIVAL31` conectado à árvore normal e input dedicado processado pelo servidor/provider. Portanto Leap deixa de ser `CONDITIONAL` e Werewolves passa de 7 para 8 ações semânticas contadas. `hide_name` continua excluído como presentation-only; `no_leap_cooldown` continua sendo uma questão separada de refinement/acquisition.

GTBC's SpellLib 2.2.0 adiciona **0 magias semânticas independentes**. É infraestrutura de biblioteca/API compartilhada; atributos e helpers reutilizáveis não são identidades de spell próprias.

A reconciliação Gaze 1.1.7.1 também adiciona **+0** ao mínimo estrito: publisher e artefato físico fecham identidade/escala, mas o registry granular atual e a reachability por objeto permanecem abertos.

- delta semântico Werewolves: **+1**;
- delta semântico GTBC SpellLib: **+0**;
- delta semântico Gaze 1.1.7.1: **+0**;
- delta semântico Alshanex 4.0.3: **+18**;
- delta semântico Cataclysm: Spellbooks 1.1.13: **+59**;
- delta semântico Somake 1.0.8-fix Phase 2BF: **+0** (`67 exact registry`, reachability/config efetivo ainda `CONDITIONAL`);
- mínimo estrito global canônico: **874**;
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
- cobertura canônica de componentes após Phase 2BE: **55/100 = 55%**; componente #55 fechado pelo PR #189 com CI pré/pós-merge verde no SHA exato.

O valor 55/100 nunca substitui a métrica semântica de magias.

## Phase 2BG — Leyline Spellbooks 1.0.3 — promotion candidate

| Mod ID | Artefato físico | Estado |
|---|---|---|
| `leylines` | `leylines-1.0.3.jar` | EXACT PHYSICAL / EXACT CURSEFORGE FILE / EXACT HASH-MATCHED ARTIFACT AUDIT / 14 UNCONDITIONAL REGISTERED SPELL IDENTITIES / CURRENT HOST ELIGIBILITY CLOSED / +14 CANDIDATE SEMANTIC DELTA / CANDIDATE #56 |

Evidence: non-merge PR #194; primary `34666436710 / 10289437099`; reachability `34666652534 / 10289292617`; school/loot gate `34667641655 / 10289184487`; exact Iron's 3.16.3 host source `e4056af90302d37eb1739f5ff05020b020e6e252`. Canonical totals remain 874 / 55/100 until durable merge and post-merge CI. Candidate totals are 888 / 56/100.

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
- no upstream implementation/assets copied or adapted; balance/acquisition/runtime/API seams remain fail-closed where not separately proven.

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

## Reconciliação Gaze 1.1.7.1 — PR #180 — parcial, sem incremento de cobertura

| Mod ID | Artefato físico | Estado |
|---|---|---|
| `gaze` | `gaze-1.1.7.1.jar` | EXACT PHYSICAL / EXACT CURSEFORGE FILE / EXACT MODRINTH VERSION / ARR / PUBLIC SCALE + NAMED 1.1.7 LINEAGE / COMPLETE CURRENT REGISTRY OPEN / +0 STRICT SEMANTIC DELTA / POST-MERGE CI GREEN |

### Evidence boundary

- physical SHA-1 `a8cb3190bde157f78160ce65c202ce2d47fb2041`;
- CurseForge project/file `1273454 / 7261638`;
- Modrinth project/version `NlvaJ5WE / od4ltbRo`;
- current publisher scale: 2 Geas, a set of Rites, 6 weapons, 8 runes, 5 Curios and Spirit-Channel pouch;
- 1.1.7 lineage names current-line Geas/Rites/runes/items, while 1.1.7.1 publishes only a narrow patch delta;
- no complete 1.1.7.1 registry, object-level reachability table or stable addon API was proven;
- no code/assets/text copied or adapted; unsupported internals remain fail-closed.

Gaze therefore leaves the global denominator open, but should not be selected again merely to repeat the same publisher evidence. Reopen it only when new exact/current evidence can materially close registry, reachability, acquisition or runtime seams.

## Phase 2AY — GTBC's SpellLib 2.2.0 — canonical #53

| Mod ID | Artefato físico | Estado |
|---|---|---|
| `gtbcs_spell_lib` | `gtbcs_spell_lib-2.2.0-1.21.1.jar` | EXACT PHYSICAL / EXACT PUBLISHER RELEASE / SHARED LIBRARY+API INFRASTRUCTURE / 0 INDEPENDENT SEMANTIC SPELLS / #53 CANONICAL / POST-MERGE CI GREEN |

### Evidence boundary

- physical version `2.2.0`, SHA-1 `36cce8ab3117e89ae992a84a566d596709db2ffe`;
- CurseForge project/file `1194714 / 8824651`;
- publisher defines SpellLib as shared library/API infrastructure with no standalone gameplay of its own;
- 2.2.0 publisher delta adds Healing Received, Damage Taken and Summon Health attributes;
- reusable `AdvancedSpell`, imbuement, Curio, trade, particle and summon surfaces are infrastructure, not proof of provider-owned spell identities;
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
| 55 | 2BE / #189 | `cataclysm_spellbooks` | CANÔNICO em `main@cce7f517...`; HEAD auditado CI #2483 GREEN; CI pós-merge #2484 attempt 2 GREEN |
| 54 | 2BD / #186 | `alshanex_familiars` | CANÔNICO em `main@95ec538f...`; HEAD auditado CI #2464 GREEN; CI pós-merge #2465 GREEN |
| 53 | 2AY / #175 | `gtbcs_spell_lib` | CANÔNICO em `main@9a4e1cd...`; CI pós-merge #2421 GREEN |
| 52 | 2AX / #166 | `familiarslib` | CANÔNICO em `main@4238275...`; CI pós-merge #2337 GREEN |
| 51 | 2AW / #161 | `apotheoticcreation` | CANÔNICO; ver nota histórica de GameTest no coverage/checkpoint |
| 50 | 2AV / #160 | `apotheosis` | CANÔNICO |
| 49 | 2AU / #158 | `apothic_enchanting` | CANÔNICO |

## Próxima seleção

Phase 2BF / Somake está encerrada e documentada; Phase 2BG / Leylines está em promotion candidate neste branch. A próxima seleção após o fechamento Phase 2BG deve escolher apenas um blocker ainda aberto com evidência nova capaz de reduzir incerteza, não repetir publisher prose já catalogada.

Prioridades ainda abertas:

- Goety 3.1.4 — exact JAR/source equivalence, Focus reachability/dedup e ritual identities permanecem abertas;
- Not Enough Glyphs 4.6.1 — 39 registrations source-enabled continuam condicionais até reconciliação da config efetiva do pack.

Gaze 1.1.7.1 continua com denominador granular aberto, mas fica **PARKED** até surgir evidência exata/current nova para registry, reachability, acquisition ou runtime. O checkpoint já mergeado não deve ser refeito.

Se nenhum desses inputs novos estiver disponível, o estado correto é manter os blockers fail-closed em vez de fabricar fechamento ou avançar Phase 3.

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