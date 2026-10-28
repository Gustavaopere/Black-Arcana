# hydro_magic — DamageType de Ace's Spell Utils 1.2.7.2

**Key:** `aces_spell_utils:hydro_magic` · **Registry:** `minecraft:damage_type` · **SchoolType associada:** `aces_spell_utils:hydro` · **Status:** ⚠️ source/pacote de dados pinados.

## Contrato exato

- [`ASDamageTypes.java`](https://github.com/AceTheEldritchKing/Aces_Spell_Utils/blob/a0b2f4c2fcfa938c8e47239279c77c2ef82647ac/src/main/java/net/acetheeldritchking/aces_spell_utils/registries/ASDamageTypes.java): `ResourceKey<DamageType>` criado por `ResourceKey.create(Registries.DAMAGE_TYPE, ...)`; não há `DeferredRegister<DamageType>` nesta classe.
- [`data/aces_spell_utils/damage_type/hydro_magic.json`](https://github.com/AceTheEldritchKing/Aces_Spell_Utils/blob/a0b2f4c2fcfa938c8e47239279c77c2ef82647ac/src/main/resources/data/aces_spell_utils/damage_type/hydro_magic.json): `exhaustion=0.0`, `message_id="hydro_magic"`, `scaling="when_caused_by_living_non_player"`.
- [`data/aces_spell_utils/tags/damage_type/hydro_magic.json`](https://github.com/AceTheEldritchKing/Aces_Spell_Utils/blob/a0b2f4c2fcfa938c8e47239279c77c2ef82647ac/src/main/resources/data/aces_spell_utils/tags/damage_type/hydro_magic.json): tag inclui apenas `aces_spell_utils:hydro_magic` na fonte; datapacks externos podem mudar resultados.
- [`ASSchoolRegistry.java`](https://github.com/AceTheEldritchKing/Aces_Spell_Utils/blob/a0b2f4c2fcfa938c8e47239279c77c2ef82647ac/src/main/java/net/acetheeldritchking/aces_spell_utils/registries/ASSchoolRegistry.java): a escola inclui `ASDamageTypes.HYDRO_MAGIC`.
- **Target/dano numérico, alcance/AoE, projétil, mana, cooldown, duração:** um DamageType fornece identidade e metadados de dano, não causa dano por si. Valores reais exigem spell/entity/consumer concreto de outro provider.

## Boundary e aceitação

Não introduzir outro registro de damage, não aplicar dano adicional ou conceder Mastery ao observar a key. O Black Arcana não delega seu runtime nem altera `WorldEffectPolicy` por mera existência deste DamageType. Fonte pinada `AceTheEldritchKing/Aces_Spell_Utils@a0b2f4c2fcfa938c8e47239279c77c2ef82647ac`; JAR instalado registrado `aces_spell_utils-1.2.7.2-1.21.1.jar` SHA-1 `8cbcd535a0b19bef49504c0b5ecafcbcd1cb1cca` (não confrontado); Iron's source build `3.16.2` vs pack `3.16.3`. `physical_qa=NOT_TESTED`, `mutating_hook=NOT_VERIFIED`, `COMPLETE_PERK_READY=false`.
