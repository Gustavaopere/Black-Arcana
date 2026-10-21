# Portal

- **Status no modpack:** PRESENTE — provider instalado
- **Provider:** Iron's Spells 'n Spellbooks
- **Mod ID:** `irons_spellbooks`
- **JAR/versão:** `irons_spellbooks-1.21.1-3.16.3.jar` / `1.21.1-3.16.3`
- **Escola:** Ender
- **Níveis:** 1–3
- **Raridade:** Uncommon → Legendary
- **Cast:** Instant
- **Mana:** 200–220
- **Cooldown:** 180 s
- **Alcance de cast:** 48 blocos
- **Duração dos portais:** 5–9 min

## O que faz

Cria um par de portais vinculados que permite deslocamento bidirecional entre os dois pontos durante a duração do efeito.

## Escalonamento

A duração listada cresce de 5 para 9 minutos; o custo de mana cresce de 200 para 220. Restrições dimensionais, validação de destino, persistência e regras de chunk permanecem `NÃO VERIFICADO` quando não constam do catálogo público.

## Obtenção e aprendizado

Segue o pipeline geral de scrolls/spellbooks do Iron's. Fontes específicas de loot/crafting permanecem `NÃO VERIFICADO`.

## Deduplicação

Já cobre portal temporário bidirecional de deslocamento. Qualquer integração Black Arcana com Immersive Portals ou novos domínios deve provar um contrato diferente e preservar world-safety/no-force-load, sem duplicar este spell por estética.

## VFX / animação / áudio

`NÃO VERIFICADO` no runtime real do pack neste passe.

## Fonte / evidência

Catálogo oficial atual: `https://iron.wiki/spells/` — consulta em 2026-09-06.

## Parâmetros de implementação para perks — source auditado

- **Classe/commit:** [`PortalSpell.java`](https://github.com/iron431/irons-spells-n-spellbooks/blob/e4056af90302d37eb1739f5ff05020b020e6e252/src/main/java/io/redspace/ironsspellbooks/spells/ender/PortalSpell.java), fixado em `e4056af90302d37eb1739f5ff05020b020e6e252` (versão 1.21.1-3.16.3).
- **ID declarado:** `irons_spellbooks:portal` (se NÃO EXTRAÍDO, consultar registry).
- **Config na classe:** minRarity `UNCOMMON`, maxLevel `3`, cooldown segundos `180`, cast `INSTANT`.
- **Campos Java:** `baseManaCost`=`200`; `manaCostPerLevel`=`10`; `baseSpellPower`=`5 * 60`; `spellPowerPerLevel`=`2 * 60`; `castTime`=`0`.
- **Métodos-chave:** `getDefaultConfig()`, `getCastType()`, `getSpellResource()`, `getEmptyCastData()`, `getRecastCount()`, `getTargetBlock()`, `checkPreCastConditions()`, `onCast()`, `handleBlockPortal()`, `handleEntityPortal()`, `onRecastFinished()`, `getRecastDuration()`, `getPortalDuration()`, `getCastDistance()`, `getUniqueInfo()`.
- **Fórmulas numéricas de retorno direto:** `getRecastCount = PORTAL_RECAST_COUNT`; `getRecastDuration = 20 * 120`; `getPortalDuration = (int) (getSpellPower(spellLevel, caster) * 20)`; `getCastDistance = 48`. Não são fórmulas completas de efeitos condicionais.
- **Pistas de efeito e targeting no source:** `addFreshEntity`, `PortalManager`.

**Para o Codex:** seguir `onCast` e métodos auxiliares até as classes que realmente aplicam dano/efeito. Campos extraídos documentam defaults, não a configuração efetiva no servidor. `getSpellPower` consulta atributos e escola nativos; eventos genéricos não demonstram modificabilidade de raio, quantidade ou alvo. Requer adapter/contrato real, cap, causalidade e fail-closed. Iron's mantém cast/custo/cooldown; RPG Skill Tree, perks/Mastery/gates; Black Arcana, o runtime mágico próprio. ⚠️ Auditoria estática sem testes físicos. [Especificação](../TECHNICAL-PERK-MAP.md).
