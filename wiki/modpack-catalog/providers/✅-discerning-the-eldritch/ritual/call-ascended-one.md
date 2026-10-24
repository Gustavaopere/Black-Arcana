# Call: The Ascended One

**Dossiê documental — 24/10/2026.** `technical_perk_dossier: 1`; identidade `COUNTED_EXACT`; lógica `SOURCE_PINNED / SOURCE_CAUSALITY`; mutabilidade `CONTRATO_CONDICIONAL`; QA físico `PENDING`. **+0 identidades/+0 strict**: boss, fases, loot e ataques filhos não criam novas spells-raiz.

## Identidade, descrição e proveniência

Spell **`discerning_the_eldritch:call_ascended_one`**, escola default **`discerning_the_eldritch:ritual`**, declarante `net.acetheeldritchking.discerning_the_eldritch.spells.ritual.CallAscendedOneSpell extends AbstractRitualSpell`. É spell do framework Iron’s/DTE; não é registro do RitualEngine Black Arcana. Legendary, default L1. [Registro][registry], [spell][spell], [escola][school].

Provider **Discerning The Eldritch**, `mod_id=discerning_the_eldritch`; Minecraft 1.21.1 / NeoForge no pack. JAR histórico `discerning_the_eldritch-1.4.4-1.21.jar`, SHA-1 `cf35c225aced23b705d1e0fd1bc5c62d96540e0c`, publisher [CurseForge 8816497](https://www.curseforge.com/minecraft/mc-mods/discerning-the-eldritch/files/8816497), 22098930 bytes. [Prova histórica de identidade](../EXACT-BINARY-SPELLS-1.4.4-1.21.md), sem equiparar todos os métodos ou configs ao source.

Source oficial `AceTheEldritchKing/Discerning_The_Eldritch@7bbd81f902c65a4452f47656ebd948cae8cd5833`, versão declarada 1.4.4-1.21. Build Iron’s 3.16.2 / NeoForge 21.1.244 / Azure 3.1.0 / Ace’s 1.2.7.2; pack Iron’s 3.16.3 / NeoForge 21.1.250 / Azure 3.1.11 / Ace’s 1.2.7.2. Host consultado Iron’s `e4056af90302d37eb1739f5ff05020b020e6e252`. `mod_license=MIT` versus TEMPLATE_LICENSE PolyForm Shield são sinais conflitantes: fatos/paráfrases/permalinks, sem importar implementação/assets. [Versão][versions], [contratos e proveniência comuns](../SPELL-PERK-BOUNDARIES-1.4.4-1.21.md). Config implantada, equivalência de métodos/JAR e compatibilidade física permanecem **PENDING**.

[Guia upstream][guide], parafraseado: chama o Ascended One para enfrentá-lo. O consumer cria um **boss hostil persistente**, não minion controlado. Não há binding de owner, SummonManager.initSummon, SpellSummonEvent ou timer de dispensa no spawn observado. [Spawn][spawn], [constructor][boss-constructor], [AI][boss-targets].

## Ingresso, custos e spawn

1. `isComplex=true` e `isSuperComplex=true`. `AbstractRitualSpell` retorna false para crafting/canBeCraftedBy/loot genérico; rejeita **CastSource.SPELLBOOK e SWORD** e delega os demais ao host. `canBeInterrupted=false` não prova invulnerabilidade a toda saída por morte/logout/cancelamento externo. Não contornar essas restrições com adapter. [Complexidade][complexity], [base Ritual][ritual-base].
2. Lead específico: `loot_table/chests/cultist_base/ascended_vault.json` contém entrada scroll, weight5, com randomize_spell e filtro Call Ascended One. É solicitação source da loot function, não garantia de geração/ingresso: vinculação ao loot executado, filtros do host, CastSource e config/Survival permanecem PENDING. Crafting=false não significa creative-only. [Loot][vault-loot].
3. Defina `L`=nível entregue, `P=(10+10×(L−1))×SPELL_POWER×RITUAL_MAGIC_POWER×POWER_MULTIPLIER`. LONG, cast base100ticks=5s, efetivo `round(100×(2−softCap(CAST_TIME_REDUCTION)))`. Mana `int((1000+100×(L−1))×MANA_MULTIPLIER)`; cooldown default1000s=20000ticks antes de modifiers. Sem recast local. Wrapper jogador publica SpellOnCastEvent/debita antes do onCast; level alterado não recalcula automaticamente o custo. [Defaults][spell], [fórmulas][host-formulas], [ordem][host-cast].
4. `#onCast` usa eyeY do caster, X/Z=eye+Gaussian×3, chama spawnAscendedOneBoss e super. **3 não é raio máximo**; não há validação local de chão/espaço/loaded chunk/claims/dimensão/cap de bosses. Spawna uma instância por execução, sem seleção de alvo inimigo. [Cast/spawn][spawn].
5. Helper privado cria AscendedOneBoss(level), posiciona e escreve stats abaixo, health=max. Chama finalizeSpawn((ServerLevelAccessor)level,difficulty,MOB_SUMMONED,null), depois addFreshEntity, cujo boolean é ignorado. Cast para ServerLevelAccessor exige contexto correto; o método não fornece guarda server própria nem refund/rollback se spawn falhar. Não confundir MobSpawnType.MOB_SUMMONED com vínculo de dono ou contrato de IMagicSummon. [Spawn][spawn].

| Atributo escrito pelo spell | Fórmula / unidade | Default L1/P10 |
|---|---|---|
| AttackDamage | `getAscendedDamage=2.5P`, input em health points por ataque | 25 |
| MAX_HEALTH / health inicial pedido | `getAscendedHealth=60.5P`, health points | 605 |
| SPELL_POWER do boss | `getAscendedSpellPower=0.75P`, atributo multiplicador | 7.5 |
| SPELL_RESIST do boss | `getAscendedSpellResist=0.075P`, atributo do host | 0.75 |

Esses são **snapshots pedidos antes de finalizeSpawn**, não dano/HP final garantidos nem atributos constantes por toda luta. Fórmulas privadas em [CallAscendedOneSpell#getAscended*][stats]; configs/atributos/clamps/modifiers e a AI participam depois. RITUAL_MAGIC_POWER é atributo nativo DTE, associado à escola; não substituir por Eldritch power por semelhança temática. [Escola][school], [atributos][ritual-attributes].

## Consumer boss, fases e mundo

| Superfície / localizador | Comportamento e limite causal |
|---|---|
| Tipo / geometria / defaults | EntityType **0.6×1.8blocks**, tracking64 (visibilidade, não alcance de dano). Factory declara armor50/toughness45, follow range80blocks, interaction4, movement attribute0.25, knockback0.5/resist0.8, MAX_MANA1000 e resistance penetration0.12; quatro stats iniciais acima são sobrescritos pelo spell. Valores efetivos/clamps da composição não foram homologados. [Tipo][boss-type], [factory][boss-attributes], [wiring][attributes-setup]. |
| Owner / AI | Constructor chama setPersistenceRequired, XP reward60. Target goals incluem Player e vários mobs/bosses, sem excluir caster por owner local. Goals de combate lançam spells próprias; não existe resolver single-target ou AI controlável pela raiz. Não interpretar boss como aliado/pet. [Constructor][boss-constructor], [targets][boss-targets], [goals][boss-goals]. |
| Fases / scaling posterior | `#tick` entra na segunda fase quando HP≤max/2, redefine health para metade se ainda vivo, altera goals e grava **SPELL_POWER1.1/SPELL_RESIST1.5**, substituindo os valores pedidos no spawn. Quando HP≤max/4 entra transição; contador começa73, depois fase final redefine SP1.5/resist3.5/armor65/toughness55 e health para um quarto se vivo. P não garante scaling persistente desses atributos. [Fases][boss-phases], [contador][boss-constructor]. |
| Dano recebido / cap | `#hurt` rejeita drown por igualdade de source e, sem BYPASSES_INVULNERABILITY, rejeita durante transição; demais caminhos delegam ao host. `ServerEvents#livingDamageEventPre` com config cap ativo e sem bypass lê **getOriginalDamage**, usa clamp0..cap e setNewDamage. Defaults COMMON: enabled=true/cap100; ordenação pode sobrescrever amount alterado antes por outro listener. Não é dano causado ou setter da vida do boss. [Hurt][boss-hurt], [evento][boss-cap], [config][boss-config], [clamp][basic-cap]. |
| DamageType / ataques | Cast raiz não chama hurt/applyDamage; grava stats e cria boss. A escola Ritual declara `discerning_the_eldritch:ritual_magic` para suas fontes de spell, mas ataques melee/spells da AI escolhem fontes próprias; não atribuir todo dano do boss a esse DamageType ou à identidade CallAscendedOne. Crit/DOT/knockback global por cast **N/A**; seguir cada ataque antes de integração. [Spawn][spawn], [goals][boss-goals], [school][school]. |
| Estados / apresentação | BossEvent, música/fases, taunts, jumpBackwards e imunidade de transição são lifecycle do boss; não são outro cast do jogador. Queries de taunt bbox.inflate15 e nearestPlayer16 não são alcance de targeting da spell. [Fases][boss-phases]. |
| Persistência / cleanup / loot | Boss persiste, salva `phase`, restaura goals conforme fase; não há timer de summon nem despawn de recast do caster. Morte chama castComplete/animação e prepara loot com contexto de atacante; cleanup de bossbar/música/animação/loot, restart e derrota continuam QA. Não aplicar despawn de minion ou rollback BA a essa instância por analogia. [NBT][boss-save], [morte/loot][boss-death]. |

## Matriz de alteração para perks

| Eixo | Valor / fase / consumer | Boundary real, limite e estado | QA |
|---|---|---|---|
| Nível / power / stats | P e quatro fórmulas acima em `spawnAscendedOneBoss`, antes de finalize/spawn; default max1. [Stats][stats], [host][host-formulas]. | SPELL_POWER e DTE RITUAL_MAGIC_POWER **NATIVE_ATTRIBUTE**, POWER_MULTIPLIER **CONFIG_NATIVE**; mudam stats juntos. SpellOnCastEvent#setSpellLevel existe, mas adapter **CONTRATO_CONDICIONAL**, sem clamp independente na classe; mudança não recalcula custo antigo nem evita sobrescritas nas fases. | Q1/Q3 |
| Mana / cooldown / cast time | Mana1000/L1, LONG100 base, cooldown1000s; sem recast próprio. [Spell][spell], [host][host-cast]. | Mana/cooldown config **CONFIG_NATIVE**, CAST_TIME_REDUCTION nativo; amount de mana/cooldown Pre host reais no contrato comum. Sem refund local por addFreshEntity=false. Charges/fuel/stamina/HP/item consumido extra **N/A** no cast observado. | Q1/Q2 |
| Range / spawn / targeting | Gaussian×3 em X/Z, eyeY; uma instância, sem alvo selecionado ou raio máximo/clamp local. [Spawn][spawn]. | Sem hook público específico de posição/count pré-spawn: **⛔ SEM_HOOK_SEGURO** para retarget, alcance, formação/AOE ou cap por perk. Pre-cast observer não comprova spawn ou espaço seguro. | Q2/Q4 |
| Summon / owner / replacement | Boss persistente sem IMagicSummon/SummonManager/event replacement neste caminho. [Spawn][spawn], [constructor][boss-constructor]. | `SpellSummonEvent#setCreature` **não é emitido aqui**. **⛔ SEM_HOOK_SEGURO** para pet/owner/AI/duração/dispensa por perk. Não reclassificar por MobSpawnType.MOB_SUMMONED nem adicionar ledger paralelo. | Q2/Q4 |
| Dano / tipo / resistência | Raiz grava atributos; fases reescrevem parte deles; cap de dano recebido global. [Phases][boss-phases], [cap][boss-cap]. | Atributo nativo não é setter de DamageType de todo ataque. SpellDamageEvent do host só cobre caminho helper verificado; conversão/cap por caster e bypass do boss **⛔ SEM_HOOK_SEGURO** sem consumer exato. Config cap COMMON é global, não perk por jogador. | Q3/Q4 |
| Geometria / velocidade / projétil | Boss0.6×1.8, movement attribute0.25/follow80; raiz não projétil. [Tipo][boss-type], [stats][boss-attributes]. | Resize/speed/AI **⛔ SEM_HOOK_SEGURO** neste cast; pierce/spread/explosion da raiz **N/A**. Projéteis dos ataques filhos exigem ficha/seam próprio; render scale não é hitbox. | Q3/Q4 |
| Mundo / estado / persistência | Entidade hostil persistente e loot, fases/efeitos/AI do provider. [Boss][boss-save], [loot][boss-death]. | Ingresso precisa autoridade de claims/chunks/budgets/WorldEffectPolicy; contrato third-party **CONTRATO_CONDICIONAL**. Não criar segundo boss/loot/teleporte ou refund para simular perk. | Q2/Q4/Q5 |

## Autoria, concepção e QA

Identidade causal: caster→cast CallAscendedOne→UUID boss→fase/AI→ataque/owner efetivo→vítima/loot. O caster não é owner demonstrado dos ataques só por ter criado o boss. Um spawn/taunt/ataque/loot não é outro cast nem recompensa automática de Mastery.

RPG Skill Tree mantém progressão/perks; **a escola custom Ritual tem contrato de lane pendente**, conforme [dossiê comum](../SPELL-PERK-BOUNDARIES-1.4.4-1.21.md), não presumir Mastery funcional por namespace. Black Arcana mantém seu RitualEngine/world safety; Enshrouded seus efeitos; DTE/Iron’s/Ace’s mantêm boss, escola, loot e combate.

Assinatura ocupada: ritual que materializa um inimigo persistente com stats de entrada e fases próprias. Um desafio original com contrato explícito de arena/budget/recompensa é concepção independente, não integração pronta deste boss.

- **Q1:** fingerprint/métodos/hosts/config, L1/eventlevel/power/Ritual attribute, tempo/cooldown/mana e sources; SPELLBOOK/SWORD negados, outras origens não presumidas válidas.
- **Q2:** scroll/filtro/vault/ingresso Survival, spawn negado/obstruído/fora de chunk/gaussianas, cancel pré-cast, falta de mana e sem refund/segundo boss.
- **Q3:** stats pedidos versus efetivos/clamps, fase2/fase4 sobrescrevendo power/resist/armor, cap100/default/bypass/listeners, dano de cada ataque/kill attribution.
- **Q4:** caster alvo/aliados/PvP/claims, AI em outras dimensões/multiplayer, orçamento de bosses persistentes, morte/logout/restart/phase/goals e loot/bossbar/música.
- **Q5:** dedicado/cliente/Survival/sync, Mastery custom lane/dedup e coexistência. **Todos PENDING**; nenhuma implementação de adapter/perk, promoção de Stage ou QA físico inferido.

[versions]: https://github.com/AceTheEldritchKing/Discerning_The_Eldritch/blob/7bbd81f902c65a4452f47656ebd948cae8cd5833/gradle.properties#L10-L25
[host-formulas]: https://github.com/iron431/irons-spells-n-spellbooks/blob/e4056af90302d37eb1739f5ff05020b020e6e252/src/main/java/io/redspace/ironsspellbooks/api/spells/AbstractSpell.java#L148-L257
[host-cast]: https://github.com/iron431/irons-spells-n-spellbooks/blob/e4056af90302d37eb1739f5ff05020b020e6e252/src/main/java/io/redspace/ironsspellbooks/api/spells/AbstractSpell.java#L305-L347
[attributes-setup]: https://github.com/AceTheEldritchKing/Discerning_The_Eldritch/blob/7bbd81f902c65a4452f47656ebd948cae8cd5833/src/main/java/net/acetheeldritchking/discerning_the_eldritch/events/CommonSetup.java#L25-L37
[registry]: https://github.com/AceTheEldritchKing/Discerning_The_Eldritch/blob/7bbd81f902c65a4452f47656ebd948cae8cd5833/src/main/java/net/acetheeldritchking/discerning_the_eldritch/registries/SpellRegistries.java#L171-L177
[spell]: https://github.com/AceTheEldritchKing/Discerning_The_Eldritch/blob/7bbd81f902c65a4452f47656ebd948cae8cd5833/src/main/java/net/acetheeldritchking/discerning_the_eldritch/spells/ritual/CallAscendedOneSpell.java#L26-L68
[complexity]: https://github.com/AceTheEldritchKing/Discerning_The_Eldritch/blob/7bbd81f902c65a4452f47656ebd948cae8cd5833/src/main/java/net/acetheeldritchking/discerning_the_eldritch/spells/ritual/CallAscendedOneSpell.java#L70-L78
[spawn]: https://github.com/AceTheEldritchKing/Discerning_The_Eldritch/blob/7bbd81f902c65a4452f47656ebd948cae8cd5833/src/main/java/net/acetheeldritchking/discerning_the_eldritch/spells/ritual/CallAscendedOneSpell.java#L80-L109
[stats]: https://github.com/AceTheEldritchKing/Discerning_The_Eldritch/blob/7bbd81f902c65a4452f47656ebd948cae8cd5833/src/main/java/net/acetheeldritchking/discerning_the_eldritch/spells/ritual/CallAscendedOneSpell.java#L112-L129
[guide]: https://github.com/AceTheEldritchKing/Discerning_The_Eldritch/blob/7bbd81f902c65a4452f47656ebd948cae8cd5833/src/main/resources/assets/discerning_the_eldritch/lang/en_us.json#L176-L177
[ritual-base]: https://github.com/AceTheEldritchKing/Discerning_The_Eldritch/blob/7bbd81f902c65a4452f47656ebd948cae8cd5833/src/main/java/net/acetheeldritchking/discerning_the_eldritch/spells/ritual/AbstractRitualSpell.java#L12-L59
[school]: https://github.com/AceTheEldritchKing/Discerning_The_Eldritch/blob/7bbd81f902c65a4452f47656ebd948cae8cd5833/src/main/java/net/acetheeldritchking/discerning_the_eldritch/registries/DTESchoolRegistry.java#L30-L40
[ritual-attributes]: https://github.com/AceTheEldritchKing/Discerning_The_Eldritch/blob/7bbd81f902c65a4452f47656ebd948cae8cd5833/src/main/java/net/acetheeldritchking/discerning_the_eldritch/registries/DTEAttributeRegistry.java#L21-L51
[vault-loot]: https://github.com/AceTheEldritchKing/Discerning_The_Eldritch/blob/7bbd81f902c65a4452f47656ebd948cae8cd5833/src/main/resources/data/discerning_the_eldritch/loot_table/chests/cultist_base/ascended_vault.json#L74-L91
[boss-type]: https://github.com/AceTheEldritchKing/Discerning_The_Eldritch/blob/7bbd81f902c65a4452f47656ebd948cae8cd5833/src/main/java/net/acetheeldritchking/discerning_the_eldritch/registries/DTEEntityRegistry.java#L114-L119
[boss-constructor]: https://github.com/AceTheEldritchKing/Discerning_The_Eldritch/blob/7bbd81f902c65a4452f47656ebd948cae8cd5833/src/main/java/net/acetheeldritchking/discerning_the_eldritch/entity/mobs/bosses/ascended_one/AscendedOneBoss.java#L81-L117
[boss-targets]: https://github.com/AceTheEldritchKing/Discerning_The_Eldritch/blob/7bbd81f902c65a4452f47656ebd948cae8cd5833/src/main/java/net/acetheeldritchking/discerning_the_eldritch/entity/mobs/bosses/ascended_one/AscendedOneBoss.java#L254-L270
[boss-goals]: https://github.com/AceTheEldritchKing/Discerning_The_Eldritch/blob/7bbd81f902c65a4452f47656ebd948cae8cd5833/src/main/java/net/acetheeldritchking/discerning_the_eldritch/entity/mobs/bosses/ascended_one/AscendedOneBoss.java#L273-L434
[boss-attributes]: https://github.com/AceTheEldritchKing/Discerning_The_Eldritch/blob/7bbd81f902c65a4452f47656ebd948cae8cd5833/src/main/java/net/acetheeldritchking/discerning_the_eldritch/entity/mobs/bosses/ascended_one/AscendedOneBoss.java#L750-L766
[boss-phases]: https://github.com/AceTheEldritchKing/Discerning_The_Eldritch/blob/7bbd81f902c65a4452f47656ebd948cae8cd5833/src/main/java/net/acetheeldritchking/discerning_the_eldritch/entity/mobs/bosses/ascended_one/AscendedOneBoss.java#L440-L569
[boss-hurt]: https://github.com/AceTheEldritchKing/Discerning_The_Eldritch/blob/7bbd81f902c65a4452f47656ebd948cae8cd5833/src/main/java/net/acetheeldritchking/discerning_the_eldritch/entity/mobs/bosses/ascended_one/AscendedOneBoss.java#L598-L621
[boss-cap]: https://github.com/AceTheEldritchKing/Discerning_The_Eldritch/blob/7bbd81f902c65a4452f47656ebd948cae8cd5833/src/main/java/net/acetheeldritchking/discerning_the_eldritch/events/ServerEvents.java#L549-L565
[boss-config]: https://github.com/AceTheEldritchKing/Discerning_The_Eldritch/blob/7bbd81f902c65a4452f47656ebd948cae8cd5833/src/main/java/net/acetheeldritchking/discerning_the_eldritch/utils/DTEServerConfig.java#L85-L95
[basic-cap]: https://github.com/AceTheEldritchKing/Aces_Spell_Utils/blob/a0b2f4c2fcfa938c8e47239279c77c2ef82647ac/src/main/java/net/acetheeldritchking/aces_spell_utils/utils/ASUtils.java#L330-L332
[boss-save]: https://github.com/AceTheEldritchKing/Discerning_The_Eldritch/blob/7bbd81f902c65a4452f47656ebd948cae8cd5833/src/main/java/net/acetheeldritchking/discerning_the_eldritch/entity/mobs/bosses/ascended_one/AscendedOneBoss.java#L779-L803
[boss-death]: https://github.com/AceTheEldritchKing/Discerning_The_Eldritch/blob/7bbd81f902c65a4452f47656ebd948cae8cd5833/src/main/java/net/acetheeldritchking/discerning_the_eldritch/entity/mobs/bosses/ascended_one/AscendedOneBoss.java#L646-L688
