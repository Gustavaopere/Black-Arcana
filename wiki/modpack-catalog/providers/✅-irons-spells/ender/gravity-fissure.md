# Gravity Fissure

- **Status no modpack:** PRESENTE — provider instalado
- **Provider:** Iron's Spells 'n Spellbooks
- **Mod ID:** `irons_spellbooks`
- **JAR/versão:** `irons_spellbooks-1.21.1-3.16.3.jar` / `1.21.1-3.16.3`
- **Escola:** Ender
- **Níveis:** 1–5
- **Raridade:** Epic → Legendary
- **Cast:** Long
- **Mana:** 150–250
- **Cooldown:** 45 s
- **Raio:** 3,5 blocos
- **Duração:** 3–7 s
- **Dano direto listado:** nenhum

## O que faz

Cria uma fissura gravitacional móvel que avança em linha e puxa criaturas próximas para seu poço gravitacional sem aplicar dano direto listado pelo catálogo atual.

## Escalonamento

A duração cresce de 3 para 7 segundos. O raio listado permanece 3,5 blocos. Força exata de atração, velocidade da fissura e regras internas de imunidade ficam `NÃO VERIFICADO`.

## Obtenção e aprendizado

Segue o pipeline geral de scrolls/spellbooks do Iron's. Fontes específicas de loot/crafting permanecem `NÃO VERIFICADO`.

## Deduplicação

Já cobre controle gravitacional móvel sem dano. É bloqueio direto para qualquer candidato de Caos/Ordem que apenas replique "campo móvel que puxa inimigos".

## VFX / animação / áudio

`NÃO VERIFICADO` no runtime real do pack neste passe.

## Fonte / evidência

Catálogo oficial atual: `https://iron.wiki/spells/` — consulta em 2026-09-06.

## Parâmetros de implementação para perks — source auditado

- **Classe/commit:** [`GravityFissureSpell.java`](https://github.com/iron431/irons-spells-n-spellbooks/blob/e4056af90302d37eb1739f5ff05020b020e6e252/src/main/java/io/redspace/ironsspellbooks/spells/ender/GravityFissureSpell.java), pin `e4056af90302d37eb1739f5ff05020b020e6e252` (Iron's 1.21.1-3.16.3).
- **ID no source:** `irons_spellbooks:gravity_fissure`; escola `ender`.
- **Config na classe:** minRarity `EPIC`, maxLevel `5`, cooldown `45` segundos, cast `LONG`.
- **Campos Java:** `baseManaCost`=`150`; `manaCostPerLevel`=`25`; `baseSpellPower`=`3`; `spellPowerPerLevel`=`1`; `castTime`=`15`.
- **Métodos para localizar no Codex:** `getUniqueInfo()`, `getCastType()`, `getDefaultConfig()`, `getSpellResource()`, `getCastStartSound()`, `getCastFinishSound()`, `onCast()`, `getRadius()`, `getDurationTicks()`, `getCastStartAnimation()`, `getCastFinishAnimation()`.
- **Fórmulas com retorno numérico direto verificadas nesta classe:** `getRadius = 3.5f`; `getDurationTicks = (int) (getSpellPower(spellLevel, entity) * 20)`. Essas fórmulas não cobrem cálculos imperativos ou de entidades auxiliares.
- **Pistas técnicas detectadas:** `addFreshEntity`; verificar semântica na classe.

**Orientação para perks:** estudar as chamadas de `onCast`, `checkPreCastConditions` e os métodos acima antes de alterar alvo/raio/duração/dano; `getSpellPower` e custo aplicam config/atributos nativos. A disponibilidade de eventos genéricos não comprova alteração de variáveis locais ou entidades. Sem adapter verificado, **⚠️ condicionado / fail-closed**. Preserve casting do Iron's, Mastery/perks/gates do RPG Skill Tree e runtime próprio do Black Arcana. Registro estático, sem QA físico. [Contrato de referência](../TECHNICAL-PERK-MAP.md).
