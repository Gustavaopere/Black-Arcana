# technomancy_focus — Ace's Spell Utils 1.2.7.2

**Registry:** `minecraft:item` (tag do tipo item) · **Tag ID exato:** `aces_spell_utils:technomancy_focus` · **Constante Java:** `ASTags.TECHNOMANCY_FOCUS` · **Estado:** ⚠️ source confirmado, membership/runtime condicionado.

## Fonte e contrato

- [`ASTags.java` da revisão pinada](https://github.com/AceTheEldritchKing/Aces_Spell_Utils/blob/a0b2f4c2fcfa938c8e47239279c77c2ef82647ac/src/main/java/net/acetheeldritchking/aces_spell_utils/utils/ASTags.java) — declaração de `TagKey`; `mod_version=1.2.7.2-1.21.1`.
- **Uso/semântica do source:** Foco de escola consumido por `ASSchoolRegistry.TECHNOMANCY`.
- **Valores conhecidos:** Tag de item declarada, membros não demonstrados pelo datapack do provider.
- **Target, range, AoE, projétil, tipo de dano, mana, cooldown e duração:** a tag apenas seleciona membros; não representa spell/cast nem fixa parâmetros de magia.
- **Hook:** consulta de `TagKey` apenas no registry correspondente; não presume consumo, efeito, gate ou implementação no Black Arcana.

## Proveniência, risco e QA

O source público está pinado em `AceTheEldritchKing/Aces_Spell_Utils@a0b2f4c2fcfa938c8e47239279c77c2ef82647ac`. JAR anotado na modlist: `aces_spell_utils-1.2.7.2-1.21.1.jar`, SHA-1 `8cbcd535a0b19bef49504c0b5ecafcbcd1cb1cca`, **sem verificação source→classfile nesta tranche**. O `build.gradle` declara Iron's `3.16.2`, pack informa `3.16.3`. Membership datapack pode mudar com outros mods/pack. **`mutating_hook=NOT_VERIFIED`, `physical_qa=NOT_TESTED`, `COMPLETE_PERK_READY=false`.** Não iniciar casting nem reimplementar transações por leitura de tag.
