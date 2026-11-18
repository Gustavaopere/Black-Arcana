# ACFoodPropertiesItem — disposição de marcador vazio (1.0.10)

**Escopo:** disposição estática de componente técnico, sem ficha de habilidade independente e sem certificado de perk. Provider OPEN; NO_MUTATION.

## Identidade e evidência

- Artefato físico `alexscaves-1.0.10-neoforge+1.21.1.jar`, 75.279.314 bytes, SHA-1 `6960b299a39a039ac8a5eb9b07be4ad0e3e0a570`, SHA-256 `36ae0a3cbd028df466a37c671ba2fdf021c060ca1c9c1c32e9f2e95bffae0e7c`.
- Modlist sibling `68a85444b70d8752e128f47301084d34d8782828`, Minecraft 1.21.1, NeoForge, Java 21.
- Classe `com/github/alexmodguy/alexscaves/server/item/ACFoodPropertiesItem`, flags 1537 (public/interface/abstract), SHA-256 `78b5fe9d3b47072e4b1708fbd11129d2669c95a1b913f3bf2ba8946364cb5d3d`, 0 campos e 0 métodos declarados, sem superinterfaces.
- Censo das 1.555 classes: somente a própria interface (constant pool #1) e BiomeTreatItem (#289). Um implementador direto, zero indiretos, zero referências tipadas a membros da interface.
- Relatório nativo SHA-256 `5e7c6410a705ab9ce60b46f90db22f8611813eedeb9471aa7f26fff5cee28df9`, [execução de descoberta](https://github.com/Gustavaopere/Black-Arcana/actions/runs/44324891388/job/134873432907).

## Rota adjacente, não certificada como item

BiomeTreatItem estende CaveInfoItem e declara implements ACFoodPropertiesItem; o pai CaveInfoItem estende Item. O probe reconciliou os oito corpos declarados de BiomeTreatItem e os sete do ancestral interno. Não há despacho nativo provado pelo marcador. As rotas comportamentais ocorrem em métodos próprios, por exemplo:

| Método | Pivôs observados | Limite |
|---|---|---|
| BiomeTreatItem.use | offsets 9/17/27/30/33: isEdible, getCaveBiome, food, canAlwaysEat, canEat; 41 startUsingItem; 46 useConsume; 52 useFail; 61 usePass | Não é chamada de membro do marcador. |
| BiomeTreatItem.finishUsingItem | 1 getCaveBiome; 8/15 Player; 25 food level; 33 isCreative; 45 getBiome, 59 create, 62 retorno; 67 delegação ao pai | Ramo de associação ao bioma não certifica settlement, sidedness ou segurança do item. |
| BiomeTreatItem.onUseTick | corpo de 134 instruções examinado | Efeitos específicos e consumidores externos exigem ficha própria. |

A interface não define alcance, AOE, targeting, dano, duração, cooldown, mana, owner, custo, persistência, efeito ou mutação. N/A para esses eixos no marcador: não possui operação executável. A identidade do item implementador não autoriza alteração global de propriedades alimentares. Reflexão, mixins externos, dispatch transformado, registros e configuração em runtime não foram testados.

## Disposição e reprodução

`EMPTY_MARKER_SUPPORT_ONLY`, +0 fichas, +0 raízes, +0 certificados individuais. ACFoodBuilder e ACFoods são componentes distintos; BiomeTreatItem continua aberto para certificação própria. Black Arcana conserva autoridade mágica; não há hook mutador homologado.

[Manifesto](EXACT-FOOD-PROPERTIES-ITEM-MARKER-1.0.10.json) · [auditor](../../../../docs/qa/alexscaves_1010_food_properties_item_probe.py) · [regressões](../../../../docs/qa/alexscaves_1010_food_properties_item_probe_test.py).

```sh
python3 docs/qa/alexscaves_1010_food_properties_item_probe.py --jar <JAR-exato> --javap <javap-21> --output build/food-properties-item-1010/report.json
AC_FOOD_PROPERTIES_REPORT=build/food-properties-item-1010/report.json python3 docs/qa/alexscaves_1010_food_properties_item_probe_test.py -v
```

Próximo símbolo alfabético após reconciliação do prefixo: ACFoods. `mutating_hook=NOT_VERIFIED`, `physical_qa=NOT_TESTED`, `perk_certification=NOT_CERTIFIED`.
