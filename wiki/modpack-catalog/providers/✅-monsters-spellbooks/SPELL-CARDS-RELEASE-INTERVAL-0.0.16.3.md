# Monsters & Spellbooks — fichas individuais de 98 spells (fonte contemporânea à release 0.0.16.3)

Status: **✅ 98/98 fichas com identidade `COUNTED_EXACT` do JAR SHA-exato 0.0.16.3 / ⚠️ alcance, dano, escola efetiva, targeting, custos e mecânicas em jogo ainda não comprovados**. A [prova física clean-room](../../../../docs/qa/monsters_spellbooks_00163_exact_registry_ids.json) documenta campos, classes compiladas e 98 ResourceLocations, com +0 novas raízes.

## Evidência e política de catalogação

- A modlist documenta `monstersspellbooks-0.0.16.3.jar`, mod ID `monstersspellbooks`, SHA-1 `b3aa89fd081bf4bfaf8d0f4380bcdc393c66ab0e` e release CurseForge File `8788560`.
- A fonte oficial examinada é `RedReaper28/Monsters-Spellbooks-1.21.1@1ab9b72af2ea44c3c8b816e665d06531ea44ddc2`. Seu `ModSpellRegistry` registra **98** campos e classes de magia. O arquivo de registry não mudou no intervalo público de releases 0.0.16.2–0.0.16.3.
- A fonte pública ainda declara `mod_version=0.0.14`. Portanto **NÃO é um build pin exato** do JAR 0.0.16.3. Os IDs atuais foram extraídos independentemente de `getSpellResource` do **JAR SHA-exato**, não inferidos da constante Java. Não converter identidade estática em school, custo ou efeito de runtime sem evidência adequada.
- Os **98 registros já estavam contabilizados**. A auditoria exata atualiza apenas a identidade de `COUNTED_RELEASE_BOUNDED` para `COUNTED_EXACT`, com **+0 novas identidades**, mínimos correntes **≥1.856 global / ≥1.854 escopo** e denominador universal aberto. Valores históricos 1.851/1.849 permanecem em snapshots antigos, não no total atual.
- As 11 famílias abaixo representam organização da fonte, não 11 `SchoolType` confirmados. `monstersspellbooks:necro` é observado na fonte, sem validação binária de escola por spell. `monstersspellbooks:aero` não pode ser tratado como instalado: zero magias Aero no registry e notas de remoção em 0.0.16.2–0.0.16.3.
- **Autoridade:** Monsters & Spellbooks controla seu conteúdo; Iron's controla casting, mana/cooldown e lifecycle de host. Black Arcana mantém seu próprio runtime, não duplica effects/summons/recursos e exige interface comprovada antes de integração.
- **Proveniência:** licenciamento documental divergente (publisher MIT, metadados da fonte All Rights Reserved); somente dados factuais de identidade/estrutura são reproduzidos, sem copiar código, recursos ou textos criativos.

## Índice e fichas individuais

## Família `blood` — 5 registros

### 01 — `ANTICOAGULATION`

- **Família organizacional na fonte:** `blood`; não comprova `SchoolType` individual.
- **Constante em `ModSpellRegistry`:** `ANTICOAGULATION`.
- **Classe da fonte pública:** `AnticoagulationSpell`.
- **Classe compilada SHA-exata 0.0.16.3:** `net.redreaper.monsterspellbooks.spells.blood.AnticoagulationSpell` ([dados da auditoria](../../../../docs/qa/monsters_spellbooks_00163_exact_registry_ids.json)).
- **Registry ID físico 0.0.16.3:** `monsterspellbooks:anticoagulation` (**`COUNTED_EXACT` apenas identidade estática**, obtida de `getSpellResource` compilado; nenhum comportamento deduzido do nome).
- **Escola e configuração individual:** `NÃO VERIFICADO`; mesmo a escola Necro observada no source não prova a associação deste registro no binário instalado.
- **Custos, cooldown, level/rarity, targeting, efeito, dano/cura, summons, filtros PvP/boss, persistência, aquisição e world safety:** `NÃO VERIFICADO`. Nenhum desses mecanismos é inferido do nome.
- **Identidade semântica:** `COUNTED_EXACT` para ID/registro estático já inventariado no lote de 98; **+0** novos objetos. O feitiço pertence ao provider, com casting/mana/cooldown hospedados no Iron's. Black Arcana não reproduz o efeito.
- **Fonte factual:** [inventário](SPELL-CATALOG.md), [proveniência](EVIDENCE-AND-PROVENANCE.md), [limites de runtime](RUNTIME-AND-SAFETY.md).

### 02 — `BLOOD_PIERCE`

- **Família organizacional na fonte:** `blood`; não comprova `SchoolType` individual.
- **Constante em `ModSpellRegistry`:** `BLOOD_PIERCE`.
- **Classe da fonte pública:** `BloodPierceSpell`.
- **Classe compilada SHA-exata 0.0.16.3:** `net.redreaper.monsterspellbooks.spells.blood.BloodPierceSpell` ([dados da auditoria](../../../../docs/qa/monsters_spellbooks_00163_exact_registry_ids.json)).
- **Registry ID físico 0.0.16.3:** `monsterspellbooks:blood_pierce` (**`COUNTED_EXACT` apenas identidade estática**, obtida de `getSpellResource` compilado; nenhum comportamento deduzido do nome).
- **Escola e configuração individual:** `NÃO VERIFICADO`; mesmo a escola Necro observada no source não prova a associação deste registro no binário instalado.
- **Custos, cooldown, level/rarity, targeting, efeito, dano/cura, summons, filtros PvP/boss, persistência, aquisição e world safety:** `NÃO VERIFICADO`. Nenhum desses mecanismos é inferido do nome.
- **Identidade semântica:** `COUNTED_EXACT` para ID/registro estático já inventariado no lote de 98; **+0** novos objetos. O feitiço pertence ao provider, com casting/mana/cooldown hospedados no Iron's. Black Arcana não reproduz o efeito.
- **Fonte factual:** [inventário](SPELL-CATALOG.md), [proveniência](EVIDENCE-AND-PROVENANCE.md), [limites de runtime](RUNTIME-AND-SAFETY.md).

### 03 — `BLOOD_THORN`

- **Família organizacional na fonte:** `blood`; não comprova `SchoolType` individual.
- **Constante em `ModSpellRegistry`:** `BLOOD_THORN`.
- **Classe da fonte pública:** `BloodThornSpell`.
- **Classe compilada SHA-exata 0.0.16.3:** `net.redreaper.monsterspellbooks.spells.blood.BloodThornSpell` ([dados da auditoria](../../../../docs/qa/monsters_spellbooks_00163_exact_registry_ids.json)).
- **Registry ID físico 0.0.16.3:** `monsterspellbooks:blood_thorn` (**`COUNTED_EXACT` apenas identidade estática**, obtida de `getSpellResource` compilado; nenhum comportamento deduzido do nome).
- **Escola e configuração individual:** `NÃO VERIFICADO`; mesmo a escola Necro observada no source não prova a associação deste registro no binário instalado.
- **Custos, cooldown, level/rarity, targeting, efeito, dano/cura, summons, filtros PvP/boss, persistência, aquisição e world safety:** `NÃO VERIFICADO`. Nenhum desses mecanismos é inferido do nome.
- **Identidade semântica:** `COUNTED_EXACT` para ID/registro estático já inventariado no lote de 98; **+0** novos objetos. O feitiço pertence ao provider, com casting/mana/cooldown hospedados no Iron's. Black Arcana não reproduz o efeito.
- **Fonte factual:** [inventário](SPELL-CATALOG.md), [proveniência](EVIDENCE-AND-PROVENANCE.md), [limites de runtime](RUNTIME-AND-SAFETY.md).

### 04 — `HYSTERIA`

- **Família organizacional na fonte:** `blood`; não comprova `SchoolType` individual.
- **Constante em `ModSpellRegistry`:** `HYSTERIA`.
- **Classe da fonte pública:** `HysteriaSpell`.
- **Classe compilada SHA-exata 0.0.16.3:** `net.redreaper.monsterspellbooks.spells.blood.HysteriaSpell` ([dados da auditoria](../../../../docs/qa/monsters_spellbooks_00163_exact_registry_ids.json)).
- **Registry ID físico 0.0.16.3:** `monsterspellbooks:hysteria` (**`COUNTED_EXACT` apenas identidade estática**, obtida de `getSpellResource` compilado; nenhum comportamento deduzido do nome).
- **Escola e configuração individual:** `NÃO VERIFICADO`; mesmo a escola Necro observada no source não prova a associação deste registro no binário instalado.
- **Custos, cooldown, level/rarity, targeting, efeito, dano/cura, summons, filtros PvP/boss, persistência, aquisição e world safety:** `NÃO VERIFICADO`. Nenhum desses mecanismos é inferido do nome.
- **Identidade semântica:** `COUNTED_EXACT` para ID/registro estático já inventariado no lote de 98; **+0** novos objetos. O feitiço pertence ao provider, com casting/mana/cooldown hospedados no Iron's. Black Arcana não reproduz o efeito.
- **Fonte factual:** [inventário](SPELL-CATALOG.md), [proveniência](EVIDENCE-AND-PROVENANCE.md), [limites de runtime](RUNTIME-AND-SAFETY.md).

### 05 — `SANGUINITE_EVISCERATION`

- **Família organizacional na fonte:** `blood`; não comprova `SchoolType` individual.
- **Constante em `ModSpellRegistry`:** `SANGUINITE_EVISCERATION`.
- **Classe da fonte pública:** `SanguiniteEviscerationSpell`.
- **Classe compilada SHA-exata 0.0.16.3:** `net.redreaper.monsterspellbooks.spells.blood.SanguiniteEviscerationSpell` ([dados da auditoria](../../../../docs/qa/monsters_spellbooks_00163_exact_registry_ids.json)).
- **Registry ID físico 0.0.16.3:** `monsterspellbooks:sanguinite_evisceration` (**`COUNTED_EXACT` apenas identidade estática**, obtida de `getSpellResource` compilado; nenhum comportamento deduzido do nome).
- **Escola e configuração individual:** `NÃO VERIFICADO`; mesmo a escola Necro observada no source não prova a associação deste registro no binário instalado.
- **Custos, cooldown, level/rarity, targeting, efeito, dano/cura, summons, filtros PvP/boss, persistência, aquisição e world safety:** `NÃO VERIFICADO`. Nenhum desses mecanismos é inferido do nome.
- **Identidade semântica:** `COUNTED_EXACT` para ID/registro estático já inventariado no lote de 98; **+0** novos objetos. O feitiço pertence ao provider, com casting/mana/cooldown hospedados no Iron's. Black Arcana não reproduz o efeito.
- **Fonte factual:** [inventário](SPELL-CATALOG.md), [proveniência](EVIDENCE-AND-PROVENANCE.md), [limites de runtime](RUNTIME-AND-SAFETY.md).


## Família `ender` — 12 registros

### 06 — `CORRUPTED_BEACON_RAY`

- **Família organizacional na fonte:** `ender`; não comprova `SchoolType` individual.
- **Constante em `ModSpellRegistry`:** `CORRUPTED_BEACON_RAY`.
- **Classe da fonte pública:** `CorruptedBeaconRaySpell`.
- **Classe compilada SHA-exata 0.0.16.3:** `net.redreaper.monsterspellbooks.spells.ender.CorruptedBeaconRaySpell` ([dados da auditoria](../../../../docs/qa/monsters_spellbooks_00163_exact_registry_ids.json)).
- **Registry ID físico 0.0.16.3:** `monsterspellbooks:corrupted_beacon_ray` (**`COUNTED_EXACT` apenas identidade estática**, obtida de `getSpellResource` compilado; nenhum comportamento deduzido do nome).
- **Escola e configuração individual:** `NÃO VERIFICADO`; mesmo a escola Necro observada no source não prova a associação deste registro no binário instalado.
- **Custos, cooldown, level/rarity, targeting, efeito, dano/cura, summons, filtros PvP/boss, persistência, aquisição e world safety:** `NÃO VERIFICADO`. Nenhum desses mecanismos é inferido do nome.
- **Identidade semântica:** `COUNTED_EXACT` para ID/registro estático já inventariado no lote de 98; **+0** novos objetos. O feitiço pertence ao provider, com casting/mana/cooldown hospedados no Iron's. Black Arcana não reproduz o efeito.
- **Fonte factual:** [inventário](SPELL-CATALOG.md), [proveniência](EVIDENCE-AND-PROVENANCE.md), [limites de runtime](RUNTIME-AND-SAFETY.md).

### 07 — `CRUSHING_PRESENCE`

- **Família organizacional na fonte:** `ender`; não comprova `SchoolType` individual.
- **Constante em `ModSpellRegistry`:** `CRUSHING_PRESENCE`.
- **Classe da fonte pública:** `CrushingPresenceSpell`.
- **Classe compilada SHA-exata 0.0.16.3:** `net.redreaper.monsterspellbooks.spells.ender.CrushingPresenceSpell` ([dados da auditoria](../../../../docs/qa/monsters_spellbooks_00163_exact_registry_ids.json)).
- **Registry ID físico 0.0.16.3:** `monsterspellbooks:crushing_presence` (**`COUNTED_EXACT` apenas identidade estática**, obtida de `getSpellResource` compilado; nenhum comportamento deduzido do nome).
- **Escola e configuração individual:** `NÃO VERIFICADO`; mesmo a escola Necro observada no source não prova a associação deste registro no binário instalado.
- **Custos, cooldown, level/rarity, targeting, efeito, dano/cura, summons, filtros PvP/boss, persistência, aquisição e world safety:** `NÃO VERIFICADO`. Nenhum desses mecanismos é inferido do nome.
- **Identidade semântica:** `COUNTED_EXACT` para ID/registro estático já inventariado no lote de 98; **+0** novos objetos. O feitiço pertence ao provider, com casting/mana/cooldown hospedados no Iron's. Black Arcana não reproduz o efeito.
- **Fonte factual:** [inventário](SPELL-CATALOG.md), [proveniência](EVIDENCE-AND-PROVENANCE.md), [limites de runtime](RUNTIME-AND-SAFETY.md).

### 08 — `CRUSH`

- **Família organizacional na fonte:** `ender`; não comprova `SchoolType` individual.
- **Constante em `ModSpellRegistry`:** `CRUSH`.
- **Classe da fonte pública:** `CrushSpell`.
- **Classe compilada SHA-exata 0.0.16.3:** `net.redreaper.monsterspellbooks.spells.ender.CrushSpell` ([dados da auditoria](../../../../docs/qa/monsters_spellbooks_00163_exact_registry_ids.json)).
- **Registry ID físico 0.0.16.3:** `monsterspellbooks:crush` (**`COUNTED_EXACT` apenas identidade estática**, obtida de `getSpellResource` compilado; nenhum comportamento deduzido do nome).
- **Escola e configuração individual:** `NÃO VERIFICADO`; mesmo a escola Necro observada no source não prova a associação deste registro no binário instalado.
- **Custos, cooldown, level/rarity, targeting, efeito, dano/cura, summons, filtros PvP/boss, persistência, aquisição e world safety:** `NÃO VERIFICADO`. Nenhum desses mecanismos é inferido do nome.
- **Identidade semântica:** `COUNTED_EXACT` para ID/registro estático já inventariado no lote de 98; **+0** novos objetos. O feitiço pertence ao provider, com casting/mana/cooldown hospedados no Iron's. Black Arcana não reproduz o efeito.
- **Fonte factual:** [inventário](SPELL-CATALOG.md), [proveniência](EVIDENCE-AND-PROVENANCE.md), [limites de runtime](RUNTIME-AND-SAFETY.md).

### 09 — `DRAGON_CHARGE`

- **Família organizacional na fonte:** `ender`; não comprova `SchoolType` individual.
- **Constante em `ModSpellRegistry`:** `DRAGON_CHARGE`.
- **Classe da fonte pública:** `DragonChargeSpell`.
- **Classe compilada SHA-exata 0.0.16.3:** `net.redreaper.monsterspellbooks.spells.ender.DragonChargeSpell` ([dados da auditoria](../../../../docs/qa/monsters_spellbooks_00163_exact_registry_ids.json)).
- **Registry ID físico 0.0.16.3:** `monsterspellbooks:dragon_charge` (**`COUNTED_EXACT` apenas identidade estática**, obtida de `getSpellResource` compilado; nenhum comportamento deduzido do nome).
- **Escola e configuração individual:** `NÃO VERIFICADO`; mesmo a escola Necro observada no source não prova a associação deste registro no binário instalado.
- **Custos, cooldown, level/rarity, targeting, efeito, dano/cura, summons, filtros PvP/boss, persistência, aquisição e world safety:** `NÃO VERIFICADO`. Nenhum desses mecanismos é inferido do nome.
- **Identidade semântica:** `COUNTED_EXACT` para ID/registro estático já inventariado no lote de 98; **+0** novos objetos. O feitiço pertence ao provider, com casting/mana/cooldown hospedados no Iron's. Black Arcana não reproduz o efeito.
- **Fonte factual:** [inventário](SPELL-CATALOG.md), [proveniência](EVIDENCE-AND-PROVENANCE.md), [limites de runtime](RUNTIME-AND-SAFETY.md).

### 10 — `ENDERSENT_SMASH`

- **Família organizacional na fonte:** `ender`; não comprova `SchoolType` individual.
- **Constante em `ModSpellRegistry`:** `ENDERSENT_SMASH`.
- **Classe da fonte pública:** `EndersentSmashSpell`.
- **Classe compilada SHA-exata 0.0.16.3:** `net.redreaper.monsterspellbooks.spells.ender.EndersentSmashSpell` ([dados da auditoria](../../../../docs/qa/monsters_spellbooks_00163_exact_registry_ids.json)).
- **Registry ID físico 0.0.16.3:** `monsterspellbooks:endersent_smash` (**`COUNTED_EXACT` apenas identidade estática**, obtida de `getSpellResource` compilado; nenhum comportamento deduzido do nome).
- **Escola e configuração individual:** `NÃO VERIFICADO`; mesmo a escola Necro observada no source não prova a associação deste registro no binário instalado.
- **Custos, cooldown, level/rarity, targeting, efeito, dano/cura, summons, filtros PvP/boss, persistência, aquisição e world safety:** `NÃO VERIFICADO`. Nenhum desses mecanismos é inferido do nome.
- **Identidade semântica:** `COUNTED_EXACT` para ID/registro estático já inventariado no lote de 98; **+0** novos objetos. O feitiço pertence ao provider, com casting/mana/cooldown hospedados no Iron's. Black Arcana não reproduz o efeito.
- **Fonte factual:** [inventário](SPELL-CATALOG.md), [proveniência](EVIDENCE-AND-PROVENANCE.md), [limites de runtime](RUNTIME-AND-SAFETY.md).

### 11 — `ENDERSENT_FORM`

- **Família organizacional na fonte:** `ender`; não comprova `SchoolType` individual.
- **Constante em `ModSpellRegistry`:** `ENDERSENT_FORM`.
- **Classe da fonte pública:** `EndersentFormSpell`.
- **Classe compilada SHA-exata 0.0.16.3:** `net.redreaper.monsterspellbooks.spells.ender.EndersentFormSpell` ([dados da auditoria](../../../../docs/qa/monsters_spellbooks_00163_exact_registry_ids.json)).
- **Registry ID físico 0.0.16.3:** `monsterspellbooks:endersent_form` (**`COUNTED_EXACT` apenas identidade estática**, obtida de `getSpellResource` compilado; nenhum comportamento deduzido do nome).
- **Escola e configuração individual:** `NÃO VERIFICADO`; mesmo a escola Necro observada no source não prova a associação deste registro no binário instalado.
- **Custos, cooldown, level/rarity, targeting, efeito, dano/cura, summons, filtros PvP/boss, persistência, aquisição e world safety:** `NÃO VERIFICADO`. Nenhum desses mecanismos é inferido do nome.
- **Identidade semântica:** `COUNTED_EXACT` para ID/registro estático já inventariado no lote de 98; **+0** novos objetos. O feitiço pertence ao provider, com casting/mana/cooldown hospedados no Iron's. Black Arcana não reproduz o efeito.
- **Fonte factual:** [inventário](SPELL-CATALOG.md), [proveniência](EVIDENCE-AND-PROVENANCE.md), [limites de runtime](RUNTIME-AND-SAFETY.md).

