# Blizzard

- **Status no modpack:** PRESENTE — ativo no catálogo atual
- **Provider:** Iron's Spells 'n Spellbooks
- **Mod ID:** `irons_spellbooks`
- **Spell ID:** `irons_spellbooks:blizzard`
- **JAR/versão instalada:** `irons_spellbooks-1.21.1-3.16.3.jar` / `1.21.1-3.16.3`
- **Escola:** Ice
- **Níveis:** 1–8
- **Raridade:** Rare → Legendary
- **Cast:** Long
- **Mana atual:** 40–110
- **Cooldown atual:** 22 s
- **Raio público atual:** 8 blocos
- **Duração pública atual:** 11,5 s

## O que faz

Canaliza um blizzard lento e móvel em uma posição-alvo, puxando criaturas para o centro com vento e neve congelantes.

## Source audit 3.16.3 — commit `e4056af...`

- classe `BlizzardSpell`;
- cast time 25 ticks;
- target helper até 32 blocos, com fallback para raycast de 32;
- move o spawn para nível relativo do chão;
- cria `BlizzardAoe`, define owner, radius, duration e movimento horizontal `0.05`;
- radius: `2 + 6 * entityPowerMultiplier`;
- duration: `20 * (10 + 1.5 * spellLevel)` ticks;
- sons: `CONE_OF_COLD_LOOP` no início e `ICE_CAST` no finish;
- animação: `ANIMATION_LONG_CAST`.

**Divergência documentação × source:** o catálogo oficial atual publica `11.5s Duration`, enquanto o source 3.16.3 calcula duração por nível. Com `entityPowerMultiplier` neutro, a fórmula resulta em 11,5 s no nível 1 e 22 s no nível 8. A Wiki preserva ambos: 11,5 s como valor player-facing atualmente publicado e a fórmula acima como implementação source-auditada; não colapsar a fórmula interna para 11,5 s em integrações.

## Targets / PvP / bosses / summons

- **Posicionamento confirmado no source:** alvo ou raycast até 32 blocos.
- **Pull/seleção de entidades pela `BlizzardAoe`:** detalhes finos `NÃO VERIFICADO` nesta auditoria.
- **Players em PvP, bosses e summons:** elegibilidade/imunidades específicas `NÃO VERIFICADO`.

## Obtenção, requisitos e aprendizado

- **Pipeline geral:** segue o sistema de scrolls/spellbooks do Iron's.
- **Rotas específicas de loot/trade/craft/recompensa:** `NÃO VERIFICADO`.
- **Condições/requisitos adicionais:** `NÃO VERIFICADO`.
- **Itens/focus/rituais obrigatórios além do pipeline normal:** `NÃO VERIFICADO`.

## Integrações / QA / fail-closed

- **Area authority:** `BlizzardAoe` no source 3.16.3.
- **Bridge específica:** `NÃO VERIFICADO`.
- **Partículas/textura e comportamento fino do pull:** `NÃO VERIFICADO`; sons/animação source-auditados estão registrados acima.
- **QA client/modpack real da apresentação e do pull:** `NÃO VERIFICADO`.
- Não criar segundo vortex/pull/settlement para o mesmo cast.

## Deduplicação

Já cobre vortex Ice móvel com pull/freezing semantics. Uma nova tempestade glacial só é lacuna se tiver contrato diferente, não apenas outro AoE que puxa e congela.

## Fonte / evidência

- Catálogo oficial atual: `https://iron.wiki/spells/` — consulta 2026-09-06.
- Source 3.16.3: `iron431/irons-spells-n-spellbooks@e4056af90302d37eb1739f5ff05020b020e6e252`, `BlizzardSpell.java`.
- Pinagem de versão: `gradle.properties` no mesmo commit (`minecraft_version=1.21.1`, `mod_version=1.21.1-3.16.3`).
