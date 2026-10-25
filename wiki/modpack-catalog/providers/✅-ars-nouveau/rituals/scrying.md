# Scrying

Status: `SOURCE-PINNED 5.13.1 / DIVINATION RITUAL`

- Registry id: `ars_nouveau:ritual_scrying`
- Class: `RitualScrying`
- Completion threshold: `15` progress steps, advanced once per 20 server ticks
- Player application radius: `5` blocks
- Base duration: `60 × 20 × 5 = 6000 ticks` (5 minutes)
- Manipulation Essence multiplier: `×3` (15 minutes)
- Exact release checkpoint: `baileyholl/Ars-Nouveau@112920ff774831f204031da75b4c4e73d3765157`

## Provider-native admission

The ritual requires at least one consumed item before start. It accepts:

- at most one Manipulation Essence as duration modifier;
- one target-defining item, either a BlockItem or an item matching a registered `ScryRitualRecipe`.

## Provider-native settlement

At completion, each `ServerPlayer` within radius 5 receives the Ars `SCRYING_EFFECT`. The ritual resolves its target as either:

- `TagScryer`, when the consumed item matches a registered scry ritual recipe; or
- `SingleBlockScryer`, when the target item is a block.

The selected `IScryer` is serialized into the player's persisted NBT under `an_scryer`, then synchronized to the client through the provider packet.

## Black Arcana boundary

Discovery/highlighting state and the serialized scry target remain Ars Nouveau authority. Black Arcana must not infer its own discovery ledger from nearby highlighted blocks or overwrite `an_scryer`.

Any Familiars & Divination integration should observe a supported provider state/hook rather than duplicating the scan/highlight system.

## QA

Source lifecycle is pinned to 5.13.1. Exact recipe-driven target coverage and client presentation in the full pack remain runtime/data QA.

## Dossiê de implementação para perks — ritual exato

- **Classe fonte:** [`RitualScrying.java`](https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/common/ritual/RitualScrying.java), fonte `112920ff774831f204031da75b4c4e73d3765157` para Ars 5.13.1.
- **Admissão:** `canStart` exige `getConsumedItems()` não vazio. `canConsumeItem` permite no máximo uma `MANIPULATION_ESSENCE` como modificador e um `BlockItem` ou item que case com `ScryRitualRegistry`.
- **Progresso:** `incrementProgress` a cada `20` ticks no servidor, completa em `>=15`; aplica a `ServerPlayer` em AABB `inflate(5.0)`. A duração de `SCRYING_EFFECT` é `60*20*5` ticks, multiplicada por 3 se Essence consumida (=6000 ou 18000 ticks defaults).
- **Persistência:** resolve `TagScryer` de receita ou `SingleBlockScryer` por BlockItem; `grantScrying` serializa o contrato para a chave `an_scryer` sob `Player.PERSISTED_NBT_TAG` e manda `PacketGetPersistentData`. Não assumir que partículas vistas no cliente são evento de descoberta confiável.
- **Perks:** revela estado persistente, mas um mod externo não deve gravar/modificar `an_scryer` sem contrato público de leitura/escrita.
- **Mutabilidade externa:** ⛔ nenhum adapter RPG provado que altere lifecycle, Source ou raio sem duplicar settlement; 🟡 fórmula/lógica source-pinned; ⚠️ runtime, receitas/config física, addons e Survival pendentes.

## Certificação técnica estática de ritual — 25/10/2026

**✅ `STATIC_TECHNICAL_CATALOG_ONLY` para planejamento de perks e balanceamento; ⛔ `mutating_hook=NOT_VERIFIED`; ⚠️ `physical_qa=NOT_TESTED`.** Documentação source-pinned não equivale a implementação de hook, aceitação de cliente, ou QA no modpack real.

