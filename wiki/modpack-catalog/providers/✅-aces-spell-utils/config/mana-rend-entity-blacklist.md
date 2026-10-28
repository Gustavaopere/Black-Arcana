# Mana Rend entity blacklist — config comum de Ace's Spell Utils 1.2.7.2

**TOML key exata:** `Mana Rend entity blacklist` · **field runtime:** `AcesSpellUtilsConfig.manaRendWhitelist` · **default:** `true` · **config type:** `COMMON` · **Estado:** ⚠️ source-pinned.

## Registro, carregamento e efeito

- [`AcesSpellUtilsConfig.java`](https://github.com/AceTheEldritchKing/Aces_Spell_Utils/blob/a0b2f4c2fcfa938c8e47239279c77c2ef82647ac/src/main/java/net/acetheeldritchking/aces_spell_utils/utils/AcesSpellUtilsConfig.java) usa `ModConfigSpec.Builder.define` (bool ou double), cria `SPEC` e atualiza field a partir de `ModConfigEvent` no método `onLoad`.
- [`AcesSpellUtils.java`](https://github.com/AceTheEldritchKing/Aces_Spell_Utils/blob/a0b2f4c2fcfa938c8e47239279c77c2ef82647ac/src/main/java/net/acetheeldritchking/aces_spell_utils/AcesSpellUtils.java) registra configuração `COMMON` em arquivo `aces_spell_utils-common.toml`.
- **Consumidor:** `manaRendEvent(LivingIncomingDamageEvent)`. **Semântica:** Apesar do nome TOML **blacklist**, o handler faz o inverso de uma lista proibitiva: quando `true`, exige que a `directEntity` pertença a `ASTags.MANA_REND_WHITELIST` **ou** seja a própria entidade atacante. Quando `false`, a restrição de tag é pulada.
- **Pontos críticos:** Preservar divergência de naming, não inverter interpretação; a tag de entidade inclui magic_missile/firebolt/icicle no datapack source.

## API, escopo e QA

É uma **opção de configuração**, não feitiço nem registry de atributo. Não possui mana, cooldown, range, área, duração, projetil nem efeito autônomo. Outros handlers/entidades podem definir os recursos reais. Não criar mirror de lógica ou pipeline de mana/cast no Black Arcana.

Fonte `AceTheEldritchKing/Aces_Spell_Utils@a0b2f4c2fcfa938c8e47239279c77c2ef82647ac`; JAR anotado `aces_spell_utils-1.2.7.2-1.21.1.jar`, SHA-1 `8cbcd535a0b19bef49504c0b5ecafcbcd1cb1cca` não inspecionado; Iron's source dependency 3.16.2 versus pack 3.16.3. Config atual e side/lifecycle no modpack devem ser medidos. `physical_qa=NOT_TESTED`, `mutating_hook=NOT_VERIFIED`, `COMPLETE_PERK_READY=false`.
