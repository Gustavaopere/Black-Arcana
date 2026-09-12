from pathlib import Path

ROOT = Path('.')


def read(path):
    return (ROOT / path).read_text(encoding='utf-8')


def write(path, text):
    p = ROOT / path
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(text, encoding='utf-8')


def replace_once(text, old, new, label):
    count = text.count(old)
    if count != 1:
        raise SystemExit(f'{label}: expected exactly one match, found {count}')
    return text.replace(old, new, 1)


def insert_before(text, marker, addition, label):
    if addition.strip() in text:
        return text
    return replace_once(text, marker, addition + '\n\n' + marker, label)


iron_readme = '''# Goety Iron 3.1 — exact-artifact semantic closure

## Estado canônico do catálogo

- JAR físico: `GoetyIron-1.21.1-NeoForge-3.1.jar`
- Mod ID: `goetyiron`
- versão: `3.1`
- Minecraft: `1.21.1`
- loader: NeoForge
- CurseForge project/file: `1367643 / 8662179`
- SHA-1 físico e auditado: `c8529867e798661ed01fb2948abda23735888fc6`
- licença publicada: **DIVERGENTE** — CurseForge declara MIT; Modrinth declara All Rights Reserved; Black Arcana mantém a postura clean-room mais restritiva
- classificação: `BRIDGE_COMPAT + SPELL/RITUAL CONTENT`
- estado semântico: `COUNTED_EXACT`
- contribuição semântica: **14**
- componente técnico: **#59** após Phase 2BL

A Phase 2BL substitui o antigo limite publisher-only por evidência do JAR exato hash-matched. O artefato não é redistribuído; os artifacts de evidência preservam somente hashes, metadata, signatures/registry identities, resource paths, conditions e resumos de outcome.

## Inventário semântico exato

O provider registra exatamente **2 Focuses próprios**:

- `FIERY_FOCUS`
- `TARNISHED_FOCUS`

Ambos são superfícies `MagicFocus` do Goety ligadas a spells de summon próprios do addon. Nenhuma dessas identidades está entre os 123 Focuses ativos já contados no Goety 3.1.4 base.

O JAR empacota **14 recipes `goety:ritual`**. Dois são apenas caminhos de aquisição dos dois Focuses e não são recontados. Os **12 rituais não-Focus** restantes têm outcomes distintos e nenhuma condition de mod carregado. O conjunto inclui conversões/summons de servants e três outcomes de item/estado (`goetyiron:hemolytic_ring`, `irons_spellbooks:rotten_spell_book` e conversão para `goety:heretic_servant`), sem duplicar os 238 outcomes distintos do inventário Goety-base canônico.

Portanto: **2 Focus + 12 rituais não-Focus = 14 objetos mágicos semânticos `COUNTED_EXACT`.**

## Gate de registration/config

O passe estrutural do initializer prova:

- Focus holders: `2`;
- branches no static initializer do registry: `0`;
- chamadas `DeferredRegister.register` observadas no initializer: `22`;
- referências a config no initializer: `0`;
- campos config enable/disable-like: `0`.

Logo os dois Focuses não dependem de um gate provider-specific de registration/config. Configs de atributos, balance e replacement behavior continuam runtime/balance QA, não identidade semântica.

## Authority e deduplicação

- Goety continua authority de Soul Energy, Focus framework e servant ownership/lifecycle.
- Iron's continua authority de seus spells, entidades e atributos-base.
- Goety Iron é authority apenas das adaptações, Focuses, rituais e servants que ele próprio registra.
- Black Arcana não cria segundo Soul ledger, segundo servant state, segundo cast pipeline nem double-processing.

## Evidência

- NON-MERGE PR #205, HEAD `1feb07a7b9c721a0851e374ebe27c8dc748191fc`;
- structural run `34704435612`, artifact `10301537361`, digest `sha256:c39d4aff68878e34aa3a88e5bd07bf12b6b6616030b5ba20789bdff1e4fd7445`;
- targeted semantic run `34704813857`, artifact `10301716793`, digest `sha256:ec1e35546743ccd9e39763e664fd236336d84278ef74036b0c70b50eba73b7ff`;
- registration/config run `34705555893`, artifact `10301284496`, digest `sha256:28ce5ae85692e82c23b3bae8bc5a7ef29c90006ac220cd86067c55fe9b854973`.

Runtime servant lifecycle, spell settlement, cross-addon compatibility, generated config behavior e qualquer adapter Black Arcana permanecem fail-closed até QA/contrato provider-native específico.
'''
write('wiki/modpack-catalog/providers/goety-iron/README.md', iron_readme)

