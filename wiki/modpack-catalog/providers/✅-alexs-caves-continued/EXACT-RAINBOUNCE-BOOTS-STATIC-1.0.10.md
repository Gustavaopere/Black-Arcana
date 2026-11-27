# Rainbounce Boots — contrato técnico estático individual (Alex's Caves Continued 1.0.10)

**Estado restrito:** ✅ `CERTIFIED_STATIC_7_AXES` somente para a ação nativa observada de `alexscaves:rainbounce_boots`, `STATIC_TECHNICAL_CATALOG_ONLY`. Não é cast ou raiz mágica nova (`new_magic_roots=0`). `NO_MUTATION` · `mutating_hook=NOT_VERIFIED` · `perk_certification=NOT_CERTIFIED` · `physical_qa=NOT_TESTED` · `installed_transformed_runtime=NOT_VERIFIED` · `provider_universe_closed=false`. **O relatório original de descoberta continua `NOT_CERTIFIED` em seu próprio escopo; este selo acrescenta vínculo individual e testes, sem reescrever a descoberta histórica.**

## Evidência reproduzível e proveniência

Modlist do sibling `neoforge-rpg-skilltree`: Minecraft **1.21.1**, NeoForge, Java **21**, Alex's Caves Continued **1.0.10** `alexscaves-1.0.10-neoforge+1.21.1.jar`, SHA-1 `6960b299a39a039ac8a5eb9b07be4ad0e3e0a570`. Publisher examinado: **75.279.314 bytes**, SHA-256 `36ae0a3cbd028df466a37c671ba2fdf021c060ca1c9c1c32e9f2e95bffae0e7c`. Paridade com um novo dump da instalação não foi testada. Censo publisher: **1.555 classes**, quatro métodos do owner `com/github/alexmodguy/alexscaves/server/item/RainbounceBootsItem`, quatro owners de referência tipada, cinco recursos JSON de nome coincidente e hash; classfile owner SHA-256 `12809966af8256aa5c55e56b54d49f5be66e9785d6616ffa934c376f3d6d31bd`. Relatório reproduzível original `report.json`, SHA-256 `c7e60198eae632614c4a87acda39f385f49347409f47d0b178f5733362a7be60`, execução de descoberta [#44952856958](https://github.com/Gustavaopere/Black-Arcana/actions/runs/44952856958). Reexecução conforme [sonda](../../../../docs/qa/alexscaves_1010_rainbounce_boots_discovery.py) e [manifesto histórico](EXACT-RAINBOUNCE-BOOTS-DISCOVERY-1.0.10.json).

O enum de `ArmorItem.Type` foi examinado independentemente no **cliente oficial vanilla Minecraft 1.21.1**: `HELMET=0, CHESTPLATE=1, LEGGINGS=2, BOOTS=3, BODY=4`, classfile SHA-256 `304d6345c9ed3d0cdeaea281ed1171b98505b266c04e2b25a023dec665197732`, relatório SHA-256 `e83bef57b5efb722a17fefb237edb7288b1668d99d7dae67e51c1905c174ff91` ([sonda oficial](../../../../docs/qa/minecraft_1211_armor_type_enum_probe.py)). **Não é prova da classe NeoForge transformada.** A [auditoria do material](EXACT-ARMOR-MATERIAL-1.0.10.md) tem `RAINBOUNCE_ARMOR_MATERIAL` com defesa por ordinal `[2,2,1,2]`, multiplicador de durabilidade `6`, base `[13,15,16,11]`, encantabilidade `40`, toughness `0`, resistência a knockback `0` e reparo inicial `Ingredient.EMPTY`. Como a factory `ACItemRegistry.lambda$static$174` fornece `BOOTS`, o contrato nominal individual é **defesa 2** e **durabilidade máxima configurada 11×6 = 66**. Isso não certifica atributo aplicado na engine, consumo/recuperação de durabilidade ou reparo físico.

A [certificação individual de Rainbounce](EXACT-RAINBOUNCE-BOOTS-STATIC-1.0.10.json), o [checker fail-closed](../../../../docs/qa/alexscaves_1010_rainbounce_boots_static_cert_checks.py) e o [workflow de replay](../../../../.github/workflows/alexscaves-1010-rainbounce-boots-static-cert.yml) ligam report SHA-exato do publisher, enum oficial, material pinado, ficha e ledger de sete eixos. O workflow recompõe os relatórios e testa alterações negativas sintéticas, **sem executar gameplay**.

## Factory, ativação e targeting

Objeto individual: `alexscaves:rainbounce_boots`, `ACItemRegistry.RAINBOUNCE_BOOTS`, factory `lambda$static$174`, constructor `RainbounceBootsItem(ACArmorMaterial,ArmorItem.Type)`, slot `EquipmentSlot.FEET`. `EntityMixin.ac_move(MoverType,Vec3,CallbackInfo)` (20 instruções, instruction SHA-256 `4c47a6571a4ab6492d9275863923b16ff0c7996d58aa6149203f74239e2f772c`) filtra `LivingEntity`, exige `ItemStack.is(RAINBOUNCE_BOOTS)` em `FEET` e chama `RainbounceBootsItem.onEntityLand(living,inputVec3)`. Aplicação, prioridade, phase e duplicidade de callback do Mixin no modpack **NOT_VERIFIED**.