### 12 — `FIRMAMENT_SPLITTER`

- **Família organizacional na fonte:** `ender`; não comprova `SchoolType` individual.
- **Constante em `ModSpellRegistry`:** `FIRMAMENT_SPLITTER`.
- **Classe da fonte pública:** `FirmamentSplitterSpell`.
- **Classe compilada SHA-exata 0.0.16.3:** `net.redreaper.monsterspellbooks.spells.ender.FirmamentSplitterSpell` ([dados da auditoria](../../../../docs/qa/monsters_spellbooks_00163_exact_registry_ids.json)).
- **Registry ID físico 0.0.16.3:** `monsterspellbooks:firmament_splitter` (**`COUNTED_EXACT` apenas identidade estática**, obtida de `getSpellResource` compilado; nenhum comportamento deduzido do nome).
- **Escola e configuração individual:** `NÃO VERIFICADO`; mesmo a escola Necro observada no source não prova a associação deste registro no binário instalado.
- **Custos, cooldown, level/rarity, targeting, efeito, dano/cura, summons, filtros PvP/boss, persistência, aquisição e world safety:** `NÃO VERIFICADO`. Nenhum desses mecanismos é inferido do nome.
- **Identidade semântica:** `COUNTED_EXACT` para ID/registro estático já inventariado no lote de 98; **+0** novos objetos. O feitiço pertence ao provider, com casting/mana/cooldown hospedados no Iron's. Black Arcana não reproduz o efeito.
- **Fonte factual:** [inventário](SPELL-CATALOG.md), [proveniência](EVIDENCE-AND-PROVENANCE.md), [limites de runtime](RUNTIME-AND-SAFETY.md).

### 13 — `GRAVITY_WELL`

- **Família organizacional na fonte:** `ender`; não comprova `SchoolType` individual.
- **Constante em `ModSpellRegistry`:** `GRAVITY_WELL`.
- **Classe da fonte pública:** `GravityWellSpell`.
- **Classe compilada SHA-exata 0.0.16.3:** `net.redreaper.monsterspellbooks.spells.ender.GravityWellSpell` ([dados da auditoria](../../../../docs/qa/monsters_spellbooks_00163_exact_registry_ids.json)).
- **Registry ID físico 0.0.16.3:** `monsterspellbooks:gravity_well` (**`COUNTED_EXACT` apenas identidade estática**, obtida de `getSpellResource` compilado; nenhum comportamento deduzido do nome).
- **Escola e configuração individual:** `NÃO VERIFICADO`; mesmo a escola Necro observada no source não prova a associação deste registro no binário instalado.
- **Custos, cooldown, level/rarity, targeting, efeito, dano/cura, summons, filtros PvP/boss, persistência, aquisição e world safety:** `NÃO VERIFICADO`. Nenhum desses mecanismos é inferido do nome.
- **Identidade semântica:** `COUNTED_EXACT` para ID/registro estático já inventariado no lote de 98; **+0** novos objetos. O feitiço pertence ao provider, com casting/mana/cooldown hospedados no Iron's. Black Arcana não reproduz o efeito.
- **Fonte factual:** [inventário](SPELL-CATALOG.md), [proveniência](EVIDENCE-AND-PROVENANCE.md), [limites de runtime](RUNTIME-AND-SAFETY.md).

### 14 — `SPACE_BREAKER`

- **Família organizacional na fonte:** `ender`; não comprova `SchoolType` individual.
- **Constante em `ModSpellRegistry`:** `SPACE_BREAKER`.
- **Classe da fonte pública:** `SpaceBreakerSpell`.
- **Classe compilada SHA-exata 0.0.16.3:** `net.redreaper.monsterspellbooks.spells.ender.SpaceBreakerSpell` ([dados da auditoria](../../../../docs/qa/monsters_spellbooks_00163_exact_registry_ids.json)).
- **Registry ID físico 0.0.16.3:** `monsterspellbooks:space_breaker` (**`COUNTED_EXACT` apenas identidade estática**, obtida de `getSpellResource` compilado; nenhum comportamento deduzido do nome).
- **Escola e configuração individual:** `NÃO VERIFICADO`; mesmo a escola Necro observada no source não prova a associação deste registro no binário instalado.
- **Custos, cooldown, level/rarity, targeting, efeito, dano/cura, summons, filtros PvP/boss, persistência, aquisição e world safety:** `NÃO VERIFICADO`. Nenhum desses mecanismos é inferido do nome.
- **Identidade semântica:** `COUNTED_EXACT` para ID/registro estático já inventariado no lote de 98; **+0** novos objetos. O feitiço pertence ao provider, com casting/mana/cooldown hospedados no Iron's. Black Arcana não reproduz o efeito.
- **Fonte factual:** [inventário](SPELL-CATALOG.md), [proveniência](EVIDENCE-AND-PROVENANCE.md), [limites de runtime](RUNTIME-AND-SAFETY.md).

### 15 — `SPACE_RUPTURE`

- **Família organizacional na fonte:** `ender`; não comprova `SchoolType` individual.
- **Constante em `ModSpellRegistry`:** `SPACE_RUPTURE`.
- **Classe da fonte pública:** `SpaceRuptureSpell`.
- **Classe compilada SHA-exata 0.0.16.3:** `net.redreaper.monsterspellbooks.spells.ender.SpaceRuptureSpell` ([dados da auditoria](../../../../docs/qa/monsters_spellbooks_00163_exact_registry_ids.json)).
- **Registry ID físico 0.0.16.3:** `monsterspellbooks:space_rupture` (**`COUNTED_EXACT` apenas identidade estática**, obtida de `getSpellResource` compilado; nenhum comportamento deduzido do nome).
- **Escola e configuração individual:** `NÃO VERIFICADO`; mesmo a escola Necro observada no source não prova a associação deste registro no binário instalado.
- **Custos, cooldown, level/rarity, targeting, efeito, dano/cura, summons, filtros PvP/boss, persistência, aquisição e world safety:** `NÃO VERIFICADO`. Nenhum desses mecanismos é inferido do nome.
- **Identidade semântica:** `COUNTED_EXACT` para ID/registro estático já inventariado no lote de 98; **+0** novos objetos. O feitiço pertence ao provider, com casting/mana/cooldown hospedados no Iron's. Black Arcana não reproduz o efeito.
- **Fonte factual:** [inventário](SPELL-CATALOG.md), [proveniência](EVIDENCE-AND-PROVENANCE.md), [limites de runtime](RUNTIME-AND-SAFETY.md).

### 16 — `UNSTABLE_TELEPORT`

- **Família organizacional na fonte:** `ender`; não comprova `SchoolType` individual.
- **Constante em `ModSpellRegistry`:** `UNSTABLE_TELEPORT`.
- **Classe da fonte pública:** `UnstableTeleportSpell`.
- **Classe compilada SHA-exata 0.0.16.3:** `net.redreaper.monsterspellbooks.spells.ender.UnstableTeleportSpell` ([dados da auditoria](../../../../docs/qa/monsters_spellbooks_00163_exact_registry_ids.json)).
- **Registry ID físico 0.0.16.3:** `monsterspellbooks:unstable_teleport` (**`COUNTED_EXACT` apenas identidade estática**, obtida de `getSpellResource` compilado; nenhum comportamento deduzido do nome).
- **Escola e configuração individual:** `NÃO VERIFICADO`; mesmo a escola Necro observada no source não prova a associação deste registro no binário instalado.
- **Custos, cooldown, level/rarity, targeting, efeito, dano/cura, summons, filtros PvP/boss, persistência, aquisição e world safety:** `NÃO VERIFICADO`. Nenhum desses mecanismos é inferido do nome.
- **Identidade semântica:** `COUNTED_EXACT` para ID/registro estático já inventariado no lote de 98; **+0** novos objetos. O feitiço pertence ao provider, com casting/mana/cooldown hospedados no Iron's. Black Arcana não reproduz o efeito.
- **Fonte factual:** [inventário](SPELL-CATALOG.md), [proveniência](EVIDENCE-AND-PROVENANCE.md), [limites de runtime](RUNTIME-AND-SAFETY.md).

### 17 — `VOID_ARROWS`

- **Família organizacional na fonte:** `ender`; não comprova `SchoolType` individual.
- **Constante em `ModSpellRegistry`:** `VOID_ARROWS`.
- **Classe da fonte pública:** `VoidArrowsSpell`.
- **Classe compilada SHA-exata 0.0.16.3:** `net.redreaper.monsterspellbooks.spells.ender.VoidArrowsSpell` ([dados da auditoria](../../../../docs/qa/monsters_spellbooks_00163_exact_registry_ids.json)).
- **Registry ID físico 0.0.16.3:** `monsterspellbooks:void_arrows` (**`COUNTED_EXACT` apenas identidade estática**, obtida de `getSpellResource` compilado; nenhum comportamento deduzido do nome).
- **Escola e configuração individual:** `NÃO VERIFICADO`; mesmo a escola Necro observada no source não prova a associação deste registro no binário instalado.
- **Custos, cooldown, level/rarity, targeting, efeito, dano/cura, summons, filtros PvP/boss, persistência, aquisição e world safety:** `NÃO VERIFICADO`. Nenhum desses mecanismos é inferido do nome.
- **Identidade semântica:** `COUNTED_EXACT` para ID/registro estático já inventariado no lote de 98; **+0** novos objetos. O feitiço pertence ao provider, com casting/mana/cooldown hospedados no Iron's. Black Arcana não reproduz o efeito.
- **Fonte factual:** [inventário](SPELL-CATALOG.md), [proveniência](EVIDENCE-AND-PROVENANCE.md), [limites de runtime](RUNTIME-AND-SAFETY.md).


## Família `evocation` — 3 registros

### 18 — `ENCHANTERS_BOOST`

- **Família organizacional na fonte:** `evocation`; não comprova `SchoolType` individual.
- **Constante em `ModSpellRegistry`:** `ENCHANTERS_BOOST`.
- **Classe da fonte pública:** `EnchantersBoostSpell`.
- **Classe compilada SHA-exata 0.0.16.3:** `net.redreaper.monsterspellbooks.spells.evocation.EnchantersBoostSpell` ([dados da auditoria](../../../../docs/qa/monsters_spellbooks_00163_exact_registry_ids.json)).
- **Registry ID físico 0.0.16.3:** `monsterspellbooks:enchanters_boost` (**`COUNTED_EXACT` apenas identidade estática**, obtida de `getSpellResource` compilado; nenhum comportamento deduzido do nome).
- **Escola e configuração individual:** `NÃO VERIFICADO`; mesmo a escola Necro observada no source não prova a associação deste registro no binário instalado.
- **Custos, cooldown, level/rarity, targeting, efeito, dano/cura, summons, filtros PvP/boss, persistência, aquisição e world safety:** `NÃO VERIFICADO`. Nenhum desses mecanismos é inferido do nome.
- **Identidade semântica:** `COUNTED_EXACT` para ID/registro estático já inventariado no lote de 98; **+0** novos objetos. O feitiço pertence ao provider, com casting/mana/cooldown hospedados no Iron's. Black Arcana não reproduz o efeito.
- **Fonte factual:** [inventário](SPELL-CATALOG.md), [proveniência](EVIDENCE-AND-PROVENANCE.md), [limites de runtime](RUNTIME-AND-SAFETY.md).

### 19 — `ENCHANTERS_PROTECTION`

- **Família organizacional na fonte:** `evocation`; não comprova `SchoolType` individual.
- **Constante em `ModSpellRegistry`:** `ENCHANTERS_PROTECTION`.
- **Classe da fonte pública:** `EnchantersProtectionSpell`.
- **Classe compilada SHA-exata 0.0.16.3:** `net.redreaper.monsterspellbooks.spells.evocation.EnchantersProtectionSpell` ([dados da auditoria](../../../../docs/qa/monsters_spellbooks_00163_exact_registry_ids.json)).
- **Registry ID físico 0.0.16.3:** `monsterspellbooks:enchanters_protection` (**`COUNTED_EXACT` apenas identidade estática**, obtida de `getSpellResource` compilado; nenhum comportamento deduzido do nome).
- **Escola e configuração individual:** `NÃO VERIFICADO`; mesmo a escola Necro observada no source não prova a associação deste registro no binário instalado.
- **Custos, cooldown, level/rarity, targeting, efeito, dano/cura, summons, filtros PvP/boss, persistência, aquisição e world safety:** `NÃO VERIFICADO`. Nenhum desses mecanismos é inferido do nome.
- **Identidade semântica:** `COUNTED_EXACT` para ID/registro estático já inventariado no lote de 98; **+0** novos objetos. O feitiço pertence ao provider, com casting/mana/cooldown hospedados no Iron's. Black Arcana não reproduz o efeito.
- **Fonte factual:** [inventário](SPELL-CATALOG.md), [proveniência](EVIDENCE-AND-PROVENANCE.md), [limites de runtime](RUNTIME-AND-SAFETY.md).

### 20 — `SPELL_OF_UNDYING`

- **Família organizacional na fonte:** `evocation`; não comprova `SchoolType` individual.
- **Constante em `ModSpellRegistry`:** `SPELL_OF_UNDYING`.
- **Classe da fonte pública:** `SpellOfUndyingSpell`.
- **Classe compilada SHA-exata 0.0.16.3:** `net.redreaper.monsterspellbooks.spells.evocation.SpellOfUndyingSpell` ([dados da auditoria](../../../../docs/qa/monsters_spellbooks_00163_exact_registry_ids.json)).
- **Registry ID físico 0.0.16.3:** `monsterspellbooks:spell_of_undying` (**`COUNTED_EXACT` apenas identidade estática**, obtida de `getSpellResource` compilado; nenhum comportamento deduzido do nome).
- **Escola e configuração individual:** `NÃO VERIFICADO`; mesmo a escola Necro observada no source não prova a associação deste registro no binário instalado.
- **Custos, cooldown, level/rarity, targeting, efeito, dano/cura, summons, filtros PvP/boss, persistência, aquisição e world safety:** `NÃO VERIFICADO`. Nenhum desses mecanismos é inferido do nome.
- **Identidade semântica:** `COUNTED_EXACT` para ID/registro estático já inventariado no lote de 98; **+0** novos objetos. O feitiço pertence ao provider, com casting/mana/cooldown hospedados no Iron's. Black Arcana não reproduz o efeito.
- **Fonte factual:** [inventário](SPELL-CATALOG.md), [proveniência](EVIDENCE-AND-PROVENANCE.md), [limites de runtime](RUNTIME-AND-SAFETY.md).


## Família `fire` — 10 registros

### 21 — `BRIMSTONE_BUZZSAW`

- **Família organizacional na fonte:** `fire`; não comprova `SchoolType` individual.
- **Constante em `ModSpellRegistry`:** `BRIMSTONE_BUZZSAW`.
- **Classe da fonte pública:** `BrimstoneBuzzsawSpell`.
- **Classe compilada SHA-exata 0.0.16.3:** `net.redreaper.monsterspellbooks.spells.fire.BrimstoneBuzzsawSpell` ([dados da auditoria](../../../../docs/qa/monsters_spellbooks_00163_exact_registry_ids.json)).
- **Registry ID físico 0.0.16.3:** `monsterspellbooks:brimstone_buzzsaw` (**`COUNTED_EXACT` apenas identidade estática**, obtida de `getSpellResource` compilado; nenhum comportamento deduzido do nome).
- **Escola e configuração individual:** `NÃO VERIFICADO`; mesmo a escola Necro observada no source não prova a associação deste registro no binário instalado.
- **Custos, cooldown, level/rarity, targeting, efeito, dano/cura, summons, filtros PvP/boss, persistência, aquisição e world safety:** `NÃO VERIFICADO`. Nenhum desses mecanismos é inferido do nome.
- **Identidade semântica:** `COUNTED_EXACT` para ID/registro estático já inventariado no lote de 98; **+0** novos objetos. O feitiço pertence ao provider, com casting/mana/cooldown hospedados no Iron's. Black Arcana não reproduz o efeito.
- **Fonte factual:** [inventário](SPELL-CATALOG.md), [proveniência](EVIDENCE-AND-PROVENANCE.md), [limites de runtime](RUNTIME-AND-SAFETY.md).

### 22 — `BRIMSTONE_RAIN`

- **Família organizacional na fonte:** `fire`; não comprova `SchoolType` individual.
- **Constante em `ModSpellRegistry`:** `BRIMSTONE_RAIN`.
- **Classe da fonte pública:** `BrimstoneRainSpell`.
- **Classe compilada SHA-exata 0.0.16.3:** `net.redreaper.monsterspellbooks.spells.fire.BrimstoneRainSpell` ([dados da auditoria](../../../../docs/qa/monsters_spellbooks_00163_exact_registry_ids.json)).
- **Registry ID físico 0.0.16.3:** `monsterspellbooks:brimstone_rain` (**`COUNTED_EXACT` apenas identidade estática**, obtida de `getSpellResource` compilado; nenhum comportamento deduzido do nome).
- **Escola e configuração individual:** `NÃO VERIFICADO`; mesmo a escola Necro observada no source não prova a associação deste registro no binário instalado.
- **Custos, cooldown, level/rarity, targeting, efeito, dano/cura, summons, filtros PvP/boss, persistência, aquisição e world safety:** `NÃO VERIFICADO`. Nenhum desses mecanismos é inferido do nome.
- **Identidade semântica:** `COUNTED_EXACT` para ID/registro estático já inventariado no lote de 98; **+0** novos objetos. O feitiço pertence ao provider, com casting/mana/cooldown hospedados no Iron's. Black Arcana não reproduz o efeito.
- **Fonte factual:** [inventário](SPELL-CATALOG.md), [proveniência](EVIDENCE-AND-PROVENANCE.md), [limites de runtime](RUNTIME-AND-SAFETY.md).

### 23 — `BRIMSTONE_WRATH`

- **Família organizacional na fonte:** `fire`; não comprova `SchoolType` individual.
- **Constante em `ModSpellRegistry`:** `BRIMSTONE_WRATH`.
- **Classe da fonte pública:** `BrimstoneWrathSpell`.
- **Classe compilada SHA-exata 0.0.16.3:** `net.redreaper.monsterspellbooks.spells.fire.BrimstoneWrathSpell` ([dados da auditoria](../../../../docs/qa/monsters_spellbooks_00163_exact_registry_ids.json)).
- **Registry ID físico 0.0.16.3:** `monsterspellbooks:brimstone_wrath` (**`COUNTED_EXACT` apenas identidade estática**, obtida de `getSpellResource` compilado; nenhum comportamento deduzido do nome).
- **Escola e configuração individual:** `NÃO VERIFICADO`; mesmo a escola Necro observada no source não prova a associação deste registro no binário instalado.
- **Custos, cooldown, level/rarity, targeting, efeito, dano/cura, summons, filtros PvP/boss, persistência, aquisição e world safety:** `NÃO VERIFICADO`. Nenhum desses mecanismos é inferido do nome.
- **Identidade semântica:** `COUNTED_EXACT` para ID/registro estático já inventariado no lote de 98; **+0** novos objetos. O feitiço pertence ao provider, com casting/mana/cooldown hospedados no Iron's. Black Arcana não reproduz o efeito.
- **Fonte factual:** [inventário](SPELL-CATALOG.md), [proveniência](EVIDENCE-AND-PROVENANCE.md), [limites de runtime](RUNTIME-AND-SAFETY.md).

### 24 — `CAUTERIZING_TOUCH`

