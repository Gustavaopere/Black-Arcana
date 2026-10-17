# half_invulnerable — Vampirism 1.10.13 · ficha causal para perks

**Identidade:** `vampirism:half_invulnerable`, provider `vampirism`; classificação lasting / defesa por mitigação condicional; classe `de.teamlapen.vampirism.entity.player.vampire.actions.HalfInvulnerableAction`. **✅ COUNTED_EXACT somente no registry compilado** [#38664546643](https://github.com/Gustavaopere/Black-Arcana/actions/runs/38664546643), **⚠️ SOURCE_CAUSALITY para corpo**, **⛔ adapter e gameplay não homologados**. JAR instalado `Vampirism-1.21-1.10.13.jar`, SHA-1 `349b6e4ea893c98a580775b1725399903e222228`. Source pin `TeamLapen/Vampirism@e1ed095713cef5e9eb151d0ee58908fa830d6bb7`; todos os números são defaults ou constantes do source, não configuração medida no modpack.

Ativa estado defensivo que pode interceptar dano elevado e cobrar blood somente na tentativa de bloqueio.

## Matriz de parâmetros e causalidade

| Eixo | Prova verificada no código exato | Estado de perk |
|---|---|---|
| Ativação/efeito | activate define specialAttributes.half_invulnerable=true, aplica MOVEMENT_SLOWDOWN por 22 ticks amplifier 1; onUpdate renova de 20 em 20 ticks no servidor; ao desativar limpa flag e efeito. | Duração/cooldown: ActionActivatedEvent; não confundir slowness com projectile size ou dano. |
| Duração | vaHalfInvulnerableCooldown default 60 segundos (1200 ticks); duration default 30 segundos (600 ticks). ActionUpdated/Deactivated do provider governa timer e reset. | Hook para duração e cooldown SOURCE-VERIFIED; não alterar via cliente. |
| Gatilho/custo de sangue | VampirePlayer damage path: se specialAttributes.half_invulnerable e amt >= maxHealth × vaHalfInvulnerableThreshold(default 0.4) × modificador de refinement (quando equipado) **e amt < 999**, tenta useBlood(vaHalfInvulnerableBloodCost, false), default 4 blood units; se falhar desativa action. | Custo é DEFERRED ON QUALIFYING HIT, não na ativação. ⛔ debitar 4 no cast ou por tick. |
| Resultado/limites | Uso de blood bem-sucedido retorna true no caminho de interceptação; se insuficiente, o fluxo não bloqueia por essa ação. Não há garantia de compensação ou proteção universal para sources injetadas por terceiros. | Observação de resultado final de dano exige test de compatibilidade, i-frames e ordem de eventos. |
| Target/área/projétil | Somente o próprio jogador; sem AOE, projétil ou DamageType criado neste corpo. | N/A para range/aoe/hitbox e mudança de damage type; foco em timing e valores de blood. |
| Deduplicação | Uma ativação pode interceptar mais de um hit; cada pagamento liga-se ao hit elegível, não a novo cast. ActionActivatedEvent é pré-sucesso. | Mastery no cast apenas com estado confirmado; bloqueios têm identidade de evento de dano separada e bounded. |

## Implementação e evidências

- [Action source](https://github.com/TeamLapen/Vampirism/blob/e1ed095713cef5e9eb151d0ee58908fa830d6bb7/src/main/java/de/teamlapen/vampirism/src/main/java/de/teamlapen/vampirism/entity/player/vampire/actions/HalfInvulnerableAction.java#L13-L77).
- [Damage settlement](https://github.com/TeamLapen/Vampirism/blob/e1ed095713cef5e9eb151d0ee58908fa830d6bb7/src/main/java/de/teamlapen/vampirism/src/main/java/de/teamlapen/vampirism/entity/player/vampire/VampirePlayer.java#L650-L668).
- [Defaults](https://github.com/TeamLapen/Vampirism/blob/e1ed095713cef5e9eb151d0ee58908fa830d6bb7/src/main/java/de/teamlapen/vampirism/src/main/java/de/teamlapen/vampirism/config/BalanceConfig.java#L418-L422).
- [ActionEvent API pública](https://github.com/TeamLapen/Vampirism/blob/e1ed095713cef5e9eb151d0ee58908fa830d6bb7/src/main/java/de/teamlapen/vampirism/src/api/java/de/teamlapen/vampirism/api/event/ActionEvent.java#L37-L78): `ActionActivatedEvent` cancelável e com `setCooldown(int)`/`setDuration(int)`, **antes de** `onActivated`. Nenhum setter de área/dano/target consta nesse evento.

**QA bloqueante:** Testar dano menor/exato/acima do threshold, amt>=999, hearts buffs, blood suficiente/insuficiente, hit repetido, outro mod cancelando, reconexão, slowness removal e DoubleCharge=false. **Sem merge de runtime, sem projeção de hooks externos, sem nova identidade semântica.**
