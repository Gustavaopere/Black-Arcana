#!/usr/bin/env python3
from pathlib import Path
import re


def read(path):
    return Path(path).read_text(encoding='utf-8')


def write(path, text):
    Path(path).write_text(text, encoding='utf-8')


def replace_once(text, old, new, label):
    count = text.count(old)
    assert count == 1, f'{label}: expected exactly 1 match, got {count}'
    return text.replace(old, new, 1)


def regex_once(text, pattern, repl, label, flags=0):
    out, count = re.subn(pattern, repl, text, count=1, flags=flags)
    assert count == 1, f'{label}: expected exactly 1 regex match, got {count}'
    return out

# Semantic ledger
p = 'wiki/modpack-catalog/meta/SEMANTIC-MAGIC-COVERAGE.md'
s = read(p)
phase = '''## Phase 2BJ semantic promotion — Gaze 1.1.7.1 exact artifact

Exact hash-matched Gaze 1.1.7.1 evidence closes one current Gaze-owned Iron's standalone spell identity, **Soulward Shield**, whose optional `irons_spellbooks` provider gate is satisfied by the physical pack. The same exact artifact closes 26 player-facing Gaze Spirit Rite identities, but their registration is suppressed when the resolved COMMON config `disableGazeRites=true`; the deployed value is unavailable, so those 26 remain `CONDITIONAL`. Two Gaze `GeasEffectType` identities and eight rune items remain excluded by the existing metric definition.

Isolated NON-MERGE PR #201 audited exact HEAD `2f4ff6536663b1c629a6a5ea92416765bea17b1e`; final evidence run `34676660467` was GREEN and published artifact `10292013626` with digest `sha256:fb69f353b672f7c8ec7b470c454d24d1c3110cb996a250076a16d2b053f23f71`. Phase 2BJ therefore contributes **+1 `COUNTED_EXACT`**, moves the Iron's ecosystem subtotal to **542**, and moves the strict reconstructible minimum to **1250**. Gaze remains an open provider component, so component coverage stays **57/100**. Runtime/config/balance and provider-owned settlement remain separate fail-closed gates.

'''
s = replace_once(s, '## Phase 2BH canonical — Goety 3.1.4\n', phase + '## Phase 2BH canonical — Goety 3.1.4\n', 'semantic insert phase')
s = replace_once(s,
    '**1249 semantic magic objects are currently reconstructible from canonical provider records after Phase 2BH.**',
    '**1250 semantic magic objects are currently reconstructible from canonical provider records after Phase 2BJ.**',
    'semantic current minimum')
