# Black Arcana — baseline de cobertura por habilidade e por provider (2026-10-15)

**Natureza:** snapshot de coordenação de catálogo e dos eixos de engenharia de perks, sem alterar os contadores canônicos. A fonte operacional dinâmica continua em `SEMANTIC-MAGIC-COVERAGE.md`, `CATALOG-COVERAGE-CURRENT.md` e `plans/STATUS.md`; atualizar esta ficha após reconciliação, sem assumir que é o último checkpoint.

## Fila de QA física — observador passivo de Arrow Volley (2026-10-15)

**Sem aumentar a cobertura semântica:** a fila de 110 identidades Iron's permanece **26/110 dossiês individuais de causalidade aprofundada (23,64%)**. Mínimo canônico **1.856 mágicos globais / 1.854 em escopo**, denominador definitivo **desconhecido (—%)**. Esta tranche adiciona infraestrutura de **observação**, não a 27ª magia nem um adapter runtime.

- [Protocolo NeoForge 21.1.248 + Iron's 3.16.3](../../../docs/qa/irons-3163-arrow-volley-runtime-acceptance.md): executar em cópia do *modpack físico*, com fingerprint do Iron's instalado, Java 21, buffs/perks documentados e logs.
- [Observador opt-in](../../../src/catalogQaProbe/java/dev/gustavopere/blackarcana/qa/catalog/ArrowVolleyRuntimeEvidence.java): exclusivo ao JAR `black_arcana_catalog_qa`, default **desabilitado** e ligado por `-Dblack_arcana.catalog_qa.arrow_volley=true`; acompanha `irons_spellbooks:arrow_volley` e `small_magic_arrow` por eventos públicos NeoForge, sem modificar entidades. Até **4 controladores ativos**, **16 sessões por processo**, **100 ticks por sessão** e **256 projéteis candidatos por sessão**; sem scans globais nem ticket de chunk.
- [Parser fail-closed](../../../docs/qa/irons_3163_arrow_volley_observation_check.py) e [testes exclusivamente sintéticos](../../../docs/qa/irons_3163_arrow_volley_observation_check_test.py): classificam ticks, fileiras, `EntityJoinLevelEvent` e presença em mundo no post-tick, ambiguidades de owner/proximidade, caps e descarte. **`TRACE_CONSISTENT_NOT_GAMETEST` não significa runtime homologado.**
- O workflow [`irons-3163-projectile-bytecode.yml`](../../../.github/workflows/irons-3163-projectile-bytecode.yml) contém tarefa de compilar `catalogQaProbeJar` e verificar que a classe de QA **não entra** no JAR canônico Black Arcana. **Estado CI deve ser consultado na revisão final**, e builds no CI não demonstram que a fixture rodou no modpack.

**Gates:** ✅ fontes/eventos modelados para instrumento não intrusivo; 🟡 pipeline de QA em revisão de CI; ⚠️ logs em mundo real, compatibilidade do pack, spawn aceito, desempenho, descarregamento/recarregamento e validação de causalidade faltam; ⛔ perks de +flechas continuam bloqueados sem hook provider-native e budgets. Stage 06.05 🟡, PR #825 *draft*, sem merge ou promoção.

## Retificação binária do contador vanilla 1.21.1 — avaliação do Arrow Volley (2026-10-15)

**[Actions #38814378449](https://github.com/Gustavaopere/Black-Arcana/actions/runs/38814378449) SUCCESS:** novo coletor [`minecraft_1211_entity_tick_proof.py`](../../../docs/qa/minecraft_1211_entity_tick_proof.py) validou o manifesto oficial Mojang e **inspecionou o classfile do servidor vanilla 1.21.1**, pacote SHA-1 `59353fb40c36d304f2035d51e7d6e6baa98dc05c`, classe mapeada `ServerLevel.tickNonPassenger(Entity)`. A prova resultante mostra escrita em `Entity.tickCount` **antes de invocar `Entity.tick()`**. O achado anterior “`ArrowVolleyEntity.tick()` não chama `super.tick()`” continua verdadeiro para o JAR Iron's, **mas não demonstra contador estagnado** no ciclo vanilla. A hipótese de spawn ilimitado **por essa única causa** foi **retificada**. O checksum do inner server JAR é `c301de10f575027d13eac18c7f34409d60648cf56a35d566aa1f530ff617840a`.

**[Modelo determinístico](../../../docs/qa/irons_3163_arrow_volley_tick_model_test.py), sem GameTest:** com incremento prévio ao método, `rows=4+level`, `perRow=5+floor(level/2)`, `delay=5` e `discard` no primeiro tick não múltiplo após `rows×5`, a previsão para níveis 1–6 é **25/36/42/56/63/80 projéteis** e remoção do controlador nos ticks **26/31/36/41/46/51**, respectivamente. Esses são números de **modelo de fluxo**, não cardinalidades medidas de spawns aceitos no pack. A prova está documentada em [recibo atualizado](../../../docs/qa/irons-3163-projectile-bytecode-pending.md) e [ficha Arrow Volley](../providers/✅-irons-spells/audits/CAUSAL-PERKS-ARROW-VOLLEY-3.16.3.md).

**Bloqueio remanescente:** ⚠️ não há prova executável do `ServerLevel` transformado NeoForge **21.1.248**, GameTest de 100 ticks, chunks/reload ou SHA do JAR instalado; ⛔ alteração por perk de count/velocidade/hitbox ainda requer seam público, limites e QA. **Não promover Stage 06.05 ou declarar exploit/bug físico.** Os números globais/por provider continuam **26/110 dossiês causais individuais (23,64%)**, **1.856 globais / 1.854 estritos**, total global desconhecido (—%). Nenhum novo spell foi catalogado.

## Verified published Java 21 bytecode — four compiled class paths (2026-10-15, PR #825 draft)

**Prova binária localizada (não aumenta o numerador de magias):** [GitHub Actions #38811661659](https://github.com/Gustavaopere/Black-Arcana/actions/runs/38811661659) **SUCCESS** para workflow [`irons-3163-projectile-bytecode.yml`](../../../.github/workflows/irons-3163-projectile-bytecode.yml), coletor [`irons_3163_projectile_bytecode.py`](../../../docs/qa/irons_3163_projectile_bytecode.py) e [relatório de QA e limites](../../../docs/qa/irons-3163-projectile-bytecode-pending.md). Download do JAR publicado do Iron's 3.16.3, CurseForge **file 8680204**, **13.890.046 bytes**, SHA-256 **`13d644474ddba4f8478b4ce68294687fd509c994b3f344a224142b102dbe6f73`**, Java 21.0.12.1. A evidência exportada é JSON, não o JAR proprietário.

- ✅ `ArrowVolleyEntity.tick`: lê `tickCount`, **não chama `super.tick` nem escreve o campo diretamente**. O ciclo do servidor vanilla Mojang 1.21.1 foi provado posteriormente como incrementando `tickCount` antes de `Entity.tick` (veja retificação acima); ⚠️ cardinalidade em NeoForge/GameTest ainda não medida; ⛔ perk +count permanece bloqueado por hook/QA.
- ✅ `SmallMagicArrow.shoot`: escreve `deltaMovement` diretamente, sem consulta a `getSpeed`; `onHitEntity` referencia `ARROW_VOLLEY_SPELL` no bytecode.
- ✅ `SummonedSkeleton`: herda `Skeleton` e não declara `performRangedAttack`; ⚠️ fonte real da flecha herdada permanece **indeterminada** sem bytecode Minecraft/NeoForge e eventos em execução.
- ✅ `PoisonCloud.applyEffect`: chama `hurt` sem `DamageSources.applyDamage`; `SpellDamageEvent` do helper do Iron's não é disparado por **esse método**, mas eventos gerais do jogo permanecem possíveis.

**Caveats:** o checksum é do arquivo do publisher baixado na Actions, **não foi confrontado com JAR instalado**. Nenhum GameTest, Minecraft runtime, servidor dedicado, cliente, PvP, reload, profilers ou teste de gameplay foi executado. O job verde é **prova de auditoria binária estática somente**; as outras 22+ fichas permanecem conforme a provenance já documentada. **Cobertura do Iron's segue 26/110 (23,64% desta fila documental), piso global 1.856 / 1.854, denominador desconhecido (—%).** Stage 06.05 🟡 e sem promoção. PR continua draft.

## Current tranche override — twenty-six causal dossiers (2026-10-15, PR #825 draft)

**Iron's 3.16.3 — 26/110 magias têm dossiês individuais causais suplementares source-pinned nesta PR (23,64% da fila documental específica).** As **110 identidades** já estão identificadas; dossiê causal **não significa** adapter, cobertura de API, equivalência JAR, GameTest ou QA de pack. A PR #795 das 110 fichas individuais está separada e seus arquivos não devem ser sobrescritos. **Nenhuma nova identidade semântica:** piso do ledger canônico preservado em **1.856 objetos mágicos mínimos globais / 1.854 no escopo estrito**, denominador global **desconhecido (—%)**. O checkpoint histórico 23/110 permanece abaixo.

**Três novas fichas individuais desta tranche:**

- [Arrow Volley 3.16.3](../providers/✅-irons-spells/audits/CAUSAL-PERKS-ARROW-VOLLEY-3.16.3.md) — fórmula matemática nominal `rows=(4+level)`, `arrowsPerRow=(5+floor(level/2))`: 25/36/42/56/63/80 flechas nos níveis 1–6, condicionadas ao scheduler real do controlador. **Nota histórica retificada acima:** ausência de `super.tick` não prova ausência de incremento, pois `ServerLevel.tickNonPassenger` vanilla 1.21.1 atualiza `tickCount` previamente; cardinalidade NeoForge/pack, TTL e budget real ainda requerem GameTest; não homologar perks antes de API e QA. `SmallMagicArrow.shoot` usa vetor diretamente, velocidade ≈0,85 inicial, e hit aponta para `ARROW_VOLLEY_SPELL`.
- [Magic Arrow 3.16.3](../providers/✅-irons-spells/audits/CAUSAL-PERKS-MAGIC-ARROW-3.16.3.md) — **um** projétil, piercing infinito, `shouldPierceShields=true`, `collidesWithBlocks=false`, velocidade base 2,7; lista `victims` de UUID permite **uma tentativa de dano** por entidade enquanto a instância vive, inclusive quando tentativa original é vetada; sua persistência em reload não é demonstrada. `SpellDamageSource` usa `MAGIC_ARROW_SPELL`.
- [Poison Arrow 3.16.3](../providers/✅-irons-spells/audits/CAUSAL-PERKS-POISON-ARROW-3.16.3.md) — dano direto do projétil com `POISON_ARROW_SPELL` via `DamageSources.applyDamage`, seguido por `PoisonCloud` de 200 ticks nominais, `reapplicationDelay=10`, efeito Poison 120 ticks por aplicação. **Divergência causal:** `PoisonCloud.applyEffect` chama `target.hurt` com `DamageSource` genérico `ISSDamageTypes.POISON_CLOUD`, não publica `SpellDamageEvent` via esse método. Não converter N reaplicações em N casts ou prescrever hook universal de MagicDamage inexistente.

**Nova auditoria transversal (não conta como 27ª magia):** [Raise Dead — Skeleton ranged attribution](../providers/✅-irons-spells/audits/CAUSAL-PERKS-RAISE-DEAD-RANGED-ATTRIBUTION-3.16.3.md). `SummonedSkeleton extends Skeleton` e não sobrescreve o pipeline `performRangedAttack` no código do provider; o **melee** explicitamente usa `RAISE_DEAD_SPELL.getDamageSource`, mas a fonte da **flecha herdada** precisa de inspeção física da implementação vanilla/NeoForge. `DamageSources.preHitEffects` reconhece `IMagicSummon` como entidade direta ou causadora e pode aplicar `SUMMON_DAMAGE` do owner, porém sem prova de que a flecha herdada referencie o skeleton em `DamageSource.getEntity()` isso permanece ⚠️ condicionado. **Não creditar Mastery por arrow hit como novo cast nem atribuir spell ID falsamente.**

**Estados e autoridade:** ✅ source pin `iron431/irons-spells-n-spellbooks@e4056af90302d37eb1739f5ff05020b020e6e252`, contratos documentados e limites declarados; ⚠️ binário/JAR, config, tick lifecycle, reload, ownership de vanilla projectile, eventos de terceiros, provas in-game e dedicated server **não executados**; ⛔ perks de count infinito, atribuição automática de dano herdado, duplicate on-hit e mutação de runtime alheio bloqueados sem contratos e QA. Iron's governa suas magias; Black Arcana apenas seu runtime, RPG Skill Tree progressão/atributos/Mastery/perks/gates. Stage 06.05 continua 🟡, PR #825 draft não mesclada.

## Current tranche override — twenty-three causal dossiers (2026-10-15, PR #825 draft)

**Iron's Spells 'n Spellbooks 3.16.3 — 23/110 magias com dossiês individuais causais suplementares source-pinned nesta PR (20,91% desta fila documental).** As 110 magias já têm identidade inventariada; os dossiês suplementares não significam 23 adapters seguros/implementados nem 23 GameTests ou validação do JAR. A PR #795 das 110 fichas individuais permanece separada. **+0 magia nova:** ledger mínimo global fica **1.856 objetos semânticos / 1.854 no escopo estrito**; denominador global definitivo **desconhecido (—%)**. O checkpoint anterior **21/110** segue abaixo apenas como histórico.

**Novas fichas individuais desta tranche:**

- [Summon Polar Bear 3.16.3](../providers/✅-irons-spells/audits/CAUSAL-PERKS-SUMMON-POLAR-BEAR-3.16.3.md) — **uma** entidade `SummonedPolarBear`, HP base `(20+4×level)×entityPowerMultiplier`, ataque base `getSpellPower`, fonte melee `SUMMON_POLAR_BEAR_SPELL`, mount para caster, regeneração de 1 HP/80 ticks, 1 recast adicional para unsummon, lifetime nominal 12000 ticks.
- [Summon Horse 3.16.3](../providers/✅-irons-spells/audits/CAUSAL-PERKS-SUMMON-HORSE-3.16.3.md) — **uma** montaria `SummonedHorse`; velocidade, salto, HP e distância segura de queda derivados de `getSpellPower/100`; `setOwnerUUID` local + `SummonManager`, rider e NBT condicionado. `Vec3.add` sem reatribuição em `SummonHorseSpell.onCast` levanta **hipótese de spawn no próprio ponto do caster**, sem bug físico reproduzido. Não foi certificado ataque mágico exclusivo da montaria.

**Novo documento transversal, não contável como spell:** [Minion damage & death/unsummon lifecycle](../providers/✅-irons-spells/audits/CAUSAL-PERKS-SUMMON-MINION-DAMAGE-LIFECYCLE-3.16.3.md). Verificou `doHurtTarget` melee com damage source de `raise_dead` em `SummonedZombie` e `SummonedSkeleton`, `summon_vex` em `SummonedVex`, `summon_swords` em `SummonedWeaponEntity`, e `summon_polar_bear` em `SummonedPolarBear`. **Não** inferir que flechas do Skeleton preservem o mesmo source sem rastrear a herança vanilla. `onUnSummon` faz `setRemoved(DISCARDED)` nos caminhos observados, **diferente de `die(DamageSource)`**; Mastery por morte precisa distinguir morte real, despawn, recast, antimagia, timeout e relog. Corrigida também a atribuição de melee na [ficha anterior Raise Dead](../providers/✅-irons-spells/audits/CAUSAL-PERKS-RAISE-DEAD-3.16.3.md) sem alterar sua identidade.

**Limites de autoridade e QA:** ✅ arquivos fonte com commit imutável `iron431/irons-spells-n-spellbooks@e4056af90302d37eb1739f5ff05020b020e6e252` e verificações documentais; ⚠️ JAR físico, tags/config, mounted state, herança de ranged attacks, event order e restauração de UUID após rejoin não testados; ⛔ nenhum adapter de novos summons, kill rewards, HP/velocidade, DamageType, on-removed events ou Mastery sem seam real e validação de deduplicação. Black Arcana preserva seu runtime, RPG Skill Tree apenas progressão/perks/gates e Iron's controla entidades invocadas. Stage 06.05 continua 🟡 e PR #825 permanece em draft.

## Current tranche override — twenty-one causal dossiers (2026-10-15, PR #825 draft)

**Iron's Spells 'n Spellbooks 3.16.3: 21/110 magias com fichas de auditoria causal suplementar source-pinned nesta PR (19,09% da fila documental específica).** Os **110 spell IDs** já estão identificados no catálogo, com fichas individuais em trabalho separado na PR #795. As 21 fichas representam **análise causal e desenho de critérios QA**, **não** 21 adapters implementados, 21 certificados binários, 21 GameTests ou conclusão da integração de perks. O mínimo canônico de magia **não mudou: 1.856 objetos semânticos mínimos globais / 1.854 no escopo restrito**; denominador total do catálogo global permanece **desconhecido (—%)**. O checkpoint histórico de 18/110 segue abaixo.

**Novos dossiês individuais, sem editar fichas da PR #795:**

- [Summon Swords 3.16.3](../providers/✅-irons-spells/audits/CAUSAL-PERKS-SUMMON-SWORDS-3.16.3.md) — três entidades distintas fixas (claymore, rapier, sword); HP/dano escalados por `getSpellPower`, `SpellSummonEvent` por criatura, `RecastInstance(total=2)` com segunda ativação para unsummon, lifetime nominal `12000 ticks`, owner events e persistência condicionada.
- [Summon Vex 3.16.3](../providers/✅-irons-spells/audits/CAUSAL-PERKS-SUMMON-VEX-3.16.3.md) — `level+2` vexes (3–7), `finalizeSpawn` e ownership pelo manager, melee com `SUMMON_VEX_SPELL` como fonte; apenas o primeiro onCast da sessão cria vexes.
- [Raise Dead 3.16.3](../providers/✅-irons-spells/audits/CAUSAL-PERKS-RAISE-DEAD-3.16.3.md) — `level+2` undead (3–8), skeleton aleatório `p=0.3` por invocação, qualidade de equipamento por power/rolagem, formação em anel + colisão, XP base `0`, AI/atribuição de damage source ainda parcial.

**Auditoria transversal nova que não entra nas 21 magias:** [summon lifecycle / ownership / eventos 3.16.3](../providers/✅-irons-spells/audits/CAUSAL-PERKS-SUMMON-LIFECYCLE-EVENTS-3.16.3.md). A `SpellSummonEvent` é source-pinned e permite `setCreature(K)`, mas não implementa cancelamento na classe inspecionada; `SetSummonOwnerEvent` é não cancelável e é possivelmente postado duas vezes por criatura devido a owner já configurado nos construtores e reconfigurado no `SummonManager.initSummon`. **É hipótese de duas notificações, não de dois spawns.** O manager governa duração, ownership, expiração de 20 ticks, serialização no logout/shutdown e restauração no login; a compatibilidade física do conjunto recast+owner+UUID ainda não foi testada. Os três spells usam recast como encerramento, em contraste com barragem ofensiva que usa recasts para disparos adicionais.

**Limites:** ✅ 21 dossiês individuais + 1 contrato transversal de summons com proveniência fixa `iron431/irons-spells-n-spellbooks@e4056af90302d37eb1739f5ff05020b020e6e252`; ⚠️ artefato/JAR/config físico, callbacks live, persistência/dimensões, budgets, GameTests e dedicated server não testados; ⛔ não atribuir Mastery por owner event ou por spawn candidato, não mutar `SummonManager`, count, IA, persistência ou cooldown sem API segura e testes. Black Arcana continua autoridade de seu runtime; RPG Skill Tree apenas progression/perks/gates, e Iron's gerencia os próprios summons. Stage 06.05 permanece 🟡, Stage09 pendente; PR em draft.

## Current tranche override — eighteen causal dossiers (2026-10-15, PR #825 draft)

**Iron's 3.16.3 — 18/110 magias com ficha causal source-pinned complementar nesta PR (16,36% da fila de 110).** Essa é métrica **documental específica**, não contagem de magias novas nem proporção de hooks, perks, adapter, JAR físico ou GameTests aceitos. A PR #795 mantém trabalho paralelo das 110 fichas individuais; não há alteração nelas neste lote. O piso canônico permanece **1.856 objetos semânticos mágicos globais / 1.854 no escopo restrito**, com **denominador global desconhecido (—%)**. O checkpoint anterior 15/110 aparece abaixo apenas como histórico.

Novas fichas desta tranche, todas clean-room e com provenance fixa `iron431/irons-spells-n-spellbooks@e4056af90302d37eb1739f5ff05020b020e6e252`:

- [Acupuncture](../providers/✅-irons-spells/audits/CAUSAL-PERKS-ACUPUNCTURE-3.16.3.md): alvo a 32 blocos; `(int)((4+level)*power)` agulhas (5–14 em power neutro), dano `1+power` por agulha, `shoot` nominal 0,875 bloco/tick. **`BloodNeedle.onHitEntity` atribui hits a `BLOOD_NEEDLES_SPELL`**, não ao cast Acupuncture. Constructor split/gravity e escala física condicionados.
- [Blood Needles](../providers/✅-irons-spells/audits/CAUSAL-PERKS-BLOOD-NEEDLES-3.16.3.md): cinco projéteis **fixos**, damage `power×0,25` por agulha, vetor shoot nominal 2,5 blocos/tick, `SpellDamageSource` com 25% lifesteal e zero i-frames; classe de projétil compartilhada com Acupuncture.
- [Flaming Barrage](../providers/✅-irons-spells/audits/CAUSAL-PERKS-FLAMING-BARRAGE-3.16.3.md): `RecastInstance(total=5, remaining=4, ttl=120)`, uma pequena fireball por `onCast`, cursor-homing com limite de consulta 48 blocos e disparo inicial nominal 0,925 bloco/tick. **`SmallMagicFireball.onHitEntity` usa `BLAZE_STORM_SPELL` como damage-source** inclusive em disparos de Flaming Barrage. Possível ignição de blocos sob `ServerConfigs.SPELL_GREIFING` depende de config/claims físicos.

**Atenção:** duas discrepâncias de `cast spell ID` vs `damage source spell ID` significam que filtragem de perks por `SpellDamageSource.spell()` **não reconstrói sozinha** a identidade da ação original para essas magias. Sem hook de provenance/correlação confiável, o adapter deve **falhar fechado**, não reatribuir dano silenciosamente. `SpellOnCastEvent` pode ocorrer em recasts sucessivos, ao passo que cobrança de mana e cooldown seguem política provider-native. Números de entidade/velocidade são defaults source-pinned, não resultados de gameplay.

**Estado:** ✅ 18 fichas causais suplementares registradas na branch; ⚠️ binário/modlist física, impact damage actual, config, addons, multiplayer e JAR/CI QA não testados; ⛔ sem autorização para modificar entidades de terceiro, hitbox, quantidade, homing ou tipo de dano sem contrato seguro. Stage 06.05 segue 🟡 e Stage 09 pendente.

## Current tranche override — fifteen causal dossiers (2026-10-15, PR #825 draft)

**Iron's Spells 'n Spellbooks 3.16.3 — 15/110 spells têm fichas suplementares de leitura causal source-pinned nesta PR (13,64% das identidades).** É métrica **estritamente documental de auditoria**, não porcentagem de APIs seguras, adapters implementados, física do JAR ou QA. As 110 fichas individuais da PR #795 continuam em draft e em trabalho separado. O mínimo do ledger global **permanece 1.856 objetos semânticos / 1.854 no escopo restrito**, pois nenhuma destas magias é identidade nova; **denominador global final desconhecido (—%)**. O checkpoint 12/110 abaixo fica como histórico.

Novos dossiês, sem sobrescrever as fichas existentes:

- [Gluttony — mana em `LivingEntityUseItemEvent.Finish`](../providers/✅-irons-spells/audits/CAUSAL-PERKS-GLUTTONY-3.16.3.md): alimento `FoodProperties` com status GLUTTONY, `nutrition × ratioForAmplifier`, server `MagicData.addMana`, cap superior `MAX_MANA`, `ChangeManaEvent` e sync; sem segundo crédito/cast.
- [Devour — mandíbula e Vigor por kill](../providers/✅-irons-spells/audits/CAUSAL-PERKS-DEVOUR-3.16.3.md): target single raycast 9 blocos, `DevourJaw` em 13 ticks, lifesteal de 15% do dano `LivingDamageEvent.Post`, heal no kill e vida máxima temporária via `VIGOR` com amplifier cap 9; não confundir retorno do hit com kill.
- [Ray of Siphoning — canalização e roubo de vida](../providers/✅-irons-spells/audits/CAUSAL-PERKS-RAY-OF-SIPHONING-3.16.3.md): scheduler de player `CONTINUOUS_CAST_TICK_INTERVAL=10`, custo por chamada nativa e reserva de 2× mana cost para continuação, raycast 12 blocos independente do nível, `SpellDamageSource.setLifestealPercent(1f).indirect()`; hits/heals recorrentes pertencem a um canal e não são casts independentes.

**Barreiras:** ✅ documentação com provenance fixa; ⚠️ sem verificação do artefato físico, `CastSource` efetivo, eventos de terceiros, stacking, save/reload ou QA multiplayer; ⛔ mudanças per-perk de `DevourJaw`, geometria, cadência de canalização, tipo de dano e recursos de outro provider permanecem bloqueadas sem hook público estável e testes. Black Arcana governa apenas seu runtime, RPG Skill Tree progressão/gates/perks, Iron's rege as próprias magias.

## Current tranche override — twelve causal dossiers (2026-10-15, PR #825 draft)

**Iron's Spells 'n Spellbooks 3.16.3: 12/110 spells com dossiê causal suplementar nesta PR** — **10,91% da fila de 110**; isso representa escopo de *auditoria documental source-pinned*, **não** completion de hooks per-perk, adapter implementado, verificação binária, GameTest ou execução real. A PR #795 continua distinta com as 110 fichas de origem em draft. O checkpoint de 9/110 abaixo permanece histórico. Nenhum novo ID mágico foi acrescentado: **1.856 objetos semânticos mínimos globais / 1.854 no escopo restrito**; denominador final do universo global continua **aberto (—%)**.

Novas fichas desta tranche, como complementos individuais sem sobrescrever arquivos da PR #795:

- [Frostbite — eventos de morte e fan-out](../providers/✅-irons-spells/audits/CAUSAL-PERKS-FROSTBITE-3.16.3.md): buff no atacante, exigência `isFullyFrozen` na vítima, criação de `FrozenHumanoid`, atraso de 100 ticks, impacto AOE e oito shards com `ICICLE_SPELL` como damage source; owner/shatter/persistência separados.
- [Echoing Strikes — event Post e anti-recursão](../providers/✅-irons-spells/audits/CAUSAL-PERKS-ECHOING-STRIKES-3.16.3.md): `LivingDamageEvent.Post`, seletor dano melee/arrow, exclusão de `SpellDamageSource`, `hitCount=level+2`, attachment codificado, espada AOE de raio 2 e flecha após delay 15 ticks.
- [Sacrifice — cast direto vs morte marcada](../providers/✅-irons-spells/audits/CAUSAL-PERKS-SACRIFICE-3.16.3.md): dois ingressos e fórmulas diferentes, `IMagicSummon` própria/mark de DeadKing, `AABB.ofSize(radius,radius,radius)` com **raio nominal e cubo de candidatos distintos**, queda de dano e potencial propagação de mortes marcadas.

**Avaliação de interoperabilidade:** ✅ observação de fonte fixa e mapeamento causal por spell; ⚠️ JAR/mundo efetivo, morte cancelada, callbacks de terceiros, i-frames, identidade de dano derivado, persistência e limites de proc não foram testados; ⛔ sem hook público seguro, manter bloqueadas alterações per-perk de spawn/shape/quantidade de projéteis/cadeias de morte. O RPG Skill Tree permanece provider de progressão/perks, sem assumir o runtime do Iron's ou do Black Arcana.

## Current tranche override — nine causal dossiers (2026-10-15, PR #825 draft)

A PR #825 passou de seis para **9/110 magias do Iron's com dossiê suplementar de auditoria causal source-pinned** (**8,18% desta categoria documental**). O novo grupo cobre **Root, Slow e Abyssal Shroud**. O checkpoint de seis arquivos abaixo é histórico, não substitui este estado mais recente. O universo semântico **não** aumentou: **1.856 objetos mágicos mínimos globais / 1.854 no escopo estrito** permanecem os mesmos do ledger canônico. Denominador global final **desconhecido (—%)**. Não confundir 9/110 fichas suplementares com implementação de perks, prova binária ou homologação da API. A PR #795 continua aberta com as 110 fichas individuais em outra branch.

- [Root 3.16.3](../providers/✅-irons-spells/audits/CAUSAL-PERKS-ROOT-3.16.3.md): alvo único 32 blocos, `CANT_ROOT` verificado na execução final, root invocada e montada como veículo, HP independente do nível, duração por power, dismount guard, antimagia e NBT.
- [Slow 3.16.3](../providers/✅-irons-spells/audits/CAUSAL-PERKS-SLOW-3.16.3.md): aquisição 32 blocos, duração por power, amplificador por entity power multiplier, quatro modificadores de atributo com impacto diferenciado para mineração e casting, sem dano direto.
- [Abyssal Shroud 3.16.3](../providers/✅-irons-spells/audits/CAUSAL-PERKS-ABYSSAL-SHROUD-3.16.3.md): defesa própria por `LivingIncomingDamageEvent` e `ProjectileImpactEvent`, bypass tags, precedência `EVASION`, tentativa de deslocamento que nem sempre se concretiza e ausência de `SpellTeleportEvent` nesse caminho direto.

**Riscos confirmados na leitura source-pinned, sem declarar bug de JAR/gameplay:** `RootSpell` pode cobrar o cast antes da verificação final `CANT_ROOT`, `RootEntity` não serializa `target` explicitamente na própria classe; `AbyssalShroudEffect.doEffect` retorna true após tentativas condicionais de movimento, permitindo veto de dano mesmo sem `teleportTo`, e contém chamada `Vec3.yRot` cujo resultado não é guardado. `SlowSpell` não usa spell level diretamente na fórmula de intensidade do amplificador, embora o nível influencie sua duração. Todos exigem QA.

**Estado:** ✅ nove dossiês suplementares source-pinned na PR #825; ⚠️ prova binária e testes provider-native não executados para os três novos; ⛔ sem adapter per-player seguro de alvo/área/posição não comprovado. Stage 06.05/09 sem promoção.

## Current tranche override — six causal dossiers (2026-10-15, PR #825 draft)

A branch mantém **6/110 spells do Iron's com fichas suplementares de auditoria causal source-pinned**: Fireball, Chain Lightning, Counterspell, **Firebolt, Wall of Fire e Teleport**. Isso é **5,45% das 110 identidades** com *este tipo específico* de aprofundamento nesta PR, **não** percentual de APIs mutáveis, implementação de perks ou QA. A tranche anterior 3/110 é preservada como checkpoint histórico abaixo. Nenhum novo objeto semântico mágico foi introduzido: o mínimo do ledger permanece **1.856 global / 1.854 no escopo restrito**, sem denominador global final (—%). As **110 fichas da PR #795** continuam em draft, num trabalho paralelo distinto.

Novos dossiês, sem sobrescrever fichas individuais em `main` nem na PR #795:

- [Firebolt 3.16.3](../providers/✅-irons-spells/audits/CAUSAL-PERKS-FIREBOLT-3.16.3.md) — `0,5×0,5` hitbox, `1,75` bloco/tick, dano `0,5×power` e fire ticks 60.
- [Wall of Fire 3.16.3](../providers/✅-irons-spells/audits/CAUSAL-PERKS-WALL-OF-FIRE-3.16.3.md) — anchors/segmentos, `20` blocos por raycast, duração 240 ticks, risco de múltiplos hits/ticks, persistência e posição final a verificar.
- [Teleport 3.16.3](../providers/✅-irons-spells/audits/CAUSAL-PERKS-TELEPORT-3.16.3.md) — alcance com soft-cap e multiplicadores, dois ramos de destino, `SpellTeleportEvent` com veto e **setters de coordenadas herdados** comprovados no código-fonte NeoForge 1.21.1; equivalência física/API, revalidação de destino e VFX no veto continuam ⚠️.

**Status:** ✅ conteúdo documental source-pinned enviado à PR; ⚠️ paridade de comportamento com JAR físico, config efetiva, efeitos/client/server/Survival e hooks de adaptação não testados; ⛔ alterações de raio/target/hitbox/tempo de terceiros sem seam seguro. A autoridade runtime continua Black Arcana para seus spells e cada provider para sua própria execução; RPG Skill Tree é sibling de perks/progressão.

## Authority consultada para esta tranche

- `Black-Arcana/main@511ec03f0da62ebfc1722825def50354594976c3`.
- `Enshrouded/main@a41dbb51aacb94b7b5db6517f1514b0b7aee3e83`.
- `neoforge-rpg-skilltree/main@9e6436edb0049a8dcc4e47165db0f6850e5efa68`.
- O arquivo sibling `PROJECT-INSTRUCTIONS/modlist/modlist.md` certifica o último dump físico com **587 linhas top-level incluindo o modloader**. Duas adições pós-snapshot foram informadas, **sem novo JAR/dump físico certificado**; ordens de substituição também permanecem pendentes de refetch.
- Conferidos os PRs de Black Arcana em aberto, especialmente a **PR #795** (110 fichas Iron's source-pinned, **draft**) e tranches de prova binária independentes. Não tratar PR aberta como `main`.

## Progresso agregado

| Dimensão | Numerador confirmado | Denominador | Porcentagem admissível |
|---|---:|---:|---|
| Objetos mágicos semânticos estritamente reconstruíveis, universo geral | **1.856 (mínimo)** | Ainda aberto | **—%** |
| Objetos mágicos no escopo restrito registrado no ledger | **1.854 (mínimo)** | Ainda aberto | **—%** |
| Diretórios de provider classificados no checkpoint estrutural | **164** | **164 nesse checkpoint** | **100% estrutural do checkpoint**, não do universo semântico |
| Campanha focal de equivalência binária anotada no ledger em 15/10 | **35 exatos** | **39 da campanha** | **35/39**, não percentual global de catalogação |
| Magias com engenharia completa de perks, todos os mods | **não aferido** | **não aferido** | **—%** |

Os valores 1.856/1.854 e 35/39 são reproduzidos do topo corrente do ledger e do tracker de 15/10, sem deduzir magias novas. O histórico do `docs/catalog/GLOBAL-MAGIC-CATALOG.md` contém checkpoints anteriores 1.849/1.851, que não substituem o ledger mais recente.

## Medidores por provider — dimensões diferentes

| Provider / versão atual da evidência | Identidade ou ficha | Engenharia para perks | Situação |
|---|---|---|---|
| Iron's Spells 'n Spellbooks 3.16.3 | **110/110** fichas ativas já existem em `main`; a PR #795 propõe mapa source-pinned para **110/110** | A PR aprofundou a causalidade de 10 Blood e seis casos adicionais; **não** equivale a 110/110 hooks verificáveis; denominador de completude técnica pendente | ✅ inventário de identidades; 🟡 mapa técnico em PR **draft**; ⚠️ API/runtime |
| Ars Nouveau 5.13.1 | **109/109** identidades estáticas = 85 glyph parts + 24 rituais; registro compilado auditado | Matriz `PERK-ENGINEERING-MATRIX-5.13.1.md` localiza fonte para 85/85 partes; hooks e execução efetiva não homologados globalmente | ✅ IDs; ⚠️ perímetro de mutação |
| Epic Fight 21.17.3.1 | **43/43** skill IDs classificados; **3/3** ações sobrenaturais com ficha individual | Outras **40** habilidades não mágicas continuam relevantes ao RPG/perks; **não** converter 43/43 em cobertura técnica individual | ✅ classificação; ⚠️ perímetro de perks combate |
| Goety, Malum, Eidolon, addons e outros | Consultar ledger por versão física para denominadores exatos | Progressão por dossiê, sem porcentagem técnica fictícia | variável por provider |

**Nota de escopo:** `COUNTED_EXACT` atesta as propriedades demonstradas na prova binária (por exemplo, identidade estática/recipe empacotada), não garante range, dano, custo, consumo, loaded registry ou mutabilidade por API. A tabela explicita deliberadamente quando a fração de engenharia ainda não pode ser calculada.

## Tranche causal adicional — 15/10/2026 (PR #825, draft)

O trio de magias do Iron's Spellbooks 3.16.3 **Fireball, Chain Lightning e Counterspell** recebeu fichas **suplementares** por spell com execução/raycast/efeitos downstream, fórmulas, tipos de parâmetros e source links permanentes. A ordem geral de quatro eventos de perks também foi documentada. Essas alterações estão na **PR #825**, **não na main** nem na PR #795. Não surgiram novas identidades mágicas.

- **3/110** magias do Iron's têm **esta tranche específica** de leitura causal aprofundada, com fichas extra na branch; é uma métrica de execução deste lote, não uma estimativa da completude de todas as 110 fichas nem do trabalho concurrente. O total de engenharia plenamente verificada para perks **continua não aferido**. As 110 fichas da PR #795 permanecem um mapeamento source-pinned, em PR paralela.
- Fireball: [cálculo de dano/raio, projétil, colisão, world explosion](../providers/✅-irons-spells/audits/CAUSAL-PERKS-FIREBALL-3.16.3.md).
- Chain Lightning: [precast 32 blocos vs jump range, ondas de 6 ticks e caps](../providers/✅-irons-spells/audits/CAUSAL-PERKS-CHAIN-LIGHTNING-3.16.3.md).
- Counterspell: [raycast de 80 blocos, evento cancelável, anti-magic alvo](../providers/✅-irons-spells/audits/CAUSAL-PERKS-COUNTERSPELL-3.16.3.md).
- Cross-cutting: [ModifySpellLevel / PreCast / OnCast / SpellDamage / CounterSpell — ordem e riscos](../providers/✅-irons-spells/audits/CAUSAL-PERKS-EVENT-ORDER-3.16.3.md).

**Nova evidência crítica:** `SpellDamageEvent.setAmount` tem efeito antes do `hurt` em `LivingEntity` com `SpellDamageSource`. `SpellOnCastEvent.setManaCost` ocorre **depois** do gate de mana; desconto pós-gate não libera automaticamente casts originalmente inviáveis. `ModifySpellLevelEvent` é observado em `getLevelFor`, porém cobertura de todas as origens de casting ainda não está comprovada. **Nenhuma dessas descobertas autoriza anunciar adapter RPG implementado/testado, mudança de hitbox, alteração arbitrária de `DamageType` ou single-target→AOE.**

## Regra das duas barras nas respostas de catalogação

1. **Barra global:** `% da catalogação técnica completa`, somente com denominador completo e regra homogênea. Enquanto aberto, renderizar barra neutra, `—%` e mínimo estrito 1.856 como valor **não percentual**; não converter o mínimo em 100%.
2. **Barra do mod sendo trabalhado:** explicitar o eixo e o numerador/denominador, preferencialmente `fichas individuais com engenharia causal suficiente / objetos aplicáveis`; quando o eixo técnico não está fechado, exibir **subbarra de identidade** verificável (ex.: Iron's 110/110) junto de `engenharia pendente`. Na UI, dizer se a prova está na `main` ou apenas em PR.
3. Em mods como Epic Fight, manter **dois conjuntos**: 3/3 mágicos para o mínimo Black Arcana; 43/43 habilidades RPG a documentar, sem duplicar os três no numerador global.
4. Ao mudar versão, modlist física, datapacks, config ou source pin, não transportar percentual anterior sem reconciliação.

**Próxima ação específica:** não duplicar a PR #795 de Iron's; revisar causalidade/mutabilidade em seus casos prioritários, mantendo foco em targeting/range/damage/cooldown/hitbox e registrando explicitamente `SEM_HOOK_SEGURO`. Em paralelo, desenvolver uma trilha **RPG skill-card** para Epic Fight separada do numerador de magia. O uso desse baseline não autoriza antecipar o Stage 07 enquanto 06.05/Stage 09 mantêm seus gates.

Contratos aplicáveis: [padrão técnico](PERK-TECHNICAL-CATALOG-CONTRACT.md), [ledger semântico](SEMANTIC-MAGIC-COVERAGE.md), [cobertura atual](CATALOG-COVERAGE-CURRENT.md), [Epic Fight skills](../providers/✅-epic-fight/skills/SKILL-DISPOSITION-21.17.3.1.md), [Ars matrix](../providers/✅-ars-nouveau/PERK-ENGINEERING-MATRIX-5.13.1.md) e [PR #795](https://github.com/Gustavaopere/Black-Arcana/pull/795).
