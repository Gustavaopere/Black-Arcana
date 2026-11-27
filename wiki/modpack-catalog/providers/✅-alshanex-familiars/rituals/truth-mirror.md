# Truth Mirror

**✅ Contrato técnico estático do ritual** · Alshanex’s Familiars 4.0.3 · `STATIC_TECHNICAL_CATALOG_ONLY`

O altar transforma o Visibility Ring do Iron’s Spells em um espelho que pode revelar um familiar impostor. O craft e o uso posterior têm custos e receptores próprios. [Evidência no JAR exato](../EXACT-4.0.3-REMAINING-RITUALS.md#truth-mirror)

| Identidade | Valor |
|---|---|
| Receita | `alshanex_familiars:ritual_recipes/truth_mirror` |
| Tipo | `alshanex_familiars:ritual_recipe` |
| Saída | `alshanex_familiars:truth_mirror` |
| Contagem semântica | `COUNTED_EXACT` · um ritual do provider |

## Custo e montagem

O núcleo recebe `irons_spellbooks:visibility_ring`. O altar exige as quatro `FamiliarStatueEntity` nos pontos cardeais, na mesma altura e a dois blocos do núcleo. Cada estátua recebe uma unidade de um ingrediente. A ordem é livre.

| Item periférico | Quantidade | Destino |
|---|---:|---|
| `minecraft:gold_ingot` | 1 | Consumido |
| `irons_spellbooks:mithril_ingot` | 1 | Consumido |
| `irons_spellbooks:shriving_stone` | 1 | Consumido |
| `irons_spellbooks:divine_pearl` | 1 | Consumido |

`RitualRecipeType.matches` verifica o item central e as quatro quantidades. `RitualCorePedestalEntity.completeRitual` limpa os ingredientes consumíveis e substitui o anel por uma unidade de Truth Mirror. O craft usa itens e tempo de altar, sem mana, XP ou cooldown por jogador na rota examinada.

## Duração, receptores e automação

`RitualCorePedestalEntity.tick` conclui após **100 incrementos válidos** no servidor. A receita solicita a partícula `minecraft:enchanted_hit` a cada dez incrementos, e o núcleo solicita o efeito visual de Evocation no final. Retirar um periférico pausa o contador enquanto o central é elegível. Trocar o central reinicia o progresso. Os receptores do craft são os inventários de bloco. Dano, status e projéteis são inaplicáveis à produção do item.

O Ritual Automator procura a receita pelo ID completo e usa o inventário abaixo dele. Cada transferência usa 20 ticks de processamento. O núcleo seleciona a receita pelos ingredientes presentes. A coleta compara item e components e tenta entregar o espelho ao inventário. A saída que não cabe ou perde o armazenamento é encaminhada para drop. [Fluxo comum do altar e da automação](../EXACT-4.0.3-ARCHMAGE-RITUAL.md)

## Uso posterior do espelho

`ItemRegistry.TRUTH_MIRROR` instancia `TruthMirror`, que configura raridade épica, stack máxima 1 e durabilidade máxima 3. `interactLivingEntity` recebe a entidade clicada e só entra na rota de uso em um `AbstractSpellCastingPet` no servidor. Para a troca de entidade, exige flag de impostor e um dos dois ramos a seguir.

- Se `getSummoner()` devolve `null`, solicita um `IllusionistPetEntity` na posição e rotação do alvo, sem copiar os campos do ramo com invocador resolvido.
- Se o retorno está presente, compara com o jogador por `LivingEntity.is`. No ramo aceito copia stacks de armadura, vida e fúria, estado de bloqueio, UUID de dono, posição e yaw. O resultado `null` vem do resolvedor de dono e, por si, não comprova ausência de um UUID salvo.

Ambos os ramos solicitam partículas, descartam o retorno de `addFreshEntity` e pedem a remoção do impostor. A rota pede **1 de desgaste** com `EquipmentSlot.MAINHAND` e retorna `SUCCESS` mesmo quando o alvo é um familiar sem flag de impostor ou a comparação com o invocador falha. Alvo incompatível e execução cliente retornam `FAIL`. O débito efetivo e a aceitação da nova entidade dependem do host. [Offsets e limites](../EXACT-4.0.3-REMAINING-RITUALS.md#truth-mirror)

## Integração e QA

Alshanex controla o consumo do altar e a revelação. RPG Skill Tree e Enshrouded podem usar esta ficha para identificar a fronteira entre craft, desgaste e troca de entidade. Hooks mutadores e atribuição de Mastery continuam `NOT_VERIFIED`. `physical_qa=NOT_TESTED`, `perk_certification=NOT_CERTIFIED`, `mutation=NO_MUTATION`.
