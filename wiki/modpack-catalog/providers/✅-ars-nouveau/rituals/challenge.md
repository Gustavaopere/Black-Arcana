# Challenge

Status: `SOURCE-PINNED 5.13.1 / RAID RITUAL`

- Registry id: `ars_nouveau:ritual_challenge`
- Class: `RitualPillagerRaid`
- Exact release checkpoint: `baileyholl/Ars-Nouveau@112920ff774831f204031da75b4c4e73d3765157`

## Provider-native behavior

Once per 20 server ticks the ritual increments progress. At progress `18`, it looks for `ServerPlayer` entities within an AABB inflated by `5.0` blocks around the ritual and asks the vanilla raid manager to create or extend a raid using the first returned player and the ritual position.

The ritual finishes only when a non-null `Raid` is returned.

### Optional Emerald modifier

Outside Hard difficulty, the ritual accepts exactly one emerald-tag item while its consumed-item list is empty. If that Emerald was consumed and a raid is successfully created, the provider sets `raid.numGroups = 7`.

On Hard difficulty the ritual refuses this optional modifier.

The provider description frames the ritual as summoning an illager raid when used inside a village; the actual village/raid validity remains enforced by the vanilla raid creation path.

## Authority / Black Arcana boundary

Raid creation, player association, raid group count and optional item consumption remain provider/vanilla authority. Black Arcana must not create a second raid, consume another Emerald or re-credit raid waves as separate ritual completions.

## QA

Source behavior is pinned to 5.13.1. Effective interaction with other raid modifiers and full-pack village mechanics remains runtime QA.

## Engenharia para perks — contrato de ritual

- **Fonte:** [`RitualPillagerRaid.java`](https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/common/ritual/RitualPillagerRaid.java), `com.hollingsworth.arsnouveau.common.ritual.RitualPillagerRaid`, Ars 5.13.1.
- **Progresso:** a cada `20` ticks server avança `progress`, e quando `>=18` procura `ServerPlayer` em `AABB(brazier).inflate(5.0)`; usa o **primeiro** player retornado para `world.getRaids().createOrExtendRaid(player,brazierPos)`. Ritual só finaliza com `Raid` não nulo; sem player ou sem raid válida pode persistir.
- **Modificador:** `canConsumeItem` permite item de `Tags.Items.GEMS_EMERALD` se dificuldade **não** HARD e `consumedItems` estiver vazio. Quando raid foi criada, `didConsumeItem(Items.EMERALD)` (tipo **exato**) altera `raid.numGroups=7`. A diferença entre aceitação por tag e teste de `Items.EMERALD` merece verificação com gems equivalentes; não presumir que qualquer emerald-tag tenha o mesmo resultado.
- **Perks:** raid e waves pertencem ao manager vanilla/Ars. Não creditar Mastery por cada onda como conclusão independente, nem mutar `raid.numGroups`/consumo sem API de integração e validação de conflito com addons.
- **Estado:** ✅ source-pinned; ⚠️ tempo, recursos e proteção exigem observar config/JAR runtime. ⛔ não existe adapter RPG/Black Arcana demonstrado para reescrever Source, progresso, alvos ou world effects deste ritual.

## Certificação técnica estática para perks — raid vanilla (25/10/2026)

**✅ `STATIC_TECHNICAL_CATALOG_ONLY` · ⛔ `mutating_hook=NOT_VERIFIED` · ⚠️ `physical_qa=NOT_TESTED`.** ID `ars_nouveau:ritual_challenge` vinculado à classe `RitualPillagerRaid` no [manifesto exato](../EXACT-BINARY-GLYPH-RITUAL-IDS-5.13.1.md). Método inspecionado em [`RitualPillagerRaid.java`](https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/common/ritual/RitualPillagerRaid.java) no commit `112920ff774831f204031da75b4c4e73d3765157`, binário 5.13.1 SHA-1 `02782d071ee5fab3b5c4b8ced67b7e1748277dfd` **somente para identificação classe/registry**.

| Campo relevante | Evidência e limite de alteração |
|---|---|
| Timing/condição | Em servidor quando `getGameTime()%20==0`, `incrementProgress()` e, se `getProgress()>=18`, busca `ServerPlayer` em `new AABB(getPos()).inflate(5.0)`. AABB não equivale a raio esférico 5 ou seleção do jogador ativador. |
| Alvo/efeito | Se houver jogadores próximos, usa **`players.get(0)`** e `world.getRaids().createOrExtendRaid(players.get(0),getPos())`. O **Raid manager vanilla** decide se existe vila, condições e se cria/estende raid; `RitualPillagerRaid` só chama `setFinished()` se o retorno `Raid != null`. Sem jogador/raid válido, continua elegível em ticks posteriores; progresso não é teto rígido nem sucesso garantido. |
| Modificador opcional | `canConsumeItem` requer `world.getDifficulty()!=Difficulty.HARD`, `consumedItems.isEmpty()` e `stack.is(Tags.Items.GEMS_EMERALD)`. Após raid não nula, testa **`didConsumeItem(Items.EMERALD)` de item exato**, e então `raid.numGroups=7`. Isso não comprova que qualquer item de tag emerald aciona as 7 ondas, nem que este número represente raids adicionais. |
| Dano/área | O próprio ritual não instancia projétil de spell, não ataca entidades nem expõe `DamageType` ou cooldown ofensivo. As waves, posições, danos, espólios e mortes pertencem ao raid manager/entidades vanilla e podem depender de mods de villagers/raids. |
| Custos | Getter herdado `AbstractRitual.getSourceCost()=0` (Source local declarado), **não equivale a ritual grátis**: custo de tablet, optional item e transação do brazier não são dedutíveis apenas desta classe. A alteração `numGroups=7` só ocorre **após** obter a raid, não é regra sobre qualquer spawn. |
| Integração e segurança | Nenhum replay de `createOrExtendRaid`, segundo raid ao concluir, Mastery por wave ou força de raid via `numGroups` sem boundary real. Não supor veto de vila implementado pelo próprio ritual nem neutralizar proteções/eventos vanilla. Ars gerencia sua execução; vanilla gerencia raid; RPG Skill Tree provê apenas atributos/perks/Mastery por contrato; Black Arcana preserva seu runtime separado. |

**Pendências:** ordenação de `ServerPlayer` na AABB, raids existentes, conflitos com mods de vila, tags configuradas, dificuldades, consumo, persistência e testes físicos. `mutating_hook=NOT_VERIFIED`; `physical_qa=NOT_TESTED`.
