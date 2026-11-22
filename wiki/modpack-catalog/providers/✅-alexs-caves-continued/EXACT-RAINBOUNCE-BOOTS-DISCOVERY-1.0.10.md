# Rainbounce Boots — descoberta causal SHA-exata (Alex's Caves Continued 1.0.10)

**Estado:** ⚠️ `STATIC_DISCOVERY_ONLY`, `static_contract=NOT_CERTIFIED`, `mutating_hook=NOT_VERIFIED`, `physical_qa=NOT_TESTED`, `NO_MUTATION`. Há **um item** conhecido nesta descoberta, mas **nenhuma nova raiz de magia/cast**. O universo do provider está **OPEN**. Esta auditoria descreve chamadas e argumentos nativos — não uma modificação executável de perk nem gameplay testado.

## Autoridade e cadeia de prova

A modlist física no sibling `Gustavaopere/neoforge-rpg-skilltree`, `PROJECT-INSTRUCTIONS/modlist/World Gen/✅-alexs-caves-continued v1.0.10.md`, identifica o mod ID `alexscaves` e a instalação `alexscaves-1.0.10-neoforge+1.21.1.jar` (Minecraft **1.21.1**, NeoForge, Java **21**, SHA-1 `6960b299a39a039ac8a5eb9b07be4ad0e3e0a570`). A auditoria obteve o **publisher JAR físico de 75.279.314 bytes**, SHA-256 `36ae0a3cbd028df466a37c671ba2fdf021c060ca1c9c1c32e9f2e95bffae0e7c`. A comparação com um dump novo da instância local, paridade com fontes de outras revisões e dependências externas continuam **NOT_VERIFIED**.

