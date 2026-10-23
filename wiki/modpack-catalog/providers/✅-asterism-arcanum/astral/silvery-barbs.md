# Silvery Barbs

**Dossiê documental — 23/10/2026.** `technical_perk_dossier: 1`; identidade `COUNTED_EXACT`; lógica `SOURCE_PINNED / SOURCE_CAUSALITY`; integração `CONTRATO_CONDICIONAL`; QA físico `PENDING`. **+0 identidades**: Luck, tag, Glowing e cancelamentos são mecanismos da mesma spell.

## Identidade e proveniência

Provider Asterism Arcanum (`mod_id=asterismarcanum`), spell **`asterismarcanum:silvery_barbs`**, escola default Astral. Classe `com.birdie.asterismarcanum.spells.SilveryBarbsSpell`; consumer terminal `events.ServerEvents#livingIncomingDamageEvent`. Usa vanilla `minecraft:luck`, `minecraft:glowing` e tag de entidade `silvery_barbs_tag`, sem efeito registrado específico de shield. [Registry][registry], [spell][spell], [handler][handler].

JAR físico histórico #56 **`asterismarcanum-1.21.1-0.1.0.jar`**, SHA-1 `4a25ba80116168ddcc812f71467c0598127e774a`; [publisher8157080](https://www.curseforge.com/minecraft/mc-mods/asterism-arcanum/files/8157080) e [prova de registry/classe](../EXACT-0.1.0-BINARY-REGISTRY-AUDIT.md). Source oficial `BirdieVibes/Asterism-Arcanum@f1738c7813a85d31a6da10e6c9f2dbce18d2b583`, versão1.21.1-0.1.0, NeoForge21.1.215/Iron’s3.15.6; host consultado Iron’s3.16.3 `e4056af90302d37eb1739f5ff05020b020e6e252`. [Versões][versions]. Identidade exata não comprova todos os corpos de métodos source↔JAR/config efetiva. Polyform Shield: consulta/paráfrases/permalinks, sem importar implementação/assets. [Contratos comuns](../SPELL-PERK-BOUNDARIES-0.1.0.md).

[Guia oficial][description], parafraseado: proteção breve aplicada a aliados próximos de um ponto escolhido. A ficha descreve o consumer real de múltiplos eventos, sem prometer “próximo hit apenas”. Obtenção segue Astral Scroll/Astromancer e host/config, sem presumir config implantada ([loot][loot]).

## Ingresso e pipeline causal

1. INSTANT, Rare, níveis default1..5, sem precondição específica sobrescrita; wrapper jogador Iron’s possui admissão, eventos, mana/cooldown. onCast atribui **static radius=n+3**, constrói ray de eye até look normalizado×25, checkForBlocks(true), bbInflation0.25, e usa localização do hit/miss como centro. [Defaults][spell], [cast][cast], [host][host-cast].
2. Host RaycastBuilder clipa COLLIDER/Fluid.NONE e seleciona hit de entidade mais próximo antes do bloco/end. Predicate inicial Utils.canHitWithRaycast exige pickable/alive/!spectator; pode atingir entidade que não será beneficiada. A consulta de aliados posterior é separada da aquisição do centro. [Ray][ray], [predicate][ray-filter].
3. Consulta LivingEntity no **AABB center±r**, sem teste esférico de distância ou LOS de cada alvo ao centro. Aceita `target!=caster` e (`target.isAlliedTo(caster)` ou IMagicSummon cujo getSummoner()==caster por referência). Solicita Luck20ticks amp1 e depois grava tag mesmo se addEffect recusado; retornos não são examinados. Sem cap/ordenação explícitos. [Cast][cast].
4. Handler de incoming damage: se vítima tem **qualquer Luck** e tag, solicita Glowing10ticks amp1 e cancela evento; não verifica fonte, amount, ally, owner ou primeiro hit e **não consome tag**. Se tem tag mas não Luck, remove tag sem cancelar por esse ramo. Assim múltiplos hits podem ser cancelados na janela; outro Luck mais longo/externo pode sustentar a condição. Tag residual pode voltar a participar se houver Luck antes do próximo cleanup por dano. [Handler][handler].
5. `getUniqueInfo` chama getRadius apenas para leitura: **não muda radius no tooltip**. O campo static começa0 e é sobrescrito por casts de qualquer instância/caster; getters não recebem jogador/nível. Estado global não é contexto seguro por jogador. Não existe timer próprio de remoção da tag neste código; expiração/merge do Luck pertencem ao host. [Info][info], [campo/cast][cast], [getter][getter].

