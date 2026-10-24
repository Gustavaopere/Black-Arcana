# Discerning The Eldritch 1.4.4-1.21 — parâmetros e contratos para perks

**Reauditoria documental — 24/10/2026.** Base Black Arcana `0c347bfa534259773bcb59b50e3ceb0010e9d7e4` (#884); RPG/modlist `ffd1f1ede5bf46ce3425a5c17bc5d279d8c572dc`, Enshrouded `a41dbb51aacb94b7b5db6517f1514b0b7aee3e83`, Factory `518278ae9c0d264a537cc1bc6ee4974e01270fdf`.

**22/22 mede as fichas de spells existentes com parâmetros, consumidores e limites por eixo.** Não encerra todo conteúdo de itens/sistemas do mod, mutadores por perk ou aceite físico. **+0 identidades/+0 strict**; config implantada, equivalência integral de métodos/JAR e QA permanecem PENDING. Nenhum runtime, adapter ou dependência alterado.

## Proveniência

[Source oficial][versions] `AceTheEldritchKing/Discerning_The_Eldritch@7bbd81f902c65a4452f47656ebd948cae8cd5833`, versão declarada 1.4.4-1.21, propriedade MC1.21/range[1.21,1.21.2), NeoForge21.1.244. O [build efetivo][build] usa Iron’s3.16.2, Azure3.1.0 e Ace’s CF8789930/1.2.7.2; a variável antiga irons_spells_version3.11.0 não é a dependência efetiva. Pack MC1.21.1/NeoForge21.1.250/Iron’s3.16.3/Azure3.1.11/Ace’s1.2.7.2, dev BA NeoForge21.1.248. Host consultado Iron’s `e4056af90302d37eb1739f5ff05020b020e6e252`. Versão Ace coincidente não prova ABI. Prometheus build1.1.2/pack1.2.5 e Soul Fire’d build6.0.2/pack6.1.0 são limites adicionais dos consumidores de fogo.

[Metadata][metadata] consome mod_license=MIT da propriedade, mas [TEMPLATE_LICENSE.txt][license] contém PolyForm Shield1.0.0; a árvore auditada não tem LICENSE MIT. Preservados esses sinais sem declarar toda implementação MIT. Somente fatos, paráfrases e referências; sem importar corpos upstream ou assets.

O [dossiê binário histórico](EXACT-BINARY-SPELLS-1.4.4-1.21.md) registra 22 IDs/classes e fingerprint físico #220: `discerning_the_eldritch-1.4.4-1.21.jar`, SHA-1 `cf35c225aced23b705d1e0fd1bc5c62d96540e0c`. Publisher [CF8816497](https://www.curseforge.com/minecraft/mc-mods/discerning-the-eldritch/files/8816497) medido nesta sessão: **22098930 bytes**, mesmo SHA-1, SHA-256 `77e53df3fe020572626593ca9f6b955abce1dd4b49697084c2226019dcf2ef14`. Não é nova medição do perfil instalado original, ausente, nem equivalência integral source/classfiles.

[Bootstrap][bootstrap] liga o [registry][registry]: 9 Eldritch, 1 Blood, 2 Evocation, 2 Fire, 1 Holy, 2 Ice e 5 Ritual. Glacial Edge/Glacial Cleave e Zealous Harbinger/Zealous Executioner preservam seus IDs únicos. Filhos, efeitos, summons e presetes não são novas raízes. O índice abaixo usa o prefixo `discerning_the_eldritch:`.

| ID | Classe declarante | Ficha |
|---|---|---|
| `silence` | `SilenceSpell` | [silence](eldritch/silence.md) |
| `conjure_forsaken_aid` | `ConjureForsakenAidSpell` | [conjure-forsaken-aid](eldritch/conjure-forsaken-aid.md) |
| `esoteric_edge` | `EsotericEdgeSpell` | [esoteric-edge](eldritch/esoteric-edge.md) |
| `conjure_gaoler` | `ConjureGaolerSpell` | [conjure-gaoler](eldritch/conjure-gaoler.md) |
| `otherworldly_presence` | `OtherworldlyPresenceSpell` | [otherworldly-presence](eldritch/otherworldly-presence.md) |
| `mend_flesh` | `MendFleshSpell` | [mend-flesh](eldritch/mend-flesh.md) |
| `rift_walker` | `RiftWalkerSpell` | [rift-walker](eldritch/rift-walker.md) |
| `abracadabra` | `AbracadabraSpell` | [abracadabra](eldritch/abracadabra.md) |
| `esoteric_strike` | `EsotericStrikeSpell` | [esoteric-strike](eldritch/esoteric-strike.md) |
| `vein_ripper` | `VeinRipperSpell` | [vein-ripper](blood/vein-ripper.md) |
| `boogie_woogie` | `BoogieWoogieSpell` | [boogie-woogie](evocation/boogie-woogie.md) |
| `guardians_gaze` | `GuardiansGazeSpell` | [guardians-gaze](evocation/guardians-gaze.md) |
| `soul_slice` | `SoulSliceSpell` | [soul-slice](fire/soul-slice.md) |
| `soul_set_ablaze` | `SoulSetAblazeSpell` | [soul-set-ablaze](fire/soul-set-ablaze.md) |
| `exorcism` | `ExorcismSpell` | [exorcism](holy/exorcism.md) |
| `glacial_edge` | `GlacialEdgeSpell` | [glacial-edge](ice/glacial-edge.md) |
| `crystalline_carver` | `CrystallineCarverSpell` | [crystalline-carver](ice/crystalline-carver.md) |
| `call_ascended_one` | `CallAscendedOneSpell` | [call-ascended-one](ritual/call-ascended-one.md) |
| `blades_of_rancor` | `BladesOfRancorSpell` | [blades-of-rancor](ritual/blades-of-rancor.md) |
| `zealous_harbinger` | `ZealousHarbingerSpell` | [zealous-harbinger](ritual/zealous-harbinger.md) |
| `ravenous_revenant` | `RavenousRevenantSpell` | [ravenous-revenant](ritual/ravenous-revenant.md) |
| `libras_judgement` | `LibrasJudgementSpell` | [libras-judgement](ritual/libras-judgement.md) |

## Inputs nativos, configuração e fases

No [AbstractSpell][power], `P=(basePower+perLevelPower×(L−1))×SPELL_POWER×schoolPower×C`, `C=POWER_MULTIPLIER`. Caster null omite atributos, mas **mantém C**. getEntityPowerMultiplier também inclui C. Otherworldly/Rift combinam P(null) com softCap desse multiplier; preservar o C externo e o interno. Cada ficha explicita snapshot, armas, truncamento e caps.

Mana é `int((baseMana+perLevelMana×(L−1))×MANA_MULTIPLIER)`; cooldown config segundos×20 antes de modifiers. Cast time comum usa softCap em não-CONTINUOUS; overrides podem ignorar atributos ou consultar CastType. [Ritual][schools] é escola própria `discerning_the_eldritch:ritual`, com [atributos][attributes] ritual_spell_power/ritual_magic_resist sync/default1/range−100..100 e [DamageType ritual_magic][damage-type]. Power não é setter isolado de área/tipo/hitbox.

[DTEServerConfig][config] é registrada como **COMMON**, arquivo `discerning_the_eldritch-common.toml`, apesar do nome. Defaults: Mend hit/XP=true; Insanity=false/max15; Abracadabra cap=true/base80/hex prevention=true. [onLoad][config-load] copia propriedades para fields estáticos. São opções globais, sem setter per-player/range demonstrado nessas entradas. Config implantada/reload/sync precisam observação.

No [wrapper jogador][cast], canBeCastedBy/checkPreCastConditions/SpellPreCastEvent precedem iniciar cast; onServerPreCast pode criar estados/filhos. No settlement: SpellOnCastEvent → débito conforme origem/recast/creative → onCast com nível do evento → recast/cooldown → pacote cliente com nível original. Mudar nível não recalcula custo automaticamente nem recompõe alvo/pre-effects. Spawn recusado, damage=false e teleporte vetado têm consequências próprias.

| Eixo | Superfície source verificada | Limite para perks |
|---|---|---|
| Nível / mana | [SpellOnCastEvent#setSpellLevel/setManaCost][cast-event]; getLevelFor publica ModifySpellLevelEvent no [host][power] | HOOK_VERIFICADO genérico, adapter CONDITIONAL; não altera automaticamente snapshots, MagicData, resolver ou pagamento anterior. |
| Cooldown / recast | [SpellCooldownAddedEvent.Pre][cooldown-event], [RecastInstance][recast-count], [PlayerRecasts][recasts] | Total casts inclui inicial; remaining=total−1. Remoção dispara callback, inclusive timeout; setter de cooldown não é setter de janela, filhos ou contagem. |
| Dano por helper | [applyDamage][damage-helper] e [SpellDamageEvent][damage-event] para Living+SpellDamageSource | Amount/cancel antes de resistência/friendly/hurt, sem setter de DamageType ou confirmação de HP. |
| Hurt direto | [Listeners host pré/pós-hit][post-hit] ainda reconhecem SpellDamageSource | Pular helper não torna a fonte plain nem elimina lifesteal/freeze/fire/iFrames/eventos NeoForge. Blood Rot plain é caminho diferente. |
| Cura | [SpellHealEvent][heal-event] tem healAmount final/getter, sem setter/cancelamento | Observer, não mutador de Mend. Cast, cura fixa por Post e cura por XP são consumidores separados. |
| Teleporte | [handleSpellTeleport][teleport] consome coords/veto do [SpellTeleportEvent][teleport-event]; boolean retornado=canceled | Otherworldly/Rift ignoram retorno e podem seguir efeitos sem chegada. Boogie usa teleportTo direto; não inferir rollback ou proteção pelo helper. |
| Summons | [SpellSummonEvent#setCreature][summon-event], [SummonManager][summon-manager] | Replacement real, não cancelável; casts para tipos concretos limitam compatibilidade. Remover binding não equivale a limpar toda fila de expiração. |
| Projétil / área / estado | Métodos por instância e [AbstractMagicProjectile][projectile] | Setter público não é callback terceiro pré-spawn. Expiry herdado e clocks locais são distintos. Sem seam completo: ⛔ SEM_HOOK_SEGURO para retarget/single→AOE/tipo/resize. |

## Consumidores globais e persistência

[ServerEvents#onPlayerCastEvent][precast] cancela pre-cast de ServerPlayer com Silence; no mesmo método pode incrementar Insanity de Eldritch **após cancelar**, sem early return, e depois vetar Metaphysical. Contador/pre-cast não confirma lançamento. [Tick Insane][insane-tick] solicita Darkness110/amplifier9 a cada100ticks sem gate enableInsanitySystem nesse trecho; desligar config não prova limpeza anterior.

[LivingIncomingDamageEvent][metaphysical] localiza o veto antes não encontrado na auditoria antiga: vítima com Metaphysical **ou causingEntity Living com Metaphysical** cancela incoming; o handler continua depois. Não prova proteção em caminhos que não publiquem o evento, nem desfaz todo custo/proc anterior.

[Attachments][attachments] serializam InsanityMeter, IsInsane, Frostbite e DevouredEntities. [SOUL_FIRE_STACKS][components] é componente persistente ExtraCodecs.POSITIVE_INT/network VAR_INT, sem prova automática de cap de gameplay ou persistência coerente de todo combo. São dados DTE, sem segundo ledger RPG. Morte/clone/relog/reload e invariantes entre flags/valores precisam QA. Slice/Ablaze consomem stacks em fases diferentes. [Blood Rot][blood-rot] tem fonte plain estática sem caster original e dano periódico próprio.

[Mend hit][mend-hit] cura1.5 por evento Post elegível sem filtro local de amount; [Mend XP][mend-xp] usa event.amount/2. Esses consumidores coexistem com lifesteal host; não somar uma segunda cura por observar o mesmo evento. Curios/armas podem retirar Silence, alterar recasts, instalar spells ou conceder afinidade. As fichas distinguem preset, AffinityData e aquisição apenas rastreada.

Os [cinco Ritual][ritual] são spells Iron’s/DTE, sem vínculo automático com RitualEngine BA. Crafting=false; loot depende de complexidade; complex+super rejeita SPELLBOOK/SWORD, complex não-super rejeita SPELLBOOK; canBeInterrupted=false é contrato local, não imunidade a todo cancelamento. Loot/cauldron/itens são pistas de aquisição, sem inferir creative-only ou Survival aprovado.

## Autoridades dos três projetos e Mastery Ritual

[RPG IronsSpellbookProgressionEvents][rpg] exige ArcaneAccess no pre-cast HIGHEST com exceções e observa SpellOnCastEvent LOWEST para Mastery antes do efeito. Escolas Iron’s normalizam para eldritch/blood/fire/ice; Ritual custom normaliza para **`discerning_the_eldritch/ritual`**. [MasteryPolicies.forIron][rpg-policy] passa esse token a [ironsDiscipline][rpg-lane-api], mas [regex MEMBER][rpg-lanes] e [dynamicMember][rpg-lane-validation] rejeitam `/` com IllegalArgumentException. Não declarar `irons:ritual` ou essa disciplina custom como lane integrada/aceita.

Reprodução estreita nesta sessão: compilar a classe pura MasteryLaneCatalog do pin RPG fora do projeto confirmou eldritch→irons:eldritch e rejeição de discerning_the_eldritch/ritual. Isso demonstra o método, **não crash observado no modpack**. Compatibilidade/progressão dos cinco Ritual é CONDITIONAL; sem contornar gates, renomear escola ou alterar repos neste lote. Inscrição usa a mesma normalização em outro consumidor; string de consulta não é lane validada.

[Enshrouded][enshrouded] mantém classificação por tags magic/magic_bypass e pode retornar UNKNOWN. Escola/nome Ritual não converte DamageType nem concede autoridade de Shroud/exposure. Factory `Gustavaopere/minecraft-mod-factory@518278ae9c0d264a537cc1bc6ee4974e01270fdf` segue referência de tooling futuro.

DTE/Iron’s/Ace’s/dependências mantêm cast, recursos, summons, procs e cleanup; BA mantém seu runtime/world policy; RPG mantém progressão; Enshrouded seus efeitos. Dedup exige cast pai/origem/owner/recast/entidade/vítima/fase/tick/sourceSpellID. Partículas, anúncios, cada DOT/jaw e tentativa falha não são novas magias ou Mastery. Static first-owner de SoulEruption/RitualBurn e singleton isFinalCast de Carver exigem casos multiplayer; não remediar por ledger ou dano paralelo.

## Verificação e pendências

As fichas separam evidência por campo, métodos observados, trechos sem efeito no caminho ativo e valores N/A/não verificados. [Painel atual](../../meta/PROGRESSO-CATALOGO-ATUAL.md): universo aplicável aberto. Identidade binária, causalidade source, capacidade mutadora e aceite físico são dimensões diferentes.

**PENDING:** métodos/JAR/hosts, config/datapacks implantados, aquisição Survival, dedicado/cliente/multiplayer/PvP/claims, chunks/destinos/rollback, budgets, autoria, callbacks/procs, persistência/sync/morte/reload/restart e execução de adapters. CI BA sem DTE não homologa esses comportamentos; nenhum Stage promovido.

[versions]: https://github.com/AceTheEldritchKing/Discerning_The_Eldritch/blob/7bbd81f902c65a4452f47656ebd948cae8cd5833/gradle.properties#L11-L30
[build]: https://github.com/AceTheEldritchKing/Discerning_The_Eldritch/blob/7bbd81f902c65a4452f47656ebd948cae8cd5833/build.gradle#L175-L245
[metadata]: https://github.com/AceTheEldritchKing/Discerning_The_Eldritch/blob/7bbd81f902c65a4452f47656ebd948cae8cd5833/src/main/templates/META-INF/neoforge.mods.toml#L12-L27
[license]: https://github.com/AceTheEldritchKing/Discerning_The_Eldritch/blob/7bbd81f902c65a4452f47656ebd948cae8cd5833/TEMPLATE_LICENSE.txt#L1-L10
[bootstrap]: https://github.com/AceTheEldritchKing/Discerning_The_Eldritch/blob/7bbd81f902c65a4452f47656ebd948cae8cd5833/src/main/java/net/acetheeldritchking/discerning_the_eldritch/DiscerningTheEldritch.java#L46-L85
[registry]: https://github.com/AceTheEldritchKing/Discerning_The_Eldritch/blob/7bbd81f902c65a4452f47656ebd948cae8cd5833/src/main/java/net/acetheeldritchking/discerning_the_eldritch/registries/SpellRegistries.java#L25-L187
[config]: https://github.com/AceTheEldritchKing/Discerning_The_Eldritch/blob/7bbd81f902c65a4452f47656ebd948cae8cd5833/src/main/java/net/acetheeldritchking/discerning_the_eldritch/utils/DTEServerConfig.java#L17-L51
[config-load]: https://github.com/AceTheEldritchKing/Discerning_The_Eldritch/blob/7bbd81f902c65a4452f47656ebd948cae8cd5833/src/main/java/net/acetheeldritchking/discerning_the_eldritch/utils/DTEServerConfig.java#L134-L159
[schools]: https://github.com/AceTheEldritchKing/Discerning_The_Eldritch/blob/7bbd81f902c65a4452f47656ebd948cae8cd5833/src/main/java/net/acetheeldritchking/discerning_the_eldritch/registries/DTESchoolRegistry.java#L16-L42
[attributes]: https://github.com/AceTheEldritchKing/Discerning_The_Eldritch/blob/7bbd81f902c65a4452f47656ebd948cae8cd5833/src/main/java/net/acetheeldritchking/discerning_the_eldritch/registries/DTEAttributeRegistry.java#L20-L54
[damage-type]: https://github.com/AceTheEldritchKing/Discerning_The_Eldritch/blob/7bbd81f902c65a4452f47656ebd948cae8cd5833/src/main/resources/data/discerning_the_eldritch/damage_type/ritual_magic.json#L1-L5
[attachments]: https://github.com/AceTheEldritchKing/Discerning_The_Eldritch/blob/7bbd81f902c65a4452f47656ebd948cae8cd5833/src/main/java/net/acetheeldritchking/discerning_the_eldritch/registries/DTEAttachmentRegistry.java#L15-L28
[components]: https://github.com/AceTheEldritchKing/Discerning_The_Eldritch/blob/7bbd81f902c65a4452f47656ebd948cae8cd5833/src/main/java/net/acetheeldritchking/discerning_the_eldritch/registries/DTEDataComponentRegistry.java#L15-L17
[precast]: https://github.com/AceTheEldritchKing/Discerning_The_Eldritch/blob/7bbd81f902c65a4452f47656ebd948cae8cd5833/src/main/java/net/acetheeldritchking/discerning_the_eldritch/events/ServerEvents.java#L87-L191
[insane-tick]: https://github.com/AceTheEldritchKing/Discerning_The_Eldritch/blob/7bbd81f902c65a4452f47656ebd948cae8cd5833/src/main/java/net/acetheeldritchking/discerning_the_eldritch/events/ServerEvents.java#L193-L205
[metaphysical]: https://github.com/AceTheEldritchKing/Discerning_The_Eldritch/blob/7bbd81f902c65a4452f47656ebd948cae8cd5833/src/main/java/net/acetheeldritchking/discerning_the_eldritch/events/ServerEvents.java#L419-L441
[mend-hit]: https://github.com/AceTheEldritchKing/Discerning_The_Eldritch/blob/7bbd81f902c65a4452f47656ebd948cae8cd5833/src/main/java/net/acetheeldritchking/discerning_the_eldritch/events/ServerEvents.java#L251-L265
[mend-xp]: https://github.com/AceTheEldritchKing/Discerning_The_Eldritch/blob/7bbd81f902c65a4452f47656ebd948cae8cd5833/src/main/java/net/acetheeldritchking/discerning_the_eldritch/events/ServerEvents.java#L525-L546
[ritual]: https://github.com/AceTheEldritchKing/Discerning_The_Eldritch/blob/7bbd81f902c65a4452f47656ebd948cae8cd5833/src/main/java/net/acetheeldritchking/discerning_the_eldritch/spells/ritual/AbstractRitualSpell.java#L12-L60
[blood-rot]: https://github.com/AceTheEldritchKing/Discerning_The_Eldritch/blob/7bbd81f902c65a4452f47656ebd948cae8cd5833/src/main/java/net/acetheeldritchking/discerning_the_eldritch/effects/BloodRotPotionEffect.java#L17-L58
[power]: https://github.com/iron431/irons-spells-n-spellbooks/blob/e4056af90302d37eb1739f5ff05020b020e6e252/src/main/java/io/redspace/ironsspellbooks/api/spells/AbstractSpell.java#L148-L257
[cast]: https://github.com/iron431/irons-spells-n-spellbooks/blob/e4056af90302d37eb1739f5ff05020b020e6e252/src/main/java/io/redspace/ironsspellbooks/api/spells/AbstractSpell.java#L263-L351
[cast-event]: https://github.com/iron431/irons-spells-n-spellbooks/blob/e4056af90302d37eb1739f5ff05020b020e6e252/src/main/java/io/redspace/ironsspellbooks/api/events/SpellOnCastEvent.java#L20-L74
[cooldown-event]: https://github.com/iron431/irons-spells-n-spellbooks/blob/e4056af90302d37eb1739f5ff05020b020e6e252/src/main/java/io/redspace/ironsspellbooks/api/events/SpellCooldownAddedEvent.java#L42-L50
[damage-helper]: https://github.com/iron431/irons-spells-n-spellbooks/blob/e4056af90302d37eb1739f5ff05020b020e6e252/src/main/java/io/redspace/ironsspellbooks/damage/DamageSources.java#L44-L64
[post-hit]: https://github.com/iron431/irons-spells-n-spellbooks/blob/e4056af90302d37eb1739f5ff05020b020e6e252/src/main/java/io/redspace/ironsspellbooks/damage/DamageSources.java#L91-L131
[damage-event]: https://github.com/iron431/irons-spells-n-spellbooks/blob/e4056af90302d37eb1739f5ff05020b020e6e252/src/main/java/io/redspace/ironsspellbooks/api/events/SpellDamageEvent.java#L13-L50
[heal-event]: https://github.com/iron431/irons-spells-n-spellbooks/blob/e4056af90302d37eb1739f5ff05020b020e6e252/src/main/java/io/redspace/ironsspellbooks/api/events/SpellHealEvent.java#L18-L40
[recast-count]: https://github.com/iron431/irons-spells-n-spellbooks/blob/e4056af90302d37eb1739f5ff05020b020e6e252/src/main/java/io/redspace/ironsspellbooks/capabilities/magic/RecastInstance.java#L27-L35
[recasts]: https://github.com/iron431/irons-spells-n-spellbooks/blob/e4056af90302d37eb1739f5ff05020b020e6e252/src/main/java/io/redspace/ironsspellbooks/capabilities/magic/PlayerRecasts.java#L117-L212
[teleport]: https://github.com/iron431/irons-spells-n-spellbooks/blob/e4056af90302d37eb1739f5ff05020b020e6e252/src/main/java/io/redspace/ironsspellbooks/api/util/Utils.java#L167-L175
[teleport-event]: https://github.com/iron431/irons-spells-n-spellbooks/blob/e4056af90302d37eb1739f5ff05020b020e6e252/src/main/java/io/redspace/ironsspellbooks/api/events/SpellTeleportEvent.java#L7-L18
[summon-event]: https://github.com/iron431/irons-spells-n-spellbooks/blob/e4056af90302d37eb1739f5ff05020b020e6e252/src/main/java/io/redspace/ironsspellbooks/api/events/SpellSummonEvent.java#L7-L39
[summon-manager]: https://github.com/iron431/irons-spells-n-spellbooks/blob/e4056af90302d37eb1739f5ff05020b020e6e252/src/main/java/io/redspace/ironsspellbooks/capabilities/magic/SummonManager.java#L79-L161
[projectile]: https://github.com/iron431/irons-spells-n-spellbooks/blob/e4056af90302d37eb1739f5ff05020b020e6e252/src/main/java/io/redspace/ironsspellbooks/entity/spells/AbstractMagicProjectile.java#L46-L114
[rpg]: https://github.com/Gustavaopere/neoforge-rpg-skilltree/blob/ffd1f1ede5bf46ce3425a5c17bc5d279d8c572dc/src/main/java/dev/gustavopere/rpgskilltree/runtime/compat/irons/IronsSpellbookProgressionEvents.java#L26-L100
[rpg-policy]: https://github.com/Gustavaopere/neoforge-rpg-skilltree/blob/ffd1f1ede5bf46ce3425a5c17bc5d279d8c572dc/src/main/java/dev/gustavopere/rpgskilltree/core/MasteryPolicies.java#L4-L12
[rpg-lanes]: https://github.com/Gustavaopere/neoforge-rpg-skilltree/blob/ffd1f1ede5bf46ce3425a5c17bc5d279d8c572dc/src/main/java/dev/gustavopere/rpgskilltree/core/MasteryLaneCatalog.java#L7-L11
[rpg-lane-api]: https://github.com/Gustavaopere/neoforge-rpg-skilltree/blob/ffd1f1ede5bf46ce3425a5c17bc5d279d8c572dc/src/main/java/dev/gustavopere/rpgskilltree/core/MasteryLaneCatalog.java#L82-L84
[rpg-lane-validation]: https://github.com/Gustavaopere/neoforge-rpg-skilltree/blob/ffd1f1ede5bf46ce3425a5c17bc5d279d8c572dc/src/main/java/dev/gustavopere/rpgskilltree/core/MasteryLaneCatalog.java#L125-L129
[enshrouded]: https://github.com/Gustavaopere/Enshrouded/blob/a41dbb51aacb94b7b5db6517f1514b0b7aee3e83/src/main/java/com/gustavaopere/enshrouded/combat/magic/DefaultMagicDamageClassifier.java#L18-L38
