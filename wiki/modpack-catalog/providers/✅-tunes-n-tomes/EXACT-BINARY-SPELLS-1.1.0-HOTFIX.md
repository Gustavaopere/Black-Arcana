# Tunes n' Tomes 1.1.0-HOTFIX — 16 inscrições físicas exatas de feitiços

**✅ `COUNTED_EXACT` 16/16 registries estáticos**, +0 raízes semânticas. Campanha: **19/39 exact / 20/39 pending**, mínimos **1857 global / 1855 escopo** inalterados. Runtime, configuração e Survival ⚠️.

## Fonte e inspeção Java 21

- Modlist física: `tunes_n_tomes-1.1.0-HOTFIX.jar`, mod ID `tunes_n_tomes`, SHA-1 `6cac45631ea63577f8eeeab454e1df0ce8f78386`, NeoForge/Minecraft 1.21.1.
- Artefato oficial [CurseForge 8370271](https://www.curseforge.com/minecraft/mc-mods/tunes-n-tomes-a-bards-journey/files/8370271) baixado via CurseMaven: **21.903.598 bytes**, SHA-1 igual ao da modlist.
- [Prova Java21 #38445001328](https://github.com/Gustavaopere/Black-Arcana/actions/runs/38445001328) **SUCCESS**; discovery [#38443961196](https://github.com/Gustavaopere/Black-Arcana/actions/runs/38443961196) também SUCCESS. Workflow `.github/workflows/audit-tunes-n-tomes-110-hotfix.yml` existe só na branch isolada `audit/tunes-n-tomes-110hotfix-20261013`, não entra na `main`.
- No bytecode `TunesNTomesMod` conecta `TSpellRegistry.register` ao event bus. `TSpellRegistry` usa `DeferredRegister<AbstractSpell>`, `SpellRegistry.SPELL_REGISTRY_KEY` e namespace `tunes_n_tomes`. O inicializador compilado chama `registerSpell` **16** vezes sem branches; o wrapper usa `spell.getSpellName()` e `DeferredRegister.register(..., Supplier)`.
- Cada classe listada existe, deriva `AbstractSpell`, expõe `getSpellResource` com literais do resource namespace/path e usa `DefaultConfig.setSchoolResource`. O provider declara a escola Melodic.

## Inventário — IDs literais, não derivados dos nomes

| # | Nome público | ResourceLocation | Classe compilada |
|---:|---|---|---|
| 1 | Chord Blast | `tunes_n_tomes:chord_blast` | `net.alshanex.tunes_n_tomes.spells.ChordBlastSpell` |
| 2 | Crescendo | `tunes_n_tomes:crescendo` | `net.alshanex.tunes_n_tomes.spells.CrescendoSpell` |
| 3 | Grand Finale | `tunes_n_tomes:grand_finale` | `net.alshanex.tunes_n_tomes.spells.GrandFinaleSpell` |
| 4 | Celestial Chant | `tunes_n_tomes:celestial_chant` | `net.alshanex.tunes_n_tomes.spells.CelestialChantSpell` |
| 5 | Rhapsody | `tunes_n_tomes:rhapsody` | `net.alshanex.tunes_n_tomes.spells.RhapsodySpell` |
| 6 | Sonata | `tunes_n_tomes:sonata` | `net.alshanex.tunes_n_tomes.spells.SonataSpell` |
| 7 | Serenade | `tunes_n_tomes:serenade` | `net.alshanex.tunes_n_tomes.spells.SerenadeSpell` |
| 8 | Fortissimo | `tunes_n_tomes:fortissimo` | `net.alshanex.tunes_n_tomes.spells.FortissimoSpell` |
| 9 | Dal Segno | `tunes_n_tomes:dal_segno` | `net.alshanex.tunes_n_tomes.spells.DalSegnoSpell` |
| 10 | Swift Melody | `tunes_n_tomes:swift_melody` | `net.alshanex.tunes_n_tomes.spells.SwiftMelodySpell` |
| 11 | Hymn of Hope | `tunes_n_tomes:hymn_of_hope` | `net.alshanex.tunes_n_tomes.spells.HymnOfHopeSpell` |
| 12 | Slumber Note | `tunes_n_tomes:slumber_note` | `net.alshanex.tunes_n_tomes.spells.SlumberNoteSpell` |
| 13 | Clamor Note | `tunes_n_tomes:clamor_note` | `net.alshanex.tunes_n_tomes.spells.ClamorNoteSpell` |
| 14 | Encore | `tunes_n_tomes:encore` | `net.alshanex.tunes_n_tomes.spells.EncoreSpell` |
| 15 | Harmonic Aria | `tunes_n_tomes:harmonic_aria` | `net.alshanex.tunes_n_tomes.spells.HarmonicAriaSpell` |
| 16 | Piercing Solo | `tunes_n_tomes:piercing_solo` | `net.alshanex.tunes_n_tomes.spells.PiercingSoloSpell` |

As [16 fichas](SPELL-CARDS-1.1.0-HOTFIX.md) já existiam em confiança publisher; esta inspeção promove apenas registro estático para `COUNTED_EXACT`. **`PHYSICAL_SPELL_REGISTRATIONS=16`**, **`EXACT_STATIC_REGISTRY_AUDIT=PASS`**, **`NEW_SEMANTIC_ROOTS=0`**. Projéteis, Segno, Resonance e outras subações não geram novos spells, tampouco Sound School migrada de Alshanex/FamiliarsLib.

## ⚠️ Gate de execução e propriedade

Não houve boot de cliente, dedicated server ou testes de Survival do modpack real. O HOTFIX anuncia Iron's **3.16.2**; o pack usa **3.16.3**. Permanecem desconhecidos: config efetiva, custo/cooldown, receitas e acesso em Survival, cast e multiplayer, causalidade/recursão de Encore, persistência e amplificação de Segno/Resonance, e hooks de integração estáveis. `Stage 06.05` segue 🟡; sem certificação runtime.

Iron's controla casting/mana; Tunes controla spells, efeitos e Resonance; Black Arcana conserva seu próprio runtime, sem copiar código/asset do provider ou duplicar custos; RPG Skill Tree é apenas progression/gates por contratos reais. Auditoria clean-room limitada a símbolos/metadata compilados.
