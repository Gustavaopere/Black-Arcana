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

- Phase 2AJ / PR #143 está canônica em `main@83a5cbf95e2e2eeb8c4e5e161aa2eb590b78712b`;
- cobertura canônica na criação da Phase 2AK: **38/100 = 38%**;
- esta revisão Phase 2AK fecha `emf_compat_iron_spells` como componente #39 ao limite exato de source-version disponível;
- o resultado **39/100 = 39%** só é canônico depois de reconciliação com a latest main, CI GREEN no HEAD reconciliado e merge;
- provider parcial não recebe ponto inteiro.

### Reconciliação física corrigida do denominador

A lista histórica possui 103 IDs. A comparação direta desses IDs contra a modlist física atual encontra:

- 98 IDs históricos ainda presentes;
- 5 ausentes reais: `ars_morph`, `morerelics`, `reliquary`, `vestis`, `woodwalkers_spellbooks`;
- 2 candidatos magic/cross-domain atuais adicionados depois da lista histórica: `soul_fire_d`, `reliquified_lenders_cataclysm_new_relics_fix`;
- denominador operacional: `103 - 5 + 2 = 100`.

Correção: `backportedspellbooks`, `crystal_chronicles` e `gtbcs_geomancy_plus` estão fisicamente presentes e não devem aparecer como removidos.

## Phase 2AK — EMF Compat: Iron's Spells 2.0.0

| Mod ID | Artefato físico | Estado da auditoria |
|---|---|---|
| `emf_compat_iron_spells` | `emf_compat_iron_spells_1.21.1_2.0.0.jar` | EXACT PHYSICAL VERSION + EXACT OFFICIAL SOURCE VERSION / CLIENT PRESENTATION COMPAT / 0 SPELLS / 0 GAMEPLAY REGISTRY / 5 JAVA CLASSES / 3 REQUIRED CLIENT MIXINS / 2 CONFIG KEYS / POSE SOURCE PRIORITY 10 / FIRST-PERSON EMF CONDITION / COMPONENT #39 CANDIDATE / BYTE-EQUIVALENCE + FULL-PACK RENDER QA FAIL-CLOSED |

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

Phase 2AK foi aberta sobre `main@83a5cbf95e2e2eeb8c4e5e161aa2eb590b78712b` após rechecagem de branches/PRs. Não havia branch nem PR equivalente para `emf_compat_iron_spells`.

Antes do merge, buscar `main` novamente e reconciliar qualquer avanço. CI anterior à última reconciliação não vale como evidência final.

## Próxima seleção após Phase 2AK

Selecionar somente depois de:

1. fetch da `main` mais recente;
2. confirmação do merge/CI da Phase 2AK;
3. verificação da modlist física atual;
4. pesquisa de PR/branch equivalente;
5. leitura do catálogo já canônico;
6. confirmação da versão exata e do melhor source/API/release aplicável.

Continuar preferindo componentes cuja superfície atual possa ser fechada sem inferência. `cataclysm_spellbooks`, `gaze`, `leylines` e `somakespells` continuam parciais sob a evidência atual.

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
- client presentation hook não é cast authority;
- registry/example object não vira spell por contagem;
- capabilities repacked mantêm provenance/namespace e não criam duplicata semântica automaticamente;
- integração sem hook seguro permanece fail-closed;
- Black Arcana não duplica mana, casting, cooldown, targeting, summon lifecycle, proc pipeline, presentation adapter ou world mutation de provider;
- source-family label ou Java symbol não deve ser confundido com registry ID sem evidência;
- provider parcial continua zero até inventário atual fechar ao teto de evidência aceito;
- Phase 3 continua bloqueada até o catálogo/deduplicação provar lacunas reais.

## Histórico

Para os 103 candidatos e respectivos estados do checkpoint de 2026-09-07, consultar `PROVIDER-AUDIT-QUEUE-2026-09-07.md`. Antes de retomar qualquer linha daquele snapshot, reconciliar presença e versão contra a modlist física atual.
