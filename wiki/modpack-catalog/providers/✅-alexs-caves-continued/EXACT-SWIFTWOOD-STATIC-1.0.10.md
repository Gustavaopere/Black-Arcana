# Swiftwood 1.0.10 — auditoria binária SHA-exata de atributos do Primitive Club

`scope=STATIC_TECHNICAL_CATALOG_ONLY` · `evidence_grade=SHA_EXACT_BINARY_BEHAVIOR` · `mutating_hook=NOT_VERIFIED` · `physical_qa=NOT_TESTED` · `NO_MUTATION`.

## Origem e identidade

- Provider: Alex's Caves Continued `alexscaves`, Minecraft 1.21.1, NeoForge, Java 21.
- JAR publisher idêntico ao fingerprint físico conhecido: `alexscaves-1.0.10-neoforge+1.21.1.jar`, CurseForge `8856293`, 75.279.314 bytes.
- SHA-1 `6960b299a39a039ac8a5eb9b07be4ad0e3e0a570`; SHA-256 `36ae0a3cbd028df466a37c671ba2fdf021c060ca1c9c1c32e9f2e95bffae0e7c`.
- JSON `data/alexscaves/enchantment/swiftwood.json`, 363 bytes, SHA-256 `3d19fac156679ac53f49424b9bb828ad44a003d3d33a8b14dda303d50fc17551`, `supported_items=#alexscaves:enchantable/primitive_club`, `max_level=3`.
- Tag `data/alexscaves/tags/item/enchantable/primitive_club.json`, SHA-256 `71829c384be93b8cef1e090b6afafa621dcd4eeb520c7a66ab0e6524e8a6ae43`, inclui `alexscaves:primitive_club`.
- English locale no JAR: `enchantment.alexscaves.swiftwood` e `.desc`. Nomes oficiais servem de confirmação de identidade, sem substituir os consumidores compilados.
- Classe `PrimitiveClubItem.class`, SHA-256 `92bfb58cb5ed2c84dd6f989afad22c98209542889e30b6214c502dbff42fa1ac`; `ACEnchantmentRegistry.class`, `60006fab1b3b29f5f93c8365416815a12770cf8877a059298cb4ee82f7a92f32`; `ACCompat.class`, `333738f324e6e9d77a488e14b7e81b169c2b2d4f6db5171206a016ad0271f57b`.

## Prova JVM e fluxo de dados

**Construtor:** `PrimitiveClubItem(Properties)V`, **22 instruções**, SHA de parse `b849a765431f981c2be6ff1c178296daa8cfc3207f4501ab8d9ac377896c5972`: inicializa array `defaultModifiers` a partir de `getStatsForEnchantmentLevel`, uma entrada por nível indexado.

**Gerador:** `getStatsForEnchantmentLevel(I)ImmutableMultimap`, **33 instruções**, SHA `a724c693a064b959f9dbd6395a4ab430114a3b1318b888546180bb0c3e09333f`.

| Offsets | Evidência estática |
|---|---|
| `@5–24` | `Attributes.ATTACK_DAMAGE`, literal `8.0D` e `AttributeModifier.Operation.ADD_VALUE` |
| `@29–55` | `Attributes.ATTACK_SPEED`, `fconst_0`, `-3.75F`, `0.15F`, `iload_1`, `i2f`, `fmul`, `fadd`, `Math.min(FF)F`, `f2d`, `ADD_VALUE` |
| `@63–66` | Build/retorno dos modificadores do item, não dano aplicado ao alvo |

A fórmula nominal certificada para o nível indexado `L` é `speed_ADD_VALUE = min(0F, -3.75F + 0.15F×L)`. O bônus de dano `+8.0D` é **idêntico com e sem encantamento**. Cálculos se dão em `float` e são convertidos em `double`; números nominais decimais não devem ser rotulados como floats exatos representáveis.

