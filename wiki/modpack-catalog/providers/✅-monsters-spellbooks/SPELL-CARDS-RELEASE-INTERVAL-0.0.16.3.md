# Monsters & Spellbooks — fichas individuais de 98 spells (fonte contemporânea à release 0.0.16.3)

Status: **✅ 98/98 fichas de registros observados na fonte / `COUNTED_RELEASE_BOUNDED` / ⚠️ IDs e mecânicas do JAR físico ainda sem prova exata**.

## Evidência e política de catalogação

- A modlist documenta `monstersspellbooks-0.0.16.3.jar`, mod ID `monstersspellbooks`, SHA-1 `b3aa89fd081bf4bfaf8d0f4380bcdc393c66ab0e` e release CurseForge File `8788560`.
- A fonte oficial examinada é `RedReaper28/Monsters-Spellbooks-1.21.1@1ab9b72af2ea44c3c8b816e665d06531ea44ddc2`. Seu `ModSpellRegistry` registra **98** campos e classes de magia. O arquivo de registry não mudou no intervalo público de releases 0.0.16.2–0.0.16.3.
- A fonte pública ainda declara `mod_version=0.0.14`. Portanto **NÃO é um build pin exato** do JAR 0.0.16.3. Não converter uma constante Java em `ResourceLocation`, school, custo ou efeito no runtime sem evidência adequada.
- Os **98 registros já estão contabilizados** no ledger como `COUNTED_RELEASE_BOUNDED`. Materializar as fichas acrescenta **+0 novas identidades**, preservando os mínimos **1.851 global / 1.849 no escopo solicitado** e o denominador final aberto.
- As 11 famílias abaixo representam organização da fonte, não 11 `SchoolType` confirmados. `monstersspellbooks:necro` é observado na fonte, sem validação binária de escola por spell. `monstersspellbooks:aero` não pode ser tratado como instalado: zero magias Aero no registry e notas de remoção em 0.0.16.2–0.0.16.3.
- **Autoridade:** Monsters & Spellbooks controla seu conteúdo; Iron's controla casting, mana/cooldown e lifecycle de host. Black Arcana mantém seu próprio runtime, não duplica effects/summons/recursos e exige interface comprovada antes de integração.
- **Proveniência:** licenciamento documental divergente (publisher MIT, metadados da fonte All Rights Reserved); somente dados factuais de identidade/estrutura são reproduzidos, sem copiar código, recursos ou textos criativos.

## Índice e fichas individuais

## Família `blood` — 5 registros

### 01 — `ANTICOAGULATION`

- **Família organizacional na fonte:** `blood`; não comprova `SchoolType` individual.
- **Constante em `ModSpellRegistry`:** `ANTICOAGULATION`.
- **Classe da fonte pública:** `AnticoagulationSpell`.
- **Registry ID físico 0.0.16.3:** `NÃO VERIFICADO`. Não derivar namespace/path de campos ou nomes de classes.
- **Escola e configuração individual:** `NÃO VERIFICADO`; mesmo a escola Necro observada no source não prova a associação deste registro no binário instalado.
- **Custos, cooldown, level/rarity, targeting, efeito, dano/cura, summons, filtros PvP/boss, persistência, aquisição e world safety:** `NÃO VERIFICADO`. Nenhum desses mecanismos é inferido do nome.
- **Identidade semântica:** `COUNTED_RELEASE_BOUNDED`, já inventariada no lote de 98 da fonte contemporânea. O feitiço pertence ao provider, com casting/mana/cooldown hospedados no Iron's. Black Arcana não reproduz o efeito.
- **Fonte factual:** [inventário](SPELL-CATALOG.md), [proveniência](EVIDENCE-AND-PROVENANCE.md), [limites de runtime](RUNTIME-AND-SAFETY.md).

### 02 — `BLOOD_PIERCE`

- **Família organizacional na fonte:** `blood`; não comprova `SchoolType` individual.
- **Constante em `ModSpellRegistry`:** `BLOOD_PIERCE`.
- **Classe da fonte pública:** `BloodPierceSpell`.
- **Registry ID físico 0.0.16.3:** `NÃO VERIFICADO`. Não derivar namespace/path de campos ou nomes de classes.
- **Escola e configuração individual:** `NÃO VERIFICADO`; mesmo a escola Necro observada no source não prova a associação deste registro no binário instalado.
- **Custos, cooldown, level/rarity, targeting, efeito, dano/cura, summons, filtros PvP/boss, persistência, aquisição e world safety:** `NÃO VERIFICADO`. Nenhum desses mecanismos é inferido do nome.
- **Identidade semântica:** `COUNTED_RELEASE_BOUNDED`, já inventariada no lote de 98 da fonte contemporânea. O feitiço pertence ao provider, com casting/mana/cooldown hospedados no Iron's. Black Arcana não reproduz o efeito.
- **Fonte factual:** [inventário](SPELL-CATALOG.md), [proveniência](EVIDENCE-AND-PROVENANCE.md), [limites de runtime](RUNTIME-AND-SAFETY.md).

### 03 — `BLOOD_THORN`

- **Família organizacional na fonte:** `blood`; não comprova `SchoolType` individual.
- **Constante em `ModSpellRegistry`:** `BLOOD_THORN`.
- **Classe da fonte pública:** `BloodThornSpell`.
- **Registry ID físico 0.0.16.3:** `NÃO VERIFICADO`. Não derivar namespace/path de campos ou nomes de classes.
- **Escola e configuração individual:** `NÃO VERIFICADO`; mesmo a escola Necro observada no source não prova a associação deste registro no binário instalado.
- **Custos, cooldown, level/rarity, targeting, efeito, dano/cura, summons, filtros PvP/boss, persistência, aquisição e world safety:** `NÃO VERIFICADO`. Nenhum desses mecanismos é inferido do nome.
- **Identidade semântica:** `COUNTED_RELEASE_BOUNDED`, já inventariada no lote de 98 da fonte contemporânea. O feitiço pertence ao provider, com casting/mana/cooldown hospedados no Iron's. Black Arcana não reproduz o efeito.
- **Fonte factual:** [inventário](SPELL-CATALOG.md), [proveniência](EVIDENCE-AND-PROVENANCE.md), [limites de runtime](RUNTIME-AND-SAFETY.md).

### 04 — `HYSTERIA`

- **Família organizacional na fonte:** `blood`; não comprova `SchoolType` individual.
- **Constante em `ModSpellRegistry`:** `HYSTERIA`.
- **Classe da fonte pública:** `HysteriaSpell`.
- **Registry ID físico 0.0.16.3:** `NÃO VERIFICADO`. Não derivar namespace/path de campos ou nomes de classes.
- **Escola e configuração individual:** `NÃO VERIFICADO`; mesmo a escola Necro observada no source não prova a associação deste registro no binário instalado.
- **Custos, cooldown, level/rarity, targeting, efeito, dano/cura, summons, filtros PvP/boss, persistência, aquisição e world safety:** `NÃO VERIFICADO`. Nenhum desses mecanismos é inferido do nome.
- **Identidade semântica:** `COUNTED_RELEASE_BOUNDED`, já inventariada no lote de 98 da fonte contemporânea. O feitiço pertence ao provider, com casting/mana/cooldown hospedados no Iron's. Black Arcana não reproduz o efeito.
- **Fonte factual:** [inventário](SPELL-CATALOG.md), [proveniência](EVIDENCE-AND-PROVENANCE.md), [limites de runtime](RUNTIME-AND-SAFETY.md).

### 05 — `SANGUINITE_EVISCERATION`

- **Família organizacional na fonte:** `blood`; não comprova `SchoolType` individual.
- **Constante em `ModSpellRegistry`:** `SANGUINITE_EVISCERATION`.
- **Classe da fonte pública:** `SanguiniteEviscerationSpell`.
- **Registry ID físico 0.0.16.3:** `NÃO VERIFICADO`. Não derivar namespace/path de campos ou nomes de classes.
- **Escola e configuração individual:** `NÃO VERIFICADO`; mesmo a escola Necro observada no source não prova a associação deste registro no binário instalado.
- **Custos, cooldown, level/rarity, targeting, efeito, dano/cura, summons, filtros PvP/boss, persistência, aquisição e world safety:** `NÃO VERIFICADO`. Nenhum desses mecanismos é inferido do nome.
- **Identidade semântica:** `COUNTED_RELEASE_BOUNDED`, já inventariada no lote de 98 da fonte contemporânea. O feitiço pertence ao provider, com casting/mana/cooldown hospedados no Iron's. Black Arcana não reproduz o efeito.
- **Fonte factual:** [inventário](SPELL-CATALOG.md), [proveniência](EVIDENCE-AND-PROVENANCE.md), [limites de runtime](RUNTIME-AND-SAFETY.md).


## Família `ender` — 12 registros

### 06 — `CORRUPTED_BEACON_RAY`

- **Família organizacional na fonte:** `ender`; não comprova `SchoolType` individual.
- **Constante em `ModSpellRegistry`:** `CORRUPTED_BEACON_RAY`.
- **Classe da fonte pública:** `CorruptedBeaconRaySpell`.
- **Registry ID físico 0.0.16.3:** `NÃO VERIFICADO`. Não derivar namespace/path de campos ou nomes de classes.
- **Escola e configuração individual:** `NÃO VERIFICADO`; mesmo a escola Necro observada no source não prova a associação deste registro no binário instalado.
- **Custos, cooldown, level/rarity, targeting, efeito, dano/cura, summons, filtros PvP/boss, persistência, aquisição e world safety:** `NÃO VERIFICADO`. Nenhum desses mecanismos é inferido do nome.
- **Identidade semântica:** `COUNTED_RELEASE_BOUNDED`, já inventariada no lote de 98 da fonte contemporânea. O feitiço pertence ao provider, com casting/mana/cooldown hospedados no Iron's. Black Arcana não reproduz o efeito.
- **Fonte factual:** [inventário](SPELL-CATALOG.md), [proveniência](EVIDENCE-AND-PROVENANCE.md), [limites de runtime](RUNTIME-AND-SAFETY.md).

### 07 — `CRUSHING_PRESENCE`

- **Família organizacional na fonte:** `ender`; não comprova `SchoolType` individual.
- **Constante em `ModSpellRegistry`:** `CRUSHING_PRESENCE`.
- **Classe da fonte pública:** `CrushingPresenceSpell`.
- **Registry ID físico 0.0.16.3:** `NÃO VERIFICADO`. Não derivar namespace/path de campos ou nomes de classes.
- **Escola e configuração individual:** `NÃO VERIFICADO`; mesmo a escola Necro observada no source não prova a associação deste registro no binário instalado.
- **Custos, cooldown, level/rarity, targeting, efeito, dano/cura, summons, filtros PvP/boss, persistência, aquisição e world safety:** `NÃO VERIFICADO`. Nenhum desses mecanismos é inferido do nome.
- **Identidade semântica:** `COUNTED_RELEASE_BOUNDED`, já inventariada no lote de 98 da fonte contemporânea. O feitiço pertence ao provider, com casting/mana/cooldown hospedados no Iron's. Black Arcana não reproduz o efeito.
- **Fonte factual:** [inventário](SPELL-CATALOG.md), [proveniência](EVIDENCE-AND-PROVENANCE.md), [limites de runtime](RUNTIME-AND-SAFETY.md).

### 08 — `CRUSH`

- **Família organizacional na fonte:** `ender`; não comprova `SchoolType` individual.
- **Constante em `ModSpellRegistry`:** `CRUSH`.
- **Classe da fonte pública:** `CrushSpell`.
- **Registry ID físico 0.0.16.3:** `NÃO VERIFICADO`. Não derivar namespace/path de campos ou nomes de classes.
- **Escola e configuração individual:** `NÃO VERIFICADO`; mesmo a escola Necro observada no source não prova a associação deste registro no binário instalado.
- **Custos, cooldown, level/rarity, targeting, efeito, dano/cura, summons, filtros PvP/boss, persistência, aquisição e world safety:** `NÃO VERIFICADO`. Nenhum desses mecanismos é inferido do nome.
- **Identidade semântica:** `COUNTED_RELEASE_BOUNDED`, já inventariada no lote de 98 da fonte contemporânea. O feitiço pertence ao provider, com casting/mana/cooldown hospedados no Iron's. Black Arcana não reproduz o efeito.
- **Fonte factual:** [inventário](SPELL-CATALOG.md), [proveniência](EVIDENCE-AND-PROVENANCE.md), [limites de runtime](RUNTIME-AND-SAFETY.md).

### 09 — `DRAGON_CHARGE`

- **Família organizacional na fonte:** `ender`; não comprova `SchoolType` individual.
- **Constante em `ModSpellRegistry`:** `DRAGON_CHARGE`.
- **Classe da fonte pública:** `DragonChargeSpell`.
- **Registry ID físico 0.0.16.3:** `NÃO VERIFICADO`. Não derivar namespace/path de campos ou nomes de classes.
- **Escola e configuração individual:** `NÃO VERIFICADO`; mesmo a escola Necro observada no source não prova a associação deste registro no binário instalado.
- **Custos, cooldown, level/rarity, targeting, efeito, dano/cura, summons, filtros PvP/boss, persistência, aquisição e world safety:** `NÃO VERIFICADO`. Nenhum desses mecanismos é inferido do nome.
- **Identidade semântica:** `COUNTED_RELEASE_BOUNDED`, já inventariada no lote de 98 da fonte contemporânea. O feitiço pertence ao provider, com casting/mana/cooldown hospedados no Iron's. Black Arcana não reproduz o efeito.
- **Fonte factual:** [inventário](SPELL-CATALOG.md), [proveniência](EVIDENCE-AND-PROVENANCE.md), [limites de runtime](RUNTIME-AND-SAFETY.md).

### 10 — `ENDERSENT_SMASH`

- **Família organizacional na fonte:** `ender`; não comprova `SchoolType` individual.
- **Constante em `ModSpellRegistry`:** `ENDERSENT_SMASH`.
- **Classe da fonte pública:** `EndersentSmashSpell`.
- **Registry ID físico 0.0.16.3:** `NÃO VERIFICADO`. Não derivar namespace/path de campos ou nomes de classes.
- **Escola e configuração individual:** `NÃO VERIFICADO`; mesmo a escola Necro observada no source não prova a associação deste registro no binário instalado.
- **Custos, cooldown, level/rarity, targeting, efeito, dano/cura, summons, filtros PvP/boss, persistência, aquisição e world safety:** `NÃO VERIFICADO`. Nenhum desses mecanismos é inferido do nome.
- **Identidade semântica:** `COUNTED_RELEASE_BOUNDED`, já inventariada no lote de 98 da fonte contemporânea. O feitiço pertence ao provider, com casting/mana/cooldown hospedados no Iron's. Black Arcana não reproduz o efeito.
- **Fonte factual:** [inventário](SPELL-CATALOG.md), [proveniência](EVIDENCE-AND-PROVENANCE.md), [limites de runtime](RUNTIME-AND-SAFETY.md).

### 11 — `ENDERSENT_FORM`

- **Família organizacional na fonte:** `ender`; não comprova `SchoolType` individual.
- **Constante em `ModSpellRegistry`:** `ENDERSENT_FORM`.
- **Classe da fonte pública:** `EndersentFormSpell`.
- **Registry ID físico 0.0.16.3:** `NÃO VERIFICADO`. Não derivar namespace/path de campos ou nomes de classes.
- **Escola e configuração individual:** `NÃO VERIFICADO`; mesmo a escola Necro observada no source não prova a associação deste registro no binário instalado.
- **Custos, cooldown, level/rarity, targeting, efeito, dano/cura, summons, filtros PvP/boss, persistência, aquisição e world safety:** `NÃO VERIFICADO`. Nenhum desses mecanismos é inferido do nome.
- **Identidade semântica:** `COUNTED_RELEASE_BOUNDED`, já inventariada no lote de 98 da fonte contemporânea. O feitiço pertence ao provider, com casting/mana/cooldown hospedados no Iron's. Black Arcana não reproduz o efeito.
- **Fonte factual:** [inventário](SPELL-CATALOG.md), [proveniência](EVIDENCE-AND-PROVENANCE.md), [limites de runtime](RUNTIME-AND-SAFETY.md).

