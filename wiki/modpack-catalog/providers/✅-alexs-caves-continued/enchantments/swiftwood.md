# Swiftwood — `alexscaves:swiftwood` (Alex's Caves Continued 1.0.10)

**Contrato técnico estático individual:** ✅ `SHA_EXACT_BINARY_BEHAVIOR` / `STATIC_TECHNICAL_CATALOG_ONLY`. **Hook mutador externo:** `NOT_VERIFIED`. **QA física:** `NOT_TESTED`. **Implementação de perk:** `NO_MUTATION`. A conclusão refere-se aos atributos *declarados* pelo Primitive Club e ao caminho de consulta nativo da stack; não certifica os atributos finais de um jogador com outros equipamentos, o cálculo do ataque pela engine ou PvP real.

## 1. Identidade, proveniência e descrição

- **Provider:** Alex's Caves Continued, mod ID `alexscaves`; Minecraft **1.21.1**, NeoForge, Java 21.
- **Artefato instalado/publisher:** `alexscaves-1.0.10-neoforge+1.21.1.jar`, 75.279.314 bytes, CurseForge projeto `1645389` / arquivo `8856293`. SHA-1 `6960b299a39a039ac8a5eb9b07be4ad0e3e0a570`; SHA-256 `36ae0a3cbd028df466a37c671ba2fdf021c060ca1c9c1c32e9f2e95bffae0e7c`.
- **Tipo:** encantamento de atributos de arma, **não** novo cast, projétil ou feitiço ativável.
- **Registro e JSON:** `data/alexscaves/enchantment/swiftwood.json`, **363 bytes**, SHA-256 `3d19fac156679ac53f49424b9bb828ad44a003d3d33a8b14dda303d50fc17551`; key `ACEnchantmentRegistry.SWIFTWOOD`.
- **Elegibilidade:** `supported_items=#alexscaves:enchantable/primitive_club`; tag publisher `data/alexscaves/tags/item/enchantable/primitive_club.json`, SHA-256 `71829c384be93b8cef1e090b6afafa621dcd4eeb520c7a66ab0e6524e8a6ae43`, contendo `alexscaves:primitive_club`.
- **Descrição editorial em português:** Swiftwood acelera o ataque do Primitive Club ao tornar menos negativo seu modificador de velocidade de ataque. O texto da localização `en_us.json` confirma essa finalidade; descrição e fórmula têm evidências independentes no JAR. Não deduzir uma chance de acerto adicional, dano novo ou redução arbitrária do cooldown do mod.
- **Fonte adjacente:** código público `Codx-org/AlexsCavesContinued` 1.1.1 ajuda na navegação, mas **não é prova** para 1.0.10. Valores, offsets e método proprietário abaixo são de auditoria estática **exclusiva do JAR 1.0.10**.

## 2. Ativação e ciclo de cálculo

O jogador utiliza o Primitive Club normalmente com a stack encantada. `PrimitiveClubItem.acModifiers(EquipmentSlot,ItemStack)`, **17 instruções JVM**, retorna `null` para slot distinto de `EquipmentSlot.MAINHAND` (`@1–8`). Na mão principal, consulta `ACCompat.enchantLevel(stack,SWIFTWOOD)` em `@10–13`, aplica `Mth.clamp(level,0,3)` em `@22–24` e seleciona `defaultModifiers[level]` em `@27–28`.

O construtor `PrimitiveClubItem(Properties)`, **22 instruções**, inicializa o conjunto de modificadores para os índices `0..3` por `getStatsForEnchantmentLevel(int)`. A tabela é pré-computada pelo item; **a seleção do índice é dinâmica, por stack**, ao consultar os atributos. Não há buff de status temporário nem `tick` próprio de Swiftwood.

A entrada `getDefaultAttributeModifiers(ItemStack)`, **8 instruções**, chama `ACCompat.itemAttributes(BiFunction,ItemStack,Supplier)` em `@14`. Uma lambda de fallback, **4 instruções**, invoca `Item.getDefaultAttributeModifiers(stack)` em `@2`. O helper `ACCompat.itemAttributes` possui a sobrecarga de `BiFunction`/stack/Supplier com **48 instruções** e outra de Multimap/slot/Supplier com **19 instruções**. Isso comprova o encadeamento de bytecode da contribuição; **não certifica a ordem/composição efetiva de outros mods, mixins ou atributos finais do servidor**.

## 3. Fórmula, unidade, escalonamento e limites

