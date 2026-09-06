# Fortify

- **Status no modpack:** PRESENTE — ativo no catálogo atual
- **Provider:** Iron's Spells 'n Spellbooks
- **Mod ID:** `irons_spellbooks`
- **Spell ID:** `irons_spellbooks:fortify`
- **JAR/versão:** `irons_spellbooks-1.21.1-3.16.3.jar` / `1.21.1-3.16.3`
- **Escola:** Holy
- **Níveis:** 1–10
- **Raridade:** Common → Legendary
- **Cast:** Long
- **Cast time auditado:** 60 ticks
- **Mana:** 80–170
- **Cooldown:** 180 s
- **HP temporário atual:** 6–15
- **Raio:** 8 blocos
- **Duração auditada:** 2400 ticks / 120 s

## O que faz

Fortifica living entities amigáveis/elegíveis ao redor do caster, concedendo a absorção/HP temporário exposta pelo provider.

## Source audit 3.16.3

- spell power: base 6, +1/level;
- alvos por `Utils.shouldHealEntity` dentro de 8 blocos;
- aplica `MobEffectRegistry.FORTIFY` por `20*120` ticks;
- amplifier = `(int)getSpellPower - 1`;
- pre-cast mostra `TargetedAreaEntity` de raio 8;
- VFX: `AbsorptionParticlesPacket` por alvo + `FortifyAreaParticlesPacket` na área.

## Targets / PvP / bosses / summons

- **Targeting confirmado:** living entities em 8 blocos filtradas por `Utils.shouldHealEntity`.
- **Players/PvP, bosses e summons:** a elegibilidade específica dentro desse helper fica `NÃO VERIFICADO`; não ampliar a seleção por bridge.
- **Efeito confirmado:** `FORTIFY` por 120 s, amplifier derivado do spell power.

## Obtenção, requisitos e aprendizado

- **Pipeline geral:** segue o sistema de scrolls/spellbooks do Iron's.
- **Rotas específicas de loot/trade/craft/recompensa:** `NÃO VERIFICADO`.
- **Condições/requisitos adicionais:** `NÃO VERIFICADO`.
- **Itens/focus/rituais específicos além do pipeline normal do provider:** `NÃO VERIFICADO`.

## Integrações / QA / fail-closed

- **Authority de seleção:** `Utils.shouldHealEntity`; **authority de efeito:** `MobEffectRegistry.FORTIFY`.
- **Bridge específica de aquisição/casting:** `NÃO VERIFICADO`.
- **Áudio/textura final e QA client/modpack real:** `NÃO VERIFICADO`.
- Não criar uma segunda pool de absorção/temporary HP para o mesmo cast.

## Deduplicação

Já cobre fortificação/absorção Holy em área. Não criar uma segunda camada equivalente de temporary HP sobre o mesmo cast nem duplicar a seleção de aliados em bridge própria.

## Fonte / evidência

- Catálogo oficial atual: `https://iron.wiki/spells/`
- Source audit canônico: `wiki/providers/irons-spellbooks/spells/holy/fortify.md`
- Consulta: 2026-09-06.
