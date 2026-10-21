# Moving Spell Turrets

State: `SOURCE-PINNED 5.4.0 / RUNTIME QA PENDING`

Ars Creo registers Create behavior on existing Ars Nouveau Basic, Timer and Enchanted Spell Turrets.

- Basic: server-side interaction with the moving actor invokes the shared cast path.
- Timer: positive stored `time` triggers when server game time is divisible by that interval.
- Enchanted: invokes the shared cast path when the moving actor visits a new block position.

The shared cast path decodes Ars spell data, uses Ars resolver/context, charges Source on the contraption first and falls back to nearby Ars Source. Projectile velocity incorporates contraption rotation/motion; Touch uses the provider's moving position/facing logic.

The wrapped caster reports Ars `CasterType.OTHER`; there is no source-supported player Mastery attribution contract here.

Rotating Turret appears in Display Source registration but not in the exact movement-behavior registration list, so moving-cast support for it is not claimed.

Black Arcana must observe this as one provider causal action and never double-settle it.

## Engenharia causal para perks — 17/10/2026

**Proveniência:** mod ID `ars_creo`, JAR instalado documentado `ars_creo-1.21.1-5.4.0.jar`, SHA-1 `22a6afd4fbe76354acc9c1ba076c89a94d120d94`. Código da versão `5.4.0`: `baileyholl/Ars-Creo@6a99d36fab441653478fc49de8f28164f0894eb2` (**SOURCE_CAUSALITY**, sem equivalência binária completa nem QA do pack). Hosts: Ars Nouveau `5.13.1`, Create `6.0.10`. **Ars Creo não registra glyph próprio: +0 IDs novos.**

**Torres mágicas móveis — casting e Source** — efeito do provider externo/integração Create, não nova raiz mágica.

| Eixo | Mecanismo no source pinado | Limite de perk |
|---|---|---|
| Gatilhos e side | Basic: handlePlayerInteraction executa `castSpell` server-side; Timer: `ticksToSignal=context.blockEntityData.getInt("time")`, deve ser positivo e `getGameTime()%ticksToSignal==0`; Enhanced: `visitNewPosition` server-side; Rotating somente registrado como Display Source, não comportamento móvel de cast. | Não criar cron/segundo cast; cooldown real é provider/actor, não timer de RPG. |
| Identidade / caster | Decodifica `spell_caster` NBT via `ANCodecs`; invalidez de `spell.isValid()` aborta. Usa `ANFakePlayer` no `SpellContext` com `ContraptionCaster` e `CasterType.OTHER`; o projétil criado tem owner `FakePlayerFactory.getMinecraft(world)`, distinto do `ANFakePlayer` usado no contexto. | Sem correspondência garantida entre dois FakePlayers e jogador real. Mastery atribuída por proximidade/interação: ⛔. |
| Custo/ordem | Antes de resolver, chama `removeSourceFromContraption(context, spell.getCost(),pos)`; se insuficiente, verifica e debita via `SourceUtil` alcance **6**. Havendo Creative Source Jar, o caminho local retorna true sem debitar. `ContraptionCaster.expendMana` é **no-op**. | Custo único em Source, não Ars mana; não fazer segundo débito/refund ou criar recurso do Black Arcana. |
| Tipo/efeito | Após custo, o método emite projétil apenas se `resolver.castType instanceof MethodProjectile`, ou executa `onCastOnBlock` se `MethodTouch`. **Outros castType não têm branch de efeito nem refund no método examinado**, embora Source já possa ter sido consumido. | ⚠️ QA de perda de Source em tipo não suportado; não inventar fallback para completar conjuração. |
| Geometria/projétil | Direção básica do bloco rotacionada por `context.rotation.apply`; vetor efetivo = facing×**0.5** + `context.motion`; posição = centro do bloco + facing×**0.7**; `EntityProjectileSpell.shoot(vx,vy,vz,0.4f,0)`. Não há setter per-player de hitbox, dano, AOE ou DamageType. | ⛔ perks de velocidade/target/range ou multiplicação sem seam de Ars/Create e medição de física. |
| Lifecycle | O chamado a `world.addFreshEntity` não é verificado quanto ao retorno; a interação Basic retorna true mesmo se `castSpell` abortou. Source debitado não é prova de spawn aceito. | Progressão só pós-evento causal de cast/hit, com idempotência e owner autenticado. |

**Âncoras verificáveis:** [BasicTurretBehavior.java](https://github.com/baileyholl/Ars-Creo/blob/6a99d36fab441653478fc49de8f28164f0894eb2/src/main/java/com/hollingsworth/ars_creo/contraption/BasicTurretBehavior.java#L14-L38) · [TimerTurretBehavior.java](https://github.com/baileyholl/Ars-Creo/blob/6a99d36fab441653478fc49de8f28164f0894eb2/src/main/java/com/hollingsworth/ars_creo/contraption/TimerTurretBehavior.java#L9-L16) · [EnhancedTurretBehavior.java](https://github.com/baileyholl/Ars-Creo/blob/6a99d36fab441653478fc49de8f28164f0894eb2/src/main/java/com/hollingsworth/ars_creo/contraption/EnhancedTurretBehavior.java#L7-L13) · [ITurretBehavior.java](https://github.com/baileyholl/Ars-Creo/blob/6a99d36fab441653478fc49de8f28164f0894eb2/src/main/java/com/hollingsworth/ars_creo/contraption/ITurretBehavior.java#L26-L80) · [ContraptionCaster.java](https://github.com/baileyholl/Ars-Creo/blob/6a99d36fab441653478fc49de8f28164f0894eb2/src/main/java/com/hollingsworth/ars_creo/contraption/ContraptionCaster.java#L16-L36) · [ContraptionUtils.java](https://github.com/baileyholl/Ars-Creo/blob/6a99d36fab441653478fc49de8f28164f0894eb2/src/main/java/com/hollingsworth/ars_creo/contraption/ContraptionUtils.java#L18-L39).

**Aceitação pendente:** Servidor dedicado com Actor parado/móvel e `time=0/1/N`, Source de um ou vários jars, Source externo a 6 blocos, creative source, MethodProjectile/MethodTouch/outros métodos, dois FakePlayers, permissão/claims, falha de spawn e ownership após reinício. O RPG Skill Tree não controla o runtime Ars/Create. **0 adapters homologados, +0 IDs de magia.**
