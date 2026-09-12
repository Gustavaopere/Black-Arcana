# Inventário atual de providers mágicos

## Estado

`AUDITORIA EM ANDAMENTO — autoridade física 2026-09-11`

A autoridade de presença/JAR/runtime é a modlist física atual do pack, com **595 entradas top-level**, Minecraft 1.21.1 e NeoForge `21.1.248`. O snapshot físico reconciliado possui SHA-1 `7aaece7acbfb07ba4d0c66029042f36c50d046f0`.

O denominador interno corrente do catálogo permanece **100 componentes mágicos/cross-domain**; Phase 2BL fecha `goetyiron` como componente **#59** e `goety_cataclysm` como componente **#60**, portanto **60 estão canônicos**. Esse 60/100 é uma métrica técnica de fechamento de componentes e **não** é a porcentagem de spells/magias.

A métrica principal para o usuário é a cobertura de objetos mágicos semânticos — spells, glyphs/spell-parts, rituais/rites e equivalentes discretos. Seu denominador global ainda está em reconstrução; portanto nenhuma porcentagem final é declarada aqui.

Capítulos e tabelas históricas abaixo continuam úteis para rastrear deltas, mas não prevalecem sobre o snapshot físico atual.

## Freshness histórica 2026-09-07

O checkpoint de 2026-09-07 registrou updates como:

- Apotheosis `8.7.0 → 8.8.0`;
- Ars 'n' Spells `3.2.4 → 3.3.0` naquele snapshot; o runtime físico atual está em `3.3.2`;
- GTBC's SpellLib `2.1.0 → 2.2.0` (`2.2.0-1.21.1` no runtime);
- Vampirism `1.10.12 → 1.10.13`.

Esse bloco é histórico. Versões correntes devem sempre ser relidas da modlist física antes de qualquer nova auditoria.

A presença/update de um JAR não revalida automaticamente hook, API ou compatibilidade já assumidos por auditorias anteriores.

## Delta histórico do snapshot 2026-09-06

O snapshot anterior continha 607 entradas top-level. O guia mágico anterior catalogava 94 JARs/providers relevantes; esses números são históricos e não substituem a reconciliação física atual.

| Provider | Guia anterior | Snapshot 2026-09-06 |
|---|---:|---:|
| Ace's Spell Utils | 1.2.7.1 | 1.2.7.2 |
| Apothic Enchanting | 1.6.1 | 1.6.2 |
| Ars 'n' Spells | 3.2.2 | 3.2.4 |
| Cataclysm: Spellbooks | 1.1.12 | 1.1.13 |
| Discerning The Eldritch | 1.4.3 | 1.4.4 |
| Iron's Spells: Recolor | 1.2.5 | 1.3.2 |
| Monsters & Spellbooks | 0.0.16.2 / metadata histórico 0.0.14 | 0.0.16.3 |
| Starbunclemania | 1.5.7 | 1.5.8 |

## Classificação obrigatória

Cada JAR mágico deve ser classificado antes da extração spell-by-spell:

1. `SPELL_PROVIDER` — possui spells/glyphs/poderes jogáveis que precisam de catálogo individual.
2. `RITUAL_RESOURCE_PROVIDER` — fornece ritos, recursos, fluidos, espíritos, toxinas, plantas, altares ou progressão mágica reutilizável.
3. `BRIDGE_COMPAT` — integra providers; não deve ser contado como escola paralela salvo se realmente adicionar spell próprio.
4. `LIBRARY_INFRA` — biblioteca/API/VFX/UI; documentar capabilities, não inventar spells.
5. `GEAR_LOOT_SUPPORT` — gear, loot ou atributos mágicos sem catálogo próprio de spells.
6. `MIXED` — contém mais de uma das categorias; decompor por feature.

## Providers prioritários para deduplicação

### Iron's Spells e grandes addons

