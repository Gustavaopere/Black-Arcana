# Aeromancy Additions 1.2.8 — JAR oficial: dez spell IDs; SHA físico incompleto

**⚠️ Estado:** `COUNTED_SOURCE_PINNED` **mantido** na campanha de 39 providers. **Dez/10 spell registries comprovados no binário oficial de publicação**, mas a equivalência por hash com o arquivo efetivamente instalado **NÃO ESTÁ COMPROVADA**. Campanha segue **16/39 exatos / 23/39 pendentes**; os dez IDs já integravam o ledger; **+0** raízes; mínimos **1857 global / 1855 escopo**.

## Identidade e provenance separadas

1. **Presença e versão instaladas (autoridade documental sibling):** `neoforge-rpg-skilltree` modlist #009 aponta `aero_additions-1.2.8.jar`, mod ID `aero_additions`, NeoForge Minecraft 1.21.1. O documento sibling não informa SHA-1 completo independente do arquivo instalado.
2. **Publicador (JAR real extraído):** [CurseForge file 8251034](https://www.curseforge.com/minecraft/mc-mods/snackpirates-aeromancy-additions/files/8251034), `aero_additions-1.2.8.jar`, **753884 bytes**, SHA-1 **`dee32c9fa84a9b3796e39846608f8f77591ea56f`**. O digest foi calculado em [GitHub Actions #38431639191](https://github.com/Gustavaopere/Black-Arcana/actions/runs/38431639191) usando JAR obtido via CurseMaven, e coincide com a informação de release publicada. Mod ID do `neoforge.mods.toml` `aero_additions`; `META-INF/jarjar/expandability-neoforge-12.0.0.jar` está presente, sem virar mod top-level extra.
3. **Bloqueio de integridade física:** o README histórico do catálogo rotula equivocadamente o texto **`dee32c9fa84d6e39846608f8f77591ea56f`** como `Physical JAR SHA-1`; possui **35 caracteres** (SHA-1 hexadecimal precisa de 40), portanto **não é um hash válido nem comprova paridade**. Não substituímos esse campo com o SHA oficial presumindo que o arquivo local é idêntico.
4. **Para encerrar o gate:** coletar SHA-1 de 40 caracteres sobre os bytes de `aero_additions-1.2.8.jar` no diretório físico do modpack; reconciliar com o publisher, confirmar origem/caminho, reexecutar a auditoria; somente após identidade binária, gates e deduplicação fechados considerar `COUNTED_EXACT`.

## Registros de spell do JAR oficial (não do JAR físico comprovado)

`Aeromancy.<init> → AASpells.register(modEventBus) → SPELLS.register(bus)`, onde `AASpells.SPELLS` é um `DeferredRegister<AbstractSpell>` sobre Iron's `SpellRegistry.SPELL_REGISTRY_KEY`, namespace `aero_additions`. O initializer `AASpells.<clinit>` instancia dez classes `AbstractSpell` e chama dez vezes o wrapper `registerSpell(AbstractSpell)`, que despacha `DeferredRegister.register(spell.getSpellName(), Supplier)`. Sem branches de registro no método inspecionado. Cada classe compilada expõe `getSpellResource` com o sufixo literal próprio via `Aeromancy.id`.

| # | Registro publicado | Classe compilada |
|---:|---|---|
| 1 | `aero_additions:wind_charge` | `com.snackpirate.aeromancy.spells.wind_charge.WindChargeSpell` |
| 2 | `aero_additions:updraft` | `com.snackpirate.aeromancy.spells.updraft.UpdraftSpell` |
| 3 | `aero_additions:airstep` | `com.snackpirate.aeromancy.spells.airstep.AirstepSpell` |
| 4 | `aero_additions:asphyxiate` | `com.snackpirate.aeromancy.spells.asphyxiate.AsphyxiateSpell` |
| 5 | `aero_additions:feather_fall` | `com.snackpirate.aeromancy.spells.feather_fall.FeatherFallSpell` |
| 6 | `aero_additions:wind_shield` | `com.snackpirate.aeromancy.spells.wind_shield.WindShieldSpell` |
| 7 | `aero_additions:airblast` | `com.snackpirate.aeromancy.spells.airblast.AirblastSpell` |
| 8 | `aero_additions:wind_blade` | `com.snackpirate.aeromancy.spells.wind_blade.WindBladeSpell` |
| 9 | `aero_additions:flush` | `com.snackpirate.aeromancy.spells.flush.FlushSpell` |
| 10 | `aero_additions:dash` | `com.snackpirate.aeromancy.spells.dash.DashSpell` |

**Exclusões:** `TornadoSpell`, `ThunderclapSpell`, `SummonBreezeSpell`, `TelelinkSpell` e `ShapeshiftSpell` aparecem como calls comentadas no source pin `ae282b32d25ad76ef8d01c637ec05566a767ae4c` e **não** são instanciados no initializer do JAR publicado. Entidades, effects, tomos, espadas e materiais de foco também não geram novas raízes semânticas quando apenas suportam uma destas dez spells.

## Pontos de risco que a prova NÃO fecha

- **Feather Fall / Feather Flight:** `aero_additions:feather_fall` e `FeatherFallSpell` são ID/classe compilados, independentemente da apresentação local. Changelog sobre mudança de comportamento não autoriza renomear o registry ou concluir resultado real do voo.
- O JAR publicado contém ExpandAbility **12.0.0** embutido. A compatibilidade montada com Iron's Spells 3.16.3, NeoForge do pack e event bus real não foi executada.
- Defaults e navegação de Scroll Forge, Breeze Rod loot, configs, custos, cooldowns, allowed crafting, alvos/friendly fire, reflexo Wind Shield, input/payload de Airstep, movimento aéreo, dimension/reconnect e Survival permanecem condicionados.
- Black Arcana não assume casting/mana/cooldown de Iron's nem duplica estado/efeitos de Aeromancy. Sem contrato provider real, bridge é **fail-closed**; RPG Skill Tree permanece sibling de progressão. Stage 06.05 🟡, sem promoção.

## Evidência reproduzível

- [Auditoria publisher completa Java 21 #38431639191](https://github.com/Gustavaopere/Black-Arcana/actions/runs/38431639191): `PUBLISHER_EXACT_STATIC_SPELLS=10`, `UNREGISTERED_SOURCE_CANDIDATES_EXCLUDED=5`, `PUBLISHER_STATIC_IDENTITY_AUDIT=PASS`, `PHYSICAL_INSTALLED_JAR_SHA_UNVERIFIED=TRUE`.
- [Discovery publisher #38431460928](https://github.com/Gustavaopere/Black-Arcana/actions/runs/38431460928) success; [tentativa inicial #38431109127](https://github.com/Gustavaopere/Black-Arcana/actions/runs/38431109127) **falhou corretamente** porque exigia digest físico inválido. Nenhuma evidência de CI isolado deve ser transformada em aceitação de jogo real.
- Workflow de auditoria fica na branch técnica `audit/aeromancy-128-binary-20261013`, **fora da main**; dossiê clean-room não copia código de terceiros.
