# Refinement victory factor — config comum de Ace's Spell Utils 1.2.7.2

**TOML key exata:** `Refinement victory factor` · **field runtime:** `AcesSpellUtilsConfig.refinementDifference` · **default:** `1.5` · **config type:** `COMMON` · **Estado:** ⚠️ source-pinned.

## Registro, carregamento e efeito

- [`AcesSpellUtilsConfig.java`](https://github.com/AceTheEldritchKing/Aces_Spell_Utils/blob/a0b2f4c2fcfa938c8e47239279c77c2ef82647ac/src/main/java/net/acetheeldritchking/aces_spell_utils/utils/AcesSpellUtilsConfig.java) usa `ModConfigSpec.Builder.define` (bool ou double), cria `SPEC` e atualiza field a partir de `ModConfigEvent` no método `onLoad`.
- [`AcesSpellUtils.java`](https://github.com/AceTheEldritchKing/Aces_Spell_Utils/blob/a0b2f4c2fcfa938c8e47239279c77c2ef82647ac/src/main/java/net/acetheeldritchking/aces_spell_utils/AcesSpellUtils.java) registra configuração `COMMON` em arquivo `aces_spell_utils-common.toml`.
- **Consumidor:** `AbstractDomainEntity.onActivation()`. **Semântica:** Em colisões de domain, compara razões `otherRefinement/thisRefinement` e inverso com o fator definido para resolver vitória automática. Se nenhuma ultrapassa o limiar, os domains entram em clash.
- **Pontos críticos:** O comentário exige razão >1, mas a declaração usa `BUILDER.define(..., 1.5D)` sem validação numérica explícita nessa classe. Não afirmar validação dura nem dividir por zero com segurança; adicionar ticket de chunk e world-safety QA.

## API, escopo e QA

É uma **opção de configuração**, não feitiço nem registry de atributo. Não possui mana, cooldown, range, área, duração, projetil nem efeito autônomo. Outros handlers/entidades podem definir os recursos reais. Não criar mirror de lógica ou pipeline de mana/cast no Black Arcana.

Fonte `AceTheEldritchKing/Aces_Spell_Utils@a0b2f4c2fcfa938c8e47239279c77c2ef82647ac`; JAR anotado `aces_spell_utils-1.2.7.2-1.21.1.jar`, SHA-1 `8cbcd535a0b19bef49504c0b5ecafcbcd1cb1cca` não inspecionado; Iron's source dependency 3.16.2 versus pack 3.16.3. Config atual e side/lifecycle no modpack devem ser medidos. `physical_qa=NOT_TESTED`, `mutating_hook=NOT_VERIFIED`, `COMPLETE_PERK_READY=false`.
