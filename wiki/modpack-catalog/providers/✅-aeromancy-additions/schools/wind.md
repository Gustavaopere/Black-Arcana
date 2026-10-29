# Wind — escola

- Provider: **SnackPirate's Aeromancy Additions**, `aero_additions` `1.2.8`.
- Identidade: `aero_additions:wind`.
- Superfície: registro `SchoolType` no registry de escolas Iron's; contribuição ao contador estrito de spells: **0**.

**Teto de evidência:** fonte imutável `ae282b32d25ad76ef8d01c637ec05566a767ae4c`; presença do contrato no JAR oficial de publicação `8251034` quando indicada. O JAR publisher tem 753884 bytes, SHA-1 `dee32c9fa84a9b3796e39846608f8f77591ea56f` e SHA-256 `b2dad354467a2cf1a92519ba68c8e2c32807a976d7b235132d625b7f0f90eea8`. Isso não comprova igualdade com o JAR instalado: o checksum histórico instalado tem 35 caracteres inválidos e permanece **`NOT_VERIFIED`**. [Contrato comum](../SOURCE-CONTRACTS-1.2.8.md) · [fechamento](../SOURCE-CATALOG-CLOSURE-1.2.8.md).

## Registro e vínculos

`AASpells.register` conecta o `DeferredRegister<SchoolType>` ao event bus; o registro da escola usa o path `wind`. A instância tem label `school.aero_additions.wind`, cor **`0xa3b6ff`**, foco **`aero_additions:wind_focus`**, potência **`aero_additions:wind_spell_power`**, resistência **`aero_additions:wind_magic_resist`**, som padrão **`aero_additions:cast.generic.wind`** e DamageType **`aero_additions:wind_magic`**. Esses vínculos são objetos de registries diferentes, sem acrescentar raízes ao total de dez spells.

O construtor provider usa sete argumentos. **No host 3.16.3**, pin `e4056af90302d37eb1739f5ff05020b020e6e252`, isso delega `requiresLearning=false`, `allowLooting=true`; são defaults de host, não prova das configurações efetivas. `SchoolType.getPowerFor` e `getResistanceFor` leem os atributos da entidade se presentes e retornam **1** se ausentes. O provider adiciona ambos ao tipo **PLAYER** em `EntityAttributeModificationEvent`, sem concessão indiscriminada a todos os LivingEntity.

## Foco, alcance semântico e aquisição

Os dados publicados acrescentam **`minecraft:breeze_rod`** tanto a `aero_additions:wind_focus` quanto a `irons_spellbooks:school_focus`. O consumo é do Scroll Forge/host; a tag não desbloqueia por si spells desabilitados, recipes removidos ou dependências ausentes. O JSON publicado `data/irons_spellbooks/irons_spellbooks_spell_config/gust.json` declara **`irons_spellbooks:school = aero_additions:wind`** para Gust do host. Isso é override de datapack sobre magia host e depende do loader host; não cria registro `aero_additions:gust` nem uma 11ª magia Aero.

Dez spells ativos apontam à escola: Wind Charge, Updraft, Airstep, Asphyxiate, Feather Flight (`feather_fall`), Wind Shield, Airblast, Wind Blade, Flush e Dash. Os cinco registros comentados (Tornado, Thunderclap, Summon Breeze, Telelink, Shapeshift) continuam experimentais apesar de referências à escola/classes/assets. [Inventário de spells](../SPELL-CARDS-1.2.8.md).

## Fórmula de potência e fronteira de dano

O host 3.16.3 calcula **`(basePower + powerPerLevel×(L−1)) × SpellPower × WindPower × configPowerMultiplier`**. Isso só altera os métodos de spell que usam tal resultado; escola não transforma automaticamente movimento, raio, duração, mana ou cada hit em potência escalável. Wind Blade usa `DamageSources.applyDamage` e a escola; MagicWindCharge dá hit direto vanilla `windCharge` de 1.0; Breathless usa DamageType `asphyxiation` com `LivingEntity.hurt`, sem o caminho `SpellDamageSource`. Não aplicar resistência Wind ou crédito de magia por nome da escola sem verificar consumidor real.

**Localizadores provider:** [AASpells.java](https://github.com/snackerpirater/aero-additions/blob/ae282b32d25ad76ef8d01c637ec05566a767ae4c/src/main/java/com/snackpirate/aeromancy/spells/AASpells.java#L50-L78) · [AASpells.java](https://github.com/snackerpirater/aero-additions/blob/ae282b32d25ad76ef8d01c637ec05566a767ae4c/src/main/java/com/snackpirate/aeromancy/spells/AASpells.java#L116-L147) · [AAServerEvents.java](https://github.com/snackerpirater/aero-additions/blob/ae282b32d25ad76ef8d01c637ec05566a767ae4c/src/main/java/com/snackpirate/aeromancy/AAServerEvents.java#L54-L60) · [AAItemTags.java](https://github.com/snackerpirater/aero-additions/blob/ae282b32d25ad76ef8d01c637ec05566a767ae4c/src/main/java/com/snackpirate/aeromancy/data/AAItemTags.java#L20-L35) · [gust.json](https://github.com/snackerpirater/aero-additions/blob/ae282b32d25ad76ef8d01c637ec05566a767ae4c/src/main/resources/data/irons_spellbooks/irons_spellbooks_spell_config/gust.json#L1-L3).

**Localizadores host distintos:** [SchoolType.java — Iron's 3.16.3](https://github.com/iron431/irons-spells-n-spellbooks/blob/e4056af90302d37eb1739f5ff05020b020e6e252/src/main/java/io/redspace/ironsspellbooks/api/spells/SchoolType.java#L30-L59) · [AbstractSpell.java — Iron's 3.16.3](https://github.com/iron431/irons-spells-n-spellbooks/blob/e4056af90302d37eb1739f5ff05020b020e6e252/src/main/java/io/redspace/ironsspellbooks/api/spells/AbstractSpell.java#L211-L225). [Wind Magic](../data-contracts/wind-magic-damage.md) · [Asphyxiation](../data-contracts/asphyxiation-damage.md).

**Consumo e QA:** Black Arcana/RPG pode catalogar esta superfície; mudanças de perks precisam de consumidor real e validação causal. Hook/adaptação **`NOT_VERIFIED`**; execução cliente/servidor, configuração efetiva e composição no modpack **`NOT_TESTED`**; **0 certificados**. Valores descritos são contratos de fonte/dados publicados, sem homologação de gameplay.