| Campo obrigatório para perks | Evidência técnica e limite de aplicabilidade |
|---|---|
| Identidade e proveniência | `ars_nouveau:ritual_scrying`, classe `RitualScrying`, release `ars_nouveau-1.21.1-5.13.1.jar`. [Source imutável](https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/common/ritual/RitualScrying.java); [IDs de 24 rituais comprovados no JAR SHA-exato](../EXACT-BINARY-GLYPH-RITUAL-IDS-5.13.1.md). |
| Causalidade, fases e settlement | A cada `gameTime%20==0` no servidor incrementa progresso. Em `progress>=15`, seleciona `ServerPlayer` em `AABB(ritualPos).inflate(5)`. Usa primeiro item consumido que não é Manipulation Essence; tenta `ScryRitualRegistry.getRecipes().stream().filter(matches(new SingleRecipeInput(item),world)).findFirst()` para `TagScryer`, senão `BlockItem` para `SingleBlockScryer`. Se `scryer!=null`, aplica status e NBT e envia pacote. **Mesmo se não encontrar alvo válido ou jogadores**, chama `setFinished()`. |
| Fórmulas, limites, duração, caps e gatilhos | `getConsumedItems` deve estar não vazio para start, mas o código permite começar com **apenas Manipulation Essence**, terminando sem `scryer` válido — não prometer visão garantida. Default status **60×20×5=6000 ticks**; com Manipulation Essence multiplica por **3 → 18000 ticks**; contagem do progresso **15** a 20 game ticks por incremento no servidor (sem inferir começo/lag de tick). `canConsumeItem` impede um segundo modifier Essence e mais de um item-alvo; recipes externas podem alterar target válido. |
| Alvo, área/volume, dano, projétil e tempo | ServerPlayer em **AABB inflada 5**, recebe `ModPotions.SCRYING_EFFECT` com timer e state `an_scryer` em `Player.PERSISTED_NBT_TAG`; sincroniza via `PacketGetPersistentData`. O glyph de Divination real é `IScryer`, não entidade atingida por Form, dano, raio de projétil ou nova classe de mundo. Dados persistentes e highlight pertencem ao Ars. |
| Fonte/custos/cooldowns e consumo de itens | Sem override local de `getSourceCost()`, herdado **0** de `AbstractRitual`; exige **consumir pelo menos um item** (`canStart`) e pode aceitar um `MANIPULATION_ESSENCE` e até um alvo `BlockItem` ou `ScryRitualRecipe`. Custo de aprendizagem/recipe e comportamento de jar além desse getter não foram auditados nesta ficha. **Não aplicáveis como custo local:** mana de glyph, cooldown de ataque/Forms ou XP por hit. Ritual físico/ativação/receitas item são próprios do Ars; não inferir pagamento bem-sucedido, drops ou custos adicionais sem a implementação de brasier/recipes. |
| Integração e limites de authority | Não sobrescrever chave `an_scryer` ou inferir progresso de XP por partículas/blocos revelados. Uma perk que amplia alvo/duração exigiria evento/payload/comparação de estado e política de privacidade de dados persistentes, não obtidos apenas na leitura desta classe. O Black Arcana detém seu runtime, rituais, hazards, Corruption, Strain e WorldEffectPolicy próprio; este ritual e sua persistência são provider-owned Ars. RPG Skill Tree fornece apenas Mastery/gates/perks através de bridge testado; não há adapter validado de mutação destes métodos. |
| Validação e pendências | Identidade e class-to-ID do publisher JAR 5.13.1 SHA-1 `02782d071ee5fab3b5c4b8ced67b7e1748277dfd` auditadas anteriormente; semântica de método provém do source fixo `baileyholl/Ars-Nouveau@112920ff774831f204031da75b4c4e73d3765157`. Essas são **provas distintas**: não se afirma equivalência de classfile completo, config efetiva, side/server do pack, snapshot persistence, proteção de mundo, multiplayer ou QA físico (`NOT_TESTED`). |

**Regra fail-closed:** qualquer alteração do ritual/custo/range/duração ou concessão de Mastery exige inspeção do ponto de mutação real, chamadas downstream de Source/settlement, bounds, deduplicação e testes específicos. Não promover Stage06.05/09 nem contar ticks/pacotes/partículas como casts.
