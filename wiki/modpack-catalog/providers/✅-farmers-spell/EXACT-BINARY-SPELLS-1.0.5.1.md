# Farmer's Spell 'n Spellbooks 1.0.5.1 — seis registros binários exatos

**✅ `COUNTED_EXACT` para 6/6 IDs e cardinalidade de registry estático. ⚠️ Sem prova de cast, configuração efetiva, cooking, Foodgeist, multiplayer ou Survival.**

## Identidade física verificada

- Modlist sibling `neoforge-rpg-skilltree/main@06ec1d1d586d4fc3cf957223cfc9ac30077f2875`, posição **#275**, `farmers-spell-n-spellbook-1.0.5.1-1.21.1.jar`, mod ID `farmers_spell`, SHA-1 `f77355e029af39bbaba3854e10cc087a608351ff`.
- Publisher [CurseForge project 1631240 / file 8760428](https://www.curseforge.com/minecraft/mc-mods/farmers-spell/files/8760428), release NeoForge 1.21.1 de **2026-08-29**, JAR **5537418 bytes**. Release posterior **1.0.6.0 não instalada**; não substitui a linha física 1.0.5.1.
- [Auditoria de JAR Java 21 #38334052069](https://github.com/Gustavaopere/Black-Arcana/actions/runs/38334052069) **SUCCESS**: download do CDN oficial, `sha1sum --check` correspondendo ao sibling, ZIP íntegro, introspecção `javap -p -c`. Branch read-only de auditoria `audit/farmers-spell-1051-physical-registry-20261012@0cdcd4c3047cb56ed2ed56500ce6c7b7a77f19e3` **não mergeada**.
- Fonte pública `GLDYM/Farmers-Spell-n-Spellbook@b7cbb40316a9ccbbc2ce2b56b3023647261ce569` mantém valor como baseline, mas a prova **não afirma build reproducível de source para JAR**.

## Prova direta de registry

O binário `com.chenjdy.farmers_spell.init.ModSpells` usa `SpellRegistry.SPELL_REGISTRY_KEY` e `DeferredRegister<AbstractSpell>`; seu inicializador possui **6 chamadas `DeferredRegister.register(String,Supplier)`** e **0 branch opcodes**. `com.chenjdy.farmers_spell.FarmersSpell` chama `ModSpells.register(IEventBus)` e o helper registra no mod event bus. Cada classe física estende `io.redspace.ironsspellbooks.api.spells.AbstractSpell`, implementa `getSpellResource()` e contém a literal correspondente ao ID.

| # | Registry ID | Classe binária | Campo estático `ModSpells` |
|---:|---|---|---|
| 1 | `farmers_spell:goodberry` | `GoodberrySpell` | `GOODBERRY_SPELL` |
| 2 | `farmers_spell:phantom_loot` | `PhantomLootSpell` | `PHANTOM_LOOT_SPELL` |
| 3 | `farmers_spell:seal_coat` | `SealCoatSpell` | `SEAL_COAT_SPELL` |
| 4 | `farmers_spell:bad_apple` | `BadAppleSpell` | `BAD_APPLE_SPELL` |
| 5 | `farmers_spell:chaos_slash` | `ChaosSlashSpell` | `CHAOS_SLASH_SPELL` |
| 6 | `farmers_spell:preserve_circle` | `PreserveCircleSpell` | `PRESERVE_CIRCLE_SPELL` |

Evidências do run: `STATIC_DEFERRED_REGISTER_INVOCATIONS=6`, `STATIC_INITIALIZER_BRANCHES=0`, `REGISTRAR_BUS_WIRING=True`, `REGISTRY_CREATE_SPELL_KEY=True`, `ENTRYPOINT_TO_REGISTRY=True`, `RESULT=EXACT_SIX_DIRECT_STATIC_SPELL_REGISTRATIONS`.

A enumeração de classes físicas no diretório `com/chenjdy/farmers_spell/spells/` identificou **exatamente as seis classes acima**. `BerserkCleaverSpell.java` está presente na árvore de source, mas não neste conjunto de classes físicas; também não é campo registrado, portanto **não é sétimo spell**. A escola `farmers_spell:gluttony`, Foodgeist, itens, status effects e receitas são superfícies de suporte, não outras spells semânticas.

## Boundary e pendências de implementação

- Iron's permanece authority de registry host, casting, mana/cooldown, escola/focus e Scroll Forge; Farmer's Spell permanece owner das seis spells Gluttony, efeitos, Foodgeist e magical cooking; Farmer's Delight permanece authority de base culinária. Black Arcana não duplica spell settlement, school stats, loot, culinária, cooking XP ou lifecycle.
- **⚠️ Não verificados neste artefato em execução:** boot da instância NeoForge e mixins combinados, configuração server real, parâmetros de dano/mana/cooldown, Spell Forge com Foodgeist Seasoning, player acquisition/Survival, server/client MP, spawn/reward Foodgeist e efeitos reais.
- **⚠️ Regressões de versão a testar em jogo:** sticky-piston block-form-food dupe corrigida em 1.0.5.1, Alchemist Pot duplicate XP/output corrigido em 1.0.5.0, food servings, autocrafting e state/load/reload. Este estudo estático **não** comprova eficácia dessas correções no modpack.
- A source baseline compila com NeoForge `21.1.238`; não equivale à versão da instância física. Não transportar signatures, efeitos ou mixins para Black Arcana sem contrato e teste.

**Contabilidade:** os 6 objetos já eram `COUNTED_SOURCE_PINNED`; agora `COUNTED_EXACT` **apenas no registry estático**, **+0 novos**, campanha congelada **✅ 10/39 exatos / ⚠️ 29/39 pendentes**, mínimos estritos **1851 global / 1849 escopo** preservados. Denominador total ainda não comprovado. Stage 06.05 segue 🟡.

**Clean-room:** nenhuma classe, corpo de implementação ou asset terceiro foi incorporado; apenas fatos de ID, hash, arquivo e estrutura de registro.
