# Throw

- **Status no modpack:** PRESENTE — provider instalado
- **Provider:** Iron's Spells 'n Spellbooks
- **Mod ID:** `irons_spellbooks`
- **JAR/versão:** `irons_spellbooks-1.21.1-3.16.3.jar` / `1.21.1-3.16.3`
- **Escola:** Evocation
- **Níveis:** 1–5
- **Raridade:** Common → Legendary
- **Cast:** Long
- **Mana:** 10–30
- **Cooldown:** 8 s
- **Dano base listado:** 1–5

## O que faz

Arremessa o item empunhado, causando dano base do spell somado ao dano que o item normalmente causaria segundo a descrição pública atual.

## Escalonamento

O dano base listado cresce de 1 para 5. Fórmula exata de combinação com weapon damage, enchantments, retorno/perda do item e entidades elegíveis ficam `NÃO VERIFICADO`.

## Obtenção e aprendizado

Segue o pipeline geral de scrolls/spellbooks do Iron's. Rotas específicas permanecem `NÃO VERIFICADO`.

## Deduplicação / authority

Já cobre conversão de item empunhado em ataque arremessado com contribuição do dano nativo do item. Uma habilidade Black Arcana equivalente precisa de mecânica distinta e não pode recalcular o dano do item por fora do provider, evitando double-dip de atributos/enchantments.

## Fonte / evidência

Catálogo oficial atual: `https://iron.wiki/spells/` — consulta em 2026-09-06.