No método `PrimitiveClubItem.getStatsForEnchantmentLevel(int)`, **33 instruções**, o JAR cria modificadores `AttributeModifier.Operation.ADD_VALUE` para **`Attributes.ATTACK_DAMAGE` com `+8.0D`** (`@5–24`) e para **`Attributes.ATTACK_SPEED` com `Math.min(0F,-3.75F+0.15F×L)`** (`@29–55`). O cálculo de velocidade ocorre em precisão `float`, seguido por `f2d` antes da criação do modificador; as casas decimais nominais abaixo podem sofrer arredondamento binário.

| Nível de Swiftwood | ATTACK_DAMAGE, `ADD_VALUE` | ATTACK_SPEED, `ADD_VALUE` nominal |
|---:|---:|---:|
| 0 (ausente) | +8,0 | −3,75 |
| I | +8,0 | −3,60 |
| II | +8,0 | −3,45 |
| III | +8,0 | −3,30 |

**Incremento do encantamento:** +0,15 de modificador `ATTACK_SPEED` a cada nível I–III em relação ao anterior. **Não** aumenta o modificador `ATTACK_DAMAGE`: o +8 é uma propriedade do Primitive Club presente mesmo sem Swiftwood. O `Math.min(0F,...)` evita modificador positivo na rotina genérica, mas o `Mth.clamp(0..3)` limita os quatro índices efetivamente selecionados pela stack nativa.

Esses são valores de **modificador `ADD_VALUE`**, não ataques por segundo efetivos, velocidade física de animação, DPS, dano aplicado ou multiplicador percentual. A engine, o atributo base, outros equipamentos, efeitos, perks e o cooldown de ataque nativo podem modificar o resultado final. Os limites do índice também não constituem autorização para adicionar níveis externos à stack.

## 4. Metadados, custos e requisitos

| Campo publisher do JSON | Valor compilado/publicado |
|---|---|
| `max_level` | 3 |
| `weight` | 2 (peso declarativo, não chance de ataque) |
| `slots` | `mainhand` |
| `min_cost` | base 1, incremento 8: I = 1; II = 9; III = 17 |
| `max_cost` | base 41, incremento 10: I = 41; II = 51; III = 61 |
| `anvil_cost` | 4 (custo de aquisição/combinação, não custo por hit) |
| `supported_items` | `#alexscaves:enchantable/primitive_club` |

O JSON próprio não define `effects` ou `exclusive_set` neste recorte. Compatibilidade global com outros encantamentos, overrides de datapack, obtenção real em loot/mesa e custo de XP em jogo não foram testados. Swiftwood não introduz cobrança de mana, stamina, charges, durabilidade extra, XP por ativação ou cooldown independente.

## 5. Efeitos e consumidores: o que muda e o que permanece nativo

| Superfície relevante a perks | Contrato individual 1.0.10 |
|---|---|
| Velocidade de ataque | Incremento `ADD_VALUE` conforme fórmula e clamp do nível, apenas para mão principal no consumidor documentado |
| Dano | Sem alteração causada por Swiftwood; o item contribui +8 `ATTACK_DAMAGE` em todos os níveis, incluindo zero |
| Targeting, alcance, LOS e AoE | **N/A como efeito próprio**: não cria busca de alvo, seleção de aliados/inimigos nem geometria adicional |
| Projéteis, hitbox, summons, efeitos de mundo | **N/A**: nenhum projétil, entidade ou mudança de blocos gerados pelo ramo Swiftwood |
| Stun, knockback e on-hit | Continuam em outros caminhos nativos do Primitive Club, como `acHurtEnemy`; não atribuir a Swiftwood um novo stun/efeito sem consumidor próprio |
| Duração / intervalo / stack | Não há duração própria de buff; o modificador é consultado na stack. O tempo real de swing e acerto permanece dependente da engine e dos demais caminhos do item |
| Persistência e owner | Nível consultado nos encantamentos da `ItemStack`; nenhum estado NBT próprio de Swiftwood, entidade persistente ou caster adicional demonstrado |
| Custos por uso | `N/A` como nova cobrança. Desgaste nativo de clube, penalidades e reparos do item são independentes do encantamento |

O mesmo classfile expõe `hurtEnemy` (6 instruções), `acHurtEnemy` (**171**), `mineBlock` (15), `onLeftClickEntity` (16), `onEntitySwing` (24) e `acInventoryTick` (27). Esses métodos podem influenciar ataques, swing, desgaste e hit, mas não contêm uma consulta direta `SWIFTWOOD` no censo de classfiles. O caminho de ataque não é automaticamente um segundo consumidor de dano de Swiftwood; o efeito de velocidade alimenta a pipeline normal de atributos.

