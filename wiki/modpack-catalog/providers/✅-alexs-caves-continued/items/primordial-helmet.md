# Primordial Helmet — bônus alimentar Primordial (Alex's Caves Continued 1.0.10)

**Estado:** ⚠️ ficha individual **PARCIAL / STATIC_DISCOVERY_ONLY**, `NO_MUTATION`, `mutating_hook=NOT_VERIFIED`, `physical_qa=NOT_TESTED`, `perks_executable=NOT_CERTIFIED`, `provider_universe_closed=false`. Este é um equipamento, **não** um novo feitiço ou ritual; `new_magic_roots=0`.

## Identidade, descrição e autoridade física

- **Provider:** Alex's Caves Continued; mod ID `alexscaves`; Minecraft **1.21.1**, NeoForge, Java 21; versão física declarada **1.0.10** na modlist sibling `PROJECT-INSTRUCTIONS/modlist/World Gen/✅-alexs-caves-continued v1.0.10.md`.
- **Item:** `alexscaves:primordial_helmet`, `ACItemRegistry.PRIMORDIAL_HELMET`, construído em factory `lambda$static$42` com material `PRIMORDIAL_ARMOR_MATERIAL` e `ArmorItem.Type.HELMET`. **Slot no contador nativo:** `EquipmentSlot.HEAD`.
- **Comportamento funcional (resumo original):** quando esta peça está equipada no slot correto, contribui **uma unidade** para a contagem Primordial de até três peças. Dois consumidores nativos usam essa contagem para alterar argumentos de nutrição e saturação em situações específicas de alimentação; não há lançamento de feitiço nem execução direta de alimentação no owner do item.
- **JAR físico/publisher:** `alexscaves-1.0.10-neoforge+1.21.1.jar`, SHA-1 `6960b299a39a039ac8a5eb9b07be4ad0e3e0a570`, SHA-256 `36ae0a3cbd028df466a37c671ba2fdf021c060ca1c9c1c32e9f2e95bffae0e7c`, **75.279.314 bytes**. Dump novo instalado **NOT_VERIFIED**; o JAR publisher exato foi inspecionado por CI.
- **Classe owner:** `com/github/alexmodguy/alexscaves/server/item/PrimordialArmorItem.class`, SHA-256 `8833c162d1507aba795b1ff809f5a6f6ddb846da308d809795cf80e69be5d09e`. Quatro métodos executáveis compartilhados entre três peças; multiplicidade de itens não cria novas magias.
- **Modelo individual:** `assets/alexscaves/models/item/primordial_helmet.json`, SHA-256 `6420214e099ec006f4c9226b5ee1333b8c90d523160c08b0584dc087cbf20160`; imagem da armadura devolvida pelo owner em slot HEAD: `alexscaves:textures/armor/primordial_armor_0.png`. Renderização efetiva **NÃO TESTADA**.
- **Receita identificada pelo filename:** `data/alexscaves/recipe/primordial_helmet.json`, SHA-256 `51777de205dd200884027441d95d875f475243f2f0566cef26b85b314cd7dc2e`; tag `data/alexscaves/tags/item/repairs_primordial_armor.json` e `ACItemRegistry.setup` associam reparo a `alexscaves:tough_hide`. Ingredientes de craft e execução de reparo/loot não foram individualmente comprovados neste relatório.
- **Fontes de prova:** [dossiê de comportamento](../EXACT-PRIMORDIAL-ARMOR-DISCOVERY-1.0.10.md), [manifesto SHA-exato](../EXACT-PRIMORDIAL-ARMOR-DISCOVERY-1.0.10.json), [material nativo](../systems/armor-material.md), [CI read-only](https://github.com/Gustavaopere/Black-Arcana/actions/runs/44951722588), artifact `14725074259` / report SHA-256 `659f60f17d549d8c795becc4d7fa7e6b8968cb546b8af002099b44abb65e4f75`.

## Ativação, condições e parâmetros

**Seleção pelo item exato:** `PrimordialArmorItem.getExtraSaturationFromArmor(LivingEntity)` tem **31 instruções**, SHA-256 `2fb7d7a8c00bc1a5b33c525f7da5b7c80d04b373b9c24bed3412fe4d04cc8317`. No trecho **@2–26**, lê `getItemBySlot(EquipmentSlot.HEAD)` e compara `ItemStack.is(ACItemRegistry.PRIMORDIAL_HELMET)`. Se verdadeiro, o contador `n` é incrementado em **+1** (`@26`). Uma peça idêntica em slot errado **não soma**; conteúdo de inventário fora do slot, desgaste, encantamento, UUID, item de outra espécie e duração não são consultados nesse método.

O mesmo método avalia as outras duas peças esperadas; `n ∈ {0,1,2,3}`. **Não existe quarta peça Primordial/boots neste recorte do registry**. O valor n é a **contagem**; não é saturação final. Dois métodos consumidores usam n:

| Consumidor físico | Gate | Parâmetros entregues ao `FoodData` |
|---|---|---|
| `PlayerMixin.ac_eat` | Item da tag `RAW_MEATS`, `n>0` e `FoodProperties != null` | `eat(nutrition(food)+n, saturationModifier(food)+0.125F×n)` |
| `DinosaurChopBlock.eat` | `player.canEat(false)`; bloco específico `ACBlockRegistry.DINOSAUR_CHOP` para contar n | `eat(foodAmount+n, saturationAmount+0.125F×n)` |

Com esta única peça identificada e nenhuma das outras duas, `n=1` e os argumentos nominais sofrem **+1 de nutrição** e **+0.125F no saturationModifier** em cada caminho que passar nas guardas. Ao somar duas ou três peças, os incrementos nominais são, respectivamente, `+2/+0.25F` e `+3/+0.375F`. Isto **não significa** ganho direto desse número de pontos de saturação armazenada: o algoritmo e os clamps de `FoodData.eat`, outras modificações e a aceitação final continuam fora do recorte binário.

No `PlayerMixin.ac_eat` (31 instruções, SHA-256 `3f928fd639c0d5e62a849fdf302ba373fc304d4a4c8fff7cfd65e11a9a2abffd`), o fallback sem bônus é `eat(FoodProperties)`. No `DinosaurChopBlock.eat` (89 instruções, SHA-256 `4e2b75751d124247a814dc386551010171bbfdc157b96a80f01c36c74cc4058c`), há solicitações de `Stats.EAT_CAKE_SLICE`, `GameEvent.EAT`, atualização de `BITES` e alteração/removal do bloco; o item de armadura não manipula o mundo diretamente. O relatório não estabelece se os mixins são efetivamente aplicados no cliente/modpack ou se as alterações do mundo foram aceitas por todas as regras de proteção.

**Material:** `PRIMORDIAL_ARMOR_MATERIAL` (parâmetros auditados separadamente) entrega defesa `[3,4,3,2]` **por ordinal**, durabilidade máxima `[260,300,320,220]` por ordinal, encantabilidade **25**, toughness **0F**, knockback **0F**, nome `primordial`, reparo `alexscaves:tough_hide`. **Ordinal real do tipo HELMET e execução dos atributos pela engine não verificados**; não atribuir índice do array a slot sem prova de ABI. Não existe custo de mana, cast, charge, cooldown ou desconto de desgaste no contador.

## Efeitos, targeting, autoria, persistência e segurança

**Efeito observado:** contribuição na contagem que modifica argumentos alimentares quando consumidores elegíveis invocam o contador. **Target:** a própria `LivingEntity` equipada, concretamente Player no uso dos consumidores; sem alvo adversário, aquisição de alvo, distância, LOS, AOE, projétil, tamanho/velocidade de projétil, dano, tipo de dano, knockback, summons, teleporte ou status mágico (**N/A no owner**). A execução alimentar é no consumidor, não um novo cast de Black Arcana.

**Custos e escala:** o bônus tem escala inteira com número de peças, **não** com nível de spell, XP, Mastery ou atributos RPG. Não há atualização temporal no owner; ele responde a uma leitura pontual. Não foram identificados campos próprios de persistência, NBT, UUID ou componente no método. `FoodData`, estado do bloco, eventos e rede pertencem à engine e consumidores, não se presume persistência/sincronização homologada.

**Possibilidades de perk:** ajuste condicionado de nutrição, saturação, bônus por conjunto e interação de alimentos é conceitualmente relevante. **Nenhuma API/hook mutador seguro foi verificado**; intervir globalmente no contador impactaria simultaneamente `PlayerMixin` e `DinosaurChopBlock`. Não duplicar chamadas `FoodData.eat`, GameEvents, receita, XP/Mastery, world changes ou efeitos em cadeia; sem boundary real de ownership/per-player, `NO_MUTATION`/fail-closed. Black Arcana mantém autoridade de seu runtime mágico e RPG Skill Tree fornece apenas perks/progressão via contratos verificados.

## Validação, limites e próximos gates

Quatro métodos completos do owner, registries/fábricas, classes consumidoras, censo de 1.555 classes e hashes de 8 recursos estão ligados ao relatório publisher exato. **Pendente:** identidade ordinal na engine, aplicação real do mixin, métodos de `ACCompat` e `FoodData`, compatibilidade da alimentação com outros mods, recipe real, perks com contexto por jogador, desgaste/reparo, save/restart, dano/mitigação final, multiplayer, QA cliente/servidor físico. Um certificado estático dos sete eixos pertinentes exigirá resolver essas lacunas e validações adicionais; manter esta ficha **⚠️ PARCIAL**.
