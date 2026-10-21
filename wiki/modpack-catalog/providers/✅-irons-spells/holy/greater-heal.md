# Greater Heal

- **Status no modpack:** PRESENTE — ativo no catálogo atual
- **Provider:** Iron's Spells 'n Spellbooks
- **Mod ID:** `irons_spellbooks`
- **Spell ID:** `irons_spellbooks:greater_heal`
- **JAR/versão:** `irons_spellbooks-1.21.1-3.16.3.jar` / `1.21.1-3.16.3`
- **Escola:** Holy
- **Níveis:** 1
- **Raridade:** Rare
- **Cast:** Long
- **Cast time auditado:** 120 ticks
- **Mana:** 100
- **Cooldown:** 45 s
- **Cura pública:** Max Healing / full self-heal

## O que faz

Ao completar o cast, tenta restaurar a vida do caster até o máximo.

## Source audit 3.16.3

- `healAmount = caster.getMaxHealth()`;
- publica `SpellHealEvent(caster, caster, healAmount, HOLY)` antes da cura;
- executa `caster.heal(healAmount)`;
- envia `HealParticlesPacket`.

O resultado final continua sujeito à semântica normal de `heal` da entidade/provider; não inventamos comportamento adicional de overheal.

## Targets / PvP / bosses / summons

- **Target confirmado:** o próprio caster.
- **PvP:** não possui target ofensivo direto; interações indiretas ficam `NÃO VERIFICADO`.
- **Bosses/summons:** `NÃO VERIFICADO` — não são targets primários deste self-heal.
- **Overheal/absorção:** não confirmado; não inferir além de `caster.heal`.

## Obtenção, requisitos e aprendizado

- **Pipeline geral:** segue o sistema de scrolls/spellbooks do Iron's.
- **Rotas específicas de loot/trade/craft/recompensa:** `NÃO VERIFICADO`.
- **Condições/requisitos adicionais:** `NÃO VERIFICADO`.
- **Itens/focus/rituais específicos além do pipeline normal do provider:** `NÃO VERIFICADO`.

## Integrações / QA / fail-closed

- **Hook causal comprovado:** `SpellHealEvent`.
- **Bridge específica de aquisição/casting:** `NÃO VERIFICADO`.
- **VFX final além de `HealParticlesPacket`, animação/áudio e QA client/modpack real:** `NÃO VERIFICADO`.
- Não conceder segunda cura, overheal ou sustain credit sem hook causal adicional comprovado.

## Deduplicação / causalidade

Já cobre full self-heal Holy preparado. O `SpellHealEvent` é o boundary causal preferível; nenhuma integração deve converter o mesmo cast em uma segunda cura ou sustain credit paralelo.

## Fonte / evidência

- Catálogo oficial atual: `https://iron.wiki/spells/`
- Source audit canônico: `wiki/modpack-catalog/providers/irons-spells/audits/source-3.16.3/spells/holy/greater-heal.md`
- Consulta: 2026-09-06.

## Parâmetros de implementação para perks — source auditado

- **Classe/commit:** [`GreaterHealSpell.java`](https://github.com/iron431/irons-spells-n-spellbooks/blob/e4056af90302d37eb1739f5ff05020b020e6e252/src/main/java/io/redspace/ironsspellbooks/spells/holy/GreaterHealSpell.java) (source fixo 1.21.1-3.16.3).
- **ID de spell lido na classe:** `irons_spellbooks:greater_heal` (NÃO EXTRAÍDO implica revisar registry).
- **Config:** minRarity `RARE`; maxLevel `1`; cooldown `45` segundos; cast `LONG`.
- **Campos Java:** `baseManaCost`=`100`; `manaCostPerLevel`=`0`; `baseSpellPower`=`0`; `spellPowerPerLevel`=`0`; `castTime`=`120`.
- **Métodos no código:** `getUniqueInfo()`, `getCastType()`, `getDefaultConfig()`, `getSpellResource()`, `onCast()`.
- **Fórmulas numéricas com retorno direto:** não extraídas; examinar lógica e entidades auxiliares. Não são fórmulas completas de efeitos indiretos.
- **Pistas de execução (verificar semântica):** nenhuma das pistas-padrão extraída.

**Contrato de perks:** escola `holy` não prova dano, cura ou imunidade universais. Inspecionar fonte de dano/cura e estado persistente do efeito nativo antes de modificar duração, alcance e alvo. Atributo provider-native e patch em entidade/efeito são integrações diferentes; requerem evento/hook real, caps e prevenção de duplicidade. Sem hook: ⚠️ condicionado/fail-closed. Iron's é autoridade do cast e mana; RPG Skill Tree, perks/Mastery/gates; Black Arcana, seu runtime mágico. QA real pendente. [Mapa global](../TECHNICAL-PERK-MAP.md).
