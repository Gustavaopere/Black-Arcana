# Humungous Hex — dimensões da Sugar Staff Hex (`alexscaves:humungous_hex`, 1.0.10)

**Contrato técnico estático:** ✅ `STATIC_TECHNICAL_CATALOG_ONLY` / `SHA_EXACT_BINARY_BEHAVIOR`, delimitado à seleção do encantamento, à produção de Sugar Staff Hex e aos consumidores de escala, AABB, dano e render. **Mutating hook:** `NOT_VERIFIED`; **QA física:** `NOT_TESTED`; **intervenção:** `NO_MUTATION`. O certificado não homologará alcance real, aumento de dano, alterações de renderer ou integração executável de perks; a homologação integral do provider permanece pendente.

## 1. Identidade, versão e proveniência

- **Provider:** Alex's Caves Continued, `mod_id=alexscaves`; modlist instalada: `alexscaves-1.0.10-neoforge+1.21.1.jar`, Minecraft 1.21.1 / NeoForge / Java 21 ([modlist sibling](https://github.com/Gustavaopere/neoforge-rpg-skilltree/blob/main/PROJECT-INSTRUCTIONS/modlist/modlist.md), entrada 019).
- **Artefato publisher exato:** CurseForge projeto `1645389`, arquivo `8856293`, **75.279.314 bytes**, SHA-1 `6960b299a39a039ac8a5eb9b07be4ad0e3e0a570`, SHA-256 `36ae0a3cbd028df466a37c671ba2fdf021c060ca1c9c1c32e9f2e95bffae0e7c`.
- **ResourceKey:** `alexscaves:humungous_hex`; caminho `data/alexscaves/enchantment/humungous_hex.json`, **364 bytes**, SHA-256 `8c45ec4c64e1ed5e258ce1a8d6a27b7693275336b76b91d108521fb91a015cc0`.
- **Tag de itens:** `data/alexscaves/tags/item/enchantable/sugar_staff.json`; SHA-256 `eb9f84b401224aba54ba91a239e4dd5b775d82012cecf9b03e8f9608e12b11fc`, com `alexscaves:sugar_staff`.
- **Traduções em `en_us.json`:** nome `Humungous Hex`; descrição: “Hexes have an additional full block in width for each level”. Essa frase corresponde à largura declarada da entidade, não ao aumento garantido do raio efetivo de dano. Tradução livre: um bloco a mais de largura por nível.

A evidência reproduzível está na [sonda SHA-exata](../../../../../docs/qa/alexscaves_1010_humungous_hex_probe.py), [manifesto de identidade e consumidores](../EXACT-HUMUNGOUS-HEX-CONTRACT-1.0.10.json), [resumo e limitações](../EXACT-HUMUNGOUS-HEX-CONTRACT-1.0.10.md), [contrato Sugar Staff Hex pré-existente](../actions/sugar-staff-hex-cast.md) e [evidência técnica comum do JAR](../EXACT-TECHNICAL-CONTRACTS-1.0.10.json). A fonte pública `Codx-org/AlexsCavesContinued@523308608422ab8e31974befa7111ecdf495dd37` declara **1.1.1** e não é autoridade de constantes para a versão 1.0.10.

## 2. JSON exato — regras de encantamento

| Campo | Publisher 1.0.10 | Interpretação |
|---|---|---|
| `description.translate` | `enchantment.alexscaves.humungous_hex` | Chave de idioma, não hook |
| `supported_items` | `#alexscaves:enchantable/sugar_staff` | Tag empacotada contém `alexscaves:sugar_staff` |
| `weight` | **5** | Peso de seleção, não chance de dano |
| `max_level` | **2** | Níveis normais I e II, sem afirmar clamp interno no consumidor |
| `min_cost` | base 1, incremento 9 | Custo declarativo I/II: **1/10** |
| `max_cost` | base 41, incremento 10 | Custo declarativo I/II: **41/51** |
| `anvil_cost` | **2** | Custo de encantamento, não durabilidade por cast |
| `slots` | `["mainhand"]` | Slot declarado pelo recurso |
| `exclusive_set`, `effects` | **Ausentes** desse JSON | Não provar compatibilidade global nem ausência de comportamento Java |