## 6. Grafo técnico e evidências da versão instalada

- `PrimitiveClubItem.class` SHA-256 `92bfb58cb5ed2c84dd6f989afad22c98209542889e30b6214c502dbff42fa1ac`; **16 métodos** parseados.
- `ACEnchantmentRegistry.class` SHA-256 `60006fab1b3b29f5f93c8365416815a12770cf8877a059298cb4ee82f7a92f32`.
- `ACCompat.class` SHA-256 `333738f324e6e9d77a488e14b7e81b169c2b2d4f6db5171206a016ad0271f57b`.
- `getStatsForEnchantmentLevel(int)`: 33 instruções, digest JVM parseado `a724c693a064b959f9dbd6395a4ab430114a3b1318b888546180bb0c3e09333f`. Âncoras `ATTACK_DAMAGE@5`, `8.0D@15`, `ADD_VALUE@18`, `ATTACK_SPEED@29`, `-3.75F@40`, `0.15F@42`, `Math.min@48`, `ADD_VALUE@52`.
- `acModifiers(EquipmentSlot,ItemStack)`: 17 instruções, digest `cdb36891f41a21806ad79e3ac68339b261c3f5f834cfdf54720b337b8df3681d`; `MAINHAND@1`, retorno `null@7–8`, `SWIFTWOOD@10`, `enchantLevel@13`, clamp `0..3@22–24`, seleção do array `@27`.
- `getDefaultAttributeModifiers(ItemStack)`: 8 instruções, digest `3ef89b9927daf6ddd6d8fa7d826e2a8a1eeb788a12faef74ad3c1d99918252e4`; helper `ACCompat.itemAttributes@14`.
- Lambda de fallback `lambda$getDefaultAttributeModifiers$0`: 4 instruções, digest `cb75b22e942d400bf70796038c5bd88e56cbb64f14239de3aa50b9d3064488d7`; método base `Item.getDefaultAttributeModifiers@2`.
- Censo de **1.555 classfiles**: referência direta `SWIFTWOOD` somente em `PrimitiveClubItem` e `ACEnchantmentRegistry`. Esse resultado não exclui reflexão, transformations, extensões de terceiros, alterações de datapack ou a engine.

## 7. Boundaries de integração, Mastery e segurança

Uma perk de aumento de velocidade de ataque poderia usar os atributos de progressão sob autoridade do RPG Skill Tree **somente mediante boundary real** que preserve a composição, o slot `MAINHAND`, caps, custos e as condições de swing/cooldown. O `getDefaultAttributeModifiers` encontrado é **método do provider**, não uma API pública de mutação segura para Black Arcana. Nenhum adapter, Mixin ou hook de integração foi homologado para alterar esse retorno, e Swiftwood não deve ser reexecutado como buff separado.

Não conceder Mastery por mera leitura dos atributos, tooltip, swing cancelado, ataque solicitado ou acerto não confirmado. Evitar double-processing da velocidade, duplo dano, múltiplas cobranças ou manipulação de client-authoritative attack speed. Falta QA de multiplayer, sincronização de atributos, hot-swap de itens, armaduras/perks adicionais e regras PvP/claims. `NO_MUTATION` / fail-closed.

## 8. Validação reproduzível e pendências

- [Manifesto exato](../EXACT-SWIFTWOOD-STATIC-1.0.10.json) · [relatório da prova](../EXACT-SWIFTWOOD-STATIC-1.0.10.md) · [sonda read-only](../../../../../docs/qa/alexscaves_1010_swiftwood_static_probe.py) · [testes negativos](../../../../../docs/qa/alexscaves_1010_swiftwood_static_probe_test.py).
- A sonda exige o SHA-1/SHA-256/tamanho do JAR, identidade de recurso/tag, hashes do registry/clube/ACCompat, censo de consumidores diretos, hashes de métodos, constantes JVM da fórmula, `MAINHAND`, clamp e bridge de atributos; os testes sintéticos detectam desvios e não autorizam mutação.
- **Certificação exclusiva:** contrato técnico estático individual `✅`. **Pendente:** avaliação física do atributo, composição com outros mods, sistema de swing e impactos, persistência/reload, testes de cliente/servidor/PvP, hooks/adapters e fechamento do provider. Nada foi integrado ao runtime de Black Arcana ou RPG Skill Tree.
