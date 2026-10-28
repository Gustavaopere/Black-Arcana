# Sea Staff — Water Bolt

- Provider: **Alex's Caves Continued** (`alexscaves`)
- Version: `1.0.10`
- Exact physical/publisher SHA-1: `6960b299a39a039ac8a5eb9b07be4ad0e3e0a570`
- Owner: `alexscaves:sea_staff`
- Trigger: direct item use
- State: `COUNTED_EXACT`

## Semantic identity

One deliberate player action causes Alex's Caves Continued to create and launch its Water Bolt action. Entity ticks, targeting, impact and enchantment modifiers are downstream settlement of this same root.

## Exact acquisition

Exact provider data closes Sea Staff through Deep One Mage barter loot.

## Boundary

Numerical tuning, cooldowns, targeting, entities, effects, particles and sounds remain provider authority. Black Arcana catalogs the identity and must not replay provider settlement.

Sources: `../EXACT-1.0.10-ARTIFACT-AUDIT.md`, `../ITEM-ACTION-DISPOSITION-1.0.10.md`.

## Engenharia causal — fonte público fixado, NÃO paridade binária

**Proveniência dos números abaixo:** inspeção somente-leitura do fonte público `Codx-org/AlexsCavesContinued@523308608422ab8e31974befa7111ecdf495dd37` (LGPL-3.0), corroborando qualitativamente a identidade do JAR físico 1.0.10. O catálogo anterior comprova os **8 registros de ações pela inspeção do JAR**, mas **não** que este snapshot público foi compilado em bytes idênticos ao artefato `6960b299a39a039ac8a5eb9b07be4ad0e3e0a570`. Assim, os valores a seguir são **SOURCE_SNAPSHOT_ONLY**, não parâmetros certificados da versão física. Configuração efetiva, hooks mutadores e QA física: `NOT_VERIFIED`.

| Propriedade | Comportamento observado no snapshot público |
|---|---|
| Entrada e proprietário | `SeaStaffItem.use(Level, Player, InteractionHand)`; seleciona o alvo no servidor, instancia `WaterBoltEntity` e envia uma única ação de uso |
| Busca / target | `getClosestLookingAtEntityFor(..., 128)` usa 128 como distância do raio de consulta e busca `Mob` vivo/não aliado com linha de visão. **128 não é limite geométrico comprovado** de todos os candidatos, porque há uma consulta adicional em AABB expandida; não tratar como `maxRange` efetivo |
| Projéteis | 1 bolha por uso; `TRIPLE_SPLASH` positivo produz 3 instâncias, central + ângulos `-50°/+50°`; velocidade inicial `2F` central ou `1F` lateral; `inaccuracy=12F` |
| Custo de item | Um ponto de durabilidade se o jogador não tem `instabuild`; o método inspecionado não chama diretamente um setter de cooldown nem cobra mana |
| Homing | `SOAK_SEEKING` ajusta `seekAmount = 0.3F + 0.2F * enchantLevel`, e o projétil registra UUID do alvo; entidade só busca o alvo sob condições de tempo/distância próprias |
| Enchantments derivados | `ENVELOPING_BUBBLE` habilita flag `BUBBLING` de forma aleatória por bolha; `BOUNCING_BOLT` habilita um ricochete que pode criar outra entidade |
| Hit / tipo de dano | `WaterBoltEntity.damageMobs()` usa `mobProjectile` e valor `3.0F` na AABB de colisão expandida em `2` por eixo; não é ataque `magic` por nomenclatura |
| Efeito secundário | Se `BUBBLING` e dano bem-sucedido, aplica `BUBBLED` por `200` ticks, com mensagem de visualidade; entidades `DeepOneBaseEntity` são excluídas |
| Encerramento | Em hit válido, `dieIn=5` aciona descarte após contagem; colisão de bloco também chama `damageMobs` |
| Ricochete | Se habilitado, procura outro alvo na AABB `32` por eixo do alvo atingido, não aliado, a mais de `3` unidades dele; gera outro `WaterBoltEntity`, já sob a autoridade do provider |

### Boundary para perks e hooks

Um bônus de alcance precisa distinguir **consulta de aquisição**, **homing**, **busca de ricochete** e **raio do impacto**; são quatro contratos diferentes. Modificar apenas um valor não altera automaticamente os outros. A fonte expõe `use`, `damageMobs` e `onRicochetHit` como métodos **observados**, não hooks externos estáveis. Sem seam provider-native comprovada no JAR 1.0.10/NeoForge, a perk fica **⛔ fail-closed**; Black Arcana não relança Water Bolts, não duplica `mobProjectile` nem paga durabilidade duas vezes.

**Referência method-pinned:** [`SeaStaffItem.java`](https://github.com/Codx-org/AlexsCavesContinued/blob/523308608422ab8e31974befa7111ecdf495dd37/src/main/java/com/github/alexmodguy/alexscaves/server/item/SeaStaffItem.java), [`WaterBoltEntity.java`](https://github.com/Codx-org/AlexsCavesContinued/blob/523308608422ab8e31974befa7111ecdf495dd37/src/main/java/com/github/alexmodguy/alexscaves/server/entity/item/WaterBoltEntity.java); evidência do JAR em [auditoria exata](../EXACT-1.0.10-ARTIFACT-AUDIT.md).