### 12 — `FIRMAMENT_SPLITTER`

- **Família organizacional na fonte:** `ender`; não comprova `SchoolType` individual.
- **Constante em `ModSpellRegistry`:** `FIRMAMENT_SPLITTER`.
- **Classe da fonte pública:** `FirmamentSplitterSpell`.
- **Registry ID físico 0.0.16.3:** `NÃO VERIFICADO`. Não derivar namespace/path de campos ou nomes de classes.
- **Escola e configuração individual:** `NÃO VERIFICADO`; mesmo a escola Necro observada no source não prova a associação deste registro no binário instalado.
- **Custos, cooldown, level/rarity, targeting, efeito, dano/cura, summons, filtros PvP/boss, persistência, aquisição e world safety:** `NÃO VERIFICADO`. Nenhum desses mecanismos é inferido do nome.
- **Identidade semântica:** `COUNTED_RELEASE_BOUNDED`, já inventariada no lote de 98 da fonte contemporânea. O feitiço pertence ao provider, com casting/mana/cooldown hospedados no Iron's. Black Arcana não reproduz o efeito.
- **Fonte factual:** [inventário](SPELL-CATALOG.md), [proveniência](EVIDENCE-AND-PROVENANCE.md), [limites de runtime](RUNTIME-AND-SAFETY.md).

### 13 — `GRAVITY_WELL`

- **Família organizacional na fonte:** `ender`; não comprova `SchoolType` individual.
- **Constante em `ModSpellRegistry`:** `GRAVITY_WELL`.
- **Classe da fonte pública:** `GravityWellSpell`.
- **Registry ID físico 0.0.16.3:** `NÃO VERIFICADO`. Não derivar namespace/path de campos ou nomes de classes.
- **Escola e configuração individual:** `NÃO VERIFICADO`; mesmo a escola Necro observada no source não prova a associação deste registro no binário instalado.
- **Custos, cooldown, level/rarity, targeting, efeito, dano/cura, summons, filtros PvP/boss, persistência, aquisição e world safety:** `NÃO VERIFICADO`. Nenhum desses mecanismos é inferido do nome.
- **Identidade semântica:** `COUNTED_RELEASE_BOUNDED`, já inventariada no lote de 98 da fonte contemporânea. O feitiço pertence ao provider, com casting/mana/cooldown hospedados no Iron's. Black Arcana não reproduz o efeito.
- **Fonte factual:** [inventário](SPELL-CATALOG.md), [proveniência](EVIDENCE-AND-PROVENANCE.md), [limites de runtime](RUNTIME-AND-SAFETY.md).

### 14 — `SPACE_BREAKER`

- **Família organizacional na fonte:** `ender`; não comprova `SchoolType` individual.
- **Constante em `ModSpellRegistry`:** `SPACE_BREAKER`.
- **Classe da fonte pública:** `SpaceBreakerSpell`.
- **Registry ID físico 0.0.16.3:** `NÃO VERIFICADO`. Não derivar namespace/path de campos ou nomes de classes.
- **Escola e configuração individual:** `NÃO VERIFICADO`; mesmo a escola Necro observada no source não prova a associação deste registro no binário instalado.
- **Custos, cooldown, level/rarity, targeting, efeito, dano/cura, summons, filtros PvP/boss, persistência, aquisição e world safety:** `NÃO VERIFICADO`. Nenhum desses mecanismos é inferido do nome.
- **Identidade semântica:** `COUNTED_RELEASE_BOUNDED`, já inventariada no lote de 98 da fonte contemporânea. O feitiço pertence ao provider, com casting/mana/cooldown hospedados no Iron's. Black Arcana não reproduz o efeito.
- **Fonte factual:** [inventário](SPELL-CATALOG.md), [proveniência](EVIDENCE-AND-PROVENANCE.md), [limites de runtime](RUNTIME-AND-SAFETY.md).

### 15 — `SPACE_RUPTURE`

- **Família organizacional na fonte:** `ender`; não comprova `SchoolType` individual.
- **Constante em `ModSpellRegistry`:** `SPACE_RUPTURE`.
- **Classe da fonte pública:** `SpaceRuptureSpell`.
- **Registry ID físico 0.0.16.3:** `NÃO VERIFICADO`. Não derivar namespace/path de campos ou nomes de classes.
- **Escola e configuração individual:** `NÃO VERIFICADO`; mesmo a escola Necro observada no source não prova a associação deste registro no binário instalado.
- **Custos, cooldown, level/rarity, targeting, efeito, dano/cura, summons, filtros PvP/boss, persistência, aquisição e world safety:** `NÃO VERIFICADO`. Nenhum desses mecanismos é inferido do nome.
- **Identidade semântica:** `COUNTED_RELEASE_BOUNDED`, já inventariada no lote de 98 da fonte contemporânea. O feitiço pertence ao provider, com casting/mana/cooldown hospedados no Iron's. Black Arcana não reproduz o efeito.
- **Fonte factual:** [inventário](SPELL-CATALOG.md), [proveniência](EVIDENCE-AND-PROVENANCE.md), [limites de runtime](RUNTIME-AND-SAFETY.md).

### 16 — `UNSTABLE_TELEPORT`

- **Família organizacional na fonte:** `ender`; não comprova `SchoolType` individual.
- **Constante em `ModSpellRegistry`:** `UNSTABLE_TELEPORT`.
- **Classe da fonte pública:** `UnstableTeleportSpell`.
- **Registry ID físico 0.0.16.3:** `NÃO VERIFICADO`. Não derivar namespace/path de campos ou nomes de classes.
- **Escola e configuração individual:** `NÃO VERIFICADO`; mesmo a escola Necro observada no source não prova a associação deste registro no binário instalado.
- **Custos, cooldown, level/rarity, targeting, efeito, dano/cura, summons, filtros PvP/boss, persistência, aquisição e world safety:** `NÃO VERIFICADO`. Nenhum desses mecanismos é inferido do nome.
- **Identidade semântica:** `COUNTED_RELEASE_BOUNDED`, já inventariada no lote de 98 da fonte contemporânea. O feitiço pertence ao provider, com casting/mana/cooldown hospedados no Iron's. Black Arcana não reproduz o efeito.
- **Fonte factual:** [inventário](SPELL-CATALOG.md), [proveniência](EVIDENCE-AND-PROVENANCE.md), [limites de runtime](RUNTIME-AND-SAFETY.md).

### 17 — `VOID_ARROWS`

- **Família organizacional na fonte:** `ender`; não comprova `SchoolType` individual.
- **Constante em `ModSpellRegistry`:** `VOID_ARROWS`.
- **Classe da fonte pública:** `VoidArrowsSpell`.
- **Registry ID físico 0.0.16.3:** `NÃO VERIFICADO`. Não derivar namespace/path de campos ou nomes de classes.
- **Escola e configuração individual:** `NÃO VERIFICADO`; mesmo a escola Necro observada no source não prova a associação deste registro no binário instalado.
- **Custos, cooldown, level/rarity, targeting, efeito, dano/cura, summons, filtros PvP/boss, persistência, aquisição e world safety:** `NÃO VERIFICADO`. Nenhum desses mecanismos é inferido do nome.
- **Identidade semântica:** `COUNTED_RELEASE_BOUNDED`, já inventariada no lote de 98 da fonte contemporânea. O feitiço pertence ao provider, com casting/mana/cooldown hospedados no Iron's. Black Arcana não reproduz o efeito.
- **Fonte factual:** [inventário](SPELL-CATALOG.md), [proveniência](EVIDENCE-AND-PROVENANCE.md), [limites de runtime](RUNTIME-AND-SAFETY.md).


## Família `evocation` — 3 registros

### 18 — `ENCHANTERS_BOOST`

- **Família organizacional na fonte:** `evocation`; não comprova `SchoolType` individual.
- **Constante em `ModSpellRegistry`:** `ENCHANTERS_BOOST`.
- **Classe da fonte pública:** `EnchantersBoostSpell`.
- **Registry ID físico 0.0.16.3:** `NÃO VERIFICADO`. Não derivar namespace/path de campos ou nomes de classes.
- **Escola e configuração individual:** `NÃO VERIFICADO`; mesmo a escola Necro observada no source não prova a associação deste registro no binário instalado.
- **Custos, cooldown, level/rarity, targeting, efeito, dano/cura, summons, filtros PvP/boss, persistência, aquisição e world safety:** `NÃO VERIFICADO`. Nenhum desses mecanismos é inferido do nome.
- **Identidade semântica:** `COUNTED_RELEASE_BOUNDED`, já inventariada no lote de 98 da fonte contemporânea. O feitiço pertence ao provider, com casting/mana/cooldown hospedados no Iron's. Black Arcana não reproduz o efeito.
- **Fonte factual:** [inventário](SPELL-CATALOG.md), [proveniência](EVIDENCE-AND-PROVENANCE.md), [limites de runtime](RUNTIME-AND-SAFETY.md).

### 19 — `ENCHANTERS_PROTECTION`

- **Família organizacional na fonte:** `evocation`; não comprova `SchoolType` individual.
- **Constante em `ModSpellRegistry`:** `ENCHANTERS_PROTECTION`.
- **Classe da fonte pública:** `EnchantersProtectionSpell`.
- **Registry ID físico 0.0.16.3:** `NÃO VERIFICADO`. Não derivar namespace/path de campos ou nomes de classes.
- **Escola e configuração individual:** `NÃO VERIFICADO`; mesmo a escola Necro observada no source não prova a associação deste registro no binário instalado.
- **Custos, cooldown, level/rarity, targeting, efeito, dano/cura, summons, filtros PvP/boss, persistência, aquisição e world safety:** `NÃO VERIFICADO`. Nenhum desses mecanismos é inferido do nome.
- **Identidade semântica:** `COUNTED_RELEASE_BOUNDED`, já inventariada no lote de 98 da fonte contemporânea. O feitiço pertence ao provider, com casting/mana/cooldown hospedados no Iron's. Black Arcana não reproduz o efeito.
- **Fonte factual:** [inventário](SPELL-CATALOG.md), [proveniência](EVIDENCE-AND-PROVENANCE.md), [limites de runtime](RUNTIME-AND-SAFETY.md).

### 20 — `SPELL_OF_UNDYING`

- **Família organizacional na fonte:** `evocation`; não comprova `SchoolType` individual.
- **Constante em `ModSpellRegistry`:** `SPELL_OF_UNDYING`.
- **Classe da fonte pública:** `SpellOfUndyingSpell`.
- **Registry ID físico 0.0.16.3:** `NÃO VERIFICADO`. Não derivar namespace/path de campos ou nomes de classes.
- **Escola e configuração individual:** `NÃO VERIFICADO`; mesmo a escola Necro observada no source não prova a associação deste registro no binário instalado.
- **Custos, cooldown, level/rarity, targeting, efeito, dano/cura, summons, filtros PvP/boss, persistência, aquisição e world safety:** `NÃO VERIFICADO`. Nenhum desses mecanismos é inferido do nome.
- **Identidade semântica:** `COUNTED_RELEASE_BOUNDED`, já inventariada no lote de 98 da fonte contemporânea. O feitiço pertence ao provider, com casting/mana/cooldown hospedados no Iron's. Black Arcana não reproduz o efeito.
- **Fonte factual:** [inventário](SPELL-CATALOG.md), [proveniência](EVIDENCE-AND-PROVENANCE.md), [limites de runtime](RUNTIME-AND-SAFETY.md).


## Família `fire` — 10 registros

### 21 — `BRIMSTONE_BUZZSAW`

- **Família organizacional na fonte:** `fire`; não comprova `SchoolType` individual.
- **Constante em `ModSpellRegistry`:** `BRIMSTONE_BUZZSAW`.
- **Classe da fonte pública:** `BrimstoneBuzzsawSpell`.
- **Registry ID físico 0.0.16.3:** `NÃO VERIFICADO`. Não derivar namespace/path de campos ou nomes de classes.
- **Escola e configuração individual:** `NÃO VERIFICADO`; mesmo a escola Necro observada no source não prova a associação deste registro no binário instalado.
- **Custos, cooldown, level/rarity, targeting, efeito, dano/cura, summons, filtros PvP/boss, persistência, aquisição e world safety:** `NÃO VERIFICADO`. Nenhum desses mecanismos é inferido do nome.
- **Identidade semântica:** `COUNTED_RELEASE_BOUNDED`, já inventariada no lote de 98 da fonte contemporânea. O feitiço pertence ao provider, com casting/mana/cooldown hospedados no Iron's. Black Arcana não reproduz o efeito.
- **Fonte factual:** [inventário](SPELL-CATALOG.md), [proveniência](EVIDENCE-AND-PROVENANCE.md), [limites de runtime](RUNTIME-AND-SAFETY.md).

### 22 — `BRIMSTONE_RAIN`

- **Família organizacional na fonte:** `fire`; não comprova `SchoolType` individual.
- **Constante em `ModSpellRegistry`:** `BRIMSTONE_RAIN`.
- **Classe da fonte pública:** `BrimstoneRainSpell`.
- **Registry ID físico 0.0.16.3:** `NÃO VERIFICADO`. Não derivar namespace/path de campos ou nomes de classes.
- **Escola e configuração individual:** `NÃO VERIFICADO`; mesmo a escola Necro observada no source não prova a associação deste registro no binário instalado.
- **Custos, cooldown, level/rarity, targeting, efeito, dano/cura, summons, filtros PvP/boss, persistência, aquisição e world safety:** `NÃO VERIFICADO`. Nenhum desses mecanismos é inferido do nome.
- **Identidade semântica:** `COUNTED_RELEASE_BOUNDED`, já inventariada no lote de 98 da fonte contemporânea. O feitiço pertence ao provider, com casting/mana/cooldown hospedados no Iron's. Black Arcana não reproduz o efeito.
- **Fonte factual:** [inventário](SPELL-CATALOG.md), [proveniência](EVIDENCE-AND-PROVENANCE.md), [limites de runtime](RUNTIME-AND-SAFETY.md).

### 23 — `BRIMSTONE_WRATH`

- **Família organizacional na fonte:** `fire`; não comprova `SchoolType` individual.
- **Constante em `ModSpellRegistry`:** `BRIMSTONE_WRATH`.
- **Classe da fonte pública:** `BrimstoneWrathSpell`.
- **Registry ID físico 0.0.16.3:** `NÃO VERIFICADO`. Não derivar namespace/path de campos ou nomes de classes.
- **Escola e configuração individual:** `NÃO VERIFICADO`; mesmo a escola Necro observada no source não prova a associação deste registro no binário instalado.
- **Custos, cooldown, level/rarity, targeting, efeito, dano/cura, summons, filtros PvP/boss, persistência, aquisição e world safety:** `NÃO VERIFICADO`. Nenhum desses mecanismos é inferido do nome.
- **Identidade semântica:** `COUNTED_RELEASE_BOUNDED`, já inventariada no lote de 98 da fonte contemporânea. O feitiço pertence ao provider, com casting/mana/cooldown hospedados no Iron's. Black Arcana não reproduz o efeito.
- **Fonte factual:** [inventário](SPELL-CATALOG.md), [proveniência](EVIDENCE-AND-PROVENANCE.md), [limites de runtime](RUNTIME-AND-SAFETY.md).

### 24 — `CAUTERIZING_TOUCH`

