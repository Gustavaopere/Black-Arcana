# Astral Gateway

**Dossiê documental — 23/10/2026.** `technical_perk_dossier: 1`; registro binário confirmado; identidade **CONDITIONAL / OUTSIDE STRICT**, publisher **UNFINISHED / CREATIVE-ONLY**; lógica `SOURCE_PINNED / SOURCE_CAUSALITY`; integração e QA físico **PENDING**. A ficha não habilita aquisição Survival, perk ou runtime. **+0 identidades**.

## Identidade e proveniência

Provider Asterism Arcanum (`mod_id=asterismarcanum`); spell **`asterismarcanum:astral_gateway`**, escola default Astral, Legendary, nível default1. Classe `com.birdie.asterismarcanum.spells.AstralGatewaySpell`; dimensão `asterismarcanum:astral_sea` de `AstralSeaManager`. [Registry][registry], [spell/defaults][spell], [dimensão-chave][sea]. Filho visual: TargetedAreaEntity do Iron’s, sem novo portal/bloco ou summon registrado por esta spell.

Artefato histórico #56 `asterismarcanum-1.21.1-0.1.0.jar`, SHA-1 `4a25ba80116168ddcc812f71467c0598127e774a`; [publisher 8157080](https://www.curseforge.com/minecraft/mc-mods/asterism-arcanum/files/8157080) descreve recurso inacabado/creative-only. A [prova exata de registry/override](../EXACT-0.1.0-BINARY-REGISTRY-AUDIT.md) não equivale à execução. Source oficial `BirdieVibes/Asterism-Arcanum@f1738c7813a85d31a6da10e6c9f2dbce18d2b583`, versão1.21.1-0.1.0, NeoForge 21.1.215/Iron’s 3.15.6; host consultado Iron’s 3.16.3 `e4056af90302d37eb1739f5ff05020b020e6e252`. [Versões][versions]. Polyform Shield: resumos/referências, sem importar implementação/assets. Corpos source↔JAR e configuração implantada não foram equiparados.

## Aquisição, admissão e ordem causal

A release não apoia Survival. Porém ausência de allowLooting/allowCrafting/isEnabled/canBeCraftedBy overrides e de host-config embutida não prova bloqueio efetivo: escola Astral tem defaults lootáveis; quality do Astromancer não exclui Legendary. [Auditoria do host](../IRONS-3.16.3-HOST-LOOT-ELIGIBILITY.md) e [checklist implantado](../SURVIVAL-CLOSURE-CHECKLIST.md) mantêm Gateway fora do strict até evidência autorizada. Não criar loot, recipe ou desbloqueio por perk para contornar isso.

1. `checkPreCastConditions` aceita somente **ServerPlayer**; não exige isCreative nem testa terreno, claims, whitelist de dimensão ou presença do level de destino. Wrapper Iron’s adiciona seus gates de custo/cooldown/eventos. [Precondição][pre], [host][host-cast].
2. LONG, castTime40ticks=2s. Override de `getEffectiveCastTime` retorna40 literal, ignorando CAST_TIME_REDUCTION. Custo default300 mana, cooldown60s. No wrapper jogador, SpellOnCastEvent/débito precedem onCast; nenhum refund por falha de dimensão demonstrado. [Defaults][spell], [tempo/precondição][pre], [host][host-cast].
3. `onServerPreCast` cria marker no caster com radius8/cor180609 e guarda TargetAreaCastData. O empty serializable declarado é SerializedTargetData, mas o cast não lê um alvo dele: o alvo de movimento continua o caster. Cleanup do marker é delegado ao EntityCastData/host, não há cleanup paralelo BA. [Pré-cast][precast], [data/reset][data].
4. `onCast` consulta LivingEntity no **cubo±8** centrado no caster, sem filtro de equipe/alive/claim no predicate local. Para cada alvo da lista original, testa **caster.distanceTo(target)≤8**; se caster é ServerPlayer, envia partículas na posição do target e muda dimensão do **próprio caster**, não do target. Inclui self na consulta; sem cap/ordenação/dedup explícitos. Mudanças de posição/dimensão do caster alteram os testes posteriores enquanto a lista permanece a original. Não prometer um transporte por cast ou portal de grupo. [Loop][cast].
5. Se já está no Astral Sea, calcula `findRespawnPositionAndUseSpawnBlock(true,DO_NOTHING)`, publica **PlayerRespawnPositionEvent(...,false)** e usa a DimensionTransition devolvida. É destino de respawn do host, não posição original guardada pelo addon. Se está fora, pede level Astral Sea ao servidor e cria transition para **(X_atual,64,Z_atual)**, delta ZERO, com **getXRot nos dois argumentos de rotação** e DO_NOTHING. Não há validação local de level não-null, colisão/loaded-chunk/worldborder ou chegada. Return de changeDimension é ignorado; som/super seguem após o loop. [Loop][cast], [chave][sea], [dados da dimensão][dimension].

