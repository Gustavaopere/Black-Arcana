# Vampirism 1.10.13 — provider audit

Status: `SOURCE-PINNED 1.10.13 / CATÁLOGO GRANULAR BASE COMPLETO / RUNTIME QA + BLOODLINES/VAMPIRE SPELLS INTEROP PENDENTES`

## Autoridade da versão

- mod id: `vampirism`
- JAR instalado: `Vampirism-1.21-1.10.13.jar`
- versão instalada: `1.10.13`
- Minecraft: `1.21.1`
- loader: NeoForge
- source oficial: `TeamLapen/Vampirism`
- source pin exato usado nesta auditoria: `e1ed095713cef5e9eb151d0ee58908fa830d6bb7`

Esse pin ainda declara `main_version=1`, `major_version=10`, `minor_version=13`; o commit subsequente `6a219122...` já sobe o minor para `14`. Portanto detalhes 1.10.14+ não são autoridade para esta auditoria.

A release 1.10.13 também alterou especificamente persistência/configuração da ActionWheel e MinionTasks, village totems e caminhos de teleportação. Por isso essas superfícies foram revalidadas diretamente no source 1.10.13 em vez de herdadas do guia 1.10.12.

## Escopo provider-native confirmado

Vampirism não é apenas um sistema de transformação. Na build instalada ele possui autoridades próprias e separadas para:

- facções Vampire/Hunter;
- níveis de facção 1–14;
- níveis Lord 1–5;
- skill trees e skill points;
- player actions com cooldown/duration próprios;
- blood stats do jogador;
- `vampirism:blood` como fluido NeoForge;
- blood saturation/exhaustion;
- sundamage/garlic/vision;
- refinements;
- tasks e Lord progression;
- NPC Entity Actions;
- servants/minions e Minion Tasks;
- village/faction warfare;
- alchemy/brewing Hunter;
- APIs e events públicos para integração.

Black Arcana deve tratar essas superfícies como provider-native first. Não deve copiar a resolução para um segundo sistema paralelo.

## Inventário estrutural fechado em source

| Superfície | Quantidade confirmada |
|---|---:|
| Vampire player actions | **14** |
| Hunter player actions | **3** |
| Shared Lord actions | **2** |
| Vampire skill registry entries, incluindo roots | **31** |
| Hunter skill registry entries, incluindo roots | **32** |
| Shared Lord skills | **3** |
| NPC Entity Actions | **10** |
| Minion Tasks | **7** |
| Provider attributes | **4** |
| Refinements | **47** |
| Task keys | **46** |
| Vampire normal max level | **14** |
| Hunter normal max level | **14** |
| Vampire Lord max level | **5** |
| Hunter Lord max level | **5** |

## Documentos deste provider

- [`ACTION-CATALOG.md`](./ACTION-CATALOG.md): 14 Vampire actions, 3 Hunter actions, 2 Lord actions e authority de timers/events.
- [`SKILL-CATALOG.md`](./SKILL-CATALOG.md): registries, custos e topologia das árvores Vampire/Hunter/Lord.
- [`PROGRESSION.md`](./PROGRESSION.md): níveis 1–14, Altares, Hunter Trainer/Table e Lord Tasks 1–5.
- [`BLOOD-AND-RESOURCE-AUDIT.md`](./BLOOD-AND-RESOURCE-AUDIT.md): blood bar, saturation/exhaustion, fluido, conversão mB, consumers/producers.
- [`TASK-MINION-REFINEMENT-CATALOG.md`](./TASK-MINION-REFINEMENT-CATALOG.md): 46 tasks, 10 NPC Entity Actions, 7 Minion Tasks e 47 refinements.
- [`TECHNICAL-AUDIT.md`](./TECHNICAL-AUDIT.md): API pública, registries, hooks, gates, authority, causalidade e riscos.
- [`INTEGRATION-RULES.md`](./INTEGRATION-RULES.md): contrato Black Arcana ↔ Vampirism, incluindo reservoir, deduplicação e fail-closed.

## Regra de autoridade

### Actions

`IActionHandler` é autoridade de:

- unlock;
- permission;
- `canUse`;
- cooldown;
- duration;
- activation/deactivation;
- timers persistidos/sincronizados.

`ActionEvent.ActionActivatedEvent` é disparado depois dos gates do handler e antes de `action.onActivated(...)`. É cancelável e permite alterar cooldown/duration. O estado/timer só é gravado se a própria action retornar sucesso.