- **Família organizacional na fonte:** `fire`; não comprova `SchoolType` individual.
- **Constante em `ModSpellRegistry`:** `CAUTERIZING_TOUCH`.
- **Classe da fonte pública:** `CauterizingTouchSpell`.
- **Registry ID físico 0.0.16.3:** `NÃO VERIFICADO`. Não derivar namespace/path de campos ou nomes de classes.
- **Escola e configuração individual:** `NÃO VERIFICADO`; mesmo a escola Necro observada no source não prova a associação deste registro no binário instalado.
- **Custos, cooldown, level/rarity, targeting, efeito, dano/cura, summons, filtros PvP/boss, persistência, aquisição e world safety:** `NÃO VERIFICADO`. Nenhum desses mecanismos é inferido do nome.
- **Identidade semântica:** `COUNTED_RELEASE_BOUNDED`, já inventariada no lote de 98 da fonte contemporânea. O feitiço pertence ao provider, com casting/mana/cooldown hospedados no Iron's. Black Arcana não reproduz o efeito.
- **Fonte factual:** [inventário](SPELL-CATALOG.md), [proveniência](EVIDENCE-AND-PROVENANCE.md), [limites de runtime](RUNTIME-AND-SAFETY.md).

### 25 — `FRENZIED_BURST`

- **Família organizacional na fonte:** `fire`; não comprova `SchoolType` individual.
- **Constante em `ModSpellRegistry`:** `FRENZIED_BURST`.
- **Classe da fonte pública:** `FrenziedBurstSpell`.
- **Registry ID físico 0.0.16.3:** `NÃO VERIFICADO`. Não derivar namespace/path de campos ou nomes de classes.
- **Escola e configuração individual:** `NÃO VERIFICADO`; mesmo a escola Necro observada no source não prova a associação deste registro no binário instalado.
- **Custos, cooldown, level/rarity, targeting, efeito, dano/cura, summons, filtros PvP/boss, persistência, aquisição e world safety:** `NÃO VERIFICADO`. Nenhum desses mecanismos é inferido do nome.
- **Identidade semântica:** `COUNTED_RELEASE_BOUNDED`, já inventariada no lote de 98 da fonte contemporânea. O feitiço pertence ao provider, com casting/mana/cooldown hospedados no Iron's. Black Arcana não reproduz o efeito.
- **Fonte factual:** [inventário](SPELL-CATALOG.md), [proveniência](EVIDENCE-AND-PROVENANCE.md), [limites de runtime](RUNTIME-AND-SAFETY.md).

### 26 — `FRENZIED_STORM`

- **Família organizacional na fonte:** `fire`; não comprova `SchoolType` individual.
- **Constante em `ModSpellRegistry`:** `FRENZIED_STORM`.
- **Classe da fonte pública:** `FrenziedStormSpell`.
- **Registry ID físico 0.0.16.3:** `NÃO VERIFICADO`. Não derivar namespace/path de campos ou nomes de classes.
- **Escola e configuração individual:** `NÃO VERIFICADO`; mesmo a escola Necro observada no source não prova a associação deste registro no binário instalado.
- **Custos, cooldown, level/rarity, targeting, efeito, dano/cura, summons, filtros PvP/boss, persistência, aquisição e world safety:** `NÃO VERIFICADO`. Nenhum desses mecanismos é inferido do nome.
- **Identidade semântica:** `COUNTED_RELEASE_BOUNDED`, já inventariada no lote de 98 da fonte contemporânea. O feitiço pertence ao provider, com casting/mana/cooldown hospedados no Iron's. Black Arcana não reproduz o efeito.
- **Fonte factual:** [inventário](SPELL-CATALOG.md), [proveniência](EVIDENCE-AND-PROVENANCE.md), [limites de runtime](RUNTIME-AND-SAFETY.md).

### 27 — `FRENZY_SURGE`

- **Família organizacional na fonte:** `fire`; não comprova `SchoolType` individual.
- **Constante em `ModSpellRegistry`:** `FRENZY_SURGE`.
- **Classe da fonte pública:** `FrenzySurgeSpell`.
- **Registry ID físico 0.0.16.3:** `NÃO VERIFICADO`. Não derivar namespace/path de campos ou nomes de classes.
- **Escola e configuração individual:** `NÃO VERIFICADO`; mesmo a escola Necro observada no source não prova a associação deste registro no binário instalado.
- **Custos, cooldown, level/rarity, targeting, efeito, dano/cura, summons, filtros PvP/boss, persistência, aquisição e world safety:** `NÃO VERIFICADO`. Nenhum desses mecanismos é inferido do nome.
- **Identidade semântica:** `COUNTED_RELEASE_BOUNDED`, já inventariada no lote de 98 da fonte contemporânea. O feitiço pertence ao provider, com casting/mana/cooldown hospedados no Iron's. Black Arcana não reproduz o efeito.
- **Fonte factual:** [inventário](SPELL-CATALOG.md), [proveniência](EVIDENCE-AND-PROVENANCE.md), [limites de runtime](RUNTIME-AND-SAFETY.md).

### 28 — `NAPALM_ORB`

- **Família organizacional na fonte:** `fire`; não comprova `SchoolType` individual.
- **Constante em `ModSpellRegistry`:** `NAPALM_ORB`.
- **Classe da fonte pública:** `NapalmOrbSpell`.
- **Registry ID físico 0.0.16.3:** `NÃO VERIFICADO`. Não derivar namespace/path de campos ou nomes de classes.
- **Escola e configuração individual:** `NÃO VERIFICADO`; mesmo a escola Necro observada no source não prova a associação deste registro no binário instalado.
- **Custos, cooldown, level/rarity, targeting, efeito, dano/cura, summons, filtros PvP/boss, persistência, aquisição e world safety:** `NÃO VERIFICADO`. Nenhum desses mecanismos é inferido do nome.
- **Identidade semântica:** `COUNTED_RELEASE_BOUNDED`, já inventariada no lote de 98 da fonte contemporânea. O feitiço pertence ao provider, com casting/mana/cooldown hospedados no Iron's. Black Arcana não reproduz o efeito.
- **Fonte factual:** [inventário](SPELL-CATALOG.md), [proveniência](EVIDENCE-AND-PROVENANCE.md), [limites de runtime](RUNTIME-AND-SAFETY.md).

### 29 — `OVERHEAT`

- **Família organizacional na fonte:** `fire`; não comprova `SchoolType` individual.
- **Constante em `ModSpellRegistry`:** `OVERHEAT`.
- **Classe da fonte pública:** `OverheatSpell`.
- **Registry ID físico 0.0.16.3:** `NÃO VERIFICADO`. Não derivar namespace/path de campos ou nomes de classes.
- **Escola e configuração individual:** `NÃO VERIFICADO`; mesmo a escola Necro observada no source não prova a associação deste registro no binário instalado.
- **Custos, cooldown, level/rarity, targeting, efeito, dano/cura, summons, filtros PvP/boss, persistência, aquisição e world safety:** `NÃO VERIFICADO`. Nenhum desses mecanismos é inferido do nome.
- **Identidade semântica:** `COUNTED_RELEASE_BOUNDED`, já inventariada no lote de 98 da fonte contemporânea. O feitiço pertence ao provider, com casting/mana/cooldown hospedados no Iron's. Black Arcana não reproduz o efeito.
- **Fonte factual:** [inventário](SPELL-CATALOG.md), [proveniência](EVIDENCE-AND-PROVENANCE.md), [limites de runtime](RUNTIME-AND-SAFETY.md).

### 30 — `WRATH`

- **Família organizacional na fonte:** `fire`; não comprova `SchoolType` individual.
- **Constante em `ModSpellRegistry`:** `WRATH`.
- **Classe da fonte pública:** `WrathSpell`.
- **Registry ID físico 0.0.16.3:** `NÃO VERIFICADO`. Não derivar namespace/path de campos ou nomes de classes.
- **Escola e configuração individual:** `NÃO VERIFICADO`; mesmo a escola Necro observada no source não prova a associação deste registro no binário instalado.
- **Custos, cooldown, level/rarity, targeting, efeito, dano/cura, summons, filtros PvP/boss, persistência, aquisição e world safety:** `NÃO VERIFICADO`. Nenhum desses mecanismos é inferido do nome.
- **Identidade semântica:** `COUNTED_RELEASE_BOUNDED`, já inventariada no lote de 98 da fonte contemporânea. O feitiço pertence ao provider, com casting/mana/cooldown hospedados no Iron's. Black Arcana não reproduz o efeito.
- **Fonte factual:** [inventário](SPELL-CATALOG.md), [proveniência](EVIDENCE-AND-PROVENANCE.md), [limites de runtime](RUNTIME-AND-SAFETY.md).


## Família `holy` — 4 registros

### 31 — `DIVINE_INTERVENTION`

- **Família organizacional na fonte:** `holy`; não comprova `SchoolType` individual.
- **Constante em `ModSpellRegistry`:** `DIVINE_INTERVENTION`.
- **Classe da fonte pública:** `DivineInterventionSpell`.
- **Registry ID físico 0.0.16.3:** `NÃO VERIFICADO`. Não derivar namespace/path de campos ou nomes de classes.
- **Escola e configuração individual:** `NÃO VERIFICADO`; mesmo a escola Necro observada no source não prova a associação deste registro no binário instalado.
- **Custos, cooldown, level/rarity, targeting, efeito, dano/cura, summons, filtros PvP/boss, persistência, aquisição e world safety:** `NÃO VERIFICADO`. Nenhum desses mecanismos é inferido do nome.
- **Identidade semântica:** `COUNTED_RELEASE_BOUNDED`, já inventariada no lote de 98 da fonte contemporânea. O feitiço pertence ao provider, com casting/mana/cooldown hospedados no Iron's. Black Arcana não reproduz o efeito.
- **Fonte factual:** [inventário](SPELL-CATALOG.md), [proveniência](EVIDENCE-AND-PROVENANCE.md), [limites de runtime](RUNTIME-AND-SAFETY.md).

### 32 — `HALLOW_SLASH`

- **Família organizacional na fonte:** `holy`; não comprova `SchoolType` individual.
- **Constante em `ModSpellRegistry`:** `HALLOW_SLASH`.
- **Classe da fonte pública:** `HallowSlashSpell`.
- **Registry ID físico 0.0.16.3:** `NÃO VERIFICADO`. Não derivar namespace/path de campos ou nomes de classes.
- **Escola e configuração individual:** `NÃO VERIFICADO`; mesmo a escola Necro observada no source não prova a associação deste registro no binário instalado.
- **Custos, cooldown, level/rarity, targeting, efeito, dano/cura, summons, filtros PvP/boss, persistência, aquisição e world safety:** `NÃO VERIFICADO`. Nenhum desses mecanismos é inferido do nome.
- **Identidade semântica:** `COUNTED_RELEASE_BOUNDED`, já inventariada no lote de 98 da fonte contemporânea. O feitiço pertence ao provider, com casting/mana/cooldown hospedados no Iron's. Black Arcana não reproduz o efeito.
- **Fonte factual:** [inventário](SPELL-CATALOG.md), [proveniência](EVIDENCE-AND-PROVENANCE.md), [limites de runtime](RUNTIME-AND-SAFETY.md).

### 33 — `PALADIN_THROW`

- **Família organizacional na fonte:** `holy`; não comprova `SchoolType` individual.
- **Constante em `ModSpellRegistry`:** `PALADIN_THROW`.
- **Classe da fonte pública:** `PaladinThrowSpell`.
- **Registry ID físico 0.0.16.3:** `NÃO VERIFICADO`. Não derivar namespace/path de campos ou nomes de classes.
- **Escola e configuração individual:** `NÃO VERIFICADO`; mesmo a escola Necro observada no source não prova a associação deste registro no binário instalado.
- **Custos, cooldown, level/rarity, targeting, efeito, dano/cura, summons, filtros PvP/boss, persistência, aquisição e world safety:** `NÃO VERIFICADO`. Nenhum desses mecanismos é inferido do nome.
- **Identidade semântica:** `COUNTED_RELEASE_BOUNDED`, já inventariada no lote de 98 da fonte contemporânea. O feitiço pertence ao provider, com casting/mana/cooldown hospedados no Iron's. Black Arcana não reproduz o efeito.
- **Fonte factual:** [inventário](SPELL-CATALOG.md), [proveniência](EVIDENCE-AND-PROVENANCE.md), [limites de runtime](RUNTIME-AND-SAFETY.md).

### 34 — `SUMMON_AEGIS_PATROL`

- **Família organizacional na fonte:** `holy`; não comprova `SchoolType` individual.
- **Constante em `ModSpellRegistry`:** `SUMMON_AEGIS_PATROL`.
- **Classe da fonte pública:** `SummonAegisPatrolSpell`.
- **Registry ID físico 0.0.16.3:** `NÃO VERIFICADO`. Não derivar namespace/path de campos ou nomes de classes.
- **Escola e configuração individual:** `NÃO VERIFICADO`; mesmo a escola Necro observada no source não prova a associação deste registro no binário instalado.
- **Custos, cooldown, level/rarity, targeting, efeito, dano/cura, summons, filtros PvP/boss, persistência, aquisição e world safety:** `NÃO VERIFICADO`. Nenhum desses mecanismos é inferido do nome.
- **Identidade semântica:** `COUNTED_RELEASE_BOUNDED`, já inventariada no lote de 98 da fonte contemporânea. O feitiço pertence ao provider, com casting/mana/cooldown hospedados no Iron's. Black Arcana não reproduz o efeito.
- **Fonte factual:** [inventário](SPELL-CATALOG.md), [proveniência](EVIDENCE-AND-PROVENANCE.md), [limites de runtime](RUNTIME-AND-SAFETY.md).


## Família `hydro` — 8 registros

### 35 — `BUBBLE_SPRAY`

- **Família organizacional na fonte:** `hydro`; não comprova `SchoolType` individual.
- **Constante em `ModSpellRegistry`:** `BUBBLE_SPRAY`.
- **Classe da fonte pública:** `BubbleSpraySpell`.
- **Registry ID físico 0.0.16.3:** `NÃO VERIFICADO`. Não derivar namespace/path de campos ou nomes de classes.
- **Escola e configuração individual:** `NÃO VERIFICADO`; mesmo a escola Necro observada no source não prova a associação deste registro no binário instalado.
- **Custos, cooldown, level/rarity, targeting, efeito, dano/cura, summons, filtros PvP/boss, persistência, aquisição e world safety:** `NÃO VERIFICADO`. Nenhum desses mecanismos é inferido do nome.
- **Identidade semântica:** `COUNTED_RELEASE_BOUNDED`, já inventariada no lote de 98 da fonte contemporânea. O feitiço pertence ao provider, com casting/mana/cooldown hospedados no Iron's. Black Arcana não reproduz o efeito.
- **Fonte factual:** [inventário](SPELL-CATALOG.md), [proveniência](EVIDENCE-AND-PROVENANCE.md), [limites de runtime](RUNTIME-AND-SAFETY.md).

### 36 — `EFFERVESCENCE_BUBBLE`

- **Família organizacional na fonte:** `hydro`; não comprova `SchoolType` individual.
- **Constante em `ModSpellRegistry`:** `EFFERVESCENCE_BUBBLE`.
- **Classe da fonte pública:** `EffervescenceBubbleSpell`.
- **Registry ID físico 0.0.16.3:** `NÃO VERIFICADO`. Não derivar namespace/path de campos ou nomes de classes.
- **Escola e configuração individual:** `NÃO VERIFICADO`; mesmo a escola Necro observada no source não prova a associação deste registro no binário instalado.
- **Custos, cooldown, level/rarity, targeting, efeito, dano/cura, summons, filtros PvP/boss, persistência, aquisição e world safety:** `NÃO VERIFICADO`. Nenhum desses mecanismos é inferido do nome.
- **Identidade semântica:** `COUNTED_RELEASE_BOUNDED`, já inventariada no lote de 98 da fonte contemporânea. O feitiço pertence ao provider, com casting/mana/cooldown hospedados no Iron's. Black Arcana não reproduz o efeito.
- **Fonte factual:** [inventário](SPELL-CATALOG.md), [proveniência](EVIDENCE-AND-PROVENANCE.md), [limites de runtime](RUNTIME-AND-SAFETY.md).

