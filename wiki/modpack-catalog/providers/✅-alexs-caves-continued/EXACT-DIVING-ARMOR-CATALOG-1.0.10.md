# Armadura de Mergulho — contratos individuais do Alex's Caves Continued 1.0.10

A prova usa o JAR publisher **8856293**, 75.279.314 bytes, SHA-1 `6960b299a39a039ac8a5eb9b07be4ad0e3e0a570` e SHA-256 `36ae0a3cbd028df466a37c671ba2fdf021c060ca1c9c1c32e9f2e95bffae0e7c`. O [selo reproduzível](EXACT-DIVING-ARMOR-CATALOG-1.0.10.json) registra os quatro bindings, sete corpos da classe de armadura, consumidores, recursos e referências fixadas. SHA-256 do selo `aa7c9dd45752291a507b3b210e59d1a94a934b63496c65c85573761d8f7d51f8`.

## Identidade, valores e condições de ativação

| Ficha | Factory `ACItemRegistry` | Slot | Defesa / durabilidade | Comportamento por peça |
|---|---|---|---|---|
| [Capacete de Mergulho](items/diving-helmet.md) | `lambda$static$99` | `HEAD` | 2 / 260 | Pede Respiração Aquática ao portador por 810 ticks quando seus olhos estão fora de fluido `WATER` ou seu veículo imediato é um `SubmarineEntity`. |
| [Colete de Mergulho](items/diving-chestplate.md) | `lambda$static$100` | `CHEST` | 6 / 300 | O ramo do colete adiciona toughness **0F** do material. Os três efeitos das outras peças não consultam este ID. |
| [Calças de Mergulho](items/diving-leggings.md) | `lambda$static$101` | `LEGS` | 5 / 320 | Adiciona **0.5D** por `ADD_VALUE` ao atributo `NeoForgeMod.SWIM_SPEED`, além da defesa. |
| [Botas de Mergulho](items/diving-boots.md) | `lambda$static$102` | `FEET` | 2 / 220 | Satisfaz o predicado do Muck que seleciona forma cheia de colisão e o ramo de movimento em contato. |

