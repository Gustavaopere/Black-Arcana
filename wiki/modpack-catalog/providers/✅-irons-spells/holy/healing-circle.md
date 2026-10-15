# Healing Circle

- **Status no modpack:** PRESENTE — ativo no catálogo atual
- **Provider:** Iron's Spells 'n Spellbooks
- **Mod ID:** `irons_spellbooks`
- **Spell ID:** `irons_spellbooks:healing_circle`
- **JAR/versão:** `irons_spellbooks-1.21.1-3.16.3.jar` / `1.21.1-3.16.3`
- **Escola:** Holy
- **Níveis:** 1–10
- **Raridade:** Common → Legendary
- **Cast:** Long
- **Cast time auditado:** 20 ticks
- **Mana:** 40–130
- **Cooldown:** 25 s
- **Cura AOE atual:** 0,5–2,75
- **Raio:** 5 blocos
- **Duração:** 200 ticks / 10 s
- **Targeting auditado:** entidade ou ponto até 32 blocos

## O que faz

Cria uma área circular estacionária de magia Holy no alvo/ponto selecionado, curando aliados dentro dela.

## Source audit 3.16.3

- spell power: base 2, +1/level;
- cria `HealingAoe` circular;
- healing value: `getSpellPower(level, caster) * 0.25` por settlement definido pela entidade do provider;
- previsualização: `TargetedAreaEntity` com fade.

## Targets / PvP / bosses / summons

- **Posicionamento confirmado:** entidade ou ponto até 32 blocos.
- **Área confirmada:** `HealingAoe` com raio 5 e duração 200 ticks.
- **Elegibilidade exata de players/PvP, bosses e summons dentro da área:** `NÃO VERIFICADO`; permanece authority da `HealingAoe`.
- Não reconstruir por fora a lista de entidades curáveis.

## Obtenção, requisitos e aprendizado

- **Pipeline geral:** segue o sistema de scrolls/spellbooks do Iron's.
- **Rotas específicas de loot/trade/craft/recompensa:** `NÃO VERIFICADO`.
- **Condições/requisitos adicionais:** `NÃO VERIFICADO`.
- **Itens/focus/rituais específicos além do pipeline normal do provider:** `NÃO VERIFICADO`.

## Integrações / QA / fail-closed

- **Area/settlement authority:** `HealingAoe`.
- **Bridge específica de aquisição/casting:** `NÃO VERIFICADO`.
- **VFX final além da previsualização, animação/áudio e QA client/modpack real:** `NÃO VERIFICADO`.
- Não criar uma segunda healing AoE nem contabilizar o mesmo tick de cura duas vezes.

## Deduplicação / área persistente

Já cobre healing AoE Holy estacionário. Uma futura zona consagrada só representa lacuna se tiver semântica adicional real — ward, exorcismo, anti-infernal, julgamento etc. — e não apenas outro campo de cura.

## Fonte / evidência

- Catálogo oficial atual: `https://iron.wiki/spells/`
- Source audit canônico: `wiki/modpack-catalog/providers/irons-spells/audits/source-3.16.3/spells/holy/healing-circle.md`
- Consulta: 2026-09-06.

## Parâmetros de implementação para perks — source auditado

- **Classe/commit:** [`HealingCircleSpell.java`](https://github.com/iron431/irons-spells-n-spellbooks/blob/e4056af90302d37eb1739f5ff05020b020e6e252/src/main/java/io/redspace/ironsspellbooks/spells/holy/HealingCircleSpell.java) (source fixo 1.21.1-3.16.3).
- **ID de spell lido na classe:** `irons_spellbooks:healing_circle` (NÃO EXTRAÍDO implica revisar registry).
- **Config:** minRarity `COMMON`; maxLevel `10`; cooldown `25` segundos; cast `LONG`.
- **Campos Java:** `baseManaCost`=`40`; `manaCostPerLevel`=`10`; `baseSpellPower`=`2`; `spellPowerPerLevel`=`1`; `castTime`=`20`.
- **Métodos no código:** `getUniqueInfo()`, `getCastType()`, `getDefaultConfig()`, `getSpellResource()`, `getCastStartSound()`, `checkPreCastConditions()`, `onCast()`, `getHealing()`, `getRadius()`, `getDuration()`, `getCastStartAnimation()`, `getTargetingColor()`.
- **Fórmulas numéricas com retorno direto:** `getHealing = getSpellPower(spellLevel, caster) * .25f`; `getRadius = 5`; `getDuration = 200`. Não são fórmulas completas de efeitos indiretos.
- **Pistas de execução (verificar semântica):** `RaycastBuilder`, `TargetEntityCastData`, `addFreshEntity`.

**Contrato de perks:** escola `holy` não prova dano, cura ou imunidade universais. Inspecionar fonte de dano/cura e estado persistente do efeito nativo antes de modificar duração, alcance e alvo. Atributo provider-native e patch em entidade/efeito são integrações diferentes; requerem evento/hook real, caps e prevenção de duplicidade. Sem hook: ⚠️ condicionado/fail-closed. Iron's é autoridade do cast e mana; RPG Skill Tree, perks/Mastery/gates; Black Arcana, seu runtime mágico. QA real pendente. [Mapa global](../TECHNICAL-PERK-MAP.md).