- Iron's Spells 'n Spellbooks;
- Cataclysm: Spellbooks;
- Monsters & Spellbooks;
- T.O Magic n' Extras;
- Hazen N Stuff;
- ISS: Magic From The East;
- Asterism Arcanum;
- Leyline Spellbooks;
- Paladin Spells;
- Somake;
- Discerning The Eldritch;
- Dreamless Spells;
- Fire's Ender Expansion;
- GTBC's Geomancy Plus;
- Farmer's Spell 'n Spellbooks;
- Apprentice's Codex;
- demais addons Iron's presentes na modlist.

### Ars Nouveau

Ars Nouveau e seus addons devem ser catalogados em nível de glyph/form/augment e também em combinações canônicas somente quando o pack tratar a combinação como poder nomeado. Não criar uma página para cada permutação possível.

### Sistemas externos de magia/ritual/recurso

- Goety;
- Malum;
- Eidolon: Repraised;
- Hexalia;
- Toxony;
- Vampirism/Bloodlines e bridges mágicas;
- demais providers ocultistas/alquímicos presentes.

### Familiars e infraestrutura relacionada

A modlist física atual inclui, entre outros, `familiarslib-1.21.1-1.7.1.jar` e `alshanex_familiars-1.21.1_v4.0.3.jar`. São componentes distintos e não compartilham automaticamente ownership semântico:

- FamiliarsLib foi fechado na Phase 2AX como `LIBRARY_INFRA`/framework de familiar, com **0** novas magias semânticas independentes;
- Alshanex's Familiars é consumidor/conteúdo concreto; Phase 2BD fecha a linha 4.0.3 em **7 spells próprios + 11 rituais próprios = 18 objetos semânticos**, usando o JAR exato hash-matched; runtime QA e seam de ownership continuam separados;
- documentação histórica que associa Sound School a Alshanex não deve prevalecer sobre a release 4.0, que moveu esse conteúdo para Tunes 'n Tomes;
- familiar ownership para Borrowed Sight continua exigindo seam provider-native verificável e revalidação server-side.

## Checkpoint Leyline Spellbooks — Phase 2BG canonical

The exact physical `leylines-1.0.3.jar` / SHA-1 `dfa6908731f432905caaaa1e53b4aedeaa26ed59` was materialized from CurseForge File ID `8565076` and hash-matched. Its current provider registry contains **14 unconditional `AbstractSpell` identities**, superseding the public nine-name lower bound.

Exact Ley-school/default evidence finds no provider-specific spell lock, and the exact Iron's 3.16.3 generic scroll-selection path corroborates ordinary host reachability. `COUNTED_EXACT` treatment is based on the exact unconditional registry; deployed generic host config remains separate runtime QA. Durable PR #195 HEAD `a9d7b55044230bbb011f7233ffd75d9a8321489b` passed CI #2503, squash merge `88f042f68429ff920314a7ec3a6923369edc93fd` passed exact-SHA post-merge CI #2504, and the canonical totals are now **888 semantic objects / 56/100 components**.

Runtime numerical tuning, final loot probabilities, pillar/rift persistence/network internals and any Black Arcana adapter remain separate fail-closed gates.

## Checkpoint Somake Spells — Phase 2BF

The exact physical `somakespells-1.0.8-1.21.1-fix.jar` / SHA-1 `b0ad94c1504709662bee2d08700375ccecbb5ec7` was materialized from File ID `8417850` and hash-matched. The provider owns **67 exact current spell registrations** under the present optional-provider set: 61 unconditional, three gated by physical `mowziesmobs`, and three gated by physical `iss_magicfromtheeast`.

This does **not** add to the strict semantic numerator. Somake's `enableSpellLockSystem` is a `COMMON` config at `somakespells/general/common.toml`, code-default `false`; the deployed config is not available in authoritative project material, and full per-object survival acquisition/reachability is not closed. At the Phase 2BF closure, the totals remained **874 semantic objects** and **55/100 structural components**; Phase 2BG later supersedes those current totals with 888 / 56/100. Runtime mechanics, Aqua/T.O coexistence and any Black Arcana adapter remain fail-closed.

