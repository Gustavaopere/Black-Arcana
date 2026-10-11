# Anchor Recall

Status: `COUNTED_EXACT / ID E CLASSE VERIFICADOS NO JAR 1.0.3 / MECÂNICA INDIVIDUAL AINDA CONDICIONADA`

## Registro exato da versão instalada

- **Registry:** `LeySpellRegistry`, campo `ANCHOR_RECALL`.
- **Registry ID:** `leylines:anchor_recall`.
- **Classe exata:** `AnchorRecallSpell`.
- **Confiança:** `COUNTED_EXACT` para identidade de registry/artefato; não implica execução física verificada em Survival.
- **Escola:** `leylines:ley`; todas as 14 classes fornecem configuração padrão para esta escola no JAR exato.
- **Autoridade:** Leyline Spellbooks mantém o efeito e o estado específico; Iron's Spells 'n Spellbooks mantém casting/mana/cooldown genéricos. Black Arcana não intercepta nem duplica esse pipeline.
- **Gate documentado:** registro incondicional, sem trava provider-native observada; elegibilidade genérica Iron's com `requiresLearning=false`, `allowLooting=true` e spell enabled por padrão. Configuração implantada no modpack e RNG de loot continuam não verificados.
- **Mecânica numérica, custo, cooldown, level, targeting exato, filtros PvP/boss, persistência e balance:** `NÃO VERIFICADO` individualmente, salvo descrição editorial pública explicitada na ficha; nenhum valor presumido.

Fonte: [registry da versão exata](../EXACT-1.0.3-SPELL-INVENTORY.md), [auditoria binária 1.0.3](../EXACT-1.0.3-ARTIFACT-AUDIT.md), [autoridade e reachability](../README.md). A menção pública abaixo continua limitada ao que foi descrito pelo editor do mod; não substitui prova do comportamento.

## Confirmado publicamente

A página oficial descreve Anchor Recall como marcação de uma posição na lattice/leyline seguida de retorno posterior do caster a essa posição.

## Matriz técnica

- Registry ID / classe: `leylines:anchor_recall` / `AnchorRecallSpell` — verificado no registry `LeySpellRegistry` do JAR 1.0.3
- Escola registrada: `leylines:ley` — configuração padrão da classe verificada em artefato exato
- Levels / rarity / mana / cooldown: `NÃO VERIFICADO`
- Cast/recast/two-stage state: `NÃO VERIFICADO`
- Persistence across logout/death/restart: `NÃO VERIFICADO`
- Dimension restrictions: `NÃO VERIFICADO`
- Anchor lifetime/replacement: `NÃO VERIFICADO`
- Safe-position validation: `NÃO VERIFICADO`
- Acquisition: rota Iron's de scrolls elegíveis verificada em nível de host; receita, loot final, configurações implantadas e chance de obter este spell continuam `NÃO VERIFICADO`

## Deduplicação

Não criar storage de anchor paralelo. Qualquer integração deverá observar o estado provider-native, incluindo cleanup e dimensão, quando esse boundary for identificado.