old_family = '''- Ars ecosystem: **199**;
- Iron's ecosystem and spell-content addons: **541**;
- Eidolon: Repraised: **42**;
- Vampirism/Bloodlines/Werewolves supernatural action layer: **55**;
- Hexalia ritual/infusion layer: **25**;
- Malum Spirit Rite layer: **26**;
- Goety Focus + ritual layer: **361**;
- total: `199 + 541 + 42 + 55 + 25 + 26 + 361 = 1249`.'''
new_family = '''- Ars ecosystem: **199**;
- Iron's ecosystem and spell-content addons: **542**;
- Eidolon: Repraised: **42**;
- Vampirism/Bloodlines/Werewolves supernatural action layer: **55**;
- Hexalia ritual/infusion layer: **25**;
- Malum Spirit Rite layer: **26**;
- Goety Focus + ritual layer: **361**;
- total: `199 + 542 + 42 + 55 + 25 + 26 + 361 = 1250`.'''
s = replace_once(s, old_family, new_family, 'semantic family arithmetic')
leyline = "| [Leyline Spellbooks](../providers/leyline-spellbooks/README.md) | 1.0.3 | 14 | `COUNTED_EXACT` | exact hash-matched JAR closes 14 unconditional `AbstractSpell` registrations; no provider-specific spell lock/conditional registration gate is present; generic Iron's host config remains separate runtime QA |\n"
gaze_row = "| [Gaze](../providers/gaze/README.md) | 1.1.7.1 | 1 | `COUNTED_EXACT` | exact hash-matched artifact closes one Gaze-owned Iron's `AbstractSpell`, Soulward Shield; physical Iron's satisfies the provider gate; 26 Spirit Rites remain config-conditional and 2 Geas + 8 rune items are metric-excluded |\n"
s = replace_once(s, leyline, leyline + gaze_row, 'semantic counted gaze row')
s = replace_once(s, '| **Strict total** |  | **1249** |  |  |', '| **Strict total** |  | **1250** |  |  |', 'semantic strict total row')
old_gaze = '| [Gaze](../providers/gaze/README.md) 1.1.7.1 | publisher states **2 Geas** plus a new set of Rites | `LOWER_BOUND / OPEN` | rite registry and complete IDs/names are not published; exact source/JAR extraction pending |'
new_gaze = '| [Gaze](../providers/gaze/README.md) 1.1.7.1 rites | exact hash-matched artifact closes **26 player-facing Spirit Rite identities** | `CONDITIONAL / EXACT REGISTRY CLOSED / +0 RITES` | exact provider control flow suppresses the rite surfaces when resolved COMMON config `disableGazeRites=true`; deployed pack value is unavailable, so source default `false` is not substituted |'
s = replace_once(s, old_gaze, new_gaze, 'semantic conditional gaze row')
old_next = '''1. current-pack config closure for Not Enough Glyphs 4.6.1 and other remaining conditional glyph/action rows;
2. exact Gaze 1.1.7.1 rites/Geas inventory only when materially new exact evidence becomes available;
3. exact Ignis Soulfires: Spellbooks 1.1.0 semantic registry inventory;
4. Goety Iron 3.1 and Goety Cataclysm 1.21.1-1.8.2 exact semantic inventories without duplicating base-Goety ownership;
5. remaining open provider inventories that can materially reduce the denominator blocker.'''
new_next = '''1. exact Ignis Soulfires: Spellbooks 1.1.0 semantic registry inventory;
2. Goety Iron 3.1 and Goety Cataclysm 1.21.1-1.8.2 exact semantic inventories without duplicating base-Goety ownership;
3. obtain deployed config evidence for input-blocked conditional rows, especially Not Enough Glyphs 4.6.1 and Gaze 1.1.7.1 Rites;
4. remaining open provider inventories that can materially reduce the denominator blocker.'''
s = replace_once(s, old_next, new_next, 'semantic next order')
write(p, s)

# Coverage current: only current-state statements; historical Phase 2BH figures remain unchanged.
p = 'wiki/modpack-catalog/meta/CATALOG-COVERAGE-CURRENT.md'
s = read(p)
s = replace_once(s,
    'The reconstructible semantic ledger lives in [`SEMANTIC-MAGIC-COVERAGE.md`](./SEMANTIC-MAGIC-COVERAGE.md). Phase 2BH canonically closes a **strict counted minimum of 1249 semantic magic objects** from provider records that meet the ledger\'s inclusion rule. The global denominator is still incomplete and no semantic percentage is declared.',
    'The reconstructible semantic ledger lives in [`SEMANTIC-MAGIC-COVERAGE.md`](./SEMANTIC-MAGIC-COVERAGE.md). Phase 2BJ raises the **strict counted minimum to 1250 semantic magic objects** from provider records that meet the ledger\'s inclusion rule. The global denominator is still incomplete and no semantic percentage is declared.',
    'coverage current total')
