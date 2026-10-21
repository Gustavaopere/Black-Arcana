# Teleport

- **Status no modpack:** PRESENTE — provider instalado
- **Provider:** Iron's Spells 'n Spellbooks
- **Mod ID:** `irons_spellbooks`
- **JAR/versão:** `irons_spellbooks-1.21.1-3.16.3.jar` / `1.21.1-3.16.3`
- **Escola:** Ender
- **Níveis:** 1–5
- **Raridade:** Uncommon → Legendary
- **Cast:** Instant
- **Mana:** 20–40
- **Cooldown:** 6 s
- **Alcance:** 8–16 blocos

## O que faz

Teleporta instantaneamente o caster para o ponto válido indicado pela mira, deixando o efeito visual Ender descrito pelo provider.

## Escalonamento

O catálogo oficial atual confirma alcance de 8 a 16 blocos e mana de 20 a 40. A página histórica 1.19 ainda exibe números antigos diferentes; ela não é usada como authority para a build atual 1.21.1-3.16.3.

## Obtenção e aprendizado

Segue o pipeline geral de scrolls/spellbooks do Iron's. Fontes específicas de loot/crafting permanecem `NÃO VERIFICADO`.

## Deduplicação

Já cobre blink/teleporte curto direcionado pela mira. Uma magia Black Arcana equivalente não possui delta mecânico apenas por usar VFX sombrio, portal ou outra nomenclatura.

## Authority / world safety

O provider é authority da resolução deste spell. Integrações não devem executar um segundo teleporte ou contornar validação de destino/chunk/world-safety.

## VFX / animação / áudio

A descrição pública confirma uma nuvem de energia Ender; detalhes de partículas, animação e áudio do runtime real do pack ficam `NÃO VERIFICADO`.

## Fonte / evidência

- Catálogo oficial atual: `https://iron.wiki/spells/` — consulta em 2026-09-06.
- Changelog oficial atual registra nerf de mana na linha recente: `https://iron.wiki/changelog/`.

## Parâmetros de implementação para perks — source auditado

- **Classe:** [`TeleportSpell.java`](https://github.com/iron431/irons-spells-n-spellbooks/blob/e4056af90302d37eb1739f5ff05020b020e6e252/src/main/java/io/redspace/ironsspellbooks/spells/ender/TeleportSpell.java) (`iron431@e4056af90302d37eb1739f5ff05020b020e6e252`, versão 1.21.1-3.16.3).
- **ID no source:** `teleport` (namespace esperado Iron's; confirmar no registry se não extraído).
- **DefaultConfig:** minRarity `UNCOMMON`; maxLevel `5`; cooldown `6` s; cast `INSTANT`.
- **Campos Java:** `baseManaCost`=`20`; `manaCostPerLevel`=`5`; `baseSpellPower`=`8`; `spellPowerPerLevel`=`2`; `castTime`=`0`.
- **Métodos de efeito/seleção:** `getDefaultConfig()`, `getCastType()`, `getSpellResource()`, `getCastStartSound()`, `getCastFinishSound()`, `onCast()`, `getDistance()`, `getTeleportTargetPosition()`, `getUniqueInfo()`, `getCastStartAnimation()`.
- **Fórmulas diretas localizadas:** `getDistance = (float) (Utils.softCapFormula(getEntityPowerMultiplier(sourceEntity)) * getSpellPower(spellLevel, null))`.
- **Pistas de código:** `TeleportData`, `handleSpellTeleport`.

**Regra de integração:** dados estáticos e nomes reais são pontos de entrada para o Codex; quantidades e alcance devem ser verificados no helper ou entidade que aplica o efeito. Perks/gates/Mastery são do RPG Skill Tree; cast e custos do Iron's; runtime mágico próprio do Black Arcana. Eventos disponíveis não garantem mutabilidade do efeito: sem contrato, fail-closed; caps e prevenção de duplicação são mandatórios. QA real pendente. [Mapa geral](../TECHNICAL-PERK-MAP.md).
