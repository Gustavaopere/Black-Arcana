# Chain Creeper

- **Status no modpack:** PRESENTE — provider instalado
- **Provider:** Iron's Spells 'n Spellbooks
- **Mod ID:** `irons_spellbooks`
- **JAR/versão:** `irons_spellbooks-1.21.1-3.16.3.jar` / `1.21.1-3.16.3`
- **Escola:** Evocation
- **Níveis:** 1–6
- **Raridade:** Uncommon → Legendary
- **Cast:** Long
- **Mana:** 40–90
- **Cooldown:** 15 s
- **Dano listado:** 5
- **Projéteis iniciais:** 3–8

## O que faz

Conjura ao redor de uma criatura ou bloco alvo um anel de cabeças de Creeper que cai e explode. Quando uma criatura morre por essa explosão, outro anel menor pode ser conjurado, permitindo uma cadeia de novas explosões.

## Escalonamento

O catálogo atual confirma 3–8 projéteis iniciais e dano listado 5. Limite exato de encadeamentos, raio, regras de atribuição de kill e redução de tamanho ficam `NÃO VERIFICADO`.

## Obtenção e aprendizado

Segue o pipeline geral de scrolls/spellbooks do Iron's. Fontes específicas de loot/crafting permanecem `NÃO VERIFICADO`.

## Deduplicação / causalidade

Já cobre explosão que gera novas instâncias por kill. Para Black Arcana, esse padrão exige atenção especial a causalidade e deduplicação: cada explosão derivada não pode ser tratada como um novo cast raiz para mastery/procs/recompensas.

## QA

O changelog 3.16.3 registra correção de dano de Chain Creeper. Portanto valores/comportamento de versões anteriores não devem sobrepor o catálogo atual.

## VFX / animação / áudio

`NÃO VERIFICADO` no runtime real do pack neste passe.

## Fonte / evidência

- Catálogo oficial atual: `https://iron.wiki/spells/`
- Changelog 3.16.3: `https://iron.wiki/changelog/`
- Consulta: 2026-09-06.