### Skills

`ISkillHandler` é autoridade sobre skill points, parents, sibling locks, skill-tree locks, enable/disable e refinements. Não existe um `SkillEvent` público equivalente ao event de actions; integrações devem ler o handler e usar eventos de facção/action quando possível, não inventar um callback inexistente.

### Faction/level

`PlayerFactionEvent.FactionLevelChangePre` é server-side e cancelável. `FactionLevelChanged` representa a transição concluída de facção/nível normal. O `IFactionPlayerHandler` expõe mutações oficiais, mas elas só devem ser usadas quando um contrato de integração explicitamente pretende alterar a progressão do Vampirism.

### Lord level

`setLordLevel(...)` possui validação provider-native, reconcilia skill-tree locks/minions e sincroniza estado, mas não emite o mesmo par público de `PlayerFactionEvent` usado pelo nível normal no source 1.10.13. Integrações de Lord devem usar Task/LordLevelReward ou transição de estado autoritativa com deduplicação, sem fingir que `FactionLevelChanged` cobre Lord.

### Blood

`BloodDrinkEvent.PlayerDrinkBloodEvent` é disparado antes do settlement em `BloodStats.addBlood(...)`; amount/saturation/useRemaining podem ser alterados pelo event. O provider permanece autoridade sobre a barra, saturation, exhaustion e overflow.

## Findings de integração de alta importância

1. **Blood bar ≠ fluido cru.** Uma unidade de blood do jogador corresponde a **100 mB** de `vampirism:blood` quando o provider faz a conversão, mas a barra possui saturation/exhaustion e settlement próprios.
2. **Bat não debita blood diretamente.** Ele adiciona exhaustion; BloodStats pode posteriormente consumir blood por sua própria regra.
3. **Half Invulnerable usa settlement tardio.** Ativar a action não cobra blood. O custo default **4 blood** é cobrado apenas quando um hit qualificante é efetivamente bloqueado; se o pagamento falhar, a action é desativada.
4. **Actions têm cooldown/duration configuráveis.** Números do catálogo são defaults 1.10.13, não constantes universais.
5. **Lord progression é Task-driven.** Não existe justificativa para criar Lord XP paralelo.
6. **Servants já geram recursos.** `collect_blood` é um Minion Task provider-native e não deve ser duplicado por uma automação Black Arcana sem deduplicação explícita.
7. **Teleport 1.10.13 foi revalidado.** A implementação usa `DimensionTransition`, desmonta passenger e é bloqueada enquanto Bat está ativo.
8. **Natural regeneration não é lifesteal.** O blood/saturation loop cura nativamente; perks de vampirismo devem preservar a causalidade de dano/origem em vez de classificar `LivingHealEvent` genericamente.
9. **Reservatório grande pode usar o fluido real**, mas capacidade/volume do tanque não altera implicitamente a barra nativa 20/20 do jogador.
10. **Village capture tem hooks públicos próprios.** Completion-sensitive rewards devem preferir `VillagerCaptureFinish.Post`, não o início da captura.

## Estado de fechamento desta auditoria

O **catálogo granular base** do provider está fechado em source para 1.10.13: actions, skill registries/topologia, progressão normal/Lord, blood economy, tasks, minions, refinements, attributes, registries públicos, hooks/events e contrato Black Arcana foram documentados.

Isso **não** significa runtime QA confirmado e **não** incorpora automaticamente semântica de addons instalados.

## Fail-closed / runtime QA ainda necessário

Permanecem pendentes:

- validar os events e timers em dedicated server;
- validar persistência de ActionWheel/MinionTask na build instalada;
- validar settlement da barra de blood sob exhaustion, alimentação, itens, fluid handling e Half Invulnerable;
- validar interações Bat/flight com Epic Fight, stamina/movement e outros mods do pack;
- validar teleporte com portais/dimensões e demais mods de movimentação;
- validar Hunter Table/Trainer e Altares sob reload/interrupção;
- validar Lord Task rewards e ausência de duplicate settlement;
- validar village capture hooks em runtime;
- validar compatibilidade **Bloodlines 3.0.9** e **Vampire Spells Addon 0.0.9** antes de atribuir a eles qualquer override sobre Vampirism base;
- validar deduplicação de kills/tasks/village capture com progressão Black Arcana.

Até esses testes, o provider pode ser usado como autoridade documental/source-pinned, mas **não recebe estado de runtime QA confirmado**.
