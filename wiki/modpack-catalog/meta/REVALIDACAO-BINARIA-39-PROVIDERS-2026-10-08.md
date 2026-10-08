# Provedores source/release-bounded — roteiro de verificação binária

**Estado:** ⚠️ 39 provedores com registro do ledger `COUNTED_SOURCE_PINNED` ou `COUNTED_RELEASE_BOUNDED`; **0/39 promovidos a `COUNTED_EXACT` neste lote**. Não rebaixe indevidamente suas identidades contadas nem assuma que o registry no JAR é idêntico à fonte pública.

Snapshot: `Black-Arcana/main@9141a8ed1c345db4e995e5f2aa849df2c24769b9` / sibling modlist `de80b186357cad20ba5b81892a8682777e96e35a`.

Uma correspondência entre **nome/versão do arquivo JAR** e o ledger já foi comprovada para 69 providers presentes pelo [crosswalk](PHYSICAL-LEDGER-VERSION-RECONCILIATION-2026-10-08.md); essa operação não lê registry nem garante os mesmos bytes de release pública.

| Provider | Linha/version ledger | Quantidade já identificada | Evidência semântica atual | Evidência para promover registry |
|---|---|---:|---|---|
| [Ars Nouveau](../providers/✅-ars-nouveau/README.md) | 5.13.1 | 109 | COUNTED_SOURCE_PINNED | ⚠️ Exato JAR SHA + enumeração exaustiva das identidades + condições de registro + deduplicação; **não executado neste lote** |
| [Ars Additions](../providers/✅-ars-additions/README.md) | 21.3.0 | 5 | COUNTED_SOURCE_PINNED | ⚠️ Exato JAR SHA + enumeração exaustiva das identidades + condições de registro + deduplicação; **não executado neste lote** |
| [Ars Controle](../providers/✅-ars-controle/README.md) | 1.6.16 | 9 | COUNTED_SOURCE_PINNED | ⚠️ Exato JAR SHA + enumeração exaustiva das identidades + condições de registro + deduplicação; **não executado neste lote** |
| [Ars Technica](../providers/✅-ars-technica/README.md) | 2.7.6 | 11 | COUNTED_SOURCE_PINNED | ⚠️ Exato JAR SHA + enumeração exaustiva das identidades + condições de registro + deduplicação; **não executado neste lote** |
| [Ars Hex](../providers/✅-ars-hex/README.md) | 5.0.4b | 1 | COUNTED_SOURCE_PINNED | ⚠️ Exato JAR SHA + enumeração exaustiva das identidades + condições de registro + deduplicação; **não executado neste lote** |
| [Ars Zero](../providers/✅-ars-zero/README.md) | 2.0.2 | 12 | COUNTED_RELEASE_BOUNDED | ⚠️ Exato JAR SHA + enumeração exaustiva das identidades + condições de registro + deduplicação; **não executado neste lote** |
| [Ars Elemental](../providers/✅-ars-elemental/README.md) | 0.7.10.1 | 47 | COUNTED_SOURCE_PINNED | ⚠️ Exato JAR SHA + enumeração exaustiva das identidades + condições de registro + deduplicação; **não executado neste lote** |
| [Ars 'n' Spells](../providers/✅-ars-n-spells/README.md) | 3.3.4 | 5 | COUNTED_RELEASE_BOUNDED | ⚠️ Exato JAR SHA + enumeração exaustiva das identidades + condições de registro + deduplicação; **não executado neste lote** |
| [Apprentice's Codex](../providers/✅-apprentice-codex/README.md) | 0.9.7.1 | 83 | COUNTED_SOURCE_PINNED | ⚠️ Exato JAR SHA + enumeração exaustiva das identidades + condições de registro + deduplicação; **não executado neste lote** |
| [Backported Spellbooks](../providers/✅-backported-spellbooks/README.md) | physical 0.1.2 / embedded 0.1.0 | 6 | COUNTED_RELEASE_BOUNDED | ⚠️ Exato JAR SHA + enumeração exaustiva das identidades + condições de registro + deduplicação; **não executado neste lote** |
| [Deeper & Darker Spellbooks](../providers/✅-deeper-and-darker-spellbooks/README.md) | 1.3.3 Version B | 4 | COUNTED_RELEASE_BOUNDED | ⚠️ Exato JAR SHA + enumeração exaustiva das identidades + condições de registro + deduplicação; **não executado neste lote** |
| [Discerning The Eldritch](../providers/✅-discerning-the-eldritch/README.md) | 1.4.4 | 22 | COUNTED_SOURCE_PINNED | ⚠️ Exato JAR SHA + enumeração exaustiva das identidades + condições de registro + deduplicação; **não executado neste lote** |
| [Dreamless Spells](../providers/✅-dreamless-spells/README.md) | 1.1.9 | 4 | COUNTED_SOURCE_PINNED | ⚠️ Exato JAR SHA + enumeração exaustiva das identidades + condições de registro + deduplicação; **não executado neste lote** |
| [GTBC's Geomancy Plus](../providers/✅-gtbcs-geomancy-plus/README.md) | 1.1.0-1.21.1 | 12 | COUNTED_RELEASE_BOUNDED | ⚠️ Exato JAR SHA + enumeração exaustiva das identidades + condições de registro + deduplicação; **não executado neste lote** |
| [Farmer's Spell 'n Spellbooks](../providers/✅-farmers-spell/README.md) | 1.0.5.1-1.21.1 | 6 | COUNTED_SOURCE_PINNED | ⚠️ Exato JAR SHA + enumeração exaustiva das identidades + condições de registro + deduplicação; **não executado neste lote** |
| [SnackPirate's Aeromancy Additions](../providers/✅-aeromancy-additions/README.md) | 1.2.8 | 10 | COUNTED_SOURCE_PINNED | ⚠️ Exato JAR SHA + enumeração exaustiva das identidades + condições de registro + deduplicação; **não executado neste lote** |
| [Hazen N Stuff](../providers/✅-hazen-n-stuff/README.md) | 1.4.0.14 | 38 | COUNTED_SOURCE_PINNED | ⚠️ Exato JAR SHA + enumeração exaustiva das identidades + condições de registro + deduplicação; **não executado neste lote** |
| [Ender's Spells and Stuff: Requiem](../providers/✅-enders-spells-and-stuff-requiem/README.md) | 0.1.7 | 53 | COUNTED_SOURCE_PINNED | ⚠️ Exato JAR SHA + enumeração exaustiva das identidades + condições de registro + deduplicação; **não executado neste lote** |
| [Fire's Ender Expansion](../providers/✅-fires-ender-expansion/README.md) | 2.4.1 | 11 | COUNTED_SOURCE_PINNED | ⚠️ Exato JAR SHA + enumeração exaustiva das identidades + condições de registro + deduplicação; **não executado neste lote** |
| [IronSable](../providers/✅-ironsable/README.md) | 1.2.0 | 7 | COUNTED_RELEASE_BOUNDED | ⚠️ Exato JAR SHA + enumeração exaustiva das identidades + condições de registro + deduplicação; **não executado neste lote** |
| [ISS: Magic From The East](../providers/✅-iss-magic-from-the-east/README.md) | 1.1.5 | 22 | COUNTED_SOURCE_PINNED | ⚠️ Exato JAR SHA + enumeração exaustiva das identidades + condições de registro + deduplicação; **não executado neste lote** |
| [Legendary Spellbooks](../providers/✅-legendary-spellbooks/README.md) | 0.3.2 | 30 | COUNTED_SOURCE_PINNED | ⚠️ Exato JAR SHA + enumeração exaustiva das identidades + condições de registro + deduplicação; **não executado neste lote** |
| [Monsters & Spellbooks](../providers/✅-monsters-spellbooks/README.md) | 0.0.16.3 | 98 | COUNTED_RELEASE_BOUNDED | ⚠️ Exato JAR SHA + enumeração exaustiva das identidades + condições de registro + deduplicação; **não executado neste lote** |
| [Paladin Spells](../providers/✅-paladin-spells/README.md) | 1.1.1 | 5 | COUNTED_SOURCE_PINNED | ⚠️ Exato JAR SHA + enumeração exaustiva das identidades + condições de registro + deduplicação; **não executado neste lote** |
| [Wind's Spellbooks](../providers/✅-winds-spellbooks/README.md) | 1.0.5 | 7 | COUNTED_RELEASE_BOUNDED | ⚠️ Exato JAR SHA + enumeração exaustiva das identidades + condições de registro + deduplicação; **não executado neste lote** |
| [Ypsilon's Fundamentalism](../providers/✅-ypsilons-fundamentalism/README.md) | 1.1.7.1 | 15 | COUNTED_SOURCE_PINNED | ⚠️ Exato JAR SHA + enumeração exaustiva das identidades + condições de registro + deduplicação; **não executado neste lote** |
| [Tunes n' Tomes](../providers/✅-tunes-n-tomes/README.md) | 1.1.0-HOTFIX | 16 | COUNTED_RELEASE_BOUNDED | ⚠️ Exato JAR SHA + enumeração exaustiva das identidades + condições de registro + deduplicação; **não executado neste lote** |
| [Companions!](../providers/✅-companions/README.md) | 1.3.4 | 9 | COUNTED_SOURCE_PINNED | ⚠️ Exato JAR SHA + enumeração exaustiva das identidades + condições de registro + deduplicação; **não executado neste lote** |
| [Crystal Chronicles](../providers/✅-crystal-chronicles/README.md) | 0.1.3-alpha | 1 | COUNTED_SOURCE_PINNED | ⚠️ Exato JAR SHA + enumeração exaustiva das identidades + condições de registro + deduplicação; **não executado neste lote** |
| [Reliquified Ars Nouveau](../providers/✅-reliquified-ars-nouveau/README.md) | 0.8.1 | 19 | COUNTED_SOURCE_PINNED | ⚠️ Exato JAR SHA + enumeração exaustiva das identidades + condições de registro + deduplicação; **não executado neste lote** |
| [Reliquified Artifacts](../providers/✅-reliquified-artifacts/README.md) | 1.0.8 | 52 | COUNTED_SOURCE_PINNED | ⚠️ Exato JAR SHA + enumeração exaustiva das identidades + condições de registro + deduplicação; **não executado neste lote** |
| [Reliquified Iron's Spells 'n Spellbooks](../providers/✅-reliquified-irons-spells-n-spellbooks/README.md) | 0.2.7 | 25 | COUNTED_SOURCE_PINNED | ⚠️ Exato JAR SHA + enumeração exaustiva das identidades + condições de registro + deduplicação; **não executado neste lote** |
| [Waystones](../providers/✅-waystones/README.md) | 21.1.45 | 3 | COUNTED_SOURCE_PINNED | ⚠️ Exato JAR SHA + enumeração exaustiva das identidades + condições de registro + deduplicação; **não executado neste lote** |
| [Eidolon: Repraised](../providers/✅-eidolon-repraised/README.md) | 0.5.0.2 | 42 | COUNTED_SOURCE_PINNED | ⚠️ Exato JAR SHA + enumeração exaustiva das identidades + condições de registro + deduplicação; **não executado neste lote** |
| [Vampirism](../providers/✅-vampirism/README.md) | 1.10.13 | 19 | COUNTED_SOURCE_PINNED | ⚠️ Exato JAR SHA + enumeração exaustiva das identidades + condições de registro + deduplicação; **não executado neste lote** |
| [Bloodlines](../providers/✅-bloodlines/README.md) | 3.0.9 | 28 | COUNTED_SOURCE_PINNED | ⚠️ Exato JAR SHA + enumeração exaustiva das identidades + condições de registro + deduplicação; **não executado neste lote** |
| [Werewolves](../providers/✅-werewolves/README.md) | 2.0.3.3 | 8 | COUNTED_SOURCE_PINNED | ⚠️ Exato JAR SHA + enumeração exaustiva das identidades + condições de registro + deduplicação; **não executado neste lote** |
| [Hexalia](../providers/✅-hexalia/README.md) | 1.3.7 | 29 | COUNTED_SOURCE_PINNED | ⚠️ Exato JAR SHA + enumeração exaustiva das identidades + condições de registro + deduplicação; **não executado neste lote** |
| [Malum](../providers/✅-malum/README.md) | 1.8.2 | 26 | COUNTED_RELEASE_BOUNDED | ⚠️ Exato JAR SHA + enumeração exaustiva das identidades + condições de registro + deduplicação; **não executado neste lote** |

## Requisitos mínimos para encerrar cada linha

- Capturar **bytes do JAR da instância efetiva** ou uma fonte oficialmente reproduzível com igualdade criptográfica verificável, usando a modlist física atual como identidade do artefato.
- Inventariar apenas spell/ritual/glyph/discrete player-owned magical roots; documentar também registries excluídos e optional-provider gates para não criar falsos positivos.
- Comparar lista de IDs/nome/owner/namespace/condições e cardinalidade com o dossiê atual; sem correspondência binária não atualizar `COUNTED_SOURCE_PINNED`/`COUNTED_RELEASE_BOUNDED`.
- Revisar consumo, aquisição e configurações como **gate independente**: registry exato não equivale a magia habilitada nem obtenível em Survival.
- Não copiar classes, assets nem código proprietário de providers (clean-room). Reproduzir apenas observações e contratos de interoperabilidade publicados.