- **Família organizacional na fonte:** `fire`; não comprova `SchoolType` individual.
- **Constante em `ModSpellRegistry`:** `CAUTERIZING_TOUCH`.
- **Classe da fonte pública:** `CauterizingTouchSpell`.
- **Classe compilada SHA-exata 0.0.16.3:** `net.redreaper.monsterspellbooks.spells.fire.CauterizingTouchSpell` ([dados da auditoria](../../../../docs/qa/monsters_spellbooks_00163_exact_registry_ids.json)).
- **Registry ID físico 0.0.16.3:** `monsterspellbooks:cauterizing_touch` (**`COUNTED_EXACT` apenas identidade estática**, obtida de `getSpellResource` compilado; nenhum comportamento deduzido do nome).
- **Escola e configuração individual:** `NÃO VERIFICADO`; mesmo a escola Necro observada no source não prova a associação deste registro no binário instalado.
- **Custos, cooldown, level/rarity, targeting, efeito, dano/cura, summons, filtros PvP/boss, persistência, aquisição e world safety:** `NÃO VERIFICADO`. Nenhum desses mecanismos é inferido do nome.
- **Identidade semântica:** `COUNTED_EXACT` para ID/registro estático já inventariado no lote de 98; **+0** novos objetos. O feitiço pertence ao provider, com casting/mana/cooldown hospedados no Iron's. Black Arcana não reproduz o efeito.
- **Fonte factual:** [inventário](SPELL-CATALOG.md), [proveniência](EVIDENCE-AND-PROVENANCE.md), [limites de runtime](RUNTIME-AND-SAFETY.md).

### 25 — `FRENZIED_BURST`

- **Família organizacional na fonte:** `fire`; não comprova `SchoolType` individual.
- **Constante em `ModSpellRegistry`:** `FRENZIED_BURST`.
- **Classe da fonte pública:** `FrenziedBurstSpell`.
- **Classe compilada SHA-exata 0.0.16.3:** `net.redreaper.monsterspellbooks.spells.fire.FrenziedBurstSpell` ([dados da auditoria](../../../../docs/qa/monsters_spellbooks_00163_exact_registry_ids.json)).
- **Registry ID físico 0.0.16.3:** `monsterspellbooks:frenzied_burst` (**`COUNTED_EXACT` apenas identidade estática**, obtida de `getSpellResource` compilado; nenhum comportamento deduzido do nome).
- **Escola e configuração individual:** `NÃO VERIFICADO`; mesmo a escola Necro observada no source não prova a associação deste registro no binário instalado.
- **Custos, cooldown, level/rarity, targeting, efeito, dano/cura, summons, filtros PvP/boss, persistência, aquisição e world safety:** `NÃO VERIFICADO`. Nenhum desses mecanismos é inferido do nome.
- **Identidade semântica:** `COUNTED_EXACT` para ID/registro estático já inventariado no lote de 98; **+0** novos objetos. O feitiço pertence ao provider, com casting/mana/cooldown hospedados no Iron's. Black Arcana não reproduz o efeito.
- **Fonte factual:** [inventário](SPELL-CATALOG.md), [proveniência](EVIDENCE-AND-PROVENANCE.md), [limites de runtime](RUNTIME-AND-SAFETY.md).

### 26 — `FRENZIED_STORM`

- **Família organizacional na fonte:** `fire`; não comprova `SchoolType` individual.
- **Constante em `ModSpellRegistry`:** `FRENZIED_STORM`.
- **Classe da fonte pública:** `FrenziedStormSpell`.
- **Classe compilada SHA-exata 0.0.16.3:** `net.redreaper.monsterspellbooks.spells.fire.FrenziedStormSpell` ([dados da auditoria](../../../../docs/qa/monsters_spellbooks_00163_exact_registry_ids.json)).
- **Registry ID físico 0.0.16.3:** `monsterspellbooks:frenzied_storm` (**`COUNTED_EXACT` apenas identidade estática**, obtida de `getSpellResource` compilado; nenhum comportamento deduzido do nome).
- **Escola e configuração individual:** `NÃO VERIFICADO`; mesmo a escola Necro observada no source não prova a associação deste registro no binário instalado.
- **Custos, cooldown, level/rarity, targeting, efeito, dano/cura, summons, filtros PvP/boss, persistência, aquisição e world safety:** `NÃO VERIFICADO`. Nenhum desses mecanismos é inferido do nome.
- **Identidade semântica:** `COUNTED_EXACT` para ID/registro estático já inventariado no lote de 98; **+0** novos objetos. O feitiço pertence ao provider, com casting/mana/cooldown hospedados no Iron's. Black Arcana não reproduz o efeito.
- **Fonte factual:** [inventário](SPELL-CATALOG.md), [proveniência](EVIDENCE-AND-PROVENANCE.md), [limites de runtime](RUNTIME-AND-SAFETY.md).

### 27 — `FRENZY_SURGE`

- **Família organizacional na fonte:** `fire`; não comprova `SchoolType` individual.
- **Constante em `ModSpellRegistry`:** `FRENZY_SURGE`.
- **Classe da fonte pública:** `FrenzySurgeSpell`.
- **Classe compilada SHA-exata 0.0.16.3:** `net.redreaper.monsterspellbooks.spells.fire.FrenzySurgeSpell` ([dados da auditoria](../../../../docs/qa/monsters_spellbooks_00163_exact_registry_ids.json)).
- **Registry ID físico 0.0.16.3:** `monsterspellbooks:frenzy_surge` (**`COUNTED_EXACT` apenas identidade estática**, obtida de `getSpellResource` compilado; nenhum comportamento deduzido do nome).
- **Escola e configuração individual:** `NÃO VERIFICADO`; mesmo a escola Necro observada no source não prova a associação deste registro no binário instalado.
- **Custos, cooldown, level/rarity, targeting, efeito, dano/cura, summons, filtros PvP/boss, persistência, aquisição e world safety:** `NÃO VERIFICADO`. Nenhum desses mecanismos é inferido do nome.
- **Identidade semântica:** `COUNTED_EXACT` para ID/registro estático já inventariado no lote de 98; **+0** novos objetos. O feitiço pertence ao provider, com casting/mana/cooldown hospedados no Iron's. Black Arcana não reproduz o efeito.
- **Fonte factual:** [inventário](SPELL-CATALOG.md), [proveniência](EVIDENCE-AND-PROVENANCE.md), [limites de runtime](RUNTIME-AND-SAFETY.md).

### 28 — `NAPALM_ORB`

- **Família organizacional na fonte:** `fire`; não comprova `SchoolType` individual.
- **Constante em `ModSpellRegistry`:** `NAPALM_ORB`.
- **Classe da fonte pública:** `NapalmOrbSpell`.
- **Classe compilada SHA-exata 0.0.16.3:** `net.redreaper.monsterspellbooks.spells.fire.NapalmOrbSpell` ([dados da auditoria](../../../../docs/qa/monsters_spellbooks_00163_exact_registry_ids.json)).
- **Registry ID físico 0.0.16.3:** `monsterspellbooks:napalm_orb` (**`COUNTED_EXACT` apenas identidade estática**, obtida de `getSpellResource` compilado; nenhum comportamento deduzido do nome).
- **Escola e configuração individual:** `NÃO VERIFICADO`; mesmo a escola Necro observada no source não prova a associação deste registro no binário instalado.
- **Custos, cooldown, level/rarity, targeting, efeito, dano/cura, summons, filtros PvP/boss, persistência, aquisição e world safety:** `NÃO VERIFICADO`. Nenhum desses mecanismos é inferido do nome.
- **Identidade semântica:** `COUNTED_EXACT` para ID/registro estático já inventariado no lote de 98; **+0** novos objetos. O feitiço pertence ao provider, com casting/mana/cooldown hospedados no Iron's. Black Arcana não reproduz o efeito.
- **Fonte factual:** [inventário](SPELL-CATALOG.md), [proveniência](EVIDENCE-AND-PROVENANCE.md), [limites de runtime](RUNTIME-AND-SAFETY.md).

### 29 — `OVERHEAT`

- **Família organizacional na fonte:** `fire`; não comprova `SchoolType` individual.
- **Constante em `ModSpellRegistry`:** `OVERHEAT`.
- **Classe da fonte pública:** `OverheatSpell`.
- **Classe compilada SHA-exata 0.0.16.3:** `net.redreaper.monsterspellbooks.spells.fire.OverheatSpell` ([dados da auditoria](../../../../docs/qa/monsters_spellbooks_00163_exact_registry_ids.json)).
- **Registry ID físico 0.0.16.3:** `monsterspellbooks:overheat` (**`COUNTED_EXACT` apenas identidade estática**, obtida de `getSpellResource` compilado; nenhum comportamento deduzido do nome).
- **Escola e configuração individual:** `NÃO VERIFICADO`; mesmo a escola Necro observada no source não prova a associação deste registro no binário instalado.
- **Custos, cooldown, level/rarity, targeting, efeito, dano/cura, summons, filtros PvP/boss, persistência, aquisição e world safety:** `NÃO VERIFICADO`. Nenhum desses mecanismos é inferido do nome.
- **Identidade semântica:** `COUNTED_EXACT` para ID/registro estático já inventariado no lote de 98; **+0** novos objetos. O feitiço pertence ao provider, com casting/mana/cooldown hospedados no Iron's. Black Arcana não reproduz o efeito.
- **Fonte factual:** [inventário](SPELL-CATALOG.md), [proveniência](EVIDENCE-AND-PROVENANCE.md), [limites de runtime](RUNTIME-AND-SAFETY.md).

### 30 — `WRATH`

- **Família organizacional na fonte:** `fire`; não comprova `SchoolType` individual.
- **Constante em `ModSpellRegistry`:** `WRATH`.
- **Classe da fonte pública:** `WrathSpell`.
- **Classe compilada SHA-exata 0.0.16.3:** `net.redreaper.monsterspellbooks.spells.fire.WrathSpell` ([dados da auditoria](../../../../docs/qa/monsters_spellbooks_00163_exact_registry_ids.json)).
- **Registry ID físico 0.0.16.3:** `monsterspellbooks:wrath` (**`COUNTED_EXACT` apenas identidade estática**, obtida de `getSpellResource` compilado; nenhum comportamento deduzido do nome).
- **Escola e configuração individual:** `NÃO VERIFICADO`; mesmo a escola Necro observada no source não prova a associação deste registro no binário instalado.
- **Custos, cooldown, level/rarity, targeting, efeito, dano/cura, summons, filtros PvP/boss, persistência, aquisição e world safety:** `NÃO VERIFICADO`. Nenhum desses mecanismos é inferido do nome.
- **Identidade semântica:** `COUNTED_EXACT` para ID/registro estático já inventariado no lote de 98; **+0** novos objetos. O feitiço pertence ao provider, com casting/mana/cooldown hospedados no Iron's. Black Arcana não reproduz o efeito.
- **Fonte factual:** [inventário](SPELL-CATALOG.md), [proveniência](EVIDENCE-AND-PROVENANCE.md), [limites de runtime](RUNTIME-AND-SAFETY.md).


## Família `holy` — 4 registros

### 31 — `DIVINE_INTERVENTION`

- **Família organizacional na fonte:** `holy`; não comprova `SchoolType` individual.
- **Constante em `ModSpellRegistry`:** `DIVINE_INTERVENTION`.
- **Classe da fonte pública:** `DivineInterventionSpell`.
- **Classe compilada SHA-exata 0.0.16.3:** `net.redreaper.monsterspellbooks.spells.holy.DivineInterventionSpell` ([dados da auditoria](../../../../docs/qa/monsters_spellbooks_00163_exact_registry_ids.json)).
- **Registry ID físico 0.0.16.3:** `monsterspellbooks:divine_intervention` (**`COUNTED_EXACT` apenas identidade estática**, obtida de `getSpellResource` compilado; nenhum comportamento deduzido do nome).
- **Escola e configuração individual:** `NÃO VERIFICADO`; mesmo a escola Necro observada no source não prova a associação deste registro no binário instalado.
- **Custos, cooldown, level/rarity, targeting, efeito, dano/cura, summons, filtros PvP/boss, persistência, aquisição e world safety:** `NÃO VERIFICADO`. Nenhum desses mecanismos é inferido do nome.
- **Identidade semântica:** `COUNTED_EXACT` para ID/registro estático já inventariado no lote de 98; **+0** novos objetos. O feitiço pertence ao provider, com casting/mana/cooldown hospedados no Iron's. Black Arcana não reproduz o efeito.
- **Fonte factual:** [inventário](SPELL-CATALOG.md), [proveniência](EVIDENCE-AND-PROVENANCE.md), [limites de runtime](RUNTIME-AND-SAFETY.md).

### 32 — `HALLOW_SLASH`

- **Família organizacional na fonte:** `holy`; não comprova `SchoolType` individual.
- **Constante em `ModSpellRegistry`:** `HALLOW_SLASH`.
- **Classe da fonte pública:** `HallowSlashSpell`.
- **Classe compilada SHA-exata 0.0.16.3:** `net.redreaper.monsterspellbooks.spells.holy.HallowSlashSpell` ([dados da auditoria](../../../../docs/qa/monsters_spellbooks_00163_exact_registry_ids.json)).
- **Registry ID físico 0.0.16.3:** `monsterspellbooks:hallow_slash` (**`COUNTED_EXACT` apenas identidade estática**, obtida de `getSpellResource` compilado; nenhum comportamento deduzido do nome).
- **Escola e configuração individual:** `NÃO VERIFICADO`; mesmo a escola Necro observada no source não prova a associação deste registro no binário instalado.
- **Custos, cooldown, level/rarity, targeting, efeito, dano/cura, summons, filtros PvP/boss, persistência, aquisição e world safety:** `NÃO VERIFICADO`. Nenhum desses mecanismos é inferido do nome.
- **Identidade semântica:** `COUNTED_EXACT` para ID/registro estático já inventariado no lote de 98; **+0** novos objetos. O feitiço pertence ao provider, com casting/mana/cooldown hospedados no Iron's. Black Arcana não reproduz o efeito.
- **Fonte factual:** [inventário](SPELL-CATALOG.md), [proveniência](EVIDENCE-AND-PROVENANCE.md), [limites de runtime](RUNTIME-AND-SAFETY.md).

### 33 — `PALADIN_THROW`

- **Família organizacional na fonte:** `holy`; não comprova `SchoolType` individual.
- **Constante em `ModSpellRegistry`:** `PALADIN_THROW`.
- **Classe da fonte pública:** `PaladinThrowSpell`.
- **Classe compilada SHA-exata 0.0.16.3:** `net.redreaper.monsterspellbooks.spells.holy.PaladinThrowSpell` ([dados da auditoria](../../../../docs/qa/monsters_spellbooks_00163_exact_registry_ids.json)).
- **Registry ID físico 0.0.16.3:** `monsterspellbooks:paladin_throw` (**`COUNTED_EXACT` apenas identidade estática**, obtida de `getSpellResource` compilado; nenhum comportamento deduzido do nome).
- **Escola e configuração individual:** `NÃO VERIFICADO`; mesmo a escola Necro observada no source não prova a associação deste registro no binário instalado.
- **Custos, cooldown, level/rarity, targeting, efeito, dano/cura, summons, filtros PvP/boss, persistência, aquisição e world safety:** `NÃO VERIFICADO`. Nenhum desses mecanismos é inferido do nome.
- **Identidade semântica:** `COUNTED_EXACT` para ID/registro estático já inventariado no lote de 98; **+0** novos objetos. O feitiço pertence ao provider, com casting/mana/cooldown hospedados no Iron's. Black Arcana não reproduz o efeito.
- **Fonte factual:** [inventário](SPELL-CATALOG.md), [proveniência](EVIDENCE-AND-PROVENANCE.md), [limites de runtime](RUNTIME-AND-SAFETY.md).

### 34 — `SUMMON_AEGIS_PATROL`

- **Família organizacional na fonte:** `holy`; não comprova `SchoolType` individual.
- **Constante em `ModSpellRegistry`:** `SUMMON_AEGIS_PATROL`.
- **Classe da fonte pública:** `SummonAegisPatrolSpell`.
- **Classe compilada SHA-exata 0.0.16.3:** `net.redreaper.monsterspellbooks.spells.holy.SummonAegisPatrolSpell` ([dados da auditoria](../../../../docs/qa/monsters_spellbooks_00163_exact_registry_ids.json)).
- **Registry ID físico 0.0.16.3:** `monsterspellbooks:summon_aegis_patrol` (**`COUNTED_EXACT` apenas identidade estática**, obtida de `getSpellResource` compilado; nenhum comportamento deduzido do nome).
- **Escola e configuração individual:** `NÃO VERIFICADO`; mesmo a escola Necro observada no source não prova a associação deste registro no binário instalado.
- **Custos, cooldown, level/rarity, targeting, efeito, dano/cura, summons, filtros PvP/boss, persistência, aquisição e world safety:** `NÃO VERIFICADO`. Nenhum desses mecanismos é inferido do nome.
- **Identidade semântica:** `COUNTED_EXACT` para ID/registro estático já inventariado no lote de 98; **+0** novos objetos. O feitiço pertence ao provider, com casting/mana/cooldown hospedados no Iron's. Black Arcana não reproduz o efeito.
- **Fonte factual:** [inventário](SPELL-CATALOG.md), [proveniência](EVIDENCE-AND-PROVENANCE.md), [limites de runtime](RUNTIME-AND-SAFETY.md).


## Família `hydro` — 8 registros

### 35 — `BUBBLE_SPRAY`

- **Família organizacional na fonte:** `hydro`; não comprova `SchoolType` individual.
- **Constante em `ModSpellRegistry`:** `BUBBLE_SPRAY`.
- **Classe da fonte pública:** `BubbleSpraySpell`.
- **Classe compilada SHA-exata 0.0.16.3:** `net.redreaper.monsterspellbooks.spells.hydro.BubbleSpraySpell` ([dados da auditoria](../../../../docs/qa/monsters_spellbooks_00163_exact_registry_ids.json)).
- **Registry ID físico 0.0.16.3:** `monsterspellbooks:bubble_spray` (**`COUNTED_EXACT` apenas identidade estática**, obtida de `getSpellResource` compilado; nenhum comportamento deduzido do nome).
- **Escola e configuração individual:** `NÃO VERIFICADO`; mesmo a escola Necro observada no source não prova a associação deste registro no binário instalado.
- **Custos, cooldown, level/rarity, targeting, efeito, dano/cura, summons, filtros PvP/boss, persistência, aquisição e world safety:** `NÃO VERIFICADO`. Nenhum desses mecanismos é inferido do nome.
- **Identidade semântica:** `COUNTED_EXACT` para ID/registro estático já inventariado no lote de 98; **+0** novos objetos. O feitiço pertence ao provider, com casting/mana/cooldown hospedados no Iron's. Black Arcana não reproduz o efeito.
- **Fonte factual:** [inventário](SPELL-CATALOG.md), [proveniência](EVIDENCE-AND-PROVENANCE.md), [limites de runtime](RUNTIME-AND-SAFETY.md).

### 36 — `EFFERVESCENCE_BUBBLE`

- **Família organizacional na fonte:** `hydro`; não comprova `SchoolType` individual.
- **Constante em `ModSpellRegistry`:** `EFFERVESCENCE_BUBBLE`.
- **Classe da fonte pública:** `EffervescenceBubbleSpell`.
- **Classe compilada SHA-exata 0.0.16.3:** `net.redreaper.monsterspellbooks.spells.hydro.EffervescenceBubbleSpell` ([dados da auditoria](../../../../docs/qa/monsters_spellbooks_00163_exact_registry_ids.json)).
- **Registry ID físico 0.0.16.3:** `monsterspellbooks:effervescence_bubble` (**`COUNTED_EXACT` apenas identidade estática**, obtida de `getSpellResource` compilado; nenhum comportamento deduzido do nome).
- **Escola e configuração individual:** `NÃO VERIFICADO`; mesmo a escola Necro observada no source não prova a associação deste registro no binário instalado.
- **Custos, cooldown, level/rarity, targeting, efeito, dano/cura, summons, filtros PvP/boss, persistência, aquisição e world safety:** `NÃO VERIFICADO`. Nenhum desses mecanismos é inferido do nome.
- **Identidade semântica:** `COUNTED_EXACT` para ID/registro estático já inventariado no lote de 98; **+0** novos objetos. O feitiço pertence ao provider, com casting/mana/cooldown hospedados no Iron's. Black Arcana não reproduz o efeito.
- **Fonte factual:** [inventário](SPELL-CATALOG.md), [proveniência](EVIDENCE-AND-PROVENANCE.md), [limites de runtime](RUNTIME-AND-SAFETY.md).