old_latest = 'The latest semantic promotion is **Goety +361**. Exact hash-matched 3.1.4 artifact evidence closes 123 active/acquirable Focus actions and 238 available distinct non-Focus ritual actions after semantic deduplication and physical-provider condition filtering. Runtime/API/balance and provider-owned settlement remain separate fail-closed gates. See [`../providers/goety/EXACT-3.1.4-ARTIFACT-AUDIT.md`](../providers/goety/EXACT-3.1.4-ARTIFACT-AUDIT.md).'
new_latest = '''The latest semantic promotion is **Gaze +1**. Exact hash-matched 1.1.7.1 artifact evidence closes one Gaze-owned Iron's standalone spell, Soulward Shield, with the optional Iron's provider gate satisfied by the physical pack. The same artifact closes 26 player-facing Spirit Rite identities, but they remain `CONDITIONAL` because the deployed COMMON `disableGazeRites` value is unavailable; two Geas effect types and eight rune items are metric-excluded. See [`../providers/gaze/EXACT-1.1.7.1-ARTIFACT-AUDIT.md`](../providers/gaze/EXACT-1.1.7.1-ARTIFACT-AUDIT.md).

The preceding semantic promotion is **Goety +361**. Exact hash-matched 3.1.4 artifact evidence closes 123 active/acquirable Focus actions and 238 available distinct non-Focus ritual actions after semantic deduplication and physical-provider condition filtering. Runtime/API/balance and provider-owned settlement remain separate fail-closed gates. See [`../providers/goety/EXACT-3.1.4-ARTIFACT-AUDIT.md`](../providers/goety/EXACT-3.1.4-ARTIFACT-AUDIT.md).'''
s = replace_once(s, old_latest, new_latest, 'coverage latest promotion')
s = replace_once(s,
    'Therefore:\n\n- semantic numerator delta from Goety 3.1.4 exact closure: **+361**;',
    'Therefore:\n\n- semantic numerator delta from Gaze 1.1.7.1 exact closure: **+1**;\n- semantic numerator delta from Goety 3.1.4 exact closure: **+361**;',
    'coverage therefore gaze')
s = replace_once(s, '- strict reconstructible semantic minimum: **1249**;', '- strict reconstructible semantic minimum: **1250**;', 'coverage strict current')
coverage_phase = '''## Phase 2BJ — Gaze 1.1.7.1 semantic-only exact promotion

Exact hash-matched artifact evidence closes **+1** current semantic object: Gaze-owned Iron's spell Soulward Shield, with the physical Iron's provider gate satisfied. Gaze's 26 exact player-facing Spirit Rites remain configuration-conditional because the deployed COMMON `disableGazeRites` value is unavailable; the two Geas effect types and eight rune items remain excluded by metric definition. Isolated NON-MERGE PR #201 final audit HEAD `2f4ff6536663b1c629a6a5ea92416765bea17b1e` passed evidence run `34676660467` and published artifact `10292013626` (`sha256:fb69f353b672f7c8ec7b470c454d24d1c3110cb996a250076a16d2b053f23f71`).

Phase 2BJ changes the strict semantic minimum to **1250** but does **not** close another provider component; the internal component metric stays **57/100**. Runtime/config/balance and any Black Arcana adapter remain fail-closed.

'''
s = replace_once(s, '## Phase 2BH — Goety 3.1.4 component #57, canonical\n', coverage_phase + '## Phase 2BH — Goety 3.1.4 component #57, canonical\n', 'coverage phase insert')
write(p, s)

