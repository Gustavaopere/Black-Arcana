# Mana Steal drains mana — config comum de Ace's Spell Utils 1.2.7.2

**TOML key exata:** `Mana Steal drains mana` · **field runtime:** `AcesSpellUtilsConfig.manaStealDrain` · **default:** `true` · **config type:** `COMMON` · **Estado:** ⚠️ source-pinned.

## Registro, carregamento e efeito

- [`AcesSpellUtilsConfig.java`](https://github.com/AceTheEldritchKing/Aces_Spell_Utils/blob/a0b2f4c2fcfa938c8e47239279c77c2ef82647ac/src/main/java/net/acetheeldritchking/aces_spell_utils/utils/AcesSpellUtilsConfig.java) usa `ModConfigSpec.Builder.define` (bool ou double), cria `SPEC` e atualiza field a partir de `ModConfigEvent` no método `onLoad`.
- [`AcesSpellUtils.java`](https://github.com/AceTheEldritchKing/Aces_Spell_Utils/blob/a0b2f4c2fcfa938c8e47239279c77c2ef82647ac/src/main/java/net/acetheeldritchking/aces_spell_utils/AcesSpellUtils.java) registra configuração `COMMON` em arquivo `aces_spell_utils-common.toml`.
- **Consumidor:** `manaStealEvent(LivingDamageEvent.Post)`. **Semântica:** Quando o alvo é `ServerPlayer`, `true` escolhe o ramo de transferência de mana da vítima para o atacante; `false` escolhe crédito de mana ao atacante até seu máximo sem débito da vítima. Também depende de quem causou dano e do filtro de entidade direta.
- **Pontos críticos:** Não é percent, manaCost ou spell cooldown. A fórmula da quantidade é `int(manaStealAttr * originalDamage)` em outra rotina. O source envia o sync da `victimMagicData` ao atacante no ramo de drenagem; validar HUD de ambos os players.

## API, escopo e QA

É uma **opção de configuração**, não feitiço nem registry de atributo. Não possui mana, cooldown, range, área, duração, projetil nem efeito autônomo. Outros handlers/entidades podem definir os recursos reais. Não criar mirror de lógica ou pipeline de mana/cast no Black Arcana.

Fonte `AceTheEldritchKing/Aces_Spell_Utils@a0b2f4c2fcfa938c8e47239279c77c2ef82647ac`; JAR anotado `aces_spell_utils-1.2.7.2-1.21.1.jar`, SHA-1 `8cbcd535a0b19bef49504c0b5ecafcbcd1cb1cca` não inspecionado; Iron's source dependency 3.16.2 versus pack 3.16.3. Config atual e side/lifecycle no modpack devem ser medidos. `physical_qa=NOT_TESTED`, `mutating_hook=NOT_VERIFIED`, `COMPLETE_PERK_READY=false`.