## Matriz de parâmetros e alteração por perks

`n`=nível recebido; defaults/fórmulas não são config implantada. P base2+1×(n−1) existe, mas não entra no raio/duração abaixo.

| Eixo | Valor / consumidor / fase | Boundary e mutabilidade | QA |
|---|---|---|---|
| Cast / mana / cooldown | INSTANT0; mana `int((25+5(n−1))×MANA_MULTIPLIER)`, neutro25..45; cooldown1s=20ticks, antes de modifiers. Sem recast próprio. [Defaults][spell], [host][host-cast]. | Config/eventos host **NATIVE/HOOK_VERIFICADO** genéricos, integração **CONDITIONAL**. Não cobrar por aliado ou dano cancelado; cooldown não é duração da tag. | Q1/Q2 |
| Alcance / aquisição | Ray25blocks do eye pelo olhar; blockcheck true, inflation0.25. Centro pode ser entity/block hit ou fim. [Cast][cast], [hostray][ray]. | Constantes locais, sem setter isolado por perk demonstrado. **⛔ SEM_HOOK_SEGURO** para range/aimassist seguro; mixins de outros mods exigem prova própria. | Q1/Q3 |
| Área / target | `r=n+3`, neutro4..8; cubo de lado2r, sem esfera/LOS por aliado, sem cap de targets. Exclui self; aceita allied/summonowner pelo teste literal. [Cast][cast]. | Mudar nível altera candidato r; native spell power não muda raio. Campo public static não é API per-player nem snapshot seguro. Single→AOE já é área e não libera expandir/filtros por heurística. | Q2/Q3 |
| Buff / duração / amp | Pedido Luck20ticks=1s, amp1 (II), depois tag. addEffect pode ser negado/mesclado; tag ainda é gravada. [Cast][cast]. | Constantes locais sem API específica. [Hook genérico MobEffectEvent.Applicable][effect-event] pode vetar Luck, mas não impede gravação da tag e não atribui cast causal completo; integração **CONDITIONAL**. | Q2/Q4 |
| Defesa / eventos / tipo | Cancela LivingIncomingDamageEvent se Luck+tag, sem teste de source/amount/contador; tenta Glowing10ticks=0.5s amp1. Não aplica dano, heal ou resistência numérica própria. [Handler][handler]. | API cancelável real usada pelo provider, mas não oferece setter de “charges”. Troca de DamageType/HP shield **N/A**; **⛔ SEM_HOOK_SEGURO** para substituição de resolver/consumo por hit. | Q2/Q4 |
| Estado / causalidade | Tag não consumida no cancelamento; limpeza apenas em evento sem Luck. Luck externo/merge pode ampliar janela; sem cast token/owner na tag. [Handler][handler]. | Não tratar tag como contador ou prova de sucesso de addEffect. Alterar duração genérica de Luck afeta outras origens e requer contrato, **CONDITIONAL**. | Q2/Q4/Q5 |
| Static / tooltip / sync | radius public static sem inicializador explícito; cast escreve n+3; getUniqueInfo/getRadius só leem, podem mostrar valor de outro cast ou0 inicial. [Info][info], [cast/getter][cast]. | Estado global, sem sync/config/actor key próprio. **⛔ SEM_HOOK_SEGURO** como knob per-player; não “corrigir” internals por observer. | Q1/Q5 |
| Projétil / hitbox / visual | Sem projétil/entidade de área persistente, speed/pierce/lifetime de projétil: **N/A**. Partículas no centro/alvos não determinam hitbox/proteção. [Cast][cast]. | Render/particles não ampliam área nem criam novas raízes. Sem hook de resize pertinente. | Q3/Q5 |
| Summons / mundo / custos extras | Não cria summon nem muda blocos/tickets/teleport/rollback; aceita summons existentes como alvos. Não paga stamina/vida por cancelamento localmente. [Cast][cast], [handler][handler]. | N/A count/AI/ownership de novos summons. Provider/host controlam buff/estado; não aplicar shield, heal ou recurso em paralelo. | Q4/Q5 |

## Autoria, concepção e pendências