# Current provider inventory
p = 'wiki/modpack-catalog/meta/CURRENT-MAGIC-PROVIDERS.md'
s = read(p)
phase_provider = '''## Checkpoint Gaze — Phase 2BJ exact-artifact semantic promotion

O artefato físico `gaze-1.1.7.1.jar` / SHA-1 `a8cb3190bde157f78160ce65c202ce2d47fb2041` foi materializado da versão Modrinth exata `od4ltbRo` e hash-matched em NON-MERGE PR #201. O registry exato fecha 26 Gaze Spirit Rites player-facing, dois Geas effect types, oito rune items e um Gaze-owned Iron's `AbstractSpell` (Soulward Shield). O pack físico contém Iron's 3.16.3, então o provider gate desse spell está satisfeito e Soulward Shield contribui **+1 `COUNTED_EXACT`**.

Os 26 Rites não são promovidos: `disableGazeRites` é COMMON e o control flow exato suprime o registry quando o valor resolvido é true; o valor implantado não está disponível. Geas e runes são excluídos pela definição atual da métrica. O mínimo semântico corrente passa a **1250**, enquanto provider-component closure permanece **57/100**. Evidência: audit HEAD `2f4ff6536663b1c629a6a5ea92416765bea17b1e`, run `34676660467`, artifact `10292013626`. Runtime/API/balance permanece fail-closed.

'''
s = replace_once(s, '## Checkpoint Goety — Phase 2BH canonical\n', phase_provider + '## Checkpoint Goety — Phase 2BH canonical\n', 'current providers gaze checkpoint')
write(p, s)

# Queue
p = 'wiki/modpack-catalog/meta/PROVIDER-AUDIT-QUEUE.md'
s = read(p)
s = regex_once(s, r'- `main` canônica após Phase 2BH durable / PR #198: `4fcc40aaf8149b5511dbd882a5616ee5240cd640`; HEAD limpo `d75f82a23b5c977ccc8ec84813bf89c928ffc0ab` passou CI #2523 e o exact-SHA post-merge CI #2524 ficou GREEN, incluindo canonical QA-JAR publication;', '- `main` canônica após Phase 2BI / PR #200: `21d63c58a2ad6cd19f4f68131bb39e4b39bdd1c2`; o exact-SHA post-merge CI #2528 ficou GREEN, incluindo canonical QA-JAR publication;', 'queue authority main')
s = replace_once(s, 'A reconstrução canônica após Phase 2BH fecha **1249 objetos mágicos semânticos** com a promoção exata de Goety 3.1.4. O denominador global continua incompleto e nenhuma porcentagem semântica é declarada.', 'A reconstrução canônica candidata da Phase 2BJ fecha **1250 objetos mágicos semânticos** após a promoção exata de Soulward Shield/Gaze. O denominador global continua incompleto e nenhuma porcentagem semântica é declarada.', 'queue semantic current')
s = replace_once(s, 'A reconciliação Gaze 1.1.7.1 também adiciona **+0** ao mínimo estrito: publisher e artefato físico fecham identidade/escala, mas o registry granular atual e a reachability por objeto permanecem abertos.', 'A Phase 2BJ substitui a reconciliação publisher-only anterior: o JAR exato Gaze 1.1.7.1 agora está hash-matched. Soulward Shield adiciona **+1**; os 26 Spirit Rites exatos permanecem `CONDITIONAL` por falta do valor COMMON implantado de `disableGazeRites`; 2 Geas e 8 runes são metric-excluded.', 'queue gaze current sentence')
s = replace_once(s, '- delta semântico Gaze 1.1.7.1: **+0**;', '- delta semântico Gaze 1.1.7.1 Phase 2BJ: **+1**;', 'queue gaze delta')
s = replace_once(s, '- mínimo estrito global canônico: **1249**;', '- mínimo estrito global candidato após Phase 2BJ: **1250**;', 'queue total')
new_gaze_queue = '''## Phase 2BJ — Gaze 1.1.7.1 — exact artifact, semantic +1, component still open

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

'''
s = regex_once(s, r'## Reconciliação Gaze 1\.1\.7\.1 — PR #180 — parcial, sem incremento de cobertura\n.*?(?=## Phase 2AY)', new_gaze_queue, 'queue replace gaze historical current block', flags=re.S)
write(p, s)