cat_readme = '''# Goety Cataclysm 1.21.1-1.8.2 — exact-artifact semantic closure

## Estado canônico do catálogo

- JAR físico: `goety_cataclysm-1.21.1-1.8.2.jar`
- Mod ID: `goety_cataclysm`
- versão: `1.21.1-1.8.2`
- Minecraft: `1.21.1`
- loader: NeoForge
- CurseForge project/file: `1224214 / 8518940`
- SHA-1 físico e auditado: `4e3052a082200371b36e1a88fdce05e294d82757`
- licença: `All Rights Reserved`
- classificação: `BRIDGE_COMPAT + SPELL/RITUAL CONTENT`
- estado semântico: `COUNTED_EXACT`
- contribuição semântica: **52**
- componente técnico: **#60** após Phase 2BL

A Phase 2BL substitui o antigo limite publisher-only por evidência do JAR exato hash-matched. O source público antigo da linha 1.20 não é tratado como authority de implementação da build física 1.21.1. O JAR não é redistribuído.

## Inventário semântico exato

O provider registra exatamente **28 Focuses próprios**:

`ABYSSAL_BEAM_FOCUS`, `ABYSSAL_MINE_FOCUS`, `ABYSSAL_ORB_FOCUS`, `AMETHYST_CLUSTER_FOCUS`, `ASHEN_BREATH_FOCUS`, `BATTLEFIELD_FOCUS`, `CURSED_CAIRN_FOCUS`, `CURSED_GRAVE_FOCUS`, `CURSED_TOMB_FOCUS`, `DEATH_LASER_FOCUS`, `DESERT_CRUSH_FOCUS`, `DESERT_RAID_FOCUS`, `EARTH_SHAKE_FOCUS`, `EXTINCT_FLAME_FOCUS`, `FLARE_BOMB_FOCUS`, `KAKOURGOS_FOCUS`, `KYRIA_FOCUS`, `LIGHTNING_SPEAR_FOCUS`, `POLEMISTIS_FOCUS`, `SANDSTORM_FOCUS`, `STORM_SERPENT_FOCUS`, `SUNKEN_CURRENT_FOCUS`, `SUNKEN_SWELL_FOCUS`, `SUNKEN_TRIBUNE_FOCUS`, `THUNDER_RAGE_FOCUS`, `VOID_RUNE_FOCUS`, `VOID_VORTEX_FOCUS`, `WATER_SPEAR_FOCUS`.

Todos os 28 possuem caminho de aquisição no artefato: **24 via `goety:ritual` e 4 via crafting normal**. As recipes de aquisição não são recontadas como ações independentes.

O JAR contém **48 recipes `goety:ritual`**; retiradas as 24 recipes de aquisição de Focus, restam **24 rituais não-Focus**. O passe direcionado fecha 24 outcomes distintos, sem conditions de mod: 10 conversões, 13 summon/thrall actions e 1 fabricator action. Esses outcomes são addon-owned e não duplicam os 238 rituais distintos já contados no Goety base.

Portanto: **28 Focus + 24 rituais não-Focus = 52 objetos mágicos semânticos `COUNTED_EXACT`.**

## Gate de registration/config

O passe estrutural do initializer prova:

- Focus holders: `28`;
- branches no static initializer do registry: `0`;
- chamadas `DeferredRegister.register` observadas no initializer: `38`;
- referências a `GCSpellConfig` no initializer: `0`;
- campos config enable/disable-like: `0`.

Logo os 28 Focuses não dependem de um gate provider-specific de registration/config. Balance, custos, servant stats e combat behavior continuam runtime/balance QA separado.

## Authority e deduplicação

- Goety continua authority de Soul Energy, Focus casting e servant lifecycle base.
- L_Ender's Cataclysm continua authority dos mobs, bosses e conteúdo-base que fornece.
- Goety Cataclysm é authority somente dos Focuses, rituais, servants e adaptações que registra.
- Black Arcana não cria segundo Soul ledger, segundo servant state, segundo ritual settlement nem segundo cast pipeline.

## Evidência

- NON-MERGE PR #206, HEAD `cd91bc9719f63ba0565981349f06a103fd6a9782`;
- structural run `34704449593`, artifact `10301367858`, digest `sha256:1dc688c4068dc4e89e6f04142cb1cd99eeff995ba1f53b8ce4e1429cc8af53d8`;
- targeted semantic run `34704823100`, artifact `10301168646`, digest `sha256:8cc6324727a854700e149df3d05ef376c5a078e9ec6c1cea79f702ec9bbde980`;
- registration/config run `34705567753`, artifact `10301603762`, digest `sha256:79054acb2c82ec3472403e9b926c9f1a6bafd1da47a873ef0a3dc3b794875850`.

Runtime servant lifecycle/combat, numerical balance, cross-addon compatibility e qualquer adapter Black Arcana permanecem fail-closed até QA/contrato provider-native específico.
'''
write('wiki/modpack-catalog/providers/goety-cataclysm/README.md', cat_readme)

