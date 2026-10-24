# Fire’s Ender Expansion 2.4.1 — parâmetros e boundaries para perks

**Reauditoria documental — 24/10/2026.** Base Black Arcana `de3ed3ddbc696597bae5e6dd993e04dbef99aa05` (#878); RPG/modlist `ffd1f1ede5bf46ce3425a5c17bc5d279d8c572dc`, Enshrouded `a41dbb51aacb94b7b5db6517f1514b0b7aee3e83`, Factory `518278ae9c0d264a537cc1bc6ee4974e01270fdf`.

**11/11 é o recorte documental das fichas de spells existentes**, com valores/fórmulas/unidades, consumidores e limites por eixo. Não homologa todas as superfícies do mod nem onze perks/rotas Survival. **+0 identidades/+0 strict**. Config implantada, equivalência de métodos/JAR, hooks integrados e QA físico permanecem PENDING; nenhum runtime, adapter, perk ou dependência foi alterado.

## Identidade, versões e licenças

[Source oficial][versions] `FireOfPower/firesenderexpansion-1.21.1@5e4067e8112316f55c9f249530ba1917a7bf6643`, versão declarada 2.4.1/MC 1.21.1/NeoForge 21.1.215/Iron’s 3.15.6. Commits posteriores mantêm version strings; usar este pin, sem inferir corpo idêntico ao JAR só pela versão. Metadata **All Rights Reserved** não é a licença MIT do template NeoForged. Apenas resumos factuais/paráfrases/permalinks; nenhuma implementação ou arte upstream importada.

O [snapshot físico #281][modlist] registra `firesenderexpansion-2.4.1.jar`, SHA-1 `da87a4a0c926dd75236766584cddbae69c6aeff7`. Publisher CurseForge [8167304](https://www.curseforge.com/minecraft/mc-mods/fires-ender-expansion/files/8167304): 2442013 bytes e SHA-256 `6a02f54a5ffea0443faf31366649be5ea5cb648f0f2cf55b557b198d93b10519`, mesmo SHA-1 do ledger histórico. Medição do publisher não é nova leitura do perfil instalado original, ausente nesta sessão. A [prova binária histórica](EXACT-BINARY-SPELLS-2.4.1.md) fecha onze identidades/refs, sem provar todos os métodos ou efeitos em jogo.

O [build efetivo][build] usa Ace’s Spell Utils file 8079666, cuja release declara 1.2.6.1-1.21.1; a propriedade mínima `asu_version` não substitui esse build target. Pack: Iron’s 3.16.3/Ace’s 1.2.7.2/NeoForge 21.1.250, versus build/dev Black Arcana NeoForge 21.1.248. Host source lido: Iron’s `e4056af90302d37eb1739f5ff05020b020e6e252`; Ace’s `a0b2f4c2fcfa938c8e47239279c77c2ef82647ac`. Os deltas são relevantes para recasts, entidades, mixins e domínios; não afirmar compatibilidade pela assinatura ou pela identidade de um arquivo isolado.

[SpellRegistries][registry] contém onze registros ativos e cada ficha preserva ID, classe e consumer próprios. Escola default de todos é **`irons_spellbooks:ender`**. Status/entidades/curios/partículas/filhos e mudanças de default de outra spell não criam novas raízes neste lote.

| ID real `firesenderexpansion:` | Classe declarante | Ficha / consumer prioritário |
|---|---|---|
| `arcane_slice` | ArcaneSliceSpell | [Arcane Slice](ender/arcane-slice.md), alvo e mana da vítima |
| `aspect_of_the_shulker` | AspectOfTheShulkerSpell | [Aspect](ender/aspect-of-the-shulker.md), buff/evento incoming/bullet vanilla |
| `hollow_crystal` | HollowCrystalSpell | [Crystal](ender/hollow-crystal.md), recasts/charge/projétil/ledger |
| `dimensional_adaptation` | DimensionalAdaptationSpell | [Adaptation](ender/dimensional-adaptation.md), reload/cache de dimensão→efeito |
| `obsidian_rod` | ObsidianRodSpell | [Rod](ender/obsidian-rod.md), channel/Anchored/conversão de bloco |
| `infinite_void` | InfiniteVoidSpell | [Void](ender/infinite-void.md), domínio herdado/transport/status/manager |
| `dragons_fury` | DragonsFurySpell | [Fury](ender/dragons-fury.md), arma+dano/AABB/knockback/child |
| `gate_of_ender` | GateOfEnderSpell | [Gate](ender/gate-of-ender.md), portais/delays/armas/contact |
| `displacement_cage` | DisplacementCageSpell | [Cage](ender/displacement-cage.md), tracking/raio/teleporte |
| `binary_stars` | BinaryStarsSpell | [Binary](ender/binary-stars.md), targets/recasts/projéteis/debuffs |
| `scintillating_stride` | ScintillatingStrideSpell | [Stride](ender/scintillating-stride.md), impulso/mapa/remoção/retorno |

## Escala e configuração: qual consumer lê qual valor

No [AbstractSpell][power], `P=(basePower+perLevelPower×(n−1))×SPELL_POWER×schoolPower×POWER_MULTIPLIER`. A [escola Ender][school] usa os [atributos nativos][attributes] ENDER_SPELL_POWER/ENDER_MAGIC_RESIST e o tipo Ender do host. Native power é input real, mas pode mudar duração/dano/contagem/raio ao mesmo tempo; não é setter isolado de qualquer eixo. Nova Burn e Void Sure Hit usam outros DamageTypes/fontes, conforme abaixo.

[Host][mana] resolve mana `int((baseMana+perLevelMana×(n−1))×MANA_MULTIPLIER)` e cooldown segundos→ticks. Nível/default não é config implantada. Cast time não-CONTINUOUS costuma aplicar o soft-cap do atributo; CONTINUOUS multiplica a duração pelo atributo cru. Overrides podem ignorar parte desse caminho: Fury bypassa redução de tempo; Crystal substitui getCastTime. Cada ficha aponta o consumer real.

FEE registra [config SERVER][bootstrap] `firesenderexpansion-server.toml`, separada da config de spell Iron’s. [Config][config] usa `worldRestart()` e defaults `allow_sword_hail=false`, `hollow_crystal_break_projectiles=true`, ICD Shulker 20 ticks, `fragments_obtainable=true`, `crystal_heart_obtainable=true`, `tbate_black_hole_obtainable=true`. São opções globais/do servidor, não setters por perk/jogador. Não confundir worldRestart com ModConfig.Type.STARTUP ou trocar valores implantados por defaults.

Dimensional Adaptation possui [resource/cache próprio][mapping] com reloadlistener registrado no bootstrap. A tabela de dimensão→efeito é datapack-global, não setter per-player; ausência/erro/reload podem preservar cache antigo ou instalar parte do parse. Classes/recursos associados e edge cases estão na ficha.

## Fases de cast, eventos e mutabilidade

No [wrapper jogador][cast], admissão/custo inicial/check provider/SpellPreCastEvent precedem iniciar cast. Em castSpell: SpellOnCastEvent com custo original → débito conforme CastSource/recast/creative → onCast com nível do evento → recast/cooldown → pacote cliente com nível original. Mudar nível não recalcula o custo automaticamente. A fase de dano/efeito não é provada por esse anúncio pré-efeito; comandos/mobs diretos podem ter outro ingresso.

[MagicManager][tick] liquida canais em intervalos de 10 ticks; onServerCastTick recebe o nível guardado em MagicData a cada tick enquanto casting permanece. **SpellOnCastEvent#setSpellLevel não demonstra alterar o nível desse callback**, por exemplo nas volleys Gate/Rod; é necessário seguir o valor até o consumer. Frequência de pagamento, frequência de tiro e lifecycle das entidades são dimensões diferentes.

| Eixo | Superfície source verificada | Limite para perks |
|---|---|---|
| Admissão | [SpellPreCastEvent][pre-event], cancelável antes do início | Veto de ingresso, não setter de dano/alvo/mana. Gates de mana já foram testados e listeners podem ter side effects próprios. |
| Nível/custo | [SpellOnCastEvent#setSpellLevel/setManaCost][cast-event], no wrapper acima | **HOOK_VERIFICADO** genérico, integração **CONTRATO_CONDICIONAL** para clamp/custo/sync e consumer. Não modifica automaticamente MagicData, alvo, área, tipo ou projétil já criado. |
| Consulta de nível | [ModifySpellLevelEvent#setLevel/addLevels][level-event] via getLevelFor | Input de consulta, não mutação arbitrária do singleton/instância; client/server, admissão e snapshot precisam contrato. |
| Cooldown | [SpellCooldownAddedEvent.Pre][cooldown-event] antes de inserção | Mutável/cancelável nesse caminho, não duração de buff, recast inteiro ou timer de domínio. |
| Dano por helper | [DamageSources.applyDamage][damage-helper] → [SpellDamageEvent][damage-event] apenas LivingEntity+SpellDamageSource | Amount/cancel reais antes de resistência/friendly-fire/hurt; não HP final ou setter de DamageType. Fontes plain/direct hurt não passam por analogia. |
| Teleporte via helper | [Utils.handleSpellTeleport][teleport] publica [SpellTeleportEvent][teleport-event], consome coords e veto | Retorno boolean é **canceled**. Mudança de coordenadas não garante validação de claims/colisão/chunk; posts manuais ignorados e changeDimension/setPos diretos são outros caminhos. |
| Projétil por instância | [AbstractMagicProjectile][projectile-setters] tem setters de damage/pierce/explosionRadius/homing; classes FEE têm setters locais nas fichas | Métodos públicos não são hook universal de spawn nem contrato de reconfiguração a qualquer tick. getSpeed não é setter; geometry/target/type/persistência permanecem condicionados. |
| Área, alvo, mundo e estados | Consumer próprio por ficha, eventualmente constante/config/datapack | Sem seam completo pré-settlement: **⛔ SEM_HOOK_SEGURO** para single→AOE, conversão de tipo, resize, segunda barreira/teleporte ou rollback. N/A só no eixo inaplicável. |

Os [tipos plain NovaBurn][nova-source] e [VoidSureHit][void-source] herdam DamageSource, não SpellDamageSource; seus consumidores usam hurt direto. Source/owner dessas chamadas podem ser a própria vítima afetada, não o caster original. Não atribuir evento de helper, resist do host, kill credit ou recompensa a esse caminho sem prova. JSON/tags/datapacks e outros listeners continuam a participar do resultado.

## Herança, lifecycle e budgets

Cast time, duration field, sync data e lifespan herdado podem ser relógios distintos. Na composição source 3.16.3, Crystal ainda passa pelo expiry do AbstractMagicProjectile antes de alcançar alguns limites maiores locais; Cage tem duration herdado de AoeEntity e outro DURATION sincronizado; Earthquake de Fury tem duração menor que reapplicationDelay. Não promover callbacks potencialmente inalcançáveis a efeito garantido do JAR nem compensar com uma execução BA.

Gate cria portais que criam armas; deadline do portal pode impedir emissões agendadas tarde. Binary Stars não executa slam/AOE comentado. Stride pode anunciar teleporte manual e depois helper, e o evento de remoção não equivale a expiração natural. Contagem de projéteis solicitados, criados, vivos, hits tentados e HP entregue deve permanecer separada.

Infinite Void herda Ace’s AbstractDomainEntity. O arquivo tem blob `1c830383020f373cc7304703a9fbeb307b70eede` tanto no [source1.2.6.1](https://github.com/AceTheEldritchKing/Aces_Spell_Utils/blob/0f6110925de4c4c0422095d9ee9ca8ce4009e438/src/main/java/net/acetheeldritchking/aces_spell_utils/entity/spells/AbstractDomainEntity.java#L37-L56) quanto no [source1.2.7.2][ace-domain]; isso prova somente esse arquivo, não JARs/ABI/hosts completos. Owner map, clash, filtros e ativação herdados não podem ser presumidos equivalentes a WorldEffectPolicy. `addRegionTicket(...,20,...,true)` passa argumento20 à API; não é prova de ticket level20 ou alcance efetivo em chunks. A ficha Void distingue overrides, mapas de origem/retorno, efeitos, manager e duração de cada fase.

## Outros consumidores que afetam integração

[ServerEvents][server-events] contém gates Anchored/InfiniteVoid e um ramo Core of Ender que tenta randomTeleport no pre-cast quando elegível. Alterações de intenção, cancelamento e efeito não são a mesma transição. Anchored também atua em EntityTeleportEvent e [mixins declarados][mixins]; o effect class sozinho não descreve todo enforcement. Compatibilidade dos injection targets3.15.6→3.16.3 continua PENDING.

O mesmo arquivo [altera defaults/item attributes][default-events]: Telekinesis passa ao default Ender nesse evento de configuração, e Dragonskin Spell Book recebe containers de Ender power/mana. Isso não cria uma nova identidade de spell FEE nem um setter per-player de escola; overrides/config implantados e o consumer do item continuam autoridade própria. Rotas de Gate via key e Void via staff são rastreadas nas fichas como leads source, sem prometer Survival montado. Estas referências não encerram todo conteúdo de itens/curios do mod.

## Autoridades dos três projetos e deduplicação

O [RPG IronsSpellbookProgressionEvents][rpg] exige ArcaneAccess no pre-cast HIGHEST com exceções próprias e observa SpellOnCastEvent em LOWEST para Mastery. Escola nativa Ender normaliza para `ender`; [MasteryLaneCatalog][rpg-lane] forma **`irons:ender`** e [MasteryPolicies][rpg-policy] distingue origem/procDepth. Esse evento pré-efeito não comprova hit, cage bounce, spawn, transporte ou duração. Não premiar cada arma, bullet, debuff ou sure-hit como outro cast por heurística.

[Enshrouded MagicDamageClassifier][enshrouded] classifica; o [baseline][enshrouded-baseline] usa tags magic/magic_bypass e pode retornar UNKNOWN. Isso não converte DamageType nem prova classificação efetiva de cada fonte plain FEE. Shroud/exposure e suas regras continuam no owner. A [Factory](https://github.com/Gustavaopere/minecraft-mod-factory/tree/518278ae9c0d264a537cc1bc6ee4974e01270fdf) é referência de tooling futuro, sem transformar esses métodos em APIs de bridge.

FEE/Iron’s/Ace’s mantêm seus efeitos, recursos, domínios e cleanup. Black Arcana mantém seu casting/rituais/domínios/WorldEffectPolicy, sem segundo dano, mana, stamina, status, movimento ou retorno. Dedup requer cast pai, owner/caster efetivo, entidade/UUID, fase/tick, alvo, tipo e consumerSpellID; source/tag/nome visual não bastam. NovaBurn/void victim-source, armas Gate, procs Shulker e anúncios duplos Stride exigem correlação própria.

## Verificação e pendências

Source-pinned por campo e identidade binária são evidências separadas. As onze fichas mantêm fórmulas/defaults, consumers e casos de QA, incluindo o que é N/A ou NÃO VERIFICADO. O [painel atual](../../meta/PROGRESSO-CATALOGO-ATUAL.md) não calcula percentual global de um universo aberto nem promove runtime por documentação.

**PENDING:** métodos/JAR/hosts, SERVER/spell configs/datapacks implantados, mixins aplicados, Survival/cliente, multiplayer/PvP/claims, orçamento de alvos/entidades, dimensões/chunks, callbacks/cancelamentos/cleanup, owner/atribuição e reload/restart/logout/morte. Build/headless BA sem FEE não homologa estes comportamentos. Nenhum Stage promovido.

[versions]: https://github.com/FireOfPower/firesenderexpansion-1.21.1/blob/5e4067e8112316f55c9f249530ba1917a7bf6643/gradle.properties#L15-L50
[build]: https://github.com/FireOfPower/firesenderexpansion-1.21.1/blob/5e4067e8112316f55c9f249530ba1917a7bf6643/build.gradle#L180-L185
[modlist]: https://github.com/Gustavaopere/neoforge-rpg-skilltree/blob/ffd1f1ede5bf46ce3425a5c17bc5d279d8c572dc/PROJECT-INSTRUCTIONS/modlist/modlist.md#L331
[registry]: https://github.com/FireOfPower/firesenderexpansion-1.21.1/blob/5e4067e8112316f55c9f249530ba1917a7bf6643/src/main/java/net/fireofpower/firesenderexpansion/registries/SpellRegistries.java#L13-L34
[power]: https://github.com/iron431/irons-spells-n-spellbooks/blob/e4056af90302d37eb1739f5ff05020b020e6e252/src/main/java/io/redspace/ironsspellbooks/api/spells/AbstractSpell.java#L211-L242
[school]: https://github.com/iron431/irons-spells-n-spellbooks/blob/e4056af90302d37eb1739f5ff05020b020e6e252/src/main/java/io/redspace/ironsspellbooks/api/registry/SchoolRegistry.java#L99-L107
[attributes]: https://github.com/iron431/irons-spells-n-spellbooks/blob/e4056af90302d37eb1739f5ff05020b020e6e252/src/main/java/io/redspace/ironsspellbooks/api/registry/AttributeRegistry.java#L25-L48
[mana]: https://github.com/iron431/irons-spells-n-spellbooks/blob/e4056af90302d37eb1739f5ff05020b020e6e252/src/main/java/io/redspace/ironsspellbooks/api/spells/AbstractSpell.java#L160-L173
[bootstrap]: https://github.com/FireOfPower/firesenderexpansion-1.21.1/blob/5e4067e8112316f55c9f249530ba1917a7bf6643/src/main/java/net/fireofpower/firesenderexpansion/FiresEnderExpansion.java#L63-L82
[config]: https://github.com/FireOfPower/firesenderexpansion-1.21.1/blob/5e4067e8112316f55c9f249530ba1917a7bf6643/src/main/java/net/fireofpower/firesenderexpansion/Config.java#L20-L51
[mapping]: https://github.com/FireOfPower/firesenderexpansion-1.21.1/blob/5e4067e8112316f55c9f249530ba1917a7bf6643/src/main/java/net/fireofpower/firesenderexpansion/effect_dimension_matcher/EffectDimensionMatcher.java#L24-L89
[cast]: https://github.com/iron431/irons-spells-n-spellbooks/blob/e4056af90302d37eb1739f5ff05020b020e6e252/src/main/java/io/redspace/ironsspellbooks/api/spells/AbstractSpell.java#L263-L338
[tick]: https://github.com/iron431/irons-spells-n-spellbooks/blob/e4056af90302d37eb1739f5ff05020b020e6e252/src/main/java/io/redspace/ironsspellbooks/capabilities/magic/MagicManager.java#L27-L85
[pre-event]: https://github.com/iron431/irons-spells-n-spellbooks/blob/e4056af90302d37eb1739f5ff05020b020e6e252/src/main/java/io/redspace/ironsspellbooks/api/events/SpellPreCastEvent.java#L21-L48
[cast-event]: https://github.com/iron431/irons-spells-n-spellbooks/blob/e4056af90302d37eb1739f5ff05020b020e6e252/src/main/java/io/redspace/ironsspellbooks/api/events/SpellOnCastEvent.java#L20-L70
[level-event]: https://github.com/iron431/irons-spells-n-spellbooks/blob/e4056af90302d37eb1739f5ff05020b020e6e252/src/main/java/io/redspace/ironsspellbooks/api/events/ModifySpellLevelEvent.java#L48-L57
[cooldown-event]: https://github.com/iron431/irons-spells-n-spellbooks/blob/e4056af90302d37eb1739f5ff05020b020e6e252/src/main/java/io/redspace/ironsspellbooks/api/events/SpellCooldownAddedEvent.java#L42-L50
[damage-helper]: https://github.com/iron431/irons-spells-n-spellbooks/blob/e4056af90302d37eb1739f5ff05020b020e6e252/src/main/java/io/redspace/ironsspellbooks/damage/DamageSources.java#L44-L64
[damage-event]: https://github.com/iron431/irons-spells-n-spellbooks/blob/e4056af90302d37eb1739f5ff05020b020e6e252/src/main/java/io/redspace/ironsspellbooks/api/events/SpellDamageEvent.java#L13-L48
[teleport]: https://github.com/iron431/irons-spells-n-spellbooks/blob/e4056af90302d37eb1739f5ff05020b020e6e252/src/main/java/io/redspace/ironsspellbooks/api/util/Utils.java#L167-L175
[teleport-event]: https://github.com/iron431/irons-spells-n-spellbooks/blob/e4056af90302d37eb1739f5ff05020b020e6e252/src/main/java/io/redspace/ironsspellbooks/api/events/SpellTeleportEvent.java#L7-L18
[projectile-setters]: https://github.com/iron431/irons-spells-n-spellbooks/blob/e4056af90302d37eb1739f5ff05020b020e6e252/src/main/java/io/redspace/ironsspellbooks/entity/spells/AbstractMagicProjectile.java#L445-L495
[nova-source]: https://github.com/FireOfPower/firesenderexpansion-1.21.1/blob/5e4067e8112316f55c9f249530ba1917a7bf6643/src/main/java/net/fireofpower/firesenderexpansion/damage/NovaBurnDamageSource.java#L15-L30
[void-source]: https://github.com/FireOfPower/firesenderexpansion-1.21.1/blob/5e4067e8112316f55c9f249530ba1917a7bf6643/src/main/java/net/fireofpower/firesenderexpansion/damage/VoidSureHitDamageSource.java#L15-L29
[ace-domain]: https://github.com/AceTheEldritchKing/Aces_Spell_Utils/blob/a0b2f4c2fcfa938c8e47239279c77c2ef82647ac/src/main/java/net/acetheeldritchking/aces_spell_utils/entity/spells/AbstractDomainEntity.java#L37-L56
[server-events]: https://github.com/FireOfPower/firesenderexpansion-1.21.1/blob/5e4067e8112316f55c9f249530ba1917a7bf6643/src/main/java/net/fireofpower/firesenderexpansion/events/ServerEvents.java#L44-L166
[default-events]: https://github.com/FireOfPower/firesenderexpansion-1.21.1/blob/5e4067e8112316f55c9f249530ba1917a7bf6643/src/main/java/net/fireofpower/firesenderexpansion/events/ServerEvents.java#L180-L199
[mixins]: https://github.com/FireOfPower/firesenderexpansion-1.21.1/blob/5e4067e8112316f55c9f249530ba1917a7bf6643/src/main/resources/firesenderexpansion.mixin.json#L1
[rpg]: https://github.com/Gustavaopere/neoforge-rpg-skilltree/blob/ffd1f1ede5bf46ce3425a5c17bc5d279d8c572dc/src/main/java/dev/gustavopere/rpgskilltree/runtime/compat/irons/IronsSpellbookProgressionEvents.java#L26-L99
[rpg-lane]: https://github.com/Gustavaopere/neoforge-rpg-skilltree/blob/ffd1f1ede5bf46ce3425a5c17bc5d279d8c572dc/src/main/java/dev/gustavopere/rpgskilltree/core/MasteryLaneCatalog.java#L82-L84
[rpg-policy]: https://github.com/Gustavaopere/neoforge-rpg-skilltree/blob/ffd1f1ede5bf46ce3425a5c17bc5d279d8c572dc/src/main/java/dev/gustavopere/rpgskilltree/core/MasteryPolicies.java#L5-L12
[enshrouded]: https://github.com/Gustavaopere/Enshrouded/blob/a41dbb51aacb94b7b5db6517f1514b0b7aee3e83/src/main/java/com/gustavaopere/enshrouded/api/combat/MagicDamageClassifier.java#L5-L8
[enshrouded-baseline]: https://github.com/Gustavaopere/Enshrouded/blob/a41dbb51aacb94b7b5db6517f1514b0b7aee3e83/src/main/java/com/gustavaopere/enshrouded/combat/magic/DefaultMagicDamageClassifier.java#L18-L36