O recurso `spell_lasting.json`, separadamente selado no mesmo publisher (SHA-256 `839c95095540d2c40624575ad74aada2df482d7b4364d86fd8ebc238593a47dc`), tem nível máximo III e altera a duração, não a escala. Custos/níveis declarativos não são mana, consumo da habilidade, cooldown ou gates do RPG Skill Tree.

## 3. Produtor e fórmula de escala

O ramo agachado de `SugarStaffItem.use(Level,Player,InteractionHand)` cria uma `SugarStaffHexEntity` no solo determinado por `ACMath.getGroundBelowPosition`, atribui owner/posição, define escala e submete a entidade a `Level.addFreshEntity`. A chamada é do provider, não um cast independente do Black Arcana. O método contém `ACCompat.enchantLevel(stack,HUMUNGOUS_HEX)` e `setHexScale(float)`; as instruções de `use` foram reconhecidas no classfile SHA-256 `d670f887debdfb95f93a52b0c58b3033154a9aa20777fb8bd2a1673ee1407c3f`, com digest do método `76ba0a5bbf219e25f809c5e4d512fab3503f3e4dd99721e628787a7bde37d475`.

A expressão numérica no método nativo é:

**\`S = 1 + 0,25 × L\`**

em que **L** é o nível lido de Humungous Hex e **S** é a escala enviada a `SugarStaffHexEntity.setHexScale`. A entidade usa `getDimensions(Pose)` com largura `4F × S` e altura fixa `0.25F`; alteração do dado sincronizado de escala invoca `refreshDimensions` em `onSyncedDataUpdated`.

| Nível L | Escala S | Largura declarada da entidade | Altura declarada |
|---:|---:|---:|---:|
| 0 — sem encantamento | 1,00 | 4 blocos | 0,25 bloco |
| I | 1,25 | 5 blocos | 0,25 bloco |
| II | 1,50 | 6 blocos | 0,25 bloco |

A largura é dimensão **total**, não raio. Valores anômalos de L não têm cap do próprio cálculo observado; não tratá-los como níveis legalmente obtidos. A atualização de escala ocorre na entidade criada; não modifica o reach da Sugar Staff, duração de uso ou dimensão dos demais feitiços. `addFreshEntity` retorna booleano: uma chamada não garante spawn aceito nem contagem de hits.

## 4. Alvos, dano, render e tempo: canais independentes

**Consulta de entidades e dano.** `SugarStaffHexEntity.hurtEntities(boolean)` enumera `LivingEntity` na AABB da Hex e exige adicionalmente `LivingEntity.distanceTo(hex) <= 4F`. Exclui alvos aliados da Hex, o próprio owner e aliados do owner; no caso de Licowitch, o filtro especial `isFriendlyFire(target)` também governa a elegibilidade. O método solicita dano pela fonte `DamageSources.indirectMagic(hex,owner)`. O resultado de `hurt` e o knockback têm suas próprias condições nativas. Sua classe SHA-256 é `39f8d11595654ccebcb78540a2772106f0ae30507490570ac6b2cbe28de8e89c`, com `hurtEntities` digest `83b41481b0f5fcd819c2ea7590bb244e16954e728ee734f2c22a34d7b7f73ee9`.

**Geometria rigorosa:** aumentar a largura AABB de **4→5→6** pode alterar quais `LivingEntity` entram no conjunto inicial, mas o teste independente `distanceTo <= 4` **permanece**. Uma AABB maior não produz automaticamente alcance máximo 5/6, raio uniforme aumentado, dano multialvo garantido, penetração de blocos ou alteração de seleção de owner/aliados. O filtro de distância é aplicado à localização/caixa do alvo conforme a implementação da engine, não a um raio visual ilustrativo.

**Valor de dano.** A lógica do Hex solicita **1F** em condição ordinária e **6F** quando `despawnsIn < 5`; `tick` chama `hurtEntities(despawnsIn < 5)` após processar o contador. Humungous Hex **não** entra no ramo que escolhe 1F versus 6F. Essas são quantias *solicitadas* por tentativa, anteriores a imunidade/mitigação/recusa; não se presume hit por tick, dano cumulativo ou kill. O movimento nativo usa knockback e não autoriza outro pipeline de Mastery/dano.

**Renderer somente visual.** O classfile SHA-exato `client/render/entity/SugarStaffHexRenderer.class` (SHA-256 `f162cdc60c9c7c0d3622edc6a3a8bd103ac0f7bbc769aae62635fe7b4eb2b7d3`) consulta `getHexScale` em `render @75` após constante `4.0f @72` e multiplicação `@78`; no mesmo método aplica `PoseStack.mulPose @108` e `PoseStack.scale @119`. Usa `renderHex @139/@207` para desenho. O render é cliente e não controla diretamente AABB, targeting, dano, cooldown ou idempotência. O `SugarStaffModel` é outro classfile (SHA-256 `329b7c1e795671c99bd13563c6888b0f8d4978ea1d0f973f6eb7a1987bf7eb06`), não uma segunda entidade de dano.

**Duração independente.** `SugarStaffItem.use` configura `lifespan = 100 + 60 × nivel(SPELL_LASTING)`; duração declarada para níveis 0/I/II/III: **100/160/220/280 ticks**. Humungous Hex não aumenta esses valores, assim como não modifica 100 ticks de cooldown compartilhado pelo Sugar Staff. O callback de `tick` define `despawnsIn` a partir de lifespan se o contador está em `-1`, decrementa e pode descartar. O processamento não prova aceitação de todos os danos/efeitos ao longo desses ticks.

**Persistência e custo.** O NBT grava `DespawnsIn`, `Lifespan` e `Owner`, mas **não `HEX_SCALE`** nesse contrato. Isso exige cuidado com save/restart; não é prova de perda física de escala nem de restauração correta. O uso solicita um ponto de desgaste de durabilidade do Sugar Staff em `ACCompat.hurtAndBreakUsedHand` e o item tem durabilidade nominal 100. Não há um débito nativo adicional por nível de Humungous Hex demonstrado. Não inventar taxa de dano ou recurso paralelo.

## 5. Fronteira de perks, integração e validação

O que a ficha disponibiliza para planejamento: `entity_width=4*(1+0.25*L)`, `entity_height=0.25`, `damage_selection=AABB∩distance<=4`, `damage_request=1/6`, `spell_lasting_duration=100+60*level`, `item_cooldown=100`, `visual_scale` e `owner_and_ally_filter`. Esses são **valores observados**, não opções configuráveis garantidas.

Sem hook seguro certificado, uma perk que mude `HEX_SCALE` após o spawn ou aumente a hitbox pode criar divergência entre cliente/servidor, persistência, raio de dano, custo, dano periódico, filtro de alvos e claims. A intervenção é **⛔ fail-closed** até existir boundary nativo estável, limites de poder, autorização server-side, causalidade/deduplicação e testes de world safety. Black Arcana não copia `hurtEntities`, não relança a entidade, não redefine mana/cooldown/dano, nem transforma ticks em casts independentes; RPG Skill Tree só oferece progressão/perks por contrato real.

A sonda read-only compara **SHA-1/SHA-256/tamanho do JAR**, recursos `humungous_hex`, `spell_lasting`, tag e classfiles compilados, além de descritores/digests selecionados, sem redistribuir JAR/bytecode integral. A auditoria de Sugar Staff Hex existente identifica o lifecycle, escala, dano, cooldown e persistência, e o renderer foi reinspecionado no publisher exato. Faltam **QA em cliente e servidor físico, addons/datapacks, reload, PvP/claims, nível anômalo e hooks de mutação**. Nenhum sucesso de CI equivale a essas observações físicas.

**Escopo do certificado:** somente contrato técnico estático desta identidade; **`mutating_hook=NOT_VERIFIED` · `physical_qa=NOT_TESTED` · `NO_MUTATION` · universo de Alex's Caves aberto**.