iron_audit = '''# Goety Iron 3.1 — exact artifact audit

Status: `EXACT HASH-MATCHED / COUNTED_EXACT / COMPONENT #59 CANDIDATE UNTIL MERGE`

Physical SHA-1 and publisher artifact SHA-1 are identical: `c8529867e798661ed01fb2948abda23735888fc6` (CurseForge `1367643 / 8662179`).

## Exact semantic facts

- 2 addon-owned Focus holders: `FIERY_FOCUS`, `TARNISHED_FOCUS`.
- Both are Goety Focus surfaces backed by addon-owned summon-spell identities.
- 14 packaged `goety:ritual` recipes.
- 2 rituals are Focus acquisition only and are deduplicated against their Focus identities.
- 12 non-Focus rituals remain; all 12 have distinct outcomes and no mod-loaded condition.
- None of the 2 Focus IDs or 12 non-Focus outcomes duplicates the exact Goety 3.1.4 semantic inventory already counted in Phase 2BH.
- Registration initializer: 0 branches, 0 config references; no enable/disable-like config field was found by the narrow gate scan.

Semantic disposition: **+14 = 2 Focus + 12 non-Focus rituals**.

## Evidence chain

NON-MERGE PR #205. Structural `34704435612 / 10301537361`; semantic `34704813857 / 10301716793`; registration gate `34705555893 / 10301284496`.

Clean-room: the evidence branch never commits the JAR and durable docs retain no implementation bodies/assets. The CurseForge MIT vs Modrinth ARR discrepancy remains unresolved; the stricter posture controls.
'''
write('wiki/modpack-catalog/providers/goety-iron/EXACT-3.1-ARTIFACT-AUDIT.md', iron_audit)

