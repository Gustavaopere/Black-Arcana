# Ypsilon's Fundamentalism / Fundamental Principles 1.1.7.1 — 15 registries físicos exatos

**✅ `COUNTED_EXACT` para 15/15 registros binários estáticos**, sem novos objetos semânticos (**+0**). Campanha dos 39 providers: **18/39 exact / 21/39 pending**. Mínimos estritos **1857 global / 1855 escopo**, inalterados. Os **13 Principles** não são novas magias. Runtime/configuração/Survival ainda ⚠️.

## Origem e integridade

- Modlist física do sibling: `#575`, JAR `ypfundamentals-1.1.7.1.jar`, mod ID `ypfundamentals`, Minecraft 1.21.1/NeoForge, SHA-1 **`a2855c253202a8fcc2925fcf5b1bf86d64fbe4da`**.
- [CurseForge file 8558503](https://www.curseforge.com/minecraft/mc-mods/fundamental-principles/files/8558503): título público `fundamental_principles_v_1.1.7.1.jar`, nome interno declarado `ypfundamentals-1.1.7.1.jar`; CurseMaven forneceu **858749 bytes**, SHA-1 idêntico ao registro físico. Não são dois mods.
- [Auditoria Java21 #38436717443](https://github.com/Gustavaopere/Black-Arcana/actions/runs/38436717443) **SUCCESS**, após [discovery #38436546247](https://github.com/Gustavaopere/Black-Arcana/actions/runs/38436546247) SUCCESS. Workflow técnico `audit/ypsilon-fundamentals-1171-20261013` fica isolado, não entra em `main`.
- `FundamentalPrinciples → ModSpells.register(IEventBus) → YPSPELLS.register(bus)`; `ModSpells.<clinit>` cria `DeferredRegister<AbstractSpell>` para `SpellRegistry.SPELL_REGISTRY_KEY` com namespace `ypfundamentals` e realiza **15** chamadas incondicionais ao wrapper `registerSpell(AbstractSpell)`; o wrapper chama `DeferredRegister.register(spell.getSpellName(), Supplier)`. Cada classe possui `getSpellResource`, sufixo literal, `ResourceLocation.fromNamespaceAndPath` e escola padrão compilada `SchoolRegistry`/`YpsSchoolRegistry`. Sem branches no initializer.

## Inventário de identidades exatas

| # | ResourceLocation | Classe compilada | Escola default | Ficha |
|---:|---|---|---|---|
| 1 | `ypfundamentals:chains` | `com.ypsi.fundamentalism.spells.ice.ChainsSpell` | Ice | [Ficha](ice/frozen-chains.md) |
| 2 | `ypfundamentals:grantstrength` | `com.ypsi.fundamentalism.spells.fire.BurningSpiritSpell` | Fire | [Ficha](fire/burning-spirit.md) |
| 3 | `ypfundamentals:pyrokinesis` | `com.ypsi.fundamentalism.spells.fire.PyrokinesisSpell` | Fire | [Ficha](fire/pyrokinesis.md) |
| 4 | `ypfundamentals:sol` | `com.ypsi.fundamentalism.spells.fire.SolSpell` | Fire | [Ficha](fire/tonatiuh.md) |
| 5 | `ypfundamentals:ignite` | `com.ypsi.fundamentalism.spells.fire.IgniteSpell` | Fire | [Ficha](fire/ignite.md) |
| 6 | `ypfundamentals:bloodstream` | `com.ypsi.fundamentalism.spells.blood.BloodstreamSpell` | Blood | [Ficha](blood/bloodstream.md) |
| 7 | `ypfundamentals:thorn` | `com.ypsi.fundamentalism.spells.blood.ThornSpell` | Blood | [Ficha](blood/thorn.md) |
| 8 | `ypfundamentals:laceration` | `com.ypsi.fundamentalism.spells.blood.LacerationSpell` | Blood | [Ficha](blood/laceration.md) |
| 9 | `ypfundamentals:holy_lightning` | `com.ypsi.fundamentalism.spells.holy.HolyLightningSpell` | Holy | [Ficha](holy/holy-lightning.md) |
| 10 | `ypfundamentals:sacred_disk` | `com.ypsi.fundamentalism.spells.holy.SacredDiskSpell` | Holy | [Ficha](holy/sacred-disk.md) |
| 11 | `ypfundamentals:pull_spell` | `com.ypsi.fundamentalism.spells.ender.PullSpell` | Ender | [Ficha](ender/pull.md) |
| 12 | `ypfundamentals:lapsus` | `com.ypsi.fundamentalism.spells.ender.LapsusSpell` | Ender | [Ficha](ender/lapsus.md) |
| 13 | `ypfundamentals:taunt` | `com.ypsi.fundamentalism.spells.evocation.TauntSpell` | Evocation | [Ficha](evocation/taunt.md) |
| 14 | `ypfundamentals:law_of_regression` | `com.ypsi.fundamentalism.spells.fundamentalism.LawOfRegressionSpell` | Fundamentalism | [Ficha](fundamentalism/law-of-regression.md) |
| 15 | `ypfundamentals:saeptum` | `com.ypsi.fundamentalism.spells.fundamentalism.SaeptumSpell` | Fundamentalism | [Ficha](fundamentalism/saeptum.md) |

**Aliases importantes:** Frozen Chains = `ypfundamentals:chains`; Burning Spirit = `ypfundamentals:grantstrength`; Tonatiuh = `ypfundamentals:sol`; Pull = `ypfundamentals:pull_spell`. `StealSummonSpell` tem classfile mas **não** tem registro no initializer; excluído dos 15, assim como registros comentados no source pin.

## Separação dos 13 Principles

`Concentratio`, `Potentia`, `Vitale`, `Locus`, `Repetitio`, `Apparitio`, `Pertinacia`, `Expansio`, `Motus`, `Perceptio`, `Remedium`, `Augere`, `Certum` são categorias/progressão e não spell IDs. `SpellCategoriesGenerator`/ASM, `spell_categories.json`, `PrinciplesLevelsAttachment`, XP, exhaustion e passivas são do próprio provider, não recursos/magias adicionais de Black Arcana ou runtime do RPG Skill Tree.

## Gates não resolvidos

**⚠️** Source do provider 1.1.7.1 compila com Iron's 3.16.2, pack usa 3.16.3: compatibilidade runtime não validada. QA obrigatório de servidor/cliente, categorias ASM, persistência, concorrência de `LapsusSpell.location`, Laceration heal vs tooltip, Burning Spirit amplificador 0 no nível 1, Pyrokinesis filtro por classe, Saeptum domain/barriers, configs, XP/passivas/custos, receitas, multiplayer/Survival e world effects. Estas questões vêm de source pin; não de teste ao vivo.

**✅ Prova limitada a:** hash publisher=registro físico, existência de classes/IDs/schools, bootstrap e 15 registrations. `PHYSICAL_SPELL_REGISTRATIONS=15`, `NONREGISTERED_STEAL_SUMMON=EXCLUDED`, `NEW_SEMANTIC_ROOTS=0`, `EXACT_STATIC_REGISTRY_AUDIT=PASS`; **🟡 Stage 06.05 inalterado**.

**Clean-room e authority:** somente metadados e símbolos compilados inspecionados, sem copiar código/assets upstream. Iron's/Ypsilon mantêm casts, mana, settlement e Principles; Black Arcana seu runtime mágico; RPG Skill Tree apenas progressão/gates por contratos reais.