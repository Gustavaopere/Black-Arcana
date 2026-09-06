# Raise Hell

- **Status no modpack:** PRESENTE — provider instalado
- **Provider:** Iron's Spells 'n Spellbooks
- **Mod ID:** `irons_spellbooks`
- **JAR/versão:** `irons_spellbooks-1.21.1-3.16.3.jar` / `1.21.1-3.16.3`
- **Escola:** Fire
- **Níveis:** 1–5
- **Raridade:** Legendary
- **Cast:** Long
- **Mana:** 90–270
- **Cooldown:** 25 s
- **Dano base listado:** 15
- **Raio:** 8 blocos
- **Casts:** 1–5

## O que faz

Golpeia com a arma para liberar uma grande onda de choque flamejante ao redor do caster. A documentação atual registra que o dano escala com a arma empunhada e que a quantidade de casts cresce até cinco.

## Escalonamento

O catálogo lista dano base 15, raio 8 blocos e 1–5 casts. A fórmula exata de scaling com arma, janela entre recasts e contribuição de encantamentos ficam `NÃO VERIFICADO`.

## Obtenção e aprendizado

Raise Hell foi adicionado na linha 3.10.0. O pipeline específico de aquisição permanece `NÃO VERIFICADO` além das regras gerais de scrolls/spellbooks.

## Deduplicação / causalidade

Já cobre shockwave melee/fire de grande raio com multi-cast e weapon scaling. Os recasts não devem virar casts raiz independentes em integrações, e o dano de arma não deve ser recalculado por Black Arcana.

## Fonte / evidência

- Catálogo oficial atual: `https://iron.wiki/spells/`
- Changelog oficial: `https://iron.wiki/changelog/`
- Consulta: 2026-09-06.
