# `somakespells:blood_cut`

- Provider: **Somake Spells** (`somakespells`)
- Artifact: `somakespells-1.0.9-1.21.1.jar`
- Physical / publisher SHA-1: `171841ac9f802be9309ecc166c1d972ac6d404c0`
- Substrate: **Iron's Spells 'n Spellbooks**
- Registry identity: `somakespells:blood_cut`
- Registration gate: **Unconditional**
- Current composition registration: **ADMITTED**
- State: `EXACT_PHYSICAL_REGISTRY / CURRENT_REGISTRATION_ADMITTED / STRICT_COUNT_CONDITIONAL`

## Registration evidence

The exact physical 1.0.9 `ModSpells` topology registers this identity without an optional-provider registration predicate.

The exact current artifact has 83 unique Somake spell registry IDs, and the present mod composition satisfies all optional registration predicates. This card records one of those **83/83 currently admitted registrations**.

## Host / progression boundary

Exact 1.0.9 structural evidence found no provider `isEnabled()` override among the 83 spell classes. That does **not** substitute for the effective deployed Iron's spell configuration.

This identity is not among the seven provider `allowCrafting()` override identities isolated by the exact 1.0.9 structural audit. Effective Iron's host `allow_crafting`/datapack state and actual survival acquisition are still not treated as deployed facts.

Still unresolved for strict semantic promotion:

- effective Iron's per-spell/global/datapack `enabled`;
- effective Iron's `allow_crafting` where applicable;
- deployed Somake `enableSpellLockSystem` COMMON value;
- object-level or bounded-set survival acquisition/reachability;
- assembled-pack progression/runtime settlement.

## Counting boundary

This is an exact current registry identity, not yet an independently strict-counted semantic action. Registration presence alone does not add this card to the strict numerator while the host/provider config and reachability gates above remain open.

Do not infer display name, school, level, rarity, mana cost, cooldown, damage, duration, targeting, recipe, loot source or formulas from the registry path.

## Authority

Iron's owns host casting/resource/cooldown settlement. Somake owns this spell identity and its provider progression. Black Arcana catalogs and may observe supported provider state; it does not recreate either runtime.

Sources: `../EXACT-1.0.9-REGISTRY-AUDIT.md`, `../EXACT-1.0.9-REGISTRATION-GATE-MAP.md`, `../SPELL-CATALOG-1.0.9.md`.


## Auditoria técnica em andamento — Blood Cut (21/10/2026)

A [nova matriz de prova](blood-cut-technical-gate.md) propõe verificar a FQCN concreta, descritores de métodos e símbolos de efeito no JAR Somake 1.0.9 SHA-1 exato, por um workflow Java 21 com testes sintéticos negativos. **A existência de uma classe candidata `BloodCutSpell` e os seus métodos ainda não estão certificados por esta nova execução**; a identidade de registry `somakespells:blood_cut` permanece comprovada no catálogo físico anterior.

Os eixos de targeting (self/entidade/área), raycast/LOS, raio, hitbox, tamanho/velocidade de projétil, dano/tipo, status, duração, escalonamento, custos, cooldown, caps e identidade de hit/proc continuam **NÃO VERIFICADOS nesta ficha**. Nenhuma API de modificação por jogador foi homologada: ⛔ `FAIL_CLOSED`. Reavaliar a ficha com as evidências extraídas pelo CI antes de publicar qualquer fórmula.
