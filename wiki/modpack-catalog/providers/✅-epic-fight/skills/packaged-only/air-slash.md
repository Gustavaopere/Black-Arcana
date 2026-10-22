# air_slash — recurso de parâmetros sem vínculo core comprovado

**Estado:** ⚠️ `PACKAGED_RESOURCE_ONLY`; ⛔ não instanciar uma skill nem contar uma nova magia a partir deste arquivo.

O JAR Epic Fight **21.17.3.1**, `epic-fight-21.17.3.1-mc1.21.1-neoforge.jar`, contém `data/epicfight/skill_parameters/air_slash.json` com o parâmetro numérico **`consumption=2.0`**. Leitura direta do ZIP publisher de **8.578.288 bytes**, SHA-1 `fb199b7bbea2fc402da28ab586e73f47e32f8fc0`, SHA-256 `8b882554cf10086398340fbdc741819ee72a801a3adce516c7f4768326a39526`; ambos coincidem com a evidência física registrada. Não houve leitura da instalação ao vivo.

## Distinção de identidades

- A auditoria core contém **43 IDs**: **42 habilidades jogáveis** e **1 sentinela `epicfight:empty`**, sem JSON próprio. `air_slash` não integra essa lista auditada.
- O ZIP possui **43 JSONs** em `data/epicfight/skill_parameters/`: **42** vinculados aos IDs core auditados e este **1** recurso adicional. Os denominadores são diferentes.
- O pool UTF-8 do classfile exato `yesman/epicfight/registry/entries/EpicFightSkills.class` contém todos os 43 literais core esperados e não contém o literal `air_slash`. Isto é evidência limitada sobre o registrar, não prova de ausência de todo carregamento dinâmico, addon ou outro consumidor.
- Existem `yesman/epicfight/api/animation/types/AirSlashAnimation.class` e `yesman/epicfight/api/animation/types/datapack/DatapackAirSlashAnimation.class`. **Classes de animação não comprovam uma skill de registry nem consumo deste JSON.** Não atribuir o parâmetro a essas classes por semelhança do nome.

## Matriz para futuras integrações

| Campo | Evidência atual | Estado |
|---|---|---|
| Tipo | Recurso JSON de parâmetros empacotado; skill vinculada não demonstrada | `PACKAGED_RESOURCE_ONLY` |
| Custo | `consumption=2.0` serializado; unidade, pagador, consumer e débito efetivo desconhecidos | `NÃO_VERIFICADO` para gameplay |
| Classe/método consumidor | Não identificado nesta auditoria | ⛔ `SEM_HOOK_SEGURO` |
| Alvo/alcance/área/LOS | Não inferíveis do arquivo | `NÃO_VERIFICADO` |
| Dano/DamageType | Não inferíveis do arquivo | `NÃO_VERIFICADO` |
| Projétil/hitbox/velocidade | Não inferíveis do arquivo nem dos nomes das animações | `NÃO_VERIFICADO` |
| Cast/duração/cooldown | Não inferíveis de `consumption` isolado | `NÃO_VERIFICADO` |
| Progressão/Mastery/perks | Nenhuma ação causal/settlement ou API mutadora comprovada | ⛔ fail-closed |

**Próximo passo:** localizar um consumidor e sua identidade, fase e versão antes de propor integração. Não declarar o recurso obsoleto, ativo ou removido por falta dessa prova. Nenhum cast, efeito, custo, perk ou gameplay foi executado nesta leitura.

[Mapa core de 43 IDs](../INDIVIDUAL-SKILL-CARDS-21.17.3.1.md) · [prova dos parâmetros core](../../EXACT-BINARY-PERK-PARAMETERS-21.17.3.1.md) · [registro desta rodada](../../../../../../docs/qa/catalog-individual-epicfight-2026-10-21.md).
