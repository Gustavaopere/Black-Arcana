# regen — Vampirism 1.10.13 · ficha causal para perks

**Identidade:** `vampirism:regen`, provider `vampirism`; classificação lasting / regeneração; classe `de.teamlapen.vampirism.entity.player.vampire.actions.RegenVampireAction`. **✅ COUNTED_EXACT somente no registry compilado** [#38664546643](https://github.com/Gustavaopere/Black-Arcana/actions/runs/38664546643), **⚠️ SOURCE_CAUSALITY para corpo**, **⛔ adapter e gameplay não homologados**. JAR instalado `Vampirism-1.21-1.10.13.jar`, SHA-1 `349b6e4ea893c98a580775b1725399903e222228`. Source pin `TeamLapen/Vampirism@e1ed095713cef5e9eb151d0ee58908fa830d6bb7`; todos os números são defaults ou constantes do source, não configuração medida no modpack.

Aplica continuamente efeito vanilla Regeneration, com amplifier condicionado ao refinement nativo.

## Matriz de parâmetros e causalidade

| Eixo | Prova verificada no código exato | Estado de perk |
|---|---|---|
| Ingresso | activate chama applyEffect e retorna true; ActionHandler gerencia timer e as gates de uso. | Event hook na admissão para cooldown/duração e veto; não mede cura efetiva. |
| Tempo | vaRegenerationCooldown default 60s (1200 ticks) e Duration default 20s (400 ticks). onUpdate no servidor a cada tickCount%50==0 renova o buff de 52 ticks. | O efeito não cura a cada update; cada tick real de regeneração vem da mecânica vanilla. Não fazer proc repetido por efeito reaplicado. |
| Efeito/magnitude | MobEffects.REGENERATION por 52 ticks, amplifier 0 normalmente e amplifier 1 se ModRefinements.REGENERATION equipado; efeitos substituídos/mascarados por outros mods podem ter prioridades não verificadas. | CONFIG_NATIVE tempo; amplificador selecionado pelo provider, per-player diferente de event setDuration. |
| Fim | onDeactivated remove MobEffects.REGENERATION (sem token de dono visível nesse corpo). Persistência e conflito com potion effects de terceiros requerem QA. | Não assumir remoção seletiva de apenas um source. |
| Alvos/dano/projétil | Self, sem hitbox, range, targeting, DamageType, projectile ou heal direto; HP settlement é downstream. | Não creditar Mastery por buff ou por todo heal sem fonte rastreada. |
| Recurso | Sem cobrança direta de blood no corpo da action. | Não inventar custo de blood. |

## Implementação e evidências

- [Action source](https://github.com/TeamLapen/Vampirism/blob/e1ed095713cef5e9eb151d0ee58908fa830d6bb7/src/main/java/de/teamlapen/vampirism/src/main/java/de/teamlapen/vampirism/entity/player/vampire/actions/RegenVampireAction.java#L14-L72).
- [Default](https://github.com/TeamLapen/Vampirism/blob/e1ed095713cef5e9eb151d0ee58908fa830d6bb7/src/main/java/de/teamlapen/vampirism/src/main/java/de/teamlapen/vampirism/config/BalanceConfig.java#L389-L391).
- [ActionEvent API pública](https://github.com/TeamLapen/Vampirism/blob/e1ed095713cef5e9eb151d0ee58908fa830d6bb7/src/main/java/de/teamlapen/vampirism/src/api/java/de/teamlapen/vampirism/api/event/ActionEvent.java#L37-L78): `ActionActivatedEvent` cancelável e com `setCooldown(int)`/`setDuration(int)`, **antes de** `onActivated`. Nenhum setter de área/dano/target consta nesse evento.

**QA bloqueante:** QA procs de regeneração, HP cheio, cancelamento, interferência com potions de outros mods, damage vs heal, refund, duration e auto reactivation. **Sem merge de runtime, sem projeção de hooks externos, sem nova identidade semântica.**
