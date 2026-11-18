# ACDynamicAttributeItem — construção dos mapas e referência NeoForge 21.1.250

**Estado:** descoberta SHA-exata ampliada; contrato individual **⚠️ parcial / NOT_CERTIFIED**. Esta evidência suplementa o [dossiê de descoberta](EXACT-DYNAMIC-ATTRIBUTE-DISCOVERY-1.0.10.md), sem acrescentar ficha ou raiz mágica. Não habilita hook ou perk.

## Autoridade e reprodução

A [execução de construção inicial](https://github.com/Gustavaopere/Black-Arcana/actions/runs/44306290596/job/134808593626), commit **249ea1e9565dd1aeecc3ab172b7735b94062d030**, leu o publisher 1.0.10 SHA-256 **36ae0a3cbd028df466a37c671ba2fdf021c060ca1c9c1c32e9f2e95bffae0e7c**, censo de **1.555** classes e artefatos oficiais **NeoForge 21.1.250** universal e userdev com tamanhos e ambos os hashes verificados pelo auditor de referência da #1117. Relatório inicial: [artefato CI](https://github.com/Gustavaopere/Black-Arcana/actions/runs/44306290596/artifacts/14427309899); SHA-256 do JSON **0886d3ffeb89a1bf7c6d7ade43f24c89f9f4d3e93233a8023294c472dc7693f7**. O artefato temporário tem retenção de 14 dias; os parâmetros e pivôs abaixo são preservados em documentação e testes reexecutáveis.

Executar o [auditor](../../../../docs/qa/alexscaves_1010_dynamic_attribute_construction.py) com JDK 21, JAR do publisher, universal e userdev oficiais:
```sh
python3 docs/qa/alexscaves_1010_dynamic_attribute_construction.py \
  --jar /caminho/alexscaves-1.0.10-neoforge+1.21.1.jar \
  --universal /caminho/neoforge-21.1.250-universal.jar \
  --userdev /caminho/neoforge-21.1.250-userdev.jar \
  --javap "$JAVA_HOME/bin/javap" --output /caminho/novo/report.json
AC_ATTRIBUTE_CONSTRUCTION_REPORT=/caminho/novo/report.json \
  python3 docs/qa/alexscaves_1010_dynamic_attribute_construction_test.py -v
```
A versão ampliada executou **6/6 testes** na [execução do commit cdf6cc6](https://github.com/Gustavaopere/Black-Arcana/actions/runs/44307123868/job/134811448297), com [artefato JSON](https://github.com/Gustavaopere/Black-Arcana/actions/runs/44307123868/artifacts/14428347370) SHA-256 **4439256ffa12570e5f20ec16d16df2912196b79297dc7757dda3a1d8dd608b77**. Os testes adicionais do último commit exigem nova execução.

## Valores nativos de mão principal (contribuições, não atributos finais)

| Owner | ATTACK_DAMAGE | ATTACK_SPEED | Operação |
|---|---:|---:|---|
| OrtholanceItem | 5D | -2.4000000953674316D | ADD_VALUE |
| SharpenedCandyCaneItem | 3D | +4D | ADD_VALUE |
| TotemOfPossessionItem | 2D | -2.4000000953674316D | ADD_VALUE |
| LimestoneSpearItem via SpearItem | 3D | -3D | ADD_VALUE |
| FrostmintSpearItem via SpearItem | 5D | -3D | ADD_VALUE |
| ExtinctionSpearItem via SpearItem | 8D | -3D | ADD_VALUE |
| PrimitiveClubItem | 8D | tabela Swiftwood 0..3 | ADD_VALUE |

Ortholance e Candy Cane: construtores de 30 instruções, offset 20 de dano, 44 de velocidade, 62 de armazenamento em defaultModifiers. Mesmo hash do Code **af6f5fea728f38268b4d857741f77f205560d3d4775b97832dc5604fe31d4d5b** não implica mesmos valores (os operandos são índices de constant pool; classfile e constantes diferem). Totem: 36 instruções, offsets 38,62,80; solicita durabilidade 1000 e raridade UNCOMMON na construção. SpearItem recebe double do construtor em @22 e insere -3D em @45; três subclasses passam 3D/5D/8D em @2, delegando em @5. PrimitiveClubItem preenche o array em @27–30; consultar [Swiftwood](enchantments/swiftwood.md) para a fórmula já certificada. Os valores de dano e velocidade são entradas de modificador, não dano aceito, taxa de acertos, dano de projétil, cooldown de cast ou DPS.

## Armaduras

DivingArmorItem (90 instruções do construtor, Code SHA-256 0c4cccc6945408536d00444c4fe556189b4fb16c6fc1a9269029a6711c5f39c6) usa o material recebido e o ArmorItem.Type. Em @52–73 solicita ARMOR=defense(type), ADD_VALUE. Para LEGGINGS (@78–110) solicita atributo de natação de ACPlatform.swimSpeedAttribute via ACCompat.attribute, **+0.5D ADD_VALUE**; para CHESTPLATE (@114–144), ARMOR_TOUGHNESS=toughness(), ADD_VALUE. Após esses ramos, knockbackResistance > 0 aciona KNOCKBACK_RESISTANCE=knockbackResistance(), ADD_VALUE (@145–178); mapa em divingArmorAttributes @184. Não implica valores fixos de defesa por slot sem material e ordem de enum comprovados.

GingerbreadArmorItem (62 instruções do construtor, Code SHA-256 016b54adf8722ae63575eb5560dc348390d69bc44aba9ac329cbc5077744cca6) cria HashMap em @22–29, guarda acSlot @34 e acDefense=material.defense(type) @40–43. Cria defaultAttributes de ARMOR/acDefense e MOVEMENT_SPEED/0.1D ADD_MULTIPLIED_BASE @73–125. Não confundir esse mapa inicial com o cache que acModifiers seleciona por damage e calcula usando 0.1+0.9*(float)damage/maxDamage: o callback usa getOrCreateDurabilityAttributes, e não defaultAttributes como saída direta. Material de defesa e durabilidade são documentados em [Armor Material](systems/armor-material.md). Reuso de cache por dano apesar de maxDamage variável permanece risco condicionado, não ocorrência física observada.

## Bindings nativos: quinze fábricas de ACItemRegistry

Os handles de bootstrap de <clinit> permitem relacionar o literal de registro imediatamente anterior a invokedynamic com a fábrica indicada, chamada register e armazenamento no campo. Este é binding estático, não prova de registro carregado na instância.

| Nome local de registro | Fábrica lambda$static$ | Classe |
|---|---:|---|
| primitive_club | 40 | PrimitiveClubItem |
| limestone_spear | 45 | LimestoneSpearItem |
| extinction_spear | 49 | ExtinctionSpearItem |
| diving_helmet / chestplate / leggings / boots | 99–102 | DivingArmorItem |
| ortholance | 110 | OrtholanceItem |
| totem_of_possession | 126 | TotemOfPossessionItem |
| sharpened_candy_cane | 172 | SharpenedCandyCaneItem |
| gingerbread_helmet / chestplate / leggings / boots | 187–190 | GingerbreadArmorItem |
| frostmint_spear | 192 | FrostmintSpearItem |

Diving usa DIVING_SUIT_ARMOR_MATERIAL; Gingerbread usa GINGERBREAD_ARMOR_MATERIAL. Fábricas de inventário/sprite adjacentes não são os mesmos bindings. Não se contam 15 habilidades mágicas ou novos certificados.

## Identidade de modificador, fallback e fronteira externa

Nos sete wrappers provider getDefaultAttributeModifiers(ItemStack), invokedynamic @1 vincula acModifiers do próprio owner, @9 vincula o supplier de fallback. Para seis owners o nome do fallback termina em $0; **TotemOfPossessionItem usa $1**, não $0. São handles de LambdaMetafactory, não chamadas de engine observadas. As duas lambdas ACCompat.lambda$itemAttributes$0/$1 chamam ItemAttributeModifiers.Builder.add @4. ACCompat.attributeModifier constrói ResourceLocation.fromNamespaceAndPath("alexscaves", path) @8, magnitude @11, operação e construtor de AttributeModifier @14; não presumir UUID original como identidade final ou ausência de colisão.

NeoForge **21.1.250 universal** (sha256 1f9cc68fe9ec0416475d34ce76e95a696b9721d5d338168563dab0632c3d2956) contém IItemStackExtension.getAttributeModifiers(): o método lê ATTRIBUTE_MODIFIERS com EMPTY de fallback (@6–15), testa lista vazia (@23–28) e, somente no ramo vazio, chama Item.getDefaultAttributeModifiers(ItemStack) virtualmente @46. Depois de ambos os caminhos, chama CommonHooks.computeModifiedAttributes(stack, modifiers) @57 e retorna o resultado. IItemExtension.getDefaultAttributeModifiers(ItemStack) tem default que invoca o método sem argumentos de Item @6; subclasses podem sobrescrever a variante stack-aware. A referência userdev SHA-256 deb6dd1e002aa85406e92501f49d5429cc8eaefe32fc353433e67030c32d8372 contém alterações nas duas variantes ItemStack.forEachModifier, com chamadas getAttributeModifiers().forEach antes da passagem separada de encantamentos. Os patches são referência upstream versionada e não um Minecraft transformado observado.

**Implicação para design de perks:** componente de atributos não vazio pode evitar a consulta dinâmica do item. Mudar um componente inteiro para implementar um bonus potencialmente suprime contribuições nativas; chamar manualmente acModifiers/reatribuir a saída também pode duplicar processamento. A fronteira CommonHooks/evento precisa ser analisada quanto a composição, autoria, operação e lado; nenhuma alteração é autorizada por sua mera existência. Ausência de hook seguro, QA física e compatibilidade testada mantém **NO_MUTATION**.

## Confirmação ampliada da identidade e da extensão externa

- **ACPlatform.swimSpeedAttribute()** (4 instruções, Code SHA-256 8d2b6d4ee1d8a8a153419ded325ac545a32fc8e3e96efc82a9f642b5acd19533): @0 lê NeoForgeMod.SWIM_SPEED (Holder), @3 chama Holder.value(), @8 converte para Attribute. **ACCompat.attribute(Attribute)** chama BuiltInRegistries.ATTRIBUTE.wrapAsHolder @4; não é um atributo inventado pelo Black Arcana.
- Os bootstraps StringConcatFactory dos construtores de armadura usam receitas **diving_armor.** e **gingerbread_armor.** seguidas pelo valor de ArmorItem.Type.getName(). ACCompat.attributeModifier forma ResourceLocation no namespace alexscaves a partir desse caminho; a factory não usa UUID nem nome descritivo como ID retornado. Não se afirma a ordem ordinal/nomes de enum externos além do que o publisher registra.
- Todos os sete suppliers de fallback têm quatro instruções; @2 é invokespecial à variante stack-aware de ArmorItem (Diving/Gingerbread) ou Item (cinco armas diretas), seguido de areturn @5. A seleção normal continua condicionada aos retornos null da implementação.
- **CommonHooks.computeModifiedAttributes**, classe universal SHA-256 86c8a56c77fff474bf4fe90f0354ad32698f018b5e19dc52a2725ee5ff96c73e, constrói ItemAttributeModifierEvent(stack, modifiers) @0–6, envia o evento a NeoForge.EVENT_BUS @10–14, depois chama event.build() @21. Não há argumento player nesse despacho.
- **ItemAttributeModifierEvent**, classe universal SHA-256 67913d84d62c3a016589816e9f4a80ce4ad26173717f95c2fdbbe77220421f0a, guarda stack @6 e defaultModifiers @11 no construtor. build() retorna o componente inicial se builder=null (@4–11), senão chama builder.build(defaultModifiers.showInTooltip()) @22–25. addModifier, removeModifier e replaceModifier encaminham ao builder interno (@7, @6, @7, respectivamente). Isso confirma superfície real de extensão **no artefato upstream**, não autoridade individual de caster, safe hook, ordem entre listeners ou execução instalada.
- Requisito para eventual integração: preservar o estado da stack, id/operação/slot, contribuição nativa e ordem da engine; resolver owner/perk por boundary real e validar recálculos repetidos, sidedness, stacking, conflitos de mod e ciclo de equipamento. Não escrever modificadores globais nem substituir o componente inteiro com base apenas nesta prova. Mantém NO_MUTATION.

## Limites

A auditoria inicial demonstrou os construtores, handles, bindings e o caminho externo até CommonHooks. Os auxiliares da natação, identificação do caminho de modifier, fallback de superclasse e despacho/build do evento foram observados na execução ampliada. Ficam em revisão semântica interna do builder e identidade final dos modificadores em todos os caminhos de construção, selo estável de certificação e comparação com o runtime realmente transformado. Não se certificam as habilidades completas dos equipamentos, targeting, dano final, uso de item, projéteis, ciclo de cache ou world safety por consequência desta auditoria. A contabilidade permanece 84/85 contratos estáticos observados, uma ficha parcial, sem nova raiz mágica, `mutating_hook=NOT_VERIFIED`, `physical_qa=NOT_TESTED`, provider OPEN.
