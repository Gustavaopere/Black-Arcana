# Dreamless Spells 1.1.9 — 4/4 IDs de registro binário estático

**✅ 4/4 `COUNTED_EXACT` apenas no registro estático do artefato físico. ⚠️ Runtime/config/Survival continuam pendentes.**

## Artefato e prova independente

- Modlist sibling certificada `de80b186357cad20ba5b81892a8682777e96e35a`: ordem **#225**, `dreamless_spells-1.1.9.jar`, mod ID `dreamless_spells`, SHA-1 `d51960bfb8af1aafa5d716ef9a48c3135f36b956`.
- Publicador [CurseForge projeto 1250250 / file 7905334](https://www.curseforge.com/minecraft/mc-mods/dreamless-spells/files/7905334), 2026-04-10, NeoForge 1.21.1. JAR oficial **443506 bytes**, SHA-1 idêntico ao JAR registrado no snapshot (checado por `sha1sum --check`).
- Auditoria [run #38302406303](https://github.com/Gustavaopere/Black-Arcana/actions/runs/38302406303), commit isolado `3b0816f648b3b264cd1785a1ab99562b9d5945e3` na branch `audit/dreamless-spells-119-physical-registry-20261012`: **SUCCESS**. Java 21 `javap -p -c`, ZIP `testzip`. Nenhum código/bytecode/asset/JAR de terceiro foi commitado.
- O source pin `stikbug/Neoforge-Dreamless-Spells-N-Spellbooks@71f7befa81f618d07bfa023c5c82d32fdb10077a` não foi comprovado como compilação reproduzível; só JAR do publicador ↔ SHA-1 físico.

## Identidades do registry

| # | Classe concreta do provider | Registry ID | Classe da evidência |
|---:|---|---|---|
| 1 | `spells/ice/JadeskinSpell.class` | `dreamless_spells:jadeskin` | `EXACT_BINARY_STATIC` |
| 2 | `spells/empty/DrainedSpell.class` | `dreamless_spells:drained` | `EXACT_BINARY_STATIC` |
| 3 | `spells/empty/DullardSpell.class` | `dreamless_spells:dullard` | `EXACT_BINARY_STATIC` |
| 4 | `spells/empty/MuteSpell.class` | `dreamless_spells:doorway_effect` | `EXACT_BINARY_STATIC` |

O log verificado confirmou `PROVIDER_SPELL_CLASSES` com quatro classes, `STATIC_SPELL_FACTORY_INVOCATIONS=4`, `DEFERRED_REGISTER_HELPER_INVOCATIONS=1`, `BOOTSTRAP_SPELL_REGISTRIES=present`, quatro IDs e `RESULT=EXACT_STATIC_BINARY_REGISTRY_FOUR_IDS`. A classe `MuteSpell` tem ID `doorway_effect`; não existe uma quinta root `dreamless_spells:mute` comprovada. School, items, mobs, potions e armor não são registrations extras de spell.

## Escopo e fail-closed

As quatro roots já integravam o ledger: `COUNTED_SOURCE_PINNED → COUNTED_EXACT` **somente para ID e cardinalidade estática do registro físico**; **+0** objetos. Campanha original **4/39** exatos e **35/39** pendentes; **1851** mínimo global e **1849** no escopo inalterados. Denominador final desconhecido.

**⚠️ Sem teste real** de startup do modpack, mixin de Counterspell, `Emptied`, mana/cooldown, custo e duração em jogo de Drained/Dullard/Mute, Scroll Forge e config, origem da Empty Rune, persistência, multiplayer, cancelamento, receita e Survival. O código-fonte documenta riscos mas a auditoria binária não valida seu comportamento.

Dreamless é owner dos spells/efeitos/escola e eventos que adiciona; Iron's é owner do casting/registry/custos; Black Arcana mantém autoridade do runtime próprio sem double-processing. RPG Skill Tree é sibling apenas por contratos reais de progressão. Stage 06.05 permanece 🟡.
