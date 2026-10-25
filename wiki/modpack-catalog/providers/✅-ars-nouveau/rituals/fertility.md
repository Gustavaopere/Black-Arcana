# Fertility

Status: `SOURCE-PINNED 5.13.1 / BREEDING RITUAL`

- Registry id: `ars_nouveau:ritual_fertility`
- Class: `RitualBreed`
- Source cost declaration: `500`
- Processing cadence: every `200` game ticks
- Radius: `5` blocks
- Local population hard cap: no effect at `20+` nearby animals
- Exact release checkpoint: `baileyholl/Ars-Nouveau@112920ff774831f204031da75b4c4e73d3765157`

## Provider-native behavior

Every 200 ticks, Fertility obtains `Animal` entities inside radius 5. If the local count is at least 20, the work cycle aborts.

Below that cap, each animal not in the provider breeding blacklist is checked for adulthood (`age == 0`) and `canFallInLove()`. Eligible animals are placed into love state through the provider. If at least one animal changes state, the cycle requests Source.

The ritual tooltip independently refreshes the `20+ animals` warning once per second.

## Authority / Black Arcana boundary

Population admission, breeding state and Source use remain Ars Nouveau authority. Black Arcana must not add a second breeding trigger, second Source charge or extra progression credit per animal.

The 20-animal ceiling is part of the provider's bounded operational identity and should not be silently bypassed by integration.

## QA

Source behavior is pinned to 5.13.1. Compatibility with modded animal breeding implementations remains full-pack runtime QA.

## Engenharia para perks — contrato de ritual

- **Fonte:** [`RitualBreed.java`](https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/common/ritual/RitualBreed.java), `com.hollingsworth.arsnouveau.common.ritual.RitualBreed`, Ars 5.13.1.
- **Frequência e cap:** a cada `200` ticks, procura `Animal` em `AABB(brazier).inflate(5)`. Se `animals.size()>=20` retorna **sem efeito** (todos os animais contam antes do filtro de blacklist); tooltips atualizam aviso a cada 20 ticks quando consultados.
- **Processamento:** ignora `EntityTags.BREED_BLACKLIST`; exige idade `getAge()==0` e `canFallInLove()`, chama `setInLove(null)` e marca `didWorkOnce`. Após ao menos uma operação marca `setNeedsSource(true)`; `getSourceCost=500` é declarado por ritual, não prova de custo por animal.
- **Perks:** remover cap populacional, tornar animals adultos ou induzir love fora de `canFallInLove` mudaria contrato da autoridade Ars; status de breeding não garante nascimento nem novo cast. Observação de Mastery deve ser deduplicada.
- **Estado:** ✅ source-pinned; ⚠️ tempo, recursos e proteção exigem observar config/JAR runtime. ⛔ não existe adapter RPG/Black Arcana demonstrado para reescrever Source, progresso, alvos ou world effects deste ritual.

## Certificação técnica estática de ritual — 25/10/2026

**✅ `STATIC_TECHNICAL_CATALOG_ONLY` para planejamento de perks e balanceamento; ⛔ `mutating_hook=NOT_VERIFIED`; ⚠️ `physical_qa=NOT_TESTED`.** Documentação source-pinned não equivale a implementação de hook, aceitação de cliente, ou QA no modpack real.

| Campo obrigatório para perks | Evidência técnica e limite de aplicabilidade |
|---|---|
| Identidade e proveniência | `ars_nouveau:ritual_fertility`, classe `RitualBreed`, release `ars_nouveau-1.21.1-5.13.1.jar`. [Source imutável](https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/common/ritual/RitualBreed.java); [IDs de 24 rituais comprovados no JAR SHA-exato](../EXACT-BINARY-GLYPH-RITUAL-IDS-5.13.1.md). |
| Causalidade, fases e settlement | A cada `world.getGameTime()%200==0` em lado servidor, `getEntitiesOfClass(Animal.class,new AABB(getPos()).inflate(5))` coleta todos os animais. **Se 20 ou mais**, aborta ciclo antes dos filtros. Depois ignora `EntityTags.BREED_BLACKLIST`, exige `age==0 && canFallInLove()` e chama `setInLove(null)`; ao menos um sucesso lógico ativa `setNeedsSource(true)`. O cliente emite partículas em raio 5, que não são operações de breeding. |
| Fórmulas, limites, duração, caps e gatilhos | AABB inflada **5** e threshold populacional **20 animais incluindo os bloqueados**, cadência **200 game ticks**; `modifyTooltips()` atualiza `tooManyAnimals` apenas a cada 20 ticks ao ser invocado, não é a regra de bloqueio. Elegibilidade depende da entidade/mod e de `canFallInLove`. Não confundir estado love com nascimento realizado. |
| Alvo, área/volume, dano, projétil e tempo | `Animal` elegível na área local; área é AABB, não esfera exata de raio 5 e não `LivingEntity` geral. Nenhum projeto, dano, DamageType ou duração de cast própria, e efeitos de reprodução posteriores são Minecraft/mod-owned. |
| Fonte/custos/cooldowns e consumo de itens | **500 Source** via `getSourceCost()`; na execução observada, `setNeedsSource(true)` ocorre **uma vez após um ciclo que mudou ao menos um estado de breeding**. Não atribuir 500 Source **por animal** nem confirmar débito efetivo em jar sem seguir `RitualBrazierTile`. **Não aplicáveis como custo local:** mana de glyph, cooldown de ataque/Forms ou XP por hit. Ritual físico/ativação/receitas item são próprios do Ars; não inferir pagamento bem-sucedido, drops ou custos adicionais sem a implementação de brasier/recipes. |
| Integração e limites de authority | Não remover cap ou blacklist por perk, não cobrar Source por animal nem creditá-lo por filhote futuro; processamento e estados são Ars-owned, integração multiplayer/farms de mods exigem QA. O Black Arcana detém seu runtime, rituais, hazards, Corruption, Strain e WorldEffectPolicy próprio; este ritual e sua persistência são provider-owned Ars. RPG Skill Tree fornece apenas Mastery/gates/perks através de bridge testado; não há adapter validado de mutação destes métodos. |
| Validação e pendências | Identidade e class-to-ID do publisher JAR 5.13.1 SHA-1 `02782d071ee5fab3b5c4b8ced67b7e1748277dfd` auditadas anteriormente; semântica de método provém do source fixo `baileyholl/Ars-Nouveau@112920ff774831f204031da75b4c4e73d3765157`. Essas são **provas distintas**: não se afirma equivalência de classfile completo, config efetiva, side/server do pack, snapshot persistence, proteção de mundo, multiplayer ou QA físico (`NOT_TESTED`). |

**Regra fail-closed:** qualquer alteração do ritual/custo/range/duração ou concessão de Mastery exige inspeção do ponto de mutação real, chamadas downstream de Source/settlement, bounds, deduplicação e testes específicos. Não promover Stage06.05/09 nem contar ticks/pacotes/partículas como casts.