### 37 — `GLOW_INK_RELEASE`

- **Família organizacional na fonte:** `hydro`; não comprova `SchoolType` individual.
- **Constante em `ModSpellRegistry`:** `GLOW_INK_RELEASE`.
- **Classe da fonte pública:** `GlowInkReleaseSpell`.
- **Registry ID físico 0.0.16.3:** `NÃO VERIFICADO`. Não derivar namespace/path de campos ou nomes de classes.
- **Escola e configuração individual:** `NÃO VERIFICADO`; mesmo a escola Necro observada no source não prova a associação deste registro no binário instalado.
- **Custos, cooldown, level/rarity, targeting, efeito, dano/cura, summons, filtros PvP/boss, persistência, aquisição e world safety:** `NÃO VERIFICADO`. Nenhum desses mecanismos é inferido do nome.
- **Identidade semântica:** `COUNTED_RELEASE_BOUNDED`, já inventariada no lote de 98 da fonte contemporânea. O feitiço pertence ao provider, com casting/mana/cooldown hospedados no Iron's. Black Arcana não reproduz o efeito.
- **Fonte factual:** [inventário](SPELL-CATALOG.md), [proveniência](EVIDENCE-AND-PROVENANCE.md), [limites de runtime](RUNTIME-AND-SAFETY.md).

### 38 — `INK_BOMB`

- **Família organizacional na fonte:** `hydro`; não comprova `SchoolType` individual.
- **Constante em `ModSpellRegistry`:** `INK_BOMB`.
- **Classe da fonte pública:** `InkBombSpell`.
- **Registry ID físico 0.0.16.3:** `NÃO VERIFICADO`. Não derivar namespace/path de campos ou nomes de classes.
- **Escola e configuração individual:** `NÃO VERIFICADO`; mesmo a escola Necro observada no source não prova a associação deste registro no binário instalado.
- **Custos, cooldown, level/rarity, targeting, efeito, dano/cura, summons, filtros PvP/boss, persistência, aquisição e world safety:** `NÃO VERIFICADO`. Nenhum desses mecanismos é inferido do nome.
- **Identidade semântica:** `COUNTED_RELEASE_BOUNDED`, já inventariada no lote de 98 da fonte contemporânea. O feitiço pertence ao provider, com casting/mana/cooldown hospedados no Iron's. Black Arcana não reproduz o efeito.
- **Fonte factual:** [inventário](SPELL-CATALOG.md), [proveniência](EVIDENCE-AND-PROVENANCE.md), [limites de runtime](RUNTIME-AND-SAFETY.md).

### 39 — `RAZORBLADE_TYPHOON`

- **Família organizacional na fonte:** `hydro`; não comprova `SchoolType` individual.
- **Constante em `ModSpellRegistry`:** `RAZORBLADE_TYPHOON`.
- **Classe da fonte pública:** `RazorbladeTyphoonSpell`.
- **Registry ID físico 0.0.16.3:** `NÃO VERIFICADO`. Não derivar namespace/path de campos ou nomes de classes.
- **Escola e configuração individual:** `NÃO VERIFICADO`; mesmo a escola Necro observada no source não prova a associação deste registro no binário instalado.
- **Custos, cooldown, level/rarity, targeting, efeito, dano/cura, summons, filtros PvP/boss, persistência, aquisição e world safety:** `NÃO VERIFICADO`. Nenhum desses mecanismos é inferido do nome.
- **Identidade semântica:** `COUNTED_RELEASE_BOUNDED`, já inventariada no lote de 98 da fonte contemporânea. O feitiço pertence ao provider, com casting/mana/cooldown hospedados no Iron's. Black Arcana não reproduz o efeito.
- **Fonte factual:** [inventário](SPELL-CATALOG.md), [proveniência](EVIDENCE-AND-PROVENANCE.md), [limites de runtime](RUNTIME-AND-SAFETY.md).

### 40 — `RIPTIDE_DASH`

- **Família organizacional na fonte:** `hydro`; não comprova `SchoolType` individual.
- **Constante em `ModSpellRegistry`:** `RIPTIDE_DASH`.
- **Classe da fonte pública:** `RiptideDashSpell`.
- **Registry ID físico 0.0.16.3:** `NÃO VERIFICADO`. Não derivar namespace/path de campos ou nomes de classes.
- **Escola e configuração individual:** `NÃO VERIFICADO`; mesmo a escola Necro observada no source não prova a associação deste registro no binário instalado.
- **Custos, cooldown, level/rarity, targeting, efeito, dano/cura, summons, filtros PvP/boss, persistência, aquisição e world safety:** `NÃO VERIFICADO`. Nenhum desses mecanismos é inferido do nome.
- **Identidade semântica:** `COUNTED_RELEASE_BOUNDED`, já inventariada no lote de 98 da fonte contemporânea. O feitiço pertence ao provider, com casting/mana/cooldown hospedados no Iron's. Black Arcana não reproduz o efeito.
- **Fonte factual:** [inventário](SPELL-CATALOG.md), [proveniência](EVIDENCE-AND-PROVENANCE.md), [limites de runtime](RUNTIME-AND-SAFETY.md).

### 41 — `SUMMON_PRISMARINE_SQUAD`

- **Família organizacional na fonte:** `hydro`; não comprova `SchoolType` individual.
- **Constante em `ModSpellRegistry`:** `SUMMON_PRISMARINE_SQUAD`.
- **Classe da fonte pública:** `SummonPrismarineSquadSpell`.
- **Registry ID físico 0.0.16.3:** `NÃO VERIFICADO`. Não derivar namespace/path de campos ou nomes de classes.
- **Escola e configuração individual:** `NÃO VERIFICADO`; mesmo a escola Necro observada no source não prova a associação deste registro no binário instalado.
- **Custos, cooldown, level/rarity, targeting, efeito, dano/cura, summons, filtros PvP/boss, persistência, aquisição e world safety:** `NÃO VERIFICADO`. Nenhum desses mecanismos é inferido do nome.
- **Identidade semântica:** `COUNTED_RELEASE_BOUNDED`, já inventariada no lote de 98 da fonte contemporânea. O feitiço pertence ao provider, com casting/mana/cooldown hospedados no Iron's. Black Arcana não reproduz o efeito.
- **Fonte factual:** [inventário](SPELL-CATALOG.md), [proveniência](EVIDENCE-AND-PROVENANCE.md), [limites de runtime](RUNTIME-AND-SAFETY.md).

### 42 — `WATER_TRIDENT`

- **Família organizacional na fonte:** `hydro`; não comprova `SchoolType` individual.
- **Constante em `ModSpellRegistry`:** `WATER_TRIDENT`.
- **Classe da fonte pública:** `WaterTridentSpell`.
- **Registry ID físico 0.0.16.3:** `NÃO VERIFICADO`. Não derivar namespace/path de campos ou nomes de classes.
- **Escola e configuração individual:** `NÃO VERIFICADO`; mesmo a escola Necro observada no source não prova a associação deste registro no binário instalado.
- **Custos, cooldown, level/rarity, targeting, efeito, dano/cura, summons, filtros PvP/boss, persistência, aquisição e world safety:** `NÃO VERIFICADO`. Nenhum desses mecanismos é inferido do nome.
- **Identidade semântica:** `COUNTED_RELEASE_BOUNDED`, já inventariada no lote de 98 da fonte contemporânea. O feitiço pertence ao provider, com casting/mana/cooldown hospedados no Iron's. Black Arcana não reproduz o efeito.
- **Fonte factual:** [inventário](SPELL-CATALOG.md), [proveniência](EVIDENCE-AND-PROVENANCE.md), [limites de runtime](RUNTIME-AND-SAFETY.md).


## Família `ice` — 8 registros

### 43 — `BLIZZARD_ASPECT`

- **Família organizacional na fonte:** `ice`; não comprova `SchoolType` individual.
- **Constante em `ModSpellRegistry`:** `BLIZZARD_ASPECT`.
- **Classe da fonte pública:** `BlizzardAspectSpell`.
- **Registry ID físico 0.0.16.3:** `NÃO VERIFICADO`. Não derivar namespace/path de campos ou nomes de classes.
- **Escola e configuração individual:** `NÃO VERIFICADO`; mesmo a escola Necro observada no source não prova a associação deste registro no binário instalado.
- **Custos, cooldown, level/rarity, targeting, efeito, dano/cura, summons, filtros PvP/boss, persistência, aquisição e world safety:** `NÃO VERIFICADO`. Nenhum desses mecanismos é inferido do nome.
- **Identidade semântica:** `COUNTED_RELEASE_BOUNDED`, já inventariada no lote de 98 da fonte contemporânea. O feitiço pertence ao provider, com casting/mana/cooldown hospedados no Iron's. Black Arcana não reproduz o efeito.
- **Fonte factual:** [inventário](SPELL-CATALOG.md), [proveniência](EVIDENCE-AND-PROVENANCE.md), [limites de runtime](RUNTIME-AND-SAFETY.md).

### 44 — `FROST_BREATH`

- **Família organizacional na fonte:** `ice`; não comprova `SchoolType` individual.
- **Constante em `ModSpellRegistry`:** `FROST_BREATH`.
- **Classe da fonte pública:** `FrostBreathSpell`.
- **Registry ID físico 0.0.16.3:** `NÃO VERIFICADO`. Não derivar namespace/path de campos ou nomes de classes.
- **Escola e configuração individual:** `NÃO VERIFICADO`; mesmo a escola Necro observada no source não prova a associação deste registro no binário instalado.
- **Custos, cooldown, level/rarity, targeting, efeito, dano/cura, summons, filtros PvP/boss, persistência, aquisição e world safety:** `NÃO VERIFICADO`. Nenhum desses mecanismos é inferido do nome.
- **Identidade semântica:** `COUNTED_RELEASE_BOUNDED`, já inventariada no lote de 98 da fonte contemporânea. O feitiço pertence ao provider, com casting/mana/cooldown hospedados no Iron's. Black Arcana não reproduz o efeito.
- **Fonte factual:** [inventário](SPELL-CATALOG.md), [proveniência](EVIDENCE-AND-PROVENANCE.md), [limites de runtime](RUNTIME-AND-SAFETY.md).

### 45 — `FROST_COATING`

- **Família organizacional na fonte:** `ice`; não comprova `SchoolType` individual.
- **Constante em `ModSpellRegistry`:** `FROST_COATING`.
- **Classe da fonte pública:** `FrostCoatingSpell`.
- **Registry ID físico 0.0.16.3:** `NÃO VERIFICADO`. Não derivar namespace/path de campos ou nomes de classes.
- **Escola e configuração individual:** `NÃO VERIFICADO`; mesmo a escola Necro observada no source não prova a associação deste registro no binário instalado.
- **Custos, cooldown, level/rarity, targeting, efeito, dano/cura, summons, filtros PvP/boss, persistência, aquisição e world safety:** `NÃO VERIFICADO`. Nenhum desses mecanismos é inferido do nome.
- **Identidade semântica:** `COUNTED_RELEASE_BOUNDED`, já inventariada no lote de 98 da fonte contemporânea. O feitiço pertence ao provider, com casting/mana/cooldown hospedados no Iron's. Black Arcana não reproduz o efeito.
- **Fonte factual:** [inventário](SPELL-CATALOG.md), [proveniência](EVIDENCE-AND-PROVENANCE.md), [limites de runtime](RUNTIME-AND-SAFETY.md).

### 46 — `FROSTED_SNOWBOLT`

- **Família organizacional na fonte:** `ice`; não comprova `SchoolType` individual.
- **Constante em `ModSpellRegistry`:** `FROSTED_SNOWBOLT`.
- **Classe da fonte pública:** `FrostedSnowboltSpell`.
- **Registry ID físico 0.0.16.3:** `NÃO VERIFICADO`. Não derivar namespace/path de campos ou nomes de classes.
- **Escola e configuração individual:** `NÃO VERIFICADO`; mesmo a escola Necro observada no source não prova a associação deste registro no binário instalado.
- **Custos, cooldown, level/rarity, targeting, efeito, dano/cura, summons, filtros PvP/boss, persistência, aquisição e world safety:** `NÃO VERIFICADO`. Nenhum desses mecanismos é inferido do nome.
- **Identidade semântica:** `COUNTED_RELEASE_BOUNDED`, já inventariada no lote de 98 da fonte contemporânea. O feitiço pertence ao provider, com casting/mana/cooldown hospedados no Iron's. Black Arcana não reproduz o efeito.
- **Fonte factual:** [inventário](SPELL-CATALOG.md), [proveniência](EVIDENCE-AND-PROVENANCE.md), [limites de runtime](RUNTIME-AND-SAFETY.md).

### 47 — `ICE_ARSENAL`

- **Família organizacional na fonte:** `ice`; não comprova `SchoolType` individual.
- **Constante em `ModSpellRegistry`:** `ICE_ARSENAL`.
- **Classe da fonte pública:** `IceArsenalSpell`.
- **Registry ID físico 0.0.16.3:** `NÃO VERIFICADO`. Não derivar namespace/path de campos ou nomes de classes.
- **Escola e configuração individual:** `NÃO VERIFICADO`; mesmo a escola Necro observada no source não prova a associação deste registro no binário instalado.
- **Custos, cooldown, level/rarity, targeting, efeito, dano/cura, summons, filtros PvP/boss, persistência, aquisição e world safety:** `NÃO VERIFICADO`. Nenhum desses mecanismos é inferido do nome.
- **Identidade semântica:** `COUNTED_RELEASE_BOUNDED`, já inventariada no lote de 98 da fonte contemporânea. O feitiço pertence ao provider, com casting/mana/cooldown hospedados no Iron's. Black Arcana não reproduz o efeito.
- **Fonte factual:** [inventário](SPELL-CATALOG.md), [proveniência](EVIDENCE-AND-PROVENANCE.md), [limites de runtime](RUNTIME-AND-SAFETY.md).

### 48 — `ORBITAL_SNOWBALL`

- **Família organizacional na fonte:** `ice`; não comprova `SchoolType` individual.
- **Constante em `ModSpellRegistry`:** `ORBITAL_SNOWBALL`.
- **Classe da fonte pública:** `OrbitalSnowballSpell`.
- **Registry ID físico 0.0.16.3:** `NÃO VERIFICADO`. Não derivar namespace/path de campos ou nomes de classes.
- **Escola e configuração individual:** `NÃO VERIFICADO`; mesmo a escola Necro observada no source não prova a associação deste registro no binário instalado.
- **Custos, cooldown, level/rarity, targeting, efeito, dano/cura, summons, filtros PvP/boss, persistência, aquisição e world safety:** `NÃO VERIFICADO`. Nenhum desses mecanismos é inferido do nome.
- **Identidade semântica:** `COUNTED_RELEASE_BOUNDED`, já inventariada no lote de 98 da fonte contemporânea. O feitiço pertence ao provider, com casting/mana/cooldown hospedados no Iron's. Black Arcana não reproduz o efeito.
- **Fonte factual:** [inventário](SPELL-CATALOG.md), [proveniência](EVIDENCE-AND-PROVENANCE.md), [limites de runtime](RUNTIME-AND-SAFETY.md).

### 49 — `SUMMON_ICE_HYDRA`