A descoberta foi executada em [GitHub Actions #44952856958](https://github.com/Gustavaopere/Black-Arcana/actions/runs/44952856958), job `136994394282`, **PASS** de sonda/read-only; artefato `14726446731`, `report.json` SHA-256 `c7e60198eae632614c4a87acda39f385f49347409f47d0b178f5733362a7be60`. Esse PASS **antecede** o checker SHA-exato introduzido na mesma PR; a CI da HEAD precisa reexecutar os gates. Reproduzir com [sonda](../../../../docs/qa/alexscaves_1010_rainbounce_boots_discovery.py), [verificador fail-closed](../../../../docs/qa/alexscaves_1010_rainbounce_boots_discovery_checks.py), [workflow](../../../../.github/workflows/alexscaves-1010-rainbounce-boots-discovery.yml) e [manifesto de classe, métodos e consumidores](EXACT-RAINBOUNCE-BOOTS-DISCOVERY-1.0.10.json). São **1.555 classfiles**, quatro métodos executáveis do owner, quatro owners referenciadores tipados (incluindo autorreferência sem callsite executável) e cinco recursos JSON filename-matched.

Owner: `com/github/alexmodguy/alexscaves/server/item/RainbounceBootsItem.class`, SHA-256 `12809966af8256aa5c55e56b54d49f5be66e9785d6616ffa934c376f3d6d31bd`. Extende `ArmorItem`; implementa `CustomArmorPostRender` e `ACClientExtensionItem`; sem campos próprios identificados. Nenhum ancestral do owner é classfile interno adicional no recorte de herança.

## Identidade, equipamento, material e recursos

- **ID:** `alexscaves:rainbounce_boots`; supplier `ACItemRegistry.RAINBOUNCE_BOOTS`; factory `ACItemRegistry.lambda$static$174`, **6 instruções**, SHA-256 `5a4f14aa8c35ae1004697b38488cad8c1e3d329bb4485af63bd452fec2b6f55a`.
- **Tipo / slot:** `ArmorItem.Type.BOOTS` no registry e `EquipmentSlot.FEET` no consumidor `EntityMixin.ac_move`. O gatilho lê a peça pelo slot exato; equipar outro item não satisfaz `ItemStack.is(RAINBOUNCE_BOOTS)`.
- **Material `RAINBOUNCE_ARMOR_MATERIAL`** (auditoria individual precedente em [armor-material](systems/armor-material.md)): multiplicador de durabilidade 6; vetor de defesa por **índice ordinal** `[2,2,1,2]`, durabilidade por **índice ordinal** `[78,90,96,66]`; encantabilidade 40, toughness 0F, knockback resistance 0F. Não converter posição do array para slot `BOOTS` sem verificar a ABI externa; material declarativo não garante absorção de dano final.
- **Recursos identificados e hashados:** modelo `assets/alexscaves/models/item/rainbounce_boots.json`, recipe `data/alexscaves/recipe/rainbounce_boots.json`, advancement `data/alexscaves/advancement/alexscaves/rainbounce_boots.json`, tag de superfícies `data/alexscaves/tags/block/reduce_rainbounce_boots_effect_on.json` e reparo `data/alexscaves/tags/item/repairs_rainbounce_armor.json`. O manifesto registra SHA-256 e bytes de cada recurso, mas **não** autoriza afirmar ingredientes, regras de receita, conteúdo da tag, drops ou reparo aceito no jogo.
- **Texture e cliente:** `getArmorTexture` retorna `alexscaves:textures/armor/rainbounce_boots.png`; `initializeClient` delega extensões ao proxy. `ACArmorRenderProperties.getACArmorModelBase` identifica o item para `RAINBOUNCE_ARMOR_MODEL` e `renderCustomArmor` possui referência `instanceof`. Renderização real **NOT_TESTED**.

## Contratos dos quatro métodos próprios completos

| Método JVM | Instruções | SHA-256 do corpo normalizado |
|---|---:|---|
| `<init>(ACArmorMaterial,ArmorItem.Type)` | 12 | `1c59bef51bc767350a0f79f732eac8355d4c7b6c50b864e6b32197f3a1efabf2` |
| `getArmorTexture(ItemStack,Entity,EquipmentSlot,String)` | 2 | `4a16426bec92aef93114cd86a2be5cf59ae72252bde57b2fafc339f2daa20bf9` |
| `initializeClient(Consumer)` | 6 | `241b312ebd6ff1e8ab0719a7fcbfd71c956258d303ba94e3a602770053402fa8` |
| `onEntityLand(LivingEntity,Vec3)` | 134 | `2005b5721f54d7100266965de674f8f5b22ab8a7c4d0c0936e784383dfe13ae8` |

A factory chama `material.vanilla()` e `material.properties(properties,type)` antes da inicialização `ArmorItem`. O efeito peculiar é o método **estático** `onEntityLand`; não é um `use` de item, cast de magia ou tick periódico no owner.

## Grafo consumidor e ativação

`com/github/alexmodguy/alexscaves/mixin/EntityMixin.ac_move(MoverType,Vec3,CallbackInfo)` possui **20 instruções**, SHA-256 `4c47a6571a4ab6492d9275863923b16ff0c7996d58aa6149203f74239e2f772c`. Ao receber uma entidade `LivingEntity` (`@5–16`), lê `getItemBySlot(EquipmentSlot.FEET)` (`@18–23`), compara com `ACItemRegistry.RAINBOUNCE_BOOTS` via `ItemStack.is` (`@26–37`) e, se elegível, solicita `RainbounceBootsItem.onEntityLand(living, inputVec3)` (`@43–46`). Sem bota/sem entidade viva retorna; os hooks externos do mixin, priority e a aplicação real da injeção na engine não foram reproduzidos em jogo.

Os outros consumidores tipados são `ACItemRegistry.lambda$static$174`, `ACArmorRenderProperties.getACArmorModelBase`, `ACArmorRenderProperties.renderCustomArmor` e o próprio classfile como autorreferência sem callsite executável. Nesses métodos, **nenhum mutador de perk por jogador foi identificado**. Ausência na pequena superfície observada não encerra todos os possíveis consumidores indiretos da engine.

## Cálculo do salto, offsets e unidades

Defina `d = inputVec3.y` (argumento do movimento entregue pelo consumidor, **não necessariamente** a velocidade atual), `a = (float)|d|`, e `v = living.getDeltaMovement()` no instante da invocação.

**Guardas**, na ordem de `onEntityLand`: se `living.isSuppressingBounce()` for verdadeiro (`@26–30`), se `a ≤ 0.2F` (`@33–37`), ou se `d ≥ 0` (`@40–46`), **não ocorre o ramo que solicita impulso, partículas e som**. Esses três gates são independentes da verificação da bota em `EntityMixin`.

Para queda elegível, o coeficiente base é:

```text
b = 1.05F se a > 0.42D; caso contrário b = 0.7F
c = 0.15000000596046448D se o BlockState em living.getOnPosLegacy()
    corresponde à tag REDUCE_RAINBOUNCE_BOOTS_EFFECT_ON; senão c = 1D
vertical_add = abs(d) * b * c
h = 1.2F se living.hasEffect(ACCompat.effect(SUGAR_RUSH)); senão h = 1.9F
requested_velocity = Vec3(v.x * h, v.y + vertical_add, v.z * h)
```

- O limite **`a > 0.42` é exclusivo**; a comparação efetiva em bytecode converte `a` float para double. Para `a=0.42` representado como float, considerar a semântica de arredondamento de `float` antes da comparação, sem inferir igualdade matemática exata.
- `REDUCE_RAINBOUNCE_BOOTS_EFFECT_ON` reduz somente o **incremento vertical calculado** nesse ramo, a aproximadamente 15%; não impõe limite global à velocidade, à proteção contra queda ou à movimentação em outros blocos. O `BlockState` é consultado via `level.getBlockState(living.getOnPosLegacy())` (`@49–91`).
- `SUGAR_RUSH` escolhe fator horizontal **1.2**, enquanto ausência do efeito escolhe **1.9** (`@93–121`). A chamada `Vec3.multiply(h,1,h).add(0,vertical_add,0)` (`@123–145`) **preserva a componente `v.y` existente antes de acrescentar o bônus**; afirmar que o novo y é apenas `vertical_add` seria incorreto.
- `LivingEntity.setDeltaMovement` recebe o vetor solicitado e `fallDistance=0F` é escrito (`@145–152`). Dano de queda efetivamente evitado, colisão, gravidade no próximo tick, simulação/replicação de movimento e clamps externos **NÃO VERIFICADOS**.
- Chama `LivingEntity.playSound(RAINBOUNCE_BOOTS_BOUNCE)`; solicita uma partícula `PLAYER_RAINBOW` usando posição anterior (`xo,yo,zo`) e ID de entidade como um dos argumentos da partícula (`@153–202`). Depois percorre um loop de partículas `CLOUD` com guard `i < 3+random.nextInt(3)` (`@208–277`); o valor aleatório do limite **é recalculado a cada verificação do loop**, não apenas sorteado uma vez. Sob retorno normal de `nextInt(3)`, o número de solicitações de nuvem é entre **3 e 5**, condicionado à execução do ramo; renderização/entrega efetiva não comprovada. `addParticle` não é confirmação de renderização.
- **Lado do mundo e owner:** não existe guarda explícita `level.isClientSide` nessa sequência do owner e o callee é `EntityMixin` aplicado a movimento; sem prova do dispatcher, não assumir autoridade exclusivamente server-side, deduplicação de chamadas entre lados, elegibilidade PvP ou comportamento multiplayer.

## Custo, alvo, persistência e escopo de perks

**Alvo:** a `LivingEntity` que veste as botas no slot FEET. Não existe aquisição adversária, raio, AOE, LOS, hitbox de projétil, dano de ataque, tipo de dano, alvo remoto, consumo de mana ou magia, cooldown, charge, cast, summon, portal ou modificação explícita de blocos **nos métodos dessa ação** (`N/A` por ausência de instruções correspondentes). A leitura do bloco é para ajustar o multiplicador; não há pedido de world-write nesse owner.

**Escala:** por `inputVec3.y`, superfície condicionada por tag e `SUGAR_RUSH`; nenhuma consulta própria a nível do encantamento, skill-tree, atributos, Mastery ou XP. **Custos:** sem decrementar durabilidade, energia ou item stack no corpo `onEntityLand`; o `ACArmorMaterial` contém atributos de armadura cuja mecânica executada pertence à engine. **Duração:** impulso instantâneo solicitado; velocidade posterior depende da engine. **Persistência:** owner sem campos próprios, NBT ou componente serializado; `fallDistance`, `deltaMovement` e efeitos visuais são estado/solicitações da `LivingEntity`/mundo, cujas consequências de logout, teleport, morte, reinício e sincronização não foram observadas.

**Possíveis perks em projeto:** fator de retorno vertical condicionado ao impacto, limite de altura, fator horizontal, superfície/categorias de bloco ou interação com Sugar Rush seriam candidatos de design. Isso **não implica** hook mutador verificado: a edição direta de `EntityMixin` ou `onEntityLand` pode gerar duplo impulso, side mismatch, bypass de colisões/claims, spam de partículas e inconsistência de velocidade. Sem uma extensão com owner e autorização server-side comprovados, **`NO_MUTATION` / fail-closed**. Black Arcana controla seu runtime mágico; RPG Skill Tree só pode prover progressão, atributos, perks e gates por boundary real.

## Limites e próximos gates

A prova identifica exatamente os quatro métodos do owner, a referência executável no `EntityMixin`, a factory e as interfaces de render. O manifesto fixa classes, descritores JVM, instruções, consumidores e cinco recursos. **Pendências:** inspeção da definição/configuração Mixin efetivamente aplicada, ABI de `Entity.move`, ordem antes/depois da colisão, checks de lado, forma dos packets, resolução do estado do bloco e conteúdo exato da tag, classe externa de `FoodData` não pertinente, hit/fall damage real, dano/defesa armor, cliente/servidor/multiplayer, integração segura com perks, limites de performance. Não executar implementação, promover root mágico, habilitar mutação ou marcar ✅ até que cada eixo relevante seja comprovado e individualmente validado.
