# Ignite

**Dossiê documental — 22/10/2026.** `technical_perk_dossier: 1`; `source_status: SOURCE_PINNED`; fidelidade `SOURCE_CAUSALITY` restrita às fontes abaixo; catálogo ⚠️ condicionado para engenharia de perks. **+0 identidades; nenhuma perk, bridge ou implementação.**

- Provider: Ypsilon's Fundamentalism / Fundamental Principles; `mod_id=ypfundamentals`; ID real **`ypfundamentals:ignite`**; taxonomia `spell`; escola default Fire; host Iron's Spellbooks. Classe `com.ypsi.fundamentalism.spells.fire.IgniteSpell`; registro [ModSpells#registerSpell][registry].
- Artefato histórico identificado: `ypfundamentals-1.1.7.1.jar`, Minecraft 1.21.1/NeoForge, SHA-1 `a2855c253202a8fcc2925fcf5b1bf86d64fbe4da`; [CurseForge 8558503](https://www.curseforge.com/minecraft/mc-mods/fundamental-principles/files/8558503), modlist física #575 e [prova binária de 13/10](../EXACT-BINARY-SPELLS-1.1.7.1.md). `COUNTED_EXACT` prova a identidade estática; não prova estas fórmulas, equivalência de métodos ou execução.
- Source Ypsilon: `a9b8f8222fb2a800edece8c1568984bd2a764fc2`, versão declarada 1.1.7.1/MIT, mas dependência declarada **Iron's 3.16.2** ([gradle.properties][versions]). Host examinado separadamente: Iron's **3.16.3**, `e4056af90302d37eb1739f5ff05020b020e6e252`; JAR de referência do pack `irons_spellbooks-1.21.1-3.16.3.jar`. Compatibilidade source→JAR e coexistência **CONDITIONAL**; QA físico **PENDING**.
- Descrição para jogador, paráfrase do [guia oficial][guide]: Seleciona uma criatura: incendeia quem está sem fogo e causa dano direto se ela já queima ou é imune a fogo.

`L` = nível entregue ao efeito; `P` = `getSpellPower(L,caster)` no source host: `(base + incremento×(L−1)) × SPELL_POWER × poder da escola × POWER_MULTIPLIER` ([AbstractSpell#getSpellPower][host-power]). “Neutro” assume esses três multiplicadores iguais a 1. Defaults não demonstram configuração implantada. Mana pertence ao host; não há recurso sangue adicional comprovado nesta classe.

## Pipeline e parâmetros

**Ingresso:** a classe recebe `CastSource`/`MagicData` do host. Item, tecla, pacote de entrada e aquisição exata no Survival **NÃO VERIFICADOS** nesta ficha; o caminho server de admissão/início é [AbstractSpell#attemptInitiateCast][host-cast]. Dimensão/chunks/claims externos não são autorizados por este catálogo.

`IgniteSpell#checkPreCastConditions` delega ao host `preCastTargetHelper(...,20,.6f)` → salva `TargetEntityCastData` por UUID → host paga mana → `onCast` resolve o UUID no ServerLevel atual → executa **um** dos dois ramos → completa o cast. Se o alvo resolveu `null`, não há efeito local, mas a classe ainda chama `super.onCast`; não há refund local ([admissão][s-target], [resolução][s-cast], [UUID][host-target-data]).

| Campo | Default/fórmula e unidade | Origem; fase e boundary | Estado / limite | QA |
|---|---|---|---|---|
| Nível/escola/cooldown | Common; L=1–6; Fire; 8 s = 160 ticks base | `IgniteSpell` config [s-values]; host [host-values], [host-cooldown] | `NATIVE` config; efetiva NÃO VERIFICADA | Q1 |
| Mana/cast | `int((15+8×(L−1))×MANA_MULTIPLIER)`; neutro 15/23/31/39/47/55; INSTANT, 0 ticks | construtor [s-values], `getCastType` [s-type], host custo [host-values]/pagamento [host-cast] | `NATIVE`; evento de custo/nível `CONDITIONAL`; sem recurso sangue | Q1 |
| Power | P neutro 12/14/16/18/20/22 | [s-values], `AbstractSpell#getSpellPower` [host-power]; resolvido server | `NATIVE` poder global/Fire/config afeta dano **e** duração do fogo | Q1/Q2 |
| Alcance/aquisição | 20 blocks desde olhos ao longo do look; aim assist = inflação do alvo 0.6 blocks; um LivingEntity do raycast | `checkPreCastConditions` [s-target]; `Utils#preCastTargetHelper` [host-target]; ray [host-ray] | constante local, alcance `SEM_HOOK_SEGURO`; sem teto separado de impacto | Q3 |
| LOS/filtros | host encurta ray em bloco COLLIDER, Fluid.NONE; resultado mais próximo; helper aceita LivingEntity, parent multipart ou passenger específico | [host-target], [host-ray]; aquisição server | filtro inicial do ray é `Utils::canHitWithRaycast`: `isPickable() && isAlive() && !isSpectator()` [host-ray-filter]; filtro extra do helper default `x→true`; não prova proteção/claims. `onCast` não repete alcance/LOS/equipe depois do UUID | Q3 |
| Dano direto | se `target.isOnFire() \|\| target.fireImmune()`: `0.8×P` = 9.6/11.2/12.8/14.4/16/17.6 health points | `onCast` [s-cast], `getFireDamage` [s-formula]; `DamageSources.applyDamage` [host-damage] | montante `CONDITIONAL` por evento; resistência/friendly-fire finais pertencem ao host | Q2/Q3 |
| DamageType/owner | default `irons_spellbooks:fire_magic`, tag Fire + `neoforge:is_magic`; directEntity e causador = caster | [s-cast], [host-type], [host-source], [host-tags] | troca de tipo `SEM_HOOK_SEGURO`; fire-immune escolhe ramo de dano, não garante que dano final atravesse imunidade | Q2/Q3 |
| Ignite/duração | caso contrário: `igniteForSeconds(int(1+0.5×P+L))` = 8/10/12/14/16/18 s neutros | [s-cast], `getFireTime` [s-formula]; server altera estado de fogo | ramo sem `applyDamage`; evento de spell damage não modifica este tempo/estado; `SEM_HOOK_SEGURO` | Q2/Q4 |
| Área/projétil/DoT | N/A AoE/projétil/hitbox/velocidade/lifetime/pierce; nenhum pulso próprio; ticks de fogo ficam no sistema vanilla | [s-cast] | não inventar damage source de cast para cada tick posterior; single→AoE `SEM_HOOK_SEGURO` | Q4 |
| Mundo/summons/recast | N/A blocos/summons/teleporte; sem recast próprio, base 0 | [s-cast], [host-recast] | falha de resolução não cria cast de reposição nem refund automático | Q3/Q4 |

**Boundary causal:** os ramos são mutuamente exclusivos; acender e causar o dano direto simultaneamente duplicaria o efeito. O ramo de ignite não passa pelos gates de `DamageSources.applyDamage`; não presumir que a proteção do ramo de dano é aplicada ali. O addon não guarda cast token no fogo vanilla. Observar cast/UUID/ramo e ticks derivados separadamente; não contar o fogo posterior como recast ou nova magia.

## Perks, autoria e verificação

`NATIVE` nesta ficha significa atributo/config do provider identificado no source; não promete controle isolado por jogador. `CONDITIONAL` exige fechar versão, configuração e adapter; `SEM_HOOK_SEGURO` = ⛔ fail-closed para o parâmetro exato. O host possui `SpellOnCastEvent#setSpellLevel(int)` / `setManaCost(int)` antes de pagar mana e chamar `onCast` ([evento][host-events], [ordem][host-cast]); alterar nível nesse ponto não recalcula necessariamente admissão ou duração já iniciada. `SpellDamageEvent#setAmount(float)` altera apenas o montante que passa por `DamageSources.applyDamage`, antes de resistência/`hurt` ([evento][host-damage-event], [settlement][host-damage]). Nenhum desses eventos prova troca de DamageType, alvos, área ou dimensões. As superfícies permanecem **CONDITIONAL** para este addon/JAR. [Boundaries compartilhados](../SPELL-PERK-BOUNDARIES-1.1.7.1.md).

Iron's/Ypsilon conservam cast, mana, cooldown, dano/estados e autoria; RPG Skill Tree conserva progressão/gates por contrato real; Black Arcana só observa ou usa seam validado. Não executar cast, dano, cura, custo ou proc paralelo para simular um parâmetro ausente.

Assinatura semântica ocupada: aplicação de fogo em alvo único com fallback exclusivo para dano Fire quando o alvo já queima/é imune. VFX, escala ou novo nome não criam outra identidade. Uma magia original precisaria de regra causal própria; lacunas de design não autorizam implementação.

**QA documental:** classes, métodos e downstream citados lidos no commit pinado; links/linhas e fórmulas revisados. **Não executado:** comparação destes métodos com JAR, servidor dedicado, GameTest, cliente, Survival, PvP/claims e coexistência no pack; todos **PENDING**. Obtenção concreta por scroll, loot, receita e progressão Survival **NÃO VERIFICADA**, salvo gate explicitamente descrito acima.

- **Q1:** custo/cooldown/config real e power Fire; conferir truncamento com power fracionário.
- **Q2:** alvo frio, em chamas e fire-immune; comprovar exclusividade e dano após resistência/imunidade.
- **Q3:** limite de 20 blocks, alvo parcialmente oculto, multipart, aliados/PvP/claims; alvo removido ou que muda de dimensão antes da resolução.
- **Q4:** distinguir evento de cast, dano direto e fogo vanilla; testar re-ignite e listeners que alteram dano sem reaplicar o ramo.

[registry]: https://github.com/ypsilonM/FundamentalPrinciples-1.21.1/blob/a9b8f8222fb2a800edece8c1568984bd2a764fc2/src/main/java/com/ypsi/fundamentalism/spells/ModSpells.java#L27-L49
[versions]: https://github.com/ypsilonM/FundamentalPrinciples-1.21.1/blob/a9b8f8222fb2a800edece8c1568984bd2a764fc2/gradle.properties#L11-L36
[guide]: https://github.com/ypsilonM/FundamentalPrinciples-1.21.1/blob/a9b8f8222fb2a800edece8c1568984bd2a764fc2/src/main/resources/assets/ypfundamentals/lang/en_us.json#L78
[host-values]: https://github.com/iron431/irons-spells-n-spellbooks/blob/e4056af90302d37eb1739f5ff05020b020e6e252/src/main/java/io/redspace/ironsspellbooks/api/spells/AbstractSpell.java#L160-L174
[host-power]: https://github.com/iron431/irons-spells-n-spellbooks/blob/e4056af90302d37eb1739f5ff05020b020e6e252/src/main/java/io/redspace/ironsspellbooks/api/spells/AbstractSpell.java#L211-L257
[host-cast]: https://github.com/iron431/irons-spells-n-spellbooks/blob/e4056af90302d37eb1739f5ff05020b020e6e252/src/main/java/io/redspace/ironsspellbooks/api/spells/AbstractSpell.java#L263-L333
[host-admission]: https://github.com/iron431/irons-spells-n-spellbooks/blob/e4056af90302d37eb1739f5ff05020b020e6e252/src/main/java/io/redspace/ironsspellbooks/api/spells/AbstractSpell.java#L371-L402
[host-recast]: https://github.com/iron431/irons-spells-n-spellbooks/blob/e4056af90302d37eb1739f5ff05020b020e6e252/src/main/java/io/redspace/ironsspellbooks/api/spells/AbstractSpell.java#L227-L232
[host-damage]: https://github.com/iron431/irons-spells-n-spellbooks/blob/e4056af90302d37eb1739f5ff05020b020e6e252/src/main/java/io/redspace/ironsspellbooks/damage/DamageSources.java#L44-L65
[host-source]: https://github.com/iron431/irons-spells-n-spellbooks/blob/e4056af90302d37eb1739f5ff05020b020e6e252/src/main/java/io/redspace/ironsspellbooks/damage/SpellDamageSource.java#L24-L51
[host-type]: https://github.com/iron431/irons-spells-n-spellbooks/blob/e4056af90302d37eb1739f5ff05020b020e6e252/src/main/java/io/redspace/ironsspellbooks/api/registry/SchoolRegistry.java#L59-L67
[host-tags]: https://github.com/iron431/irons-spells-n-spellbooks/blob/e4056af90302d37eb1739f5ff05020b020e6e252/src/main/java/io/redspace/ironsspellbooks/datagen/DamageTypeTagGenerator.java#L29-L94
[host-events]: https://github.com/iron431/irons-spells-n-spellbooks/blob/e4056af90302d37eb1739f5ff05020b020e6e252/src/main/java/io/redspace/ironsspellbooks/api/events/SpellOnCastEvent.java#L29-L74
[host-damage-event]: https://github.com/iron431/irons-spells-n-spellbooks/blob/e4056af90302d37eb1739f5ff05020b020e6e252/src/main/java/io/redspace/ironsspellbooks/api/events/SpellDamageEvent.java#L24-L51
[host-cooldown]: https://github.com/iron431/irons-spells-n-spellbooks/blob/e4056af90302d37eb1739f5ff05020b020e6e252/src/main/java/io/redspace/ironsspellbooks/capabilities/magic/MagicManager.java#L94-L123
[s-values]: https://github.com/ypsilonM/FundamentalPrinciples-1.21.1/blob/a9b8f8222fb2a800edece8c1568984bd2a764fc2/src/main/java/com/ypsi/fundamentalism/spells/fire/IgniteSpell.java#L36-L49
[s-target]: https://github.com/ypsilonM/FundamentalPrinciples-1.21.1/blob/a9b8f8222fb2a800edece8c1568984bd2a764fc2/src/main/java/com/ypsi/fundamentalism/spells/fire/IgniteSpell.java#L51-L54
[s-cast]: https://github.com/ypsilonM/FundamentalPrinciples-1.21.1/blob/a9b8f8222fb2a800edece8c1568984bd2a764fc2/src/main/java/com/ypsi/fundamentalism/spells/fire/IgniteSpell.java#L56-L74
[s-formula]: https://github.com/ypsilonM/FundamentalPrinciples-1.21.1/blob/a9b8f8222fb2a800edece8c1568984bd2a764fc2/src/main/java/com/ypsi/fundamentalism/spells/fire/IgniteSpell.java#L76-L81
[s-type]: https://github.com/ypsilonM/FundamentalPrinciples-1.21.1/blob/a9b8f8222fb2a800edece8c1568984bd2a764fc2/src/main/java/com/ypsi/fundamentalism/spells/fire/IgniteSpell.java#L88-L96
[host-target]: https://github.com/iron431/irons-spells-n-spellbooks/blob/e4056af90302d37eb1739f5ff05020b020e6e252/src/main/java/io/redspace/ironsspellbooks/api/util/Utils.java#L665-L712
[host-ray]: https://github.com/iron431/irons-spells-n-spellbooks/blob/e4056af90302d37eb1739f5ff05020b020e6e252/src/main/java/io/redspace/ironsspellbooks/api/util/RaycastBuilder.java#L25-L123
[host-target-data]: https://github.com/iron431/irons-spells-n-spellbooks/blob/e4056af90302d37eb1739f5ff05020b020e6e252/src/main/java/io/redspace/ironsspellbooks/capabilities/magic/TargetEntityCastData.java#L12-L40
[host-ray-filter]: https://github.com/iron431/irons-spells-n-spellbooks/blob/e4056af90302d37eb1739f5ff05020b020e6e252/src/main/java/io/redspace/ironsspellbooks/api/util/Utils.java#L459-L462
