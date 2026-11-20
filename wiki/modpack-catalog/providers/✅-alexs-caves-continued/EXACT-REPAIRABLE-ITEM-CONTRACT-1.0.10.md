# ACRepairableItem — contrato estático delimitado 1.0.10

**CERTIFIED_STATIC_7_AXES / STATIC_TECHNICAL_CATALOG_ONLY / SHA_EXACT_BINARY_BEHAVIOR** — candidato #1124. NO_MUTATION; mutating_hook=NOT_VERIFIED; physical_qa=NOT_TESTED; runtime_dispatch=NOT_VERIFIED; perk_certification=NOT_CERTIFIED; provider_universe_closed=false.

| Eixo | Evidência |
|---|---|
| identity | Publisher 1.0.10 SHA-1/SHA-256/size; interface flags 1537, zero fields, three methods; five direct implementers, zero indirect, one in-JAR ancestor, six typed reference owners across 1555 classes. |
| behavior | Getter ABI, default false and dagger true, complete helper loop with ItemStack.is(Item) short circuit; all five material producers and isValidRepairItem overrides, six registration bindings; fallback hierarchy and engine reference separated. |
| parameters | Six literal material fields and registry paths, array cardinalities 1/1/1/1/2; identity vs tag matching; vanilla per-material restoration min(D,floor(M/4)), loop bounded by stack count and remaining damage; raw material eligibility does not set cost. |
| targeting | No entity targeting, AOE, LOS, projectile, damage application or cast. Receiver equipment and material ItemStack are the predicates' inputs; player/slots in external anvil reference only. |
| costs | Helper does not spend resources or repair. Vanilla createResult increments base cost per material, onTake deducts experience levels when not instabuild and settles right stack count; final anvil price not determined by this interface. |
| integration | Native override calls and registry suppliers; ACItemRegistry contract reused for five item bindings, block binding bounded to literal and helper. Official Minecraft 1.21.1 and NeoForge 21.1.250 AnvilUpdateEvent/AnvilRepairEvent boundaries; no verified safe mutating hook. |
| validation | Job 135321798629 on 60869d51 passed 4 native plus 5 boundary regressions; replay SHA-exact reports and ledger/card/index gates required on final HEAD. No installed transform or physical execution. |

## Prova e escopo causal

O [manifesto de descoberta](EXACT-REPAIRABLE-ITEM-DISCOVERY-1.0.10.json) e a [prova nativa](EXACT-REPAIRABLE-ITEM-DISCOVERY-1.0.10.md) selam roster, corpos selecionados, hashes e referências. A [prova da fronteira](EXACT-REPAIRABLE-ITEM-BOUNDARY-1.0.10.md) e seu [manifesto](EXACT-REPAIRABLE-ITEM-BOUNDARY-1.0.10.json) delimitam registro, ancestral e engine de referência. Os cinco campos de ACItemRegistry são vinculados aos caminhos literais no [contrato integrado de registro](systems/item-registry.md); PACKED_GALENA conserva a prova do nome e chamada registerBlockAndItem, não o contrato integral de ACBlockRegistry.

Não há campos de estado na interface. Seu método abstrato fornece materiais; default acReplacesTierRepairMaterials retorna false, e a única substituição observada é DesolateDagger=true. Não há member ref nativo ao booleano no censo auditado. O dagger implementa de fato a regra exclusiva em isValidRepairItem. Os cinco getters criam arrays novos mediante Supplier.get (Galena usa Block.asItem); a helper percorre os itens retornando no primeiro match. Não introduz cache, custo, dano, alteração de stack nem owner. Falhas de null ou supplier não são tratadas localmente.

O fallback do ExtinctionSpear resolve a hierarquia SpearItem -> Item sem override do descriptor no ancestral nativo. Item retorna false e ShieldItem testa PLANKS ou super na referência não transformada. O ResistorShield conserva a regra de tábuas nessa referência; não se afirma o conteúdo de tags ativas. Nenhum fallback completo de item ou entidade é recertificado como habilidade.

## Validação

JAR SHA-1 6960b299a39a039ac8a5eb9b07be4ad0e3e0a570, SHA-256 36ae0a3cbd028df466a37c671ba2fdf021c060ca1c9c1c32e9f2e95bffae0e7c, 75279314 bytes. Censo 1555 classfiles. Classe alvo SHA-256 04a9b942d2459794503eebc1415a29c245710a0625f1a126f5df2714266d6a05. Nativo 6b930d9bc296c736278df961dea6db3b0af31789b39fd623df4cdea232016b2f, boundary 03519b95b38412c1efccba0157f83c59dffc0e865dd55efe05c7c779ed2e789a. Job histórico 135321798629: 4+5 testes. Auditorias reproduzíveis em [probe](../../../../docs/qa/alexscaves_1010_repairable_item_probe.py) e [boundary](../../../../docs/qa/alexscaves_1010_repairable_item_boundary.py). O [selo de sete eixos](EXACT-REPAIRABLE-ITEM-CONTRACT-1.0.10.json) e a [ficha individual](systems/repairable-item.md) devem permanecer reconciliados com ledger, inventário e índices. CI final após sincronização obrigatória.

Escopo estático de elegibilidade; não certifica pipeline integral de bigorna, equipamentos, registro em execução, integração mutadora nem QA física. Uma ficha e zero raízes mágicas; próximo ACSwingControlItem. Black Arcana mantém autoridade de runtime mágico; RPG Skill Tree é provider de progressão. Não reprocessar custo/efeitos após liquidação.
