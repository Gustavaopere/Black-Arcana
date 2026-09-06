# Cleanse

- **Status no modpack:** PRESENTE — spell ativo no catálogo atual
- **Provider:** Iron's Spells 'n Spellbooks
- **Mod ID:** `irons_spellbooks`
- **Spell ID auditado:** `irons_spellbooks:cleanse`
- **JAR/versão:** `irons_spellbooks-1.21.1-3.16.3.jar` / `1.21.1-3.16.3`
- **Escola:** Holy
- **Nível:** 1
- **Raridade:** Epic
- **Cast:** Long — 60 ticks auditados
- **Mana:** 100
- **Cooldown:** 60 s
- **Raio:** 3 blocos

## O que faz

Purifica o caster e aliados elegíveis próximos, removendo efeitos nocivos.

## Runtime auditado

O source 3.16.3 busca living entities numa caixa 6×6×6 centrada no caster, filtra aliados/elegíveis com `Utils.shouldHealEntity`, remove efeitos de categoria `MobEffectCategory.HARMFUL` e preserva efeitos marcados com `ModTags.CLEANSE_IMMUNE`.

## VFX / animação

O pre-cast cria `TargetedAreaEntity` de raio 3. A auditoria registra `CAST_KNEELING_PRAYER` no início e `SELF_CAST_TWO_HANDS` ao finalizar, além de partículas de cleanse.

## Deduplicação

Já ocupa a purificação Holy genérica de efeitos harmful. Exorcismo continua sendo possível como delta somente quando operar sobre semânticas causais específicas — possession, demon, spirit, curse — e não como segunda remoção indiscriminada de debuffs.

## Fonte / evidência

- Catálogo oficial atual: `https://iron.wiki/spells/`.
- Auditoria source 3.16.3: `wiki/providers/irons-spellbooks/spells/holy/cleanse.md`.