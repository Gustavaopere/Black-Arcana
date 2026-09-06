# Fortify

- **Status no modpack:** PRESENTE — spell ativo no catálogo atual
- **Provider:** Iron's Spells 'n Spellbooks
- **Mod ID:** `irons_spellbooks`
- **Spell ID auditado:** `irons_spellbooks:fortify`
- **JAR/versão:** `irons_spellbooks-1.21.1-3.16.3.jar` / `1.21.1-3.16.3`
- **Escola:** Holy
- **Níveis:** 1–10
- **Raridade:** Common → Legendary
- **Cast:** Long — 60 ticks auditados
- **Mana:** 80–170
- **Cooldown:** 180 s
- **Temporary HP público atual:** 6–15
- **Raio:** 8 blocos

## O que faz

Fortifica criaturas amigáveis ao redor do caster, concedendo temporary HP/absorção.

## Runtime auditado

O source 3.16.3 usa `Utils.shouldHealEntity` para selecionar entidades elegíveis dentro de 8 blocos e aplica `MobEffectRegistry.FORTIFY` por 2400 ticks (120 s). O amplifier é derivado de `(int)getSpellPower - 1`.

## VFX

O pre-cast usa `TargetedAreaEntity` de raio 8; o runtime envia `AbsorptionParticlesPacket` por alvo e `FortifyAreaParticlesPacket` para a área.

## Deduplicação

Já cobre proteção Holy de grupo via absorção/fortificação. Intercessão Celestial futura precisa de outro contrato — por exemplo prevenção condicionada de evento ou Sanctum — e não apenas mais temporary HP.

## Fonte / evidência

- Catálogo oficial atual: `https://iron.wiki/spells/`.
- Auditoria source 3.16.3: `wiki/providers/irons-spellbooks/spells/holy/fortify.md`.