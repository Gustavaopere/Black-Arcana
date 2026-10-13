# Touch Dig

- **Status:** PRESENTE — ativo
- **Spell ID:** `irons_spellbooks:touch_dig`
- **Provider/JAR:** Iron's Spells / `1.21.1-3.16.3`
- **Escola:** Nature
- **Níveis/raridade:** 1–3 / Rare → Legendary
- **Cast:** Instant, 0 ticks
- **Mana:** 15 fixo
- **Cooldown player-facing:** 0 s
- **Cooldown `DefaultConfig` 3.16.3:** 0,5 s
- **Range:** 8 blocos

## Função

Usa magia para quebrar um bloco, mantendo o item da mão como contexto de drops. O source preserva gates importantes do jogo/NeoForge e não é um simples `setAir`.

## Source audit 3.16.3

- spell power: 10, 13, 16 nos níveis 1–3;
- harvest thresholds: `<13` Iron, `>=13` Diamond, `>=15` Netherite;
- usa tags vanilla `INCORRECT_FOR_*_TOOL` para determinar capacidade de harvest;
- falha em Adventure mode com action-bar error;
- exige block target até 8 blocos;
- falha se destroy speed <0 ou harvest tag impedir;
- antes de quebrar, para ServerPlayer chama `CommonHooks.fireBlockBreak(...)`; se cancelado, **não quebra**;
- drops via `Block.dropResources(..., livingEntity.getMainHandItem())`;
- substitui bloco pelo legacy block do fluid state e emite `GameEvent.BLOCK_DESTROY`;
- particles `CRIT` ao longo do ray + impacto;
- finish sound `TOUCH_DIG_CAST`.

## Divergência documentada

A página pública atual mostra cooldown `0s`; o source pinado 3.16.3 usa `.setCooldownSeconds(0.5)`. Nenhuma das duas evidências é apagada. Runtime/config efetiva no pack deve ser QA-observada antes de uma integração depender de sub-second recast.

## Authority / anti-abuso / dedup

O spell source + NeoForge block-break hook são authority. Bridges não podem contornar Adventure mode, harvest tags, proteção/cancelamento de break event ou duplicar drops. Não conceder Mastery/XP por tentativa cancelada sem causalidade explícita.

## Verificação obrigatória

- dano/cura: não aplicável;
- targets: bloco; PvP/boss/summon não aplicável;
- range 8; duração instantânea;
- item/focus: main-hand influencia drops, mas item obrigatório específico `NÃO VERIFICADO`;
- loot/craft/acquisition do spell: `NÃO VERIFICADO` além do pipeline geral;
- VFX/som confirmados; QA de protections/modded blocks e cooldown efetivo: `NÃO VERIFICADO`;
- fail-closed: respeitar event cancellation e harvest gates.

## Fonte

- `https://iron.wiki/spells/` — cooldown player-facing, consulta 2026-09-06.
- `TouchDigSpell.java` — `DefaultConfig` e break pipeline do source 3.16.3.

## Parâmetros de implementação para perks — source auditado

- **Classe/commit:** [`TouchDigSpell.java`](https://github.com/iron431/irons-spells-n-spellbooks/blob/e4056af90302d37eb1739f5ff05020b020e6e252/src/main/java/io/redspace/ironsspellbooks/spells/nature/TouchDigSpell.java) (source fixo 1.21.1-3.16.3).
- **ID de spell lido na classe:** `irons_spellbooks:touch_dig`; o ID pode divergir do título de exibição.
- **Config:** minRarity `RARE`; maxLevel `3`; cooldown `0.5` segundos; cast `INSTANT`.
- **Campos Java:** `baseManaCost`=`15`; `manaCostPerLevel`=`0`; `baseSpellPower`=`10`; `spellPowerPerLevel`=`3`; `castTime`=`0`.
- **Métodos no código:** `getUniqueInfo()`, `getCastFinishSound()`, `getCastType()`, `getDefaultConfig()`, `getSpellResource()`, `getHarvestLevel()`, `checkPreCastConditions()`, `onCast()`, `doDestroyBlock()`.
- **Fórmulas numéricas com retorno direto:** não extraídas; examinar lógica e entidades auxiliares. Não são fórmulas completas de efeitos indiretos.
- **Pistas de execução (verificar semântica):** nenhuma das pistas-padrão extraída.

**Contrato de perks:** escola `nature` não implica toxicidade, dano ácido, status ou transformação automática. Verificar aplicação real por helper, entidade, efeito ou damage source. Separar atributo nativo de mudar geometria/status/quantidade; exigir contrato real, caps, segurança e dedup; sem hook ⚠️ condicionado/fail-closed. Iron's controla cast/efeitos/mana; RPG Skill Tree perks/Mastery/gates; Black Arcana seu runtime mágico. QA real pendente. [Mapa global](../TECHNICAL-PERK-MAP.md).