### 37 — `GLOW_INK_RELEASE`

- **Família organizacional na fonte:** `hydro`; não comprova `SchoolType` individual.
- **Constante em `ModSpellRegistry`:** `GLOW_INK_RELEASE`.
- **Classe da fonte pública:** `GlowInkReleaseSpell`.
- **Classe compilada SHA-exata 0.0.16.3:** `net.redreaper.monsterspellbooks.spells.hydro.GlowInkReleaseSpell` ([dados da auditoria](../../../../docs/qa/monsters_spellbooks_00163_exact_registry_ids.json)).
- **Registry ID físico 0.0.16.3:** `monsterspellbooks:glow_ink_release` (**`COUNTED_EXACT` apenas identidade estática**, obtida de `getSpellResource` compilado; nenhum comportamento deduzido do nome).
- **Escola e configuração individual:** `NÃO VERIFICADO`; mesmo a escola Necro observada no source não prova a associação deste registro no binário instalado.
- **Custos, cooldown, level/rarity, targeting, efeito, dano/cura, summons, filtros PvP/boss, persistência, aquisição e world safety:** `NÃO VERIFICADO`. Nenhum desses mecanismos é inferido do nome.
- **Identidade semântica:** `COUNTED_EXACT` para ID/registro estático já inventariado no lote de 98; **+0** novos objetos. O feitiço pertence ao provider, com casting/mana/cooldown hospedados no Iron's. Black Arcana não reproduz o efeito.
- **Fonte factual:** [inventário](SPELL-CATALOG.md), [proveniência](EVIDENCE-AND-PROVENANCE.md), [limites de runtime](RUNTIME-AND-SAFETY.md).

### 38 — `INK_BOMB`

- **Família organizacional na fonte:** `hydro`; não comprova `SchoolType` individual.
- **Constante em `ModSpellRegistry`:** `INK_BOMB`.
- **Classe da fonte pública:** `InkBombSpell`.
- **Classe compilada SHA-exata 0.0.16.3:** `net.redreaper.monsterspellbooks.spells.hydro.InkBombSpell` ([dados da auditoria](../../../../docs/qa/monsters_spellbooks_00163_exact_registry_ids.json)).
- **Registry ID físico 0.0.16.3:** `monsterspellbooks:ink_bomb` (**`COUNTED_EXACT` apenas identidade estática**, obtida de `getSpellResource` compilado; nenhum comportamento deduzido do nome).
- **Escola e configuração individual:** `NÃO VERIFICADO`; mesmo a escola Necro observada no source não prova a associação deste registro no binário instalado.
- **Custos, cooldown, level/rarity, targeting, efeito, dano/cura, summons, filtros PvP/boss, persistência, aquisição e world safety:** `NÃO VERIFICADO`. Nenhum desses mecanismos é inferido do nome.
- **Identidade semântica:** `COUNTED_EXACT` para ID/registro estático já inventariado no lote de 98; **+0** novos objetos. O feitiço pertence ao provider, com casting/mana/cooldown hospedados no Iron's. Black Arcana não reproduz o efeito.
- **Fonte factual:** [inventário](SPELL-CATALOG.md), [proveniência](EVIDENCE-AND-PROVENANCE.md), [limites de runtime](RUNTIME-AND-SAFETY.md).

### 39 — `RAZORBLADE_TYPHOON`

- **Família organizacional na fonte:** `hydro`; não comprova `SchoolType` individual.
- **Constante em `ModSpellRegistry`:** `RAZORBLADE_TYPHOON`.
- **Classe da fonte pública:** `RazorbladeTyphoonSpell`.
- **Classe compilada SHA-exata 0.0.16.3:** `net.redreaper.monsterspellbooks.spells.hydro.RazorbladeTyphoonSpell` ([dados da auditoria](../../../../docs/qa/monsters_spellbooks_00163_exact_registry_ids.json)).
- **Registry ID físico 0.0.16.3:** `monsterspellbooks:razor_typhoon` (**`COUNTED_EXACT` apenas identidade estática**, obtida de `getSpellResource` compilado; nenhum comportamento deduzido do nome).
- **Escola e configuração individual:** `NÃO VERIFICADO`; mesmo a escola Necro observada no source não prova a associação deste registro no binário instalado.
- **Custos, cooldown, level/rarity, targeting, efeito, dano/cura, summons, filtros PvP/boss, persistência, aquisição e world safety:** `NÃO VERIFICADO`. Nenhum desses mecanismos é inferido do nome.
- **Identidade semântica:** `COUNTED_EXACT` para ID/registro estático já inventariado no lote de 98; **+0** novos objetos. O feitiço pertence ao provider, com casting/mana/cooldown hospedados no Iron's. Black Arcana não reproduz o efeito.
- **Fonte factual:** [inventário](SPELL-CATALOG.md), [proveniência](EVIDENCE-AND-PROVENANCE.md), [limites de runtime](RUNTIME-AND-SAFETY.md).

### 40 — `RIPTIDE_DASH`

- **Família organizacional na fonte:** `hydro`; não comprova `SchoolType` individual.
- **Constante em `ModSpellRegistry`:** `RIPTIDE_DASH`.
- **Classe da fonte pública:** `RiptideDashSpell`.
- **Classe compilada SHA-exata 0.0.16.3:** `net.redreaper.monsterspellbooks.spells.hydro.RiptideDashSpell` ([dados da auditoria](../../../../docs/qa/monsters_spellbooks_00163_exact_registry_ids.json)).
- **Registry ID físico 0.0.16.3:** `monsterspellbooks:riptide_dash` (**`COUNTED_EXACT` apenas identidade estática**, obtida de `getSpellResource` compilado; nenhum comportamento deduzido do nome).
- **Escola e configuração individual:** `NÃO VERIFICADO`; mesmo a escola Necro observada no source não prova a associação deste registro no binário instalado.
- **Custos, cooldown, level/rarity, targeting, efeito, dano/cura, summons, filtros PvP/boss, persistência, aquisição e world safety:** `NÃO VERIFICADO`. Nenhum desses mecanismos é inferido do nome.
- **Identidade semântica:** `COUNTED_EXACT` para ID/registro estático já inventariado no lote de 98; **+0** novos objetos. O feitiço pertence ao provider, com casting/mana/cooldown hospedados no Iron's. Black Arcana não reproduz o efeito.
- **Fonte factual:** [inventário](SPELL-CATALOG.md), [proveniência](EVIDENCE-AND-PROVENANCE.md), [limites de runtime](RUNTIME-AND-SAFETY.md).

### 41 — `SUMMON_PRISMARINE_SQUAD`

- **Família organizacional na fonte:** `hydro`; não comprova `SchoolType` individual.
- **Constante em `ModSpellRegistry`:** `SUMMON_PRISMARINE_SQUAD`.
- **Classe da fonte pública:** `SummonPrismarineSquadSpell`.
- **Classe compilada SHA-exata 0.0.16.3:** `net.redreaper.monsterspellbooks.spells.hydro.SummonPrismarineSquadSpell` ([dados da auditoria](../../../../docs/qa/monsters_spellbooks_00163_exact_registry_ids.json)).
- **Registry ID físico 0.0.16.3:** `monsterspellbooks:summon_prismarine_squad` (**`COUNTED_EXACT` apenas identidade estática**, obtida de `getSpellResource` compilado; nenhum comportamento deduzido do nome).
- **Escola e configuração individual:** `NÃO VERIFICADO`; mesmo a escola Necro observada no source não prova a associação deste registro no binário instalado.
- **Custos, cooldown, level/rarity, targeting, efeito, dano/cura, summons, filtros PvP/boss, persistência, aquisição e world safety:** `NÃO VERIFICADO`. Nenhum desses mecanismos é inferido do nome.
- **Identidade semântica:** `COUNTED_EXACT` para ID/registro estático já inventariado no lote de 98; **+0** novos objetos. O feitiço pertence ao provider, com casting/mana/cooldown hospedados no Iron's. Black Arcana não reproduz o efeito.
- **Fonte factual:** [inventário](SPELL-CATALOG.md), [proveniência](EVIDENCE-AND-PROVENANCE.md), [limites de runtime](RUNTIME-AND-SAFETY.md).

### 42 — `WATER_TRIDENT`

- **Família organizacional na fonte:** `hydro`; não comprova `SchoolType` individual.
- **Constante em `ModSpellRegistry`:** `WATER_TRIDENT`.
- **Classe da fonte pública:** `WaterTridentSpell`.
- **Classe compilada SHA-exata 0.0.16.3:** `net.redreaper.monsterspellbooks.spells.hydro.WaterTridentSpell` ([dados da auditoria](../../../../docs/qa/monsters_spellbooks_00163_exact_registry_ids.json)).
- **Registry ID físico 0.0.16.3:** `monsterspellbooks:water_trident` (**`COUNTED_EXACT` apenas identidade estática**, obtida de `getSpellResource` compilado; nenhum comportamento deduzido do nome).
- **Escola e configuração individual:** `NÃO VERIFICADO`; mesmo a escola Necro observada no source não prova a associação deste registro no binário instalado.
- **Custos, cooldown, level/rarity, targeting, efeito, dano/cura, summons, filtros PvP/boss, persistência, aquisição e world safety:** `NÃO VERIFICADO`. Nenhum desses mecanismos é inferido do nome.
- **Identidade semântica:** `COUNTED_EXACT` para ID/registro estático já inventariado no lote de 98; **+0** novos objetos. O feitiço pertence ao provider, com casting/mana/cooldown hospedados no Iron's. Black Arcana não reproduz o efeito.
- **Fonte factual:** [inventário](SPELL-CATALOG.md), [proveniência](EVIDENCE-AND-PROVENANCE.md), [limites de runtime](RUNTIME-AND-SAFETY.md).


## Família `ice` — 8 registros

### 43 — `BLIZZARD_ASPECT`

- **Família organizacional na fonte:** `ice`; não comprova `SchoolType` individual.
- **Constante em `ModSpellRegistry`:** `BLIZZARD_ASPECT`.
- **Classe da fonte pública:** `BlizzardAspectSpell`.
- **Classe compilada SHA-exata 0.0.16.3:** `net.redreaper.monsterspellbooks.spells.ice.BlizzardAspectSpell` ([dados da auditoria](../../../../docs/qa/monsters_spellbooks_00163_exact_registry_ids.json)).
- **Registry ID físico 0.0.16.3:** `monsterspellbooks:blizzard_aspect` (**`COUNTED_EXACT` apenas identidade estática**, obtida de `getSpellResource` compilado; nenhum comportamento deduzido do nome).
- **Escola e configuração individual:** `NÃO VERIFICADO`; mesmo a escola Necro observada no source não prova a associação deste registro no binário instalado.
- **Custos, cooldown, level/rarity, targeting, efeito, dano/cura, summons, filtros PvP/boss, persistência, aquisição e world safety:** `NÃO VERIFICADO`. Nenhum desses mecanismos é inferido do nome.
- **Identidade semântica:** `COUNTED_EXACT` para ID/registro estático já inventariado no lote de 98; **+0** novos objetos. O feitiço pertence ao provider, com casting/mana/cooldown hospedados no Iron's. Black Arcana não reproduz o efeito.
- **Fonte factual:** [inventário](SPELL-CATALOG.md), [proveniência](EVIDENCE-AND-PROVENANCE.md), [limites de runtime](RUNTIME-AND-SAFETY.md).

### 44 — `FROST_BREATH`

- **Família organizacional na fonte:** `ice`; não comprova `SchoolType` individual.
- **Constante em `ModSpellRegistry`:** `FROST_BREATH`.
- **Classe da fonte pública:** `FrostBreathSpell`.
- **Classe compilada SHA-exata 0.0.16.3:** `net.redreaper.monsterspellbooks.spells.ice.FrostBreathSpell` ([dados da auditoria](../../../../docs/qa/monsters_spellbooks_00163_exact_registry_ids.json)).
- **Registry ID físico 0.0.16.3:** `monsterspellbooks:frost_breath` (**`COUNTED_EXACT` apenas identidade estática**, obtida de `getSpellResource` compilado; nenhum comportamento deduzido do nome).
- **Escola e configuração individual:** `NÃO VERIFICADO`; mesmo a escola Necro observada no source não prova a associação deste registro no binário instalado.
- **Custos, cooldown, level/rarity, targeting, efeito, dano/cura, summons, filtros PvP/boss, persistência, aquisição e world safety:** `NÃO VERIFICADO`. Nenhum desses mecanismos é inferido do nome.
- **Identidade semântica:** `COUNTED_EXACT` para ID/registro estático já inventariado no lote de 98; **+0** novos objetos. O feitiço pertence ao provider, com casting/mana/cooldown hospedados no Iron's. Black Arcana não reproduz o efeito.
- **Fonte factual:** [inventário](SPELL-CATALOG.md), [proveniência](EVIDENCE-AND-PROVENANCE.md), [limites de runtime](RUNTIME-AND-SAFETY.md).

### 45 — `FROST_COATING`

- **Família organizacional na fonte:** `ice`; não comprova `SchoolType` individual.
- **Constante em `ModSpellRegistry`:** `FROST_COATING`.
- **Classe da fonte pública:** `FrostCoatingSpell`.
- **Classe compilada SHA-exata 0.0.16.3:** `net.redreaper.monsterspellbooks.spells.ice.FrostCoatingSpell` ([dados da auditoria](../../../../docs/qa/monsters_spellbooks_00163_exact_registry_ids.json)).
- **Registry ID físico 0.0.16.3:** `monsterspellbooks:frost_coating` (**`COUNTED_EXACT` apenas identidade estática**, obtida de `getSpellResource` compilado; nenhum comportamento deduzido do nome).
- **Escola e configuração individual:** `NÃO VERIFICADO`; mesmo a escola Necro observada no source não prova a associação deste registro no binário instalado.
- **Custos, cooldown, level/rarity, targeting, efeito, dano/cura, summons, filtros PvP/boss, persistência, aquisição e world safety:** `NÃO VERIFICADO`. Nenhum desses mecanismos é inferido do nome.
- **Identidade semântica:** `COUNTED_EXACT` para ID/registro estático já inventariado no lote de 98; **+0** novos objetos. O feitiço pertence ao provider, com casting/mana/cooldown hospedados no Iron's. Black Arcana não reproduz o efeito.
- **Fonte factual:** [inventário](SPELL-CATALOG.md), [proveniência](EVIDENCE-AND-PROVENANCE.md), [limites de runtime](RUNTIME-AND-SAFETY.md).

### 46 — `FROSTED_SNOWBOLT`

- **Família organizacional na fonte:** `ice`; não comprova `SchoolType` individual.
- **Constante em `ModSpellRegistry`:** `FROSTED_SNOWBOLT`.
- **Classe da fonte pública:** `FrostedSnowboltSpell`.
- **Classe compilada SHA-exata 0.0.16.3:** `net.redreaper.monsterspellbooks.spells.ice.FrostedSnowboltSpell` ([dados da auditoria](../../../../docs/qa/monsters_spellbooks_00163_exact_registry_ids.json)).
- **Registry ID físico 0.0.16.3:** `monsterspellbooks:frosted_snowbolt` (**`COUNTED_EXACT` apenas identidade estática**, obtida de `getSpellResource` compilado; nenhum comportamento deduzido do nome).
- **Escola e configuração individual:** `NÃO VERIFICADO`; mesmo a escola Necro observada no source não prova a associação deste registro no binário instalado.
- **Custos, cooldown, level/rarity, targeting, efeito, dano/cura, summons, filtros PvP/boss, persistência, aquisição e world safety:** `NÃO VERIFICADO`. Nenhum desses mecanismos é inferido do nome.
- **Identidade semântica:** `COUNTED_EXACT` para ID/registro estático já inventariado no lote de 98; **+0** novos objetos. O feitiço pertence ao provider, com casting/mana/cooldown hospedados no Iron's. Black Arcana não reproduz o efeito.
- **Fonte factual:** [inventário](SPELL-CATALOG.md), [proveniência](EVIDENCE-AND-PROVENANCE.md), [limites de runtime](RUNTIME-AND-SAFETY.md).

### 47 — `ICE_ARSENAL`

- **Família organizacional na fonte:** `ice`; não comprova `SchoolType` individual.
- **Constante em `ModSpellRegistry`:** `ICE_ARSENAL`.
- **Classe da fonte pública:** `IceArsenalSpell`.
- **Classe compilada SHA-exata 0.0.16.3:** `net.redreaper.monsterspellbooks.spells.ice.IceArsenalSpell` ([dados da auditoria](../../../../docs/qa/monsters_spellbooks_00163_exact_registry_ids.json)).
- **Registry ID físico 0.0.16.3:** `monsterspellbooks:ice_arsenal` (**`COUNTED_EXACT` apenas identidade estática**, obtida de `getSpellResource` compilado; nenhum comportamento deduzido do nome).
- **Escola e configuração individual:** `NÃO VERIFICADO`; mesmo a escola Necro observada no source não prova a associação deste registro no binário instalado.
- **Custos, cooldown, level/rarity, targeting, efeito, dano/cura, summons, filtros PvP/boss, persistência, aquisição e world safety:** `NÃO VERIFICADO`. Nenhum desses mecanismos é inferido do nome.
- **Identidade semântica:** `COUNTED_EXACT` para ID/registro estático já inventariado no lote de 98; **+0** novos objetos. O feitiço pertence ao provider, com casting/mana/cooldown hospedados no Iron's. Black Arcana não reproduz o efeito.
- **Fonte factual:** [inventário](SPELL-CATALOG.md), [proveniência](EVIDENCE-AND-PROVENANCE.md), [limites de runtime](RUNTIME-AND-SAFETY.md).

### 48 — `ORBITAL_SNOWBALL`

- **Família organizacional na fonte:** `ice`; não comprova `SchoolType` individual.
- **Constante em `ModSpellRegistry`:** `ORBITAL_SNOWBALL`.
- **Classe da fonte pública:** `OrbitalSnowballSpell`.
- **Classe compilada SHA-exata 0.0.16.3:** `net.redreaper.monsterspellbooks.spells.ice.OrbitalSnowballSpell` ([dados da auditoria](../../../../docs/qa/monsters_spellbooks_00163_exact_registry_ids.json)).
- **Registry ID físico 0.0.16.3:** `monsterspellbooks:orbital_snowball` (**`COUNTED_EXACT` apenas identidade estática**, obtida de `getSpellResource` compilado; nenhum comportamento deduzido do nome).
- **Escola e configuração individual:** `NÃO VERIFICADO`; mesmo a escola Necro observada no source não prova a associação deste registro no binário instalado.
- **Custos, cooldown, level/rarity, targeting, efeito, dano/cura, summons, filtros PvP/boss, persistência, aquisição e world safety:** `NÃO VERIFICADO`. Nenhum desses mecanismos é inferido do nome.
- **Identidade semântica:** `COUNTED_EXACT` para ID/registro estático já inventariado no lote de 98; **+0** novos objetos. O feitiço pertence ao provider, com casting/mana/cooldown hospedados no Iron's. Black Arcana não reproduz o efeito.
- **Fonte factual:** [inventário](SPELL-CATALOG.md), [proveniência](EVIDENCE-AND-PROVENANCE.md), [limites de runtime](RUNTIME-AND-SAFETY.md).

### 49 — `SUMMON_ICE_HYDRA`