cat_audit = '''# Goety Cataclysm 1.21.1-1.8.2 — exact artifact audit

Status: `EXACT HASH-MATCHED / COUNTED_EXACT / COMPONENT #60 CANDIDATE UNTIL MERGE`

Physical SHA-1 and publisher artifact SHA-1 are identical: `4e3052a082200371b36e1a88fdce05e294d82757` (CurseForge `1224214 / 8518940`).

## Exact semantic facts

- 28 addon-owned Focus holders with provider-owned spell surfaces.
- all 28 have packaged acquisition recipes: 24 ritual, 4 ordinary crafting.
- 48 packaged `goety:ritual` recipes.
- 24 rituals are Focus acquisition only and are deduplicated against their Focus identities.
- 24 non-Focus rituals remain; all have distinct outcomes and no mod-loaded condition.
- non-Focus outcome classes: 10 conversion, 13 summon/thrall, 1 fabricator.
- neither the 28 Focus identities nor the 24 non-Focus outcomes duplicates the exact Goety 3.1.4 semantic inventory already counted in Phase 2BH.
- Registration initializer: 0 branches, 0 config references; no enable/disable-like config field was found by the narrow gate scan.

Semantic disposition: **+52 = 28 Focus + 24 non-Focus rituals**.

## Evidence chain

NON-MERGE PR #206. Structural `34704449593 / 10301367858`; semantic `34704823100 / 10301168646`; registration gate `34705567753 / 10301603762`.

Clean-room: the evidence branch never commits the JAR and durable docs retain no implementation bodies/assets. ARR is preserved. Older 1.20 public source is not treated as exact 1.21.1 implementation authority.
'''
write('wiki/modpack-catalog/providers/goety-cataclysm/EXACT-1.21.1-1.8.2-ARTIFACT-AUDIT.md', cat_audit)

checkpoint = '''# Phase 2BL — Goety addon exact semantic closure checkpoint

Base considered: `main@4041316e2261d6ca46bbc4c1b6e717ddabb44047`.

## Result

- Goety Iron 3.1: **+14** (`2 Focus + 12 distinct non-Focus rituals`), component **#59**.
- Goety Cataclysm 1.21.1-1.8.2: **+52** (`28 Focus + 24 distinct non-Focus rituals`), component **#60**.
- Combined Phase 2BL semantic delta: **+66**.
- Strict semantic minimum: **1250 -> 1316**.
- Provider-component closure: **58/100 -> 60/100**.
- Global semantic denominator remains incomplete; no semantic percentage is declared.

Both providers are deduplicated against the exact base-Goety 3.1.4 inventory (123 active Focus + 238 distinct available non-Focus rituals). Acquisition recipes are pathways, not second semantic identities.

## Evidence boundary

Goety Iron: NON-MERGE PR #205, exact HEAD `1feb07a7b9c721a0851e374ebe27c8dc748191fc`; evidence artifacts `10301537361`, `10301716793`, `10301284496`.

Goety Cataclysm: NON-MERGE PR #206, exact HEAD `cd91bc9719f63ba0565981349f06a103fd6a9782`; evidence artifacts `10301367858`, `10301168646`, `10301603762`.

All evidence artifacts are text-only clean-room summaries. JARs are not committed/redistributed. Runtime behavior, numerical balance, servant lifecycle, full-modpack compatibility and any Black Arcana adapter remain separate fail-closed gates.
'''
write('wiki/modpack-catalog/meta/PHASE2BL-GOETY-ADDONS-EXACT-CHECKPOINT.md', checkpoint)

