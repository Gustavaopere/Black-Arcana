# Esoteric Strike

**Dossiê documental — 24/10/2026.** `technical_perk_dossier: 1`; identidade `COUNTED_EXACT`, lógica `SOURCE_PINNED / SOURCE_CAUSALITY`, integração `CONTRATO_CONDICIONAL`, QA físico `PENDING`. **+0 identidades/+0 strict**: swipe/animação e partículas são filhos desta spell.

## Identidade, descrição e ingresso

Provider Discerning The Eldritch (`mod_id=discerning_the_eldritch`), spell **`discerning_the_eldritch:esoteric_strike`**, escola default `irons_spellbooks:eldritch`. Declarante `net.acetheeldritchking.discerning_the_eldritch.spells.eldritch.EsotericStrikeSpell`; executor de dano `#onCast`; entidade `entity.spells.esoteric_strike.EsotericStrike` é apresentação com applyEffect vazio. [Registry][registry], [cast executor][execution], [swipe][swipe].

JAR físico histórico **`discerning_the_eldritch-1.4.4-1.21.jar`**, SHA-1 `cf35c225aced23b705d1e0fd1bc5c62d96540e0c`, publisher [CurseForge8816497](https://www.curseforge.com/minecraft/mc-mods/discerning-the-eldritch/files/8816497), 22098930 bytes segundo a [prova binária anterior](../EXACT-BINARY-SPELLS-1.4.4-1.21.md). Source oficial `AceTheEldritchKing/Discerning_The_Eldritch@7bbd81f902c65a4452f47656ebd948cae8cd5833`, versão declarada1.4.4-1.21. Build Iron’s3.16.2/NeoForge21.1.244/Azure3.1.0/Ace1.2.7.2; pack registrado Iron’s3.16.3/NeoForge21.1.250/Azure3.1.11/Ace1.2.7.2. Host consultado Iron’s3.16.3 `e4056af90302d37eb1739f5ff05020b020e6e252`. [Versões][versions], [contratos comuns](../SPELL-PERK-BOUNDARIES-1.4.4-1.21.md). Não se equiparam todos os métodos source/JAR nem a composição de hosts. Metadata MIT versus template PolyForm Shield permanece conflito de sinais de licença; somente fatos/paráfrases/permalinks, sem importar implementação/assets.

[Guia oficial][guide], parafraseado: golpe fortalecido por mana Eldritch. Não implica ataque melee vanilla adicional. A classe não altera loot/crafting/learning: escola Eldritch exige aprendizado e não permite loot genérico por default; crafting segue config/gate host. Aquisição concreta/config física/Survival **NÃO VERIFICADOS**, sem inferir creative-only. [Escola][school], [aquisição][acquisition].

## Pipeline causal e fórmula

Defina `L`=nível recebido no onCast, `C=POWER_MULTIPLIER`, `P=(5+2(L−1))×SPELL_POWER×schoolPower×C`, `A=ATTACK_DAMAGE` atual do caster e `W=Utils.getWeaponDamage(caster)`. **`D=0.35×(P+A)+W` health points por alvo elegível**. `ASUtils#getDamageForAttributes` soma o atributo ao power antes de multiplicar0.35; não é0.35P isolado. W no host pode ser0 quando ATTACK_DAMAGE≤base ou o atributo atual acrescido de Sharpness processado da arma. A e W têm contribuição correlacionada; não adicionar um segundo hit/bonus de arma externo. P/A/W são consultados por vítima no loop, não snapshot explícito único antes dele. [Fórmula][formula], [Ace helper][attribute-helper], [arma][weapon], [power][power].

| L default | Mana neutra | P neutro | Parcela de P no D |
|---|---|---|---|
|1|25|5|1.75HP +0.35A+W|
|2|30|7|2.45HP +0.35A+W|
|3|35|9|3.15HP +0.35A+W|
|4|40|11|3.85HP +0.35A+W|
|5|45|13|4.55HP +0.35A+W|

1. Legendary, níveis default1–5, **INSTANT0ticks**, cooldown default1s. Wrapper Iron’s faz admissão/aprendizado/recursos/pre-cast, publica SpellOnCastEvent e debita antes do onCast. Não há gate local de arma específica, target selection remota ou recast. [Defaults][spell], [host][cast].
2. `#onCast` define radius2.15 e distance1.2; hitLocation=`caster.position+(0,0.3×bbHeight,0)+forward×(1.2,0.35,1.2)`. Consulta Entity em **AABB4.3×2.15×4.3blocks** centrado ali, excluindo caster pela overload de getEntities. Em seguida exige **distância3D ao caster<2.15**, LOS do olho→centroAABB do target (`hasLineOfSight(...,true)`) e target não ItemEntity. `isPickable()` testa o **caster**, não o alvo. A consulta deslocada e o filtro de distância têm centros distintos; não chamar esfera de radius2.15 em torno do hitLocation. [Executor][execution].
3. Para cada elegível, tenta applyDamage com D e fonte da própria spell, direta=causador=caster. Só em retorno true produz50partículas e chama post-attack enchantments. Não há cap, ordenação ou ledger por cast explícitos, mas o loop local visita cada referência consultada uma vez. Sem critical/knockback/debuff próprio declarado; listeners e arma ainda podem produzir consequências downstream. [Executor][execution], [fonte][damage-source].
4. Living+SpellDamageSource usa SpellDamageEvent mutável/cancelável → resistência escolar → friendly fire → hurt; Entity não Living segue hurt direto. Default DamageType **`irons_spellbooks:eldritch_magic`** vem da escola; não do texto de death message. Um retorno true não quantifica HP final. [Helper][damage-helper], [escola][school].
5. Depois do scan cria1 `EsotericStrike` visual, mirrored quando castingEquipmentSlot é OFFHAND; move ao hitLocation e aplica yaw. O visual não recebe D nem owner nesse trecho, e `#applyEffect` é vazio. Seu tick testa `!firstTick`, pode consultar checkHits, e solicita discard quando tickCount≥8 (ticksPerFrame2×4); não chama super.tick. Não inferir idade congelada ou oito ticks físicos sem rastrear o tick externo. Registry2×1/tracking64 e dimensões herdadas2r×1.2 (radius default2) não são a caixa de dano do cast. `#shouldBeSaved=false`. [Spawn][execution], [visual][swipe], [registro][visual-registry], [AoE host][aoe].

## Matriz de parâmetros para perks

| Eixo | Valor / consumer / fase | Boundary real e limite para perks | QA |
|---|---|---|---|
| Dano / escala / crit | D=.35(P+A)+W em `EsotericStrikeSpell#getDamage`, resolvido dentro do loop. Sem crit local. [Fórmula][formula], [Ace][attribute-helper], [arma][weapon]. | SPELL_POWER/ELDRITCH_SPELL_POWER/ATTACK_DAMAGE **NATIVE_ATTRIBUTE**, C **CONFIG_NATIVE**. SpellDamageEvent#setAmount/cancel **HOOK_VERIFICADO** para Living pré-resistência/hurt; adapter **CONDITIONAL**, sem segundo hit melee. | Q1/Q3 |
| Tipo / source | Fonte direta/causadora=caster; default eldritch_magic. [Fonte][damage-source], [escola][school]. | Amount mutável não permite substituir DamageType; conversão **⛔ SEM_HOOK_SEGURO**. Preservar autoria/eventos e tags implantadas. | Q3 |
| Alcance / targeting / LOS | Query deslocada4.3×2.15×4.3; raio de distância2.15 ao caster, LOS e exclusão Item; isPickable do caster. [Executor][execution]. | Sem setter/target resolver externo verificado nesse scan. Reach attribute não é lido aqui por analogia; retarget/range **⛔ SEM_HOOK_SEGURO**. | Q2 |
| Área / budget | Pode afetar vários Entity em uma consulta, sem cap/ordenação/LOS de claims local; helper filtra parte do friendly em Living. [Executor][execution], [helper][damage-helper]. | Já é scan múltiplo, não target único. Area/maxTargets/cylinder/cone por perk **⛔ SEM_HOOK_SEGURO**; não criar AOE paralelo. | Q2/Q3 |
| Projétil / hitbox / apresentação | Não há projétil ofensivo;1swipe pós-scan, OFFHAND espelha; applyEffect vazio. Registro2×1/tracking64 não define melee box. [Visual][swipe], [registro][visual-registry]. | Damage/pierce/speed/homing ofensivos **N/A**. Alterar tamanho/lifetime visual não altera radius literal do cast. Hook visual terceiro **NÃO VERIFICADO**. | Q2/Q4 |
| Tempo / cooldown | INSTANT0ticks; cooldown1s=20ticks default; visual solicita discard em idade≥8, sem super.tick. [Spell][spell], [swipe][swipe]. | Cooldown config e evento Pre descritos no [contrato comum](../SPELL-PERK-BOUNDARIES-1.4.4-1.21.md); tempo visual não é cooldown/cast. Adapter **CONDITIONAL**. | Q1/Q4 |
| Mana / level / recast | `int((25+5(L−1))×MANA_MULTIPLIER)`; sem recast/charge. [Spell][spell], [host][power], [cast][cast]. | **CONFIG_NATIVE**; SpellOnCastEvent#setManaCost/setSpellLevel pré-onCast são hooks reais, admissão já usou custo original e level não recalcula mana. | Q1 |
| Estados / mundo / encantamentos | Só em helper=true há partículas/post-enchant; sem status, teleporte ou mutação de bloco local. [Executor][execution]. | Enchantments são consumer downstream, não segundo cast permitido ao RPG. Novos status/knockback **⛔ SEM_HOOK_SEGURO** nesse método. | Q3 |
| Summons / persistência | Swipe sem AI/owner no spawn observado e shouldBeSaved=false; sem ledger local/summon/custo extra. [Executor][execution], [swipe][swipe]. | Summon cap/AI **N/A**; cleanup visual/sync/firstTick/idade externos **PENDING**. Dedup deve partir do cast pai, não UUID de visual sem autoria. | Q4/Q5 |

## Autoria, concepção e pendências

DTE/Iron’s/Ace possuem cálculo, scan, custo e settlement. RPG Skill Tree possui progressão/perks/Mastery; BA seus casts/world safety e Enshrouded sua classificação/Shroud. Correlação: cast pai→alvo→tentativa helper→resultado→post-enchant; anúncio de cast/visual/50partículas não prova dano nem outra habilidade. Assinatura ocupada: soco curto em área, dependente de spellPower+ATTACK_DAMAGE+arma, com animação espelhável. Nova magia original exige pipeline próprio e dedup, sem copiar implementação/assets.

- **Q1:** aprendizado/origens/config/Survival, níveis1–5, poder/A/W/Sharpness/arma vazia e troca por listener, mana/cooldown/eventlevel.
- **Q2:** caixa versus esfera em centros distintos, pitch/altura/offhand, LOS/cantos/Item/Entity não Living, caster não-pickable, aliados/PvP/claims e budgets.
- **Q3:** SpellDamageEvent cancel/amount/resistência/friendly/iFrames, post-enchant apenas no retorno true, dano final/atribuição/procs e nenhum segundo crédito por VFX.
- **Q4:** spawn visual negado, tickCount/firstTick sem super, deadline8, no-save, sync cliente/servidor e cleanup.
- **Q5:** dedicado/cliente real/multiplayer, logout/morte/restart. **Todos PENDING**; nenhum adapter/perk/runtime novo ou Stage promovido.

[versions]: https://github.com/AceTheEldritchKing/Discerning_The_Eldritch/blob/7bbd81f902c65a4452f47656ebd948cae8cd5833/gradle.properties#L11-L25
[power]: https://github.com/iron431/irons-spells-n-spellbooks/blob/e4056af90302d37eb1739f5ff05020b020e6e252/src/main/java/io/redspace/ironsspellbooks/api/spells/AbstractSpell.java#L148-L241
[cast]: https://github.com/iron431/irons-spells-n-spellbooks/blob/e4056af90302d37eb1739f5ff05020b020e6e252/src/main/java/io/redspace/ironsspellbooks/api/spells/AbstractSpell.java#L263-L347
[school]: https://github.com/iron431/irons-spells-n-spellbooks/blob/e4056af90302d37eb1739f5ff05020b020e6e252/src/main/java/io/redspace/ironsspellbooks/api/registry/SchoolRegistry.java#L138-L148
[acquisition]: https://github.com/iron431/irons-spells-n-spellbooks/blob/e4056af90302d37eb1739f5ff05020b020e6e252/src/main/java/io/redspace/ironsspellbooks/api/spells/AbstractSpell.java#L594-L630
[damage-source]: https://github.com/iron431/irons-spells-n-spellbooks/blob/e4056af90302d37eb1739f5ff05020b020e6e252/src/main/java/io/redspace/ironsspellbooks/api/spells/AbstractSpell.java#L560-L565
[damage-helper]: https://github.com/iron431/irons-spells-n-spellbooks/blob/e4056af90302d37eb1739f5ff05020b020e6e252/src/main/java/io/redspace/ironsspellbooks/damage/DamageSources.java#L44-L64
[damage-event]: https://github.com/iron431/irons-spells-n-spellbooks/blob/e4056af90302d37eb1739f5ff05020b020e6e252/src/main/java/io/redspace/ironsspellbooks/api/events/SpellDamageEvent.java#L24-L51
[registry]: https://github.com/AceTheEldritchKing/Discerning_The_Eldritch/blob/7bbd81f902c65a4452f47656ebd948cae8cd5833/src/main/java/net/acetheeldritchking/discerning_the_eldritch/registries/SpellRegistries.java#L71-L75
[guide]: https://github.com/AceTheEldritchKing/Discerning_The_Eldritch/blob/7bbd81f902c65a4452f47656ebd948cae8cd5833/src/main/resources/assets/discerning_the_eldritch/lang/en_us.json#L194-L195
[spell]: https://github.com/AceTheEldritchKing/Discerning_The_Eldritch/blob/7bbd81f902c65a4452f47656ebd948cae8cd5833/src/main/java/net/acetheeldritchking/discerning_the_eldritch/spells/eldritch/EsotericStrikeSpell.java#L36-L77
[execution]: https://github.com/AceTheEldritchKing/Discerning_The_Eldritch/blob/7bbd81f902c65a4452f47656ebd948cae8cd5833/src/main/java/net/acetheeldritchking/discerning_the_eldritch/spells/eldritch/EsotericStrikeSpell.java#L99-L126
[formula]: https://github.com/AceTheEldritchKing/Discerning_The_Eldritch/blob/7bbd81f902c65a4452f47656ebd948cae8cd5833/src/main/java/net/acetheeldritchking/discerning_the_eldritch/spells/eldritch/EsotericStrikeSpell.java#L128-L155
[attribute-helper]: https://github.com/AceTheEldritchKing/Aces_Spell_Utils/blob/a0b2f4c2fcfa938c8e47239279c77c2ef82647ac/src/main/java/net/acetheeldritchking/aces_spell_utils/utils/ASUtils.java#L227-L237
[weapon]: https://github.com/iron431/irons-spells-n-spellbooks/blob/e4056af90302d37eb1739f5ff05020b020e6e252/src/main/java/io/redspace/ironsspellbooks/api/util/Utils.java#L787-L803
[swipe]: https://github.com/AceTheEldritchKing/Discerning_The_Eldritch/blob/7bbd81f902c65a4452f47656ebd948cae8cd5833/src/main/java/net/acetheeldritchking/discerning_the_eldritch/entity/spells/esoteric_strike/EsotericStrike.java#L17-L89
[visual-registry]: https://github.com/AceTheEldritchKing/Discerning_The_Eldritch/blob/7bbd81f902c65a4452f47656ebd948cae8cd5833/src/main/java/net/acetheeldritchking/discerning_the_eldritch/registries/DTEEntityRegistry.java#L144-L150
[aoe]: https://github.com/iron431/irons-spells-n-spellbooks/blob/e4056af90302d37eb1739f5ff05020b020e6e252/src/main/java/io/redspace/ironsspellbooks/entity/spells/AoeEntity.java#L216-L286
