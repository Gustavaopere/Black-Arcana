# IronSable 1.2.0 — sete spells exatos no JAR físico

**✅ Prova `COUNTED_EXACT` de identidade/registry estático:** **7/7 spells próprios**; são os mesmos sete já catalogados por release/log, logo **+0** identidades estritas. Campanha congelada: **16/39 exact / 23/39 pending**; mínimo semântico permanece **1857 global / 1855 escopo**. Config efetiva, hooks, casting ao vivo, física Sable e Survival **⚠️ não verificados**.

## Proveniência

- Fonte binária oficial: [CurseForge IronSable file 8598255](https://www.curseforge.com/minecraft/mc-mods/ironsable/files/8598255); `ironsable-1.2.0.jar`, NeoForge/Minecraft 1.21.1, tamanho **130973 bytes** e SHA-1 **`6ea9ce03144ec741a1e8d322f06985366d9ecc9e`**, rigorosamente idêntico à modlist física sibling `#344`, com mod ID `ironsable`.
- [Auditoria Java 21 #38408009738](https://github.com/Gustavaopere/Black-Arcana/actions/runs/38408009738) **SUCCESS** para identidade, bootstrap, campos tipados, ausência de branch no initializer, escola, 7 construtores e isolamento de overlays. [Inspeção física inicial #38407275804](https://github.com/Gustavaopere/Black-Arcana/actions/runs/38407275804) e [disassembly #38407407382](https://github.com/Gustavaopere/Black-Arcana/actions/runs/38407407382) também passaram.
- Cadeia física: `com.ironsable.Ironsable.<clinit> → SpellRegistry.SPELL_REGISTRY_KEY + DeferredRegister.create("ironsable") → DeferredRegister.register(suffix, Supplier)` sete vezes sem gates; `Ironsable(IEventBus) → SPELLS.register(IEventBus)`. Os sete campos `DeferredHolder<AbstractSpell, ConcreteSpell>` e cada classe/ID `getSpellResource()` foram confirmados. Não há 8ª identidade de spell próprio no registrador.

## Sete registries exatos

| # | ResourceLocation | Classe compilada no JAR | School source |
|---:|---|---|---|
| 1 | `ironsable:tempests_grasp` | `com.ironsable.spells.TempestsGraspSpell` | Wind* |
| 2 | `ironsable:maelstrom` | `com.ironsable.spells.MaelstromSpell` | Wind* |
| 3 | `ironsable:gyroscopic_spin` | `com.ironsable.spells.GyroscopicSpinSpell` | Lightning |
| 4 | `ironsable:downburst` | `com.ironsable.spells.DownburstSpell` | Wind* |
| 5 | `ironsable:stasis_lock` | `com.ironsable.spells.StasisLockSpell` | Ender |
| 6 | `ironsable:kinetic_barrier` | `com.ironsable.spells.KineticBarrierSpell` | Evocation |
| 7 | `ironsable:elastic_tether` | `com.ironsable.spells.ElasticTetherSpell` | Ender |

`Wind*`: `WindSchool.orEvocation()` verifica `ModList.isLoaded("wind_spellbooks")` e usa `wind_spellbooks:wind`, fazendo fallback para `SchoolRegistry.EVOCATION_RESOURCE` na ausência do addon. A modlist física inclui Wind's Spellbooks 1.0.5, então a condição de presença está **documentalmente satisfeita**; bootstrap conjunto não é prova de escola aplicada no cliente real. As quatro escolas antes marcadas como não verificadas são agora confirmadas na configuração default construída no bytecode: Gyroscopic Spin **Lightning**, Stasis Lock **Ender**, Kinetic Barrier **Evocation**, Elastic Tether **Ender**. A configuração implantada ainda requer QA.

## Sobreposição com dez spells Iron's — exclusão semântica

Os dez overlays de Sable ships permanecem próprios do IronSable *somente na física*, sem novos `ironsable:*` spell IDs: Telekinesis, Gust, Sonic Boom, Shockwave, Black Hole, Gravity Fissure, Stomp, Blizzard, Earthquake e Raise Hell. No JAR há classes `ShipTelekinesis`, `GustPhysicsHandler`, `SonicBoomPhysicsHandler`, `ShockwavePhysicsHandler`, `BlackHolePhysicsHandler`, `EarthquakePhysicsHandler`, `BlizzardPhysicsHandler`, `StompPhysicsHandler` e `RaiseHellPhysicsHandler`; o bootstrap emprega `CompatGuard.checkMixinTarget` e `registerIfPresent` para alvos opcionais. **A presença do handler não certifica que cada hook executou** no pack nem autoriza +10 identidades semânticas.

## Superfície Java pública factual, não bridge aprovada

No JAR existem `com.ironsable.core.PhysicsMagic` e métodos públicos **com assinaturas compiladas**, dentre os quais:

- `impulseOnBody(ServerLevel, ServerSubLevel, Vec3, Vec3): void`;
- `bodiesNear(ServerLevel, Vec3, double): List<ServerSubLevel>`;
- `bodyAtWorldPoint(ServerLevel, Vec3): ServerSubLevel`;
- `raycastBody(ServerLevel, Vec3, Vec3, double): PhysicsMagic.RayHit`;
- `bodyOf(Entity): ServerSubLevel`;
- `toLocalPoint(ServerSubLevel, Vec3): Vec3`, `toWorldPoint(ServerSubLevel, Vec3): Vec3`;
- `massOf(ServerSubLevel): double`;
- `dampBody(ServerLevel, ServerSubLevel, double, double): void`.

A listagem pública foi registrada pelo runner a partir de `javap -p`, não por guesswork. **Não existe contrato Black Arcana/provider implementado, aprovado ou testado** por essa evidência. Precisam ser verificadas semânticas de propriedade, side/thread, ticks, unidades SI, handle inválido, duplicidade e runtime de Sable. O helper binário tem guard para `RigidBodyHandle` ausente e registra aviso; Black Arcana não deve ignorar esse estado.

## Limites estritos e clean-room

- **✅ Verificado:** artefato, SHA, sete identidades e bootstrap, escola padrão nos bytecodes, gates/overlays estruturais.
- **⚠️ Não verificado:** mana/cooldown efetivos, config aplicada, Scroll Forge/loot real, casting de servidor, navios/sublevels, compat Iron's 3.16.3 e Sable 2.0.5, lifetime multi-caster/chunk/dimension, friendly-fire, deduplicação de força, Create Aeronautics e testes Survival.
- O Iron's controla spell registry/casts/mana/cooldown; Sable controla physics ship body; IronSable gerencia integração spell→physics, e Black Arcana **não** reexecuta a física ou debita mana novamente. RPG Skill Tree permanece sibling de progressão/gates por contrato. Stage 06.05 🟡 sem alteração.
- Pesquisa factual clean-room de nomes, assinaturas, ids, gates e paths, sem copiar código, bytecode ou assets proprietários.
