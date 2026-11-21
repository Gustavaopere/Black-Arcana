# Galena Gauntlet — descoberta causal parcial SHA-exata (Alex's Caves Continued 1.0.10)

**Escopo:** `STATIC_DISCOVERY_ONLY`, ficha individual [equipment/galena-gauntlet.md](equipment/galena-gauntlet.md) em **⚠️ PARCIAL**. O inventário de métodos, seus hashes e callsites relevantes são provas estáticas da versão publisher, **não** certificação integral de contratos da Gauntlet, compatibilidade transformada, hooks mutadores ou QA física. `NO_MUTATION` · `mutating_hook=NOT_VERIFIED` · `physical_qa=NOT_TESTED` · `provider_universe_closed=false`.

## Proveniência e reprodução

- Modlist física no sibling: [Alex's Caves Continued 1.0.10](https://github.com/Gustavaopere/neoforge-rpg-skilltree/blob/main/PROJECT-INSTRUCTIONS/modlist/World%20Gen/%E2%9C%85-alexs-caves-continued%20v1.0.10.md), `alexscaves-1.0.10-neoforge+1.21.1.jar`, `modid=alexscaves`, Minecraft 1.21.1/NeoForge/Java 21, SHA-1 `6960b299a39a039ac8a5eb9b07be4ad0e3e0a570`.
- **JAR publisher realmente examinado:** SHA-256 `36ae0a3cbd028df466a37c671ba2fdf021c060ca1c9c32e9f2e95bffae0e7c`, 75.279.314 bytes, 1.555 classes. Um novo dump de JAR da instalação não foi confrontado com o publisher.
- **Classfiles observados:** `com/github/alexmodguy/alexscaves/server/item/GalenaGauntletItem` SHA-256 `5a74328a7130704a4e2dca9e607bed4dc3a468b8bbcb6d4e238b4d2d962573b0`; `com/github/alexmodguy/alexscaves/server/entity/item/MagneticWeaponEntity` SHA-256 `a26794c9eba89c554e812078886beda6129d5298219f685f6d0e2be315fbf071`.
- [Sonda](../../../../docs/qa/alexscaves_1010_galena_gauntlet_discovery.py) usa o censo tipado existente, disassembly de todos os métodos executáveis do item e da entidade, owners/consumers e registries/resources relacionados. [Validador fail-closed](../../../../docs/qa/alexscaves_1010_galena_gauntlet_static_checks.py) compara SHA de relatório, classes, roster, cada método e recursos com [manifesto imutável](EXACT-GALENA-GAUNTLET-DISCOVERY-1.0.10.json). [Workflow dedicado](../../../../.github/workflows/alexscaves-1010-galena-gauntlet-discovery.yml).
- **Execução de descoberta confirmada:** [run #44934418449](https://github.com/Gustavaopere/Black-Arcana/actions/runs/44934418449), job `136937828915`, PASS; relatório `report.json` SHA-256 `c91a48f9892be09c4ab951c8083703b0c5ffbb026fc43e7d808c2033dde8bba9`; artefato Actions `14719225697`, ZIP SHA-256 `7c72db7946900a66c7fd8f624505bd740812d8bc94193726f7cbb039b06cf516`, expiração declarada 05/12/2026. Os 17/24 métodos e os 6 recursos estão enumerados por identidade, assinatura, digest e tamanho no manifesto do repositório; o relatório completo permanece como artefato temporário. A validação adicional do manifesto com caso negativo só conta como aprovada após a CI da revisão correspondente.

Comandos reproduzíveis, após obter o publisher exato na versão indicada:

```sh
python3 docs/qa/alexscaves_1010_galena_gauntlet_discovery.py --jar /caminho/alexscaves-1.0.10-neoforge+1.21.1.jar --javap /caminho/java21/bin/javap --output build/galena-gauntlet-1010/report.json
python3 docs/qa/alexscaves_1010_galena_gauntlet_static_checks.py --manifest 'wiki/modpack-catalog/providers/✅-alexs-caves-continued/EXACT-GALENA-GAUNTLET-DISCOVERY-1.0.10.json' --report build/galena-gauntlet-1010/report.json
python3 scripts/catalog/generate_perk_ready_indexes.py --check
python3 scripts/catalog/check_perk_ready_indexes.py
```

## Artefato, propriedades de item e receita

**Classe `GalenaGauntletItem`:** 17 métodos com corpo, nenhum campo próprio declarado no censo. Construtor `<init>()V` pede `stacksTo(1)`, `durability(400)` e `Rarity.UNCOMMON`. `getEquipmentSlot()=OFFHAND`, `getEnchantmentValue()=1`, `getUseDuration(...)=72000` ticks, `getUseAnimation(...)=UseAnim.NONE`. `isEnchantable(ItemStack)` retorna verdadeiro para `getCount()==1`. Esses valores são do classfile, não confirmação de UI física ou efeitos herdados.

Recurso `data/alexscaves/recipe/galena_gauntlet.json` (SHA-256 `4354b2b27a8a0caa3073e499b5f0532919d16a97d0321776446f3cbca7301c6c`; 516 bytes) declara `crafting_shaped` com matriz `PPP / PTP / SNS`: **5** `alexscaves:packed_galena`, **1** `alexscaves:telecore`, **2** `alexscaves:ferrouslime_ball`, **1** `alexscaves:scarlet_neodymium_ingot` → **1** `alexscaves:galena_gauntlet`. A receita declarada não prova obtenção/execução física. `acExtraRepairMaterials` refere `PACKED_GALENA`; `isValidRepairItem` combina `ACRepairableItem.isExtraRepairMaterial` e super `Item.isValidRepairItem`.

O conjunto de recursos filename-matched no relatório contém **seis entradas**: modelo de item, advancement, receita, tag de encantabilidade, tag `ferromagnetic_items` e tag `galena_gauntlet_crystallization_items`. Não equivale à enumeração integral de todos os registries indiretos, traduções ou datapacks.

## Causalidade do uso e fronteiras não transacionais

| Método, versão 1.0.10 | Janela JVM reproduzida | Efeito solicitado e limite |
|---|---|---|
| `use(Level,Player,InteractionHand)` — 47 instruções | `CRYSTALLIZATION @35`, `enchantLevel @38`, tags `@58/@64`, `ItemStack.is @67`, `hurtAndBreakUsedHand @84`, `startUsingItem @89` | Controla elegibilidade de item da mão oposta e pede **1** de desgaste da Gauntlet fora de criativo; sem garantia da liquidação |
| `onUseTick(Level,LivingEntity,ItemStack,int)` — 120 instruções | `AABB.inflate(64,64,64) @121`, `getEntitiesOfClass @124`, `ItemStack.copy @193`, `setCount(0) @201`, `setItemStack @228`, `setControllerUUID @252`, `addFreshEntity @258`, `pop @261` | Procura instância controlada, retira stack original **antes** do pedido de spawn e descarta resultado do spawn; **sem rollback demonstrado**, sem confirmação de perda efetiva |
| `releaseUsing(ItemStack,Level,LivingEntity,int)` — 25 instruções | `addCooldown @26`, cache/som `@33/@48` | Pede cooldown **5 ticks** somente no ramo Player, limpa cache e som; não determina duração da entidade |

Essas três rotas são as mesmas que [Crystallization](enchantments/crystallization.md) já comprovou, mas **a certificação do encantamento não certifica automaticamente o item**. Crystallization apenas seleciona a tag de itens elegíveis `GALENA_GAUNTLET_CRYSTALLIZATION_ITEMS` em lugar da tag base `MAGNETIC_ITEMS` quando nível `E>0`. O escopo de target/efeito deve ser tratado como a **entidade nativa**, não como cast adicional.

## Tempo de uso, apresentação e sincronização

No método `acInventoryTick` (64 instruções), apenas o ramo `Level.isClientSide==true` manipula o temporizador da apresentação. O predicado `active` compara `LivingEntity.getUseItem().equals(stack)`. Quando `PrevUseTime != UseTime`, a rotina atualiza o campo anterior; se `active && UseTime<5`, solicita `setUseTime(UseTime+1)`; se `!active && UseTime>0`, solicita `setUseTime(UseTime-1)`. O método não garante que valores arbitrários fora do intervalo sejam clampados. `setUseTime` salva o antigo `UseTime` em `PrevUseTime` e escreve o novo; `getUseTime` devolve 0 quando o tag é nulo. `getLerpedUseTime(stack,partialTick)` calcula **`PrevUseTime + partialTick × (UseTime - PrevUseTime)`**, com defaults 0 se o tag está nulo. Este timer é visual/client-side, diferente do `getUseDuration=72000` e do cooldown 5.

`shouldCauseReequipAnimation(old,new,slotChanged)` suprime animação de reequip **somente quando ambos os stacks são Gauntlet**; o argumento slotChanged não aparece nas instruções selecionadas. `initializeClient` obtém extensão de apresentação via proxy/Citadel empacotado/NeoForge; não é contrato de authority de cast.

## Entidade controlada, dano, targeting e mineração

`MagneticWeaponEntity` possui **24 métodos executáveis** (contando `<clinit>`) e 17 campos. O resumo de métodos, digests e assinaturas encontra-se no [manifesto](EXACT-GALENA-GAUNTLET-DISCOVERY-1.0.10.json). Os consumidores de maior relevância incluem:

- `tick()V` (744 instruções): chama `hurtEntity` em dois ramos, consulta `FERROUS_HASTE` e `FIELD_EXTENSION`, usa `ProjectileUtil.getHitResultOnViewVector`, pode solicitar `Level.destroyBlock` em dois ramos. Esses callsites **não** provam dois ataques por uso nem autorização de destruição de mundo. O valor **64** do item não é alcance de raycast; a fórmula completa de alcance da entidade nesta versão continua **NÃO VERIFICADA**.
- `hurtEntity(LivingEntity,Entity)V` (141 instruções): `DamageSources.mobAttack` e `ACCompat.hurt` antes de efeitos pós-ataque e `damageItem(1)`, condicionados pela aceitação local; `getDamageForItem` delega `ACCompat.attackDamageBonus(stack)`. Dano efetivo, bônus externos, PvP e target filters finalizados: **NÃO VERIFICADOS**.
- `getDigSpeed(Player,BlockState,BlockPos)F` (80 instruções): `ItemStack.getDestroySpeed`, `ACCompat.miningEfficiencyBonus`, haste/fadiga, submersão, `onGround`, e `EventHooks.getBreakSpeed` do NeoForge. Nenhuma autorização de quebra por Black Arcana decorre do método.
- `damageItem(int)V`: resolve controller, checa criativo, `isDamageableItem`, pede desgaste da stack controlada; pode remover entidade ao atingir durabilidade máxima. Distinguir de desgaste da própria Gauntlet na ativação.
- `getController`, `getTarget`, `isOwnerWearingGauntlet`, `plopItem`, `getControllerHandPos`, `directMovementTowards`, `addAdditionalSaveData` e `readAdditionalSaveData` delimitam owner UUID, target ID, devolução/descarte e persistência. NBT próprio declara `WeaponStack` e `ControllerUUID`; efetivo reload, dimensão, inventário e autoria de dano continuam **NÃO VERIFICADOS**.

## Critérios pendentes de certificação

O censo completo de **41 corpos** (17+24) é evidência **da existência e assinatura** dos métodos, não análise causal integral de cada guarda/ramo transacional e das chamadas herdadas. Faltam: fórmula integral de range e dano aplicáveis, configuração ativa, verificação de engine NeoForge/Minecraft, limites de hitbox/targeting, resultado de `addFreshEntity`, devolução de inventário, proteção de mundo, compatibilidade com mods externos, casos de `null`/reload/ownership e QA física. A auditoria não promove automaticamente `PERK-READY-CERTIFICATIONS.json`.

**Integração segura:** o Black Arcana deve preservar `WorldEffectPolicy`, custos e autoridade do provider. RPG Skill Tree apenas integra perks/atributos/Mastery por boundary **real**. Sem hook individual mutador comprovado, permanece `NO_MUTATION` e fail-closed. Clean-room: a ficha oferece parâmetros e evidências de interoperabilidade sem copiar implementação, assets ou bytecode proprietários.