# Semantic ledger reconciliation.
p = 'wiki/modpack-catalog/meta/SEMANTIC-MAGIC-COVERAGE.md'
s = read(p)
phase = '''## Phase 2BL canonical candidate — Goety Iron 3.1 + Goety Cataclysm 1.21.1-1.8.2

Exact hash-matched artifact evidence closes both remaining Goety addon rows without duplicating base-Goety ownership. Goety Iron contributes **2 Focus + 12 distinct non-Focus rituals = +14**. Goety Cataclysm contributes **28 Focus + 24 distinct non-Focus rituals = +52**. Focus-acquisition recipes are deduplicated against the Focus identities themselves. Targeted scans find no mod-loaded conditions on the counted non-Focus rituals, while registry initializers have zero conditional branches and zero config references; no enable/disable-like registration gate was found.

Evidence is isolated in NON-MERGE PRs #205 and #206. Phase 2BL therefore adds **+66 `COUNTED_EXACT`**, moving the strict reconstructible minimum from **1250 to 1316** and, separately, closing provider components **#59 and #60**. Runtime/balance/servant-lifecycle QA remains separate and fail-closed.'''
s = insert_before(s, '## Phase 2BK exact zero closure — Ignis Soulfires: Spellbooks 1.1.0', phase, 'semantic phase insert')
s = replace_once(s, '**1250 semantic magic objects are currently reconstructible from canonical provider records after Phase 2BJ.**', '**1316 semantic magic objects are currently reconstructible from canonical provider records after Phase 2BL.**', 'semantic strict heading')
s = replace_once(s, '- Goety Focus + ritual layer: **361**;\n- total: `199 + 542 + 42 + 55 + 25 + 26 + 361 = 1250`.', '- Goety base Focus + ritual layer: **361**;\n- Goety Iron Focus + ritual layer: **14**;\n- Goety Cataclysm Focus + ritual layer: **52**;\n- total: `199 + 542 + 42 + 55 + 25 + 26 + 361 + 14 + 52 = 1316`.', 'semantic arithmetic')
goety_row = '| [Goety](../providers/goety/README.md) | 3.1.4 | 361 | `COUNTED_EXACT` | exact hash-matched JAR closes 123 active/acquirable Focus actions + 238 available distinct non-Focus ritual actions after semantic deduplication and physical-provider condition filtering; runtime/API/balance QA remains separate |'
addon_rows = goety_row + '\n| [Goety Iron](../providers/goety-iron/README.md) | 3.1 | 14 | `COUNTED_EXACT` | exact hash-matched JAR closes 2 unconditional addon-owned Focus identities + 12 distinct non-Focus rituals; 2 Focus-acquisition rituals deduplicated; no base-Goety semantic duplicates |\n| [Goety Cataclysm](../providers/goety-cataclysm/README.md) | 1.21.1-1.8.2 | 52 | `COUNTED_EXACT` | exact hash-matched JAR closes 28 unconditional addon-owned Focus identities + 24 distinct non-Focus rituals; 24 Focus-acquisition rituals deduplicated; no base-Goety semantic duplicates |'
s = replace_once(s, goety_row, addon_rows, 'semantic counted rows')
s = replace_once(s, '| **Strict total** |  | **1250** |  |  |', '| **Strict total** |  | **1316** |  |  |', 'semantic table total')
for old in [
    '| [Goety Cataclysm](../providers/goety-cataclysm/README.md) 1.21.1-1.8.2 | exact installed release; public semantic surface proves addon spells/abilities exist | `OPEN` | complete Focus/spell/ritual inventory unavailable for current build |\n',
    '| [Goety Iron](../providers/goety-iron/README.md) 3.1 | exact installed release; servant/focus/ritual bridge publicly established | `OPEN / BRIDGE-BOUNDED` | public servant list is not a spell inventory; focus/ritual registry totals are unverified |\n'
]:
    s = replace_once(s, old, '', 'semantic remove open row')
s = s.replace('These rows are deliberately **not additive to 1249**', 'These rows are deliberately **not additive to 1316**')
s = s.replace('1. **1249 is not “1249 / unknown”.**', '1. **1316 is not “1316 / unknown”.**')
s = s.replace('The current component target is `57/100`', 'The current component target is `60/100`')
old_order = '''1. Goety Iron 3.1 and Goety Cataclysm 1.21.1-1.8.2 exact semantic inventories without duplicating base-Goety ownership;
2. obtain deployed config evidence for input-blocked conditional rows, especially Not Enough Glyphs 4.6.1 and Gaze 1.1.7.1 Rites;
3. remaining open provider inventories that can materially reduce the denominator blocker.'''
new_order = '''1. obtain deployed config evidence for input-blocked conditional rows, especially Not Enough Glyphs 4.6.1 and Gaze 1.1.7.1 Rites;
2. close Somake 1.0.8-fix survival reachability/config if authoritative deployed evidence becomes available;
3. remaining open provider inventories that can materially reduce the denominator blocker.'''
s = replace_once(s, old_order, new_order, 'semantic next order')
write(p, s)

