# Fila operacional de auditoria dos providers mágicos

## Autoridade atual

Este arquivo é a fila operacional corrente. O snapshot detalhado de 2026-09-07 permanece preservado em [`PROVIDER-AUDIT-QUEUE-2026-09-07.md`](./PROVIDER-AUDIT-QUEUE-2026-09-07.md).

Autoridade física deste checkpoint:

- Minecraft 1.21.1;
- NeoForge `21.1.248`;
- modlist física mais recente: **595 entradas top-level**;
- SHA-1 da modlist: `7aaece7acbfb07ba4d0c66029042f36c50d046f0`;
- dependências internas/jarjar não contam como providers top-level.

O snapshot histórico de 2026-09-07 usava 612 entradas / 103 candidatos e não é mais autoridade de presença, versão nem denominador.

## Cobertura global

Ver [`CATALOG-COVERAGE-CURRENT.md`](./CATALOG-COVERAGE-CURRENT.md).

- Phase 2AL / PR #145 está canônica em `main@433233164f61bbf6b6d5cb8aa9625cf286a79a23`;
- cobertura canônica na criação da Phase 2AM: **40/100 = 40%**;
- esta revisão Phase 2AM fecha `reliquified_lenders_cataclysm_new_relics_fix` como componente #41 ao limite exato de evidência física/publisher disponível;
- o resultado **41/100 = 41%** só é canônico depois de reconciliação com a latest main, CI GREEN no HEAD reconciliado e merge;
- provider parcial não recebe ponto inteiro.

### Reconciliação física corrigida do denominador

A lista histórica possui 103 IDs. A comparação direta desses IDs contra a modlist física atual encontra:

- 98 IDs históricos ainda presentes;
- 5 ausentes reais: `ars_morph`, `morerelics`, `reliquary`, `vestis`, `woodwalkers_spellbooks`;
- 2 candidatos magic/cross-domain atuais adicionados depois da lista histórica: `soul_fire_d`, `reliquified_lenders_cataclysm_new_relics_fix`;
- denominador operacional: `103 - 5 + 2 = 100`.

Correção: `backportedspellbooks`, `crystal_chronicles` e `gtbcs_geomancy_plus` estão fisicamente presentes e não devem aparecer como removidos.

## Phase 2AM — Reliquified L_Ender's Cataclysm New Relics Fix 1.0.2

| Mod ID | Artefato físico | Estado da auditoria |
|---|---|---|
| `reliquified_lenders_cataclysm_new_relics_fix` | `reliquified-lenders-cataclysm-new-relics-fix-1.0.2.jar` | EXACT PHYSICAL+PUBLISHER 1.0.2 / RELICS 0.10→0.12 COMPATIBILITY BRIDGE / 5 EXISTING RELICS IN PUBLISHED SCOPE / 8 PUBLISHED REPAIR FAMILIES / 0 NEW SEMANTIC RELIC IDS / 0 PUBLISHED STANDALONE SPELL IDS / 1.0.2 BASE-CLASS-ONLY TRANSFORM SCOPE / COMPONENT #41 CANDIDATE / EXACT SOURCE+MIXIN+PACKET+PERSISTENCE INTERNALS FAIL-CLOSED |

### Evidence boundary

- Physical SHA-1: `9d4710e665ec74af917bb9f5f819154ca9f74ca0`.
- CurseForge project/file: `1665965 / 8778365`, exact 1.0.2 release dated 2026-08-31.
- Publisher: NeoForge 1.21.1, Client & Server, All Rights Reserved.
- Publisher defines the component as a bridge allowing Reliquified L_Ender's Cataclysm `0.1.1` to work with newer Relics `0.12` after old Relics `0.10` classes/methods changed or disappeared.
- Exact physical required stack includes Relics `0.12.8`, Curios `9.5.1+1.21.1`, OctoLib `0.6.2`, L_Ender's Cataclysm `3.33` and Reliquified L_Ender's Cataclysm `0.1.1`.
- Publisher names exactly five fixed existing relics: Void Cloak, Scouring Eye, Void Vortex in Bottle, Vacuum Glove and Void Bubble.
- Publisher lists repair of `IRelicItem` startup/API breakage, RelicTemplate conversion, Curios/modifiers, stats/levels/ranks/cooldowns/XP, legacy active abilities, player-motion networking, ability order/progression values and descriptions/tooltips.
- Exact file 1.0.2 changelog narrows the bridge to the addon's base class and prevents global `RelicItem` modification.
- No exact public source for the fix was located; exact mixin classes/counts/targets, bytecode transforms, packet schema and persistence keys remain fail-closed.
- Original addon's current public `1.21.1` branch declares `mod_version=0.2`, so it is not substituted for the physical target addon `0.1.1` or for missing fix source.