**Selecionador:** `acModifiers(EquipmentSlot,ItemStack)Multimap`, **17 instruções**, SHA `cdb36891f41a21806ad79e3ac68339b261c3f5f834cfdf54720b337b8df3681d`: `MAINHAND@1/if_acmpeq9@4`, `null@7–8`, `SWIFTWOOD@10`, `ACCompat.enchantLevel@13`, `iconst_0@22`, `iconst_3@23`, `Mth.clamp(III)I@24`, seleção array `aaload@27`.

**Bridge nativa:** `getDefaultAttributeModifiers(ItemStack)`, **8 instruções**, SHA `3ef89b9927daf6ddd6d8fa7d826e2a8a1eeb788a12faef74ad3c1d99918252e4`; em `@14` invoca `ACCompat.itemAttributes(BiFunction,ItemStack,Supplier)`. A lambda `lambda$getDefaultAttributeModifiers$0`, **4 instruções**, SHA `cb75b22e942d400bf70796038c5bd88e56cbb64f14239de3aa50b9d3064488d7`, aponta para o default de `Item`. `ACCompat.itemAttributes(BiFunction,ItemStack,Supplier)` tem **48 instruções**, SHA `75e48e223681347822ad84fd6ac8a6f545d6368457be30608b5928d1fac40809`; a sobrecarga `(Multimap,EquipmentSlot,Supplier)` tem **19**, SHA `78458bf90e03969ad9054e041a356e40482bc3dc27f54edd4e278f264d331f09`.

A sonda valida explicitamente os offsets/operandos relevantes da fórmula e do selecionador, além de garantir o bridge; armazena hashes de outros métodos de item para futuras auditorias. O método `acHurtEnemy` (**171 instruções**) e callbacks nativos de swing existem mas **não foram certificados como um efeito próprio de Swiftwood**. Censo direto em 1.555 classfiles: token `SWIFTWOOD` em registry e Primitive Club somente.

## Comandos reproduzíveis

```sh
python3 docs/qa/alexscaves_1010_swiftwood_static_probe_test.py -v
python3 docs/qa/alexscaves_1010_swiftwood_static_probe.py \
  --jar '/caminho/alexscaves-1.0.10-neoforge+1.21.1.jar' \
  --javap "$JAVA_HOME/bin/javap" \
  --seal 'wiki/modpack-catalog/providers/✅-alexs-caves-continued/EXACT-SWIFTWOOD-STATIC-1.0.10.json'
python3 scripts/catalog/check_perk_ready_indexes.py
python3 scripts/catalog/generate_perk_ready_indexes.py --check
```

A execução read-only do publisher JAR e os testes de fórmula/guardas foram verificados no [GitHub Actions run 42534407134](https://github.com/Gustavaopere/Black-Arcana/actions/runs/42534407134). [Manifesto selado](EXACT-SWIFTWOOD-STATIC-1.0.10.json). O JAR e o código de terceiros **não são versionados** no repositório; conservam-se apenas fatos de interoperabilidade, hashes, janelas JVM delimitadas e contratos próprios.

## Limites de certificação

Não há prova de novo cast, feitiço, projétil, targeting, AOE, dano adicional causado por Swiftwood, duração ou cobrança própria de mana/stamina/cooldown. Sua ação é uma contribuição de atributo calculada a partir da stack e do nível indexado. O pipeline de swing, dano final/aceito, componente efetivamente aplicado pelo motor, sincronização com outros mods, PvP, NBT e reload ficam fora desta prova. Não é possível inferir DPS ou ataques por segundo finais de um `ADD_VALUE` isolado.

Este é **um contrato técnico estático individual**; a aplicação física do atributo e o comportamento de componentes/overrides em servidor não foram testados. Nenhum hook mutador próprio de Black Arcana foi comprovado: `NO_MUTATION`. A integração de Mastery/perks requer autorização/contrato independente, testes de autoridade server-side e prevenção de duplicações. O universo integral de Alex's Caves Continued permanece aberto.