- **Família organizacional na fonte:** `ice`; não comprova `SchoolType` individual.
- **Constante em `ModSpellRegistry`:** `SUMMON_ICE_HYDRA`.
- **Classe da fonte pública:** `SummonIceHydraSpell`.
- **Classe compilada SHA-exata 0.0.16.3:** `net.redreaper.monsterspellbooks.spells.ice.SummonIceHydraSpell` ([dados da auditoria](../../../../docs/qa/monsters_spellbooks_00163_exact_registry_ids.json)).
- **Registry ID físico 0.0.16.3:** `monsterspellbooks:summon_ice_hydra` (**`COUNTED_EXACT` apenas identidade estática**, obtida de `getSpellResource` compilado; nenhum comportamento deduzido do nome).
- **Escola e configuração individual:** `NÃO VERIFICADO`; mesmo a escola Necro observada no source não prova a associação deste registro no binário instalado.
- **Custos, cooldown, level/rarity, targeting, efeito, dano/cura, summons, filtros PvP/boss, persistência, aquisição e world safety:** `NÃO VERIFICADO`. Nenhum desses mecanismos é inferido do nome.
- **Identidade semântica:** `COUNTED_EXACT` para ID/registro estático já inventariado no lote de 98; **+0** novos objetos. O feitiço pertence ao provider, com casting/mana/cooldown hospedados no Iron's. Black Arcana não reproduz o efeito.
- **Fonte factual:** [inventário](SPELL-CATALOG.md), [proveniência](EVIDENCE-AND-PROVENANCE.md), [limites de runtime](RUNTIME-AND-SAFETY.md).

### 50 — `TUNDRA_TERRAIN`

- **Família organizacional na fonte:** `ice`; não comprova `SchoolType` individual.
- **Constante em `ModSpellRegistry`:** `TUNDRA_TERRAIN`.
- **Classe da fonte pública:** `TundraTerrainSpell`.
- **Classe compilada SHA-exata 0.0.16.3:** `net.redreaper.monsterspellbooks.spells.ice.TundraTerrainSpell` ([dados da auditoria](../../../../docs/qa/monsters_spellbooks_00163_exact_registry_ids.json)).
- **Registry ID físico 0.0.16.3:** `monsterspellbooks:tundra_terrain` (**`COUNTED_EXACT` apenas identidade estática**, obtida de `getSpellResource` compilado; nenhum comportamento deduzido do nome).
- **Escola e configuração individual:** `NÃO VERIFICADO`; mesmo a escola Necro observada no source não prova a associação deste registro no binário instalado.
- **Custos, cooldown, level/rarity, targeting, efeito, dano/cura, summons, filtros PvP/boss, persistência, aquisição e world safety:** `NÃO VERIFICADO`. Nenhum desses mecanismos é inferido do nome.
- **Identidade semântica:** `COUNTED_EXACT` para ID/registro estático já inventariado no lote de 98; **+0** novos objetos. O feitiço pertence ao provider, com casting/mana/cooldown hospedados no Iron's. Black Arcana não reproduz o efeito.
- **Fonte factual:** [inventário](SPELL-CATALOG.md), [proveniência](EVIDENCE-AND-PROVENANCE.md), [limites de runtime](RUNTIME-AND-SAFETY.md).


## Família `lightning` — 14 registros

### 51 — `PRIMORDIAL_FLASH`

- **Família organizacional na fonte:** `lightning`; não comprova `SchoolType` individual.
- **Constante em `ModSpellRegistry`:** `PRIMORDIAL_FLASH`.
- **Classe da fonte pública:** `PrimordialFlashSpell`.
- **Classe compilada SHA-exata 0.0.16.3:** `net.redreaper.monsterspellbooks.spells.lightning.PrimordialFlashSpell` ([dados da auditoria](../../../../docs/qa/monsters_spellbooks_00163_exact_registry_ids.json)).
- **Registry ID físico 0.0.16.3:** `monsterspellbooks:ancient_flash` (**`COUNTED_EXACT` apenas identidade estática**, obtida de `getSpellResource` compilado; nenhum comportamento deduzido do nome).
- **Escola e configuração individual:** `NÃO VERIFICADO`; mesmo a escola Necro observada no source não prova a associação deste registro no binário instalado.
- **Custos, cooldown, level/rarity, targeting, efeito, dano/cura, summons, filtros PvP/boss, persistência, aquisição e world safety:** `NÃO VERIFICADO`. Nenhum desses mecanismos é inferido do nome.
- **Identidade semântica:** `COUNTED_EXACT` para ID/registro estático já inventariado no lote de 98; **+0** novos objetos. O feitiço pertence ao provider, com casting/mana/cooldown hospedados no Iron's. Black Arcana não reproduz o efeito.
- **Fonte factual:** [inventário](SPELL-CATALOG.md), [proveniência](EVIDENCE-AND-PROVENANCE.md), [limites de runtime](RUNTIME-AND-SAFETY.md).

### 52 — `DISCHARGE`

- **Família organizacional na fonte:** `lightning`; não comprova `SchoolType` individual.
- **Constante em `ModSpellRegistry`:** `DISCHARGE`.
- **Classe da fonte pública:** `DischargeSpell`.
- **Classe compilada SHA-exata 0.0.16.3:** `net.redreaper.monsterspellbooks.spells.lightning.DischargeSpell` ([dados da auditoria](../../../../docs/qa/monsters_spellbooks_00163_exact_registry_ids.json)).
- **Registry ID físico 0.0.16.3:** `monsterspellbooks:discharge` (**`COUNTED_EXACT` apenas identidade estática**, obtida de `getSpellResource` compilado; nenhum comportamento deduzido do nome).
- **Escola e configuração individual:** `NÃO VERIFICADO`; mesmo a escola Necro observada no source não prova a associação deste registro no binário instalado.
- **Custos, cooldown, level/rarity, targeting, efeito, dano/cura, summons, filtros PvP/boss, persistência, aquisição e world safety:** `NÃO VERIFICADO`. Nenhum desses mecanismos é inferido do nome.
- **Identidade semântica:** `COUNTED_EXACT` para ID/registro estático já inventariado no lote de 98; **+0** novos objetos. O feitiço pertence ao provider, com casting/mana/cooldown hospedados no Iron's. Black Arcana não reproduz o efeito.
- **Fonte factual:** [inventário](SPELL-CATALOG.md), [proveniência](EVIDENCE-AND-PROVENANCE.md), [limites de runtime](RUNTIME-AND-SAFETY.md).

### 53 — `RAIJIN_JUDGEMENT`

- **Família organizacional na fonte:** `lightning`; não comprova `SchoolType` individual.
- **Constante em `ModSpellRegistry`:** `RAIJIN_JUDGEMENT`.
- **Classe da fonte pública:** `RaijinJudgementSpell`.
- **Classe compilada SHA-exata 0.0.16.3:** `net.redreaper.monsterspellbooks.spells.lightning.RaijinJudgementSpell` ([dados da auditoria](../../../../docs/qa/monsters_spellbooks_00163_exact_registry_ids.json)).
- **Registry ID físico 0.0.16.3:** `monsterspellbooks:raijin_judgement` (**`COUNTED_EXACT` apenas identidade estática**, obtida de `getSpellResource` compilado; nenhum comportamento deduzido do nome).
- **Escola e configuração individual:** `NÃO VERIFICADO`; mesmo a escola Necro observada no source não prova a associação deste registro no binário instalado.
- **Custos, cooldown, level/rarity, targeting, efeito, dano/cura, summons, filtros PvP/boss, persistência, aquisição e world safety:** `NÃO VERIFICADO`. Nenhum desses mecanismos é inferido do nome.
- **Identidade semântica:** `COUNTED_EXACT` para ID/registro estático já inventariado no lote de 98; **+0** novos objetos. O feitiço pertence ao provider, com casting/mana/cooldown hospedados no Iron's. Black Arcana não reproduz o efeito.
- **Fonte factual:** [inventário](SPELL-CATALOG.md), [proveniência](EVIDENCE-AND-PROVENANCE.md), [limites de runtime](RUNTIME-AND-SAFETY.md).

### 54 — `REDSTONE_BOLT`

- **Família organizacional na fonte:** `lightning`; não comprova `SchoolType` individual.
- **Constante em `ModSpellRegistry`:** `REDSTONE_BOLT`.
- **Classe da fonte pública:** `RedstoneBoltSpell`.
- **Classe compilada SHA-exata 0.0.16.3:** `net.redreaper.monsterspellbooks.spells.lightning.RedstoneBoltSpell` ([dados da auditoria](../../../../docs/qa/monsters_spellbooks_00163_exact_registry_ids.json)).
- **Registry ID físico 0.0.16.3:** `monsterspellbooks:redstone_bolt` (**`COUNTED_EXACT` apenas identidade estática**, obtida de `getSpellResource` compilado; nenhum comportamento deduzido do nome).
- **Escola e configuração individual:** `NÃO VERIFICADO`; mesmo a escola Necro observada no source não prova a associação deste registro no binário instalado.
- **Custos, cooldown, level/rarity, targeting, efeito, dano/cura, summons, filtros PvP/boss, persistência, aquisição e world safety:** `NÃO VERIFICADO`. Nenhum desses mecanismos é inferido do nome.
- **Identidade semântica:** `COUNTED_EXACT` para ID/registro estático já inventariado no lote de 98; **+0** novos objetos. O feitiço pertence ao provider, com casting/mana/cooldown hospedados no Iron's. Black Arcana não reproduz o efeito.
- **Fonte factual:** [inventário](SPELL-CATALOG.md), [proveniência](EVIDENCE-AND-PROVENANCE.md), [limites de runtime](RUNTIME-AND-SAFETY.md).

### 55 — `REDSTONE_MINES`

- **Família organizacional na fonte:** `lightning`; não comprova `SchoolType` individual.
- **Constante em `ModSpellRegistry`:** `REDSTONE_MINES`.
- **Classe da fonte pública:** `RedstoneMinesSpell`.
- **Classe compilada SHA-exata 0.0.16.3:** `net.redreaper.monsterspellbooks.spells.lightning.RedstoneMinesSpell` ([dados da auditoria](../../../../docs/qa/monsters_spellbooks_00163_exact_registry_ids.json)).
- **Registry ID físico 0.0.16.3:** `monsterspellbooks:redstone_mines` (**`COUNTED_EXACT` apenas identidade estática**, obtida de `getSpellResource` compilado; nenhum comportamento deduzido do nome).
- **Escola e configuração individual:** `NÃO VERIFICADO`; mesmo a escola Necro observada no source não prova a associação deste registro no binário instalado.
- **Custos, cooldown, level/rarity, targeting, efeito, dano/cura, summons, filtros PvP/boss, persistência, aquisição e world safety:** `NÃO VERIFICADO`. Nenhum desses mecanismos é inferido do nome.
- **Identidade semântica:** `COUNTED_EXACT` para ID/registro estático já inventariado no lote de 98; **+0** novos objetos. O feitiço pertence ao provider, com casting/mana/cooldown hospedados no Iron's. Black Arcana não reproduz o efeito.
- **Fonte factual:** [inventário](SPELL-CATALOG.md), [proveniência](EVIDENCE-AND-PROVENANCE.md), [limites de runtime](RUNTIME-AND-SAFETY.md).

### 56 — `GUARDIANS_NEUTRALIZER`

- **Família organizacional na fonte:** `lightning`; não comprova `SchoolType` individual.
- **Constante em `ModSpellRegistry`:** `GUARDIANS_NEUTRALIZER`.
- **Classe da fonte pública:** `GuardiansNeutralizerSpell`.
- **Classe compilada SHA-exata 0.0.16.3:** `net.redreaper.monsterspellbooks.spells.lightning.GuardiansNeutralizerSpell` ([dados da auditoria](../../../../docs/qa/monsters_spellbooks_00163_exact_registry_ids.json)).
- **Registry ID físico 0.0.16.3:** `monsterspellbooks:guardians_neutralizer` (**`COUNTED_EXACT` apenas identidade estática**, obtida de `getSpellResource` compilado; nenhum comportamento deduzido do nome).
- **Escola e configuração individual:** `NÃO VERIFICADO`; mesmo a escola Necro observada no source não prova a associação deste registro no binário instalado.
- **Custos, cooldown, level/rarity, targeting, efeito, dano/cura, summons, filtros PvP/boss, persistência, aquisição e world safety:** `NÃO VERIFICADO`. Nenhum desses mecanismos é inferido do nome.
- **Identidade semântica:** `COUNTED_EXACT` para ID/registro estático já inventariado no lote de 98; **+0** novos objetos. O feitiço pertence ao provider, com casting/mana/cooldown hospedados no Iron's. Black Arcana não reproduz o efeito.
- **Fonte factual:** [inventário](SPELL-CATALOG.md), [proveniência](EVIDENCE-AND-PROVENANCE.md), [limites de runtime](RUNTIME-AND-SAFETY.md).

### 57 — `REDSTONE_CHAIN`

- **Família organizacional na fonte:** `lightning`; não comprova `SchoolType` individual.
- **Constante em `ModSpellRegistry`:** `REDSTONE_CHAIN`.
- **Classe da fonte pública:** `RedstoneChainSpell`.
- **Classe compilada SHA-exata 0.0.16.3:** `net.redreaper.monsterspellbooks.spells.lightning.RedstoneChainSpell` ([dados da auditoria](../../../../docs/qa/monsters_spellbooks_00163_exact_registry_ids.json)).
- **Registry ID físico 0.0.16.3:** `monsterspellbooks:redstone_chain` (**`COUNTED_EXACT` apenas identidade estática**, obtida de `getSpellResource` compilado; nenhum comportamento deduzido do nome).
- **Escola e configuração individual:** `NÃO VERIFICADO`; mesmo a escola Necro observada no source não prova a associação deste registro no binário instalado.
- **Custos, cooldown, level/rarity, targeting, efeito, dano/cura, summons, filtros PvP/boss, persistência, aquisição e world safety:** `NÃO VERIFICADO`. Nenhum desses mecanismos é inferido do nome.
- **Identidade semântica:** `COUNTED_EXACT` para ID/registro estático já inventariado no lote de 98; **+0** novos objetos. O feitiço pertence ao provider, com casting/mana/cooldown hospedados no Iron's. Black Arcana não reproduz o efeito.
- **Fonte factual:** [inventário](SPELL-CATALOG.md), [proveniência](EVIDENCE-AND-PROVENANCE.md), [limites de runtime](RUNTIME-AND-SAFETY.md).

### 58 — `REDSTONE_LASERS`

- **Família organizacional na fonte:** `lightning`; não comprova `SchoolType` individual.
- **Constante em `ModSpellRegistry`:** `REDSTONE_LASERS`.
- **Classe da fonte pública:** `RedstoneLasersSpell`.
- **Classe compilada SHA-exata 0.0.16.3:** `net.redreaper.monsterspellbooks.spells.lightning.RedstoneLasersSpell` ([dados da auditoria](../../../../docs/qa/monsters_spellbooks_00163_exact_registry_ids.json)).
- **Registry ID físico 0.0.16.3:** `monsterspellbooks:redstone_lasers` (**`COUNTED_EXACT` apenas identidade estática**, obtida de `getSpellResource` compilado; nenhum comportamento deduzido do nome).
- **Escola e configuração individual:** `NÃO VERIFICADO`; mesmo a escola Necro observada no source não prova a associação deste registro no binário instalado.
- **Custos, cooldown, level/rarity, targeting, efeito, dano/cura, summons, filtros PvP/boss, persistência, aquisição e world safety:** `NÃO VERIFICADO`. Nenhum desses mecanismos é inferido do nome.
- **Identidade semântica:** `COUNTED_EXACT` para ID/registro estático já inventariado no lote de 98; **+0** novos objetos. O feitiço pertence ao provider, com casting/mana/cooldown hospedados no Iron's. Black Arcana não reproduz o efeito.
- **Fonte factual:** [inventário](SPELL-CATALOG.md), [proveniência](EVIDENCE-AND-PROVENANCE.md), [limites de runtime](RUNTIME-AND-SAFETY.md).

### 59 — `RAIGO`

- **Família organizacional na fonte:** `lightning`; não comprova `SchoolType` individual.
- **Constante em `ModSpellRegistry`:** `RAIGO`.
- **Classe da fonte pública:** `RaigoSpell`.
- **Classe compilada SHA-exata 0.0.16.3:** `net.redreaper.monsterspellbooks.spells.lightning.RaigoSpell` ([dados da auditoria](../../../../docs/qa/monsters_spellbooks_00163_exact_registry_ids.json)).
- **Registry ID físico 0.0.16.3:** `monsterspellbooks:raigo` (**`COUNTED_EXACT` apenas identidade estática**, obtida de `getSpellResource` compilado; nenhum comportamento deduzido do nome).
- **Escola e configuração individual:** `NÃO VERIFICADO`; mesmo a escola Necro observada no source não prova a associação deste registro no binário instalado.
- **Custos, cooldown, level/rarity, targeting, efeito, dano/cura, summons, filtros PvP/boss, persistência, aquisição e world safety:** `NÃO VERIFICADO`. Nenhum desses mecanismos é inferido do nome.
- **Identidade semântica:** `COUNTED_EXACT` para ID/registro estático já inventariado no lote de 98; **+0** novos objetos. O feitiço pertence ao provider, com casting/mana/cooldown hospedados no Iron's. Black Arcana não reproduz o efeito.
- **Fonte factual:** [inventário](SPELL-CATALOG.md), [proveniência](EVIDENCE-AND-PROVENANCE.md), [limites de runtime](RUNTIME-AND-SAFETY.md).

### 60 — `STATIC_CLEAVE`

- **Família organizacional na fonte:** `lightning`; não comprova `SchoolType` individual.
- **Constante em `ModSpellRegistry`:** `STATIC_CLEAVE`.
- **Classe da fonte pública:** `StaticCleaveSpell`.
- **Classe compilada SHA-exata 0.0.16.3:** `net.redreaper.monsterspellbooks.spells.lightning.StaticCleaveSpell` ([dados da auditoria](../../../../docs/qa/monsters_spellbooks_00163_exact_registry_ids.json)).
- **Registry ID físico 0.0.16.3:** `monsterspellbooks:static_cleave` (**`COUNTED_EXACT` apenas identidade estática**, obtida de `getSpellResource` compilado; nenhum comportamento deduzido do nome).
- **Escola e configuração individual:** `NÃO VERIFICADO`; mesmo a escola Necro observada no source não prova a associação deste registro no binário instalado.
- **Custos, cooldown, level/rarity, targeting, efeito, dano/cura, summons, filtros PvP/boss, persistência, aquisição e world safety:** `NÃO VERIFICADO`. Nenhum desses mecanismos é inferido do nome.
- **Identidade semântica:** `COUNTED_EXACT` para ID/registro estático já inventariado no lote de 98; **+0** novos objetos. O feitiço pertence ao provider, com casting/mana/cooldown hospedados no Iron's. Black Arcana não reproduz o efeito.
- **Fonte factual:** [inventário](SPELL-CATALOG.md), [proveniência](EVIDENCE-AND-PROVENANCE.md), [limites de runtime](RUNTIME-AND-SAFETY.md).

### 61 — `THUNDER_STEP`

- **Família organizacional na fonte:** `lightning`; não comprova `SchoolType` individual.
- **Constante em `ModSpellRegistry`:** `THUNDER_STEP`.
- **Classe da fonte pública:** `ThunderStepSpell`.
- **Classe compilada SHA-exata 0.0.16.3:** `net.redreaper.monsterspellbooks.spells.lightning.ThunderStepSpell` ([dados da auditoria](../../../../docs/qa/monsters_spellbooks_00163_exact_registry_ids.json)).
- **Registry ID físico 0.0.16.3:** `monsterspellbooks:thunder_step` (**`COUNTED_EXACT` apenas identidade estática**, obtida de `getSpellResource` compilado; nenhum comportamento deduzido do nome).
- **Escola e configuração individual:** `NÃO VERIFICADO`; mesmo a escola Necro observada no source não prova a associação deste registro no binário instalado.
- **Custos, cooldown, level/rarity, targeting, efeito, dano/cura, summons, filtros PvP/boss, persistência, aquisição e world safety:** `NÃO VERIFICADO`. Nenhum desses mecanismos é inferido do nome.
- **Identidade semântica:** `COUNTED_EXACT` para ID/registro estático já inventariado no lote de 98; **+0** novos objetos. O feitiço pertence ao provider, com casting/mana/cooldown hospedados no Iron's. Black Arcana não reproduz o efeito.
- **Fonte factual:** [inventário](SPELL-CATALOG.md), [proveniência](EVIDENCE-AND-PROVENANCE.md), [limites de runtime](RUNTIME-AND-SAFETY.md).