### Provider authority

- Relics owns current framework/rank/level/XP/cooldown infrastructure.
- Reliquified L_Ender's Cataclysm owns the five relic identities and content behavior.
- Curios owns equip-slot infrastructure.
- this fix owns only old-addon→new-Relics compatibility translation.
- Black Arcana does not duplicate template/modifier/progression/cooldown/ability/network adaptation and retains its own canonical magic runtime.
- RPG Skill Tree receives no relic or magic runtime authority from this compatibility component.

## Phase 2AL — `efiscompat` 3.1.0 — canonical predecessor

| Mod ID | Artefato físico | Estado da auditoria |
|---|---|---|
| `efiscompat` | `efiscompat-3.1.0.jar` | CANÔNICO VIA PR #145 / EXACT PHYSICAL VERSION + EXACT OFFICIAL SOURCE VERSION PIN / EPIC FIGHT↔IRON'S CASTING-INTERACTION+ANIMATION COMPAT / 0 SPELLS / 28 JAVA FILES / 35 ANIMATION ACCESSORS / 12 REQUIRED MIXINS (6 CLIENT + 6 COMMON) / 6 CONFIG KEYS / DATA-DRIVEN SPELL-ANIMATION MAP / IRON'S PRECAST+CANCEL RECONCILIATION / COMPONENT #40 / LICENSE-CONFLICT + BYTE/HOST/FULL-PACK QA FAIL-CLOSED |

### Evidence boundary

- Physical SHA-1: `4250e1c65732d70d1091cc50b84a91b6ed5b2b3f`.
- CurseForge project/file: `1109064 / 8372294`, release `3.1.0` dated 2026-07-05.
- Official exact-version source: `domanhthang2110/efiscompat@b4b58aff86e707420fac8a7c29fe647d7f5aaac4` on branch `1.21.1`.
- The pinned commit is titled `Fixed dedicated server crash` and changes `mod_version=3.0.0` to `3.1.0`.
- Exact source metadata: Minecraft 1.21.1, Java 21, NeoForge baseline 21.1.219, Iron's baseline 3.15.6.
- Generated runtime metadata requires BOTH-side Epic Fight `[21,)` and Iron's `[1.21.1-3.15.0,)`.
- Physical pack uses Epic Fight `21.17.3.1` and Iron's `1.21.1-3.16.3`; declared ranges are satisfied, but exact mixin/API/event-order parity remains runtime QA.
- Standalone provider spell count is **0**; Iron's `SpellRegistry` is queried only to resolve host spells for animation selection.
- Exact source surface contains 28 Java files, 35 provider animation accessors, 12 required mixins and 6 common config keys.
- `SpellAnimationLoader` provides a reloadable 9-role chant/cast/continuous + staff-side mapping with default fallback.
- Server-relevant compatibility includes an Iron's pre-cast veto from Epic Fight stun/recent-action state and cancellation of active Iron's casts from Epic Fight skill/guard/dodge paths.
- `MixinComboBasicAttack` targets `com.p1nero.invincible.skill.ComboBasicAttack`; physical target owner/presence is not established from the top-level modlist and remains fail-closed QA.
- License metadata conflict is preserved: CurseForge labels MIT, exact source metadata declares `GNU GPLv3`, and no root `LICENSE` file was observed at the source pin.
- Exact source-version pin is not promoted to byte-for-byte source/JAR identity without reproducibility evidence.

