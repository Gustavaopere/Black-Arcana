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

O dano base listado cresce de 5 para 13. A fórmula exata de incorporação de weapon damage/enchantments e a hitbox ficam `NÃO VERIFICADO`.

## Obtenção e aprendizado

Segue o pipeline geral de scrolls/spellbooks do Iron's. O changelog 3.6.0 registra a revisão de hitbox/registro e a redução do dano por nível para a linha atual; o changelog 3.10.0 registra a substituição da antiga visual entity por partícula.

## Deduplicação / authority

Já cobre melee spell uninterruptible que escala com arma. Black Arcana não deve recalcular a mesma contribuição de weapon damage/enchantments por um segundo pipeline, evitando double-dip.

## VFX / animação / áudio

O changelog confirma que a visual entity de Flaming Strike foi substituída por partícula em 3.10.0. A aparência final, animação e áudio no runtime real do pack ainda ficam `NÃO VERIFICADO` neste passe.

## Fonte / evidência

- Catálogo oficial atual: `https://iron.wiki/spells/`
- Changelog oficial: `https://iron.wiki/changelog/`
- Consulta: 2026-09-06.