- **Família organizacional na fonte:** `ice`; não comprova `SchoolType` individual.
- **Constante em `ModSpellRegistry`:** `SUMMON_ICE_HYDRA`.
- **Classe da fonte pública:** `SummonIceHydraSpell`.
- **Registry ID físico 0.0.16.3:** `NÃO VERIFICADO`. Não derivar namespace/path de campos ou nomes de classes.
- **Escola e configuração individual:** `NÃO VERIFICADO`; mesmo a escola Necro observada no source não prova a associação deste registro no binário instalado.
- **Custos, cooldown, level/rarity, targeting, efeito, dano/cura, summons, filtros PvP/boss, persistência, aquisição e world safety:** `NÃO VERIFICADO`. Nenhum desses mecanismos é inferido do nome.
- **Identidade semântica:** `COUNTED_RELEASE_BOUNDED`, já inventariada no lote de 98 da fonte contemporânea. O feitiço pertence ao provider, com casting/mana/cooldown hospedados no Iron's. Black Arcana não reproduz o efeito.
- **Fonte factual:** [inventário](SPELL-CATALOG.md), [proveniência](EVIDENCE-AND-PROVENANCE.md), [limites de runtime](RUNTIME-AND-SAFETY.md).

### 50 — `TUNDRA_TERRAIN`

- **Família organizacional na fonte:** `ice`; não comprova `SchoolType` individual.
- **Constante em `ModSpellRegistry`:** `TUNDRA_TERRAIN`.
- **Classe da fonte pública:** `TundraTerrainSpell`.
- **Registry ID físico 0.0.16.3:** `NÃO VERIFICADO`. Não derivar namespace/path de campos ou nomes de classes.
- **Escola e configuração individual:** `NÃO VERIFICADO`; mesmo a escola Necro observada no source não prova a associação deste registro no binário instalado.
- **Custos, cooldown, level/rarity, targeting, efeito, dano/cura, summons, filtros PvP/boss, persistência, aquisição e world safety:** `NÃO VERIFICADO`. Nenhum desses mecanismos é inferido do nome.
- **Identidade semântica:** `COUNTED_RELEASE_BOUNDED`, já inventariada no lote de 98 da fonte contemporânea. O feitiço pertence ao provider, com casting/mana/cooldown hospedados no Iron's. Black Arcana não reproduz o efeito.
- **Fonte factual:** [inventário](SPELL-CATALOG.md), [proveniência](EVIDENCE-AND-PROVENANCE.md), [limites de runtime](RUNTIME-AND-SAFETY.md).


## Família `lightning` — 14 registros

### 51 — `PRIMORDIAL_FLASH`

- **Família organizacional na fonte:** `lightning`; não comprova `SchoolType` individual.
- **Constante em `ModSpellRegistry`:** `PRIMORDIAL_FLASH`.
- **Classe da fonte pública:** `PrimordialFlashSpell`.
- **Registry ID físico 0.0.16.3:** `NÃO VERIFICADO`. Não derivar namespace/path de campos ou nomes de classes.
- **Escola e configuração individual:** `NÃO VERIFICADO`; mesmo a escola Necro observada no source não prova a associação deste registro no binário instalado.
- **Custos, cooldown, level/rarity, targeting, efeito, dano/cura, summons, filtros PvP/boss, persistência, aquisição e world safety:** `NÃO VERIFICADO`. Nenhum desses mecanismos é inferido do nome.
- **Identidade semântica:** `COUNTED_RELEASE_BOUNDED`, já inventariada no lote de 98 da fonte contemporânea. O feitiço pertence ao provider, com casting/mana/cooldown hospedados no Iron's. Black Arcana não reproduz o efeito.
- **Fonte factual:** [inventário](SPELL-CATALOG.md), [proveniência](EVIDENCE-AND-PROVENANCE.md), [limites de runtime](RUNTIME-AND-SAFETY.md).

### 52 — `DISCHARGE`

- **Família organizacional na fonte:** `lightning`; não comprova `SchoolType` individual.
- **Constante em `ModSpellRegistry`:** `DISCHARGE`.
- **Classe da fonte pública:** `DischargeSpell`.
- **Registry ID físico 0.0.16.3:** `NÃO VERIFICADO`. Não derivar namespace/path de campos ou nomes de classes.
- **Escola e configuração individual:** `NÃO VERIFICADO`; mesmo a escola Necro observada no source não prova a associação deste registro no binário instalado.
- **Custos, cooldown, level/rarity, targeting, efeito, dano/cura, summons, filtros PvP/boss, persistência, aquisição e world safety:** `NÃO VERIFICADO`. Nenhum desses mecanismos é inferido do nome.
- **Identidade semântica:** `COUNTED_RELEASE_BOUNDED`, já inventariada no lote de 98 da fonte contemporânea. O feitiço pertence ao provider, com casting/mana/cooldown hospedados no Iron's. Black Arcana não reproduz o efeito.
- **Fonte factual:** [inventário](SPELL-CATALOG.md), [proveniência](EVIDENCE-AND-PROVENANCE.md), [limites de runtime](RUNTIME-AND-SAFETY.md).

### 53 — `RAIJIN_JUDGEMENT`

- **Família organizacional na fonte:** `lightning`; não comprova `SchoolType` individual.
- **Constante em `ModSpellRegistry`:** `RAIJIN_JUDGEMENT`.
- **Classe da fonte pública:** `RaijinJudgementSpell`.
- **Registry ID físico 0.0.16.3:** `NÃO VERIFICADO`. Não derivar namespace/path de campos ou nomes de classes.
- **Escola e configuração individual:** `NÃO VERIFICADO`; mesmo a escola Necro observada no source não prova a associação deste registro no binário instalado.
- **Custos, cooldown, level/rarity, targeting, efeito, dano/cura, summons, filtros PvP/boss, persistência, aquisição e world safety:** `NÃO VERIFICADO`. Nenhum desses mecanismos é inferido do nome.
- **Identidade semântica:** `COUNTED_RELEASE_BOUNDED`, já inventariada no lote de 98 da fonte contemporânea. O feitiço pertence ao provider, com casting/mana/cooldown hospedados no Iron's. Black Arcana não reproduz o efeito.
- **Fonte factual:** [inventário](SPELL-CATALOG.md), [proveniência](EVIDENCE-AND-PROVENANCE.md), [limites de runtime](RUNTIME-AND-SAFETY.md).

### 54 — `REDSTONE_BOLT`

- **Família organizacional na fonte:** `lightning`; não comprova `SchoolType` individual.
- **Constante em `ModSpellRegistry`:** `REDSTONE_BOLT`.
- **Classe da fonte pública:** `RedstoneBoltSpell`.
- **Registry ID físico 0.0.16.3:** `NÃO VERIFICADO`. Não derivar namespace/path de campos ou nomes de classes.
- **Escola e configuração individual:** `NÃO VERIFICADO`; mesmo a escola Necro observada no source não prova a associação deste registro no binário instalado.
- **Custos, cooldown, level/rarity, targeting, efeito, dano/cura, summons, filtros PvP/boss, persistência, aquisição e world safety:** `NÃO VERIFICADO`. Nenhum desses mecanismos é inferido do nome.
- **Identidade semântica:** `COUNTED_RELEASE_BOUNDED`, já inventariada no lote de 98 da fonte contemporânea. O feitiço pertence ao provider, com casting/mana/cooldown hospedados no Iron's. Black Arcana não reproduz o efeito.
- **Fonte factual:** [inventário](SPELL-CATALOG.md), [proveniência](EVIDENCE-AND-PROVENANCE.md), [limites de runtime](RUNTIME-AND-SAFETY.md).

### 55 — `REDSTONE_MINES`

- **Família organizacional na fonte:** `lightning`; não comprova `SchoolType` individual.
- **Constante em `ModSpellRegistry`:** `REDSTONE_MINES`.
- **Classe da fonte pública:** `RedstoneMinesSpell`.
- **Registry ID físico 0.0.16.3:** `NÃO VERIFICADO`. Não derivar namespace/path de campos ou nomes de classes.
- **Escola e configuração individual:** `NÃO VERIFICADO`; mesmo a escola Necro observada no source não prova a associação deste registro no binário instalado.
- **Custos, cooldown, level/rarity, targeting, efeito, dano/cura, summons, filtros PvP/boss, persistência, aquisição e world safety:** `NÃO VERIFICADO`. Nenhum desses mecanismos é inferido do nome.
- **Identidade semântica:** `COUNTED_RELEASE_BOUNDED`, já inventariada no lote de 98 da fonte contemporânea. O feitiço pertence ao provider, com casting/mana/cooldown hospedados no Iron's. Black Arcana não reproduz o efeito.
- **Fonte factual:** [inventário](SPELL-CATALOG.md), [proveniência](EVIDENCE-AND-PROVENANCE.md), [limites de runtime](RUNTIME-AND-SAFETY.md).

### 56 — `GUARDIANS_NEUTRALIZER`

- **Família organizacional na fonte:** `lightning`; não comprova `SchoolType` individual.
- **Constante em `ModSpellRegistry`:** `GUARDIANS_NEUTRALIZER`.
- **Classe da fonte pública:** `GuardiansNeutralizerSpell`.
- **Registry ID físico 0.0.16.3:** `NÃO VERIFICADO`. Não derivar namespace/path de campos ou nomes de classes.
- **Escola e configuração individual:** `NÃO VERIFICADO`; mesmo a escola Necro observada no source não prova a associação deste registro no binário instalado.
- **Custos, cooldown, level/rarity, targeting, efeito, dano/cura, summons, filtros PvP/boss, persistência, aquisição e world safety:** `NÃO VERIFICADO`. Nenhum desses mecanismos é inferido do nome.
- **Identidade semântica:** `COUNTED_RELEASE_BOUNDED`, já inventariada no lote de 98 da fonte contemporânea. O feitiço pertence ao provider, com casting/mana/cooldown hospedados no Iron's. Black Arcana não reproduz o efeito.
- **Fonte factual:** [inventário](SPELL-CATALOG.md), [proveniência](EVIDENCE-AND-PROVENANCE.md), [limites de runtime](RUNTIME-AND-SAFETY.md).

### 57 — `REDSTONE_CHAIN`

- **Família organizacional na fonte:** `lightning`; não comprova `SchoolType` individual.
- **Constante em `ModSpellRegistry`:** `REDSTONE_CHAIN`.
- **Classe da fonte pública:** `RedstoneChainSpell`.
- **Registry ID físico 0.0.16.3:** `NÃO VERIFICADO`. Não derivar namespace/path de campos ou nomes de classes.
- **Escola e configuração individual:** `NÃO VERIFICADO`; mesmo a escola Necro observada no source não prova a associação deste registro no binário instalado.
- **Custos, cooldown, level/rarity, targeting, efeito, dano/cura, summons, filtros PvP/boss, persistência, aquisição e world safety:** `NÃO VERIFICADO`. Nenhum desses mecanismos é inferido do nome.
- **Identidade semântica:** `COUNTED_RELEASE_BOUNDED`, já inventariada no lote de 98 da fonte contemporânea. O feitiço pertence ao provider, com casting/mana/cooldown hospedados no Iron's. Black Arcana não reproduz o efeito.
- **Fonte factual:** [inventário](SPELL-CATALOG.md), [proveniência](EVIDENCE-AND-PROVENANCE.md), [limites de runtime](RUNTIME-AND-SAFETY.md).

### 58 — `REDSTONE_LASERS`

- **Família organizacional na fonte:** `lightning`; não comprova `SchoolType` individual.
- **Constante em `ModSpellRegistry`:** `REDSTONE_LASERS`.
- **Classe da fonte pública:** `RedstoneLasersSpell`.
- **Registry ID físico 0.0.16.3:** `NÃO VERIFICADO`. Não derivar namespace/path de campos ou nomes de classes.
- **Escola e configuração individual:** `NÃO VERIFICADO`; mesmo a escola Necro observada no source não prova a associação deste registro no binário instalado.
- **Custos, cooldown, level/rarity, targeting, efeito, dano/cura, summons, filtros PvP/boss, persistência, aquisição e world safety:** `NÃO VERIFICADO`. Nenhum desses mecanismos é inferido do nome.
- **Identidade semântica:** `COUNTED_RELEASE_BOUNDED`, já inventariada no lote de 98 da fonte contemporânea. O feitiço pertence ao provider, com casting/mana/cooldown hospedados no Iron's. Black Arcana não reproduz o efeito.
- **Fonte factual:** [inventário](SPELL-CATALOG.md), [proveniência](EVIDENCE-AND-PROVENANCE.md), [limites de runtime](RUNTIME-AND-SAFETY.md).

### 59 — `RAIGO`

- **Família organizacional na fonte:** `lightning`; não comprova `SchoolType` individual.
- **Constante em `ModSpellRegistry`:** `RAIGO`.
- **Classe da fonte pública:** `RaigoSpell`.
- **Registry ID físico 0.0.16.3:** `NÃO VERIFICADO`. Não derivar namespace/path de campos ou nomes de classes.
- **Escola e configuração individual:** `NÃO VERIFICADO`; mesmo a escola Necro observada no source não prova a associação deste registro no binário instalado.
- **Custos, cooldown, level/rarity, targeting, efeito, dano/cura, summons, filtros PvP/boss, persistência, aquisição e world safety:** `NÃO VERIFICADO`. Nenhum desses mecanismos é inferido do nome.
- **Identidade semântica:** `COUNTED_RELEASE_BOUNDED`, já inventariada no lote de 98 da fonte contemporânea. O feitiço pertence ao provider, com casting/mana/cooldown hospedados no Iron's. Black Arcana não reproduz o efeito.
- **Fonte factual:** [inventário](SPELL-CATALOG.md), [proveniência](EVIDENCE-AND-PROVENANCE.md), [limites de runtime](RUNTIME-AND-SAFETY.md).

### 60 — `STATIC_CLEAVE`

- **Família organizacional na fonte:** `lightning`; não comprova `SchoolType` individual.
- **Constante em `ModSpellRegistry`:** `STATIC_CLEAVE`.
- **Classe da fonte pública:** `StaticCleaveSpell`.
- **Registry ID físico 0.0.16.3:** `NÃO VERIFICADO`. Não derivar namespace/path de campos ou nomes de classes.
- **Escola e configuração individual:** `NÃO VERIFICADO`; mesmo a escola Necro observada no source não prova a associação deste registro no binário instalado.
- **Custos, cooldown, level/rarity, targeting, efeito, dano/cura, summons, filtros PvP/boss, persistência, aquisição e world safety:** `NÃO VERIFICADO`. Nenhum desses mecanismos é inferido do nome.
- **Identidade semântica:** `COUNTED_RELEASE_BOUNDED`, já inventariada no lote de 98 da fonte contemporânea. O feitiço pertence ao provider, com casting/mana/cooldown hospedados no Iron's. Black Arcana não reproduz o efeito.
- **Fonte factual:** [inventário](SPELL-CATALOG.md), [proveniência](EVIDENCE-AND-PROVENANCE.md), [limites de runtime](RUNTIME-AND-SAFETY.md).

### 61 — `THUNDER_STEP`

- **Família organizacional na fonte:** `lightning`; não comprova `SchoolType` individual.
- **Constante em `ModSpellRegistry`:** `THUNDER_STEP`.
- **Classe da fonte pública:** `ThunderStepSpell`.
- **Registry ID físico 0.0.16.3:** `NÃO VERIFICADO`. Não derivar namespace/path de campos ou nomes de classes.
- **Escola e configuração individual:** `NÃO VERIFICADO`; mesmo a escola Necro observada no source não prova a associação deste registro no binário instalado.
- **Custos, cooldown, level/rarity, targeting, efeito, dano/cura, summons, filtros PvP/boss, persistência, aquisição e world safety:** `NÃO VERIFICADO`. Nenhum desses mecanismos é inferido do nome.
- **Identidade semântica:** `COUNTED_RELEASE_BOUNDED`, já inventariada no lote de 98 da fonte contemporânea. O feitiço pertence ao provider, com casting/mana/cooldown hospedados no Iron's. Black Arcana não reproduz o efeito.
- **Fonte factual:** [inventário](SPELL-CATALOG.md), [proveniência](EVIDENCE-AND-PROVENANCE.md), [limites de runtime](RUNTIME-AND-SAFETY.md).