### Provider authority

- Iron's owns spells, cast state, mana, spell effects and cooldown semantics.
- Epic Fight owns combat action/stun/skill/animation state.
- `efiscompat` owns only the reconciliation policy and animation compatibility around those providers.
- Black Arcana must not duplicate the same Iron's↔Epic Fight interruption/animation layer or route BA-native spells through Iron's to inherit it.
- Black Arcana retains canonical casting/cost/target/effect/cooldown, Corruption, Strain, Arcane Danger, ritual/hazard and `WorldEffectPolicy` authority.
- RPG Skill Tree receives no magic runtime authority from this compat.

## Phase 2AK — EMF Compat: Iron's Spells 2.0.0 — canonical predecessor

| Mod ID | Artefato físico | Estado da auditoria |
|---|---|---|
| `emf_compat_iron_spells` | `emf_compat_iron_spells_1.21.1_2.0.0.jar` | CANÔNICO VIA PR #144 / EXACT PHYSICAL VERSION + EXACT OFFICIAL SOURCE VERSION / CLIENT PRESENTATION COMPAT / 0 SPELLS / 0 GAMEPLAY REGISTRY / 5 JAVA CLASSES / 3 REQUIRED CLIENT MIXINS / 2 CONFIG KEYS / POSE SOURCE PRIORITY 10 / FIRST-PERSON EMF CONDITION / COMPONENT #39 / BYTE-EQUIVALENCE + FULL-PACK RENDER QA FAIL-CLOSED |

### Evidence boundary

- Physical SHA-1: `515b545870fce128bbf01a0ccacdd19566ed3b22`.
- Official source revision: `victorkozhokin/emf-compat@79d730a9d02275b7d721967c75f5f22dc815d9dc`.
- Exact NeoForge 1.21.1 subproject metadata declares `mod_version=2.0.0`, Java 21 and `mod_license=GNU GPL 3.0`.
- Complete addon Java surface: `EMFCompatIronSpellsMod`, `IronSpellsCompat`, `PlayerModelMixin`, `PlayerRendererMixin`, `EMFAnimationPauseHandlerMixin`.
- Required mixin manifest contains exactly the three client mixins above and no common/server mixins.
- Config keys: `ironspells.enabled` and `ironspells.bodyFollowArms`, both default true.
- Casting state is consumed from Iron's client data only; the compat does not originate or authorize a cast.
- Source build baseline: NeoForge 21.1.230, Iron's 3.15.6, EMF 3.3.2.
- Runtime metadata requires Core >=2.0.0, Iron's >=3.15.0 and EMF >=3.3.2, client-side. Physical pack uses Core 2.0.0, Iron's 3.16.3 and EMF 3.3.5.
- Some public web file indices remain stale at 1.0.0; physical artifact + exact publisher source metadata are used as stronger version evidence.
- Exact source version is not promoted to byte-for-byte source/JAR identity without reproducibility evidence.

### Provider authority

- Iron's owns casting state, spells, mana, cooldowns and remote synced cast state.
- EMF Compat: Iron's owns only the client pose compatibility adapter.
- EMF Compat Core / EMF own their shared presentation APIs/runtime.
- Black Arcana must not treat EMF pose state or client casting state as server authority and must not duplicate this Iron's-specific pose adapter.
- RPG Skill Tree receives no progression authority from this visual layer.

## Phase 2AJ — Ace's Spell Utils 1.2.7.2 — canonical predecessor

