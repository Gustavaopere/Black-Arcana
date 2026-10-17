# disguise_hunter — Vampirism 1.10.13 · engenharia causal para perks

**Identidade:** `vampirism:disguise_hunter` · `de.teamlapen.vampirism.entity.player.hunter.actions.DisguiseHunterAction` · lasting / ocultação Hunter.

**Proveniência:** `Vampirism-1.21-1.10.13.jar`, mod ID `vampirism`, SHA-1 instalado `349b6e4ea893c98a580775b1725399903e222228`; registry físico 19/19 ✅ [Java21 #38664546643](https://github.com/Gustavaopere/Black-Arcana/actions/runs/38664546643). Comportamento abaixo é **⚠️ SOURCE_CAUSALITY** do pin `TeamLapen/Vampirism@e1ed095713cef5e9eb151d0ee58908fa830d6bb7`, não equivalência binária integral, valores efetivos de config ou gameplay. `⛔` nenhum adapter per-caster aprovado.

## Eixos e limites de perk

| Eixo | Código verificado e implicação | Mutabilidade |
|---|---|---|
| Ingresso | activate chama HunterPlayer.specialAttributes.activateDisguise() e retorna true; canBeUsedBy exige que AwarenessHunter não esteja ativa. | Mutação de atributos nativos pertence ao provider; não é equivalente a invisibilidade vanilla. |
| Fade/tempo | Constante FADE_TICKS=20; onUpdate chama specialAttributes.increaseDisguiseTicks() a cada atualização do handler. getCooldown()=0, getDuration()=Integer.MAX_VALUE (ticks), sem leitura de config de tempo. | ActionActivatedEvent permite timer, mas alterar fade exige hook interno NÃO VERIFICADO. |
| Visibilidade | BalanceConfig.haDisguiseVisibilityMod default 0.2 multiplica detecção de mobs; haDisguiseInvisibleSQ default 256 é distância ao quadrado para invisibilidade contextual. **Não** são 256 blocos de alcance nem raio de magias; fórmula downstream de detecção ainda requer verificação. | CONFIG_NATIVE para tuning global, sem per-player adapter homologado. |
| Lifecycle | onActivatedClient e onReActivated restabelecem disfarce; onDeactivated resetDisguise; isEnabled depende de haDisguiseEnabled. | Conflito com Awareness, IA de facção e server/client devem QA. |
| Target/dano | Self; nenhum projétil, AOE de impacto, raycast, DamageType ou sangue debitado na action. | N/A dano ou conversion para stealth ofensivo. |

## Localizadores

- [Source](https://github.com/TeamLapen/Vampirism/blob/e1ed095713cef5e9eb151d0ee58908fa830d6bb7/src/main/java/de/teamlapen/vampirism/entity/player/hunter/actions/DisguiseHunterAction.java#L14-L75)
- [Config](https://github.com/TeamLapen/Vampirism/blob/e1ed095713cef5e9eb151d0ee58908fa830d6bb7/src/main/java/de/teamlapen/vampirism/config/BalanceConfig.java#L292-L294)
- [ActionEvent — setters de cooldown/duração, veto](https://github.com/TeamLapen/Vampirism/blob/e1ed095713cef5e9eb151d0ee58908fa830d6bb7/src/api/java/de/teamlapen/vampirism/api/event/ActionEvent.java#L37-L78): evento pré-onActivated, não setter de raio/dano/target.

**QA obrigatório:** Testar visibilidade de mobs, picos de detecção, fade 20, pós-reload, AI owner, toggle simultâneo com Awareness e restauração após morte. Não duplicar casts, buffs/consumo nem autoridade da action. **+0 novas identidades; Stage 06.05 🟡; Stage 09 PENDING.**
