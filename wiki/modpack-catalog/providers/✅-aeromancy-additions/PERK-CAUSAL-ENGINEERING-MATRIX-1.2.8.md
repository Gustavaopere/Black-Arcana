# Aeromancy Additions 1.2.8 — matriz de engenharia causal para perks

**Atualizado em 29/10/2026 após o fechamento documental de 58 fichas.** Este documento indexa o aprofundamento causal das dez magias Wind de `aero_additions`, preservando autoridade nativa de Iron's e do addon e autoria clean-room do Black Arcana.

## Proveniência e progresso

- **Presença e versão:** modlist sibling identifica `aero_additions-1.2.8.jar` como instalado; ID `aero_additions`, Minecraft 1.21.1/NeoForge. Source oficial fixo [snackerpirater/aero-additions@ae282b32d25ad76ef8d01c637ec05566a767ae4c](https://github.com/snackerpirater/aero-additions/tree/ae282b32d25ad76ef8d01c637ec05566a767ae4c), release 1.2.8.
- **Registry publisher:** [Java21 #38431639191](https://github.com/Gustavaopere/Black-Arcana/actions/runs/38431639191) confirmou dez classes de spell/IDs no JAR *publicado*. JAR publisher SHA-1 `dee32c9fa84a9b3796e39846608f8f77591ea56f`; hash do artefato **fisicamente instalado** é um registro legado incompleto, 35 caracteres. Até medir os bytes instalados, **⚠️ COUNTED_SOURCE_PINNED**, **não COUNTED_EXACT**. [Dossiê físico](EXACT-PUBLISHER-SPELLS-1.2.8-PHYSICAL-SHA-BLOCKED.md).
- **Progresso global:** [índice geral gerado](../INDEX.md), com catálogo e certificação separados. Esta conclusão preserva as dez raízes Aero e acrescenta **0 raízes semânticas**.
- **Barra Aeromancy:** ✅ **58/58 (100%)** fichas da versão-fonte, incluindo os dez spells desta matriz e 48 contratos de suporte; [fechamento e limites](SOURCE-CATALOG-CLOSURE-1.2.8.md). Identidade instalada e gameplay permanecem pendentes; **0/58** certificações estáticas para perks e **0 adapters** homologados. Não converter cobertura de dossiê em percentual de QA.

## Catálogo — dez identidades e semântica causal

| ID `aero_additions:*` | Ficha | Parâmetros/fórmulas e fase observados | Risco/gate | Adapter |
|---|---|---|---|---|
| `wind_charge` | [Wind Charge](spells/wind-charge.md) | MagicWindCharge: lançamento velocidade 1.5; direct hit windCharge fixo 1.0; explosão raio 1.5 sem dano de HP pelo calculator local, força K=1.22×D escalada por power | ⚠️ WorldEffectPolicy/anti-magic, hit + explosion, claims | ⛔ sem hook velocidade/explosão |
| `updraft` | [Updraft](spells/updraft.md) | target helper64, RecastInstance até 3–9 slots; na conclusão movimento +0.9Y, Slow 100 ticks amp3; UI usa getStunDuration 100+20×level | ⚠️ tooltip não equivale à duração de Slow; dano de queda não rastreado | ⛔ sem target/recast edits |
| `airstep` | [Airstep](spells/airstep.md) | 2–8 pulos, duração power×30 ticks, C2S AirstepPacket int,int; save NBT float vs load int | ⚠️ persistência, packet validation, player lifecycle | ⛔ sem incrementar counter externamente |
| `asphyxiate` | [Asphyxiate](spells/asphyxiate.md) | target helper15, continuous 200/300/400 ticks, BREATHLESS a cada 10 remanescentes; ASPHYXIATION 1+0.2×amp a cada 6/5/4 ticks | ⚠️ channel/DOT settlement/i-frames | ⛔ sem DamageType mutation |
| `feather_fall` | [Feather Fall](spells/feather-fall.md) | target helper32 e fallback self, AABB+distância raio3, até 5 alvos; FLIGHT power×20 ticks; modifier GRAVITY weighted | ⚠️ equipamento e multiplicadores de gravidade | ⛔ sem seleção/cap/mutação de attrs |
| `wind_shield` | [Wind Shield](spells/wind-shield.md) | self effect, chance 30–70% no ProjectileImpactEvent, reflexão REVERSE e projectile immunity tag | ⚠️ timing de impacto, demais Dodge semantics/side | ⛔ não ampliar área ou taxa via second handler |
| `airblast` | [Airblast](spells/airblast.md) | projéteis em raio 3–7, cone semiângulo 25–45°, troca owner e nova velocidade 0.15×spellPower (Player) | ⚠️ damage attribution/reflection entity types | ⛔ sem target/radius/caps |
| `wind_blade` | [Wind Blade](spells/wind-blade.md) | um projétil 1.75, sem gravidade; damage=0.5×power; knockback antes de DamageSources.applyDamage | ⚠️ knockback sem dano aceito | ⛔ sem direct geometry mutation |
| `flush` | [Flush](spells/flush.md) | BFS: profundidade 8/10/12, cap 90/140/190 posições únicas aceitas pelo predicado, incluindo origin aceito; pickup, block drops e AIR mutation; getValue(WATERLOGGED) sem guard local | ⛔ WORLD SAFETY BLOCKER: fluidos/blocks/claims/side, exception potential | ⛔ expansão de região/perk ambiental |
| `dash` | [Dash](spells/dash.md) | self impulse direção ponderada por (15+power)/12, server velocity overwrite versus client add; invulnerableTime=20 | ⚠️ client/server movement, i-frames/anti-cheat | ⛔ movement scaling per-caster |

Todas as dez fichas separam: identidade e proveniência; DefaultConfig; cast time/cost e power neutros; targeting/área/tipo de alvo; geometry e hitboxes; spawn/projectile/velocidade quando aplicáveis; durações/status/dano/atributos; ownership e tick/lifecycle; hooks observados versus **SEM_HOOK_SEGURO**, com roteiros de QA. Campos ausentes no source não são inventados.

## Riscos compartilhados

1. **WORLD SAFETY crítica de Flush**: `FlushSpell.removeWaterBreadthFirstSearch` invoca `setBlock(AIR)`, `BucketPickup.pickupBlock`, `Block.dropResources`, busca visitada/bounded e `BlockState.getValue(WATERLOGGED)` sem guard `hasProperty` naquele ramo. Pode afetar conteúdos que não são simplesmente água dependendo de `spongeState.canBeHydrated` e pode ter risco de exceção; isso é **evidência de código e hipótese de QA**, não bug reproduzido. Não deixar uma perk de aumento de radius contornar claims ou WorldEffectPolicy. O Black Arcana **não controla** automaticamente operações do provider externo.
2. **Causalidade de dano diferente da escola:** Wind Charge usa `damageSources().windCharge` para hit direto 1.0 e explosão própria com HP desabilitado no calculator local; Asphyxiate utiliza `AADamageTypes.ASPHYXIATION`; Wind Blade chama `AASpells.WIND_BLADE.getDamageSource`; Airblast reatribui owner de projétil alheio; nenhum deles autoriza mapear por nome uma nova DamageType de RPG. Aplicar XP/Mastery somente a consequências autorizadas e comprovadas.
3. **Network e attachments:** Airstep usa `AirstepPacket` C2S de inteiros e `AeromancySpellData`; `saveNBTData` usa `putFloat` em `airStepHitsRemaining`, `loadNBTData` usa `getInt`. Essa divergência pede teste de save/reload/compat e validação de input/replay. Não editar attachment ou simular salto via comando.
4. **Stages/timing:** Updraft usa `RecastInstance` com targets acumulados; Asphyxiate usa channel server ticks e aplica BREATHLESS temporário; Wind Shield reage a impacto de projétil. Evento de cast, efeito aplicado, projétil desviado e hit/dano liquidado são fases diferentes e devem ser deduplicadas. `UpdraftSpell.getStunDuration` difere dos 100 ticks de slowdown realmente escritos em `onRecastFinished`.
5. **Atributos/equipamentos:** Feather Fall cria `aero_additions:flight.gravity` (ADD_VALUE) a cada 20 ticks conforme peso de equipamento, enquanto a execução de Airstep/Dash impõe velocidades/invulnerableTime. Integrações com Epic Fight e perks de mobilidade precisam medir `AttributeInstance` com jogador real, não apenas registry/tooltip.
6. **Host e compatibilidade:** provider source da 1.2.8 aponta para Iron's 3.16.1, enquanto modpack usa Iron's 3.16.3; ExpandAbility 12.0.0 está embarcada jar-in-jar. Compatibilidade de ABI/métodos, callbacks, efeitos e configuração precisa QA com host instalado, não é inferida da faixa declarada.

## Protocolo de aceitação e proibições

**PENDENTE:** hash SHA-1 do JAR realmente instalado (40 hex); análise dos bytecodes sensíveis exatamente desse arquivo e do Iron's 3.16.3; testes em dedicated server + cliente natural; mana/cooldown ajustados por config; world claims/PvP/Survival, fluidos e blocos com BlockEntity; save/restart/dimensão; anti-magic, onHit/damage accepted, cooldown/recasts e network malformed; performance dos scans e cap de entidades. `Stage 06.05` continua 🟡 e `Stage 09` físico ⚠️ pendente.

Sem hooks seguros de mutação por personagem, a ação é **fail-closed**: não injetar setter/mixin presumido, não fazer dano/efeitos em duplicidade nem transferir ownership de casting/mana/cooldowns e worldstate do provider ao RPG Skill Tree.
