# ACTickingItem — descoberta SHA-exata 1.0.10

**DISCOVERY_NOT_CERTIFIED / NO_MUTATION.** Auditoria da interface e roster de consumidores, não certificação de cada poder ou item.

JAR publisher alexscaves 1.0.10, Minecraft 1.21.1, Java 21, SHA-1 6960b299a39a039ac8a5eb9b07be4ad0e3e0a570, SHA-256 36ae0a3cbd028df466a37c671ba2fdf021c060ca1c9c1c32e9f2e95bffae0e7c, 75279314 bytes. Censo de 1555 classfiles. Classe alvo SHA-256 a96fc5427180e594aa59c3272395c207f3570f49165e33af0fdfa429a9922a1e, flags 1537, zero campos, uma declaração abstrata acInventoryTick(ItemStack,Level,Entity,boolean)V. Registro físico conferido no sibling main 67ebba0d0194c74f9aa331853544cf16b0631790.

## Despacho observado

alexscaves.mixins.json declara ItemStackTickMixin em mixins (comum), pacote com.github.alexmodguy.alexscaves.mixin; SHA-256 6e120e2d2cf226a25cbe3d0605968a184384194354eac0b1153108f74632c140. O mixin ac_inventoryTick tem 19 instruções; getItem @8, instanceof @15, ifeq @18, checkcast @23, invokeinterface acInventoryTick @36. Único owner com referência de membro exata no censo. O descriptor do mixin possui int de slot, mas o callback expõe booleano e não slot numérico. Não inferir tick exclusivo de equipamento, execução somente servidor ou periodicidade efetiva sem inspecionar anotações, target e caller engine. A prova anterior de material/armadura é [reutilizável](EXACT-ARMOR-MATERIAL-1.0.10.md).

## Roster de implementadores

| Classe | Instruções no callback | Relações selecionadas (não exaustivas) |
|---|---:|---|
| CandyCaneHookItem | 39 | Estado de recolhimento e UUID do hook; canLaunchHook. |
| CaveMapItem | 167 | Validação de bioma, UUID do mapa, mensagens e fillOutCaveMap. |
| DarknessArmorItem | 123 | Encaminhamento para acArmorTick, medidor/chaves, tags e mensagens. |
| DreadbowItem | 192 | UseTime, PrevUseTime, PerfectShotTicks, níveis de encantamento e partículas. |
| GalenaGauntletItem | 64 | UseTime e PrevUseTime. |
| GazingPearlItem | 46 | Reputação Deep One, timestamp e atualização de tag. |
| HazmatArmorItem | 16 | Guard de armadura vestida e chamada acArmorTick. |
| OccultGemItem | 77 | Beholder, posição/dimensão, validação de estado e tag. |
| PrimitiveClubItem | 27 | Callback periódico distinto dos predicados de swing. |
| RadioactiveBlockItem | 73 | Callback periódico de radiação; regra e efeitos downstream em auditoria. |
| RadioactiveItem | 73 | Callback periódico de radiação; hash de instruções coincide com RadioactiveBlockItem. |
| RaygunItem | 109 | UseTime, carga, chance de recarga e condições de céu/sol. |
| RemoteDetonatorItem | 75 | Posição/dimensão da bomba, validação de bloco e remoção de tags. |
| ResistorShieldItem | 79 | UseTime, SwitchTime e valores prévios. |
| SackOfSatingItem | 159 | Alimentação, timestamp, som, criação de entidade de explosão e shrink. |
| SeaStaffItem | 42 | Chance e condição ambiental de recuperação de durabilidade. |
| ShotGumItem | 285 | Temporização, encantamentos, criação de GumballEntity, parâmetros de tiro e gasto de munição. |
| RadioactiveOnDestroyedBlockItem | herdado | Sem override de acInventoryTick no recorte; ancestral RadioactiveBlockItem. |

17 diretos, 1 indireto, dois ancestrais nativos (BlockItemWithSupplier e RadioactiveBlockItem). As 17 implementações declaradas e um dispatcher têm hashes, descriptors, número de instruções e crosswalk de invocações/escritas de campos no [manifesto](EXACT-TICKING-ITEM-DISCOVERY-1.0.10.json). Callsite não confirma que o ramo seja atingido, que spawn/dano/efeito seja aceito nem que a transação seja segura. O callback de ShotGum chama setDamage, shootFromRotation, setMaximumBounces e addFreshEntity; o de SackOfSating chama setSize e addFreshEntity de NuclearExplosionEntity, depois shrink. Essas ações precisam de auditoria individual de controle, parâmetros e consumidores antes de homologar perks; não criar scheduler duplicado.

## Validação e pendência

[Auditor](../../../../docs/qa/alexscaves_1010_ticking_item_probe.py) e [job aprovado](https://github.com/Gustavaopere/Black-Arcana/actions/runs/44669234165/job/136065935731), relatório SHA-256 c0c0b479729361af74fb5ca404df6997a792185973455c4e52089773fb84f72b. O gate geral verify 136065936134 falhou na configuração Gradle por resolução de gson:2.10.1 antes dos testes; nenhum teste dispensado. Próximo: replay do manifesto, anotação/injeção do mixin, caller vanilla/NeoForge, guards e parâmetros de cada callback delimitado; reconciliar #1126 antes da promoção de ledger. Provider OPEN; NO_MUTATION, NOT_VERIFIED, NOT_TESTED. Zero novos certificados/raízes nesta descoberta.