RPG/Black Arcana não devem duplicar Luck/tag/cancelamento ou premiar cada incoming como novo cast. É necessário correlacionar cast/caster/alvo, instância real de efeito e evento; tag e Luck isolados não preservam autoria nem origem exclusiva. Enshrouded continua dono dos seus sistemas. Assinatura ocupada: buff coletivo breve com negação de eventos enquanto condição Luck+tag; visual/nome novo não constitui outra magia.

- **Q1:** fingerprint/config real, nível/modifiers, tooltip antes/depois e concorrência entre casters/sides, mana/cooldown.
- **Q2:** vários hits no mesmo tick/janela, amount0/ambiental/ownerless, cancelamentos de outros listeners, Luck recusado/externo/mais longo, tag residual/novo Luck.
- **Q3:** ray entidade/bloco/miss, range25/bordas/cantos do cubo, LOS entre centro/aliados, owner de summons e PvP/claims.
- **Q4:** refresh/merge/remoção de efeitos, Glow recusado, expiração sem novo dano, logout/morte e atribuição de prática/perks.
- **Q5:** persistência de tags/efeitos após save/restart, sync/multiplayer/Survival e coexistência. **PENDING**, sem adapter/perk/runtime novo nem Stage promovido.

[versions]: https://github.com/BirdieVibes/Asterism-Arcanum/blob/f1738c7813a85d31a6da10e6c9f2dbce18d2b583/gradle.properties#L9-L24
[registry]: https://github.com/BirdieVibes/Asterism-Arcanum/blob/f1738c7813a85d31a6da10e6c9f2dbce18d2b583/src/main/java/com/birdie/asterismarcanum/registries/ASARSpellRegistry.java#L68-L71
[spell]: https://github.com/BirdieVibes/Asterism-Arcanum/blob/f1738c7813a85d31a6da10e6c9f2dbce18d2b583/src/main/java/com/birdie/asterismarcanum/spells/SilveryBarbsSpell.java#L32-L55
[info]: https://github.com/BirdieVibes/Asterism-Arcanum/blob/f1738c7813a85d31a6da10e6c9f2dbce18d2b583/src/main/java/com/birdie/asterismarcanum/spells/SilveryBarbsSpell.java#L42-L46
[cast]: https://github.com/BirdieVibes/Asterism-Arcanum/blob/f1738c7813a85d31a6da10e6c9f2dbce18d2b583/src/main/java/com/birdie/asterismarcanum/spells/SilveryBarbsSpell.java#L77-L114
[getter]: https://github.com/BirdieVibes/Asterism-Arcanum/blob/f1738c7813a85d31a6da10e6c9f2dbce18d2b583/src/main/java/com/birdie/asterismarcanum/spells/SilveryBarbsSpell.java#L117-L119
[handler]: https://github.com/BirdieVibes/Asterism-Arcanum/blob/f1738c7813a85d31a6da10e6c9f2dbce18d2b583/src/main/java/com/birdie/asterismarcanum/events/ServerEvents.java#L50-L60
[description]: https://github.com/BirdieVibes/Asterism-Arcanum/blob/f1738c7813a85d31a6da10e6c9f2dbce18d2b583/src/main/resources/assets/asterismarcanum/lang/en_us.json#L32-L33
[loot]: https://github.com/BirdieVibes/Asterism-Arcanum/blob/f1738c7813a85d31a6da10e6c9f2dbce18d2b583/src/main/resources/data/asterismarcanum/loot_table/entities/astromancer.json#L1
[host-cast]: https://github.com/iron431/irons-spells-n-spellbooks/blob/e4056af90302d37eb1739f5ff05020b020e6e252/src/main/java/io/redspace/ironsspellbooks/api/spells/AbstractSpell.java#L160-L325
[ray]: https://github.com/iron431/irons-spells-n-spellbooks/blob/e4056af90302d37eb1739f5ff05020b020e6e252/src/main/java/io/redspace/ironsspellbooks/api/util/RaycastBuilder.java#L19-L124
[ray-filter]: https://github.com/iron431/irons-spells-n-spellbooks/blob/e4056af90302d37eb1739f5ff05020b020e6e252/src/main/java/io/redspace/ironsspellbooks/api/util/Utils.java#L459-L462

[effect-event]: https://github.com/neoforged/NeoForge/blob/e0e7ab5d273fdc034f23fee7bf91c61ae39d3019/src/main/java/net/neoforged/neoforge/event/entity/living/MobEffectEvent.java#L94-L161