Os quatro suppliers retornam `Item` e constroem `DivingArmorItem(ACArmorMaterial,ArmorItem.Type)` com `DIVING_SUIT_ARMOR_MATERIAL`. O [material](systems/armor-material.md) fixa defesa `[2,6,5,2]`, multiplicador de durabilidade 20, array de bases `[13,15,16,11]`, encantabilidade 25, toughness e knockback 0F. A [referência de engine](EXACT-DARKNESS-ITEMS-CATALOG-1.0.10.md#referências-do-engine) já fixa o JAR e o mapeamento de `ArmorItem.Type`. Em `csf$a.<clinit>()V`, os trechos @0–17, @20–37, @40–57 e @60–77 constroem os ordinais 0 a 3 e nomes `helmet`, `chestplate`, `leggings`, `boots`. Os valores de durabilidade da tabela usam o array do provider.

O construtor @51–76 usa `material.defense(type)` com `ADD_VALUE`; @77–110 acrescenta natação apenas em `LEGGINGS`; @113–144 resolve toughness somente em `CHESTPLATE`; @145–178 acrescentaria resistência a knockback se o material retornasse valor maior que zero. `acModifiers(EquipmentSlot,ItemStack)` @0–21 devolve o mapa fixo para o slot escolhido ou mapa vazio. `ACCompat.itemAttributes` converte mapas por grupo de slot, e `ACCompat.attributeModifier` usa `alexscaves:diving_armor.` mais o nome do tipo como ID. O [contrato de atributos dinâmicos](systems/dynamic-attributes.md) detalha a composição e o evento upstream. Um componente explícito de atributos pode alterar a resolução desse caminho.

## Consumidores e alvo

O censo tipado cobre as **1.555 classes** do artefato. Seis owners têm referência de classe a `DivingArmorItem` ou referência de campo no registry para as peças/material. São o próprio item, `ACItemRegistry`, `ACCreativeTabRegistry`, `ACArmorRenderProperties`, `CommonEvents` e `MuckBlock`. Isso delimita consumidores diretos dentro do artefato. Usos genéricos da engine, configuração efetiva, mixins externos e efeitos de outros mods ficam fora do censo.

- `CommonEvents.livingTick(EntityTickEvent.Pre)` @126–191 consulta o item exato em `HEAD`, testa fluido nos olhos e veículo direto e chama `LivingEntity.addEffect` no portador. `MobEffectInstance(Holder,int,int,boolean,boolean,boolean)` recebe `WATER_BREATHING,810,0,false,false,true`. O retorno da chamada é descartado. A guarda de lado posterior está fora desse ramo.
- `MuckBlock.isOceanEntity(Entity)` @0–57 aceita tipo da tag `alexscaves:seafloor_denizens` ou `LivingEntity` com o item exato em `FEET`. `getCollisionShape` @0–55 seleciona cubo cheio para esse predicado ou `FallingBlockEntity` em contexto com entidade. O fallback é `Block.box(0,0,0,16,13,16)`. `entityInside` @0–93 exige `getInBlockState().is(this)` para entidades vivas. Entidades não vivas passam sem esse teste. Para predicado verdadeiro, solicita Y igual a `(double)((float)blockY+1F)` e soma `(0,0.1D,0)` ao delta. Para predicado falso, multiplica o delta por `(0.85D,1D,0.85D)`.
- `initializeClient` @0–15 pede as propriedades de render da proxy. `ACArmorRenderProperties` escolhe `DivingArmorModel`. O método de textura usa `diving_suit_1.png` para `LEGS` e `diving_suit_0.png` nos demais. [Seleção de renderizador](systems/custom-armor-post-render.md)

O portador, o slot de equipamento e, no Muck, a entidade do contexto de colisão definem quem recebe os efeitos. Os caminhos examinados operam sem alvo remoto, área de dano, projétil, consumo de mana ou recarga própria.

## Obtenção, reparo e custos

O pool publisher `alexscaves:chests/abyssal_ruins` tem **8–10 rolls** e as quatro peças têm peso **5** cada. A varredura de JSONs `data/` encontra os quatro IDs na loot table, no advancement de inventário e nos respectivos tags de armadura. Nenhum resultado de receita com esses IDs aparece no JAR. O guia do bioma e as duas localizações são recursos de descrição. Datapacks e outros mods podem acrescentar aquisições.

`CommonEvents.onEntityJoinWorld(FinalizeSpawnEvent)` @43–389 exige Drowned em `ABYSSAL_CHASM` com `FEET`, `LEGS`, `CHEST` e `HEAD` vazios antes dos quatro sorteios. São quatro chamadas de `nextFloat()` comparadas com `drowned_diving_gear_spawn_chance` (default **0.2D**, faixa **0..1**, `ACServerConfig.<init>` @177–199). Cada atribuição de peça pede drop chance **0.5F** no slot correspondente. O resultado efetivo de spawn e drop depende da configuração e do engine.

`ACItemRegistry.setup()` @54–70 passa `Ingredient.of(Items.COPPER_INGOT)` ao material. O JSON de reparo também lista cobre. A armadura usa a durabilidade do material. Desgaste de combate, custo da bigorna e resultado de reparo pertencem à engine.

## Reprodução e limites

```sh
python3 docs/qa/alexscaves_1010_diving_armor_catalog.py \
  --jar /caminho/alexscaves-1.0.10.jar \
  --javap "$JAVA_HOME/bin/javap" \
  --output /tmp/alexscaves-diving-armor-evidence.json
```

O verificador valida tamanho, SHA-1 e SHA-256 do JAR, lê os classfiles e recompõe os hashes de corpos, referências tipadas, ligações de factories e recursos do artefato. A saída exige igualdade com o selo. A [CI dedicada](../../../../.github/workflows/alexscaves-1010-diving-armor-catalog.yml) roda a mesma reprodução em Java 21.

As quatro fichas recebem `STATIC_TECHNICAL_CATALOG_ONLY`. A configuração efetiva do pack, a composição de atributos, a duração aceita dos efeitos e a ordem de colisão/movimento exigem QA em jogo. `mutating_hook=NOT_VERIFIED`, `physical_qa=NOT_TESTED`, `NO_MUTATION`. O escopo soma quatro fichas de equipamento passivo, zero raízes mágicas e mantém o provider aberto.
