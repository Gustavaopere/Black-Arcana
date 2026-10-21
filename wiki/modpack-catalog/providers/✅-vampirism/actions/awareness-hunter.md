# awareness_hunter — Vampirism 1.10.13 · engenharia causal para perks

**Identidade:** `vampirism:awareness_hunter` · `de.teamlapen.vampirism.entity.player.hunter.actions.AwarenessHunterAction` · lasting / sensor de proximidade de vampiros.

**Proveniência:** `Vampirism-1.21-1.10.13.jar`, mod ID `vampirism`, SHA-1 instalado `349b6e4ea893c98a580775b1725399903e222228`; registry físico 19/19 ✅ [Java21 #38664546643](https://github.com/Gustavaopere/Black-Arcana/actions/runs/38664546643). Comportamento abaixo é **⚠️ SOURCE_CAUSALITY** do pin `TeamLapen/Vampirism@e1ed095713cef5e9eb151d0ee58908fa830d6bb7`, não equivalência binária integral, valores efetivos de config ou gameplay. `⛔` nenhum adapter per-caster aprovado.

## Eixos e limites de perk

| Eixo | Código verificado e implicação | Mutabilidade |
|---|---|---|
| Ingresso/compatibilidade | canBeUsedBy recusa execução simultânea com Hunter DISGUISE_HUNTER. activate retorna true sem observação imediata de uma entidade detectada. | ActionActivatedEvent pode alterar cooldown/duração e vetar, mas não certifica vampiro visível/detectado. |
| Targeting e área | Busca getNearestEntity(LivingEntity, TargetingConditions.forNonCombat com predicado da facção Vampire, AABB X/Z ±r, Y de −r+1 a +r+1), r=haAwarenessRadius default 25 (config 0..50). Distância usada é entre player e o alvo mais próximo, não dano nem seleção de ataque. | CONFIG_NATIVE raio global, mas ⛔ nenhum setter per-caster de raio, alvo ou facção comprovado. |
| Cálculo e sidedness | onUpdate executa a cada 8 ticks **somente client-side**, calcula intensidade 1−dist/r se encontrou vampiro e escreve HunterPlayer.specialAttributes.nearbyVampire(value); em ausência de alvo, valor 0. Com raio 0 permitido na config, fórmula deve ser revisada no runtime antes de adaptar. | Client state é apresentação/sensor; não autoriza Mastery ou gates server-side. |
| Duration/cooldown | getCooldown() retorna haAwarenessCooldown diretamente em TICKS (default 1); duration haAwarenessDuration default Integer.MAX_VALUE ticks. NÃO multiplicar por 20. | Event pode mutar timers; overlay/cleanup nativos. |
| Dano/projétil/recursos | Nenhum hurt, projectile, AOE de dano, status ofensivo ou blood debit neste action. | N/A attack damage/type/radius. Informar sensor não significa conversão de spell. |
| Fim | onDeactivated zera nearbyVampire(0), onActivatedClient e onReActivated chamam onUpdate. | Persistência e competição DisguiseHunter pendentes. |

## Localizadores

- [Source](https://github.com/TeamLapen/Vampirism/blob/e1ed095713cef5e9eb151d0ee58908fa830d6bb7/src/main/java/de/teamlapen/vampirism/entity/player/hunter/actions/AwarenessHunterAction.java#L16-L96)
- [Config](https://github.com/TeamLapen/Vampirism/blob/e1ed095713cef5e9eb151d0ee58908fa830d6bb7/src/main/java/de/teamlapen/vampirism/config/BalanceConfig.java#L292-L299)
- [ActionEvent — setters de cooldown/duração, veto](https://github.com/TeamLapen/Vampirism/blob/e1ed095713cef5e9eb151d0ee58908fa830d6bb7/src/api/java/de/teamlapen/vampirism/api/event/ActionEvent.java#L37-L78): evento pré-onActivated, não setter de raio/dano/target.

**QA obrigatório:** Testar zero radius, facções, alvos atrás de paredes, radar somente client, reconnect e desativação; excluir sensor client-side de procs server-only. Não duplicar casts, buffs/consumo nem autoridade da action. **+0 novas identidades; Stage 06.05 🟡; Stage 09 PENDING.**
