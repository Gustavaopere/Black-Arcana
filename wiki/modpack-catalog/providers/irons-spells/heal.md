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
- Source audit canônico: `wiki/providers/irons-spellbooks/spells/holy/heal.md`
- Consulta: 2026-09-06.
