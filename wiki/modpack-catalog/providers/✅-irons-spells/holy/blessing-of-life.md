# Blessing Of Life

- **Status no modpack:** PRESENTE — ativo no catálogo atual
- **Provider:** Iron's Spells 'n Spellbooks
- **Mod ID:** `irons_spellbooks`
- **Spell ID:** `irons_spellbooks:blessing_of_life`
- **JAR/versão:** `irons_spellbooks-1.21.1-3.16.3.jar` / `1.21.1-3.16.3`
- **Escola:** Holy
- **Níveis:** 1–10
- **Raridade:** Common → Legendary
- **Cast:** Long
- **Cast time auditado:** 30 ticks
- **Mana:** 10–55
- **Cooldown:** 10 s
- **Cura atual:** 6–15
- **Target helper auditado:** até 64 blocos

## O que faz

Seleciona uma criatura e, ao completar o cast, cura o alvo.

## Source audit 3.16.3

- spell power: base 6, +1/level;
- com `TargetEntityCastData` válido: `healAmount = getSpellPower(level, caster)`;
- publica `SpellHealEvent(caster, target, healAmount, HOLY)` antes da cura;
- aplica a cura e envia `HealParticlesPacket`.

## Targets / PvP / bosses / summons

- **Target confirmado:** entidade válida via `TargetEntityCastData`, com helper até 64 blocos.
- **Elegibilidade exata de player aliado/PvP, boss e summon:** `NÃO VERIFICADO` neste passe; não inferir a policy apenas do conceito de “aliado”.
- Bridges devem respeitar o target aceito pelo provider e o `SpellHealEvent`; não ampliar a elegibilidade por conta própria.

## Obtenção, requisitos e aprendizado

- **Pipeline geral:** segue o sistema de scrolls/spellbooks do Iron's.
- **Rotas específicas de loot/trade/craft/recompensa:** `NÃO VERIFICADO`.
- **Condições/requisitos adicionais:** `NÃO VERIFICADO`.
- **Itens/focus/rituais específicos além do pipeline normal do provider:** `NÃO VERIFICADO`.

## Integrações / QA / fail-closed

- **Hook causal comprovado:** `SpellHealEvent`.
- **Bridge específica de aquisição/casting:** `NÃO VERIFICADO`.
- **VFX final além de `HealParticlesPacket`, textura/animação/áudio:** `NÃO VERIFICADO`.
- **QA client/modpack real e exceções de target:** `NÃO VERIFICADO`; falhar fechado em vez de inventar elegibilidade.

## Deduplicação / causalidade

Já cobre cura Holy de alvo único. O `SpellHealEvent` é o hook causal preferível para integrações; não inferir uma segunda cura por diferença de HP nem executar settlement paralelo.

## Fonte / evidência

- Catálogo oficial atual: `https://iron.wiki/spells/`
- Source audit canônico: `wiki/modpack-catalog/providers/irons-spells/audits/source-3.16.3/spells/holy/blessing-of-life.md`
- Consulta: 2026-09-06.

## Parâmetros de implementação para perks — source auditado

- **Classe/commit:** [`BlessingOfLifeSpell.java`](https://github.com/iron431/irons-spells-n-spellbooks/blob/e4056af90302d37eb1739f5ff05020b020e6e252/src/main/java/io/redspace/ironsspellbooks/spells/holy/BlessingOfLifeSpell.java) (source fixo 1.21.1-3.16.3).
- **ID de spell lido na classe:** `irons_spellbooks:blessing_of_life` (NÃO EXTRAÍDO implica revisar registry).
- **Config:** minRarity `COMMON`; maxLevel `10`; cooldown `10` segundos; cast `LONG`.
- **Campos Java:** `baseManaCost`=`10`; `manaCostPerLevel`=`5`; `baseSpellPower`=`6`; `spellPowerPerLevel`=`1`; `castTime`=`30`.
- **Métodos no código:** `getUniqueInfo()`, `getCastType()`, `getDefaultConfig()`, `getSpellResource()`, `checkPreCastConditions()`, `onCast()`, `getTargetingColor()`.
- **Fórmulas numéricas com retorno direto:** não extraídas; examinar lógica e entidades auxiliares. Não são fórmulas completas de efeitos indiretos.
- **Pistas de execução (verificar semântica):** `RaycastBuilder`, `TargetEntityCastData`.

**Contrato de perks:** escola `holy` não prova dano, cura ou imunidade universais. Inspecionar fonte de dano/cura e estado persistente do efeito nativo antes de modificar duração, alcance e alvo. Atributo provider-native e patch em entidade/efeito são integrações diferentes; requerem evento/hook real, caps e prevenção de duplicidade. Sem hook: ⚠️ condicionado/fail-closed. Iron's é autoridade do cast e mana; RPG Skill Tree, perks/Mastery/gates; Black Arcana, seu runtime mágico. QA real pendente. [Mapa global](../TECHNICAL-PERK-MAP.md).
