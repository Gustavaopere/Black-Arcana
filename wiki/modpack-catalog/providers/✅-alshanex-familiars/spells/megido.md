# Megido

- **Provider:** Alshanex's Familiars
- **Mod ID:** `alshanex_familiars`
- **Exact installed JAR:** `alshanex_familiars-1.21.1_v4.0.3.jar`
- **Exact current spell ID:** `alshanex_familiars:megido`
- **Registry field:** `PetSpellRegistry.MEGIDO`
- **Provider class identity:** `MegidoSpell`
- **Semantic class:** standalone provider spell
- **Semantic state:** `COUNTED_EXACT`

## Exact-current evidence

The hash-matched 4.0.3 JAR declares this spell in the provider spell registry. The registry field is assigned through the exact registry initializer, and the corresponding provider class contains the filtered literal ID `megido`. The provider's `en_us` language resources also expose `spell.alshanex_familiars.megido`.

## Mechanics / balance

Exact 4.0.3 mana cost, cooldown, level range, damage/effect formula, targeting details and acquisition are **NÃO VERIFICADO** here unless separately stated above. Identity closure is not permission to infer numerical mechanics from class names or presentation.

## Authority / deduplication

This spell remains Alshanex-owned and executes through provider/Iron's authority as applicable. Black Arcana must not replay the cast, double-charge mana, duplicate cooldown settlement or treat a similar familiar theme as ownership transfer.

## Provenance

Read-only exact-artifact factual inspection only. No upstream implementation or asset is copied/adapted.

## ABI declarada no binário exato 4.0.3 — 2026-10-29

- Classe: `MegidoSpell`; ID canônico: `alshanex_familiars:megido`.
- Métodos **declarados**, com parâmetros e retorno verificados por `javap -p -s` após SHA-1 físico: `checkPreCastConditions(Level, int, LivingEntity, MagicData): boolean`; `getDamage(int, LivingEntity): float`; `getRadius(): float`; `getRange(): float`; `getMaxConnections(int, LivingEntity): int`; `onCast(Level, int, LivingEntity, CastSource, MagicData): void`.
- Observação de integração: raio e alcance são sem parâmetros, enquanto limite de conexões recebe nível/caster; não inferir alvo nem corrente sem fluxo.
- A classe também declara `getDefaultConfig()` e `getCastType()`, sem que seus valores tenham sido decodificados.
- Evidência: [check de ABI JAR 4.0.3](https://github.com/Gustavaopere/Black-Arcana/actions/runs/40933045252), artifact `12922838095`. Uma assinatura não constitui API pública mutadora; valores numéricos, hooks e QA do modpack continuam `NOT_VERIFIED` e `NOT_TESTED`. Veja `../EXACT-4.0.3-RITUAL-SCHEMA-SPELL-ABI-20261029.md`.

## Constantes de getRange/getRadius — JAR exato 4.0.3 (2026-10-29)

O [audit binário de constantes literais](../EXACT-4.0.3-MEGIDO-RANGE-RADIUS-LITERALS-20261029.md) validou o publisher JAR 4.0.3 contra SHA-1 `e5051c2385a426d05bf203ba8081a23d891f6686` e comprovou no método **sem parâmetros** `MegidoSpell.getRange():float` um retorno direto de **15.0F**, e em `MegidoSpell.getRadius():float`, **10.0F**. Foi feito pelo [CI run 40935905518](https://github.com/Gustavaopere/Black-Arcana/actions/runs/40935905518), artifact `12925410592`. Ambos têm status `EXACT_DIRECT_FLOAT_LITERAL`.

**Limite:** estes são valores retornados pelos getters exatos, **não** prova de alcance/raio efetivo em todos os estágios de `onCast`. Consumidores, escala de `getMaxConnections`, fórmulas de dano, custo, cooldown e mutabilidade por perk ainda `NOT_VERIFIED`; `physical_qa=NOT_TESTED`, nenhum hook certificado.
