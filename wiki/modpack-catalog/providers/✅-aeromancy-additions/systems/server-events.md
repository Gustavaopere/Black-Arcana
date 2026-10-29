# Integração de eventos — AAServerEvents

**Contrato:** suporte de Aeromancy Additions `1.2.8`, source fixo `snackerpirater/aero-additions@ae282b32d25ad76ef8d01c637ec05566a767ae4c`. Não é nova identidade de magia. `hooks=NOT_VERIFIED`; `physical_runtime=NOT_TESTED`; **0 certificações / +0 magias / +0 adapters aprovados**. O JAR oficial de publicação foi adquirido separadamente; isso não comprova paridade com o JAR instalado historicamente (SHA-1 histórico de 35 caracteres inválido). [Proveniência e limites](../SOURCE-CONTRACTS-1.2.8.md).

## Registro, combate e movimentação

`AAServerEvents` e a classe interna `Game` usam `@EventBusSubscriber(modid=aero_additions)`. O nome da classe não é prova de gate de side: os métodos ativos não apresentam verificação universal de `isClientSide`; `ServerPlayer` limita os caminhos de sync.

| Callback | Contrato ativo |
|---|---|
| `addAttributes(EntityAttributeModificationEvent)` | Adiciona WIND_SPELL_POWER e WIND_MAGIC_RESIST a `EntityType.PLAYER`. Definições pertencem à escola/registro. |
| `onAttributeCreate(EntityAttributeCreationEvent)` | Registra attributes de SummonedBreeze. |
| `windShieldDeflection(ProjectileImpactEvent)` | Só entra para `EntityHitResult` contra `LivingEntity`. Se tem WIND_SHIELD e projétil não está em `REFLECTION_IMMUNE`, sorteia `<chanceToDeflect(amplifier)`. Sucesso cancela impacto, toca BREEZE_DEFLECT e usa deflexão REVERSE, com alvo como deflector e owner e booleano `target instanceof Player`. |
| `else if` de SummonedBreeze | Se o primeiro `if` não entrou e tipo do atingido é SUMMONED_BREEZE, cancela e deflete REVERSE com owner obtido por `SummonManager.getOwner`. Não exige rolagem; não aplica `REFLECTION_IMMUNE` neste ramo. Se o primeiro `if` entrou mas a rolagem falhou, o `else if` não executa. |
| `activateFlight(PlayerSwimEvent)` | Com MobEffect FLIGHT, muda resultado para ExpandAbility `EventResult.SUCCESS`; não escreve contador/flags de Aeromancy. |

A chance local é delegada ao callback `WindShieldSpell.chanceToDeflect(amplifier) = amplifier/10f + 0.3f`, sem clamp nesse método (níveis padrão 1–5 usam amplifier 0–4 e chances 30–70%); [efeito Wind Shield](../effects/wind-shield.md) e [Summoned Breeze](../entities/summoned-breeze.md) detalham o combate. Este arquivo não define spell range, dano direto ou custo de mana.

## Lifecycle de sync — papéis literais

| Evento | Snapshot enviado | Destinatário |
|---|---|---|
| `PlayerLoggedInEvent` | Attachment do player do evento | O próprio `ServerPlayer`. |
| `PlayerRespawnEvent` | Attachment do player do evento | O próprio `ServerPlayer`; não copia estado antigo aqui. |
| `PlayerChangedDimensionEvent` | Attachment do player do evento | O próprio `ServerPlayer`. |
| `StartTracking` | **Attachment de `event.getEntity()` (tracker)** | **`event.getTarget()` (target)**, somente se ambos forem `ServerPlayer`. |

A direção do último caso é a implementada, mesmo sendo distinta do fluxo usual target→tracker. Não há sync ativo para target mob neste handler. As tentativas de water-walk, fall damage por evento de explosão e Telelink/portal/dimensão estão comentadas, sem contrato de execução ativo.

| Eixo | Contrato para perks |
|---|---|
| Dano | N/A direto; impacto é cancelado/redirecionado. Responsabilidade do dano posterior pertence ao projétil/engine. |
| Alcance | O evento já traz o impacto; sem raycast ou raio novo. Sync usa destinatário explícito. |
| Alvo | LivingEntity atingido; branch especial SummonedBreeze; lifecycle limitado a ServerPlayer. |
| Tempo | Por evento; não há tick periódico, timer ou recarga de cargas neste arquivo. |
| Custo | N/A: sem mana/cooldown; não reinterpretar deflexão ou sync como novo cast/XP. |

[Contrato integrado](state-lifecycle-network-ui.md). Eventos, chance, ownership de projéteis e direção do tracking são source-only; multiplayer/runtime continuam `NOT_TESTED`.


**Fonte imutável:** [Attributes e combate](https://github.com/snackerpirater/aero-additions/blob/ae282b32d25ad76ef8d01c637ec05566a767ae4c/src/main/java/com/snackpirate/aeromancy/AAServerEvents.java#L54-L89) · [Lifecycle e Flight](https://github.com/snackerpirater/aero-additions/blob/ae282b32d25ad76ef8d01c637ec05566a767ae4c/src/main/java/com/snackpirate/aeromancy/AAServerEvents.java#L92-L124) · [Handlers desativados](https://github.com/snackerpirater/aero-additions/blob/ae282b32d25ad76ef8d01c637ec05566a767ae4c/src/main/java/com/snackpirate/aeromancy/AAServerEvents.java#L125-L170) · [Telelink desativado](https://github.com/snackerpirater/aero-additions/blob/ae282b32d25ad76ef8d01c637ec05566a767ae4c/src/main/java/com/snackpirate/aeromancy/AAServerEvents.java#L172-L202) · [Chance delegada](https://github.com/snackerpirater/aero-additions/blob/ae282b32d25ad76ef8d01c637ec05566a767ae4c/src/main/java/com/snackpirate/aeromancy/spells/wind_shield/WindShieldSpell.java#L51-L77).
