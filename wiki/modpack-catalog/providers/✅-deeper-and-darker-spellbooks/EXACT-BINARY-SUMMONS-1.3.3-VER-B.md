# Deeper and Darker: Spellbooks 1.3.3 Version B — four exact binary summon registrations

**✅ 4/4 `COUNTED_EXACT` somente para identidade de registro binário estático. ⚠️ Não há teste de cast/Survival ou eficácia do hotfix em servidor.**

## Identidade física e publicador

- Snapshot físico: `neoforge-rpg-skilltree/main@06ec1d1d586d4fc3cf957223cfc9ac30077f2875`, JAR #214 `darkermagic-1.3.3-1.21.1-ver.b.jar`, mod ID `darkermagic`, SHA-1 `783123ae86c91c01527c10f338679caaef42eb42`.
- Publisher [CurseForge file 7897469](https://www.curseforge.com/minecraft/mc-mods/deeper-and-darker-spellbooks/files/7897469) (2026-04-09), Version B, **100219 bytes**. [Auditoria Java 21 #38329132941](https://github.com/Gustavaopere/Black-Arcana/actions/runs/38329132941) obteve o artefato oficial, `sha1sum --check` confirmou o SHA físico e `zipfile.testzip` passou.
- `META-INF/neoforge.mods.toml` inspecionado: `modId="darkermagic"`, `version="1.3.3-1.21.1"`; também registra `irons_spellbooks` e `deeperdarker` como dependências, sem provar a compatibilidade runtime.
- O source público `RevTheSprout/Deeper-and-Darker-Spellbooks@df242888d16e580a8f76e0d937fe50d66bbed8ed` declara **1.3.0**; não é equivalência do hotfix 1.3.3. O registrador foi movido: **source 1.3.0** `net.rev.darkermagic.item.DDISSSpellRegistery` → **JAR 1.3.3** `net.rev.darkermagic.registeries.DDISSSpellRegistery`. A primeira auditoria [#38329040366](https://github.com/Gustavaopere/Black-Arcana/actions/runs/38329040366) falhou por pressupor o pacote antigo; a prova final enumerou as classes do JAR.

## Quatro registros exatos

O bytecode do registrador usa `SpellRegistry.SPELL_REGISTRY_KEY` e `DeferredRegister<AbstractSpell>`, efetua quatro `registerSpell(AbstractSpell)` estáticos que levam `getSpellName()` a `DeferredRegister.register(String,Supplier)`. O entrypoint `DarkerMagic` registra o grupo no mod event bus.

| # | Classe física | Campo do registrador | Registry ID |
|---:|---|---|---|
| 1 | `SummonWardenSpell` | `SUMMON_WARDEN_SPELL` | `darkermagic:summoned_warden` |
| 2 | `SummonShatteredSpell` | `SUMMON_SHATTERED_SPELL` | `darkermagic:summoned_shattered` |
| 3 | `SummonSculkCentipedeSpell` | `SUMMON_SCULK_CENTIPEDE_SPELL` | `darkermagic:summoned_sculk_centipede` |
| 4 | `SummonSculkSnapperSpell` | `SUMMON_SCULK_SNAPPER_SPELL` | `darkermagic:summoned_sculk_snapper` |

Provas do log: `OWNED_SPELL_CLASS_COUNT=4`, `STATIC_REGISTER_SPELL_INVOCATIONS=4`, `DEFERRED_REGISTER_HELPER_CALLS=1`, `REGISTRY_BUS_WIRING=True`, `ENTRYPOINT_TO_REGISTRY=True`, `RESULT=FOUR_EXACT_BINARY_STATIC_SUMMON_SPELL_REGISTRATIONS`. Cada classe estende `io.redspace.ironsspellbooks.api.spells.AbstractSpell`, implementa `getSpellResource()` e possui literal da sua chave e namespace `darkermagic`.

## Limites

A **Version B** anuncia Warden Mage Armor com bônus de 10% Eldritch Spell Power em vez dos 5% da A; o changelog 1.3.3 diz corrigir crash de summons em servidor. A auditoria **não executou as magias** e não testou implementação do bônus ou eficácia do hotfix. Quantidades invocadas, mana, cooldown, nível, raridade, recast, summon lifetime, IA, `SpellSummonEvent`, `SummonManager`, proprietário/friendly-fire, aquisição, configurações, reload, client/server e Survival continuam **⚠️**. Valores anteriores das fichas provêm do source 1.3.0 e não são garantias do runtime 1.3.3.

Iron's controla cast/custos/cooldown, Deeper and Darker controla os mobs originais, este addon controla as definições das quatro invocações. Black Arcana não duplica summon manager, efeitos, ownership ou pagamento; RPG Skill Tree é somente provider de progressão via contratos reais.

**Contabilidade:** quatro IDs já contados avançam de `COUNTED_RELEASE_BOUNDED` a `COUNTED_EXACT` *somente para registro estático*, **8/39 exatos / 31/39 pendentes**, **+0** magias novas; mínimos **1851 global / 1849 escopo** preservados, denominador semântico completo desconhecido. **Stage 06.05 🟡**; não é aprovação de release nem de Survival.

**Clean-room:** apenas inspeção de metadados/registries; nenhum código ou asset do provider incorporado.
