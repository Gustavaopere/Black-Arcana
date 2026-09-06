# Healing Circle

- **Status no modpack:** PRESENTE — spell ativo no catálogo atual
- **Provider:** Iron's Spells 'n Spellbooks
- **Mod ID:** `irons_spellbooks`
- **Spell ID auditado:** `irons_spellbooks:healing_circle`
- **JAR/versão:** `irons_spellbooks-1.21.1-3.16.3.jar` / `1.21.1-3.16.3`
- **Escola:** Holy
- **Níveis:** 1–10
- **Raridade:** Common → Legendary
- **Cast:** Long — 20 ticks auditados
- **Mana:** 40–130
- **Cooldown:** 25 s
- **AOE Healing público:** 0,5–2,75
- **Raio:** 5 blocos
- **Duração:** 10 s / 200 ticks

## O que faz

Cria um círculo estacionário de magia Holy em criatura ou ponto-alvo, curando aliados dentro da área.

## Runtime e causalidade auditados

O source 3.16.3 cria `HealingAoe` com raio 5, duração 200 ticks e valor `getSpellPower * 0.25` por settlement definido pela entidade do provider. Targeting auditado alcança entidade/ponto até 32 blocos. Diferentemente das curas diretas, a causalidade detalhada por tick pertence a `HealingAoe` e não deve ser presumida como um novo `SpellHealEvent` sem confirmar o path real.

## VFX

A auditoria também registra `TargetedAreaEntity` visual com fade. Aparência final no pack permanece sujeita à validação real-client.

## Deduplicação

Já cobre healing zone Holy persistente. Uma futura área consagrada precisa agregar semântica própria — ward, exorcismo, anti-infernal, law etc. — e não apenas outra healing AoE.

## Fonte / evidência

- Catálogo oficial atual: `https://iron.wiki/spells/`.
- Auditoria source 3.16.3: `wiki/providers/irons-spellbooks/spells/holy/healing-circle.md`.