# Catalog coverage reconciliation.
p = 'wiki/modpack-catalog/meta/CATALOG-COVERAGE-CURRENT.md'
s = read(p)
s = replace_once(s, 'The reconstructible semantic ledger lives in [`SEMANTIC-MAGIC-COVERAGE.md`](./SEMANTIC-MAGIC-COVERAGE.md). Phase 2BK keeps the **strict counted minimum at 1250 semantic magic objects** while closing Ignis Soulfires: Spellbooks 1.1.0 as an exact zero-semantic bridge/gear provider. The global denominator is still incomplete and no semantic percentage is declared.', 'The reconstructible semantic ledger lives in [`SEMANTIC-MAGIC-COVERAGE.md`](./SEMANTIC-MAGIC-COVERAGE.md). Phase 2BL raises the **strict counted minimum to 1316 semantic magic objects** by closing exact Goety Iron 3.1 (+14) and Goety Cataclysm 1.21.1-1.8.2 (+52) inventories without duplicating base-Goety ownership. The global denominator is still incomplete and no semantic percentage is declared.', 'coverage intro')
phase_cov = '''## Phase 2BL — Goety addon exact closures, components #59 and #60

Exact hash-matched evidence closes **Goety Iron +14** (2 Focus + 12 non-Focus rituals) and **Goety Cataclysm +52** (28 Focus + 24 non-Focus rituals). Acquisition recipes are deduplicated against Focus identities; counted non-Focus rituals have distinct outcomes and no mod-loaded conditions. Narrow registry-gate scans find zero initializer branches and zero config references for Focus registration in both providers.

Phase 2BL therefore moves the strict semantic minimum to **1316** and the separate provider-component metric to **60/100**. NON-MERGE evidence PRs are #205 and #206. Runtime/balance/servant lifecycle and any Black Arcana adapter remain separate fail-closed gates.'''
s = insert_before(s, '## Phase 2BK — Ignis Soulfires: Spellbooks 1.1.0 component #58, exact zero closure', phase_cov, 'coverage phase insert')
s = replace_once(s, '**Canonical provider-component coverage after Phase 2BK: 58/100 = 58%.**', '**Canonical provider-component coverage after Phase 2BL: 60/100 = 60%.**', 'coverage headline')
# Update current-result bullets only where unambiguously current.
s = s.replace('- strict reconstructible semantic minimum: **1250**;', '- semantic numerator delta from Goety Iron 3.1 exact closure: **+14**;\n- semantic numerator delta from Goety Cataclysm 1.21.1-1.8.2 exact closure: **+52**;\n- strict reconstructible semantic minimum: **1316**;')
write(p, s)

# Current provider inventory summary.
p = 'wiki/modpack-catalog/meta/CURRENT-MAGIC-PROVIDERS.md'
s = read(p)
s = replace_once(s, 'O denominador interno corrente do catálogo permanece **100 componentes mágicos/cross-domain**; Phase 2BK fecha `ignissoulfires_spellbooks` como componente **#58**, portanto **58 estão canônicos**. Esse 58/100 é uma métrica técnica de fechamento de componentes e **não** é a porcentagem de spells/magias.', 'O denominador interno corrente do catálogo permanece **100 componentes mágicos/cross-domain**; Phase 2BL fecha `goetyiron` como componente **#59** e `goety_cataclysm` como componente **#60**, portanto **60 estão canônicos**. Esse 60/100 é uma métrica técnica de fechamento de componentes e **não** é a porcentagem de spells/magias.', 'current providers headline')
checkpoint_text = '''## Checkpoint Goety addons — Phase 2BL exact semantic closure

Goety Iron 3.1 e Goety Cataclysm 1.21.1-1.8.2 foram materializados em audits clean-room hash-matched, separados do Goety base 3.1.4. Goety Iron fecha **2 Focus + 12 rituais não-Focus = +14**; Goety Cataclysm fecha **28 Focus + 24 rituais não-Focus = +52**. Recipes de aquisição de Focus são caminhos de obtenção e não segunda identidade semântica. Os registries de Focus não têm branch/config gate de registration observado.

O delta conjunto é **+66**, levando o mínimo estrito a **1316**. Como ambos já eram providers abertos no denominador reconciliado, tornam-se componentes **#59 e #60 / 60/100**. Evidência isolada: PR #205 (Goety Iron) e PR #206 (Goety Cataclysm), ambas NON-MERGE. Runtime servant/cast settlement, balance e adapters continuam fail-closed.'''
s = insert_before(s, '## Checkpoint Ignis Soulfires: Spellbooks — Phase 2BK exact zero closure', checkpoint_text, 'current providers phase insert')
write(p, s)