### 62 — `THUNDERSTORM_WAVE`

- **Família organizacional na fonte:** `lightning`; não comprova `SchoolType` individual.
- **Constante em `ModSpellRegistry`:** `THUNDERSTORM_WAVE`.
- **Classe da fonte pública:** `ThunderstormWaveSpell`.
- **Registry ID físico 0.0.16.3:** `NÃO VERIFICADO`. Não derivar namespace/path de campos ou nomes de classes.
- **Escola e configuração individual:** `NÃO VERIFICADO`; mesmo a escola Necro observada no source não prova a associação deste registro no binário instalado.
- **Custos, cooldown, level/rarity, targeting, efeito, dano/cura, summons, filtros PvP/boss, persistência, aquisição e world safety:** `NÃO VERIFICADO`. Nenhum desses mecanismos é inferido do nome.
- **Identidade semântica:** `COUNTED_RELEASE_BOUNDED`, já inventariada no lote de 98 da fonte contemporânea. O feitiço pertence ao provider, com casting/mana/cooldown hospedados no Iron's. Black Arcana não reproduz o efeito.
- **Fonte factual:** [inventário](SPELL-CATALOG.md), [proveniência](EVIDENCE-AND-PROVENANCE.md), [limites de runtime](RUNTIME-AND-SAFETY.md).

### 63 — `VOLTAIC_MULTISHOT`

- **Família organizacional na fonte:** `lightning`; não comprova `SchoolType` individual.
- **Constante em `ModSpellRegistry`:** `VOLTAIC_MULTISHOT`.
- **Classe da fonte pública:** `VoltaicMultishotSpell`.
- **Registry ID físico 0.0.16.3:** `NÃO VERIFICADO`. Não derivar namespace/path de campos ou nomes de classes.
- **Escola e configuração individual:** `NÃO VERIFICADO`; mesmo a escola Necro observada no source não prova a associação deste registro no binário instalado.
- **Custos, cooldown, level/rarity, targeting, efeito, dano/cura, summons, filtros PvP/boss, persistência, aquisição e world safety:** `NÃO VERIFICADO`. Nenhum desses mecanismos é inferido do nome.
- **Identidade semântica:** `COUNTED_RELEASE_BOUNDED`, já inventariada no lote de 98 da fonte contemporânea. O feitiço pertence ao provider, com casting/mana/cooldown hospedados no Iron's. Black Arcana não reproduz o efeito.
- **Fonte factual:** [inventário](SPELL-CATALOG.md), [proveniência](EVIDENCE-AND-PROVENANCE.md), [limites de runtime](RUNTIME-AND-SAFETY.md).

### 64 — `ZAP`

- **Família organizacional na fonte:** `lightning`; não comprova `SchoolType` individual.
- **Constante em `ModSpellRegistry`:** `ZAP`.
- **Classe da fonte pública:** `ZapSpell`.
- **Registry ID físico 0.0.16.3:** `NÃO VERIFICADO`. Não derivar namespace/path de campos ou nomes de classes.
- **Escola e configuração individual:** `NÃO VERIFICADO`; mesmo a escola Necro observada no source não prova a associação deste registro no binário instalado.
- **Custos, cooldown, level/rarity, targeting, efeito, dano/cura, summons, filtros PvP/boss, persistência, aquisição e world safety:** `NÃO VERIFICADO`. Nenhum desses mecanismos é inferido do nome.
- **Identidade semântica:** `COUNTED_RELEASE_BOUNDED`, já inventariada no lote de 98 da fonte contemporânea. O feitiço pertence ao provider, com casting/mana/cooldown hospedados no Iron's. Black Arcana não reproduz o efeito.
- **Fonte factual:** [inventário](SPELL-CATALOG.md), [proveniência](EVIDENCE-AND-PROVENANCE.md), [limites de runtime](RUNTIME-AND-SAFETY.md).


## Família `nature` — 7 registros

### 65 — `BLAST_FUNGUS`

- **Família organizacional na fonte:** `nature`; não comprova `SchoolType` individual.
- **Constante em `ModSpellRegistry`:** `BLAST_FUNGUS`.
- **Classe da fonte pública:** `BlastFungusSpell`.
- **Registry ID físico 0.0.16.3:** `NÃO VERIFICADO`. Não derivar namespace/path de campos ou nomes de classes.
- **Escola e configuração individual:** `NÃO VERIFICADO`; mesmo a escola Necro observada no source não prova a associação deste registro no binário instalado.
- **Custos, cooldown, level/rarity, targeting, efeito, dano/cura, summons, filtros PvP/boss, persistência, aquisição e world safety:** `NÃO VERIFICADO`. Nenhum desses mecanismos é inferido do nome.
- **Identidade semântica:** `COUNTED_RELEASE_BOUNDED`, já inventariada no lote de 98 da fonte contemporânea. O feitiço pertence ao provider, com casting/mana/cooldown hospedados no Iron's. Black Arcana não reproduz o efeito.
- **Fonte factual:** [inventário](SPELL-CATALOG.md), [proveniência](EVIDENCE-AND-PROVENANCE.md), [limites de runtime](RUNTIME-AND-SAFETY.md).

### 66 — `INFECTION_SLASH`

- **Família organizacional na fonte:** `nature`; não comprova `SchoolType` individual.
- **Constante em `ModSpellRegistry`:** `INFECTION_SLASH`.
- **Classe da fonte pública:** `InfectionSlashSpell`.
- **Registry ID físico 0.0.16.3:** `NÃO VERIFICADO`. Não derivar namespace/path de campos ou nomes de classes.
- **Escola e configuração individual:** `NÃO VERIFICADO`; mesmo a escola Necro observada no source não prova a associação deste registro no binário instalado.
- **Custos, cooldown, level/rarity, targeting, efeito, dano/cura, summons, filtros PvP/boss, persistência, aquisição e world safety:** `NÃO VERIFICADO`. Nenhum desses mecanismos é inferido do nome.
- **Identidade semântica:** `COUNTED_RELEASE_BOUNDED`, já inventariada no lote de 98 da fonte contemporânea. O feitiço pertence ao provider, com casting/mana/cooldown hospedados no Iron's. Black Arcana não reproduz o efeito.
- **Fonte factual:** [inventário](SPELL-CATALOG.md), [proveniência](EVIDENCE-AND-PROVENANCE.md), [limites de runtime](RUNTIME-AND-SAFETY.md).

### 67 — `LEAF_CRYSTAL`

- **Família organizacional na fonte:** `nature`; não comprova `SchoolType` individual.
- **Constante em `ModSpellRegistry`:** `LEAF_CRYSTAL`.
- **Classe da fonte pública:** `LifeCrystalSpell`.
- **Registry ID físico 0.0.16.3:** `NÃO VERIFICADO`. Não derivar namespace/path de campos ou nomes de classes.
- **Escola e configuração individual:** `NÃO VERIFICADO`; mesmo a escola Necro observada no source não prova a associação deste registro no binário instalado.
- **Custos, cooldown, level/rarity, targeting, efeito, dano/cura, summons, filtros PvP/boss, persistência, aquisição e world safety:** `NÃO VERIFICADO`. Nenhum desses mecanismos é inferido do nome.
- **Identidade semântica:** `COUNTED_RELEASE_BOUNDED`, já inventariada no lote de 98 da fonte contemporânea. O feitiço pertence ao provider, com casting/mana/cooldown hospedados no Iron's. Black Arcana não reproduz o efeito.
- **Fonte factual:** [inventário](SPELL-CATALOG.md), [proveniência](EVIDENCE-AND-PROVENANCE.md), [limites de runtime](RUNTIME-AND-SAFETY.md).

### 68 — `POISON_QUILL`

- **Família organizacional na fonte:** `nature`; não comprova `SchoolType` individual.
- **Constante em `ModSpellRegistry`:** `POISON_QUILL`.
- **Classe da fonte pública:** `PoisonQuillSpell`.
- **Registry ID físico 0.0.16.3:** `NÃO VERIFICADO`. Não derivar namespace/path de campos ou nomes de classes.
- **Escola e configuração individual:** `NÃO VERIFICADO`; mesmo a escola Necro observada no source não prova a associação deste registro no binário instalado.
- **Custos, cooldown, level/rarity, targeting, efeito, dano/cura, summons, filtros PvP/boss, persistência, aquisição e world safety:** `NÃO VERIFICADO`. Nenhum desses mecanismos é inferido do nome.
- **Identidade semântica:** `COUNTED_RELEASE_BOUNDED`, já inventariada no lote de 98 da fonte contemporânea. O feitiço pertence ao provider, com casting/mana/cooldown hospedados no Iron's. Black Arcana não reproduz o efeito.
- **Fonte factual:** [inventário](SPELL-CATALOG.md), [proveniência](EVIDENCE-AND-PROVENANCE.md), [limites de runtime](RUNTIME-AND-SAFETY.md).

### 69 — `SPIDER_FANGS`

- **Família organizacional na fonte:** `nature`; não comprova `SchoolType` individual.
- **Constante em `ModSpellRegistry`:** `SPIDER_FANGS`.
- **Classe da fonte pública:** `SpiderFangsSpell`.
- **Registry ID físico 0.0.16.3:** `NÃO VERIFICADO`. Não derivar namespace/path de campos ou nomes de classes.
- **Escola e configuração individual:** `NÃO VERIFICADO`; mesmo a escola Necro observada no source não prova a associação deste registro no binário instalado.
- **Custos, cooldown, level/rarity, targeting, efeito, dano/cura, summons, filtros PvP/boss, persistência, aquisição e world safety:** `NÃO VERIFICADO`. Nenhum desses mecanismos é inferido do nome.
- **Identidade semântica:** `COUNTED_RELEASE_BOUNDED`, já inventariada no lote de 98 da fonte contemporânea. O feitiço pertence ao provider, com casting/mana/cooldown hospedados no Iron's. Black Arcana não reproduz o efeito.
- **Fonte factual:** [inventário](SPELL-CATALOG.md), [proveniência](EVIDENCE-AND-PROVENANCE.md), [limites de runtime](RUNTIME-AND-SAFETY.md).

### 70 — `SUMMON_POISON_VINE`

- **Família organizacional na fonte:** `nature`; não comprova `SchoolType` individual.
- **Constante em `ModSpellRegistry`:** `SUMMON_POISON_VINE`.
- **Classe da fonte pública:** `SummonPoisonVinesSpell`.
- **Registry ID físico 0.0.16.3:** `NÃO VERIFICADO`. Não derivar namespace/path de campos ou nomes de classes.
- **Escola e configuração individual:** `NÃO VERIFICADO`; mesmo a escola Necro observada no source não prova a associação deste registro no binário instalado.
- **Custos, cooldown, level/rarity, targeting, efeito, dano/cura, summons, filtros PvP/boss, persistência, aquisição e world safety:** `NÃO VERIFICADO`. Nenhum desses mecanismos é inferido do nome.
- **Identidade semântica:** `COUNTED_RELEASE_BOUNDED`, já inventariada no lote de 98 da fonte contemporânea. O feitiço pertence ao provider, com casting/mana/cooldown hospedados no Iron's. Black Arcana não reproduz o efeito.
- **Fonte factual:** [inventário](SPELL-CATALOG.md), [proveniência](EVIDENCE-AND-PROVENANCE.md), [limites de runtime](RUNTIME-AND-SAFETY.md).

### 71 — `VITAL_BLAST`

- **Família organizacional na fonte:** `nature`; não comprova `SchoolType` individual.
- **Constante em `ModSpellRegistry`:** `VITAL_BLAST`.
- **Classe da fonte pública:** `VitalBlastSpell`.
- **Registry ID físico 0.0.16.3:** `NÃO VERIFICADO`. Não derivar namespace/path de campos ou nomes de classes.
- **Escola e configuração individual:** `NÃO VERIFICADO`; mesmo a escola Necro observada no source não prova a associação deste registro no binário instalado.
- **Custos, cooldown, level/rarity, targeting, efeito, dano/cura, summons, filtros PvP/boss, persistência, aquisição e world safety:** `NÃO VERIFICADO`. Nenhum desses mecanismos é inferido do nome.
- **Identidade semântica:** `COUNTED_RELEASE_BOUNDED`, já inventariada no lote de 98 da fonte contemporânea. O feitiço pertence ao provider, com casting/mana/cooldown hospedados no Iron's. Black Arcana não reproduz o efeito.
- **Fonte factual:** [inventário](SPELL-CATALOG.md), [proveniência](EVIDENCE-AND-PROVENANCE.md), [limites de runtime](RUNTIME-AND-SAFETY.md).


## Família `necro` — 25 registros

### 72 — `REAPER_ASPECT`

- **Família organizacional na fonte:** `necro`; não comprova `SchoolType` individual.
- **Constante em `ModSpellRegistry`:** `REAPER_ASPECT`.
- **Classe da fonte pública:** `ReaperAspectSpell`.
- **Registry ID físico 0.0.16.3:** `NÃO VERIFICADO`. Não derivar namespace/path de campos ou nomes de classes.
- **Escola e configuração individual:** `NÃO VERIFICADO`; mesmo a escola Necro observada no source não prova a associação deste registro no binário instalado.
- **Custos, cooldown, level/rarity, targeting, efeito, dano/cura, summons, filtros PvP/boss, persistência, aquisição e world safety:** `NÃO VERIFICADO`. Nenhum desses mecanismos é inferido do nome.
- **Identidade semântica:** `COUNTED_RELEASE_BOUNDED`, já inventariada no lote de 98 da fonte contemporânea. O feitiço pertence ao provider, com casting/mana/cooldown hospedados no Iron's. Black Arcana não reproduz o efeito.
- **Fonte factual:** [inventário](SPELL-CATALOG.md), [proveniência](EVIDENCE-AND-PROVENANCE.md), [limites de runtime](RUNTIME-AND-SAFETY.md).

### 73 — `BANSHEE_SCREAM`

- **Família organizacional na fonte:** `necro`; não comprova `SchoolType` individual.
- **Constante em `ModSpellRegistry`:** `BANSHEE_SCREAM`.
- **Classe da fonte pública:** `BansheeScreamSpell`.
- **Registry ID físico 0.0.16.3:** `NÃO VERIFICADO`. Não derivar namespace/path de campos ou nomes de classes.
- **Escola e configuração individual:** `NÃO VERIFICADO`; mesmo a escola Necro observada no source não prova a associação deste registro no binário instalado.
- **Custos, cooldown, level/rarity, targeting, efeito, dano/cura, summons, filtros PvP/boss, persistência, aquisição e world safety:** `NÃO VERIFICADO`. Nenhum desses mecanismos é inferido do nome.
- **Identidade semântica:** `COUNTED_RELEASE_BOUNDED`, já inventariada no lote de 98 da fonte contemporânea. O feitiço pertence ao provider, com casting/mana/cooldown hospedados no Iron's. Black Arcana não reproduz o efeito.
- **Fonte factual:** [inventário](SPELL-CATALOG.md), [proveniência](EVIDENCE-AND-PROVENANCE.md), [limites de runtime](RUNTIME-AND-SAFETY.md).

### 74 — `BONE_DAGGER`

