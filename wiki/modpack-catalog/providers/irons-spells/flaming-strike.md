# Flaming Strike

- **Status no modpack:** PRESENTE — provider instalado
- **Provider:** Iron's Spells 'n Spellbooks
- **Mod ID:** `irons_spellbooks`
- **JAR/versão:** `irons_spellbooks-1.21.1-3.16.3.jar` / `1.21.1-3.16.3`
- **Escola:** Fire
- **Níveis:** 1–5
- **Raridade:** Common → Legendary
- **Cast:** Long
- **Mana:** 30–90
- **Cooldown:** 15 s
- **Dano base listado:** 5–13
- **Interruptibilidade:** uninterruptible

## O que faz

Executa um ataque corpo a corpo em arco envolto em chamas. A documentação atual registra que o dano escala com o dano melee e os encantamentos da arma empunhada.

## Escalonamento

O dano base listado cresce de 5 para 13. A fórmula exata de incorporação de weapon damage/enchantments e hitbox ficam `NÃO VERIFICADO`.

## Obtenção e aprendizado

Segue o pipeline geral de scrolls/spellbooks do Iron's. O changelog 3.10.0 registra revisão de hitbox/registro e redução do dano por nível para a linha atual.

## Deduplicação / authority

Já cobre melee spell uninterruptible que escala com arma. Black Arcana não deve recalcular o mesmo weapon/enchantment contribution por um segundo pipeline, evitando double-dip.

## Fonte / evidência

- Catálogo oficial atual: `https://iron.wiki/spells/`
- Changelog oficial: `https://iron.wiki/changelog/`
- Consulta: 2026-09-06.
