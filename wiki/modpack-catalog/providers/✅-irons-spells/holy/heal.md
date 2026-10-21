# Heal

- **Status no modpack:** PRESENTE — ativo no catálogo atual
- **Provider:** Iron's Spells 'n Spellbooks
- **Mod ID:** `irons_spellbooks`
- **Spell ID:** `irons_spellbooks:heal`
- **JAR/versão:** `irons_spellbooks-1.21.1-3.16.3.jar` / `1.21.1-3.16.3`
- **Escola:** Holy
- **Níveis:** 1–8
- **Raridade:** Uncommon → Legendary
- **Cast:** Instant
- **Mana:** 30–135
- **Cooldown:** 30 s
- **Cura atual:** 5–12

## O que faz

Cura imediatamente o próprio caster.

## Source audit 3.16.3

- spell power: base 5, +1/level;
- `healAmount = getSpellPower(level, caster)`;
- antes de `caster.heal`, publica `SpellHealEvent(caster, caster, healAmount, HOLY)`;
- VFX: círculo de 16 partículas `HEART`;
- animação: `SELF_CAST_ANIMATION`.

## Targets / PvP / bosses / summons

- **Target confirmado:** o próprio caster.
- **PvP:** não possui target ofensivo direto; interações indiretas ficam `NÃO VERIFICADO`.
- **Bosses/summons:** `NÃO VERIFICADO` — não são targets primários deste self-heal.
- **Overheal/absorção:** `NÃO VERIFICADO`; não inferir além do heal normal do provider.

## Obtenção, requisitos e aprendizado

- **Pipeline geral:** segue o sistema de scrolls/spellbooks do Iron's.
- **Rotas específicas de loot/trade/craft/recompensa:** `NÃO VERIFICADO`.
- **Condições/requisitos adicionais:** `NÃO VERIFICADO`.
- **Itens/focus/rituais específicos além do pipeline normal do provider:** `NÃO VERIFICADO`.

## Integrações / QA / fail-closed

- **Hook causal comprovado:** `SpellHealEvent`.
- **Bridge específica de aquisição/casting:** `NÃO VERIFICADO`.
- **Áudio/textura final e QA client/modpack real:** `NÃO VERIFICADO`; VFX/animação source-auditados estão registrados acima.
- Não gerar segunda cura, lifesteal ou sustain credit para o mesmo settlement.

## Deduplicação / causalidade

Já cobre self-heal instantâneo Holy. Quando uma perk precisa de causalidade de cura, deve preferir `SpellHealEvent` a inferir healing por diferença de HP. Não gerar segunda cura, lifesteal ou sustain credit para o mesmo settlement.

## Fonte / evidência

- Catálogo oficial atual: `https://iron.wiki/spells/`
- Source audit canônico: `wiki/modpack-catalog/providers/irons-spells/audits/source-3.16.3/spells/holy/heal.md`
- Consulta: 2026-09-06.

## Parâmetros de implementação para perks — source auditado

- **Classe/commit:** [`HealSpell.java`](https://github.com/iron431/irons-spells-n-spellbooks/blob/e4056af90302d37eb1739f5ff05020b020e6e252/src/main/java/io/redspace/ironsspellbooks/spells/holy/HealSpell.java) (source fixo 1.21.1-3.16.3).
- **ID de spell lido na classe:** `irons_spellbooks:heal` (NÃO EXTRAÍDO implica revisar registry).
- **Config:** minRarity `UNCOMMON`; maxLevel `8`; cooldown `30` segundos; cast `INSTANT`.
- **Campos Java:** `baseManaCost`=`30`; `manaCostPerLevel`=`15`; `baseSpellPower`=`5`; `spellPowerPerLevel`=`1`; `castTime`=`0`.
- **Métodos no código:** `getUniqueInfo()`, `getCastType()`, `getDefaultConfig()`, `getSpellResource()`, `onCast()`, `getCastStartAnimation()`.
- **Fórmulas numéricas com retorno direto:** não extraídas; examinar lógica e entidades auxiliares. Não são fórmulas completas de efeitos indiretos.
- **Pistas de execução (verificar semântica):** nenhuma das pistas-padrão extraída.

**Contrato de perks:** escola `holy` não prova dano, cura ou imunidade universais. Inspecionar fonte de dano/cura e estado persistente do efeito nativo antes de modificar duração, alcance e alvo. Atributo provider-native e patch em entidade/efeito são integrações diferentes; requerem evento/hook real, caps e prevenção de duplicidade. Sem hook: ⚠️ condicionado/fail-closed. Iron's é autoridade do cast e mana; RPG Skill Tree, perks/Mastery/gates; Black Arcana, seu runtime mágico. QA real pendente. [Mapa global](../TECHNICAL-PERK-MAP.md).
