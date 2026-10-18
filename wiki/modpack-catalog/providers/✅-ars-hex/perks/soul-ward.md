# Soul Ward — ficha técnica para perks | Ars Hex 5.0.4b

**Tipo de evidência:** `SOURCE_CAUSALITY`, fonte exata de revisão alinhada à release 5.0.4b; **não** há prova de equivalência integral de bytecode com o JAR instalado nem QA de equip/unequip em jogador real. JAR físico `ars_hex-1.21.1-5.0.4b.jar`, SHA-1 documentado `2354710ea312e2a6e0fbc3eb2dbafb8e06f10cf4`. Minecraft 1.21.1, NeoForge; Malum presente na modlist.

## Delimitação adicional de constantes compiladas — 17/10/2026

✅ [Prova SHA-exata de operandos Java21 #39089774180](../EXACT-PUBLISHER-NUMERIC-OPERANDS-5.0.4b.md): `iconst_2`, double `0.5`, multiplicação e leitura de `slotValue` presentes no `applyAttributeModifiers`. Não há prova completa de fluxo da constante para cada modifier; equip/unequip de `ServerPlayer` e soma final permanecem ⚠️. Nenhum adapter.

## Prova binária adicional — 17/10/2026

✅ [JAR publisher SHA-1 exato, auditoria Java21 #39087382649](../EXACT-PUBLISHER-PERK-SCYTHE-REFERENCES-5.0.4b.md): `SoulWardPerk.applyAttributeModifiers` contém referências compiladas aos dois atributos Malum, operações `ADD_VALUE` e `ADD_MULTIPLIED_BASE`, e `withModifierAdded`. **2 × slotValue / 0,5 × slotValue** são fórmulas da fonte, **não dataflow dos operandos comprovado**. Ainda ⚠️ sem `AttributeInstance` de player real / ⛔ sem adapter.

## Evidência binária de dataflow concluída — 18/10/2026

✅ [Auditoria Java21 #39093013655](../EXACT-BINARY-PERK-SCYTHE-DATAFLOW-5.0.4b.md): a pilha compilada dos dois `withModifierAdded` foi rastreada até os construtores de `AttributeModifier`. **`SOUL_WARD_CAPACITY = 2 * slotValue`, `ADD_VALUE`**; **`SOUL_WARD_INTEGRITY = 0.5 * slotValue`, `ADD_MULTIPLIED_BASE`**, com `EquipmentSlotGroup` e registry ID da perk como operandos. Escopo: método compilado SHA-verificado, sem equip/unequip, stacking final de Malum ou `ServerPlayer` real. ⚠️ runtime / ⛔ adapter.

## Identidade e propósito
- ID source: `ars_hex:thread_soul_ward`; classe `com.alexthw.ars_hex.malum.perks.SoulWardPerk`.
- Descrição técnica (paráfrase): thread de Ars que aumenta capacidade e integridade do Soul Ward mantido por Malum.
- Ativação: `ArsNouveauRegistry.registerCompatPerks()` registra esta perk apenas se `ModList.get().isLoaded("malum")`. **Não é spell/cast** nem acrescenta raiz ao catálogo de magias.

## Contrato exato observado no source

| Eixo | Observação | Ponto de código |
|---|---|---|
| Capacidade | `SOUL_WARD_CAPACITY` com `2 * slotValue`, `ADD_VALUE` | `SoulWardPerk.applyAttributeModifiers` |
| Integridade | `SOUL_WARD_INTEGRITY` com `0.5 * slotValue`, `ADD_MULTIPLIED_BASE` | mesmo método |
| Identificador de modifier | `INSTANCE.getRegistryName()` em ambos; o registry name da perk | mesmo método |
| Grupo de slot | o `EquipmentSlotGroup` recebido é passado aos dois modificadores | mesmo método |
| Contexto | recebe `ItemAttributeModifiers`, `ItemStack`, `slotValue`, `equipmentSlotGroup` e devolve uma coleção enriquecida | mesmo método |

**Equações de input da perk**, não valores finais de personagem: `capacity_delta = 2 × slotValue`; `integrity_base_multiplier = 0.5 × slotValue`. O resultado agregado depende dos atributos-base e regras de combinação Malum/Minecraft, que não foram medidos nesta ficha.

**Campos não aplicáveis à perk de atributo:** seleção ativa de alvo, raycast, range, AOE, hitbox, velocidade de projétil, tipo de dano, ticks de cast, duração de projétil e cooldown de magia. A classe não declara esses mecanismos; não assumir valores zero aplicáveis a outros providers.

## Engenharia de integração
- **Owner:** Ars Thread/Perk para o equipamento; Malum para os atributos e Soul Ward; RPG Skill Tree apenas progressão/gates por contrato real; Black Arcana apenas seu runtime mágico.
- **Perk de amplificação futura:** só aplicar um modificador RPG novo após verificar se `slotValue` já está sendo aumentado por Ars; caso contrário, risco de amplificação dupla. Não sobrescrever `SOUL_WARD_CAPACITY`/`SOUL_WARD_INTEGRITY` nem fabricar hook.
- **Causalidade:** um evento de equipamento não é evento de cast nem geração de Mastery. Reequipamento/reload precisam garantir ausência de somas residuais.
- **QA bloqueado:** stacking multisslot, IDs de modifiers em dois atributos, reload, troca de equipamento, exclusão de Malum, resultado em `AttributeInstance` de `ServerPlayer` real, persistência e modpack completo. Sem API de modificação in-place certificada: **⛔ adapter**.

## Proveniência
- [Registry de perks condicionado a Malum — `ArsNouveauRegistry.java#L38-L48`](https://github.com/Alexthw46/Ars-Unity/blob/b25528adf8c0135585cd6d654582efa147e0a227/src/main/java/com/alexthw/ars_hex/ArsNouveauRegistry.java#L38-L48)
- [ID, dois atributos, fórmulas e operações — `SoulWardPerk.java#L14-L36`](https://github.com/Alexthw46/Ars-Unity/blob/b25528adf8c0135585cd6d654582efa147e0a227/src/main/java/com/alexthw/ars_hex/malum/perks/SoulWardPerk.java#L14-L36)
- [Índice local](../PERK-CAUSAL-ENGINEERING-MATRIX-5.0.4b.md)

**Clean-room:** apenas mapeamento factual de contratos observáveis; nenhum código ou asset do provider foi reutilizado.