# Operational queue.
p = 'wiki/modpack-catalog/meta/PROVIDER-AUDIT-QUEUE.md'
s = read(p)
s = replace_once(s, '- base canônica considerada para Phase 2BK: `main@fa14b75bf08482031e4fabbc779d30d295e22c5e`; esse SHA contém Phase 2BJ / PR #202 e passou exact-SHA post-merge CI #2531, incluindo canonical QA-JAR publication;', '- base canônica considerada para Phase 2BL: `main@4041316e2261d6ca46bbc4c1b6e717ddabb44047`; esse SHA contém Phase 2BK / PR #204 e passou exact-SHA post-merge CI #2534 / run `34703943824`, incluindo canonical QA-JAR publication;', 'queue base')
s = replace_once(s, 'A reconstrução canônica após Phase 2BJ fecha **1250 objetos mágicos semânticos**. Phase 2BK fecha Ignis Soulfires: Spellbooks em **+0** por evidência exata, portanto o mínimo continua **1250**. O denominador global continua incompleto e nenhuma porcentagem semântica é declarada.', 'A reconstrução canônica após Phase 2BK fecha **1250 objetos mágicos semânticos**. Phase 2BL fecha Goety Iron 3.1 em **+14** e Goety Cataclysm 1.21.1-1.8.2 em **+52**, portanto o mínimo passa a **1316**. O denominador global continua incompleto e nenhuma porcentagem semântica é declarada.', 'queue semantic intro')
s = replace_once(s, '- delta semântico Goety 3.1.4 Phase 2BH: **+361** (`123 active Focus + 238 available distinct non-Focus rituals`);\n- mínimo estrito global após Phase 2BK: **1250**;', '- delta semântico Goety 3.1.4 Phase 2BH: **+361** (`123 active Focus + 238 available distinct non-Focus rituals`);\n- delta semântico Goety Iron 3.1 Phase 2BL: **+14** (`2 Focus + 12 distinct non-Focus rituals`);\n- delta semântico Goety Cataclysm 1.21.1-1.8.2 Phase 2BL: **+52** (`28 Focus + 24 distinct non-Focus rituals`);\n- mínimo estrito global após Phase 2BL: **1316**;', 'queue deltas')
s = replace_once(s, '- cobertura de componentes após o fechamento Phase 2BK: **58/100 = 58%**; `ignissoulfires_spellbooks` é componente #58 por exact-artifact closure, sem delta semântico.\n\nO valor 58/100 nunca substitui a métrica semântica de magias.', '- cobertura de componentes após o fechamento Phase 2BL: **60/100 = 60%**; `goetyiron` é componente #59 e `goety_cataclysm` é componente #60 por exact-artifact semantic closure.\n\nO valor 60/100 nunca substitui a métrica semântica de magias.', 'queue component total')
queue_phase = '''## Phase 2BL — Goety Iron 3.1 + Goety Cataclysm 1.21.1-1.8.2 — componentes #59/#60 / semantic +66

| Mod ID | Artefato físico | Estado |
|---|---|---|
| `goetyiron` | `GoetyIron-1.21.1-NeoForge-3.1.jar` | EXACT HASH-MATCHED / 2 FOCUS + 12 DISTINCT NON-FOCUS RITUALS / UNCONDITIONAL REGISTRATION GATE / +14 / COMPONENT #59 |
| `goety_cataclysm` | `goety_cataclysm-1.21.1-1.8.2.jar` | EXACT HASH-MATCHED / 28 FOCUS + 24 DISTINCT NON-FOCUS RITUALS / UNCONDITIONAL REGISTRATION GATE / +52 / COMPONENT #60 |

Evidence: NON-MERGE PR #205 (Iron) and #206 (Cataclysm). Both audits hard-gate exact physical SHA-1, deduplicate Focus acquisition recipes and compare semantic ownership against base Goety 3.1.4. Runtime mechanics and adapters remain fail-closed.'''
s = insert_before(s, '## Phase 2BK — Ignis Soulfires: Spellbooks 1.1.0 — componente #58 / semantic +0', queue_phase, 'queue phase insert')
write(p, s)