### 62 — `THUNDERSTORM_WAVE`

- **Família organizacional na fonte:** `lightning`; não comprova `SchoolType` individual.
- **Constante em `ModSpellRegistry`:** `THUNDERSTORM_WAVE`.
- **Classe da fonte pública:** `ThunderstormWaveSpell`.
- **Classe compilada SHA-exata 0.0.16.3:** `net.redreaper.monsterspellbooks.spells.lightning.ThunderstormWaveSpell` ([dados da auditoria](../../../../docs/qa/monsters_spellbooks_00163_exact_registry_ids.json)).
- **Registry ID físico 0.0.16.3:** `monsterspellbooks:thunderstorm_wave` (**`COUNTED_EXACT` apenas identidade estática**, obtida de `getSpellResource` compilado; nenhum comportamento deduzido do nome).
- **Escola e configuração individual:** `NÃO VERIFICADO`; mesmo a escola Necro observada no source não prova a associação deste registro no binário instalado.
- **Custos, cooldown, level/rarity, targeting, efeito, dano/cura, summons, filtros PvP/boss, persistência, aquisição e world safety:** `NÃO VERIFICADO`. Nenhum desses mecanismos é inferido do nome.
- **Identidade semântica:** `COUNTED_EXACT` para ID/registro estático já inventariado no lote de 98; **+0** novos objetos. O feitiço pertence ao provider, com casting/mana/cooldown hospedados no Iron's. Black Arcana não reproduz o efeito.
- **Fonte factual:** [inventário](SPELL-CATALOG.md), [proveniência](EVIDENCE-AND-PROVENANCE.md), [limites de runtime](RUNTIME-AND-SAFETY.md).

### 63 — `VOLTAIC_MULTISHOT`

- **Família organizacional na fonte:** `lightning`; não comprova `SchoolType` individual.
- **Constante em `ModSpellRegistry`:** `VOLTAIC_MULTISHOT`.
- **Classe da fonte pública:** `VoltaicMultishotSpell`.
- **Classe compilada SHA-exata 0.0.16.3:** `net.redreaper.monsterspellbooks.spells.lightning.VoltaicMultishotSpell` ([dados da auditoria](../../../../docs/qa/monsters_spellbooks_00163_exact_registry_ids.json)).
- **Registry ID físico 0.0.16.3:** `monsterspellbooks:voltaic_multishot` (**`COUNTED_EXACT` apenas identidade estática**, obtida de `getSpellResource` compilado; nenhum comportamento deduzido do nome).
- **Escola e configuração individual:** `NÃO VERIFICADO`; mesmo a escola Necro observada no source não prova a associação deste registro no binário instalado.
- **Custos, cooldown, level/rarity, targeting, efeito, dano/cura, summons, filtros PvP/boss, persistência, aquisição e world safety:** `NÃO VERIFICADO`. Nenhum desses mecanismos é inferido do nome.
- **Identidade semântica:** `COUNTED_EXACT` para ID/registro estático já inventariado no lote de 98; **+0** novos objetos. O feitiço pertence ao provider, com casting/mana/cooldown hospedados no Iron's. Black Arcana não reproduz o efeito.
- **Fonte factual:** [inventário](SPELL-CATALOG.md), [proveniência](EVIDENCE-AND-PROVENANCE.md), [limites de runtime](RUNTIME-AND-SAFETY.md).

### 64 — `ZAP`

- **Família organizacional na fonte:** `lightning`; não comprova `SchoolType` individual.
- **Constante em `ModSpellRegistry`:** `ZAP`.
- **Classe da fonte pública:** `ZapSpell`.
- **Classe compilada SHA-exata 0.0.16.3:** `net.redreaper.monsterspellbooks.spells.lightning.ZapSpell` ([dados da auditoria](../../../../docs/qa/monsters_spellbooks_00163_exact_registry_ids.json)).
- **Registry ID físico 0.0.16.3:** `monsterspellbooks:zap` (**`COUNTED_EXACT` apenas identidade estática**, obtida de `getSpellResource` compilado; nenhum comportamento deduzido do nome).
- **Escola e configuração individual:** `NÃO VERIFICADO`; mesmo a escola Necro observada no source não prova a associação deste registro no binário instalado.
- **Custos, cooldown, level/rarity, targeting, efeito, dano/cura, summons, filtros PvP/boss, persistência, aquisição e world safety:** `NÃO VERIFICADO`. Nenhum desses mecanismos é inferido do nome.
- **Identidade semântica:** `COUNTED_EXACT` para ID/registro estático já inventariado no lote de 98; **+0** novos objetos. O feitiço pertence ao provider, com casting/mana/cooldown hospedados no Iron's. Black Arcana não reproduz o efeito.
- **Fonte factual:** [inventário](SPELL-CATALOG.md), [proveniência](EVIDENCE-AND-PROVENANCE.md), [limites de runtime](RUNTIME-AND-SAFETY.md).


## Família `nature` — 7 registros

### 65 — `BLAST_FUNGUS`

- **Família organizacional na fonte:** `nature`; não comprova `SchoolType` individual.
- **Constante em `ModSpellRegistry`:** `BLAST_FUNGUS`.
- **Classe da fonte pública:** `BlastFungusSpell`.
- **Classe compilada SHA-exata 0.0.16.3:** `net.redreaper.monsterspellbooks.spells.nature.BlastFungusSpell` ([dados da auditoria](../../../../docs/qa/monsters_spellbooks_00163_exact_registry_ids.json)).
- **Registry ID físico 0.0.16.3:** `monsterspellbooks:blast_fungus` (**`COUNTED_EXACT` apenas identidade estática**, obtida de `getSpellResource` compilado; nenhum comportamento deduzido do nome).
- **Escola e configuração individual:** `NÃO VERIFICADO`; mesmo a escola Necro observada no source não prova a associação deste registro no binário instalado.
- **Custos, cooldown, level/rarity, targeting, efeito, dano/cura, summons, filtros PvP/boss, persistência, aquisição e world safety:** `NÃO VERIFICADO`. Nenhum desses mecanismos é inferido do nome.
- **Identidade semântica:** `COUNTED_EXACT` para ID/registro estático já inventariado no lote de 98; **+0** novos objetos. O feitiço pertence ao provider, com casting/mana/cooldown hospedados no Iron's. Black Arcana não reproduz o efeito.
- **Fonte factual:** [inventário](SPELL-CATALOG.md), [proveniência](EVIDENCE-AND-PROVENANCE.md), [limites de runtime](RUNTIME-AND-SAFETY.md).

### 66 — `INFECTION_SLASH`

- **Família organizacional na fonte:** `nature`; não comprova `SchoolType` individual.
- **Constante em `ModSpellRegistry`:** `INFECTION_SLASH`.
- **Classe da fonte pública:** `InfectionSlashSpell`.
- **Classe compilada SHA-exata 0.0.16.3:** `net.redreaper.monsterspellbooks.spells.nature.InfectionSlashSpell` ([dados da auditoria](../../../../docs/qa/monsters_spellbooks_00163_exact_registry_ids.json)).
- **Registry ID físico 0.0.16.3:** `monsterspellbooks:infection_slash` (**`COUNTED_EXACT` apenas identidade estática**, obtida de `getSpellResource` compilado; nenhum comportamento deduzido do nome).
- **Escola e configuração individual:** `NÃO VERIFICADO`; mesmo a escola Necro observada no source não prova a associação deste registro no binário instalado.
- **Custos, cooldown, level/rarity, targeting, efeito, dano/cura, summons, filtros PvP/boss, persistência, aquisição e world safety:** `NÃO VERIFICADO`. Nenhum desses mecanismos é inferido do nome.
- **Identidade semântica:** `COUNTED_EXACT` para ID/registro estático já inventariado no lote de 98; **+0** novos objetos. O feitiço pertence ao provider, com casting/mana/cooldown hospedados no Iron's. Black Arcana não reproduz o efeito.
- **Fonte factual:** [inventário](SPELL-CATALOG.md), [proveniência](EVIDENCE-AND-PROVENANCE.md), [limites de runtime](RUNTIME-AND-SAFETY.md).

### 67 — `LEAF_CRYSTAL`

- **Família organizacional na fonte:** `nature`; não comprova `SchoolType` individual.
- **Constante em `ModSpellRegistry`:** `LEAF_CRYSTAL`.
- **Classe da fonte pública:** `LifeCrystalSpell`.
- **Classe compilada SHA-exata 0.0.16.3:** `net.redreaper.monsterspellbooks.spells.nature.LifeCrystalSpell` ([dados da auditoria](../../../../docs/qa/monsters_spellbooks_00163_exact_registry_ids.json)).
- **Registry ID físico 0.0.16.3:** `monsterspellbooks:leaf_crystal` (**`COUNTED_EXACT` apenas identidade estática**, obtida de `getSpellResource` compilado; nenhum comportamento deduzido do nome).
- **Escola e configuração individual:** `NÃO VERIFICADO`; mesmo a escola Necro observada no source não prova a associação deste registro no binário instalado.
- **Custos, cooldown, level/rarity, targeting, efeito, dano/cura, summons, filtros PvP/boss, persistência, aquisição e world safety:** `NÃO VERIFICADO`. Nenhum desses mecanismos é inferido do nome.
- **Identidade semântica:** `COUNTED_EXACT` para ID/registro estático já inventariado no lote de 98; **+0** novos objetos. O feitiço pertence ao provider, com casting/mana/cooldown hospedados no Iron's. Black Arcana não reproduz o efeito.
- **Fonte factual:** [inventário](SPELL-CATALOG.md), [proveniência](EVIDENCE-AND-PROVENANCE.md), [limites de runtime](RUNTIME-AND-SAFETY.md).

### 68 — `POISON_QUILL`

- **Família organizacional na fonte:** `nature`; não comprova `SchoolType` individual.
- **Constante em `ModSpellRegistry`:** `POISON_QUILL`.
- **Classe da fonte pública:** `PoisonQuillSpell`.
- **Classe compilada SHA-exata 0.0.16.3:** `net.redreaper.monsterspellbooks.spells.nature.PoisonQuillSpell` ([dados da auditoria](../../../../docs/qa/monsters_spellbooks_00163_exact_registry_ids.json)).
- **Registry ID físico 0.0.16.3:** `monsterspellbooks:poison_quill` (**`COUNTED_EXACT` apenas identidade estática**, obtida de `getSpellResource` compilado; nenhum comportamento deduzido do nome).
- **Escola e configuração individual:** `NÃO VERIFICADO`; mesmo a escola Necro observada no source não prova a associação deste registro no binário instalado.
- **Custos, cooldown, level/rarity, targeting, efeito, dano/cura, summons, filtros PvP/boss, persistência, aquisição e world safety:** `NÃO VERIFICADO`. Nenhum desses mecanismos é inferido do nome.
- **Identidade semântica:** `COUNTED_EXACT` para ID/registro estático já inventariado no lote de 98; **+0** novos objetos. O feitiço pertence ao provider, com casting/mana/cooldown hospedados no Iron's. Black Arcana não reproduz o efeito.
- **Fonte factual:** [inventário](SPELL-CATALOG.md), [proveniência](EVIDENCE-AND-PROVENANCE.md), [limites de runtime](RUNTIME-AND-SAFETY.md).

### 69 — `SPIDER_FANGS`

- **Família organizacional na fonte:** `nature`; não comprova `SchoolType` individual.
- **Constante em `ModSpellRegistry`:** `SPIDER_FANGS`.
- **Classe da fonte pública:** `SpiderFangsSpell`.
- **Classe compilada SHA-exata 0.0.16.3:** `net.redreaper.monsterspellbooks.spells.nature.SpiderFangsSpell` ([dados da auditoria](../../../../docs/qa/monsters_spellbooks_00163_exact_registry_ids.json)).
- **Registry ID físico 0.0.16.3:** `monsterspellbooks:spider_fangs` (**`COUNTED_EXACT` apenas identidade estática**, obtida de `getSpellResource` compilado; nenhum comportamento deduzido do nome).
- **Escola e configuração individual:** `NÃO VERIFICADO`; mesmo a escola Necro observada no source não prova a associação deste registro no binário instalado.
- **Custos, cooldown, level/rarity, targeting, efeito, dano/cura, summons, filtros PvP/boss, persistência, aquisição e world safety:** `NÃO VERIFICADO`. Nenhum desses mecanismos é inferido do nome.
- **Identidade semântica:** `COUNTED_EXACT` para ID/registro estático já inventariado no lote de 98; **+0** novos objetos. O feitiço pertence ao provider, com casting/mana/cooldown hospedados no Iron's. Black Arcana não reproduz o efeito.
- **Fonte factual:** [inventário](SPELL-CATALOG.md), [proveniência](EVIDENCE-AND-PROVENANCE.md), [limites de runtime](RUNTIME-AND-SAFETY.md).

### 70 — `SUMMON_POISON_VINE`

- **Família organizacional na fonte:** `nature`; não comprova `SchoolType` individual.
- **Constante em `ModSpellRegistry`:** `SUMMON_POISON_VINE`.
- **Classe da fonte pública:** `SummonPoisonVinesSpell`.
- **Classe compilada SHA-exata 0.0.16.3:** `net.redreaper.monsterspellbooks.spells.nature.SummonPoisonVinesSpell` ([dados da auditoria](../../../../docs/qa/monsters_spellbooks_00163_exact_registry_ids.json)).
- **Registry ID físico 0.0.16.3:** `monsterspellbooks:summon_poison_vines` (**`COUNTED_EXACT` apenas identidade estática**, obtida de `getSpellResource` compilado; nenhum comportamento deduzido do nome).
- **Escola e configuração individual:** `NÃO VERIFICADO`; mesmo a escola Necro observada no source não prova a associação deste registro no binário instalado.
- **Custos, cooldown, level/rarity, targeting, efeito, dano/cura, summons, filtros PvP/boss, persistência, aquisição e world safety:** `NÃO VERIFICADO`. Nenhum desses mecanismos é inferido do nome.
- **Identidade semântica:** `COUNTED_EXACT` para ID/registro estático já inventariado no lote de 98; **+0** novos objetos. O feitiço pertence ao provider, com casting/mana/cooldown hospedados no Iron's. Black Arcana não reproduz o efeito.
- **Fonte factual:** [inventário](SPELL-CATALOG.md), [proveniência](EVIDENCE-AND-PROVENANCE.md), [limites de runtime](RUNTIME-AND-SAFETY.md).

### 71 — `VITAL_BLAST`

- **Família organizacional na fonte:** `nature`; não comprova `SchoolType` individual.
- **Constante em `ModSpellRegistry`:** `VITAL_BLAST`.
- **Classe da fonte pública:** `VitalBlastSpell`.
- **Classe compilada SHA-exata 0.0.16.3:** `net.redreaper.monsterspellbooks.spells.nature.VitalBlastSpell` ([dados da auditoria](../../../../docs/qa/monsters_spellbooks_00163_exact_registry_ids.json)).
- **Registry ID físico 0.0.16.3:** `monsterspellbooks:vital_blast` (**`COUNTED_EXACT` apenas identidade estática**, obtida de `getSpellResource` compilado; nenhum comportamento deduzido do nome).
- **Escola e configuração individual:** `NÃO VERIFICADO`; mesmo a escola Necro observada no source não prova a associação deste registro no binário instalado.
- **Custos, cooldown, level/rarity, targeting, efeito, dano/cura, summons, filtros PvP/boss, persistência, aquisição e world safety:** `NÃO VERIFICADO`. Nenhum desses mecanismos é inferido do nome.
- **Identidade semântica:** `COUNTED_EXACT` para ID/registro estático já inventariado no lote de 98; **+0** novos objetos. O feitiço pertence ao provider, com casting/mana/cooldown hospedados no Iron's. Black Arcana não reproduz o efeito.
- **Fonte factual:** [inventário](SPELL-CATALOG.md), [proveniência](EVIDENCE-AND-PROVENANCE.md), [limites de runtime](RUNTIME-AND-SAFETY.md).


## Família `necro` — 25 registros

### 72 — `REAPER_ASPECT`

- **Família organizacional na fonte:** `necro`; não comprova `SchoolType` individual.
- **Constante em `ModSpellRegistry`:** `REAPER_ASPECT`.
- **Classe da fonte pública:** `ReaperAspectSpell`.
- **Classe compilada SHA-exata 0.0.16.3:** `net.redreaper.monsterspellbooks.spells.necro.ReaperAspectSpell` ([dados da auditoria](../../../../docs/qa/monsters_spellbooks_00163_exact_registry_ids.json)).
- **Registry ID físico 0.0.16.3:** `monsterspellbooks:reaper_aspect` (**`COUNTED_EXACT` apenas identidade estática**, obtida de `getSpellResource` compilado; nenhum comportamento deduzido do nome).
- **Escola e configuração individual:** `NÃO VERIFICADO`; mesmo a escola Necro observada no source não prova a associação deste registro no binário instalado.
- **Custos, cooldown, level/rarity, targeting, efeito, dano/cura, summons, filtros PvP/boss, persistência, aquisição e world safety:** `NÃO VERIFICADO`. Nenhum desses mecanismos é inferido do nome.
- **Identidade semântica:** `COUNTED_EXACT` para ID/registro estático já inventariado no lote de 98; **+0** novos objetos. O feitiço pertence ao provider, com casting/mana/cooldown hospedados no Iron's. Black Arcana não reproduz o efeito.
- **Fonte factual:** [inventário](SPELL-CATALOG.md), [proveniência](EVIDENCE-AND-PROVENANCE.md), [limites de runtime](RUNTIME-AND-SAFETY.md).

### 73 — `BANSHEE_SCREAM`

- **Família organizacional na fonte:** `necro`; não comprova `SchoolType` individual.
- **Constante em `ModSpellRegistry`:** `BANSHEE_SCREAM`.
- **Classe da fonte pública:** `BansheeScreamSpell`.
- **Classe compilada SHA-exata 0.0.16.3:** `net.redreaper.monsterspellbooks.spells.necro.BansheeScreamSpell` ([dados da auditoria](../../../../docs/qa/monsters_spellbooks_00163_exact_registry_ids.json)).
- **Registry ID físico 0.0.16.3:** `monsterspellbooks:banshee_scream` (**`COUNTED_EXACT` apenas identidade estática**, obtida de `getSpellResource` compilado; nenhum comportamento deduzido do nome).
- **Escola e configuração individual:** `NÃO VERIFICADO`; mesmo a escola Necro observada no source não prova a associação deste registro no binário instalado.
- **Custos, cooldown, level/rarity, targeting, efeito, dano/cura, summons, filtros PvP/boss, persistência, aquisição e world safety:** `NÃO VERIFICADO`. Nenhum desses mecanismos é inferido do nome.
- **Identidade semântica:** `COUNTED_EXACT` para ID/registro estático já inventariado no lote de 98; **+0** novos objetos. O feitiço pertence ao provider, com casting/mana/cooldown hospedados no Iron's. Black Arcana não reproduz o efeito.
- **Fonte factual:** [inventário](SPELL-CATALOG.md), [proveniência](EVIDENCE-AND-PROVENANCE.md), [limites de runtime](RUNTIME-AND-SAFETY.md).

### 74 — `BONE_DAGGER`