## Matriz de parâmetros para perks

| Eixo | Valor / consumidor / fase | Boundary e mutabilidade | QA |
|---|---|---|---|
| Cast / duração / recast | LONG40ticks fixos; override ignora redução de tempo. Cooldown60s=1200ticks antes dos modifiers de cooldown; recast próprio0 herdado. [Spell][spell], [override][pre]. | Config cooldown e evento do host são **NATIVE/HOOK_VERIFICADO** nesse caminho; castTime literal **⛔ SEM_HOOK_SEGURO** para bônus genérico CAST_TIME_REDUCTION. Não existe portal temporizado pelo radius. | Q1/Q2 |
| Mana / power | `(int)(300×MANA_MULTIPLIER)`; baseSpellPower/perLevel0, sem fórmula de dano ou raio por P. [Defaults][spell], [host][host-cast]. | Config/evento pré-débito **NATIVE/HOOK_VERIFICADO**, integração **CONDITIONAL**; aumentar Astral power não demonstra alterar radius, duração ou destino. Sem recurso/segunda cobrança por target. | Q1/Q2 |
| Área / targeting | Consulta cubo±8, filtro distância≤8 reavaliado contra caster móvel; movimento sempre no ServerPlayer caster. Marker visual também radius8. [Precast][precast], [loop][cast]. | Radius public static **final**8, sem setter. Não é AOE de transporte de terceiros. **⛔ SEM_HOOK_SEGURO** para single→grupo, expandir área ou filtros próprios. | Q2/Q3 |
| Entrada de dimensão | Key `asterismarcanum:astral_sea`; X/Z do caster no momento, Y64, delta0, XRot duplicado nos campos de rotação. [Transition][cast], [manager][sea]. | Não usa Utils.handleSpellTeleport nem SpellTeleportEvent no caminho inspecionado. Destino/collision/claims **⛔ SEM_HOOK_SEGURO** por essa API de spell-teleport. | Q2/Q3 |
| Saída / retorno | Respawn transition + PlayerRespawnPositionEvent manual; flag false literal. Não grava âncora de retorno do cast. [Saída][cast]. | Host NeoForge oferece setDimensionTransition/setRespawnLevel, sem ICancellableEvent nesse evento; **HOOK_VERIFICADO** genérico apenas para essa fase, contrato do Gateway **CONDITIONAL** e survival continua fechado. [Prova comum](../SPELL-PERK-BOUNDARIES-0.1.0.md). | Q2/Q3 |
| Multiplicidade / orçamento | Uma consulta/lista; até uma tentativa por item elegível no foreach, sem cap local de entidades. Posição/dimensão corrente decide ramo a cada passagem. [Cast][cast]. | Não confundir número de targets com número transportado; somente caster. Não duplicar teleport para “corrigir” a intenção do comentário. **⛔ SEM_HOOK_SEGURO** para setter de budget. | Q3/Q4 |
| Entidade / projétil / hitbox | Marker TargetedAreaEntity é apresentação e cast data; nenhum projétil de dano, velocidade/pierce, summon com AI ou portal físico: **N/A**. [Precast][precast], [data][data]. | Radius visual não é hitbox nem prova de área segura. Cleanup/reset do host **CONDITIONAL** quando há mudança de dimensão/erro. | Q2/Q4 |
| Dano / cura / status / mundo | Não chama hurt/heal nem aplica buff próprio; troca de dimensão e uso do destino de respawn são consequências reais. [Cast][cast]. | Dano/tipo/cura **N/A**. Não oferecer bridge de dano, geração de terreno, ticket ou rollback BA por afinidade Astral. | Q3/Q4 |
| Movimento na dimensão | [ServerEvents][dimension-motion] retorna SUCCESS em PlayerSwimEvent no Astral Sea; EntityJoinLevelEvent liga noGravity/tag para não-player que chega com flagfalse, e remove ao chegar fora se tagueado. | Não é MobEffect ou dano do cast. Estado dimensional pode condicionar trajetória dos projéteis; API de voo, velocidade e interação com Expandability **CONDITIONAL**. | Q3/Q4 |
| Ownership / persistência | Caster ServerPlayer; sem SavedData de âncora, lista de passageiros persistida ou transação por cast no addon. Key/level pertencem ao provider/Minecraft. [Cast][cast], [manager][sea]. | Não implementar segunda dimensão/return-anchor/owner map. `changeDimension` ignorado não comprova sucesso; progressão não pode premiar chegada por SpellOnCastEvent. | Q4/Q5 |

