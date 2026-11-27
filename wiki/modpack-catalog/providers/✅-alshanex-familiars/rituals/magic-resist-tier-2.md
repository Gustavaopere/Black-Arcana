# Magic Resist Tier 2

**✅ Contrato técnico estático do ritual** · Alshanex’s Familiars 4.0.3 · `STATIC_TECHNICAL_CATALOG_ONLY`

O altar melhora o consumível de familiar do tier 1 para o tier 2. O bônus de atributo é aplicado mais tarde ao familiar que recebe o item. [Evidência no JAR exato](../EXACT-4.0.3-REMAINING-RITUALS.md#consumíveis-de-familiar)

| Identidade | Valor |
|---|---|
| Receita | `alshanex_familiars:ritual_recipes/magic_resist_tier_2` |
| Tipo | `alshanex_familiars:ritual_recipe` |
| Saída | `alshanex_familiars:magic_resist_tier_2` |
| Contagem semântica | `COUNTED_EXACT` · um ritual do provider |

## Custo, montagem e resultado

Coloque uma unidade de `alshanex_familiars:magic_resist_tier_1` no núcleo e os quatro itens abaixo nas estátuas. As `FamiliarStatueEntity` ficam na mesma altura, a dois blocos do núcleo nos pontos cardeais. A ordem é livre. `RitualRecipeType.matches` verifica o central e exige quatro unidades no total.

| Item periférico | Quantidade | Destino ao concluir |
|---|---:|---|
| `minecraft:ghast_tear` | 1 | Consumido |
| `irons_spellbooks:cinder_essence` | 1 | Consumido |
| `minecraft:warped_fungus` | 1 | Consumido |
| `irons_spellbooks:hogskin` | 1 | Consumido |

`RitualCorePedestalEntity.completeRitual` chama a limpeza e substitui o item central por uma nova stack de uma unidade. A receita consome os quatro itens periféricos. A nova stack recebe os components padrão do item de saída. A produção usa inventário e tempo de altar, com mana, XP e cooldown de jogador inaplicáveis.

## Duração e Ritual Automator

`RitualCorePedestalEntity.tick` conclui ao atingir **100 incrementos de servidor com a receita válida**. A falta de um periférico pausa o progresso enquanto o central permanece elegível. A troca do central reinicia a contagem. O núcleo solicita `irons_spellbooks:unstable_ender` a cada dez incrementos e o efeito visual de Evocation ao concluir. Os receptores do craft são os inventários do núcleo e das estátuas. O craft não solicita dano, projétil ou status em alvos vivos.

O Ritual Automator busca a receita por ID completo. Usa o inventário imediatamente abaixo e programa transferências de 20 ticks ativos. O núcleo continua resolvendo o craft pela montagem presente. O Automator recolhe a saída e tenta inseri-la no inventário, com drop para o restante ou quando o armazenamento deixa de existir. [Geometria, relógio, persistência e automação](../EXACT-4.0.3-ARCHMAGE-RITUAL.md)

## Consumidor do resultado

`ItemRegistry.<clinit> @1159–1170` registra `MAGIC_RESIST_TIER_2` com bootstrap 65 para `lambda$static$43`. A fábrica cria `Item` de raridade `RARE` e stack máxima de 64. `FAMILIAR_CONSUMABLE` recebe o tipo `SPELL_RESIST` em `@37` e o tier 2 em `@40`.

`AbstractSpellCastingPet.mobInteract` delega ao FamiliarsLib 1.7.1 em `@87` na rota de familiar alojado com verificação do dono pelo armazenamento e em `@316` na rota de dono resolvido pelo UUID. `handleConsumableInteraction` lê o componente e o bônus acumulado `C` do familiar. No servidor, a aplicação do tier 2 exige `C < 30`. No caminho aceito, grava **`min(C + 5, 30)`**, aplica o modificador e reduz a stack em uma unidade. Os limites são próprios do item. A aplicação aceita o tier 2 a partir de `C = 0`; o tier anterior é insumo do craft.

`FamiliarConsumableSystem.applyAttributeModifiers` usa o total acumulado dividido por 100 como modificador permanente `ADD_MULTIPLIED_BASE` sobre o atributo `SPELL_RESIST` do Iron’s Spells no familiar. O estado do consumível é salvo e carregado pelo FamiliarsLib. Por exemplo, `C = 0` passa a 5 em uma aplicação deste item, e o amount enviado à base do atributo passa a `0.05`. O resultado de combate depende dos consumidores do atributo e da composição do host. [Fórmula, limites e métodos](../EXACT-4.0.3-REMAINING-RITUALS.md#consumíveis-de-familiar)

## Integração e QA

O altar controla a produção e o FamiliarsLib aplica o bônus. Custos, duração, retenção e teto estão disponíveis para o desenho de perks do RPG Skill Tree e Enshrouded. A atribuição de Mastery e a mutação dos parâmetros exigem contratos específicos. `mutating_hook=NOT_VERIFIED`, `physical_qa=NOT_TESTED`, `perk_certification=NOT_CERTIFIED`, `mutation=NO_MUTATION`.
