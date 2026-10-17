# bat — Vampirism 1.10.13 · ficha causal para perks

**Identidade:** `vampirism:bat`, provider `vampirism`; classificação lasting / transformação e voo; classe `de.teamlapen.vampirism.entity.player.vampire.actions.BatVampireAction`. **✅ COUNTED_EXACT somente no registry compilado** [#38664546643](https://github.com/Gustavaopere/Black-Arcana/actions/runs/38664546643), **⚠️ SOURCE_CAUSALITY para corpo**, **⛔ adapter e gameplay não homologados**. JAR instalado `Vampirism-1.21-1.10.13.jar`, SHA-1 `349b6e4ea893c98a580775b1725399903e222228`. Source pin `TeamLapen/Vampirism@e1ed095713cef5e9eb151d0ee58908fa830d6bb7`; todos os números são defaults ou constantes do source, não configuração medida no modpack.

Transformação em morcego com dimensão física, voo e modificadores de atributos geridos pelo Vampirism.

## Matriz de parâmetros e causalidade

| Eixo | Prova verificada no código exato | Estado de perk |
|---|---|---|
| Admissão/condições | canBeUsedBy recusa sun damage, guarda-chuva na mão, garlic damage, Rage ativa, água, dimensões da blacklist e veículos. ActionHandler é autoridade de unlock, cooldown, permission e veto. | Veto e cooldown/duração via ActionActivatedEvent SOURCE-VERIFIED; alterar condições de elegibilidade por perk é ⛔. |
| Geometria/movimento | BAT_SIZE = EntityDimensions.fixed(0.6,0.6), olho 0.51; updatePlayer usa forced pose/refreshDimensions e eleva Y por 1.8−0.6=1.2 no ingresso. A física de voo e colisão usa Minecraft/NeoForge e hooks auxiliares não reproduzidos aqui. | Alterar tamanho ou flight collision externamente: ⛔ sem seam. As dimensões de modelo são distintas de range de ataque. |
| Atributos | setModifier aplica AttributeModifier identificado pela action: ARMOR e ARMOR_TOUGHNESS −1 ADD_MULTIPLIED_TOTAL, NeoForgeMod.CREATIVE_FLIGHT +1 ADD_VALUE; flight speed da ability = vaBatFlightSpeed default 0.025, restabelece 0.05 ao sair. | Native attributes provider-owned; RPG não deve sobrescrever o modifier nem reexecutar setModifier. |
| Duração/custos | vaBatCooldown default 0s e código soma +1 tick; duração default enorme é clamp de segundos 10..(Integer.MAX_VALUE/20−1) convertido para ticks. onUpdate cobra vaBatExhaustion default 0.005 via addExhaustion enquanto elegível, sem useBlood direto. | Cooldown/duração no evento de action; blood/exhaustion provider-owned, ⛔ cobrança paralela. |
| Deactivation/persistência | Ao desativar, remove modifiers, restaura dimensões, remove attachment VAMPIRE_BAT; se fora do chão, aplica resistência 20 ticks, amplifier 5. Reactivation reconcilia flags/modifiers. | Lifecycle precisa QA relog/respawn e Epic Fight; não concluir que dimensão e stamina de todos os mods foram homologadas. |
| Dano/projétil/área | A action não emite projétil nem executa hurt no caminho analisado; voo e movimentação não são AOE ou tipo de dano. | N/A damageType/radius/projectile multiplier; Mastery por transformação única, não por update tick. |

## Implementação e evidências

- [Vampire action](https://github.com/TeamLapen/Vampirism/blob/e1ed095713cef5e9eb151d0ee58908fa830d6bb7/src/main/java/de/teamlapen/vampirism/entity/player/vampire/actions/BatVampireAction.java#L34-L185).
- [Defaults](https://github.com/TeamLapen/Vampirism/blob/e1ed095713cef5e9eb151d0ee58908fa830d6bb7/src/main/java/de/teamlapen/vampirism/config/BalanceConfig.java#L402-L408).
- [ActionEvent API pública](https://github.com/TeamLapen/Vampirism/blob/e1ed095713cef5e9eb151d0ee58908fa830d6bb7/src/api/java/de/teamlapen/vampirism/api/event/ActionEvent.java#L37-L78): `ActionActivatedEvent` cancelável e com `setCooldown(int)`/`setDuration(int)`, **antes de** `onActivated`. Nenhum setter de área/dano/target consta nesse evento.

**QA bloqueante:** Testar client, respawn, logged-in real, mudança de dimensão, sol/garlic, modpack com Epic Fight, voo/stamina, estado de armadura, exaustão→blood, ativação simultânea e restauração de atributos. **Sem merge de runtime, sem projeção de hooks externos, sem nova identidade semântica.**
