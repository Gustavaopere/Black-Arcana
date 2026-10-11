# Reliquified Artifacts 1.0.8 — `artifacts:obsidian_skull` / `lava`

Estado: **✅ CATALOGADO / `COUNTED_SOURCE_PINNED`** · **⚠️ igualdade binária source↔JAR e execução em Survival não comprovadas**.

## Identidade da habilidade

- **Owner original:** `artifacts:obsidian_skull` (namespace de item do mod-base Artifacts).
- **Ability root do addon:** `lava` (root da construção de habilidade do framework Relics na fonte auditada; não é um registro de spell do Iron's ou Ars).
- **Classe de implementação na fonte 1.0.8:** `ObsidianSkullItem`.
- **Identidade contabilizada:** par `artifacts:obsidian_skull` + `lava`, atribuído ao comportamento Reliquified sobre o item Artifacts.
- **Ordinal editorial:** 41/52. A ordem não é prioridade de registro, loot ou cast.
- **Provider de habilidade:** Reliquified Artifacts, mod ID `reliquified_artifacts`. O framework de ability/XP/rank pertence ao Relics.
- **JAR declarado no pack:** `reliquified_artifacts-1.21.1-1.0.8.jar`, SHA-1 físico `00ad43d5a1aa287fd0084bc3b48546821494ff80` (sem inspeção binária adicional nesta ficha).
- **Fonte exata de versão:** `Octo-Studios/reliquified-artifacts@529fa0cd865a95dbe1bf02081de0275e90c69aee`; `COUNTED_SOURCE_PINNED`, não `COUNTED_EXACT`.
- **Contagem nesta individualização:** **+0 novas identidades semânticas** — ability já incluída nas 52 roots do provider.

## Aquisição e condição de obtenção

A classe implementadora consta entre as 47 classes de owners com `LootTemplate` no inventário source-pinned; **a categoria/tabela de loot específica deste owner não foi verificada nesta ficha**.

A rota de obtenção é evidência de fonte para a versão 1.0.8, não confirmação de que o loot, receitas, mixins, filtros e configurações estão efetivamente ativos no pack completo.

## Deduplicação e autoridade

A chave semântica deste catálogo é a combinação owner + root. A classe da fonte identifica a implementação observada, mas não constitui contrato público de API.

Artifacts mantém os owners originais e seu conteúdo-base. Reliquified Artifacts fornece a implementação de habilidade em cima desses owners. Relics mantém XP, rank, estado e processamento genérico de ability. Curios e integrações de inventário têm autoridades próprias.

O Black Arcana não deve replicar efeitos, rank, cooldowns, consumo, evolução, crédito de XP ou efeitos causados pelo mesmo evento. Sem hook/provider-native compatível e testado na versão implantada, a integração permanece **⛔ fail-closed**.

## Limites obrigatórios

- **Trigger exato, efeito, parâmetros, custo, ranks, cooldowns, duração, sincronização, relações entre skills:** **NÃO VERIFICADOS individualmente** nesta materialização. O nome da root não prova a mecânica.
- **Paridade byte-a-byte entre source e JAR físico, config implantada, loot final, equip/unequip, save/relog/restart, death, multiplayer e execução Survival:** **⚠️ PENDENTE**.
- **API/hook externo suportado:** **NÃO VERIFICADO**. A classe documentada não deve ser usada como API pública por inferência.
- **Clean-room:** somente identificadores, classes e fatos de origem já registrados; nenhum código/asset/JAR/arquivo de localização de terceiros redistribuído.

**Referências:** [matriz source-pinned 52/52](../../ABILITY-INVENTORY-1.0.8.md) · [provider e fronteiras de autoridade](../../README.md).
