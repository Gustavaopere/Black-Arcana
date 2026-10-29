# Sound events e recursos de áudio

- Provider: **SnackPirate's Aeromancy Additions**, `aero_additions` `1.2.8`.
- Identidade: 4 SoundEvents registrados; 5 keys em sounds.json.
- Superfície: registros de som e apresentação publicada; contribuição ao contador estrito de spells: **0**.

**Teto de evidência:** fonte imutável `ae282b32d25ad76ef8d01c637ec05566a767ae4c`; presença do contrato no JAR oficial de publicação `8251034` quando indicada. O JAR publisher tem 753884 bytes, SHA-1 `dee32c9fa84a9b3796e39846608f8f77591ea56f` e SHA-256 `b2dad354467a2cf1a92519ba68c8e2c32807a976d7b235132d625b7f0f90eea8`. Isso não comprova igualdade com o JAR instalado: o checksum histórico instalado tem 35 caracteres inválidos e permanece **`NOT_VERIFIED`**. [Contrato comum](../SOURCE-CONTRACTS-1.2.8.md) · [fechamento](../SOURCE-CATALOG-CLOSURE-1.2.8.md).

## Quatro registros ativos

`AASounds` possui `DeferredRegister<SoundEvent>` em `Registries.SOUND_EVENT`, ligado ao mod event bus por `Aeromancy`. Cada registro usa **`SoundEvent.createVariableRangeEvent`**; Aero não declara alcance fixo numérico aqui.

| SoundEvent registrado | Arquivo listado no sounds.json | Consumidor conhecido |
|---|---|---|
| `aero_additions:cast.generic.wind` | `generic/wind_cast.ogg` | som padrão da escola Wind |
| `aero_additions:cast.generic.airblast` | `generic/airblast_woosh.ogg` | finish sound Airblast |
| `aero_additions:cast.generic.thunderclap` | `generic/thunderclap_cast.ogg` | referência no spell Thunderclap, cujo registro de spell está comentado |
| `aero_additions:cast.generic.wind_reversed` | `generic/wind_cast_reversed.ogg` | start sounds em classes Tornado/Thunderclap, sem spell ativo registrado |

Os quatro registros existem independentemente de consumidores experimentais. Som Thunderclap registrado não reativa ThunderclapSpell.

## Quinto recurso sem registro correspondente

`sounds.json` ainda declara key **`cast.generic.airblast_success`** → **`aero_additions:generic/airblast_redirect_success`** e o `.ogg` correspondente está no publisher. **Não há quinto registerSoundEvent em AASounds.** A chamada `entity.playSound(AASounds.AIRBLAST_REDIRECT...)` está comentada em AirblastSpell, e não existe holder `AIRBLAST_REDIRECT` ativo nessa classe de registro. Portanto é recurso de áudio presente, sem SoundEvent provider correspondente demonstrado; não inventar ID ativo pela key de assets.

Os cinco `.ogg` e `sounds.json` são recursos publicados. Volume/pitch/atenuação efetivos são de cada chamada/engine; nenhum hook de perk validado permite tratar som como sucesso de cast ou dano. Updraft/Wind Shield/Asphyxiate e outros callbacks também podem usar sons vanilla/host sem que AASounds os registre.

**Localizadores:** [AASounds.java](https://github.com/snackerpirater/aero-additions/blob/ae282b32d25ad76ef8d01c637ec05566a767ae4c/src/main/java/com/snackpirate/aeromancy/AASounds.java#L10-L26) · [Aeromancy.java](https://github.com/snackerpirater/aero-additions/blob/ae282b32d25ad76ef8d01c637ec05566a767ae4c/src/main/java/com/snackpirate/aeromancy/Aeromancy.java#L34-L40) · [sounds.json](https://github.com/snackerpirater/aero-additions/blob/ae282b32d25ad76ef8d01c637ec05566a767ae4c/src/main/resources/assets/aero_additions/sounds.json#L1-L29) · [AASpells.java](https://github.com/snackerpirater/aero-additions/blob/ae282b32d25ad76ef8d01c637ec05566a767ae4c/src/main/java/com/snackpirate/aeromancy/spells/AASpells.java#L121-L129) · [AirblastSpell.java](https://github.com/snackerpirater/aero-additions/blob/ae282b32d25ad76ef8d01c637ec05566a767ae4c/src/main/java/com/snackpirate/aeromancy/spells/airblast/AirblastSpell.java#L84-L89) · [AirblastSpell.java](https://github.com/snackerpirater/aero-additions/blob/ae282b32d25ad76ef8d01c637ec05566a767ae4c/src/main/java/com/snackpirate/aeromancy/spells/airblast/AirblastSpell.java#L113-L118) · [ThunderclapSpell.java](https://github.com/snackerpirater/aero-additions/blob/ae282b32d25ad76ef8d01c637ec05566a767ae4c/src/main/java/com/snackpirate/aeromancy/spells/thunderclap/ThunderclapSpell.java#L46-L64) · [TornadoSpell.java](https://github.com/snackerpirater/aero-additions/blob/ae282b32d25ad76ef8d01c637ec05566a767ae4c/src/main/java/com/snackpirate/aeromancy/spells/tornado/TornadoSpell.java#L69-L72).

**Consumo e QA:** Black Arcana/RPG pode catalogar esta superfície; mudanças de perks precisam de consumidor real e validação causal. Hook/adaptação **`NOT_VERIFIED`**; execução cliente/servidor, configuração efetiva e composição no modpack **`NOT_TESTED`**; **0 certificados**. Valores descritos são contratos de fonte/dados publicados, sem homologação de gameplay.