`onEntityLand(LivingEntity,Vec3)`, **134 instruções**, instruction SHA-256 `2005b5721f54d7100266965de674f8f5b22ab8a7c4d0c0936e784383dfe13ae8`, consulta `d=inputVec3.y` e `a=(float)abs(d)`; só entra no efeito sob as três guardas: `!living.isSuppressingBounce()`, `a>0.2F`, `d<0`. Os limites são exclusivos. Não há `use` ou `cast` no owner: o evento é consumo do callback de movimento de uma entidade viva equipada, não seleção de alvo inimigo.

## Parâmetros, causalidade, efeitos e consumidores

Em cada passagem elegível, a sequência nativa **solicita**:

```text
b = 1.05F, se a > 0.42D; senão 0.7F
c = 0.15000000596046448D, se BlockState(getOnPosLegacy()) está em
    REDUCE_RAINBOUNCE_BOOTS_EFFECT_ON; senão 1D
vertical_add = abs(d) * b * c
h = 1.2F, se living.hasEffect(SUGAR_RUSH); senão 1.9F
requested_delta = Vec3(v.x * h, v.y + vertical_add, v.z * h),
    onde v = living.getDeltaMovement() antes da chamada
```

O valor `a` é `float` na comparação `>0.42D`, portanto respeitar promoção de float a double e arredondamento JVM. A tag do bloco reduz apenas o acréscimo vertical, não `h`; `v.y` prévio é mantido e acrescido, não substituído. `Sugar Rush` é lido e não concedido. O owner solicita `setDeltaMovement(requested_delta)`, escreve `fallDistance=0F`, solicita um som `RAINBOUNCE_BOOTS_BOUNCE`, uma partícula `PLAYER_RAINBOW` e loop de **3 a 5** solicitações de `CLOUD`, com `nextInt(3)` reavaliado a cada verificação da condição do laço. Deslocamento efetivo, queda real, renderização, sincronização, clamps e resultados de servidor/cliente não foram medidos.

**Outros métodos da classe owner:** constructor (12 instruções), `getArmorTexture` (2, textura `alexscaves:textures/armor/rainbounce_boots.png`), `initializeClient` (6), mais `onEntityLand`; sem campos próprios, armazenamento NBT ou payload de rede no owner. Os consumidores tipados identificados no report são `EntityMixin`, `ACItemRegistry`, `ACArmorRenderProperties` (dois corpos de render) e autorreferência sem callsite. O censo tipado não prova ausência universal de reflexão, datapacks ou consumidores indiretos. Model, receita, advancement, tag de bloco e tag de reparo têm hashes no manifesto histórico; **seus conteúdos e execução real não foram homologados**.

**N/A no método de ação:** dano ofensivo, tipo de dano, LOS, raycast de inimigos, AOE ofensiva, hitbox/tamanho/velocidade de projétil, summons, teleporte, custo de mana, cast, charge, cooldown, duração fixa ou escala por nível/Mastery. Alcance é o próprio portador e a superfície consultada sob ele; não converter deslocamento `d` em raio. Não há escrita de mundo em `onEntityLand`. Duração da alteração de velocidade depende da física subsequente. Não há custo de desgaste próprio do impulso no owner; a durabilidade declarada do equipamento continua sujeita à engine. Persistência de `fallDistance` e `deltaMovement` não foi certificada.

## Boundary de perks e sete eixos de certificação

1. **Identidade:** ID, owner, factory e recursos, JAR publisher SHA-exato e `BOOTS=3` da enumeração oficial.
2. **Comportamento:** quatro corpos nativos, `EntityMixin.ac_move`, guardas de elegibilidade, ordem das ações no relatório.
3. **Parâmetros:** limiares, fórmulas, multiplicadores, chances e loops de partículas, defesa nominal 2, durabilidade solicitada 66 e encantabilidade 40.
4. **Targeting:** apenas `LivingEntity` vestindo o ID exato em `FEET`; consulta de superfície e de efeito, sem seleção ofensiva.
5. **Custos:** nenhum cast/mana/cooldown/desgaste próprio da ação, com reparo/uso da armadura herdado não testado.
6. **Integração:** `EntityMixin` é consumidor do provider, **não** hook per-player seguro para Black Arcana. Conceitualmente perks poderiam regular multiplicadores, limites e Sugar Rush, mas `mutating_hook=NOT_VERIFIED`; repetir `setDeltaMovement` ou callback poderia duplicar impulso e criar divergência client/server. `NO_MUTATION`.
7. **Validação:** report publisher, enum e material hashes, manifestos imutáveis, checker adversarial e CI específica; nenhum teste de modpack físico, hardware, cliente/dedicated server, colisão, fall damage ou sincronização de rede.

**Pendências separadas:** `installed_transformed_runtime=NOT_VERIFIED`, `mixin_injection=NOT_VERIFIED`, `physical_qa=NOT_TESTED`, `perk_certification=NOT_CERTIFIED`, `mutating_hook=NOT_VERIFIED`, `provider_universe_closed=false`. Nenhuma nova API foi inventada, e nenhuma implementação/asset de terceiros é copiada ao Black Arcana.