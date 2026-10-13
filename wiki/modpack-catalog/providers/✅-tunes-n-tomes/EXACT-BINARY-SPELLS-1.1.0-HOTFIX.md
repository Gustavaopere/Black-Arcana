# Tunes n' Tomes 1.1.0-HOTFIX — 16 registros binários de feitiços SHA-exatos

**✅ COUNTED_EXACT para o registry estático de 16/16 spells**, com **+0 novas identidades semânticas** (as 16 já estavam contabilizadas). Campanha dos 39 providers: **19/39 exatos / 20/39 pendentes**. Mínimo estrito **1857 global / 1855 escopo** inalterado. Configuração, gameplay e Survival **⚠️ não verificados**.

## Proveniência e integridade

- Modlist física do sibling: `tunes_n_tomes-1.1.0-HOTFIX.jar`, mod ID `tunes_n_tomes`, Minecraft 1.21.1 / NeoForge, SHA-1 `6cac45631ea63577f8eeeab454e1df0ce8f78386`.
- Publisher [CurseForge file 8370271](https://www.curseforge.com/minecraft/mc-mods/tunes-n-tomes-a-bards-journey/files/8370271): `21903598` bytes, SHA-1 `6cac45631ea63577f8eeeab454e1df0ce8f78386`, idêntico ao registro da modlist.
- [Discovery Java 21 #38443961196](https://github.com/Gustavaopere/Black-Arcana/actions/runs/38443961196) **SUCCESS**; [auditoria com asserções Java 21 #38445001328](https://github.com/Gustavaopere/Black-Arcana/actions/runs/38445001328) **SUCCESS**.
- Workflow técnico isolado na branch [`audit/tunes-n-tomes-110hotfix-20261013`](https://github.com/Gustavaopere/Black-Arcana/tree/audit/tunes-n-tomes-110hotfix-20261013); não adicionar este workflow à `main`, que permanece de catálogo/runtime canônico. JAR terceiro não é copiado ao repositório.

## Topologia compilada comprovada

- `net.alshanex.tunes_n_tomes.TunesNTomesMod` conecta `TSpellRegistry.register` ao bootstrap.
- `net.alshanex.tunes_n_tomes.registry.TSpellRegistry` inicializa `DeferredRegister<AbstractSpell>`, usando `SpellRegistry.SPELL_REGISTRY_KEY` e namespace `tunes_n_tomes`.
- O inicializador instancia as **16** classes abaixo e invoca o wrapper `registerSpell(AbstractSpell)` exatamente 16 vezes, sem branches/loops condicionais no bloco inspecionado; o wrapper envia `getSpellName()` ao `DeferredRegister.register(...)`.
- Cada classfile tem `getSpellResource()`, `ResourceLocation.fromNamespaceAndPath` com namespace e sufixo literais abaixo e chamada de `DefaultConfig.setSchoolResource(...)`. A configuração de escola específica, os valores efetivos e o runtime Melodic não foram testados; a escola Melodic é identificada pela documentação do provider.

## Identidades exatas no JAR

| # | Feitiço publicado | ResourceLocation compilada | Classe compilada |
|---:|---|---|---|
| 1 | Chord Blast | `tunes_n_tomes:chord_blast` | `net.alshanex.tunes_n_tomes.spells.ChordBlastSpell` |
| 2 | Crescendo | `tunes_n_tomes:crescendo` | `net.alshanex.tunes_n_tomes.spells.CrescendoSpell` |
| 3 | Grand Finale | `tunes_n_tomes:grand_finale` | `net.alshanex.tunes_n_tomes.spells.GrandFinaleSpell` |
| 4 | Celestial Chant | `tunes_n_tomes:celestial_chant` | `net.alshanex.tunes_n_tomes.spells.CelestialChantSpell` |
| 5 | Rhapsody | `tunes_n_tomes:rhapsody` | `net.alshanex.tunes_n_tomes.spells.RhapsodySpell` |
| 6 | Sonata | `tunes_n_tomes:sonata` | `net.alshanex.tunes_n_tomes.spells.SonataSpell` |
| 7 | Serenade | `tunes_n_tomes:serenade` | `net.alshanex.tunes_n_tomes.spells.SerenadeSpell` |
| 8 | Dal Segno | `tunes_n_tomes:dal_segno` | `net.alshanex.tunes_n_tomes.spells.DalSegnoSpell` |
| 9 | Encore | `tunes_n_tomes:encore` | `net.alshanex.tunes_n_tomes.spells.EncoreSpell` |
| 10 | Fortissimo | `tunes_n_tomes:fortissimo` | `net.alshanex.tunes_n_tomes.spells.FortissimoSpell` |
| 11 | Swift Melody | `tunes_n_tomes:swift_melody` | `net.alshanex.tunes_n_tomes.spells.SwiftMelodySpell` |
| 12 | Hymn of Hope | `tunes_n_tomes:hymn_of_hope` | `net.alshanex.tunes_n_tomes.spells.HymnOfHopeSpell` |
| 13 | Slumber Note | `tunes_n_tomes:slumber_note` | `net.alshanex.tunes_n_tomes.spells.SlumberNoteSpell` |
| 14 | Clamor Note | `tunes_n_tomes:clamor_note` | `net.alshanex.tunes_n_tomes.spells.ClamorNoteSpell` |
| 15 | Harmonic Aria | `tunes_n_tomes:harmonic_aria` | `net.alshanex.tunes_n_tomes.spells.HarmonicAriaSpell` |
| 16 | Piercing Solo | `tunes_n_tomes:piercing_solo` | `net.alshanex.tunes_n_tomes.spells.PiercingSoloSpell` |

**PHYSICAL_SPELL_REGISTRATIONS=16**
**NEW_SEMANTIC_ROOTS=0**
**EXACT_STATIC_REGISTRY_AUDIT=PASS**
**PUBLISHER_EQUALS_PHYSICAL_SHA1=PASS**
**RUNTIME_SURVIVAL_NOT_VERIFIED=TRUE**

## Exclusões semânticas e authority

- Os 16 registros correspondem às 16 fichas editoriais já existentes: nenhum duplicado é gerado por normalização de nomes; o ID literal é a autoridade.
- Resonance/Segno, marcadores, recasts derivados e armadura Bard são caminhos de execução/amplificação do provider, não novas identidades de spell por efeito/instância.
- Conteúdo Sound removido de Alshanex/FamiliarsLib 4.x não pode ser recontabilizado.
- Iron's é o substrate de casting/mana/cooldowns; Tunes n' Tomes é authority da identidade Melodic e de Resonance/Segno. Black Arcana não deve criar uma segunda cobrança ou atribuição de cast. RPG Skill Tree continua responsável apenas por progressão/perks/gates através de contratos verificados.

## Gates ainda abertos

**⚠️** A release HOTFIX menciona compatibilidade com Iron's 3.16.2, enquanto o pack tem 3.16.3. Os logs de auditoria validam o JAR estaticamente, **não** confirmam carga em cliente, servidor dedicado, execução dos 16 casts, aquisição Survival, valores ativos de mana/cooldown, autorização/PvP, Resonance/Segno lifecycle/persistência/multiplayer ou Encore forced-recast/recursion. Exigir evidência do modpack real antes de declarar integração ou runtime PASS.

Clean-room: somente metadados de registries/classes/IDs e propriedades observáveis foram documentados; não copiar corpos de implementação, assets ou textos do provider.
