# Wind Rune — material Jewelry

- Provider: **SnackPirate's Aeromancy Additions**, `aero_additions` `1.2.8`.
- Identidade: `aero_additions:rune_wind` no registry de materiais Iron's Jewelry.
- Superfície: contrato de material de datapack host; contribuição ao contador estrito de spells: **0**.

**Teto de evidência:** fonte imutável `ae282b32d25ad76ef8d01c637ec05566a767ae4c`; presença do contrato no JAR oficial de publicação `8251034` quando indicada. O JAR publisher tem 753884 bytes, SHA-1 `dee32c9fa84a9b3796e39846608f8f77591ea56f` e SHA-256 `b2dad354467a2cf1a92519ba68c8e2c32807a976d7b235132d625b7f0f90eea8`. Isso não comprova igualdade com o JAR instalado: o checksum histórico instalado tem 35 caracteres inválidos e permanece **`NOT_VERIFIED`**. [Contrato comum](../SOURCE-CONTRACTS-1.2.8.md) · [fechamento](../SOURCE-CATALOG-CLOSURE-1.2.8.md).

## Material e operação

Recurso publicado **`data/aero_additions/irons_jewelry/material/rune_wind.json`** declara descrição **`material.aero_additions.rune_wind`**, ingrediente **`aero_additions:wind_rune`**, palette **`aero_additions:palettes/rune_wind`**, **quality 1.5**, e bonusParameters **`irons_jewelry:attribute`**: atributo **`aero_additions:wind_spell_power`**, amount **0.05**, operação **`add_multiplied_total`**. A palette PNG existe em assets do publisher; ela é apresentação de material, não outro item registrado.

`data/irons_spellbooks/tags/irons_jewelry/material/rune.json` (`replace=false`) acrescenta **`aero_additions:rune_wind`** à tag de material **`irons_spellbooks:rune`**, consumida no contexto do registry de materiais Jewelry. É distinta da tag de item `irons_spellbooks:inscribed_rune` e do item Wind Rune.

Para um modificador simples desse bônus, a operação total multiplica o valor do atributo após adições/base por **1.05**. O **quality=1.5 não prova automaticamente +7.5% Wind**: a transformação de qualidade, contagem de materiais, slots, crafting e limites de jewelry pertence ao consumer Iron's Jewelry e não foi fechada por esta fonte Aero. O build declara runtimeOnly **Iron's Jewelry 1.21.1-2.0.0**, e não implementação Java provider própria do material. Não inventar receita de anel ou item `aero_additions:affinity_ring_wind` a partir dessa paleta/modelo.

**Localizadores:** [rune_wind.json](https://github.com/snackerpirater/aero-additions/blob/ae282b32d25ad76ef8d01c637ec05566a767ae4c/src/main/resources/data/aero_additions/irons_jewelry/material/rune_wind.json#L1-L15) · [rune.json](https://github.com/snackerpirater/aero-additions/blob/ae282b32d25ad76ef8d01c637ec05566a767ae4c/src/main/resources/data/irons_spellbooks/tags/irons_jewelry/material/rune.json#L1-L6) · [AALang.java](https://github.com/snackerpirater/aero-additions/blob/ae282b32d25ad76ef8d01c637ec05566a767ae4c/src/main/java/com/snackpirate/aeromancy/data/AALang.java#L49-L51) · [build.gradle](https://github.com/snackerpirater/aero-additions/blob/ae282b32d25ad76ef8d01c637ec05566a767ae4c/build.gradle#L175-L181). [Wind Rune item](../items/wind-rune.md) · [assets sem registro](unregistered-item-helpers.md).

**Consumo e QA:** Black Arcana/RPG pode catalogar esta superfície; mudanças de perks precisam de consumidor real e validação causal. Hook/adaptação **`NOT_VERIFIED`**; execução cliente/servidor, configuração efetiva e composição no modpack **`NOT_TESTED`**; **0 certificados**. Valores descritos são contratos de fonte/dados publicados, sem homologação de gameplay.
