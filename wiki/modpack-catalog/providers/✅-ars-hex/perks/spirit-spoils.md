# Spirit Spoils — ficha técnica para perks | Ars Hex 5.0.4b

**Tipo de evidência:** `SOURCE_CAUSALITY`, fonte exata de revisão alinhada à release 5.0.4b; **não** há prova de equivalência integral de bytecode com o JAR instalado nem QA de equip/unequip em jogador real. JAR físico `ars_hex-1.21.1-5.0.4b.jar`, SHA-1 documentado `2354710ea312e2a6e0fbc3eb2dbafb8e06f10cf4`. Minecraft 1.21.1, NeoForge; Malum presente na modlist.

## Delimitação adicional de operandos compilados — 17/10/2026

✅ [Prova SHA-exata Java21 #39089774180](../EXACT-PUBLISHER-NUMERIC-OPERANDS-5.0.4b.md): método `applyAttributeModifiers` lê o argumento inteiro `slotValue` (índice de variável local 3), além das referências de atributo/operação já comprovadas. Essa constatação não estabelece o valor efetivo de espíritos recebidos no host Malum. ⚠️ QA / ⛔ adapter.

## Prova binária adicional — 17/10/2026

✅ [JAR publisher SHA-1 exato, auditoria Java21 #39087382649](../EXACT-PUBLISHER-PERK-SCYTHE-REFERENCES-5.0.4b.md): `SPIRIT_SPOILS`, `ADD_VALUE` e `withModifierAdded` presentes no método compilado. **`slotValue` como quantidade** segue derivado do source; drop/RNG/payout de Malum não examinados. ⚠️ Player real e recompensa pendentes / ⛔ adapter.

## Evidência binária de dataflow concluída — 18/10/2026

✅ [Auditoria Java21 #39093013655](../EXACT-BINARY-PERK-SCYTHE-DATAFLOW-5.0.4b.md): o argumento `slotValue` é convertido e ligado ao `AttributeModifier` de `SPIRIT_SPOILS`, `ADD_VALUE`, antes de `withModifierAdded`. Não foi auditada a interpretação desse atributo nos drops/kill events do Malum ou sua concessão em player real. ⚠️ payout e equipamento / ⛔ perk/reward adapter.

## Identidade e propósito
- ID source: `ars_hex:thread_soul_spoils` (não `spirit_spoils`); classe `SpiritSpoilsPerk`.
- Descrição técnica (paráfrase): thread que eleva o atributo de Malum associado aos espíritos obtidos em eliminações elegíveis; **não** é fonte autônoma de espíritos.
- Registro de perk em `ArsNouveauRegistry.registerCompatPerks` exige `malum`; não cria spell, cast, evento de kill nem Mastery separada.

## Contrato exato observado no source

| Eixo | Observação |
|---|---|
| Atributo | `MalumAttributes.SPIRIT_SPOILS` |
| Quantidade | `slotValue` (linear, sem multiplicador local adicional) |
| Operação | `AttributeModifier.Operation.ADD_VALUE` |
| Modifier ID | `INSTANCE.getRegistryName()` |
| Equipamento | passa `EquipmentSlotGroup` do caller ao modificador |
| Técnica | `applyAttributeModifiers(ItemAttributeModifiers, ItemStack, int, EquipmentSlotGroup)` |
| Não aplicáveis | raio, projétil, velocidade, hitbox, tipo de dano, AOE, raycast, tempo de cast e cooldown |

**Equação de entrada:** `spirit_spoils_attribute_delta = slotValue`. A correspondência entre o atributo e o número efetivo de espíritos, elegibilidade de morte, RNG/caps e eventos de recompensa é **desconhecida nesta classe**; requer código/QA de Malum.

## Engenharia de integração
- Não criar segundo payout de espírito no `LivingDeathEvent`, nem interpretar uma alteração de atributo como kill ou spell. O host Malum conserva o mecanismo de liquidação e suas condições.
- Para perk de loot/recompensa do RPG Skill Tree, verificar um contrato observável *após* resolução de Malum e deduplicação por morte; sem boundary comprovado, **fail-closed**.
- **⚠️** Sem prova de stack no equipamento, atributo efetivo no jogador, persistência, loot real de Malum nem paridade binária dos métodos; **⛔** adapter/hook de reward não homologado.

## Proveniência
- [Registro condicionado — `ArsNouveauRegistry.java#L43-L48`](https://github.com/Alexthw46/Ars-Unity/blob/b25528adf8c0135585cd6d654582efa147e0a227/src/main/java/com/alexthw/ars_hex/ArsNouveauRegistry.java#L43-L48)
- [ID, atributo e operação — `SpiritSpoilsPerk.java#L14-L34`](https://github.com/Alexthw46/Ars-Unity/blob/b25528adf8c0135585cd6d654582efa147e0a227/src/main/java/com/alexthw/ars_hex/malum/perks/SpiritSpoilsPerk.java#L14-L34)
- [Índice local](../PERK-CAUSAL-ENGINEERING-MATRIX-5.0.4b.md)

**Clean-room:** sem replicação de código ou lógica de payout proprietária.
