# Black Hole

- **Provider:** Iron's Spells 'n Spellbooks
- **Escola:** Ender
- **Níveis:** 1–6
- **Raridade:** Legendary
- **Cast:** Long
- **Mana:** 300–800
- **Cooldown:** 120 s
- **Dano AOE listado:** 2
- **Raio:** 6–16 blocos

## O que faz

Abre uma fissura localizada que manifesta uma singularidade, puxando criaturas próximas para o centro e causando dano em área ao longo do efeito.

## Escalonamento

Raio e custo crescem com o nível. Duração/frequência de dano e regras exatas de força gravitacional ainda serão normalizadas.

## Obtenção e aprendizado

Pipeline padrão do Iron's; Ender Pearl é o Focus da escola Ender.

## Deduplicação

É bloqueio direto para qualquer “buraco negro” novo em Caos/Ordem. Gravity Fissure cobre a variante móvel sem dano.

## VFX / animação / áudio

A catalogar no runtime.

## Fonte

`https://iron.wiki/spells/`.

## Parâmetros de implementação para perks — source auditado

- **Classe/commit:** [`BlackHoleSpell.java`](https://github.com/iron431/irons-spells-n-spellbooks/blob/e4056af90302d37eb1739f5ff05020b020e6e252/src/main/java/io/redspace/ironsspellbooks/spells/ender/BlackHoleSpell.java), pin `e4056af90302d37eb1739f5ff05020b020e6e252` (Iron's 1.21.1-3.16.3).
- **ID no source:** `irons_spellbooks:black_hole`; escola `ender`.
- **Config na classe:** minRarity `LEGENDARY`, maxLevel `6`, cooldown `120` segundos, cast `LONG`.
- **Campos Java:** `baseManaCost`=`300`; `manaCostPerLevel`=`100`; `baseSpellPower`=`1`; `spellPowerPerLevel`=`0`; `castTime`=`100`.
- **Métodos para localizar no Codex:** `getUniqueInfo()`, `getCastType()`, `getDefaultConfig()`, `getSpellResource()`, `getCastStartSound()`, `getCastFinishSound()`, `onCast()`, `getDamage()`, `getRadius()`, `getCastStartAnimation()`, `getCastFinishAnimation()`.
- **Fórmulas com retorno numérico direto verificadas nesta classe:** `getDamage = getSpellPower(spellLevel, entity) * 2`; `getRadius = (2 * spellLevel + 4) + (3 * (getSpellPower(spellLevel, entity) - 1))`. Essas fórmulas não cobrem cálculos imperativos ou de entidades auxiliares.
- **Pistas técnicas detectadas:** `RaycastBuilder`, `addFreshEntity`; verificar semântica na classe.

**Orientação para perks:** estudar as chamadas de `onCast`, `checkPreCastConditions` e os métodos acima antes de alterar alvo/raio/duração/dano; `getSpellPower` e custo aplicam config/atributos nativos. A disponibilidade de eventos genéricos não comprova alteração de variáveis locais ou entidades. Sem adapter verificado, **⚠️ condicionado / fail-closed**. Preserve casting do Iron's, Mastery/perks/gates do RPG Skill Tree e runtime próprio do Black Arcana. Registro estático, sem QA físico. [Contrato de referência](../TECHNICAL-PERK-MAP.md).
