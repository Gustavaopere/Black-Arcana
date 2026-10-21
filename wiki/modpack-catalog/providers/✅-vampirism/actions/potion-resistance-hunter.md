# potion_resistance_hunter — Vampirism 1.10.13 · engenharia causal para perks

**Identidade:** `vampirism:potion_resistance_hunter` · `de.teamlapen.vampirism.entity.player.hunter.actions.PotionResistanceHunterAction` · lasting / remoção seletiva de efeitos.

**Proveniência:** `Vampirism-1.21-1.10.13.jar`, mod ID `vampirism`, SHA-1 instalado `349b6e4ea893c98a580775b1725399903e222228`; registry físico 19/19 ✅ [Java21 #38664546643](https://github.com/Gustavaopere/Black-Arcana/actions/runs/38664546643). Comportamento abaixo é **⚠️ SOURCE_CAUSALITY** do pin `TeamLapen/Vampirism@e1ed095713cef5e9eb151d0ee58908fa830d6bb7`, não equivalência binária integral, valores efetivos de config ou gameplay. `⛔` nenhum adapter per-caster aprovado.

## Eixos e limites de perk

| Eixo | Código verificado e implicação | Mutabilidade |
|---|---|---|
| Gate/duração | getCooldown() lê haPotionResistanceCooldown default 1200 TICKS; duration lê haPotionResistanceDuration default 400 TICKS; sem conversão por 20 nos métodos. | ActionActivatedEvent muta cooldown/duração; não fornece setter de predicado/tag. |
| Target e filtros | Self: shouldRemove(Holder<MobEffect>) retorna effect.is(ModTags.Effects.HUNTER_POTION_RESISTANCE); apenas MobEffects com a **tag provider** entram na remoção; não é imunidade universal a todos os efeitos. | CONFIG_NATIVE tag/datapack, adaptação per-skill sem filtro provider autenticado ⛔. |
| Fase e periodicidade | onUpdate aplica remoção quando !(player.tickCount % 3 == 0), ou seja, nos ticks com restos 1 ou 2; activate chama onUpdate imediatamente; onActivatedClient/onReActivated também chamam onUpdate. | Importante: NÃO normalizar para uma vez a cada 3 ticks. Inspecionar sidedness e side effects concretos do effect removal. |
| Resultado | Remove efeitos correspondentes via removeEffect; a action retorna true mesmo se não existir qualquer efeito para remover. A estatística de activation não prova efeito neutralizado. | Mastery por *remoção bem-sucedida* exige observar delta de MobEffects, não só ActionActivatedEvent. |
| Dano/área | Não possui projectile, dano/elemento, área de combate, expansão de hitbox ou target entity. | N/A dano e alcance. Nenhum custo de blood local. |

## Localizadores

- [Source](https://github.com/TeamLapen/Vampirism/blob/e1ed095713cef5e9eb151d0ee58908fa830d6bb7/src/main/java/de/teamlapen/vampirism/entity/player/hunter/actions/PotionResistanceHunterAction.java#L17-L76)
- [Config](https://github.com/TeamLapen/Vampirism/blob/e1ed095713cef5e9eb151d0ee58908fa830d6bb7/src/main/java/de/teamlapen/vampirism/config/BalanceConfig.java#L299-L301)
- [ActionEvent — setters de cooldown/duração, veto](https://github.com/TeamLapen/Vampirism/blob/e1ed095713cef5e9eb151d0ee58908fa830d6bb7/src/api/java/de/teamlapen/vampirism/api/event/ActionEvent.java#L37-L78): evento pré-onActivated, não setter de raio/dano/target.

**QA obrigatório:** Testar dois efeitos tagueados e não tagueados, 3 fases de tick, status adicionado no mesmo tick, duration 400, cooldown 1200, amplificadores e reação com outro mod. Não duplicar casts, buffs/consumo nem autoridade da action. **+0 novas identidades; Stage 06.05 🟡; Stage 09 PENDING.**
