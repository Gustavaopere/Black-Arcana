# ACRepairableItem — fronteira de referência 1.0.10 / Minecraft 1.21.1 / NeoForge 21.1.250

**Escopo:** evidência estática delimitada; candidato de descoberta #1124, sem certificado individual integrado. NO_MUTATION; mutating_hook=NOT_VERIFIED; physical_qa=NOT_TESTED.

## Identidade e materiais

O auditor [reprodutível](../../../../docs/qa/alexscaves_1010_repairable_item_boundary.py) verifica o publisher físico 1.0.10 por SHA-1 e SHA-256, o cliente vanilla oficial e mappings por SHA-256, e os artefatos NeoForge universal/userdev 21.1.250 por tamanho e hashes. [Job aprovado](https://github.com/Gustavaopere/Black-Arcana/actions/runs/44452908844/job/135320920618), relatório SHA-256 `03519b95b38412c1efccba0157f83c59dffc0e865dd55efe05c7c779ed2e789a`. O [manifesto](EXACT-REPAIRABLE-ITEM-BOUNDARY-1.0.10.json) sela hashes e descriptors de todos os métodos selecionados.

| Campo do registry | Literal de registro | putstatic offset |
|---|---|---:|
| ACBlockRegistry.PACKED_GALENA | packed_galena | 131 |
| ACItemRegistry.AZURE_NEODYMIUM_INGOT | azure_neodymium_ingot | 505 |
| ACItemRegistry.HEAVY_BONE | heavy_bone | 964 |
| ACItemRegistry.PURE_DARKNESS | pure_darkness | 2426 |
| ACItemRegistry.SCARLET_NEODYMIUM_INGOT | scarlet_neodymium_ingot | 488 |
| ACItemRegistry.TECTONIC_SHARD | tectonic_shard | 1117 |

PACKED_GALENA passa pelo helper registerBlockAndItem; os outros cinco pelo ACDeferredRegister.register. São bindings estáticos de nomes, não prova de execução da registry nem de disponibilidade de itens no pack. A classe SpearItem (SHA-256 `37b96d1b7936408c0dbd92f0a0715af8400ef55d452c196527e912c3eaf10583`) não declara isValidRepairItem com o descriptor auditado; sua superclasse é Item. Logo o fallback do ExtinctionSpearItem é resolvido na hierarquia externa, não numa segunda regra nativa do SpearItem.

## Elegibilidade e transação de referência vanilla

- ItemStack.is(Item) (Lcul;)Z compara identidade do getItem com o argumento @5 (if_acmpne); não é matching por NBT, tag ou quantidade nesse overload.
- Item.isValidRepairItem(ItemStack,ItemStack) retorna false. ShieldItem consulta ItemTags.PLANKS @1–4 e, em caso negativo, Item.isValidRepairItem @13. Assim, no recorte vanilla, o ResistorShieldItem soma os dois lingotes à regra herdada de tábuas; GalenaGauntlet/PrimitiveClub/ExtinctionSpear têm fallback Item=false. DesolateDagger não chama super. Tags efetivas e transforms instalados não verificados.
- AnvilMenu.createResult @156–175 verifica damageable e dispatch virtual Item.isValidRepairItem. No ramo de material elegível, calcula reparo por unidade r=min(D, floor(M/4)), com D damageValue e M maxDamage (inteiros, divisão JVM). Se r<=0, esvazia output, zera custo e retorna. Enquanto r>0 e unidades processadas < count do material: pede setDamageValue(D−r) @252, incrementa contador de custo @255, recalcula r @270 e incrementa unidades @275. Grava repairItemCountCost @284. Esse é o ramo de material, não toda a soma de encantamentos, nome, penalidade prévia ou preço final da bigorna.
- mayPickup exige custo positivo e (materiais infinitos ou experienceLevel >= custo); onTake chama giveExperienceLevels(−cost) @19 quando não instabuild, esvazia slot esquerdo @30, e reduz a pilha direita por repairItemCountCost @76 se houver excedente; senão a esvazia. Custo é zerado @127. Não é mana, Mastery nem um hook por unidade de reparo.

## NeoForge oficial

O patch AnvilMenu.java SHA-256 `ce25eb90f69a09d99546f3ae9c9147fb3681869c414990a3c0ee2fa0731ee2d0` conecta CommonHooks.onAnvilChange antes do cálculo default (entrada esquerda não vazia). A chamada posta AnvilUpdateEvent @22:
- cancelado: esvazia saída @41, custo e materialCost zero @48/53, retorna false;
- output vazio e sem cancelamento: retorna true @70 para cálculo normal;
- output fornecido: escreve output @78, custo @89 e materialCost @98, retorna false @102; o patch encerra cálculo default.
CommonHooks.onAnvilRepair posta AnvilRepairEvent @18 e retorna getBreakChance @26; o patch usa essa chance para a quebra/desgaste da bigorna, não como quantia reparada nem como API de débito de experiência. O evento de update dispõe de Player, output, custo e custo de material; o evento de repair dispõe de breakChance. Não confundir IItemStackExtension.isRepairable, canGrindstoneRepair e getXpRepairRatio com a elegibilidade particular do ACRepairableItem.

## Limites e caminho de integração

Superfícies reais de referência, não autorização para reescrever transações. Um perk que altera preço, quantia reparada ou material deve preservar autoridade de servidor, atomicidade, deduplicação e settlement; não reaplicar reparo após onTake. Mastery só por transação própria validada. A referência não prova execução no modpack, listener order, tags ativas, servidor físico, registro completo, quantidade/custo final ou segurança de hook. Mantidos NO_MUTATION/fail-closed e provider OPEN. O contrato individual depende da reconciliação alfabética com #1122 e #1123.