- **Família organizacional na fonte:** `necro`; não comprova `SchoolType` individual.
- **Constante em `ModSpellRegistry`:** `BONE_DAGGER`.
- **Classe da fonte pública:** `BoneDaggerSpell`.
- **Classe compilada SHA-exata 0.0.16.3:** `net.redreaper.monsterspellbooks.spells.necro.BoneDaggerSpell` ([dados da auditoria](../../../../docs/qa/monsters_spellbooks_00163_exact_registry_ids.json)).
- **Registry ID físico 0.0.16.3:** `monsterspellbooks:bone_dagger` (**`COUNTED_EXACT` apenas identidade estática**, obtida de `getSpellResource` compilado; nenhum comportamento deduzido do nome).
- **Escola e configuração individual:** `NÃO VERIFICADO`; mesmo a escola Necro observada no source não prova a associação deste registro no binário instalado.
- **Custos, cooldown, level/rarity, targeting, efeito, dano/cura, summons, filtros PvP/boss, persistência, aquisição e world safety:** `NÃO VERIFICADO`. Nenhum desses mecanismos é inferido do nome.
- **Identidade semântica:** `COUNTED_EXACT` para ID/registro estático já inventariado no lote de 98; **+0** novos objetos. O feitiço pertence ao provider, com casting/mana/cooldown hospedados no Iron's. Black Arcana não reproduz o efeito.
- **Fonte factual:** [inventário](SPELL-CATALOG.md), [proveniência](EVIDENCE-AND-PROVENANCE.md), [limites de runtime](RUNTIME-AND-SAFETY.md).

### 75 — `SUMMON_DEATH_KNIGHT`

- **Família organizacional na fonte:** `necro`; não comprova `SchoolType` individual.
- **Constante em `ModSpellRegistry`:** `SUMMON_DEATH_KNIGHT`.
- **Classe da fonte pública:** `SummonDeathKnightSpell`.
- **Classe compilada SHA-exata 0.0.16.3:** `net.redreaper.monsterspellbooks.spells.necro.SummonDeathKnightSpell` ([dados da auditoria](../../../../docs/qa/monsters_spellbooks_00163_exact_registry_ids.json)).
- **Registry ID físico 0.0.16.3:** `monsterspellbooks:summon_death_knight` (**`COUNTED_EXACT` apenas identidade estática**, obtida de `getSpellResource` compilado; nenhum comportamento deduzido do nome).
- **Escola e configuração individual:** `NÃO VERIFICADO`; mesmo a escola Necro observada no source não prova a associação deste registro no binário instalado.
- **Custos, cooldown, level/rarity, targeting, efeito, dano/cura, summons, filtros PvP/boss, persistência, aquisição e world safety:** `NÃO VERIFICADO`. Nenhum desses mecanismos é inferido do nome.
- **Identidade semântica:** `COUNTED_EXACT` para ID/registro estático já inventariado no lote de 98; **+0** novos objetos. O feitiço pertence ao provider, com casting/mana/cooldown hospedados no Iron's. Black Arcana não reproduz o efeito.
- **Fonte factual:** [inventário](SPELL-CATALOG.md), [proveniência](EVIDENCE-AND-PROVENANCE.md), [limites de runtime](RUNTIME-AND-SAFETY.md).

### 76 — `FALL_CURSE`

- **Família organizacional na fonte:** `necro`; não comprova `SchoolType` individual.
- **Constante em `ModSpellRegistry`:** `FALL_CURSE`.
- **Classe da fonte pública:** `FallCurseSpell`.
- **Classe compilada SHA-exata 0.0.16.3:** `net.redreaper.monsterspellbooks.spells.necro.FallCurseSpell` ([dados da auditoria](../../../../docs/qa/monsters_spellbooks_00163_exact_registry_ids.json)).
- **Registry ID físico 0.0.16.3:** `monsterspellbooks:fall_curse` (**`COUNTED_EXACT` apenas identidade estática**, obtida de `getSpellResource` compilado; nenhum comportamento deduzido do nome).
- **Escola e configuração individual:** `NÃO VERIFICADO`; mesmo a escola Necro observada no source não prova a associação deste registro no binário instalado.
- **Custos, cooldown, level/rarity, targeting, efeito, dano/cura, summons, filtros PvP/boss, persistência, aquisição e world safety:** `NÃO VERIFICADO`. Nenhum desses mecanismos é inferido do nome.
- **Identidade semântica:** `COUNTED_EXACT` para ID/registro estático já inventariado no lote de 98; **+0** novos objetos. O feitiço pertence ao provider, com casting/mana/cooldown hospedados no Iron's. Black Arcana não reproduz o efeito.
- **Fonte factual:** [inventário](SPELL-CATALOG.md), [proveniência](EVIDENCE-AND-PROVENANCE.md), [limites de runtime](RUNTIME-AND-SAFETY.md).

### 77 — `GRAVEYARD_FISSURE`

- **Família organizacional na fonte:** `necro`; não comprova `SchoolType` individual.
- **Constante em `ModSpellRegistry`:** `GRAVEYARD_FISSURE`.
- **Classe da fonte pública:** `GraveyardFissureSpell`.
- **Classe compilada SHA-exata 0.0.16.3:** `net.redreaper.monsterspellbooks.spells.necro.GraveyardFissureSpell` ([dados da auditoria](../../../../docs/qa/monsters_spellbooks_00163_exact_registry_ids.json)).
- **Registry ID físico 0.0.16.3:** `monsterspellbooks:graveyard_fissure` (**`COUNTED_EXACT` apenas identidade estática**, obtida de `getSpellResource` compilado; nenhum comportamento deduzido do nome).
- **Escola e configuração individual:** `NÃO VERIFICADO`; mesmo a escola Necro observada no source não prova a associação deste registro no binário instalado.
- **Custos, cooldown, level/rarity, targeting, efeito, dano/cura, summons, filtros PvP/boss, persistência, aquisição e world safety:** `NÃO VERIFICADO`. Nenhum desses mecanismos é inferido do nome.
- **Identidade semântica:** `COUNTED_EXACT` para ID/registro estático já inventariado no lote de 98; **+0** novos objetos. O feitiço pertence ao provider, com casting/mana/cooldown hospedados no Iron's. Black Arcana não reproduz o efeito.
- **Fonte factual:** [inventário](SPELL-CATALOG.md), [proveniência](EVIDENCE-AND-PROVENANCE.md), [limites de runtime](RUNTIME-AND-SAFETY.md).

### 78 — `LICHDOM`

- **Família organizacional na fonte:** `necro`; não comprova `SchoolType` individual.
- **Constante em `ModSpellRegistry`:** `LICHDOM`.
- **Classe da fonte pública:** `LichdomSpell`.
- **Classe compilada SHA-exata 0.0.16.3:** `net.redreaper.monsterspellbooks.spells.necro.LichdomSpell` ([dados da auditoria](../../../../docs/qa/monsters_spellbooks_00163_exact_registry_ids.json)).
- **Registry ID físico 0.0.16.3:** `monsterspellbooks:lichdom` (**`COUNTED_EXACT` apenas identidade estática**, obtida de `getSpellResource` compilado; nenhum comportamento deduzido do nome).
- **Escola e configuração individual:** `NÃO VERIFICADO`; mesmo a escola Necro observada no source não prova a associação deste registro no binário instalado.
- **Custos, cooldown, level/rarity, targeting, efeito, dano/cura, summons, filtros PvP/boss, persistência, aquisição e world safety:** `NÃO VERIFICADO`. Nenhum desses mecanismos é inferido do nome.
- **Identidade semântica:** `COUNTED_EXACT` para ID/registro estático já inventariado no lote de 98; **+0** novos objetos. O feitiço pertence ao provider, com casting/mana/cooldown hospedados no Iron's. Black Arcana não reproduz o efeito.
- **Fonte factual:** [inventário](SPELL-CATALOG.md), [proveniência](EVIDENCE-AND-PROVENANCE.md), [limites de runtime](RUNTIME-AND-SAFETY.md).

### 79 — `LIFE_DRAIN`

- **Família organizacional na fonte:** `necro`; não comprova `SchoolType` individual.
- **Constante em `ModSpellRegistry`:** `LIFE_DRAIN`.
- **Classe da fonte pública:** `LifeDrainSpell`.
- **Classe compilada SHA-exata 0.0.16.3:** `net.redreaper.monsterspellbooks.spells.necro.LifeDrainSpell` ([dados da auditoria](../../../../docs/qa/monsters_spellbooks_00163_exact_registry_ids.json)).
- **Registry ID físico 0.0.16.3:** `monsterspellbooks:life_drain` (**`COUNTED_EXACT` apenas identidade estática**, obtida de `getSpellResource` compilado; nenhum comportamento deduzido do nome).
- **Escola e configuração individual:** `NÃO VERIFICADO`; mesmo a escola Necro observada no source não prova a associação deste registro no binário instalado.
- **Custos, cooldown, level/rarity, targeting, efeito, dano/cura, summons, filtros PvP/boss, persistência, aquisição e world safety:** `NÃO VERIFICADO`. Nenhum desses mecanismos é inferido do nome.
- **Identidade semântica:** `COUNTED_EXACT` para ID/registro estático já inventariado no lote de 98; **+0** novos objetos. O feitiço pertence ao provider, com casting/mana/cooldown hospedados no Iron's. Black Arcana não reproduz o efeito.
- **Fonte factual:** [inventário](SPELL-CATALOG.md), [proveniência](EVIDENCE-AND-PROVENANCE.md), [limites de runtime](RUNTIME-AND-SAFETY.md).

### 80 — `PUTRESCENCE_MASS`

- **Família organizacional na fonte:** `necro`; não comprova `SchoolType` individual.
- **Constante em `ModSpellRegistry`:** `PUTRESCENCE_MASS`.
- **Classe da fonte pública:** `PutrescenceMassSpell`.
- **Classe compilada SHA-exata 0.0.16.3:** `net.redreaper.monsterspellbooks.spells.necro.PutrescenceMassSpell` ([dados da auditoria](../../../../docs/qa/monsters_spellbooks_00163_exact_registry_ids.json)).
- **Registry ID físico 0.0.16.3:** `monsterspellbooks:putrescence_mass` (**`COUNTED_EXACT` apenas identidade estática**, obtida de `getSpellResource` compilado; nenhum comportamento deduzido do nome).
- **Escola e configuração individual:** `NÃO VERIFICADO`; mesmo a escola Necro observada no source não prova a associação deste registro no binário instalado.
- **Custos, cooldown, level/rarity, targeting, efeito, dano/cura, summons, filtros PvP/boss, persistência, aquisição e world safety:** `NÃO VERIFICADO`. Nenhum desses mecanismos é inferido do nome.
- **Identidade semântica:** `COUNTED_EXACT` para ID/registro estático já inventariado no lote de 98; **+0** novos objetos. O feitiço pertence ao provider, com casting/mana/cooldown hospedados no Iron's. Black Arcana não reproduz o efeito.
- **Fonte factual:** [inventário](SPELL-CATALOG.md), [proveniência](EVIDENCE-AND-PROVENANCE.md), [limites de runtime](RUNTIME-AND-SAFETY.md).

### 81 — `RANCORCALL`

- **Família organizacional na fonte:** `necro`; não comprova `SchoolType` individual.
- **Constante em `ModSpellRegistry`:** `RANCORCALL`.
- **Classe da fonte pública:** `RancorCallSpell`.
- **Classe compilada SHA-exata 0.0.16.3:** `net.redreaper.monsterspellbooks.spells.necro.RancorCallSpell` ([dados da auditoria](../../../../docs/qa/monsters_spellbooks_00163_exact_registry_ids.json)).
- **Registry ID físico 0.0.16.3:** `monsterspellbooks:rancorcall` (**`COUNTED_EXACT` apenas identidade estática**, obtida de `getSpellResource` compilado; nenhum comportamento deduzido do nome).
- **Escola e configuração individual:** `NÃO VERIFICADO`; mesmo a escola Necro observada no source não prova a associação deste registro no binário instalado.
- **Custos, cooldown, level/rarity, targeting, efeito, dano/cura, summons, filtros PvP/boss, persistência, aquisição e world safety:** `NÃO VERIFICADO`. Nenhum desses mecanismos é inferido do nome.
- **Identidade semântica:** `COUNTED_EXACT` para ID/registro estático já inventariado no lote de 98; **+0** novos objetos. O feitiço pertence ao provider, com casting/mana/cooldown hospedados no Iron's. Black Arcana não reproduz o efeito.
- **Fonte factual:** [inventário](SPELL-CATALOG.md), [proveniência](EVIDENCE-AND-PROVENANCE.md), [limites de runtime](RUNTIME-AND-SAFETY.md).

### 82 — `SOUL_CASTING_FIELD`

- **Família organizacional na fonte:** `necro`; não comprova `SchoolType` individual.
- **Constante em `ModSpellRegistry`:** `SOUL_CASTING_FIELD`.
- **Classe da fonte pública:** `SoulCastingFieldSpell`.
- **Classe compilada SHA-exata 0.0.16.3:** `net.redreaper.monsterspellbooks.spells.necro.SoulCastingFieldSpell` ([dados da auditoria](../../../../docs/qa/monsters_spellbooks_00163_exact_registry_ids.json)).
- **Registry ID físico 0.0.16.3:** `monsterspellbooks:soul_casting_field` (**`COUNTED_EXACT` apenas identidade estática**, obtida de `getSpellResource` compilado; nenhum comportamento deduzido do nome).
- **Escola e configuração individual:** `NÃO VERIFICADO`; mesmo a escola Necro observada no source não prova a associação deste registro no binário instalado.
- **Custos, cooldown, level/rarity, targeting, efeito, dano/cura, summons, filtros PvP/boss, persistência, aquisição e world safety:** `NÃO VERIFICADO`. Nenhum desses mecanismos é inferido do nome.
- **Identidade semântica:** `COUNTED_EXACT` para ID/registro estático já inventariado no lote de 98; **+0** novos objetos. O feitiço pertence ao provider, com casting/mana/cooldown hospedados no Iron's. Black Arcana não reproduz o efeito.
- **Fonte factual:** [inventário](SPELL-CATALOG.md), [proveniência](EVIDENCE-AND-PROVENANCE.md), [limites de runtime](RUNTIME-AND-SAFETY.md).

### 83 — `SOUL_CHAIN`

- **Família organizacional na fonte:** `necro`; não comprova `SchoolType` individual.
- **Constante em `ModSpellRegistry`:** `SOUL_CHAIN`.
- **Classe da fonte pública:** `SoulChainSpell`.
- **Classe compilada SHA-exata 0.0.16.3:** `net.redreaper.monsterspellbooks.spells.necro.SoulChainSpell` ([dados da auditoria](../../../../docs/qa/monsters_spellbooks_00163_exact_registry_ids.json)).
- **Registry ID físico 0.0.16.3:** `monsterspellbooks:soul_chain` (**`COUNTED_EXACT` apenas identidade estática**, obtida de `getSpellResource` compilado; nenhum comportamento deduzido do nome).
- **Escola e configuração individual:** `NÃO VERIFICADO`; mesmo a escola Necro observada no source não prova a associação deste registro no binário instalado.
- **Custos, cooldown, level/rarity, targeting, efeito, dano/cura, summons, filtros PvP/boss, persistência, aquisição e world safety:** `NÃO VERIFICADO`. Nenhum desses mecanismos é inferido do nome.
- **Identidade semântica:** `COUNTED_EXACT` para ID/registro estático já inventariado no lote de 98; **+0** novos objetos. O feitiço pertence ao provider, com casting/mana/cooldown hospedados no Iron's. Black Arcana não reproduz o efeito.
- **Fonte factual:** [inventário](SPELL-CATALOG.md), [proveniência](EVIDENCE-AND-PROVENANCE.md), [limites de runtime](RUNTIME-AND-SAFETY.md).

### 84 — `SOUL_FIREBOLT`

- **Família organizacional na fonte:** `necro`; não comprova `SchoolType` individual.
- **Constante em `ModSpellRegistry`:** `SOUL_FIREBOLT`.
- **Classe da fonte pública:** `SoulFireBoltSpell`.
- **Classe compilada SHA-exata 0.0.16.3:** `net.redreaper.monsterspellbooks.spells.necro.SoulFireBoltSpell` ([dados da auditoria](../../../../docs/qa/monsters_spellbooks_00163_exact_registry_ids.json)).
- **Registry ID físico 0.0.16.3:** `monsterspellbooks:soul_firebolt` (**`COUNTED_EXACT` apenas identidade estática**, obtida de `getSpellResource` compilado; nenhum comportamento deduzido do nome).
- **Escola e configuração individual:** `NÃO VERIFICADO`; mesmo a escola Necro observada no source não prova a associação deste registro no binário instalado.
- **Custos, cooldown, level/rarity, targeting, efeito, dano/cura, summons, filtros PvP/boss, persistência, aquisição e world safety:** `NÃO VERIFICADO`. Nenhum desses mecanismos é inferido do nome.
- **Identidade semântica:** `COUNTED_EXACT` para ID/registro estático já inventariado no lote de 98; **+0** novos objetos. O feitiço pertence ao provider, com casting/mana/cooldown hospedados no Iron's. Black Arcana não reproduz o efeito.
- **Fonte factual:** [inventário](SPELL-CATALOG.md), [proveniência](EVIDENCE-AND-PROVENANCE.md), [limites de runtime](RUNTIME-AND-SAFETY.md).

### 85 — `SOUL_FIRE_TELEPORT`

- **Família organizacional na fonte:** `necro`; não comprova `SchoolType` individual.
- **Constante em `ModSpellRegistry`:** `SOUL_FIRE_TELEPORT`.
- **Classe da fonte pública:** `SoulFireTeleportSpell`.
- **Classe compilada SHA-exata 0.0.16.3:** `net.redreaper.monsterspellbooks.spells.necro.SoulFireTeleportSpell` ([dados da auditoria](../../../../docs/qa/monsters_spellbooks_00163_exact_registry_ids.json)).
- **Registry ID físico 0.0.16.3:** `monsterspellbooks:soul_fire_teleport` (**`COUNTED_EXACT` apenas identidade estática**, obtida de `getSpellResource` compilado; nenhum comportamento deduzido do nome).
- **Escola e configuração individual:** `NÃO VERIFICADO`; mesmo a escola Necro observada no source não prova a associação deste registro no binário instalado.
- **Custos, cooldown, level/rarity, targeting, efeito, dano/cura, summons, filtros PvP/boss, persistência, aquisição e world safety:** `NÃO VERIFICADO`. Nenhum desses mecanismos é inferido do nome.
- **Identidade semântica:** `COUNTED_EXACT` para ID/registro estático já inventariado no lote de 98; **+0** novos objetos. O feitiço pertence ao provider, com casting/mana/cooldown hospedados no Iron's. Black Arcana não reproduz o efeito.
- **Fonte factual:** [inventário](SPELL-CATALOG.md), [proveniência](EVIDENCE-AND-PROVENANCE.md), [limites de runtime](RUNTIME-AND-SAFETY.md).

### 86 — `SOUL_FORM`

- **Família organizacional na fonte:** `necro`; não comprova `SchoolType` individual.
- **Constante em `ModSpellRegistry`:** `SOUL_FORM`.
- **Classe da fonte pública:** `SoulFormSpell`.
- **Classe compilada SHA-exata 0.0.16.3:** `net.redreaper.monsterspellbooks.spells.necro.SoulFormSpell` ([dados da auditoria](../../../../docs/qa/monsters_spellbooks_00163_exact_registry_ids.json)).
- **Registry ID físico 0.0.16.3:** `monsterspellbooks:soul_form` (**`COUNTED_EXACT` apenas identidade estática**, obtida de `getSpellResource` compilado; nenhum comportamento deduzido do nome).
- **Escola e configuração individual:** `NÃO VERIFICADO`; mesmo a escola Necro observada no source não prova a associação deste registro no binário instalado.
- **Custos, cooldown, level/rarity, targeting, efeito, dano/cura, summons, filtros PvP/boss, persistência, aquisição e world safety:** `NÃO VERIFICADO`. Nenhum desses mecanismos é inferido do nome.
- **Identidade semântica:** `COUNTED_EXACT` para ID/registro estático já inventariado no lote de 98; **+0** novos objetos. O feitiço pertence ao provider, com casting/mana/cooldown hospedados no Iron's. Black Arcana não reproduz o efeito.
- **Fonte factual:** [inventário](SPELL-CATALOG.md), [proveniência](EVIDENCE-AND-PROVENANCE.md), [limites de runtime](RUNTIME-AND-SAFETY.md).

