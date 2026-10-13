# Discerning The Eldritch 1.4.4-1.21 — 22 registros exatos do JAR físico

**✅ `COUNTED_EXACT` de 22/22 inscrições estáticas `AbstractSpell`, sem novos objetos semânticos**. Campanha de 39 providers: **22/39 exatos / 17/39 pendentes**. O mínimo estrito permanece **1857 global / 1855 escopo**. Registry provado; valores efetivos/casting/Survival **⚠️**.

## Proveniência publisher/físico e evidência

- Modlist física sibling, item **#220**: `discerning_the_eldritch-1.4.4-1.21.jar`, mod ID `discerning_the_eldritch`, SHA-1 `cf35c225aced23b705d1e0fd1bc5c62d96540e0c`.
- Release oficial [CurseForge File ID 8816497](https://www.curseforge.com/minecraft/mc-mods/discerning-the-eldritch/files/8816497), **22098930 bytes**, SHA-1 `cf35c225aced23b705d1e0fd1bc5c62d96540e0c`, idêntico ao registro físico do pack.
- [Discovery Java21 #38455035362](https://github.com/Gustavaopere/Black-Arcana/actions/runs/38455035362) **SUCCESS**; [auditoria de asserções do registry, 22 IDs/classes/escolas #38455449207](https://github.com/Gustavaopere/Black-Arcana/actions/runs/38455449207) **SUCCESS**.
- Workflow clean-room fica apenas em [`audit/discerning-eldritch-144-20261013`](https://github.com/Gustavaopere/Black-Arcana/tree/audit/discerning-eldritch-144-20261013), sem artefatos proprietários copiados à `main`.

## Inscrições comprovadas no bytecode

- `net.acetheeldritchking.discerning_the_eldritch.DiscerningTheEldritch` conecta `SpellRegistries.register` ao bootstrap.
- `net.acetheeldritchking.discerning_the_eldritch.registries.SpellRegistries` registra `DeferredRegister<AbstractSpell>` em `SpellRegistry.SPELL_REGISTRY_KEY`, namespace `discerning_the_eldritch`.
- O inicializador possui **22** instances/classes únicas e **22** chamadas a `registerSpell(AbstractSpell)`, sem branches condicionais no bloco de inicialização.
- Cada classe compila `ResourceLocation.fromNamespaceAndPath(`namespace literal`, `suffix literal`)`, gravado no campo `spellId` e usado na configuração do spell. As referências padrão da escola foram verificadas nos classfiles: `SchoolRegistry.*_RESOURCE` para seis escolas Iron's e `DTESchoolRegistry.RITUAL_RESOURCE` para Ritual.
- A antiga publicação oficial descreve 15 magias e nomeia 14; a autoridade de identidade física atual é o registrador **22** inspecionado, sem inferir 15ª identidade pelo marketing.

## Inventário exato de 22 magias

| # | Nome catalogado | ResourceLocation no JAR | Classe exata | Ficha |
|---:|---|---|---|---|
| 1 | Silence | `discerning_the_eldritch:silence` | `net.acetheeldritchking.discerning_the_eldritch.spells.eldritch.SilenceSpell` | [Ficha](eldritch/silence.md) |
| 2 | Conjure Forsaken Aid | `discerning_the_eldritch:conjure_forsaken_aid` | `net.acetheeldritchking.discerning_the_eldritch.spells.eldritch.ConjureForsakenAidSpell` | [Ficha](eldritch/conjure-forsaken-aid.md) |
| 3 | Esoteric Edge | `discerning_the_eldritch:esoteric_edge` | `net.acetheeldritchking.discerning_the_eldritch.spells.eldritch.EsotericEdgeSpell` | [Ficha](eldritch/esoteric-edge.md) |
| 4 | Conjure Gaoler | `discerning_the_eldritch:conjure_gaoler` | `net.acetheeldritchking.discerning_the_eldritch.spells.eldritch.ConjureGaolerSpell` | [Ficha](eldritch/conjure-gaoler.md) |
| 5 | Otherworldly Presence | `discerning_the_eldritch:otherworldly_presence` | `net.acetheeldritchking.discerning_the_eldritch.spells.eldritch.OtherworldlyPresenceSpell` | [Ficha](eldritch/otherworldly-presence.md) |
| 6 | Mend Flesh | `discerning_the_eldritch:mend_flesh` | `net.acetheeldritchking.discerning_the_eldritch.spells.eldritch.MendFleshSpell` | [Ficha](eldritch/mend-flesh.md) |
| 7 | Rift Walker | `discerning_the_eldritch:rift_walker` | `net.acetheeldritchking.discerning_the_eldritch.spells.eldritch.RiftWalkerSpell` | [Ficha](eldritch/rift-walker.md) |
| 8 | Abracadabra | `discerning_the_eldritch:abracadabra` | `net.acetheeldritchking.discerning_the_eldritch.spells.eldritch.AbracadabraSpell` | [Ficha](eldritch/abracadabra.md) |
| 9 | Esoteric Strike | `discerning_the_eldritch:esoteric_strike` | `net.acetheeldritchking.discerning_the_eldritch.spells.eldritch.EsotericStrikeSpell` | [Ficha](eldritch/esoteric-strike.md) |
| 10 | Vein Ripper | `discerning_the_eldritch:vein_ripper` | `net.acetheeldritchking.discerning_the_eldritch.spells.blood.VeinRipperSpell` | [Ficha](blood/vein-ripper.md) |
| 11 | Boogie Woogie | `discerning_the_eldritch:boogie_woogie` | `net.acetheeldritchking.discerning_the_eldritch.spells.evocation.BoogieWoogieSpell` | [Ficha](evocation/boogie-woogie.md) |
| 12 | Guardian's Gaze | `discerning_the_eldritch:guardians_gaze` | `net.acetheeldritchking.discerning_the_eldritch.spells.evocation.GuardiansGazeSpell` | [Ficha](evocation/guardians-gaze.md) |
| 13 | Soul Slice | `discerning_the_eldritch:soul_slice` | `net.acetheeldritchking.discerning_the_eldritch.spells.fire.SoulSliceSpell` | [Ficha](fire/soul-slice.md) |
| 14 | Soul Set Ablaze | `discerning_the_eldritch:soul_set_ablaze` | `net.acetheeldritchking.discerning_the_eldritch.spells.fire.SoulSetAblazeSpell` | [Ficha](fire/soul-set-ablaze.md) |
| 15 | Exorcism | `discerning_the_eldritch:exorcism` | `net.acetheeldritchking.discerning_the_eldritch.spells.holy.ExorcismSpell` | [Ficha](holy/exorcism.md) |
| 16 | Glacial Edge | `discerning_the_eldritch:glacial_edge` | `net.acetheeldritchking.discerning_the_eldritch.spells.ice.GlacialEdgeSpell` | [Ficha](ice/glacial-edge.md) |
| 17 | Crystalline Carver | `discerning_the_eldritch:crystalline_carver` | `net.acetheeldritchking.discerning_the_eldritch.spells.ice.CrystallineCarverSpell` | [Ficha](ice/crystalline-carver.md) |
| 18 | Call Ascended One | `discerning_the_eldritch:call_ascended_one` | `net.acetheeldritchking.discerning_the_eldritch.spells.ritual.CallAscendedOneSpell` | [Ficha](ritual/call-ascended-one.md) |
| 19 | Blades Of Rancor | `discerning_the_eldritch:blades_of_rancor` | `net.acetheeldritchking.discerning_the_eldritch.spells.ritual.BladesOfRancorSpell` | [Ficha](ritual/blades-of-rancor.md) |
| 20 | Zealous Harbinger | `discerning_the_eldritch:zealous_harbinger` | `net.acetheeldritchking.discerning_the_eldritch.spells.ritual.ZealousHarbingerSpell` | [Ficha](ritual/zealous-harbinger.md) |
| 21 | Ravenous Revenant | `discerning_the_eldritch:ravenous_revenant` | `net.acetheeldritchking.discerning_the_eldritch.spells.ritual.RavenousRevenantSpell` | [Ficha](ritual/ravenous-revenant.md) |
| 22 | Libras Judgement | `discerning_the_eldritch:libras_judgement` | `net.acetheeldritchking.discerning_the_eldritch.spells.ritual.LibrasJudgementSpell` | [Ficha](ritual/libras-judgement.md) |

**Distribuição:** Eldritch 9; Blood 1; Evocation 2; Fire 2; Holy 1; Ice 2; Ritual 5.

**PUBLISHER_EQUALS_PHYSICAL_SHA1=PASS**

**PHYSICAL_SPELL_REGISTRATIONS=22**

**STATIC_INITIALIZER_BRANCHES=0**

**NEW_SEMANTIC_ROOTS=0**

**EXACT_STATIC_REGISTRY_AUDIT=PASS**

**RUNTIME_SURVIVAL_NOT_VERIFIED=TRUE**

## Exclusões, restrições e contratos de autoridade

- `discerning_the_eldritch:glacial_edge` é o ID ativo compilado do feitiço anunciado como *Glacial Cleave*; não criar uma segunda identidade. Registrations hipotéticas/comentadas não compõem o inventário.
- Os cinco itens Ritual são **spells do provider Iron's/DTE** e não registros do `RitualEngine` próprio do Black Arcana. A escola Ritual, suas restrições de cast/loot e lógica de execução pertencem ao DTE.
- `ExorcismSpell` consta incondicionalmente no registry físico, mas o sistema Insanity tem configuração default **desabilitada** segundo a fonte; disponibilidade/uso real do spell **⚠️** até observar config e runtime.
- O modpack físico registra Iron's **3.16.3**, Ace's Spell Utils **1.2.7.2-1.21.1** e AzureLib **3.1.11**. A release 1.4.4 corrige crash/config anteriores, mas isso **não prova compatibilidade operacional** deste conjunto sem teste.
- Permanecem ⚠️: mana/cooldown ativo, dano, casts/recasts e cancelamentos, Soul Fire e Frostbite, Insanity, spells Ritual complex/supercomplex, aquisição/loot, summons, relog, clientes, servidor dedicado, multiplayer e Survival. Observações estáticas preexistentes sobre Ravenous Revenant, Zealous Harbinger, Guardian's Gaze, Crystalline Carver e Otherworldly Presence não são promovidas a correções.
- DTE responde por conteúdo, schools, efeitos e criaturas próprias; Iron's por framework de casting/mana; Black Arcana por seu runtime mágico; RPG Skill Tree exclusivamente por progressão/perks/gates via contratos verificados. Sem boundary real, qualquer integração opcional deve falhar com segurança.