- **Família organizacional na fonte:** `necro`; não comprova `SchoolType` individual.
- **Constante em `ModSpellRegistry`:** `BONE_DAGGER`.
- **Classe da fonte pública:** `BoneDaggerSpell`.
- **Registry ID físico 0.0.16.3:** `NÃO VERIFICADO`. Não derivar namespace/path de campos ou nomes de classes.
- **Escola e configuração individual:** `NÃO VERIFICADO`; mesmo a escola Necro observada no source não prova a associação deste registro no binário instalado.
- **Custos, cooldown, level/rarity, targeting, efeito, dano/cura, summons, filtros PvP/boss, persistência, aquisição e world safety:** `NÃO VERIFICADO`. Nenhum desses mecanismos é inferido do nome.
- **Identidade semântica:** `COUNTED_RELEASE_BOUNDED`, já inventariada no lote de 98 da fonte contemporânea. O feitiço pertence ao provider, com casting/mana/cooldown hospedados no Iron's. Black Arcana não reproduz o efeito.
- **Fonte factual:** [inventário](SPELL-CATALOG.md), [proveniência](EVIDENCE-AND-PROVENANCE.md), [limites de runtime](RUNTIME-AND-SAFETY.md).

### 75 — `SUMMON_DEATH_KNIGHT`

- **Família organizacional na fonte:** `necro`; não comprova `SchoolType` individual.
- **Constante em `ModSpellRegistry`:** `SUMMON_DEATH_KNIGHT`.
- **Classe da fonte pública:** `SummonDeathKnightSpell`.
- **Registry ID físico 0.0.16.3:** `NÃO VERIFICADO`. Não derivar namespace/path de campos ou nomes de classes.
- **Escola e configuração individual:** `NÃO VERIFICADO`; mesmo a escola Necro observada no source não prova a associação deste registro no binário instalado.
- **Custos, cooldown, level/rarity, targeting, efeito, dano/cura, summons, filtros PvP/boss, persistência, aquisição e world safety:** `NÃO VERIFICADO`. Nenhum desses mecanismos é inferido do nome.
- **Identidade semântica:** `COUNTED_RELEASE_BOUNDED`, já inventariada no lote de 98 da fonte contemporânea. O feitiço pertence ao provider, com casting/mana/cooldown hospedados no Iron's. Black Arcana não reproduz o efeito.
- **Fonte factual:** [inventário](SPELL-CATALOG.md), [proveniência](EVIDENCE-AND-PROVENANCE.md), [limites de runtime](RUNTIME-AND-SAFETY.md).

### 76 — `FALL_CURSE`

- **Família organizacional na fonte:** `necro`; não comprova `SchoolType` individual.
- **Constante em `ModSpellRegistry`:** `FALL_CURSE`.
- **Classe da fonte pública:** `FallCurseSpell`.
- **Registry ID físico 0.0.16.3:** `NÃO VERIFICADO`. Não derivar namespace/path de campos ou nomes de classes.
- **Escola e configuração individual:** `NÃO VERIFICADO`; mesmo a escola Necro observada no source não prova a associação deste registro no binário instalado.
- **Custos, cooldown, level/rarity, targeting, efeito, dano/cura, summons, filtros PvP/boss, persistência, aquisição e world safety:** `NÃO VERIFICADO`. Nenhum desses mecanismos é inferido do nome.
- **Identidade semântica:** `COUNTED_RELEASE_BOUNDED`, já inventariada no lote de 98 da fonte contemporânea. O feitiço pertence ao provider, com casting/mana/cooldown hospedados no Iron's. Black Arcana não reproduz o efeito.
- **Fonte factual:** [inventário](SPELL-CATALOG.md), [proveniência](EVIDENCE-AND-PROVENANCE.md), [limites de runtime](RUNTIME-AND-SAFETY.md).

### 77 — `GRAVEYARD_FISSURE`

- **Família organizacional na fonte:** `necro`; não comprova `SchoolType` individual.
- **Constante em `ModSpellRegistry`:** `GRAVEYARD_FISSURE`.
- **Classe da fonte pública:** `GraveyardFissureSpell`.
- **Registry ID físico 0.0.16.3:** `NÃO VERIFICADO`. Não derivar namespace/path de campos ou nomes de classes.
- **Escola e configuração individual:** `NÃO VERIFICADO`; mesmo a escola Necro observada no source não prova a associação deste registro no binário instalado.
- **Custos, cooldown, level/rarity, targeting, efeito, dano/cura, summons, filtros PvP/boss, persistência, aquisição e world safety:** `NÃO VERIFICADO`. Nenhum desses mecanismos é inferido do nome.
- **Identidade semântica:** `COUNTED_RELEASE_BOUNDED`, já inventariada no lote de 98 da fonte contemporânea. O feitiço pertence ao provider, com casting/mana/cooldown hospedados no Iron's. Black Arcana não reproduz o efeito.
- **Fonte factual:** [inventário](SPELL-CATALOG.md), [proveniência](EVIDENCE-AND-PROVENANCE.md), [limites de runtime](RUNTIME-AND-SAFETY.md).

### 78 — `LICHDOM`

- **Família organizacional na fonte:** `necro`; não comprova `SchoolType` individual.
- **Constante em `ModSpellRegistry`:** `LICHDOM`.
- **Classe da fonte pública:** `LichdomSpell`.
- **Registry ID físico 0.0.16.3:** `NÃO VERIFICADO`. Não derivar namespace/path de campos ou nomes de classes.
- **Escola e configuração individual:** `NÃO VERIFICADO`; mesmo a escola Necro observada no source não prova a associação deste registro no binário instalado.
- **Custos, cooldown, level/rarity, targeting, efeito, dano/cura, summons, filtros PvP/boss, persistência, aquisição e world safety:** `NÃO VERIFICADO`. Nenhum desses mecanismos é inferido do nome.
- **Identidade semântica:** `COUNTED_RELEASE_BOUNDED`, já inventariada no lote de 98 da fonte contemporânea. O feitiço pertence ao provider, com casting/mana/cooldown hospedados no Iron's. Black Arcana não reproduz o efeito.
- **Fonte factual:** [inventário](SPELL-CATALOG.md), [proveniência](EVIDENCE-AND-PROVENANCE.md), [limites de runtime](RUNTIME-AND-SAFETY.md).

### 79 — `LIFE_DRAIN`

- **Família organizacional na fonte:** `necro`; não comprova `SchoolType` individual.
- **Constante em `ModSpellRegistry`:** `LIFE_DRAIN`.
- **Classe da fonte pública:** `LifeDrainSpell`.
- **Registry ID físico 0.0.16.3:** `NÃO VERIFICADO`. Não derivar namespace/path de campos ou nomes de classes.
- **Escola e configuração individual:** `NÃO VERIFICADO`; mesmo a escola Necro observada no source não prova a associação deste registro no binário instalado.
- **Custos, cooldown, level/rarity, targeting, efeito, dano/cura, summons, filtros PvP/boss, persistência, aquisição e world safety:** `NÃO VERIFICADO`. Nenhum desses mecanismos é inferido do nome.
- **Identidade semântica:** `COUNTED_RELEASE_BOUNDED`, já inventariada no lote de 98 da fonte contemporânea. O feitiço pertence ao provider, com casting/mana/cooldown hospedados no Iron's. Black Arcana não reproduz o efeito.
- **Fonte factual:** [inventário](SPELL-CATALOG.md), [proveniência](EVIDENCE-AND-PROVENANCE.md), [limites de runtime](RUNTIME-AND-SAFETY.md).

### 80 — `PUTRESCENCE_MASS`

- **Família organizacional na fonte:** `necro`; não comprova `SchoolType` individual.
- **Constante em `ModSpellRegistry`:** `PUTRESCENCE_MASS`.
- **Classe da fonte pública:** `PutrescenceMassSpell`.
- **Registry ID físico 0.0.16.3:** `NÃO VERIFICADO`. Não derivar namespace/path de campos ou nomes de classes.
- **Escola e configuração individual:** `NÃO VERIFICADO`; mesmo a escola Necro observada no source não prova a associação deste registro no binário instalado.
- **Custos, cooldown, level/rarity, targeting, efeito, dano/cura, summons, filtros PvP/boss, persistência, aquisição e world safety:** `NÃO VERIFICADO`. Nenhum desses mecanismos é inferido do nome.
- **Identidade semântica:** `COUNTED_RELEASE_BOUNDED`, já inventariada no lote de 98 da fonte contemporânea. O feitiço pertence ao provider, com casting/mana/cooldown hospedados no Iron's. Black Arcana não reproduz o efeito.
- **Fonte factual:** [inventário](SPELL-CATALOG.md), [proveniência](EVIDENCE-AND-PROVENANCE.md), [limites de runtime](RUNTIME-AND-SAFETY.md).

### 81 — `RANCORCALL`

- **Família organizacional na fonte:** `necro`; não comprova `SchoolType` individual.
- **Constante em `ModSpellRegistry`:** `RANCORCALL`.
- **Classe da fonte pública:** `RancorCallSpell`.
- **Registry ID físico 0.0.16.3:** `NÃO VERIFICADO`. Não derivar namespace/path de campos ou nomes de classes.
- **Escola e configuração individual:** `NÃO VERIFICADO`; mesmo a escola Necro observada no source não prova a associação deste registro no binário instalado.
- **Custos, cooldown, level/rarity, targeting, efeito, dano/cura, summons, filtros PvP/boss, persistência, aquisição e world safety:** `NÃO VERIFICADO`. Nenhum desses mecanismos é inferido do nome.
- **Identidade semântica:** `COUNTED_RELEASE_BOUNDED`, já inventariada no lote de 98 da fonte contemporânea. O feitiço pertence ao provider, com casting/mana/cooldown hospedados no Iron's. Black Arcana não reproduz o efeito.
- **Fonte factual:** [inventário](SPELL-CATALOG.md), [proveniência](EVIDENCE-AND-PROVENANCE.md), [limites de runtime](RUNTIME-AND-SAFETY.md).

### 82 — `SOUL_CASTING_FIELD`

- **Família organizacional na fonte:** `necro`; não comprova `SchoolType` individual.
- **Constante em `ModSpellRegistry`:** `SOUL_CASTING_FIELD`.
- **Classe da fonte pública:** `SoulCastingFieldSpell`.
- **Registry ID físico 0.0.16.3:** `NÃO VERIFICADO`. Não derivar namespace/path de campos ou nomes de classes.
- **Escola e configuração individual:** `NÃO VERIFICADO`; mesmo a escola Necro observada no source não prova a associação deste registro no binário instalado.
- **Custos, cooldown, level/rarity, targeting, efeito, dano/cura, summons, filtros PvP/boss, persistência, aquisição e world safety:** `NÃO VERIFICADO`. Nenhum desses mecanismos é inferido do nome.
- **Identidade semântica:** `COUNTED_RELEASE_BOUNDED`, já inventariada no lote de 98 da fonte contemporânea. O feitiço pertence ao provider, com casting/mana/cooldown hospedados no Iron's. Black Arcana não reproduz o efeito.
- **Fonte factual:** [inventário](SPELL-CATALOG.md), [proveniência](EVIDENCE-AND-PROVENANCE.md), [limites de runtime](RUNTIME-AND-SAFETY.md).

### 83 — `SOUL_CHAIN`

- **Família organizacional na fonte:** `necro`; não comprova `SchoolType` individual.
- **Constante em `ModSpellRegistry`:** `SOUL_CHAIN`.
- **Classe da fonte pública:** `SoulChainSpell`.
- **Registry ID físico 0.0.16.3:** `NÃO VERIFICADO`. Não derivar namespace/path de campos ou nomes de classes.
- **Escola e configuração individual:** `NÃO VERIFICADO`; mesmo a escola Necro observada no source não prova a associação deste registro no binário instalado.
- **Custos, cooldown, level/rarity, targeting, efeito, dano/cura, summons, filtros PvP/boss, persistência, aquisição e world safety:** `NÃO VERIFICADO`. Nenhum desses mecanismos é inferido do nome.
- **Identidade semântica:** `COUNTED_RELEASE_BOUNDED`, já inventariada no lote de 98 da fonte contemporânea. O feitiço pertence ao provider, com casting/mana/cooldown hospedados no Iron's. Black Arcana não reproduz o efeito.
- **Fonte factual:** [inventário](SPELL-CATALOG.md), [proveniência](EVIDENCE-AND-PROVENANCE.md), [limites de runtime](RUNTIME-AND-SAFETY.md).

### 84 — `SOUL_FIREBOLT`

- **Família organizacional na fonte:** `necro`; não comprova `SchoolType` individual.
- **Constante em `ModSpellRegistry`:** `SOUL_FIREBOLT`.
- **Classe da fonte pública:** `SoulFireBoltSpell`.
- **Registry ID físico 0.0.16.3:** `NÃO VERIFICADO`. Não derivar namespace/path de campos ou nomes de classes.
- **Escola e configuração individual:** `NÃO VERIFICADO`; mesmo a escola Necro observada no source não prova a associação deste registro no binário instalado.
- **Custos, cooldown, level/rarity, targeting, efeito, dano/cura, summons, filtros PvP/boss, persistência, aquisição e world safety:** `NÃO VERIFICADO`. Nenhum desses mecanismos é inferido do nome.
- **Identidade semântica:** `COUNTED_RELEASE_BOUNDED`, já inventariada no lote de 98 da fonte contemporânea. O feitiço pertence ao provider, com casting/mana/cooldown hospedados no Iron's. Black Arcana não reproduz o efeito.
- **Fonte factual:** [inventário](SPELL-CATALOG.md), [proveniência](EVIDENCE-AND-PROVENANCE.md), [limites de runtime](RUNTIME-AND-SAFETY.md).

### 85 — `SOUL_FIRE_TELEPORT`

- **Família organizacional na fonte:** `necro`; não comprova `SchoolType` individual.
- **Constante em `ModSpellRegistry`:** `SOUL_FIRE_TELEPORT`.
- **Classe da fonte pública:** `SoulFireTeleportSpell`.
- **Registry ID físico 0.0.16.3:** `NÃO VERIFICADO`. Não derivar namespace/path de campos ou nomes de classes.
- **Escola e configuração individual:** `NÃO VERIFICADO`; mesmo a escola Necro observada no source não prova a associação deste registro no binário instalado.
- **Custos, cooldown, level/rarity, targeting, efeito, dano/cura, summons, filtros PvP/boss, persistência, aquisição e world safety:** `NÃO VERIFICADO`. Nenhum desses mecanismos é inferido do nome.
- **Identidade semântica:** `COUNTED_RELEASE_BOUNDED`, já inventariada no lote de 98 da fonte contemporânea. O feitiço pertence ao provider, com casting/mana/cooldown hospedados no Iron's. Black Arcana não reproduz o efeito.
- **Fonte factual:** [inventário](SPELL-CATALOG.md), [proveniência](EVIDENCE-AND-PROVENANCE.md), [limites de runtime](RUNTIME-AND-SAFETY.md).

### 86 — `SOUL_FORM`

- **Família organizacional na fonte:** `necro`; não comprova `SchoolType` individual.
- **Constante em `ModSpellRegistry`:** `SOUL_FORM`.
- **Classe da fonte pública:** `SoulFormSpell`.
- **Registry ID físico 0.0.16.3:** `NÃO VERIFICADO`. Não derivar namespace/path de campos ou nomes de classes.
- **Escola e configuração individual:** `NÃO VERIFICADO`; mesmo a escola Necro observada no source não prova a associação deste registro no binário instalado.
- **Custos, cooldown, level/rarity, targeting, efeito, dano/cura, summons, filtros PvP/boss, persistência, aquisição e world safety:** `NÃO VERIFICADO`. Nenhum desses mecanismos é inferido do nome.
- **Identidade semântica:** `COUNTED_RELEASE_BOUNDED`, já inventariada no lote de 98 da fonte contemporânea. O feitiço pertence ao provider, com casting/mana/cooldown hospedados no Iron's. Black Arcana não reproduz o efeito.
- **Fonte factual:** [inventário](SPELL-CATALOG.md), [proveniência](EVIDENCE-AND-PROVENANCE.md), [limites de runtime](RUNTIME-AND-SAFETY.md).