### 87 — `SOUL_SCORCH`

- **Família organizacional na fonte:** `necro`; não comprova `SchoolType` individual.
- **Constante em `ModSpellRegistry`:** `SOUL_SCORCH`.
- **Classe da fonte pública:** `SoulScorchSpell`.
- **Classe compilada SHA-exata 0.0.16.3:** `net.redreaper.monsterspellbooks.spells.necro.SoulScorchSpell` ([dados da auditoria](../../../../docs/qa/monsters_spellbooks_00163_exact_registry_ids.json)).
- **Registry ID físico 0.0.16.3:** `monsterspellbooks:soul_scorch` (**`COUNTED_EXACT` apenas identidade estática**, obtida de `getSpellResource` compilado; nenhum comportamento deduzido do nome).
- **Escola e configuração individual:** `NÃO VERIFICADO`; mesmo a escola Necro observada no source não prova a associação deste registro no binário instalado.
- **Custos, cooldown, level/rarity, targeting, efeito, dano/cura, summons, filtros PvP/boss, persistência, aquisição e world safety:** `NÃO VERIFICADO`. Nenhum desses mecanismos é inferido do nome.
- **Identidade semântica:** `COUNTED_EXACT` para ID/registro estático já inventariado no lote de 98; **+0** novos objetos. O feitiço pertence ao provider, com casting/mana/cooldown hospedados no Iron's. Black Arcana não reproduz o efeito.
- **Fonte factual:** [inventário](SPELL-CATALOG.md), [proveniência](EVIDENCE-AND-PROVENANCE.md), [limites de runtime](RUNTIME-AND-SAFETY.md).

### 88 — `SPECTRAL_BLAST`

- **Família organizacional na fonte:** `necro`; não comprova `SchoolType` individual.
- **Constante em `ModSpellRegistry`:** `SPECTRAL_BLAST`.
- **Classe da fonte pública:** `SpectralBlastSpell`.
- **Classe compilada SHA-exata 0.0.16.3:** `net.redreaper.monsterspellbooks.spells.necro.SpectralBlastSpell` ([dados da auditoria](../../../../docs/qa/monsters_spellbooks_00163_exact_registry_ids.json)).
- **Registry ID físico 0.0.16.3:** `monsterspellbooks:spectral_blast` (**`COUNTED_EXACT` apenas identidade estática**, obtida de `getSpellResource` compilado; nenhum comportamento deduzido do nome).
- **Escola e configuração individual:** `NÃO VERIFICADO`; mesmo a escola Necro observada no source não prova a associação deste registro no binário instalado.
- **Custos, cooldown, level/rarity, targeting, efeito, dano/cura, summons, filtros PvP/boss, persistência, aquisição e world safety:** `NÃO VERIFICADO`. Nenhum desses mecanismos é inferido do nome.
- **Identidade semântica:** `COUNTED_EXACT` para ID/registro estático já inventariado no lote de 98; **+0** novos objetos. O feitiço pertence ao provider, com casting/mana/cooldown hospedados no Iron's. Black Arcana não reproduz o efeito.
- **Fonte factual:** [inventário](SPELL-CATALOG.md), [proveniência](EVIDENCE-AND-PROVENANCE.md), [limites de runtime](RUNTIME-AND-SAFETY.md).

### 89 — `SPIRIT_STRIKE`

- **Família organizacional na fonte:** `necro`; não comprova `SchoolType` individual.
- **Constante em `ModSpellRegistry`:** `SPIRIT_STRIKE`.
- **Classe da fonte pública:** `SpiritStrikeSpell`.
- **Classe compilada SHA-exata 0.0.16.3:** `net.redreaper.monsterspellbooks.spells.necro.SpiritStrikeSpell` ([dados da auditoria](../../../../docs/qa/monsters_spellbooks_00163_exact_registry_ids.json)).
- **Registry ID físico 0.0.16.3:** `monsterspellbooks:spirit_strike` (**`COUNTED_EXACT` apenas identidade estática**, obtida de `getSpellResource` compilado; nenhum comportamento deduzido do nome).
- **Escola e configuração individual:** `NÃO VERIFICADO`; mesmo a escola Necro observada no source não prova a associação deste registro no binário instalado.
- **Custos, cooldown, level/rarity, targeting, efeito, dano/cura, summons, filtros PvP/boss, persistência, aquisição e world safety:** `NÃO VERIFICADO`. Nenhum desses mecanismos é inferido do nome.
- **Identidade semântica:** `COUNTED_EXACT` para ID/registro estático já inventariado no lote de 98; **+0** novos objetos. O feitiço pertence ao provider, com casting/mana/cooldown hospedados no Iron's. Black Arcana não reproduz o efeito.
- **Fonte factual:** [inventário](SPELL-CATALOG.md), [proveniência](EVIDENCE-AND-PROVENANCE.md), [limites de runtime](RUNTIME-AND-SAFETY.md).

### 90 — `STRAY_GRASP`

- **Família organizacional na fonte:** `necro`; não comprova `SchoolType` individual.
- **Constante em `ModSpellRegistry`:** `STRAY_GRASP`.
- **Classe da fonte pública:** `StrayGraspSpell`.
- **Classe compilada SHA-exata 0.0.16.3:** `net.redreaper.monsterspellbooks.spells.necro.StrayGraspSpell` ([dados da auditoria](../../../../docs/qa/monsters_spellbooks_00163_exact_registry_ids.json)).
- **Registry ID físico 0.0.16.3:** `monsterspellbooks:stray_grasp` (**`COUNTED_EXACT` apenas identidade estática**, obtida de `getSpellResource` compilado; nenhum comportamento deduzido do nome).
- **Escola e configuração individual:** `NÃO VERIFICADO`; mesmo a escola Necro observada no source não prova a associação deste registro no binário instalado.
- **Custos, cooldown, level/rarity, targeting, efeito, dano/cura, summons, filtros PvP/boss, persistência, aquisição e world safety:** `NÃO VERIFICADO`. Nenhum desses mecanismos é inferido do nome.
- **Identidade semântica:** `COUNTED_EXACT` para ID/registro estático já inventariado no lote de 98; **+0** novos objetos. O feitiço pertence ao provider, com casting/mana/cooldown hospedados no Iron's. Black Arcana não reproduz o efeito.
- **Fonte factual:** [inventário](SPELL-CATALOG.md), [proveniência](EVIDENCE-AND-PROVENANCE.md), [limites de runtime](RUNTIME-AND-SAFETY.md).

### 91 — `SUMMON_SOUL_WIZARD`

- **Família organizacional na fonte:** `necro`; não comprova `SchoolType` individual.
- **Constante em `ModSpellRegistry`:** `SUMMON_SOUL_WIZARD`.
- **Classe da fonte pública:** `SummonSoulWizardSpell`.
- **Classe compilada SHA-exata 0.0.16.3:** `net.redreaper.monsterspellbooks.spells.necro.SummonSoulWizardSpell` ([dados da auditoria](../../../../docs/qa/monsters_spellbooks_00163_exact_registry_ids.json)).
- **Registry ID físico 0.0.16.3:** `monsterspellbooks:summon_soul_wizard` (**`COUNTED_EXACT` apenas identidade estática**, obtida de `getSpellResource` compilado; nenhum comportamento deduzido do nome).
- **Escola e configuração individual:** `NÃO VERIFICADO`; mesmo a escola Necro observada no source não prova a associação deste registro no binário instalado.
- **Custos, cooldown, level/rarity, targeting, efeito, dano/cura, summons, filtros PvP/boss, persistência, aquisição e world safety:** `NÃO VERIFICADO`. Nenhum desses mecanismos é inferido do nome.
- **Identidade semântica:** `COUNTED_EXACT` para ID/registro estático já inventariado no lote de 98; **+0** novos objetos. O feitiço pertence ao provider, com casting/mana/cooldown hospedados no Iron's. Black Arcana não reproduz o efeito.
- **Fonte factual:** [inventário](SPELL-CATALOG.md), [proveniência](EVIDENCE-AND-PROVENANCE.md), [limites de runtime](RUNTIME-AND-SAFETY.md).

### 92 — `TORMENT_ARROW`

- **Família organizacional na fonte:** `necro`; não comprova `SchoolType` individual.
- **Constante em `ModSpellRegistry`:** `TORMENT_ARROW`.
- **Classe da fonte pública:** `TormentArrowSpell`.
- **Classe compilada SHA-exata 0.0.16.3:** `net.redreaper.monsterspellbooks.spells.necro.TormentArrowSpell` ([dados da auditoria](../../../../docs/qa/monsters_spellbooks_00163_exact_registry_ids.json)).
- **Registry ID físico 0.0.16.3:** `monsterspellbooks:torment_arrow` (**`COUNTED_EXACT` apenas identidade estática**, obtida de `getSpellResource` compilado; nenhum comportamento deduzido do nome).
- **Escola e configuração individual:** `NÃO VERIFICADO`; mesmo a escola Necro observada no source não prova a associação deste registro no binário instalado.
- **Custos, cooldown, level/rarity, targeting, efeito, dano/cura, summons, filtros PvP/boss, persistência, aquisição e world safety:** `NÃO VERIFICADO`. Nenhum desses mecanismos é inferido do nome.
- **Identidade semântica:** `COUNTED_EXACT` para ID/registro estático já inventariado no lote de 98; **+0** novos objetos. O feitiço pertence ao provider, com casting/mana/cooldown hospedados no Iron's. Black Arcana não reproduz o efeito.
- **Fonte factual:** [inventário](SPELL-CATALOG.md), [proveniência](EVIDENCE-AND-PROVENANCE.md), [limites de runtime](RUNTIME-AND-SAFETY.md).

### 93 — `VILE_SLASH`

- **Família organizacional na fonte:** `necro`; não comprova `SchoolType` individual.
- **Constante em `ModSpellRegistry`:** `VILE_SLASH`.
- **Classe da fonte pública:** `VileSlashSpell`.
- **Classe compilada SHA-exata 0.0.16.3:** `net.redreaper.monsterspellbooks.spells.necro.VileSlashSpell` ([dados da auditoria](../../../../docs/qa/monsters_spellbooks_00163_exact_registry_ids.json)).
- **Registry ID físico 0.0.16.3:** `monsterspellbooks:vile_slash` (**`COUNTED_EXACT` apenas identidade estática**, obtida de `getSpellResource` compilado; nenhum comportamento deduzido do nome).
- **Escola e configuração individual:** `NÃO VERIFICADO`; mesmo a escola Necro observada no source não prova a associação deste registro no binário instalado.
- **Custos, cooldown, level/rarity, targeting, efeito, dano/cura, summons, filtros PvP/boss, persistência, aquisição e world safety:** `NÃO VERIFICADO`. Nenhum desses mecanismos é inferido do nome.
- **Identidade semântica:** `COUNTED_EXACT` para ID/registro estático já inventariado no lote de 98; **+0** novos objetos. O feitiço pertence ao provider, com casting/mana/cooldown hospedados no Iron's. Black Arcana não reproduz o efeito.
- **Fonte factual:** [inventário](SPELL-CATALOG.md), [proveniência](EVIDENCE-AND-PROVENANCE.md), [limites de runtime](RUNTIME-AND-SAFETY.md).

### 94 — `SUMMON_WITHER_ARMY`

- **Família organizacional na fonte:** `necro`; não comprova `SchoolType` individual.
- **Constante em `ModSpellRegistry`:** `SUMMON_WITHER_ARMY`.
- **Classe da fonte pública:** `SummonWitherArmy`.
- **Classe compilada SHA-exata 0.0.16.3:** `net.redreaper.monsterspellbooks.spells.necro.SummonWitherArmy` ([dados da auditoria](../../../../docs/qa/monsters_spellbooks_00163_exact_registry_ids.json)).
- **Registry ID físico 0.0.16.3:** `monsterspellbooks:summon_wither_warrior` (**`COUNTED_EXACT` apenas identidade estática**, obtida de `getSpellResource` compilado; nenhum comportamento deduzido do nome).
- **Escola e configuração individual:** `NÃO VERIFICADO`; mesmo a escola Necro observada no source não prova a associação deste registro no binário instalado.
- **Custos, cooldown, level/rarity, targeting, efeito, dano/cura, summons, filtros PvP/boss, persistência, aquisição e world safety:** `NÃO VERIFICADO`. Nenhum desses mecanismos é inferido do nome.
- **Identidade semântica:** `COUNTED_EXACT` para ID/registro estático já inventariado no lote de 98; **+0** novos objetos. O feitiço pertence ao provider, com casting/mana/cooldown hospedados no Iron's. Black Arcana não reproduz o efeito.
- **Fonte factual:** [inventário](SPELL-CATALOG.md), [proveniência](EVIDENCE-AND-PROVENANCE.md), [limites de runtime](RUNTIME-AND-SAFETY.md).

### 95 — `WITHER_BOMB`

- **Família organizacional na fonte:** `necro`; não comprova `SchoolType` individual.
- **Constante em `ModSpellRegistry`:** `WITHER_BOMB`.
- **Classe da fonte pública:** `WitherBombSpell`.
- **Classe compilada SHA-exata 0.0.16.3:** `net.redreaper.monsterspellbooks.spells.necro.WitherBombSpell` ([dados da auditoria](../../../../docs/qa/monsters_spellbooks_00163_exact_registry_ids.json)).
- **Registry ID físico 0.0.16.3:** `monsterspellbooks:wither_bomb` (**`COUNTED_EXACT` apenas identidade estática**, obtida de `getSpellResource` compilado; nenhum comportamento deduzido do nome).
- **Escola e configuração individual:** `NÃO VERIFICADO`; mesmo a escola Necro observada no source não prova a associação deste registro no binário instalado.
- **Custos, cooldown, level/rarity, targeting, efeito, dano/cura, summons, filtros PvP/boss, persistência, aquisição e world safety:** `NÃO VERIFICADO`. Nenhum desses mecanismos é inferido do nome.
- **Identidade semântica:** `COUNTED_EXACT` para ID/registro estático já inventariado no lote de 98; **+0** novos objetos. O feitiço pertence ao provider, com casting/mana/cooldown hospedados no Iron's. Black Arcana não reproduz o efeito.
- **Fonte factual:** [inventário](SPELL-CATALOG.md), [proveniência](EVIDENCE-AND-PROVENANCE.md), [limites de runtime](RUNTIME-AND-SAFETY.md).

### 96 — `WITHER_NOVA`

- **Família organizacional na fonte:** `necro`; não comprova `SchoolType` individual.
- **Constante em `ModSpellRegistry`:** `WITHER_NOVA`.
- **Classe da fonte pública:** `WitherNovaSpell`.
- **Classe compilada SHA-exata 0.0.16.3:** `net.redreaper.monsterspellbooks.spells.necro.WitherNovaSpell` ([dados da auditoria](../../../../docs/qa/monsters_spellbooks_00163_exact_registry_ids.json)).
- **Registry ID físico 0.0.16.3:** `monsterspellbooks:wither_nova` (**`COUNTED_EXACT` apenas identidade estática**, obtida de `getSpellResource` compilado; nenhum comportamento deduzido do nome).
- **Escola e configuração individual:** `NÃO VERIFICADO`; mesmo a escola Necro observada no source não prova a associação deste registro no binário instalado.
- **Custos, cooldown, level/rarity, targeting, efeito, dano/cura, summons, filtros PvP/boss, persistência, aquisição e world safety:** `NÃO VERIFICADO`. Nenhum desses mecanismos é inferido do nome.
- **Identidade semântica:** `COUNTED_EXACT` para ID/registro estático já inventariado no lote de 98; **+0** novos objetos. O feitiço pertence ao provider, com casting/mana/cooldown hospedados no Iron's. Black Arcana não reproduz o efeito.
- **Fonte factual:** [inventário](SPELL-CATALOG.md), [proveniência](EVIDENCE-AND-PROVENANCE.md), [limites de runtime](RUNTIME-AND-SAFETY.md).


## Família `technomancy` — 2 registros

### 97 — `SPINBLADE`

- **Família organizacional na fonte:** `technomancy`; não comprova `SchoolType` individual.
- **Constante em `ModSpellRegistry`:** `SPINBLADE`.
- **Classe da fonte pública:** `SpinbladeSpell`.
- **Classe compilada SHA-exata 0.0.16.3:** `net.redreaper.monsterspellbooks.spells.technomancy.SpinbladeSpell` ([dados da auditoria](../../../../docs/qa/monsters_spellbooks_00163_exact_registry_ids.json)).
- **Registry ID físico 0.0.16.3:** `monsterspellbooks:spinblade` (**`COUNTED_EXACT` apenas identidade estática**, obtida de `getSpellResource` compilado; nenhum comportamento deduzido do nome).
- **Escola e configuração individual:** `NÃO VERIFICADO`; mesmo a escola Necro observada no source não prova a associação deste registro no binário instalado.
- **Custos, cooldown, level/rarity, targeting, efeito, dano/cura, summons, filtros PvP/boss, persistência, aquisição e world safety:** `NÃO VERIFICADO`. Nenhum desses mecanismos é inferido do nome.
- **Identidade semântica:** `COUNTED_EXACT` para ID/registro estático já inventariado no lote de 98; **+0** novos objetos. O feitiço pertence ao provider, com casting/mana/cooldown hospedados no Iron's. Black Arcana não reproduz o efeito.
- **Fonte factual:** [inventário](SPELL-CATALOG.md), [proveniência](EVIDENCE-AND-PROVENANCE.md), [limites de runtime](RUNTIME-AND-SAFETY.md).

### 98 — `SUMMON_DWARVEN_DRONES`

- **Família organizacional na fonte:** `technomancy`; não comprova `SchoolType` individual.
- **Constante em `ModSpellRegistry`:** `SUMMON_DWARVEN_DRONES`.
- **Classe da fonte pública:** `SummonDwarvenDronesSpell`.
- **Classe compilada SHA-exata 0.0.16.3:** `net.redreaper.monsterspellbooks.spells.technomancy.SummonDwarvenDronesSpell` ([dados da auditoria](../../../../docs/qa/monsters_spellbooks_00163_exact_registry_ids.json)).
- **Registry ID físico 0.0.16.3:** `monsterspellbooks:summon_dwarven_drones` (**`COUNTED_EXACT` apenas identidade estática**, obtida de `getSpellResource` compilado; nenhum comportamento deduzido do nome).
- **Escola e configuração individual:** `NÃO VERIFICADO`; mesmo a escola Necro observada no source não prova a associação deste registro no binário instalado.
- **Custos, cooldown, level/rarity, targeting, efeito, dano/cura, summons, filtros PvP/boss, persistência, aquisição e world safety:** `NÃO VERIFICADO`. Nenhum desses mecanismos é inferido do nome.
- **Identidade semântica:** `COUNTED_EXACT` para ID/registro estático já inventariado no lote de 98; **+0** novos objetos. O feitiço pertence ao provider, com casting/mana/cooldown hospedados no Iron's. Black Arcana não reproduz o efeito.
- **Fonte factual:** [inventário](SPELL-CATALOG.md), [proveniência](EVIDENCE-AND-PROVENANCE.md), [limites de runtime](RUNTIME-AND-SAFETY.md).

## Exclusões e limites finais

- `aero` = **0 registros** na fonte `ModSpellRegistry`; não acrescentar feitiços por menção a escola decompilada ou fonte com versão desatualizada.
- Não contar school, equipment, projectile, summon entity, effects e itens como segunda identidade do mesmo registro.
- Exatamente **98/98 fichas de campos/classes da fonte**. A paridade de IDs e classes no JAR instalado, configuração efetiva, aquisição em Survival, comportamento e hooks permanece ⚠️ **PENDENTE**, não promovida por documentação.
- Sem novos casts, bridges, APIs, hooks, balance, dano ou efeitos adicionados ao runtime Black Arcana. Etapa 06.05 e futuras etapas não avançam por esta tarefa.
