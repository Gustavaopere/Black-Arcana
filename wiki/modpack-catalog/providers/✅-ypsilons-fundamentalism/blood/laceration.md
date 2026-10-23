# Laceration

**Dossiê documental — 22/10/2026.** `technical_perk_dossier: 1`; `source_status: SOURCE_PINNED`; fidelidade `SOURCE_CAUSALITY` restrita às fontes abaixo; catálogo ⚠️ condicionado para engenharia de perks. **+0 identidades; nenhuma perk, bridge ou implementação.**

- Provider: Ypsilon's Fundamentalism / Fundamental Principles; `mod_id=ypfundamentals`; ID real **`ypfundamentals:laceration`**; taxonomia `spell`; escola default Blood; host Iron's Spellbooks. Classe `com.ypsi.fundamentalism.spells.blood.LacerationSpell`; registro [ModSpells#registerSpell][registry].
- Artefato histórico identificado: `ypfundamentals-1.1.7.1.jar`, Minecraft 1.21.1/NeoForge, SHA-1 `a2855c253202a8fcc2925fcf5b1bf86d64fbe4da`; [CurseForge 8558503](https://www.curseforge.com/minecraft/mc-mods/fundamental-principles/files/8558503), modlist física #575 e [prova binária de 13/10](../EXACT-BINARY-SPELLS-1.1.7.1.md). `COUNTED_EXACT` prova a identidade estática; não prova estas fórmulas, equivalência de métodos ou execução.
- Source Ypsilon: `a9b8f8222fb2a800edece8c1568984bd2a764fc2`, versão declarada 1.1.7.1/MIT, mas dependência declarada **Iron's 3.16.2** ([gradle.properties][versions]). Host examinado separadamente: Iron's **3.16.3**, `e4056af90302d37eb1739f5ff05020b020e6e252`; JAR de referência do pack `irons_spellbooks-1.21.1-3.16.3.jar`. Compatibilidade source→JAR e coexistência **CONDITIONAL**; QA físico **PENDING**.
- Descrição para jogador, paráfrase do [guia oficial][guide]: Golpe frontal em área curta que aplica um estado de redução de cura nos alvos atingidos.

`L` = nível entregue ao efeito; `P` = `getSpellPower(L,caster)` no source host: `(base + incremento×(L−1)) × SPELL_POWER × poder da escola × POWER_MULTIPLIER` ([AbstractSpell#getSpellPower][host-power]). “Neutro” assume esses três multiplicadores iguais a 1. Defaults não demonstram configuração implantada. Mana pertence ao host; não há recurso sangue adicional comprovado nesta classe.

## Pipeline e parâmetros

**Ingresso:** a classe recebe `CastSource`/`MagicData` do host. Item, tecla, pacote de entrada e aquisição exata no Survival **NÃO VERIFICADOS** nesta ficha; o caminho server de admissão/início é [AbstractSpell#attemptInitiateCast][host-cast]. Dimensão/chunks/claims externos não são autorizados por este catálogo.

LONG não interrompível pelo override → `LacerationSpell#onCast` cria caixa frontal → filtra LivingEntity/vida/frente/LOS → `DamageSources.applyDamage` → **somente se retorna true**, executa enchantment post-attack, VFX e aplica **`ypfundamentals:lacerated`** → listener `LaceratedEffect#laceratedHeal` altera futuras `LivingHealEvent`. Não há projétil nem DoT próprio ([golpe][s-cast], [listener][effect-heal]).

| Campo | Default/fórmula e unidade | Origem; fase e boundary | Estado / limite | QA |
|---|---|---|---|---|
| Nível/escola/cooldown | Common; L=1–5; Blood;30 s=600 ticks base | `LacerationSpell` config [s-values]; host [host-values]/[host-cooldown] | `NATIVE` config; efetiva NÃO VERIFICADA | Q1 |
| Mana/cast | `int((40+10×(L−1))×MANA_MULTIPLIER)`=40/50/60/70/80; LONG15 ticks=0.75 s | [s-values], [host-values]/[host-cast] | `NATIVE` custo/config; efetiva duração usa override abaixo | Q1 |
| Tempo/interrupção | `getEffectiveCastTime` retorna `getCastTime(L)`, sem fórmula de cast reduction; `canBeInterrupted(Player)` retorna false | [s-time] | não demonstra imunidade a qualquer cancelamento externo, morte/desconexão; duração seletiva `SEM_HOOK_SEGURO` | Q1/Q4 |
| Targeting/alcance | centro `caster.position + (0,0.3×alturaCaster,0) + forward×2`; AABB.ofSize **1.6×3.2×1.6 blocks** em eixos do mundo | `onCast` [s-cast]; server no settlement | não é raio2 nem cone rotacionado; caixa recebe translação pela direção; `SEM_HOOK_SEGURO` para alcance/geometria | Q2 |
| Filtros/LOS | todos da caixa exceto caster; LivingEntity viva; **caster.isPickable()**; dois testes dot≥0 para posição/centro do alvo; LOS olhos→centro com shields=true | [s-cast], host LOS [host-los] | não “corrigir” caster por target; nenhum cap/ordem/filtro local de ally; helper de dano aplica gates host | Q2/Q3 |
| Power/dano | P neutro5/7/9/11/13; `A=(Utils.getWeaponDamage(caster)+sharpnessLevelCondicional)/2`; dano=`P+A` health points | `getDamage/getAdditionalDamage` [s-formula]; helper host arma [host-weapon] | **A não depende de haver enchantments**; só a adição de Sharpness depende; `NATIVE` power e ATTACK_DAMAGE têm efeitos correlacionados | Q1/Q3 |
| Semântica de arma | host retorna0 se ATTACK_DAMAGE total≤base; caso contrário retorna total e pode já incluir processamento de Sharpness; addon soma ainda o nível de Sharpness se arma não vazia possui ENCHANTMENTS | [host-weapon], [s-formula] | não reduzir a “dano do item”; possível contribuição adicional de Sharpness exige compatibilidade3.16.2→3.16.3 | Q3 |
| DamageType/owner | default `irons_spellbooks:blood_magic`; tags Blood/`neoforge:is_magic`; directEntity=causador=caster | [s-cast], [host-type], [host-source], [host-tags] | dano por evento `CONDITIONAL`; trocar tipo `SEM_HOOK_SEGURO`; nenhum lifesteal explícito | Q3 |
| Lacerated/duração | se dano aceito, `int(P×15 + A×40)` ticks; amp=**1** fixo; ambient/particles/icon=true | [s-cast], `getDuration` [s-formula] | sem A:75/105/135/165/195 ticks; sem cadence/DoT; duração/amp seletivos `SEM_HOOK_SEGURO` | Q3/Q4 |
| Redução de cura | listener LOWEST: sem Blight multiplica0.6 e sempre multiplica0.8 → **0.48×cura**, redução52%; amp não lido | `LaceratedEffect#laceratedHeal` [effect-heal]; evento global por portador | tooltip40% não é cálculo terminal; sem atribuição ao caster original; `SEM_HOOK_SEGURO` para coeficiente por perk | Q4 |
| Coexistência Blight | com Blight, Ypsilon só faz×0.8; host normal faz `1−0.10×(blightAmp+1)` | [effect-heal], `BlightEffect#reduceHealing` [host-blight] | source combinado esperado `0.8×(1−0.1×(amp+1))` com só estes listeners; outros mods, ordem/cancelamento e valores extremos exigem QA | Q4 |
| Projétil/summons/mundo/recast | N/A hitbox de entidade ofensiva, speed/lifetime/pierce, summons e blocos; sem recast próprio, host0 | [s-cast], [host-recast] | AABB é consulta de golpe; VFX100 partículas por hit aceito não é nova área ofensiva | Q2/Q4 |

**Correções e dedup:** a fórmula anterior restringia A a armas encantadas; o source sempre retorna metade de `Utils.getWeaponDamage`, acrescentando Sharpness só no branch de enchantments. `EnchantmentHelper.doPostAttackEffects` roda uma vez por alvo cujo dano foi aceito, usando o damage source do spell; não repetir via bridge. O estado de cura não armazena owner/token; o listener lê apenas presença de Lacerated/Blight, sem scaling pelo amplifier de Lacerated. Correlacionar cast→alvo→dano aceito→effect aplicado; eventos de cura posteriores não são novos hits ou casts. O texto de dano do tooltip ainda anexa `(+weaponDamage/2)` após uma string que já usa `getDamage`; não somar esse texto de novo ([tooltip][s-tooltip]).

## Perks, autoria e verificação

`NATIVE` nesta ficha significa atributo/config do provider identificado no source; não promete controle isolado por jogador. `CONDITIONAL` exige fechar versão, configuração e adapter; `SEM_HOOK_SEGURO` = ⛔ fail-closed para o parâmetro exato. O host possui `SpellOnCastEvent#setSpellLevel(int)` / `setManaCost(int)` antes de pagar mana e chamar `onCast` ([evento][host-events], [ordem][host-cast]); alterar nível nesse ponto não recalcula necessariamente admissão ou duração já iniciada. `SpellDamageEvent#setAmount(float)` altera apenas o montante que passa por `DamageSources.applyDamage`, antes de resistência/`hurt` ([evento][host-damage-event], [settlement][host-damage]). Nenhum desses eventos prova troca de DamageType, alvos, área ou dimensões. As superfícies permanecem **CONDITIONAL** para este addon/JAR. [Boundaries compartilhados](../SPELL-PERK-BOUNDARIES-1.1.7.1.md).

Iron's/Ypsilon conservam cast, mana, cooldown, dano/estados e autoria; RPG Skill Tree conserva progressão/gates por contrato real; Black Arcana só observa ou usa seam validado. Não executar cast, dano, cura, custo ou proc paralelo para simular um parâmetro ausente.

Assinatura semântica ocupada: golpe frontal multialvo curto com contribuição de arma, post-attack de enchantment e estado posterior de cura reduzida. VFX, escala ou novo nome não criam outra identidade. Uma magia original precisaria de regra causal própria; lacunas de design não autorizam implementação.

**QA documental:** classes, métodos e downstream citados lidos no commit pinado; links/linhas e fórmulas revisados. **Não executado:** comparação destes métodos com JAR, servidor dedicado, GameTest, cliente, Survival, PvP/claims e coexistência no pack; todos **PENDING**. Obtenção concreta por scroll, loot, receita e progressão Survival **NÃO VERIFICADA**, salvo gate explicitamente descrito acima.

- **Q1:** duração fixa com cast reduction, custo/cooldown, interrupções internas/externas e mana insuficiente.
- **Q2:** direção vertical/horizontal, bordas/cantos da caixa, diferentes alturas/scales, alvo atrás, parede/escudo e caster não pickable.
- **Q3:** arma sem enchantments, Sharpness, ATTACK_DAMAGE alterado, alvo invulnerável/PvP aliado; effect/enchantment só se applyDamage=true.
- **Q4:** heal sem/com Blight em vários amplifiers e outros listeners; refresh/remoção/morte, listener global sem caster e nenhuma duplicação de post-hit/mastery.

[registry]: https://github.com/ypsilonM/FundamentalPrinciples-1.21.1/blob/a9b8f8222fb2a800edece8c1568984bd2a764fc2/src/main/java/com/ypsi/fundamentalism/spells/ModSpells.java#L27-L49
[versions]: https://github.com/ypsilonM/FundamentalPrinciples-1.21.1/blob/a9b8f8222fb2a800edece8c1568984bd2a764fc2/gradle.properties#L11-L36
[guide]: https://github.com/ypsilonM/FundamentalPrinciples-1.21.1/blob/a9b8f8222fb2a800edece8c1568984bd2a764fc2/src/main/resources/assets/ypfundamentals/lang/en_us.json#L77
[host-values]: https://github.com/iron431/irons-spells-n-spellbooks/blob/e4056af90302d37eb1739f5ff05020b020e6e252/src/main/java/io/redspace/ironsspellbooks/api/spells/AbstractSpell.java#L160-L174
[host-power]: https://github.com/iron431/irons-spells-n-spellbooks/blob/e4056af90302d37eb1739f5ff05020b020e6e252/src/main/java/io/redspace/ironsspellbooks/api/spells/AbstractSpell.java#L211-L257
[host-cast]: https://github.com/iron431/irons-spells-n-spellbooks/blob/e4056af90302d37eb1739f5ff05020b020e6e252/src/main/java/io/redspace/ironsspellbooks/api/spells/AbstractSpell.java#L263-L333
[host-admission]: https://github.com/iron431/irons-spells-n-spellbooks/blob/e4056af90302d37eb1739f5ff05020b020e6e252/src/main/java/io/redspace/ironsspellbooks/api/spells/AbstractSpell.java#L371-L402
[host-recast]: https://github.com/iron431/irons-spells-n-spellbooks/blob/e4056af90302d37eb1739f5ff05020b020e6e252/src/main/java/io/redspace/ironsspellbooks/api/spells/AbstractSpell.java#L227-L232
[host-damage]: https://github.com/iron431/irons-spells-n-spellbooks/blob/e4056af90302d37eb1739f5ff05020b020e6e252/src/main/java/io/redspace/ironsspellbooks/damage/DamageSources.java#L44-L65
[host-source]: https://github.com/iron431/irons-spells-n-spellbooks/blob/e4056af90302d37eb1739f5ff05020b020e6e252/src/main/java/io/redspace/ironsspellbooks/damage/SpellDamageSource.java#L24-L51
[host-type]: https://github.com/iron431/irons-spells-n-spellbooks/blob/e4056af90302d37eb1739f5ff05020b020e6e252/src/main/java/io/redspace/ironsspellbooks/api/registry/SchoolRegistry.java#L109-L116
[host-tags]: https://github.com/iron431/irons-spells-n-spellbooks/blob/e4056af90302d37eb1739f5ff05020b020e6e252/src/main/java/io/redspace/ironsspellbooks/datagen/DamageTypeTagGenerator.java#L29-L94
[host-events]: https://github.com/iron431/irons-spells-n-spellbooks/blob/e4056af90302d37eb1739f5ff05020b020e6e252/src/main/java/io/redspace/ironsspellbooks/api/events/SpellOnCastEvent.java#L29-L74
[host-damage-event]: https://github.com/iron431/irons-spells-n-spellbooks/blob/e4056af90302d37eb1739f5ff05020b020e6e252/src/main/java/io/redspace/ironsspellbooks/api/events/SpellDamageEvent.java#L24-L51
[host-cooldown]: https://github.com/iron431/irons-spells-n-spellbooks/blob/e4056af90302d37eb1739f5ff05020b020e6e252/src/main/java/io/redspace/ironsspellbooks/capabilities/magic/MagicManager.java#L94-L123
[s-values]: https://github.com/ypsilonM/FundamentalPrinciples-1.21.1/blob/a9b8f8222fb2a800edece8c1568984bd2a764fc2/src/main/java/com/ypsi/fundamentalism/spells/blood/LacerationSpell.java#L47-L60
[s-time]: https://github.com/ypsilonM/FundamentalPrinciples-1.21.1/blob/a9b8f8222fb2a800edece8c1568984bd2a764fc2/src/main/java/com/ypsi/fundamentalism/spells/blood/LacerationSpell.java#L62-L70
[s-cast]: https://github.com/ypsilonM/FundamentalPrinciples-1.21.1/blob/a9b8f8222fb2a800edece8c1568984bd2a764fc2/src/main/java/com/ypsi/fundamentalism/spells/blood/LacerationSpell.java#L73-L118
[s-formula]: https://github.com/ypsilonM/FundamentalPrinciples-1.21.1/blob/a9b8f8222fb2a800edece8c1568984bd2a764fc2/src/main/java/com/ypsi/fundamentalism/spells/blood/LacerationSpell.java#L120-L136
[s-tooltip]: https://github.com/ypsilonM/FundamentalPrinciples-1.21.1/blob/a9b8f8222fb2a800edece8c1568984bd2a764fc2/src/main/java/com/ypsi/fundamentalism/spells/blood/LacerationSpell.java#L138-L162
[effect-heal]: https://github.com/ypsilonM/FundamentalPrinciples-1.21.1/blob/a9b8f8222fb2a800edece8c1568984bd2a764fc2/src/main/java/com/ypsi/fundamentalism/effect/custom/LaceratedEffect.java#L13-L33
[host-blight]: https://github.com/iron431/irons-spells-n-spellbooks/blob/e4056af90302d37eb1739f5ff05020b020e6e252/src/main/java/io/redspace/ironsspellbooks/effect/BlightEffect.java#L13-L33
[host-weapon]: https://github.com/iron431/irons-spells-n-spellbooks/blob/e4056af90302d37eb1739f5ff05020b020e6e252/src/main/java/io/redspace/ironsspellbooks/api/util/Utils.java#L787-L802
[host-los]: https://github.com/iron431/irons-spells-n-spellbooks/blob/e4056af90302d37eb1739f5ff05020b020e6e252/src/main/java/io/redspace/ironsspellbooks/api/util/Utils.java#L274-L288
