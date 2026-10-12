# Backported Spellbooks 0.1.2 — seis registros de feitiços no JAR físico

**✅ 6/6 identidades `COUNTED_EXACT` exclusivamente quanto ao registro binário estático. ⚠️ Configuração instalada, execução e Survival não foram aprovados.**

## Proveniência exata

- Sibling físico `neoforge-rpg-skilltree/main@06ec1d1d586d4fc3cf957223cfc9ac30077f2875`: posição **#63**, `backportedspellbooks-0.1.2.jar`, mod ID `backportedspellbooks`, SHA-1 `747847c1f38c73250ebac05ea06b41a381187850`.
- Publicador: [CurseForge project 1543731 / file 8158731](https://www.curseforge.com/minecraft/mc-mods/backported-spells-irons-spells-x-vanilla-backport/files/8158731), NeoForge 1.21.1. Artefato oficial de **209868 bytes**; comparação `sha1sum --check` confirmou byte identity com o SHA-1 do snapshot físico.
- `META-INF/neoforge.mods.toml` do **JAR físico exato** declara `modId="backportedspellbooks"`, `version="0.1.0"`. **A divergência `0.1.2` (arquivo/publicação) versus `0.1.0` (metadata de execução) é real e não foi corrigida artificialmente.**
- Prova isolada não-merge: [GitHub Actions #38318268989](https://github.com/Gustavaopere/Black-Arcana/actions/runs/38318268989), commit `453fcefe5639c87dcb11be4f36a7f88a6882f78a`, job `static-jar-proof` **SUCCESS** com Java 21, `javap -p -c` e integridade ZIP.
- Source do publicador em [RedReaper28/BackportedSpellbooks-1.21.1@07cb65efca0c264762a21c2d6bce0f83e3947226](https://github.com/RedReaper28/BackportedSpellbooks-1.21.1/tree/07cb65efca0c264762a21c2d6bce0f83e3947226), de mesma data de release, é somente baseline comparativo. **Não há alegação de build reproduzível source→JAR.**

## Identidade estática e cardinalidade

O registrador binário `net.redreaper.backported_spellbooks.init.ModSpellRegistry` constrói e passa **seis** objetos de spell para `registerSpell(AbstractSpell)`. O helper usa `AbstractSpell.getSpellName()` e chama `DeferredRegister.register(String, Supplier)`, com `SpellRegistry.SPELL_REGISTRY_KEY`; o entrypoint `BackportedSpellbooks` chama o registrador no mod event bus. Cada classe física contém namespace `backportedspellbooks` e sua respectiva chave `getSpellResource()`.

| # | Classe física | Campo estático | Registry ID |
|---:|---|---|---|
| 1 | `AspectOfTheSlimeSpell` | `SLIME_ASPECT` | `backportedspellbooks:slime_aspect` |
| 2 | `SulfurBombSPell` | `SULFUR_BOMB` | `backportedspellbooks:sulfur_bomb` |
| 3 | `SulfurCloudSpell` | `SULFUR_CLOUD` | `backportedspellbooks:sulfur_clouds` |
| 4 | `SulfurReleaseSpell` | `SULFUR_RELEASE` | `backportedspellbooks:sulfur_release` |
| 5 | `PaleThornSpell` | `PALE_THORN` | `backportedspellbooks:pale_thorn` |
| 6 | `ResinSpraySpell` | `RESIN_SPRAY` | `backportedspellbooks:resin_spray` |

A grafia `SulfurBombSPell` (com **SP** maiúsculos) pertence ao binário; um filtro simples de `*Spell.class` a perderia. `PaleThornSpell` herda por meio de `AbstractPaleSpells`, cujo pai físico é o `io.redspace.ironsspellbooks.api.spells.AbstractSpell`. Não constitui um novo tipo/identidade semântica.

Evidência do run: `OWNED_SPELL_CLASS_COUNT=6`, `STATIC_REGISTER_SPELL_INVOCATIONS=6`, `REGISTRATION_HELPER_DEFERRED_REGISTER_CALLS=1`, `ENTRYPOINT_TO_REGISTRY=present` e `RESULT=EXACT_SIX_BINARY_STATIC_SPELL_REGISTRATIONS`. Os seis literais e campos passaram asserções independentes.

## Alcance da promoção

As seis spells já constam do ledger. Promoção `COUNTED_RELEASE_BOUNDED → COUNTED_EXACT` **só para identidade/cardinalidade de registro estático**, **+0 magias novas**, campanha congelada de 39 providers **7/39 exatos / 32/39 pendentes**, mínimos **1851 global / 1849 escopo** inalterados. O denominador semântico completo permanece desconhecido.

**⚠️ Não verificados:** carregamento conjunto Iron's 3.16.3 / Vanilla Backport / Ace's Spell Utils, optional hard dependencies, versão efetiva percebida pelo loader, configs, efeitos, mana/cooldown, níveis, loot/Scroll Forge, atributos/procs de equipamentos, worldgen, dedicated server real do pack, cliente, PvP/multiplayer, aquisição e Survival. Dados numéricos documentados em [SPELLS-AND-IRON-RUNTIME.md](SPELLS-AND-IRON-RUNTIME.md) derivam do source oficial de referência e **não** são evidência dos números efetivos instalados.

Iron's permanece autoridade de casting, mana/cooldown e host networking; Backported Spellbooks é owner de suas seis spells, school `pale_flora` e efeitos; Black Arcana não duplica a execução ou os procs do provider. RPG Skill Tree continua sibling de progressão mediante contrato. Nenhum código ou ativo de terceiros foi incorporado. Stage 06.05 segue 🟡.
