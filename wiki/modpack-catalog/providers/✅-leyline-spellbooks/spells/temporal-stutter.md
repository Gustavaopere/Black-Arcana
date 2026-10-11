# Temporal Stutter

Status: `COUNTED_EXACT / ID E CLASSE VERIFICADOS NO JAR 1.0.3 / MECÂNICA INDIVIDUAL AINDA CONDICIONADA`

## Registro exato da versão instalada

- **Registry:** `LeySpellRegistry`, campo `TEMPORAL_STUTTER`.
- **Registry ID:** `leylines:temporal_stutter`.
- **Classe exata:** `TemporalStutterSpell`.
- **Confiança:** `COUNTED_EXACT` para identidade de registry/artefato; não implica execução física verificada em Survival.
- **Escola:** `leylines:ley`; todas as 14 classes fornecem configuração padrão para esta escola no JAR exato.
- **Autoridade:** Leyline Spellbooks mantém o efeito e o estado específico; Iron's Spells 'n Spellbooks mantém casting/mana/cooldown genéricos. Black Arcana não intercepta nem duplica esse pipeline.
- **Gate documentado:** registro incondicional, sem trava provider-native observada; elegibilidade genérica Iron's com `requiresLearning=false`, `allowLooting=true` e spell enabled por padrão. Configuração implantada no modpack e RNG de loot continuam não verificados.
- **Mecânica numérica, custo, cooldown, level, targeting exato, filtros PvP/boss, persistência e balance:** `NÃO VERIFICADO` individualmente, salvo descrição editorial pública explicitada na ficha; nenhum valor presumido.

Fonte: [registry da versão exata](../EXACT-1.0.3-SPELL-INVENTORY.md), [auditoria binária 1.0.3](../EXACT-1.0.3-ARTIFACT-AUDIT.md), [autoridade e reachability](../README.md). A menção pública abaixo continua limitada ao que foi descrito pelo editor do mod; não substitui prova do comportamento.

## Confirmado publicamente

A descrição oficial apresenta Temporal Stutter como uma interrupção temporal que congela brevemente um inimigo.

## Matriz técnica

- Registry ID / classe: `leylines:temporal_stutter` / `TemporalStutterSpell` — verificado no registry `LeySpellRegistry` do JAR 1.0.3
- Escola registrada: `leylines:ley` — configuração padrão da classe verificada em artefato exato
- Levels / rarity / mana / cooldown: `NÃO VERIFICADO`
- Target acquisition / range: `NÃO VERIFICADO`
- Freeze implementation: `NÃO VERIFICADO`
- Duration / caps / boss resistance: `NÃO VERIFICADO`
- AI, movement, attack e projectile interaction: `NÃO VERIFICADO`
- PvP behavior: `NÃO VERIFICADO`
- Acquisition: rota Iron's de scrolls elegíveis verificada em nível de host; receita, loot final, configurações implantadas e chance de obter este spell continuam `NÃO VERIFICADO`

## Deduplicação

Não traduzir automaticamente “freeze mid-timeline” em stun, slowness, frozen ticks ou tick-rate override. O mecanismo exato precisa vir do JAR.