# Provenance appendices: preserve existing history and append exact audit evidence.
p = 'SOURCES.md'
s = read(p)
source_add = '''\n\n## Phase 2BL — Goety addon exact-artifact evidence (2026-09-12)\n\n- **Goety Iron 3.1** — physical `GoetyIron-1.21.1-NeoForge-3.1.jar`, mod id `goetyiron`, SHA-1 `c8529867e798661ed01fb2948abda23735888fc6`, CurseForge `1367643 / 8662179`. NON-MERGE PR #205; structural `34704435612 / 10301537361`, targeted semantics `34704813857 / 10301716793`, registration gate `34705555893 / 10301284496`. License surfaces conflict (CurseForge MIT vs Modrinth ARR); strict clean-room posture retained.\n- **Goety Cataclysm 1.21.1-1.8.2** — physical `goety_cataclysm-1.21.1-1.8.2.jar`, mod id `goety_cataclysm`, SHA-1 `4e3052a082200371b36e1a88fdce05e294d82757`, CurseForge `1224214 / 8518940`. NON-MERGE PR #206; structural `34704449593 / 10301367858`, targeted semantics `34704823100 / 10301168646`, registration gate `34705567753 / 10301603762`. ARR; older public 1.20 source is not exact 1.21.1 authority.\n\nThe upstream JARs are not redistributed. Evidence retained by Black Arcana is factual clean-room metadata/registry/resource/condition/outcome material only.''' 
if '## Phase 2BL — Goety addon exact-artifact evidence (2026-09-12)' not in s:
    s += source_add
write(p, s)

p = 'THIRD_PARTY_NOTICES.md'
s = read(p)
notice_add = '''\n\n## Phase 2BL exact-artifact audit notices — 2026-09-12\n\n| Project | Physical artifact | License posture | Audit use |\n|---|---|---|---|\n| Goety Iron | `GoetyIron-1.21.1-NeoForge-3.1.jar` / SHA-1 `c8529867e798661ed01fb2948abda23735888fc6` | Publisher surfaces conflict: CurseForge MIT, Modrinth ARR; Black Arcana applies the stricter clean-room posture | factual hash/metadata/registry/resource/condition/outcome inspection only; no JAR/assets/source implementation redistributed |\n| Goety Cataclysm | `goety_cataclysm-1.21.1-1.8.2.jar` / SHA-1 `4e3052a082200371b36e1a88fdce05e294d82757` | All Rights Reserved | factual hash/metadata/registry/resource/condition/outcome inspection only; no JAR/assets/source implementation redistributed |\n'''
if '## Phase 2BL exact-artifact audit notices — 2026-09-12' not in s:
    s += notice_add
write(p, s)

# Postconditions independent of prose placement.
assert '1316 semantic magic objects' in read('wiki/modpack-catalog/meta/SEMANTIC-MAGIC-COVERAGE.md')
assert '| [Goety Iron]' in read('wiki/modpack-catalog/meta/SEMANTIC-MAGIC-COVERAGE.md')
assert '| [Goety Cataclysm]' in read('wiki/modpack-catalog/meta/SEMANTIC-MAGIC-COVERAGE.md')
assert '60/100 = 60%' in read('wiki/modpack-catalog/meta/CATALOG-COVERAGE-CURRENT.md')
assert '**#59**' in read('wiki/modpack-catalog/providers/goety-iron/README.md')
assert '**#60**' in read('wiki/modpack-catalog/providers/goety-cataclysm/README.md')