# SOURCES row
p = 'SOURCES.md'
s = read(p)
new_source_row = "| [Gaze `1.1.7.1`](https://www.curseforge.com/minecraft/mc-mods/gaze-a-malum-addon/files/7261638) | exact hash-matched installed-artifact audit for the Malum addon; 26 Gaze Spirit Rite identities, 2 Geas effect types, 8 rune items and one Gaze-owned Iron's spell structurally reconciled for semantic catalog/deduplication; physical/audit SHA-1 `a8cb3190bde157f78160ce65c202ce2d47fb2041` | `REFERENCE_ONLY / COMPATIBILITY_TARGET / ARR`; exact Modrinth version `NlvaJ5WE / od4ltbRo` was materialized in isolated NON-MERGE PR #201 and hash-matched before factual inspection. Binary inspection retained only cryptographic identity, metadata, registry/member/type relationships, resource identities/paths and targeted config/provider-gate facts. No implementation bodies/source reconstruction/recipe ingredient lists/numerical balance/localization prose/assets/models/sounds are copied or adapted; deployed `disableGazeRites`, runtime/API/resource-settlement seams and any future derivation remain fail-closed / `REVIEW_REQUIRED` |"
s = regex_once(s, r'^\| \[Gaze `1\.1\.7\.1`\].*$', new_source_row, 'sources gaze row', flags=re.M)
write(p, s)

# THIRD_PARTY_NOTICES row
p = 'THIRD_PARTY_NOTICES.md'
s = read(p)
new_notice_row = "| Gaze | installed `1.1.7.1`; JAR `gaze-1.1.7.1.jar`; CurseForge File ID `7261638`; Modrinth project/version `NlvaJ5WE / od4ltbRo`; physical/audit SHA-1 `a8cb3190bde157f78160ce65c202ce2d47fb2041`; exact evidence PR #201/run `34676660467` | `REFERENCE_ONLY / COMPATIBILITY_TARGET` exact-artifact factual audit closing 26 Gaze Spirit Rite identities, two Geas effect types, eight rune items and one Gaze-owned Iron's spell for catalog/deduplication; only Soulward Shield is currently promoted semantically because the Rite registry remains config-conditional | project is **All Rights Reserved**. Exact binary inspection is restricted to cryptographic identity, factual metadata/registry/type/member/resource-path evidence and narrow config/provider-gate control facts. No implementation bodies/source reconstruction, recipe ingredient lists, numerical balance values, localization prose, assets, models or sounds are copied/adapted. `disableGazeRites`, runtime/API/resource-settlement seams and any stronger derivation remain `REVIEW_REQUIRED`/fail-closed |"
s = regex_once(s, r'^\| Gaze \|.*$', new_notice_row, 'notices gaze row', flags=re.M)
write(p, s)

# Postconditions
sem = read('wiki/modpack-catalog/meta/SEMANTIC-MAGIC-COVERAGE.md')
assert '**1250 semantic magic objects are currently reconstructible' in sem
assert '| [Gaze](../providers/gaze/README.md) | 1.1.7.1 | 1 | `COUNTED_EXACT` |' in sem
assert '26 player-facing Spirit Rite identities' in sem
assert '| **Strict total** |  | **1250** |' in sem
assert '199 + 542 + 42 + 55 + 25 + 26 + 361 = 1250' in sem
cov = read('wiki/modpack-catalog/meta/CATALOG-COVERAGE-CURRENT.md')
assert 'strict counted minimum to 1250' in cov
assert 'latest semantic promotion is **Gaze +1**' in cov
assert '**57/100**' in cov
queue = read('wiki/modpack-catalog/meta/PROVIDER-AUDIT-QUEUE.md')
assert 'Phase 2BJ — Gaze 1.1.7.1' in queue
assert 'does not create component #58' in queue
sources = read('SOURCES.md')
assert 'NON-MERGE PR #201' in sources and 'Gaze `1.1.7.1`' in sources
notices = read('THIRD_PARTY_NOTICES.md')
assert 'Gaze | installed `1.1.7.1`' in notices
print('Phase 2BJ reconciliation postconditions: OK')
