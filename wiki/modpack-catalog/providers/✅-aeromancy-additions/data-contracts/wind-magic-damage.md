# Wind Magic — DamageType

- Provider: **SnackPirate's Aeromancy Additions**, `aero_additions` `1.2.8`.
- Identidade: `aero_additions:wind_magic`.
- Superfície: ResourceKey/registro de datapack `minecraft:damage_type`; contribuição ao contador estrito de spells: **0**.

**Teto de evidência:** fonte imutável `ae282b32d25ad76ef8d01c637ec05566a767ae4c`; presença do contrato no JAR oficial de publicação `8251034` quando indicada. O JAR publisher tem 753884 bytes, SHA-1 `dee32c9fa84a9b3796e39846608f8f77591ea56f` e SHA-256 `b2dad354467a2cf1a92519ba68c8e2c32807a976d7b235132d625b7f0f90eea8`. Isso não comprova igualdade com o JAR instalado: o checksum histórico instalado tem 35 caracteres inválidos e permanece **`NOT_VERIFIED`**. [Contrato comum](../SOURCE-CONTRACTS-1.2.8.md) · [fechamento](../SOURCE-CATALOG-CLOSURE-1.2.8.md).

## Tipo publicado

`AADamageTypes.register` cria ResourceKey no registry **`Registries.DAMAGE_TYPE`**. Bootstrap define `DamageType(messageId="wind_magic", scaling=WHEN_CAUSED_BY_LIVING_NON_PLAYER, exhaustion=0.0)`. O JSON gerado **`data/aero_additions/damage_type/wind_magic.json`** está no publisher com `message_id=wind_magic`, `scaling=when_caused_by_living_non_player`, `exhaustion=0.0`. Bootstrap é datagen, enquanto o JSON é dado carregável em runtime; nenhum DeferredRegister Java independente de DamageType é necessário para inferir outra identidade.

A escola **`aero_additions:wind`** usa este key como seu DamageType. **Exhaustion 0** é parâmetro de dano, não custo de mana. Scaling determina a categoria de escalonamento por dificuldade, não fórmula de spell power. Os cinco tags especiais de dano fornecidos pelo Aero (`bypasses_armor`, `bypasses_shield`, `bypasses_wolf_armor`, `no_impact`, `no_knockback`) listam **somente `asphyxiation`**; não inferir os mesmos bypasses para `wind_magic`.

## Caminhos consumidores

Wind Blade cria DamageSource pelo spell e chama `DamageSources.applyDamage`: esta é a fronteira concreta de Wind school/atribuição de owner. No host 3.16.3, o ramo SpellDamageSource passa por SpellDamageEvent, resistência e hurt aceito; [resistência Wind](../attributes/wind-magic-resist.md). MagicWindCharge usa hit direto **vanilla `damageSources().windCharge(this,owner)`** de **1.0**, e Breathless usa **`asphyxiation`**. Não trocar os DamageTypes com base no nome Wind nem contabilizar dano de movimento/deflexão como um hit `wind_magic` sem evidência.

Não há tradução provider específica `death.attack.wind_magic` em AALang; texto de tooltip ou de morte `wind_blade` não altera o `message_id` do DamageType. Fallback de tradução do ambiente não foi testado.

**Localizadores:** [AADamageTypes.java](https://github.com/snackerpirater/aero-additions/blob/ae282b32d25ad76ef8d01c637ec05566a767ae4c/src/main/java/com/snackpirate/aeromancy/data/AADamageTypes.java#L10-L20) · [AAData.java](https://github.com/snackerpirater/aero-additions/blob/ae282b32d25ad76ef8d01c637ec05566a767ae4c/src/main/java/com/snackpirate/aeromancy/data/AAData.java#L24-L29) · [wind_magic.json](https://github.com/snackerpirater/aero-additions/blob/ae282b32d25ad76ef8d01c637ec05566a767ae4c/src/generated/resources/data/aero_additions/damage_type/wind_magic.json#L1-L5) · [AASpells.java](https://github.com/snackerpirater/aero-additions/blob/ae282b32d25ad76ef8d01c637ec05566a767ae4c/src/main/java/com/snackpirate/aeromancy/spells/AASpells.java#L121-L129) · [WindBladeProjectile.java](https://github.com/snackerpirater/aero-additions/blob/ae282b32d25ad76ef8d01c637ec05566a767ae4c/src/main/java/com/snackpirate/aeromancy/spells/wind_blade/WindBladeProjectile.java#L74-L80) · [MagicWindCharge.java](https://github.com/snackerpirater/aero-additions/blob/ae282b32d25ad76ef8d01c637ec05566a767ae4c/src/main/java/com/snackpirate/aeromancy/spells/wind_charge/MagicWindCharge.java#L96-L110) · [AALang.java](https://github.com/snackerpirater/aero-additions/blob/ae282b32d25ad76ef8d01c637ec05566a767ae4c/src/main/java/com/snackpirate/aeromancy/data/AALang.java#L45-L59).

**Consumo e QA:** Black Arcana/RPG pode catalogar esta superfície; mudanças de perks precisam de consumidor real e validação causal. Hook/adaptação **`NOT_VERIFIED`**; execução cliente/servidor, configuração efetiva e composição no modpack **`NOT_TESTED`**; **0 certificados**. Valores descritos são contratos de fonte/dados publicados, sem homologação de gameplay.
