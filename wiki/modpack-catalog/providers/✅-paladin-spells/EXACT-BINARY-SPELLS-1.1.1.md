# Paladin Spells 1.1.1 — cinco registros mágicos comprovados no JAR físico

**✅ 5/5 identidades de spell `COUNTED_EXACT` somente para registry estático. ⚠️ Sem aprovação de execução em jogo.**

## Âncora física

- Sibling modlist certificada na posição **#432**, `paladin_spells-1.21.1-1.1.1.jar`, mod ID `paladin_spells`, NeoForge 1.21.1; SHA-1 `e4c6f4fa70989f0b9f1819e46e29f68d414ccbaf`. Evidência: [dossiê físico sibling](https://github.com/Gustavaopere/neoforge-rpg-skilltree/blob/06ec1d1d586d4fc3cf957223cfc9ac30077f2875/PROJECT-INSTRUCTIONS/modlist/Addons%20%2B%20Magic/%E2%9C%85-paladin-spells-irons-spells-addon%20v1.21.1-1.1.1.md).
- Artefato publicado: [CurseForge project 1593269 / file 8661566](https://www.curseforge.com/minecraft/mc-mods/paladin-spells-irons-spells-addon/files/8661566), release NeoForge 1.21.1 de 2026-08-16. O JAR baixado nessa auditoria mede **1858683 bytes**; `sha1sum --check` confirmou correspondência com o SHA-1 do arquivo registrado no snapshot físico.
- Auditoria **isolada não-merge**: [GitHub Actions #38308575364](https://github.com/Gustavaopere/Black-Arcana/actions/runs/38308575364), commit `e52b3cccfdba3a1849b4a28d33044bdb43d6bc37`, job `binary-identity` **SUCCESS**; `zipfile.testzip()` e `javap -c -p` com Java 21, sem execução do provider.
- Source pin [Kaufko/Paladin-Spells@31f64ccdb39d062b21cc25d434cb62d6463b486e](https://github.com/Kaufko/Paladin-Spells/tree/31f64ccdb39d062b21cc25d434cb62d6463b486e) confirma cinco registrations no checkpoint `1.21.1-1.1.1`. Não há alegação de compilação reproduzível source→JAR; só JAR do publicador ↔ hash físico.

## Cinco roots / cinco registros literais

| # | Classe física própria | Registry ID | Evidência |
|---:|---|---|---|
| 1 | `TauntSpell` | `paladin_spells:taunt` | `EXACT_BINARY_STATIC` |
| 2 | `BulwarkSpell` | `paladin_spells:bulwark` | `EXACT_BINARY_STATIC` |
| 3 | `SwornProtectorSpell` | `paladin_spells:sworn_protector` | `EXACT_BINARY_STATIC` |
| 4 | `BedrockSkinSpell` | `paladin_spells:bedrock_skin` | `EXACT_BINARY_STATIC` |
| 5 | `RamSpell` | `paladin_spells:ram` | `EXACT_BINARY_STATIC` |

O log do job confirma cinco classes top-level `*Spell.class` sob `eu/kaufko/paladin_spells/spells/`, `STATIC_DEFERRED_REGISTER_INVOCATIONS=5`, `STATIC_REGISTRATION_PATHS=['taunt', 'bulwark', 'sworn_protector', 'bedrock_skin', 'ram']`, `ENTRYPOINT_TO_REGISTRY=present` e `RESULT=EXACT_STATIC_BINARY_REGISTRY_FIVE_IDS`. O registrador `PaladinSpellRegistry` instancia cinco DeferredRegistrations e o entrypoint `PaladinSpells` chama seu bootstrap. Não foi identificada uma sexta root na superfície examinada. Classes de efeitos, Armor, partículas e outras entidades não contam como novas spells.

## Alcance da promoção e gates

As cinco magias já integravam o ledger. A promoção é `COUNTED_SOURCE_PINNED → COUNTED_EXACT` **exclusivamente para identidade/cardinalidade de registry estático**: **+0 novas magias**, campanha original **5/39 exatos / 34/39 pendentes**, mínimos **1851 global / 1849 escopo** inalterados. O denominador global completo permanece desconhecido.

**⚠️ Não aprovados:** loader/registro efetivo no modpack, compatibilidade real de Iron's 3.16.3, Scroll Forge, raridades ou desbloqueios, configuração, mana/cooldown aplicados, Bulwark Armor `0.0` no source, Sworn Protector authority cliente/servidor, ausência de consumidor estático para Bedrock Skin reduction, friendly-fire do Ram, comportamento Taunt em mobs customizados, cliente, multiplayer, dedicated-server e Survival. O changelog upstream que corrige server crash não prova que a instância montada inicia.

Iron's continua com authority de host casting, mana e cooldown; Paladin Spells é owner de suas cinco magias, efeitos e mecânicas Holy. Black Arcana não copia código/bytecode/arte/receitas e não replica settlement. RPG Skill Tree permanece sibling de progressão apenas por contracts reais. Stage 06.05 não avança e os gates de Survival permanecem bloqueados até prova física.
