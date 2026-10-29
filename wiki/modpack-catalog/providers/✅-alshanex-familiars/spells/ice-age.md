# Ice Age

- **Provider:** Alshanex's Familiars
- **Mod ID:** `alshanex_familiars`
- **Exact installed JAR:** `alshanex_familiars-1.21.1_v4.0.3.jar`
- **Exact current spell ID:** `alshanex_familiars:ice_age`
- **Registry field:** `PetSpellRegistry.ICE_AGE`
- **Provider class identity:** `IceAgeSpell`
- **Semantic class:** standalone provider spell
- **Semantic state:** `COUNTED_EXACT`

## Exact-current evidence

The hash-matched 4.0.3 JAR declares this spell in the provider spell registry. The registry field is assigned through the exact registry initializer, and the corresponding provider class contains the filtered literal ID `ice_age`. The provider's `en_us` language resources also expose `spell.alshanex_familiars.ice_age`.

## Mechanics / balance

Exact 4.0.3 mana cost, cooldown, level range, damage/effect formula, targeting details and acquisition are **NÃO VERIFICADO** here unless separately stated above. Identity closure is not permission to infer numerical mechanics from class names or presentation.

## Authority / deduplication

This spell remains Alshanex-owned and executes through provider/Iron's authority as applicable. Black Arcana must not replay the cast, double-charge mana, duplicate cooldown settlement or treat a similar familiar theme as ownership transfer.

## Provenance

Read-only exact-artifact factual inspection only. No upstream implementation or asset is copied/adapted.

## ABI declarada no binário exato 4.0.3 — 2026-10-29

- Classe: `IceAgeSpell`; ID canônico: `alshanex_familiars:ice_age`.
- Métodos **declarados**, com parâmetros e retorno verificados por `javap -p -s` após SHA-1 físico: `getCastTime(int): int`; `onServerCastTick(Level, int, LivingEntity, MagicData): void`; `onServerCastComplete(Level, int, LivingEntity, MagicData, boolean): void`; `freezeAround(Level, int, LivingEntity, int): void`; `getDamage(int, LivingEntity): float`; `getRadius(int, LivingEntity): float`; `getDamageSource(Entity, Entity): SpellDamageSource`.
- Observação de integração: casting por tick e conclusão são fases distintas; getters não provam o raio efetivo.
- A classe também declara `getDefaultConfig()` e `getCastType()`, sem que seus valores tenham sido decodificados.
- Evidência: [check de ABI JAR 4.0.3](https://github.com/Gustavaopere/Black-Arcana/actions/runs/40933045252), artifact `12922838095`. Uma assinatura não constitui API pública mutadora; valores numéricos, hooks e QA do modpack continuam `NOT_VERIFIED` e `NOT_TESTED`. Veja `../EXACT-4.0.3-RITUAL-SCHEMA-SPELL-ABI-20261029.md`.