### 87 — `SOUL_SCORCH`

- **Família organizacional na fonte:** `necro`; não comprova `SchoolType` individual.
- **Constante em `ModSpellRegistry`:** `SOUL_SCORCH`.
- **Classe da fonte pública:** `SoulScorchSpell`.
- **Registry ID físico 0.0.16.3:** `NÃO VERIFICADO`. Não derivar namespace/path de campos ou nomes de classes.
- **Escola e configuração individual:** `NÃO VERIFICADO`; mesmo a escola Necro observada no source não prova a associação deste registro no binário instalado.
- **Custos, cooldown, level/rarity, targeting, efeito, dano/cura, summons, filtros PvP/boss, persistência, aquisição e world safety:** `NÃO VERIFICADO`. Nenhum desses mecanismos é inferido do nome.
- **Identidade semântica:** `COUNTED_RELEASE_BOUNDED`, já inventariada no lote de 98 da fonte contemporânea. O feitiço pertence ao provider, com casting/mana/cooldown hospedados no Iron's. Black Arcana não reproduz o efeito.
- **Fonte factual:** [inventário](SPELL-CATALOG.md), [proveniência](EVIDENCE-AND-PROVENANCE.md), [limites de runtime](RUNTIME-AND-SAFETY.md).

### 88 — `SPECTRAL_BLAST`

- **Família organizacional na fonte:** `necro`; não comprova `SchoolType` individual.
- **Constante em `ModSpellRegistry`:** `SPECTRAL_BLAST`.
- **Classe da fonte pública:** `SpectralBlastSpell`.
- **Registry ID físico 0.0.16.3:** `NÃO VERIFICADO`. Não derivar namespace/path de campos ou nomes de classes.
- **Escola e configuração individual:** `NÃO VERIFICADO`; mesmo a escola Necro observada no source não prova a associação deste registro no binário instalado.
- **Custos, cooldown, level/rarity, targeting, efeito, dano/cura, summons, filtros PvP/boss, persistência, aquisição e world safety:** `NÃO VERIFICADO`. Nenhum desses mecanismos é inferido do nome.
- **Identidade semântica:** `COUNTED_RELEASE_BOUNDED`, já inventariada no lote de 98 da fonte contemporânea. O feitiço pertence ao provider, com casting/mana/cooldown hospedados no Iron's. Black Arcana não reproduz o efeito.
- **Fonte factual:** [inventário](SPELL-CATALOG.md), [proveniência](EVIDENCE-AND-PROVENANCE.md), [limites de runtime](RUNTIME-AND-SAFETY.md).

### 89 — `SPIRIT_STRIKE`

- **Família organizacional na fonte:** `necro`; não comprova `SchoolType` individual.
- **Constante em `ModSpellRegistry`:** `SPIRIT_STRIKE`.
- **Classe da fonte pública:** `SpiritStrikeSpell`.
- **Registry ID físico 0.0.16.3:** `NÃO VERIFICADO`. Não derivar namespace/path de campos ou nomes de classes.
- **Escola e configuração individual:** `NÃO VERIFICADO`; mesmo a escola Necro observada no source não prova a associação deste registro no binário instalado.
- **Custos, cooldown, level/rarity, targeting, efeito, dano/cura, summons, filtros PvP/boss, persistência, aquisição e world safety:** `NÃO VERIFICADO`. Nenhum desses mecanismos é inferido do nome.
- **Identidade semântica:** `COUNTED_RELEASE_BOUNDED`, já inventariada no lote de 98 da fonte contemporânea. O feitiço pertence ao provider, com casting/mana/cooldown hospedados no Iron's. Black Arcana não reproduz o efeito.
- **Fonte factual:** [inventário](SPELL-CATALOG.md), [proveniência](EVIDENCE-AND-PROVENANCE.md), [limites de runtime](RUNTIME-AND-SAFETY.md).

### 90 — `STRAY_GRASP`

- **Família organizacional na fonte:** `necro`; não comprova `SchoolType` individual.
- **Constante em `ModSpellRegistry`:** `STRAY_GRASP`.
- **Classe da fonte pública:** `StrayGraspSpell`.
- **Registry ID físico 0.0.16.3:** `NÃO VERIFICADO`. Não derivar namespace/path de campos ou nomes de classes.
- **Escola e configuração individual:** `NÃO VERIFICADO`; mesmo a escola Necro observada no source não prova a associação deste registro no binário instalado.
- **Custos, cooldown, level/rarity, targeting, efeito, dano/cura, summons, filtros PvP/boss, persistência, aquisição e world safety:** `NÃO VERIFICADO`. Nenhum desses mecanismos é inferido do nome.
- **Identidade semântica:** `COUNTED_RELEASE_BOUNDED`, já inventariada no lote de 98 da fonte contemporânea. O feitiço pertence ao provider, com casting/mana/cooldown hospedados no Iron's. Black Arcana não reproduz o efeito.
- **Fonte factual:** [inventário](SPELL-CATALOG.md), [proveniência](EVIDENCE-AND-PROVENANCE.md), [limites de runtime](RUNTIME-AND-SAFETY.md).

### 91 — `SUMMON_SOUL_WIZARD`

- **Família organizacional na fonte:** `necro`; não comprova `SchoolType` individual.
- **Constante em `ModSpellRegistry`:** `SUMMON_SOUL_WIZARD`.
- **Classe da fonte pública:** `SummonSoulWizardSpell`.
- **Registry ID físico 0.0.16.3:** `NÃO VERIFICADO`. Não derivar namespace/path de campos ou nomes de classes.
- **Escola e configuração individual:** `NÃO VERIFICADO`; mesmo a escola Necro observada no source não prova a associação deste registro no binário instalado.
- **Custos, cooldown, level/rarity, targeting, efeito, dano/cura, summons, filtros PvP/boss, persistência, aquisição e world safety:** `NÃO VERIFICADO`. Nenhum desses mecanismos é inferido do nome.
- **Identidade semântica:** `COUNTED_RELEASE_BOUNDED`, já inventariada no lote de 98 da fonte contemporânea. O feitiço pertence ao provider, com casting/mana/cooldown hospedados no Iron's. Black Arcana não reproduz o efeito.
- **Fonte factual:** [inventário](SPELL-CATALOG.md), [proveniência](EVIDENCE-AND-PROVENANCE.md), [limites de runtime](RUNTIME-AND-SAFETY.md).

### 92 — `TORMENT_ARROW`

- **Família organizacional na fonte:** `necro`; não comprova `SchoolType` individual.
- **Constante em `ModSpellRegistry`:** `TORMENT_ARROW`.
- **Classe da fonte pública:** `TormentArrowSpell`.
- **Registry ID físico 0.0.16.3:** `NÃO VERIFICADO`. Não derivar namespace/path de campos ou nomes de classes.
- **Escola e configuração individual:** `NÃO VERIFICADO`; mesmo a escola Necro observada no source não prova a associação deste registro no binário instalado.
- **Custos, cooldown, level/rarity, targeting, efeito, dano/cura, summons, filtros PvP/boss, persistência, aquisição e world safety:** `NÃO VERIFICADO`. Nenhum desses mecanismos é inferido do nome.
- **Identidade semântica:** `COUNTED_RELEASE_BOUNDED`, já inventariada no lote de 98 da fonte contemporânea. O feitiço pertence ao provider, com casting/mana/cooldown hospedados no Iron's. Black Arcana não reproduz o efeito.
- **Fonte factual:** [inventário](SPELL-CATALOG.md), [proveniência](EVIDENCE-AND-PROVENANCE.md), [limites de runtime](RUNTIME-AND-SAFETY.md).

### 93 — `VILE_SLASH`

- **Família organizacional na fonte:** `necro`; não comprova `SchoolType` individual.
- **Constante em `ModSpellRegistry`:** `VILE_SLASH`.
- **Classe da fonte pública:** `VileSlashSpell`.
- **Registry ID físico 0.0.16.3:** `NÃO VERIFICADO`. Não derivar namespace/path de campos ou nomes de classes.
- **Escola e configuração individual:** `NÃO VERIFICADO`; mesmo a escola Necro observada no source não prova a associação deste registro no binário instalado.
- **Custos, cooldown, level/rarity, targeting, efeito, dano/cura, summons, filtros PvP/boss, persistência, aquisição e world safety:** `NÃO VERIFICADO`. Nenhum desses mecanismos é inferido do nome.
- **Identidade semântica:** `COUNTED_RELEASE_BOUNDED`, já inventariada no lote de 98 da fonte contemporânea. O feitiço pertence ao provider, com casting/mana/cooldown hospedados no Iron's. Black Arcana não reproduz o efeito.
- **Fonte factual:** [inventário](SPELL-CATALOG.md), [proveniência](EVIDENCE-AND-PROVENANCE.md), [limites de runtime](RUNTIME-AND-SAFETY.md).

### 94 — `SUMMON_WITHER_ARMY`

- **Família organizacional na fonte:** `necro`; não comprova `SchoolType` individual.
- **Constante em `ModSpellRegistry`:** `SUMMON_WITHER_ARMY`.
- **Classe da fonte pública:** `SummonWitherArmy`.
- **Registry ID físico 0.0.16.3:** `NÃO VERIFICADO`. Não derivar namespace/path de campos ou nomes de classes.
- **Escola e configuração individual:** `NÃO VERIFICADO`; mesmo a escola Necro observada no source não prova a associação deste registro no binário instalado.
- **Custos, cooldown, level/rarity, targeting, efeito, dano/cura, summons, filtros PvP/boss, persistência, aquisição e world safety:** `NÃO VERIFICADO`. Nenhum desses mecanismos é inferido do nome.
- **Identidade semântica:** `COUNTED_RELEASE_BOUNDED`, já inventariada no lote de 98 da fonte contemporânea. O feitiço pertence ao provider, com casting/mana/cooldown hospedados no Iron's. Black Arcana não reproduz o efeito.
- **Fonte factual:** [inventário](SPELL-CATALOG.md), [proveniência](EVIDENCE-AND-PROVENANCE.md), [limites de runtime](RUNTIME-AND-SAFETY.md).

### 95 — `WITHER_BOMB`

- **Família organizacional na fonte:** `necro`; não comprova `SchoolType` individual.
- **Constante em `ModSpellRegistry`:** `WITHER_BOMB`.
- **Classe da fonte pública:** `WitherBombSpell`.
- **Registry ID físico 0.0.16.3:** `NÃO VERIFICADO`. Não derivar namespace/path de campos ou nomes de classes.
- **Escola e configuração individual:** `NÃO VERIFICADO`; mesmo a escola Necro observada no source não prova a associação deste registro no binário instalado.
- **Custos, cooldown, level/rarity, targeting, efeito, dano/cura, summons, filtros PvP/boss, persistência, aquisição e world safety:** `NÃO VERIFICADO`. Nenhum desses mecanismos é inferido do nome.
- **Identidade semântica:** `COUNTED_RELEASE_BOUNDED`, já inventariada no lote de 98 da fonte contemporânea. O feitiço pertence ao provider, com casting/mana/cooldown hospedados no Iron's. Black Arcana não reproduz o efeito.
- **Fonte factual:** [inventário](SPELL-CATALOG.md), [proveniência](EVIDENCE-AND-PROVENANCE.md), [limites de runtime](RUNTIME-AND-SAFETY.md).

### 96 — `WITHER_NOVA`

- **Família organizacional na fonte:** `necro`; não comprova `SchoolType` individual.
- **Constante em `ModSpellRegistry`:** `WITHER_NOVA`.
- **Classe da fonte pública:** `WitherNovaSpell`.
- **Registry ID físico 0.0.16.3:** `NÃO VERIFICADO`. Não derivar namespace/path de campos ou nomes de classes.
- **Escola e configuração individual:** `NÃO VERIFICADO`; mesmo a escola Necro observada no source não prova a associação deste registro no binário instalado.
- **Custos, cooldown, level/rarity, targeting, efeito, dano/cura, summons, filtros PvP/boss, persistência, aquisição e world safety:** `NÃO VERIFICADO`. Nenhum desses mecanismos é inferido do nome.
- **Identidade semântica:** `COUNTED_RELEASE_BOUNDED`, já inventariada no lote de 98 da fonte contemporânea. O feitiço pertence ao provider, com casting/mana/cooldown hospedados no Iron's. Black Arcana não reproduz o efeito.
- **Fonte factual:** [inventário](SPELL-CATALOG.md), [proveniência](EVIDENCE-AND-PROVENANCE.md), [limites de runtime](RUNTIME-AND-SAFETY.md).


## Família `technomancy` — 2 registros

### 97 — `SPINBLADE`

- **Família organizacional na fonte:** `technomancy`; não comprova `SchoolType` individual.
- **Constante em `ModSpellRegistry`:** `SPINBLADE`.
- **Classe da fonte pública:** `SpinbladeSpell`.
- **Registry ID físico 0.0.16.3:** `NÃO VERIFICADO`. Não derivar namespace/path de campos ou nomes de classes.
- **Escola e configuração individual:** `NÃO VERIFICADO`; mesmo a escola Necro observada no source não prova a associação deste registro no binário instalado.
- **Custos, cooldown, level/rarity, targeting, efeito, dano/cura, summons, filtros PvP/boss, persistência, aquisição e world safety:** `NÃO VERIFICADO`. Nenhum desses mecanismos é inferido do nome.
- **Identidade semântica:** `COUNTED_RELEASE_BOUNDED`, já inventariada no lote de 98 da fonte contemporânea. O feitiço pertence ao provider, com casting/mana/cooldown hospedados no Iron's. Black Arcana não reproduz o efeito.
- **Fonte factual:** [inventário](SPELL-CATALOG.md), [proveniência](EVIDENCE-AND-PROVENANCE.md), [limites de runtime](RUNTIME-AND-SAFETY.md).

### 98 — `SUMMON_DWARVEN_DRONES`

- **Família organizacional na fonte:** `technomancy`; não comprova `SchoolType` individual.
- **Constante em `ModSpellRegistry`:** `SUMMON_DWARVEN_DRONES`.
- **Classe da fonte pública:** `SummonDwarvenDronesSpell`.
- **Registry ID físico 0.0.16.3:** `NÃO VERIFICADO`. Não derivar namespace/path de campos ou nomes de classes.
- **Escola e configuração individual:** `NÃO VERIFICADO`; mesmo a escola Necro observada no source não prova a associação deste registro no binário instalado.
- **Custos, cooldown, level/rarity, targeting, efeito, dano/cura, summons, filtros PvP/boss, persistência, aquisição e world safety:** `NÃO VERIFICADO`. Nenhum desses mecanismos é inferido do nome.
- **Identidade semântica:** `COUNTED_RELEASE_BOUNDED`, já inventariada no lote de 98 da fonte contemporânea. O feitiço pertence ao provider, com casting/mana/cooldown hospedados no Iron's. Black Arcana não reproduz o efeito.
- **Fonte factual:** [inventário](SPELL-CATALOG.md), [proveniência](EVIDENCE-AND-PROVENANCE.md), [limites de runtime](RUNTIME-AND-SAFETY.md).

## Exclusões e limites finais

- `aero` = **0 registros** na fonte `ModSpellRegistry`; não acrescentar feitiços por menção a escola decompilada ou fonte com versão desatualizada.
- Não contar school, equipment, projectile, summon entity, effects e itens como segunda identidade do mesmo registro.
- Exatamente **98/98 fichas de campos/classes da fonte**. A paridade de IDs e classes no JAR instalado, configuração efetiva, aquisição em Survival, comportamento e hooks permanece ⚠️ **PENDENTE**, não promovida por documentação.
- Sem novos casts, bridges, APIs, hooks, balance, dano ou efeitos adicionados ao runtime Black Arcana. Etapa 06.05 e futuras etapas não avançam por esta tarefa.