| Mod ID | Artefato físico | Estado da auditoria |
|---|---|---|
| `aces_spell_utils` | `aces_spell_utils-1.2.7.2-1.21.1.jar` | CANÔNICO VIA PR #143 / EXACT PHYSICAL VERSION + EXACT OFFICIAL SOURCE VERSION PIN / API+LIBRARY PROVIDER / 0 STANDALONE SPELL REGISTRATIONS / 3 SCHOOLS / 19 ATTRIBUTES / 3 DAMAGE TYPES / 14 TAGS / 8 RARITIES / 27 EXAMPLE ITEM REGISTRATIONS / 8 S2C VFX PAYLOADS / 2 REQUIRED MIXINS / 5 CONFIG VALUES / COMPONENT #38 / HOST-VERSION+BYTE-EQUIVALENCE QA FAIL-CLOSED |

### Evidence boundary

- Physical SHA-1: `8cbcd535a0b19bef49504c0b5ecafcbcd1cb1cca`.
- CurseForge project/file: `1299492 / 8789930`, exact 1.2.7.2 release dated 2026-09-02.
- Official exact-version source: `AceTheEldritchKing/Aces_Spell_Utils@a0b2f4c2fcfa938c8e47239279c77c2ef82647ac`.
- Source `gradle.properties` declares exactly `mod_version=1.2.7.2-1.21.1`.
- No `registerSpell(...)` call and no provider standalone spell-registry registration surface were found: exact provider spell count is **0**.
- School registry IDs are `aces_spell_utils:ritual`, `aces_spell_utils:hydro`, `aces_spell_utils:technomancy`.
- Publisher display language may call Ritual `Occult`; exact registry remains `ritual`.
- Source Java supplier `ABYSSAL` actually registers `hydro`; do not fabricate an Abyssal school.
- Source targets NeoForge 21.1.230 / Iron's 3.11.0 while pack uses NeoForge 21.1.248 / Iron's 3.16.3. Exact host-runtime parity remains QA/fail-closed.
- Exact source-version pin is not promoted to byte-for-byte source/JAR identity without reproducibility evidence.

### Provider authority

- Iron's owns underlying spell casting, mana and cooldown authority.
- Ace's owns shared attributes/proc helpers, API classes, mixins, attachment, VFX transport and example runtime it registers.
- consuming addons own concrete spells/entities/items built on the Ace's API.
- Black Arcana does not duplicate these pipelines and retains its own canonical casting, Corruption, Strain, Arcane Danger and WorldEffectPolicy.
- RPG Skill Tree remains progression/mastery only through real contracts.

## Phase 2AI — canonical predecessor, zero delta

| Mod ID | Artefato físico | Estado |
|---|---|---|
| `somakespells` | `somakespells-1.0.8-1.21.1-fix.jar` | CANÔNICO VIA PR #141 / EXACT PHYSICAL+RELEASE IDENTITY / OFFICIAL 1.0.x RELEASE SURFACE AUDITED / PUBLISHER `OVER 50` SCALE / COMPLETE CURRENT SPELL REGISTRY NOT AVAILABLE / EXACT SOURCE+API NOT LOCATED / AQUA↔T.O RUNTIME QA BLOCKED / ZERO COVERAGE DELTA / FAIL-CLOSED |

## Phase 2AH — canonical predecessor

| Mod ID | Artefato físico | Estado |
|---|---|---|
| `monstersspellbooks` | `monstersspellbooks-0.0.16.3.jar` | CANÔNICO VIA PR #140 / EXACT PHYSICAL+RELEASE 0.0.16.3 / 98 SPELL REGISTRATIONS CLOSED SEMANTICALLY / NECRO+AERO SCHOOLTYPES OBSERVED IN SOURCE ONLY / AERO 0 SPELL REGISTRATIONS + INSTALLED AERO STATE UNVERIFIED AFTER 0.0.16.3 CLEANUP / EXACT BINARY NUMERICAL/API INTERNALS FAIL-CLOSED |

## Phase 2AG — canonical predecessor

| Mod ID | Artefato físico | Estado |
|---|---|---|
| `ars_n_spells` | `ars_n_spells-3.3.2.jar` | CANÔNICO VIA PR #137 / EXACT PHYSICAL+RELEASE 3.3.2 / OFFICIAL NEOFORGE SOURCE BASELINE 3.3.0 / 5 RITUAIS / 5 MANA MODES / SPELL LOOM+CARRIERS / 8 TRANSPORT PROXIES, 0 SPELLS SEMÂNTICOS INDEPENDENTES |

