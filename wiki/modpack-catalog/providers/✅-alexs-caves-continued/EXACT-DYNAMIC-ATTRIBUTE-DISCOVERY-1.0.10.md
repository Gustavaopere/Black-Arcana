# ACDynamicAttributeItem 1.0.10 — descoberta SHA-exata de ABI e consumidores

```text
claim_scope=SHA_EXACT_DISCOVERY_ONLY_NOT_CERTIFIED
static_technical_contract=NOT_CERTIFIED
artifact_version=1.0.10
artifact_sha1=6960b299a39a039ac8a5eb9b07be4ad0e3e0a570
artifact_sha256=36ae0a3cbd028df466a37c671ba2fdf021c060ca1c9c1c32e9f2e95bffae0e7c
artifact_size_bytes=75279314
mutating_hook=NOT_VERIFIED
physical_qa=NOT_TESTED
mutation=NO_MUTATION
provider_universe_closed=false
semantic_magic_roots_delta=0
```

## Fonte, abrangência e contabilidade

O [auditor read-only](../../../../docs/qa/alexscaves_1010_dynamic_attribute_probe.py) abriu o publisher **alexscaves-1.0.10-neoforge+1.21.1.jar**, de CurseForge projeto 1645389/arquivo 8856293, validou 75.279.314 bytes, ambos os hashes e os **1.555 classfiles** Java 21, e confrontou caminhos ZIP com os owners declarados. A [modlist sibling](https://github.com/Gustavaopere/neoforge-rpg-skilltree/blob/main/PROJECT-INSTRUCTIONS/modlist/World%20Gen/%E2%9C%85-alexs-caves-continued%20v1.0.10.md) confirma o artefato exato na posição física #19. O código público Codx-org/AlexsCavesContinued @ 523308608422ab8e31974befa7111ecdf495dd37 declara **1.1.1**, é adjacente e não serve de autoridade para parâmetros da 1.0.10.

Este recorte só fecha **o censo de declarações e os corpos selecionados**, não a semântica integral de todos os itens. O relatório JSON temporário (artefato do workflow) conserva o classpath/roster, hashes por classfile, descritores, referências tipadas e instruções de métodos selecionados. O JAR, código alheio e assets não são versionados.

**Interface exata:** com/github/alexmodguy/alexscaves/server/item/ACDynamicAttributeItem, classfile SHA-256 **22671a5b460c001b73982a2cff6c555f52559ee3390d48728c7ccff04c9e52be**. Define um método **público abstrato** acModifiers(EquipmentSlot,ItemStack):Multimap, descritor JVM **(Lnet/minecraft/world/entity/EquipmentSlot;Lnet/minecraft/world/item/ItemStack;)Lcom/google/common/collect/Multimap;**, access flags **1025**, sem corpo próprio.

O censo encontrou **sete implementadores diretos** e **três subclasses atribuíveis por herança dentro do publisher**, ExtinctionSpearItem, FrostmintSpearItem e LimestoneSpearItem, cujo método vem de SpearItem. As referências CONSTANT_Methodref com o nome acModifiers pertencem aos próprios sete implementadores; não demonstram um caller NeoForge externo. Não existe prova de dispatch do engine por mera declaração.

## Sete corpos próprios de acModifiers, indexação e retornos

Todos têm o descriptor da interface e são públicos, sem exception handlers no corpo. O hash listado é do atributo Code, não do classfile.

| Implementador direto em server/item | Code SHA-256 | Bytes | Retorno estático do corpo |
|---|---|---:|---|
| DivingArmorItem | 58f64ea8dc4a948b39982a1401ef374232b19000d863bd256b793def406771ba | 22 | acSlot.getSlot() correspondente → campo divingArmorAttributes; diferente → ImmutableMultimap.of() |
| GingerbreadArmorItem | 1b24de0379720c175d5baf54153113551d0fcd539913a73cf11700bc3894fd99 | 30 | slot correto → getOrCreateDurabilityAttributes(damage,maxDamage); diferente → ImmutableMultimap.of() |
| OrtholanceItem | 713afd60cedfafa0d4efcf1c6c587065448336750da17a8cb3a581aefdd14fa4 | 16 | MAINHAND → defaultModifiers; outro slot → null |
| PrimitiveClubItem | 4ac265cccbde09cbcd95261bd83e24b2f226434f5970fb0ef078f2152a696c81 | 29 | MAINHAND → defaultModifiers[clamp(enchantLevel(SWIFTWOOD),0,3)]; outro slot → null |
| SharpenedCandyCaneItem | 3bd5e22a894aa23700f10b1d26dcb897caba1f231d7d9e71e80735a9fd88eb7a | 16 | MAINHAND → defaultModifiers; outro slot → null |
| SpearItem | 3e498329ea5c1d9f3107ac39631e20a348c7ca470e4235d70d208c3154aa9ad2 | 16 | MAINHAND → defaultModifiers; outro slot → null |
| TotemOfPossessionItem | 3162c7dec1dafe79f70f448391ad3aad18ca2803033bb41acdf1ded1588cb3e3 | 16 | MAINHAND → defaultModifiers; outro slot → null |

**Pivôs delimitados:** slots de armadura @0–8 e retorno vazio @18 (Diving) ou @26 (Gingerbread); armas de mão @1/4, defaultModifiers @8 e retorno null @14; Primitive Club lê SWIFTWOOD @10, ACCompat.enchantLevel @13, aplica clamp 0..3 @22–24 e seleciona array @27. O contrato completo e a fórmula de ataque de **Swiftwood** já são certificados na [ficha do encantamento](enchantments/swiftwood.md) e na [prova 1.0.10](EXACT-SWIFTWOOD-STATIC-1.0.10.md), sem criar segundo certificado para o mesmo efeito.

## Bridge de componentes e distinção essencial entre null e vazio

Os sete implementadores declaram getDefaultAttributeModifiers(ItemStack) com **oito instruções** por corpo; em **@14** invocam **ACCompat.itemAttributes(BiFunction,ItemStack,Supplier)**. A implementação nativa desse overload tem **48 instruções**: cria builder @0; itera **EquipmentSlot.values()** @7–84; solicita o Multimap via BiFunction.apply @38; ignora **null** @50–53; em retorno **não null**, marca answered=true @56, determina EquipmentSlotGroup.bySlot @61 e acrescenta entradas com Multimap.forEach @76; se respondeu a algum slot, devolve builder.build @93, caso contrário usa Supplier.get @100.

O overload de suporte **ACCompat.itemAttributes(Multimap,EquipmentSlot,Supplier)** tem **19 instruções**. Se o Multimap é **null**, chama Supplier.get @5 e retorna o fallback @13. Para um valor não null, mesmo vazio, cria builder com grupo do slot, chama forEach @33 e retorna build @43.

Consequência lógica limitada ao código: **null = sem resposta**, enquanto **multimap vazio = resposta autoritativa sem entrada para aquele slot**. Assim, as duas armaduras retornam vazio quando consultadas fora de seu slot; as armas consultadas fora da MAINHAND retornam null, e o fallback de agregado só é escolhido quando **todos** os slots consultados responderam null. Isto não certifica aplicação real da componente aos atributos do jogador nem conflitos com outros mods/mixins/datapacks.

## Gingerbread — fórmula, cache e risco condicionado

Em **GingerbreadArmorItem.getOrCreateDurabilityAttributes(int damage,int maxDamage)** (73 instruções), o campo gingerbreadDurabilityDependentAttributes é consultado com **Map.containsKey(Integer.valueOf(damage)) @8**; uma chave presente retorna o Multimap @24–32. Em cache miss, o método calcula um float **r=damage/maxDamage** com i2f/i2f/fdiv @33–38 e um double **s=0.1D + 0.9D×(double)r** @39–49. Cria dois modificadores:
- **Attributes.ARMOR**, valor double de acDefense, operação **ADD_VALUE** @83–105;
- **Attributes.MOVEMENT_SPEED**, valor double s, operação **ADD_MULTIPLIED_BASE** @111–128.

O mesmo array ARMOR_MODIFIERS[acSlot.ordinal()] @51–61 fornece o identificador derivado do slot; o Multimap é construído em @134 e guardado por **Map.put(Integer.valueOf(damage), result) @149**, antes do retorno @157. Não há clamp nem validação explícita de maxDamage no trecho da divisão. A chave de cache é **damage**, **não o par damage/maxDamage**: se uma instância atender stacks com mesmo dano e maxDamage diferente, um valor anterior poderia ser reutilizado. Trata-se de **risco condicionado à variação externa de maxDamage**, e não de bug runtime demonstrado.

O valor s é argumento de **ADD_MULTIPLIED_BASE**, não velocidade final do jogador. Não se deduz APS, DPS, PvP, sincronização ou comportamento no movimento físico. Uma variação de durabilidade pelo equipamento é **input**, não débito efetuado pelo callback. As configurações de material/defesa são documentadas separadamente em [Armor Material](systems/armor-material.md).

## Provas negativas, limites e reprodução

As janelas verificadas não criam projétil, entidade, spell, mana, dano novo ou ataque em acModifiers. Não determinam owner/caster, alvo, LOS, raio, duração, cooldown, recarga, persistência ou mutação segura por jogador. Campos de atributos e cache de item são consumidores de configuração; **não** autorizam alteração global ou por perk na sessão física. O fallback usa APIs/ItemAttributeModifiers de Minecraft e NeoForge cujos efeitos e composição real não foram executados; **mutating_hook=NOT_VERIFIED**, **physical_qa=NOT_TESTED**, **NO_MUTATION**.

Reproduzir com JDK 21 e JAR SHA-exato (output JSON em caminho novo):

```sh
python3 docs/qa/alexscaves_1010_dynamic_attribute_probe.py \
  --jar /caminho/alexscaves-1.0.10-neoforge+1.21.1.jar \
  --javap /caminho/jdk-21/bin/javap \
  --output /caminho/novo/dynamic-attribute-discovery.json
AC_DYNAMIC_ATTRIBUTE_REPORT=/caminho/novo/dynamic-attribute-discovery.json \
  python3 docs/qa/alexscaves_1010_dynamic_attribute_probe_test.py -v
```

O [workflow read-only](../../../../.github/workflows/alexscaves-1010-dynamic-attribute-probe.yml) validou a identidade do artefato e **oito testes de pivôs nativos PASS** na [execução SHA-exata](https://github.com/Gustavaopere/Black-Arcana/actions/runs/44220000000) **(link de execução deve ser substituído pelo job real antes do merge)**. Os testes defendem contagens, branches e linhas de cálculo; não fecham a parametrização interna dos cinco mapas defaultModifiers nem a interface como um todo. Até aprofundar construção desses mapas, dispatch externo e ciclo engine de aplicação, o objeto permanece **⚠️ parcial** e não entra no manifesto de contratos estáticos certificados.
