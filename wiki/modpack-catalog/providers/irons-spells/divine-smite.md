# Divine Smite

- **Status no modpack:** PRESENTE — spell ativo no catálogo atual
- **Provider:** Iron's Spells 'n Spellbooks
- **Mod ID:** `irons_spellbooks`
- **Spell ID auditado:** `irons_spellbooks:divine_smite`
- **JAR/versão:** `irons_spellbooks-1.21.1-3.16.3.jar` / `1.21.1-3.16.3`
- **Escola:** Holy
- **Níveis:** 1–5
- **Raridade:** Common → Legendary
- **Cast:** Long — 16 ticks auditados
- **Mana:** 30–90
- **Cooldown:** 15 s
- **Dano Holy público atual:** 8–20
- **Interruptibilidade:** uninterruptible

## O que faz

Executa um ataque melee em área imbuído de energia Holy. O dano escala com o dano melee e encantamentos da arma empunhada.

## Runtime auditado

O source 3.16.3 registra avanço/raycast curto de aproximadamente 1,7 bloco, raio de impacto 2,2 blocos e line of sight por entidade. A composição é `HolySpellPower + weaponDamage + SmiteEnchantmentContribution`; efeitos pós-ataque de enchantment são aplicados quando o dano confirma. O spell deliberadamente ignora cast-time scaling para preservar o timing da animação melee.

## VFX / animação

A auditoria registra blastwave Holy, 50 electric sparks, camera shake, sons próprios de windup/cast e `OVERHEAD_MELEE_SWING_ANIMATION`.

## Deduplicação / authority

Já cobre smite melee Holy com weapon scaling. Black Arcana não deve recalcular weapon/enchantment contribution por um segundo pipeline. Um futuro julgamento Celestial precisa de condição/alvo/recurso/semântica distintos.

## Fonte / evidência

- Catálogo oficial atual: `https://iron.wiki/spells/`.
- Auditoria source 3.16.3: `wiki/providers/irons-spellbooks/spells/holy/divine-smite.md`.