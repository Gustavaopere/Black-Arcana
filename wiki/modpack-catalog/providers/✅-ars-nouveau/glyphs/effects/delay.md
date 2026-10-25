# Ars Nouveau — Delay

Status: `SOURCE-PINNED 5.13.1 / STATIC TECHNICAL CONTRACT / RUNTIME CONFIG QA PENDING`

- Registry id: `ars_nouveau:glyph_delay`; classe `com.hollingsworth.arsnouveau.common.spell.effect.EffectDelay` [S-delay].
- Escola Manipulation; tier default **I**; mana default **0**.
- Augments nativos: Extend Time, Reduce Time (`glyph_duration_down`), Randomize.

## Comportamento e caminho causal

A descrição do provider é adiar a resolução dos componentes à direita. O consumidor efetivo é `sendPacket`: sai sem agendar quando `currentIndex >= spell.size()`; caso haja continuação, cria `DelayedSpellEvent`, guarda em `spellContext.delay`, adiciona à fila **server** e envia `PacketClientDelayEffect` [S-delay]. Os callbacks de bloco e entidade passam o hit original ao mesmo caminho; não há dano, status, raio ou projétil próprios.

`SpellContext.hasNextPart()` interrompe o laço quando `isDelayed()` é verdadeiro, que exige evento não nulo com `duration > 0` [S-context-loop] [S-context-delay]. `DelayedSpellEvent.tick` decrementa duração; quando ela chega a zero no servidor, chama `resolveSpell` → `resolver.resume(world)` [S-event]. Esse caminho retoma o **mesmo resolver/contexto**, sem `resetCastCounter`, sem novo `onCast` e sem `expendMana`; conserva o hit já guardado em `resolver.hitResult` [S-resolve]. Se o resultado era entidade já removida, `resolveSpell` retorna sem retomar [S-event]. Não há nova aquisição de alvo, raycast ou garantia de LOS no fim da espera.

O pacote do cliente armazena duração, spell e IDs, reconstrói um resultado e agenda evento na fila **client**; nesse lado o evento emite partículas, não chama a resolução server [S-packet] [S-event]. FX não são outra aplicação nem outro cast.

## Parâmetros, unidades e casos de borda

Defina `E=count(Extend Time)`, `D=count(Duration Down)` e `R=count(Randomize)` na lista de augments de `SpellStats`. O cálculo **usa contagens**, não `getDurationMultiplier()` [S-delay]:

```text
T = GENERIC_INT + EXTEND_TIME*20*E - DURATION_DOWN_TIME*D
  = 20 + 20*E - 10*D                         # defaults, ticks
r = R*RANDOMIZE_CHANCE = 0,25*R               # default
Tfinal = nextIntBetweenInclusive((int)(T*(1-r)), (int)(T*(1+r)))
```

O sorteio só ocorre quando `stats.isRandomized()`; os dois limites truncam para `int` e são inclusivos [S-delay]. A descrição fala 25% do atraso base, mas o código usa **todo `T` já modificado**. Exemplo default `E=1,D=0,R=1`: `T=40`, sorteio **30…50 ticks**, não 35…45. Um aumento somente do scalar de duração por perk não muda essa fórmula.

`buildConfig` define base 20 ticks, Extend 1 (convertido por `*20`), Down 10 ticks, randomize 0,25; getters são acessados diretamente, sem fallback local se a config não estiver inicializada [S-config]. Os helpers admitem base/tempo de zero até `Integer.MAX_VALUE` e randomize até esse valor; não há clamp local de `T`, de `r` a 1, nem proteção local de overflow da multiplicação inteira [S-config-helper]. Portanto uma lista/config extrema pode gerar duração negativa ou intervalo inválido; isso não é contrato de gameplay seguro.

**Zero/negativo não equivale a aguardar um tick:** `EventQueue.tick` testa `isExpired()` **antes** de `tick`; o evento com duração ≤0 expira e sai sem executar `resolveSpell` [S-queue] [S-event]. Ao mesmo tempo `SpellContext.isDelayed()` é falso, então o laço de resolução atual pode continuar imediatamente à direita [S-context-loop] [S-context-delay]. Para duração positiva, a contagem é de ticks de fila; servidor congelado/stepping e cliente pausado têm gates próprios [S-queue-clock]. Não converter em segundos de relógio sem condições.

## Targeting, custos e aprendizagem

A Form/Effects anteriores escolhem o alvo. Delay conserva `BlockHitResult` ou `EntityHitResult`; alcance, AOE, tamanho/velocidade de projétil, dano e tipo de dano **não se aplicam ao próprio glyph**. Os Effects posteriores ainda podem gerar área/dano/entidades normalmente. Espera não é cooldown adicional.

Receita datagen: `ars_nouveau:manipulation_essence` + `minecraft:repeater` + `minecraft:clock` [S-recipe]. XP default **27** (tier I) [S-xp]; starter default **não** [S-starter]. Aprendizagem e consumo do glyph em Survival pertencem a Ars; ver [aquisição 85/85](../../ACQUISITION.md). Mana default0 é do componente, não custo0 de toda composição: `getCastingCost()` usa a config e o resolver paga o cast composto quando a Form obtém sucesso [S-cost] [S-mana].

