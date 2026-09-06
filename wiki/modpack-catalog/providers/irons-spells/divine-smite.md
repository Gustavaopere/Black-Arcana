# Divine Smite

- **Status no modpack:** PRESENTE — ativo no catálogo atual
- **Provider:** Iron's Spells 'n Spellbooks
- **Mod ID:** `irons_spellbooks`
- **Spell ID:** `irons_spellbooks:divine_smite`
- **JAR/versão:** `irons_spellbooks-1.21.1-3.16.3.jar` / `1.21.1-3.16.3`
- **Escola:** Holy
- **Níveis:** 1–5
- **Raridade:** Common → Legendary
- **Cast:** Long
- **Cast time auditado:** 16 ticks
- **Mana:** 30–90
- **Cooldown:** 15 s
- **Dano Holy base atual:** 8–20
- **Interrupção:** não interrompível pelo método do spell
- **Cast-time scaling:** deliberadamente ignorado pelo provider para preservar o timing melee

## O que faz

Executa um ataque melee em área imbuído de energia Holy.

## Source audit 3.16.3

- spell power Holy: base 8, +3/level;
- avanço/raycast curto: ~1,7 bloco;
- raio de impacto: 2,2 blocos;
- exige line of sight para cada entidade atingida;
- fórmula auditada: `damage = HolySpellPower + weaponDamage + SmiteEnchantmentContribution`;
- quando o dano confirma, aplica efeitos pós-ataque de enchantment.

VFX/animação auditados: blastwave Holy, 50 electric sparks, camera shake, sons próprios de windup/cast e `OVERHEAD_MELEE_SWING_ANIMATION`.

## Deduplicação / causalidade

Já cobre smite Holy melee dependente da arma. Uma bridge deve preservar um único evento causal de cast/ataque; não reaplicar weapon damage, Smite contribution ou enchantment post-hit em um segundo pipeline.

## Fonte / evidência

- Catálogo oficial atual: `https://iron.wiki/spells/`
- Source audit canônico: `wiki/providers/irons-spellbooks/spells/holy/divine-smite.md`
- Consulta: 2026-09-06.