## Phase 2AF — canonical predecessor

| Mod ID | Artefato físico | Estado |
|---|---|---|
| `not_enough_glyphs` | `not_enough_glyphs-1.21.1-4.6.1.jar` | CANÔNICO VIA PR #135 / SOURCE-PINNED 4.6.1 / 40 REGISTROS CONDICIONAIS / 39 SOURCE-ENABLED / 4 FORMS + 36 EFFECTS / BINDER 25 STORAGE + 10 CASTER / 13 PERKS |

## Concorrência — não colidir

Phase 2AM foi aberta sobre `main@433233164f61bbf6b6d5cb8aa9625cf286a79a23` após rechecagem de branches/PRs. Não havia branch nem PR equivalente para `reliquified_lenders_cataclysm_new_relics_fix`.

PRs antigos de Ars permanecem concorrência separada e não são usados como autoridade contra a main mais recente.

Antes do merge, buscar `main` novamente e reconciliar qualquer avanço. CI anterior à última reconciliação não vale como evidência final.

## Próxima seleção após Phase 2AM

Selecionar somente depois de:

1. fetch da `main` mais recente;
2. confirmação do merge/CI da Phase 2AM;
3. verificação da modlist física atual;
4. pesquisa de PR/branch equivalente;
5. leitura do catálogo já canônico;
6. confirmação da versão exata e do melhor source/API/release aplicável.

`soul_fire_d` permanece como o outro candidato atual adicionado ao denominador e ainda exige classificação/fechamento em fase própria. Continuar preferindo componentes cuja superfície atual possa ser fechada sem inferência. `cataclysm_spellbooks`, `gaze`, `leylines` e `somakespells` continuam parciais sob a evidência atual.

## Providers parcialmente fechados — não contam como concluídos

Exemplos atuais:

- `leylines` — nomes públicos parciais; inventário total atual não verificado;
- `somakespells` — exact artifact/release e release-line auditados, mas inventário granular atual ainda não fechado;
- `cataclysm_spellbooks` — artefato instalado 1.1.13 sem source público exato equivalente já fechado;
- `gaze` — superfície pública auditada, mas registry/source-JAR exato ainda não fechado.

## Regras de fila

- presença/versão vêm da modlist/JAR atual, não do snapshot histórico;
- README preparatório, guia lido ou branch antiga não equivale a catálogo canônico;
- source público de versão diferente não autoriza promover internals da versão instalada;
- exact source-version pin não equivale automaticamente a byte-for-byte JAR reproducibility;
- library/API ou compat provider pode fechar com zero spells se zero registro próprio for demonstrado e suas superfícies reais estiverem inventariadas;
- compatibility bridge pode fechar semanticamente no publisher evidence ceiling quando o escopo público atual é explicitamente bounded e nenhuma identidade nova é atribuída, mantendo internals não publicados fail-closed;
- client presentation hook não é cast authority;
- cross-provider cast cancellation/reconciliation não vira segundo cast authority;
- registry/example/animation/compatibility object não vira spell por contagem;
- capabilities repacked mantêm provenance/namespace e não criam duplicata semântica automaticamente;
- integração sem hook seguro permanece fail-closed;
- Black Arcana não duplica mana, casting, cooldown, targeting, summon lifecycle, proc pipeline, relic migration/settlement, presentation adapter ou world mutation de provider;
- source-family label ou Java symbol não deve ser confundido com registry ID sem evidência;
- provider parcial continua zero até inventário atual fechar ao teto de evidência aceito;
- Phase 3 continua bloqueada até o catálogo/deduplicação provar lacunas reais.

## Histórico

Para os 103 candidatos e respectivos estados do checkpoint de 2026-09-07, consultar `PROVIDER-AUDIT-QUEUE-2026-09-07.md`. Antes de retomar qualquer linha daquele snapshot, reconciliar presença e versão contra a modlist física atual.
