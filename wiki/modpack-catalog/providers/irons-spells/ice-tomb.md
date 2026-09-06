# Ice Tomb

- **Status no modpack:** PRESENTE — ativo no catálogo atual
- **Provider:** Iron's Spells 'n Spellbooks
- **Mod ID:** `irons_spellbooks`
- **Spell ID:** `irons_spellbooks:ice_tomb`
- **JAR/versão instalada:** `irons_spellbooks-1.21.1-3.16.3.jar` / `1.21.1-3.16.3`
- **Escola:** Ice
- **Níveis:** 1–8
- **Raridade:** Uncommon → Legendary
- **Cast:** Instant
- **Mana:** 30–135
- **Cooldown:** 30 s
- **Healing atual:** 1
- **Duração atual:** 5–12 s

## O que faz

Encasa o próprio caster em um tomb de gelo protetor que fornece healing, absorve um hit ou counterspell antes de quebrar e pode ser abandonado ao desmontar.

## Snapshot upstream `e4056af...` — NÃO tratado como tag 3.16.3

- cria `IceTombEntity` na posição do caster e transfere seu movimento;
- healing = `sqrt(entityPowerMultiplier)`;
- duração = `80 + level * 20 * sqrt(entityPowerMultiplier)` ticks;
- o caster começa a montar a `IceTombEntity`;
- animação `SELF_CAST_TWO_HANDS`.

O comportamento player-facing “absorve um hit ou counterspell” vem do catálogo oficial; a liquidação interna de break/counterspell pertence à entidade e não foi inferida a partir do spell class.

## Targets / PvP / bosses / summons

- **Target:** o próprio caster.
- **PvP:** interação do tomb com ataques de players/counterspells segue a entidade provider; detalhes `NÃO VERIFICADO`.
- **Bosses/summons:** não são targets primários; interação de ataques contra o tomb `NÃO VERIFICADO`.

## Obtenção, requisitos e aprendizado

- pipeline geral de scrolls/spellbooks;
- rotas específicas `NÃO VERIFICADO`;
- requisitos adicionais `NÃO VERIFICADO`;
- itens/focus/rituais específicos `NÃO VERIFICADO`.

## Integrações / QA / fail-closed

- **Protection entity authority:** `IceTombEntity`.
- bridge/counterspell compat específica `NÃO VERIFICADO`.
- VFX/áudio finais e QA client-real `NÃO VERIFICADO`.
- Não adicionar segunda absorção/heal/break ledger ao mesmo tomb.

## Deduplicação

Já cobre stasis/protective Ice tomb self-cast com heal e single-hit/counterspell absorption.

## Fonte / evidência

- Catálogo oficial atual: `https://iron.wiki/spells/` — consulta 2026-09-06.
- Snapshot upstream `e4056af...`: `IceTombSpell.java`.
