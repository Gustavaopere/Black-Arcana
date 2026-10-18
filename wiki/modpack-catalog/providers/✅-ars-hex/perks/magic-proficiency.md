# Magic Proficiency — ficha técnica para perks | Ars Hex 5.0.4b

**Tipo de evidência:** `SOURCE_CAUSALITY`, fonte exata de revisão alinhada à release 5.0.4b; **não** há prova de equivalência integral de bytecode com o JAR instalado nem QA de equip/unequip em jogador real. JAR físico `ars_hex-1.21.1-5.0.4b.jar`, SHA-1 documentado `2354710ea312e2a6e0fbc3eb2dbafb8e06f10cf4`. Minecraft 1.21.1, NeoForge; Malum presente na modlist.

## Prova binária adicional — 17/10/2026

✅ [JAR publisher SHA-1 exato, auditoria Java21 #39087382649](../EXACT-PUBLISHER-PERK-SCYTHE-REFERENCES-5.0.4b.md): método `applyAttributeModifiers` referência `MAGIC_PROFICIENCY`, `ADD_MULTIPLIED_BASE`, `withModifierAdded`; **0,1 × slotValue** permanece fórmula da fonte, sem fluxo de operandos ou consumidores de dano comprovados. ⚠️ Player equipado e efeitos finais não testados / ⛔ adapter.

## Identidade e propósito
- ID source: `ars_hex:thread_magic_proficiency`; classe compilável no source `MagicProficencyPerk` (**grafia efetiva**, sem corrigir artificialmente).
- Descrição técnica (paráfrase): thread que aumenta o atributo de proficiência mágica do Lodestone; quais tipos de ataque são afetados e em que magnitude final depende do provider.
- `ArsNouveauRegistry.registerCompatPerks()` o registra somente se Malum estiver carregado, apesar de o atributo projetado pertencer a Lodestone. Isto **não** comprova execução sem Lodestone.

## Contrato exato observado no source

| Eixo | Observação |
|---|---|
| Atributo | `LodestoneAttributes.MAGIC_PROFICIENCY` |
| Quantidade | `0.1 * slotValue` |
| Operação | `AttributeModifier.Operation.ADD_MULTIPLIED_BASE` |
| Modifier ID | `INSTANCE.getRegistryName()`, derivado do ID da perk |
| Equipamento | `equipmentSlotGroup` recebido é retransmitido a `withModifierAdded` |
| Técnica | override `applyAttributeModifiers(ItemAttributeModifiers, ItemStack, int, EquipmentSlotGroup)` |
| Não aplicáveis | range, AOE, targeting ativo, dano direto, projétil, cast time, cooldown, ticking ofensivo |

**Equação de entrada:** `proficiency_base_multiplier = 0.1 × slotValue`. Não interpretar `0.1` como aumento final fixo de 10% sobre todos os danos mágicos: seria necessário observar os consumidores de `MAGIC_PROFICIENCY` e as outras fontes de modifiers.

## Engenharia de integração
- A perk não declara um evento de dano; portanto nenhum `SpellDamageEvent` ou alteração de `DamageType` é garantido aqui.
- Evitar somar proficiência em um segundo pipeline Black Arcana ou atribuir Mastery com base em `applyAttributeModifiers`: é preparação de atributo, não cast bem-sucedido.
- RPG Skill Tree pode usar atribuição/gate *somente* se um boundary real vincular o estado do thread ao jogador sem duplicar a autoridade Ars.
- **⚠️** Validar combinação multisslot, remoção/reload do equipment modifier, lookup exato do atributo em Lodestone 1.8.2, `AttributeInstance` no servidor e configuração efetiva; **⛔** perk adapter/Mastery não homologados.

## Proveniência
- [Registro condicionado — `ArsNouveauRegistry.java#L43-L48`](https://github.com/Alexthw46/Ars-Unity/blob/b25528adf8c0135585cd6d654582efa147e0a227/src/main/java/com/alexthw/ars_hex/ArsNouveauRegistry.java#L43-L48)
- [ID e modificador real — `MagicProficencyPerk.java#L14-L34`](https://github.com/Alexthw46/Ars-Unity/blob/b25528adf8c0135585cd6d654582efa147e0a227/src/main/java/com/alexthw/ars_hex/malum/perks/MagicProficencyPerk.java#L14-L34)
- [Índice local](../PERK-CAUSAL-ENGINEERING-MATRIX-5.0.4b.md)

**Clean-room:** somente fatos de registry, atributo e operação observáveis.