## Deduplicação, concepção e pendências

Asterism/Iron’s/Minecraft possuem marker, casting e transição. RPG é dono da sua progressão; Black Arcana/Enshrouded não replicam portal, teleporte ou aquisição. Um único cast pode tentar várias transições sem novos casts; partículas por target não comprovam que terceiros mudaram de dimensão. Dedup exige caster/cast/fase/tentativa/destino, sem inferir sucesso pelo evento pré-efeito.

Assinatura source ocupada: transição do jogador entre Astral Sea e destino de respawn, com seleção local que pode repetir o transporte do caster. A intenção comentada de levar entidades não demonstra implementação. Nova magia original precisa contrato próprio seguro e não reutiliza assets/código.

- **Q1:** manter Gateway conditional/fora strict; capturar effective enabled/school/crafting/global/datapacks e gates reais, sem promover Survival por defaults.
- **Q2:** interrupção do LONG/marker, listeners, mana/cooldown, coordenadas/rotação, montaria e level de destino ausente.
- **Q3:** lista com self/outros, ordem, borda8/cantos, mudança de dimensão no loop, múltiplas transições e respawn listener, colisão/void/claims/worldborder/chunks.
- **Q4:** falha/exceção parcial, logout/morte/restart, reset da cast data após transporte, sync do marker e cliente/multiplayer.
- **Q5:** contrato/atribuição de prática antes de efeito versus chegada. **Runtime, Survival, JAR funcional e integração PENDING**, nenhum Stage/adapter/perk promovido.

[registry]: https://github.com/BirdieVibes/Asterism-Arcanum/blob/f1738c7813a85d31a6da10e6c9f2dbce18d2b583/src/main/java/com/birdie/asterismarcanum/registries/ASARSpellRegistry.java#L43-L46
[spell]: https://github.com/BirdieVibes/Asterism-Arcanum/blob/f1738c7813a85d31a6da10e6c9f2dbce18d2b583/src/main/java/com/birdie/asterismarcanum/spells/AstralGatewaySpell.java#L30-L72
[pre]: https://github.com/BirdieVibes/Asterism-Arcanum/blob/f1738c7813a85d31a6da10e6c9f2dbce18d2b583/src/main/java/com/birdie/asterismarcanum/spells/AstralGatewaySpell.java#L50-L62
[precast]: https://github.com/BirdieVibes/Asterism-Arcanum/blob/f1738c7813a85d31a6da10e6c9f2dbce18d2b583/src/main/java/com/birdie/asterismarcanum/spells/AstralGatewaySpell.java#L85-L98
[cast]: https://github.com/BirdieVibes/Asterism-Arcanum/blob/f1738c7813a85d31a6da10e6c9f2dbce18d2b583/src/main/java/com/birdie/asterismarcanum/spells/AstralGatewaySpell.java#L100-L121
[sea]: https://github.com/BirdieVibes/Asterism-Arcanum/blob/f1738c7813a85d31a6da10e6c9f2dbce18d2b583/src/main/java/com/birdie/asterismarcanum/capabilities/magic/AstralSeaManager.java#L11-L13
[dimension]: https://github.com/BirdieVibes/Asterism-Arcanum/blob/f1738c7813a85d31a6da10e6c9f2dbce18d2b583/src/main/resources/data/asterismarcanum/dimension/astral_sea.json#L1-L24
[versions]: https://github.com/BirdieVibes/Asterism-Arcanum/blob/f1738c7813a85d31a6da10e6c9f2dbce18d2b583/gradle.properties#L9-L24
[data]: https://github.com/iron431/irons-spells-n-spellbooks/blob/e4056af90302d37eb1739f5ff05020b020e6e252/src/main/java/io/redspace/ironsspellbooks/spells/EntityCastData.java#L9-L29
[host-cast]: https://github.com/iron431/irons-spells-n-spellbooks/blob/e4056af90302d37eb1739f5ff05020b020e6e252/src/main/java/io/redspace/ironsspellbooks/api/spells/AbstractSpell.java#L160-L325

[dimension-motion]: https://github.com/BirdieVibes/Asterism-Arcanum/blob/f1738c7813a85d31a6da10e6c9f2dbce18d2b583/src/main/java/com/birdie/asterismarcanum/events/ServerEvents.java#L21-L38