## Checkpoint Cataclysm: Spellbooks — Phase 2BE

O artefato físico `cataclysm_spellbooks-1.1.13-1.21.jar` / SHA-1 `4af8348cc77bbff2ab7057c1fac26a5ab0a5b6a2` foi materializado pelo File ID exato `8792628` em auditoria isolada e bateu criptograficamente com a modlist. O registry exato fecha **59 `AbstractSpell` registrations `COUNTED_EXACT`**. Por implementation package group: 7 Abyssal, 4 Ender, 1 Evocation, 5 Holy, 11 Fire, 5 Ice, 4 Nature e 22 Technomancy; essa distribuição de packages não é promovida automaticamente a uma tabela de escolas/runtime mechanics.

O `en_us` contém 69 root spell keys, mas dez não possuem identidade registrada no 1.1.13 e ficam excluídos como translation-only/WIP-or-residual. O claim genérico/current do publisher de 65 spells não substitui o registry físico instalado; existe inclusive uma 1.1.14 beta posterior ao arquivo do pack.

Esse fechamento é de identidade/contagem. O HEAD exato do PR #189 (`e787699d25b283b8040cd179f605143e8ee396de`) passou CI #2483; o merge `main@cce7f51794e4e65b0d97511eb55f710afc6e02f0` passou CI #2484 attempt 2 completo após um primeiro attempt encerrar por timeout externo no download da API do Iron's. Balance numérico, acquisition, runtime QA específico do provider e qualquer seam futuro Black Arcana↔Cataclysm Spellbooks continuam separados e fail-closed até evidência provider-native segura.

## Checkpoint Alshanex's Familiars — Phase 2BD

O artefato físico `alshanex_familiars-1.21.1_v4.0.3.jar` / SHA-1 `e5051c2385a426d05bf203ba8081a23d891f6686` foi materializado pelo File ID exato `8675568` em auditoria isolada e bateu criptograficamente com o pack. O inventário current-version fecha **7 spell registrations** e **11 `alshanex_familiars:ritual_recipe` identities**, totalizando **18 objetos mágicos semânticos `COUNTED_EXACT`**. Sound/Melodic continua pertencendo a Tunes n' Tomes e não é recontado.

Esse fechamento é de catálogo/identidade. Runtime QA, valores numéricos e qualquer adapter Black Arcana↔Alshanex permanecem fail-closed até contrato provider-native seguro.

## Checkpoint Apprentice's Codex — Phase 2L

`apprenticecodex` está source-catalogado contra o artefato instalado `0.9.7.1` e o pin exato `hexqua/apprentice_codex@305ea6aef7bb9642a9d1fc2b9042f3dfb2ce5b2e`:

- 83/83 spells individualizados;
- 9 escolas canônicas do Iron's;
- School Affinity auditado;
- registries de suporte auditados;
- acquisition/learning auditados;
- compat packages reconciliados com a modlist física;
- runtime QA integral do pack ainda pendente.

A cobertura source-level não converte o addon em authority de Black Arcana nem em provider de Mastery do RPG Skill Tree.

## Checkpoint Goety addons — Phase 2BL exact semantic closure

Goety Iron 3.1 e Goety Cataclysm 1.21.1-1.8.2 foram materializados em audits clean-room hash-matched, separados do Goety base 3.1.4. Goety Iron fecha **2 Focus + 12 rituais não-Focus = +14**; Goety Cataclysm fecha **28 Focus + 24 rituais não-Focus = +52**. Recipes de aquisição de Focus são caminhos de obtenção e não segunda identidade semântica. Os registries de Focus não têm branch/config gate de registration observado.

O delta conjunto é **+66**, levando o mínimo estrito a **1316**. Como ambos já eram providers abertos no denominador reconciliado, tornam-se componentes **#59 e #60 / 60/100**. Evidência isolada: PR #205 (Goety Iron) e PR #206 (Goety Cataclysm), ambas NON-MERGE. Runtime servant/cast settlement, balance e adapters continuam fail-closed.

