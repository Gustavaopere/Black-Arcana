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

## Source audit 3.16.3 — commit `e4056af...`

- cria `IceTombEntity` na posição do caster e transfere seu movimento;
- healing = `sqrt(entityPowerMultiplier)`;
- duração = `80 + level * 20 * sqrt(entityPowerMultiplier)` ticks;
- o caster começa a montar a `IceTombEntity`;
- animação `SELF_CAST_TWO_HANDS`.

O comportamento player-facing “absorve um hit ou counterspell” vem do catálogo oficial; a liquidação interna de break/counterspell pertence à entidade e não foi inferida a partir da spell class.

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

## Matriz obrigatória de verificação

- **Status/provider/mod ID/JAR/spell ID/escola/tipo:** confirmados; tipo funcional = self-stasis/protection Ice.
- **Descrição funcional:** outcome público confirmado; break/counterspell fino pertence à entidade.
- **Níveis/raridade:** 1–8 / Uncommon → Legendary.
- **Cast type / cast time / channel:** `INSTANT` / 0 ticks / não channel.
- **Recurso/custo:** mana / 30–135; fórmula fina de custo `NÃO VERIFICADO`.
- **Cooldown:** 30 s.
- **Dano/cura/tipo de dano:** healing público 1 e fórmula source `sqrt(entityPowerMultiplier)`; dano não é outcome do cast auditado; tipo de dano não aplicável ao spell class.
- **Alcance/raio/área/duração:** self; duração pública 5–12 s e fórmula source acima; dimensões/hitbox da `IceTombEntity` `NÃO VERIFICADO`.
- **Scaling/fórmulas/caps:** healing/duration formulas acima; caps adicionais além de nível8 `NÃO VERIFICADO`.
- **Targets/PvP/bosses/summons:** self target; interactions de ataques/counterspell `NÃO VERIFICADO`.
- **Condições/requisitos:** desmontar pode abandonar o tomb segundo descrição pública; condições internas adicionais `NÃO VERIFICADO`.
- **Obtenção/fabricação/ganho/aprendizado:** pipeline geral; rotas específicas `NÃO VERIFICADO`.
- **Itens/focus/rituais:** específicos `NÃO VERIFICADO`.
- **VFX/partículas/textura/animação/áudio:** `SELF_CAST_TWO_HANDS` confirmado; VFX/partículas/textura/áudio `NÃO VERIFICADO`.
- **Integrações/bridges:** `IceTombEntity` authority; counterspell bridge específica `NÃO VERIFICADO`.
- **Deduplicação/sobreposição:** conclusão baseada no source 3.16.3 pinado + outcome público.
- **Bugs/QA/fail-closed:** QA real `NÃO VERIFICADO`; não duplicar heal/absorb/break settlement.
- **Fonte/evidência/estado:** catálogo + source 3.16.3.

## Fonte / evidência

- Catálogo oficial atual: `https://iron.wiki/spells/` — consulta 2026-09-06.
- Source 3.16.3 `e4056af...`: `IceTombSpell.java` + `gradle.properties`.
