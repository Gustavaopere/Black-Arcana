# Sunbeam

- **Status no modpack:** PRESENTE — spell ativo no catálogo atual
- **Provider:** Iron's Spells 'n Spellbooks
- **Mod ID:** `irons_spellbooks`
- **Spell ID auditado:** `irons_spellbooks:sunbeam`
- **JAR/versão:** `irons_spellbooks-1.21.1-3.16.3.jar` / `1.21.1-3.16.3`
- **Escola:** Holy
- **Níveis:** 1–10
- **Raridade:** Uncommon → Legendary
- **Cast:** Instant
- **Mana:** 40–130
- **Cooldown:** 20 s
- **Dano público atual:** 12–25,5
- **Targeting auditado:** até 48 blocos

## O que faz

Canaliza o poder dos céus em um feixe Holy que desce sobre a área/alvo e causa dano.

## Runtime auditado

O source 3.16.3 cria `SunbeamEntity` na posição resolvida pelo raycast e calcula `damage = getSpellPower(level, caster) * 0.5`. Quando não há target entity, o spell procura uma posição relativa ao chão; o runtime toca `SUNBEAM_WINDUP` na posição criada.

## Deduplicação

Já cobre “raio de luz do céu” ofensivo Holy. Magia Celestial futura precisa adicionar condição celeste, Sanctum/Ressonância, julgamento ou outro contrato real; outro beam com VFX diferente é duplicata.

## Fonte / evidência

- Catálogo oficial atual: `https://iron.wiki/spells/`.
- Auditoria source 3.16.3: `wiki/providers/irons-spellbooks/spells/holy/sunbeam.md`.