## Certificação estática individual — 25/10/2026

| Campo | Contrato documentado e limite |
|---|---|
| Identidade e release | `ars_nouveau:glyph_delay`, `EffectDelay`, Ars5.13.1; source imutável [S-delay] e auditoria compilada ID/classe no rodapé. |
| Comportamento e causalidade | `sendPacket` → contexto atrasado → fila → `DelayedSpellEvent` → mesmo `resolver.resume`; cliente só FX; entidade removida interrompe continuação. |
| Parâmetros e caps | `20+20E−10D` default; Randomize usa `T` modificado e contagem; sem clamp local, scalar de duração isolado não consumido; config carregada não comprovada. |
| Targeting e resultado | Hit de bloco/entidade existente, sem nova seleção/LOS; sem dano, projétil, área ou status próprios; posteriores preservam seus contratos. |
| Custos e aprendizagem | Mana0, tierI, 27XP, starter não, ingredientes acima; custo composto/provider e cooldown distintos de atraso. |
| Integração e authority | API pública de stats/eventos existe; contagem e scheduler não são um slider genérico de duração; adapter RPG não validado; continuação não é novo cast. |
| Validação e pendências | `PINNED_SOURCE_PLUS_SHA_EXACT_BINARY_IDENTITY`; source/ID auditados, corpos binários/config efetiva/gameplay não; `mutating_hook=NOT_VERIFIED`, `physical_qa=NOT_TESTED`. |

## Evidência e fronteira de integração

**✅ `claim_scope=STATIC_TECHNICAL_CATALOG_ONLY`; ⛔ `mutating_hook=NOT_VERIFIED`; ⚠️ `physical_qa=NOT_TESTED`.** A revisão de source não implementa perks nem valida gameplay.

O source é `baileyholl/Ars-Nouveau@112920ff774831f204031da75b4c4e73d3765157`, release **5.13.1**. A [auditoria de identidades compiladas](../../EXACT-BINARY-GLYPH-RITUAL-IDS-5.13.1.md) usa publisher `ars_nouveau-1.21.1-5.13.1.jar`, SHA-1 `02782d071ee5fab3b5c4b8ced67b7e1748277dfd`, e comprova **ID/classe**, não equivalência de todos os corpos Java/bytecode. Config instalada, addons, claims, unload/reload e execução física permanecem não testados.

`SpellModifierEvent` é uma API pública real: `SpellStats.Builder.build` aplica augments/itens, publica o evento com o builder e devolve seu `spellStats` [S-builder]. Uma alteração *in-place* no builder original tem superfície source-verified; apenas substituir `event.builder` não troca o objeto retornado. `EffectResolveEvent.Pre` permite cancelamento antes do callback; `SpellResolver.resume` consulta `isCanceled`, mas passa seus **objetos locais** a `effect.onResolve` [S-resolve]. Reatribuir `event.spellStats`, `rayTraceResult`, `resolveEffect` ou `context` não substitui esses locais. `Post` pode ocorrer sem efeito aplicado e não comprova sucesso físico.

Um adapter de perks RPG Skill Tree/Black Arcana que preserve caps, fase, recurso, identidade causal e deduplicação **não foi comprovado**. Ars conserva casting, mana de jogador, scheduler, contexto e efeitos. Source é recurso separado. Black Arcana mantém sua própria transação, Corruption, Strain e WorldEffectPolicy; observar continuação/tick/contexto filho não cria outro cast, cobrança, cooldown ou prêmio de mastery. Mudança de JAR, configs ou consumidores exige reauditoria.

[S-builder]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/api/spell/SpellStats.java#L138-L152
[S-resolve]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/api/spell/SpellResolver.java#L200-L270
[S-cost]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/api/spell/AbstractSpellPart.java#L127-L150
[S-starter]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/api/spell/AbstractSpellPart.java#L307-L310
[S-xp]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/common/datagen/GlyphRecipeProvider.java#L142-L157
[S-mana]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/api/spell/SpellResolver.java#L127-L173
[S-delay]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/common/spell/effect/EffectDelay.java#L26-L61
[S-config]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/common/spell/effect/EffectDelay.java#L63-L105
[S-config-helper]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/api/spell/AbstractEffect.java#L162-L177
[S-context-loop]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/api/spell/SpellContext.java#L148-L175
[S-context-delay]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/api/spell/SpellContext.java#L265-L275
[S-event]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/api/event/DelayedSpellEvent.java#L20-L67
[S-queue]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/api/event/EventQueue.java#L24-L47
[S-queue-clock]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/api/event/EventQueue.java#L78-L100
[S-packet]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/common/network/PacketClientDelayEffect.java#L64-L87
[S-recipe]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/common/datagen/GlyphRecipeProvider.java#L59-L65
