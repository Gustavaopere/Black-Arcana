# Wind Spell Power

- Provider: **SnackPirate's Aeromancy Additions**, `aero_additions` `1.2.8`.
- Identidade: `aero_additions:wind_spell_power`.
- Superfície: atributo registrado (`MagicRangedAttribute`); contribuição ao contador estrito de spells: **0**.

**Teto de evidência:** fonte imutável `ae282b32d25ad76ef8d01c637ec05566a767ae4c`; presença do contrato no JAR oficial de publicação `8251034` quando indicada. O JAR publisher tem 753884 bytes, SHA-1 `dee32c9fa84a9b3796e39846608f8f77591ea56f` e SHA-256 `b2dad354467a2cf1a92519ba68c8e2c32807a976d7b235132d625b7f0f90eea8`. Isso não comprova igualdade com o JAR instalado: o checksum histórico instalado tem 35 caracteres inválidos e permanece **`NOT_VERIFIED`**. [Contrato comum](../SOURCE-CONTRACTS-1.2.8.md) · [fechamento](../SOURCE-CATALOG-CLOSURE-1.2.8.md).

## Registro e valor

Registro em **`Registries.ATTRIBUTE`**, via `AASpells.Attributes`, adicionado ao event bus por `AASpells.register`. Descrição **`attribute.aero_additions.wind_spell_power`**, default **1.0**, intervalo declarado **[−100, 100]**, **syncable=true**. `AAServerEvents.addAttributes` adiciona o atributo ao tipo **PLAYER**. Isso não prova que qualquer mob tenha o atributo, e o intervalo não é promessa de comportamento estável para valores extremos.

A escola Wind usa este holder como atributo de potência. No host 3.16.3 pin `e4056af90302d37eb1739f5ff05020b020e6e252`, `SchoolType.getPowerFor` retorna o valor raw se presente, ou 1 se ausente; `AbstractSpell.getSpellPower` calcula **`(basePower + powerPerLevel×(L−1)) × SpellPower × WindSpellPower × configPowerMultiplier`**. Modificadores Wind de gear não são aplicados de novo pelo RPG; tampouco implicam que todos os métodos provider consumam o resultado.

## Consumidores e operações conhecidas

| Origem provider | Quantidade | Operação | Aplicação declarada |
|---|---:|---|---|
| Air Staff | +0.15 | `ADD_MULTIPLIED_BASE` | MAINHAND |
| Updraft Tome | +0.10 | `ADD_MULTIPLIED_BASE` | atributo de spellbook, resolvido pelo host |
| Tempest Blade | +0.10 | `ADD_MULTIPLIED_BASE` | MAINHAND |
| Tipo Wind Upgrade Orb | +0.05 | `ADD_MULTIPLIED_BASE` | aplicação de upgrade delegada ao host |
| Material Jewelry `aero_additions:rune_wind` | +0.05 | **`ADD_MULTIPLIED_TOTAL`** | bônus de material, delegado a Jewelry |
| Cada peça Windmaker | +0.10 no host 3.16.3 inspecionado | `ADD_MULTIPLIED_BASE` | slot de armadura correspondente |

Para base Wind `B`, adições de valor `A`, soma de modificadores base `M` e modificadores totais `tᵢ`, o modelo de atributos é **`((B+A) + (B+A)×M) × ∏(1+tᵢ)`**, sujeito ao clamp do atributo. Assim, base 1 com Staff dá **1.15**; adicionar bônus Jewelry +0.05 total dá **1.15×1.05=1.2075**, enquanto um orb +0.05 base, se validamente aplicado pelo host, daria **1.20** antes de totais. Operações são diferentes; não somar Jewelry como base. Limites de upgrade/qualidade Jewelry não vêm desta fórmula.

A contribuição de cada peça Windmaker acima deriva separadamente do host **3.16.3**; Aero foi construído contra **3.16.1**. Valores compostos e aplicação efetiva ficam `NOT_VERIFIED`, sem adapter homologado.

**Localizadores provider:** [AASpells.java](https://github.com/snackerpirater/aero-additions/blob/ae282b32d25ad76ef8d01c637ec05566a767ae4c/src/main/java/com/snackpirate/aeromancy/spells/AASpells.java#L136-L147) · [AASpells.java](https://github.com/snackerpirater/aero-additions/blob/ae282b32d25ad76ef8d01c637ec05566a767ae4c/src/main/java/com/snackpirate/aeromancy/spells/AASpells.java#L121-L129) · [AAServerEvents.java](https://github.com/snackerpirater/aero-additions/blob/ae282b32d25ad76ef8d01c637ec05566a767ae4c/src/main/java/com/snackpirate/aeromancy/AAServerEvents.java#L54-L60) · [AAItems.java](https://github.com/snackerpirater/aero-additions/blob/ae282b32d25ad76ef8d01c637ec05566a767ae4c/src/main/java/com/snackpirate/aeromancy/item/AAItems.java#L29-L67) · [WindmakerRobeItem.java](https://github.com/snackerpirater/aero-additions/blob/ae282b32d25ad76ef8d01c637ec05566a767ae4c/src/main/java/com/snackpirate/aeromancy/item/WindmakerRobeItem.java#L17-L23) · [AAUpgradeOrbs.java](https://github.com/snackerpirater/aero-additions/blob/ae282b32d25ad76ef8d01c637ec05566a767ae4c/src/main/java/com/snackpirate/aeromancy/data/AAUpgradeOrbs.java#L12-L19) · [rune_wind.json](https://github.com/snackerpirater/aero-additions/blob/ae282b32d25ad76ef8d01c637ec05566a767ae4c/src/main/resources/data/aero_additions/irons_jewelry/material/rune_wind.json#L1-L15).

**Localizadores host distintos:** [SchoolType.java — Iron's 3.16.3](https://github.com/iron431/irons-spells-n-spellbooks/blob/e4056af90302d37eb1739f5ff05020b020e6e252/src/main/java/io/redspace/ironsspellbooks/api/spells/SchoolType.java#L54-L59) · [AbstractSpell.java — Iron's 3.16.3](https://github.com/iron431/irons-spells-n-spellbooks/blob/e4056af90302d37eb1739f5ff05020b020e6e252/src/main/java/io/redspace/ironsspellbooks/api/spells/AbstractSpell.java#L211-L225) · [ExtendedArmorItem.java — Iron's 3.16.3](https://github.com/iron431/irons-spells-n-spellbooks/blob/e4056af90302d37eb1739f5ff05020b020e6e252/src/main/java/io/redspace/ironsspellbooks/item/armor/ExtendedArmorItem.java#L61-L70).

**Consumo e QA:** Black Arcana/RPG pode catalogar esta superfície; mudanças de perks precisam de consumidor real e validação causal. Hook/adaptação **`NOT_VERIFIED`**; execução cliente/servidor, configuração efetiva e composição no modpack **`NOT_TESTED`**; **0 certificados**. Valores descritos são contratos de fonte/dados publicados, sem homologação de gameplay.