## Checkpoint Ignis Soulfires: Spellbooks — Phase 2BK exact zero closure

O artefato físico `ignissoulfires_spellbooks-1.1.0.jar` / SHA-1 `dcde77db35b6de3562b4e6de0025746eaf68f119` foi materializado do File ID CurseForge exato `8620663` e hash-matched em NON-MERGE PR #203. O JAR possui 11 classes próprias; seus registries são um armor material e exatamente cinco equipment items. Não há `AbstractSpell`, `registerSpell`, `SpellRegistry`, `Ritual`, `Rite` ou `Ability` nas classes do provider, nem spell/ritual/action data registry empacotado.

A classificação exata é `BRIDGE_COMPAT + GEAR_LOOT_SUPPORT`; semanticamente é `ZERO_BRIDGE_INFRA`, **+0** objetos. O mínimo estrito permanece **1250**. Como o provider já era uma unidade aberta do denominador técnico de 100 componentes, seu fechamento exato torna-o componente **#58 / 58/100**. Evidência: audit HEAD `ed807b77345cde1803767d804e26ea972c41d964`, run `34688273425`, text-only artifact `10296406134`. Runtime gear/balance e qualquer adapter Black Arcana continuam fail-closed.

## Checkpoint Gaze — Phase 2BJ exact-artifact semantic promotion

O artefato físico `gaze-1.1.7.1.jar` / SHA-1 `a8cb3190bde157f78160ce65c202ce2d47fb2041` foi materializado da versão Modrinth exata `od4ltbRo` e hash-matched em NON-MERGE PR #201. O registry exato fecha 26 Gaze Spirit Rites player-facing, dois Geas effect types, oito rune items e um Gaze-owned Iron's `AbstractSpell` (Soulward Shield). O pack físico contém Iron's 3.16.3, então o provider gate desse spell está satisfeito e Soulward Shield contribui **+1 `COUNTED_EXACT`**.

Os 26 Rites não são promovidos: `disableGazeRites` é COMMON e o control flow exato suprime o registry quando o valor resolvido é true; o valor implantado não está disponível. Geas e runes são excluídos pela definição atual da métrica. O mínimo semântico corrente passa a **1250**, enquanto provider-component closure permanece **57/100**. Evidência: audit HEAD `2f4ff6536663b1c629a6a5ea92416765bea17b1e`, run `34676660467`, artifact `10292013626`. Runtime/API/balance permanece fail-closed.

## Checkpoint Goety — Phase 2BH canonical

Exact `goety-3.1.4.jar` evidence closes **123 active Focus actions + 238 available distinct non-Focus ritual actions = +361**. Durable PR #198 HEAD `d75f82a23b5c977ccc8ec84813bf89c928ffc0ab` passed CI #2523; squash merge `4fcc40aaf8149b5511dbd882a5616ee5240cd640` passed exact-SHA post-merge CI #2524 and published QA artifact `10291461067` with SHA-256 `4f2ccf8be11cdba348c7cd0bdc64e595f6b101257b2b99f80fbe5542fae41ada`. Canonical totals are **1249 semantic objects / 57 of 100 components**. Runtime/API/provider settlement remains fail-closed.

## Regra de completude

A Wiki só poderá declarar `CATÁLOGO MÁGICO COMPLETO` quando:

- todos os JARs mágicos/relacionados da modlist atual tiverem classificação;
- todo `SPELL_PROVIDER` tiver inventário individual ou regra explícita de composição;
- todo spell tiver assinatura semântica para deduplicação;
- versão/JAR/mod ID estiverem reconciliados com a modlist atual;
- aquisição, custo, dano/efeito, cooldown e scaling forem extraídos do provider/runtime/config, não inferidos;
- sobreposições forem resolvidas por provider-native first;
- novos spells Black Arcana tiverem justificativa de delta mecânico real.

Até esses gates fecharem, Phase 3 permanece bloqueada.