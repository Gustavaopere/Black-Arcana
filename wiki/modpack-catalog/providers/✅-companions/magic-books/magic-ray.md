# Magic Ray Magic Book

**Prova física Java21 (2026-10-13):** ✅ `COUNTED_EXACT` — `companions:book_magic_ray`, `dev.xylonity.companions.common.item.book.books.MagicRayBook` (subclasse real de `AbstractMagicBook`), [auditoria #38458161666](https://github.com/Gustavaopere/Black-Arcana/actions/runs/38458161666) e [dossiê SHA-exato](../EXACT-BINARY-MAGIC-BOOKS-1.3.4.md). Item mágico provider-native, não spell Iron's. Cooldown, cast e aquisição continuam source-pinned/Survival ⚠️; +0 identidade nova.

- Provider: **Companions!** (`companions`)
- Version: `1.3.4`
- Registry id: `companions:book_magic_ray`
- Concrete class: `MagicRayBook`
- Semantic type: **provider-owned Magic Book action**
- Semantic state: `COUNTED_EXACT` (**identidade estática somente**)
- Strict contribution: `1`
- Source-default cooldown: **200 ticks**
- Source-level survival acquisition: **provider injection into vanilla chest-table loot**

## Action surface

builds a provider magic ray from successive ray pieces along the look direction until the configured/source-bounded path is exhausted or blocked.

## Registration closure

The exact 1.3.4 source pin registers this item directly in `CompanionsItems` as a concrete `AbstractMagicBook` subclass. No mod-presence/config branch around the nine Magic Book registrations was found.

## Acquisition boundary

The route above is closed at source/catalog level. Effective assembled-pack loot, recipe/datapack mutation, probabilities and deployed config remain runtime QA.

## Soul Mage deduplication

Soul Mage can consume/equip the same Magic Book identity. Its AI goal reuses this action and does not mint a second semantic object.

## Authority boundary

Companions! remains authority for activation, cooldown/config settlement and any projectile/effect/state created by this action. Black Arcana must not replay the provider's damage, healing, summon/projectile or cooldown settlement.

## Evidence boundary

The source-default cooldown and action description are factual metadata from the pinned provider inventory, not deployed-pack measurements. Runtime attribution, protection behavior, multiplayer behavior and lifecycle remain separate QA.

Source: `../SOURCE-1.3.4-MAGIC-BOOK-INVENTORY.md`.

## Engenharia causal para perks — Magic Ray (source pin 1.3.4, 17/10/2026)

**Escopo da prova:** leitura de `Xylonity/Companions@95c9445e1514648418064ea90b5c373e81375d2f`; SHA exato do JAR físico prova apenas a identidade registral descrita acima. **SOURCE-CAUSALITY**, não equivalência binária dos efeitos, runtime, adapter RPG ou QA. Host KnightLib 2.0.1 é uma dependência real cuja semântica de scheduler/lifetime não foi homologada neste dossiê.

### Matriz por eixo

| Eixo | Comportamento observável em Java | Mutabilidade externa |
|---|---|---|
| Ingresso / cast | `MagicRayBook.use` executa ramo server-only; gera todos os segmentos na mesma ação do livro e depois aplica cooldown. `AbstractMagicBook.use` herda swing e som, sem etapa de mana exposta no corpo examinado. | `SEM_HOOK_SEGURO` para modificar o cast por perk; nenhuma API de cast própria comprovada. |
| Alcance / targeting | Vetor do olhar, origem no olho + 1 bloco; loop `i < 30`, incremento de distância de **1 bloco por iteração**: **até 30 posições amostradas**, não raio esférico nem 30 hits garantidos. Interrompe depois de criar um segmento também na primeira posição de bloco **não passável**, onde `getCollisionShape(...).isEmpty()` é falso. | Alcance de feixe constante no corpo; `SEM_HOOK_SEGURO` para multiplicar por perks. |
| Número / atraso | Primeiro segmento cria `MagicRayCircleProjectile` imediatamente; os demais criam `MagicRayPieceProjectile`, todos com `TickScheduler.scheduleServer(..., 3)` quando há ServerLevel. **Um mesmo atraso de 3 ticks**, não espaçamento progressivo de 3 ticks por segmento. | `SEM_HOOK_SEGURO` para multiplicar segmentos, delay ou converter alvo único em AOE. |
| Área / hitbox | Cada segmento examina `LivingEntity` em AABB da entidade ampliada em **0,75 bloco** e seleciona **somente o primeiro** elemento da lista a cada tick. AABB física-base, bounding boxes reais e ordenação da consulta dependem do runtime, não da escala visual. | Não há raio central configurável no livro; `SEM_HOOK_SEGURO` para largura/targets por segmento. |
| Dano / tipo / periodicidade | Por tick de cada `MagicRayPieceProjectile` server-side, chama `hurt(damageSources().indirectMagic(segment, owner), MAGIC_PIECE_DAMAGE)` para o primeiro alvo elegível. Default `MAGIC_PIECE_DAMAGE=5.5` (config declarada [1,1000]); **tentativa de dano ≠ dano aceito** por invulnerability/eventos. `MagicRayCircleProjectile` herda o mesmo tick de colisão. | `CONFIG_NATIVE` para o valor global de dano; `NÃO_VERIFICADO` para hook de valor por jogador; tipo `indirectMagic` não é conversão elemental livre. |
| Lifetime / efeito persistente | `baseLifetime()` retorna **18 ticks** para Piece e **22 ticks** para Circle. O descarte efetivo pertence à classe `KnightLib AbstractProjectile`, não inspecionada nesta prova; números são overrides source, não tempo físico cronometrado. | `SEM_HOOK_SEGURO` para tempo por perk. |
| Cooldown / custos | Default `MAGIC_RAY_COOLDOWN=200 ticks`. `addCooldown(this,(int)(base × (1 - pieces × MAGE_SET_COOLDOWN_REDUCTION)))`; helper de nome enganoso `hasFullSetOn` **retorna contagem de peças** (0–4); default redução **0,15 por peça**. Sem leitura de mana/XP no método de livro. | `CONFIG_NATIVE` apenas valores globais; `SEM_HOOK_SEGURO` para benefício individual via RPG. |

### Âncoras e condições de QA

- [MagicRayBook.java — 32–89](https://github.com/Xylonity/Companions/blob/95c9445e1514648418064ea90b5c373e81375d2f/common/src/main/java/dev/xylonity/companions/common/item/book/books/MagicRayBook.java#L32-L89): geração, corte por colisão de bloco, scheduler, owner e cooldown.
- [MagicRayPieceProjectile.java — 33–76](https://github.com/Xylonity/Companions/blob/95c9445e1514648418064ea90b5c373e81375d2f/common/src/main/java/dev/xylonity/companions/common/entity/projectile/MagicRayPieceProjectile.java#L33-L76): detecção por segmento, `indirectMagic`, primeira vítima e hitbox AABB.
- [MagicRayPieceProjectile.java — 83–96](https://github.com/Xylonity/Companions/blob/95c9445e1514648418064ea90b5c373e81375d2f/common/src/main/java/dev/xylonity/companions/common/entity/projectile/MagicRayPieceProjectile.java#L83-L96) e [MagicRayCircleProjectile.java — 9–28](https://github.com/Xylonity/Companions/blob/95c9445e1514648418064ea90b5c373e81375d2f/common/src/main/java/dev/xylonity/companions/common/entity/projectile/MagicRayCircleProjectile.java#L9-L28): overrides de tempo de vida.
- [CompanionsConfig.java — damage](https://github.com/Xylonity/Companions/blob/95c9445e1514648418064ea90b5c373e81375d2f/common/src/main/java/dev/xylonity/companions/config/CompanionsConfig.java#L678-L683), [cooldown](https://github.com/Xylonity/Companions/blob/95c9445e1514648418064ea90b5c373e81375d2f/common/src/main/java/dev/xylonity/companions/config/CompanionsConfig.java#L790-L795) e [Mage set](https://github.com/Xylonity/Companions/blob/95c9445e1514648418064ea90b5c373e81375d2f/common/src/main/java/dev/xylonity/companions/config/CompanionsConfig.java#L879-L884); [Util.hasFullSetOn](https://github.com/Xylonity/Companions/blob/95c9445e1514648418064ea90b5c373e81375d2f/common/src/main/java/dev/xylonity/companions/common/util/Util.java#L260-L274): valores default e contagem real de armadura.

**Riscos e aceitação:** segmentos podem tentar `hurt` repetidamente em ticks sucessivos; procs/Mastery devem depender de resultado efetivamente aplicado e deduplicar por **identidade causal da conjuração**, ainda não demonstrada no provider. Testar paredão logo à frente (o source ainda gera o segmento bloqueado), vários alvos, i-frames, cancellation, owner offline, recasts, scheduler e permanência ao descarregar chunk; não declarar 30 acertos nem cooldown do Soul Mage idêntico ao jogador sem testar. **+0 novas magias, +0 adapters.**
