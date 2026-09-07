# Bloodlines 3.0.9 — provider audit

Status: `SOURCE-PINNED 3.0.9 / CORE REGISTRIES + PROGRESSION + RESOURCE AUTHORITY CATALOGED / ACTION DETAIL + RUNTIME QA PENDENTES`

## Autoridade da versão

- mod id: `bloodlines`
- JAR instalado: `bloodlines-1.21-3.0.9.jar`
- runtime/version: `1.21-3.0.9`
- Minecraft: `1.21.1`
- loader: NeoForge
- provider base obrigatório: Vampirism `1.10.13`
- source oficial: `TheDrOfDoctoring/bloodlines`
- source pin exato usado nesta auditoria: `c8fd517d204d09dfcb9a544c17d7df87755eaa5c`

Esse commit é a autoridade escolhida porque contém as alterações da linha 3.0.9 e o próprio `gradle.properties` declara `mod_version=1.21-3.0.9`. O commit posterior em `master` observado durante a auditoria altera traduções, portanto não é necessário promovê-lo a autoridade mecânica desta build.

## O que Bloodlines é no pack

Bloodlines é um addon estrutural de Vampirism. Ele não cria uma engine mágica independente; ele amplia as facções Vampire/Hunter com uma segunda camada de identidade e progressão que reutiliza registries, `ISkill`, `ISkillTree`, `IAction`, `Task` e o `SkillHandler` de Vampirism.

A build 3.0.9 registra cinco bloodlines:

| Bloodline | Faction base | Skill tree |
|---|---|---|
| Noble | Vampire | `bloodlines:vampire/noble` |
| Zealot | Vampire | `bloodlines:vampire/zealot` |
| Ectotherm | Vampire | `bloodlines:vampire/ectotherm` |
| Bloodknight | Vampire | `bloodlines:vampire/bloodknight` |
| Gravebound | Hunter | `bloodlines:hunter/gravebound` |

O registry próprio de bloodlines é sincronizado e usa `bloodlines:empty` como default key. Cada `IBloodline` pertence a exatamente uma faction base.

## Inventário estrutural confirmado em source

| Superfície | Quantidade confirmada |
|---|---:|
| Bloodlines registradas | **5** |
| Vampire bloodlines | **4** |
| Hunter bloodlines | **1** |
| Bloodline skill trees | **5** |
| `ISkill` registrations, incluindo roots/rank skills | **101** |
| Noble skills | **19** |
| Zealot skills | **19** |
| Ectotherm skills | **19** |
| Bloodknight skills | **20** |
| Gravebound skills | **24** |
| `IAction` registrations | **29** |
| Rank tasks | **15** |
| Bloodline-perk tasks | **7** |
| Task keys Bloodlines | **22** |
| Bloodline ranks | **4 por bloodline** |
| Mob effects próprios auditados no core | **4** (`blood_frenzy`, `heinous_curse`, `cold_blooded`, `soul_rending`) |

## Autoridades provider-native

### Identidade, rank e state

`BloodlineManager` é um NeoForge attachment de player e é a autoridade sobre:

- bloodline atual;
- rank 0–4;
- wallet de Bloodline perk points;
- contador de Bloodline skills habilitadas;
- state específico da bloodline, quando existente;
- serialização/sincronização desses valores.

Trocar/remover bloodline desabilita as skills da bloodline anterior no `SkillHandler` do Vampirism, limpa os Bloodline perk points, limpa o state específico e força recálculo dos skill-tree locks.

### Rank

Rank é separado de perk points. `BloodlineParentSkill` representa os marcos de Rank 1–4 e não consome Bloodline perk point. Os ranks 2–4 são entregues por `BloodlineRankReward` através de tasks; o reward só aplica a transição se `currentRank == targetRank - 1`, impedindo skip direto pelo pipeline normal.

### Bloodline perk points

O wallet próprio persiste:

- `blSkillPoints` — pontos vindos de tasks;
- `blOtherSkillPoints` — pontos de outras fontes autorizadas;
- `blEnabledSkills` — número de Bloodline skills cobradas como habilitadas.

`remaining = max(0, taskSkillPoints + otherSkillPoints - enabledSkills)`.

`BloodlinePerkReward` adiciona pontos com `fromTask=true` e sincroniza o `BloodlineManager`.

### Skills

As Bloodline skills continuam registradas no `VampirismRegistries.Keys.SKILL`. As trees continuam sujeitas ao `SkillHandler` do Vampirism para node topology, parents, sibling exclusivity, tree locks e habilitação/desabilitação.

Bloodlines injeta gates adicionais:

- bloodline perk point disponível quando `requiresBloodlineSkillPoints()`;
- `requiredBloodlineRank()`;
- bloqueio de unlock manual para default/rank skills configuradas.

### Actions

As 29 actions são registradas diretamente em `VampirismRegistries.Keys.ACTION`. Portanto cooldown, duration, activation/deactivation e selection permanecem dentro do pipeline de `IActionHandler` do Vampirism, com gates adicionais da bloodline quando aplicáveis.

## Findings de alta importância

1. **Não existe justificativa para um segundo BloodlineManager Black Arcana.** Bloodline id/rank/points/state já possuem attachment próprio, NBT e sync.
2. **Bloodline perk points não são skill points comuns.** O addon mantém wallet próprio e UI própria.
3. **Existe uma discrepância estática a validar em runtime.** Bloodline skills com `getSkillPointCost() > 0` continuam passando pelo `SkillHandler.canSkillBeEnabled` do Vampirism, que verifica os skill points normais, enquanto Bloodlines também exige seu wallet próprio. O README do provider afirma que Bloodline skills usam Bloodline perk points *instead of regular skill points*. Não classificar como bug nem compensar externamente até runtime QA.
4. **O wallet próprio cobra uma unidade por skill habilitada**, mesmo quando `getSkillPointCost()` da skill é 2 ou 3. Isso reforça a necessidade de validar o dual-gate acima em runtime.
5. **Perk tasks são estruturalmente repetíveis.** Seus rewards chamam `resetUniqueTask`, que remove o estado de concluída e a instância unique no `TaskManager` do Vampirism. Gravebound possui `MaxPerkUnlocker` em três faixas e encerra a rota de task points em 15; Noble/Zealot/Ectotherm/Bloodknight não possuem esse cap adicional no source 3.0.9.
6. **`MaxPerkUnlocker.CODEC` possui nomes de campos invertidos nos getters.** O round-trip interno pode permanecer autoconsistente, mas datapacks externos devem tratar `maxPerkPoints`/`minPerkPoints` como superfície de risco até QA.
7. **Gravebound Souls são recurso próprio, não Soul Energy genérica.** O state persiste souls, max souls, total devoured, Phylactery, Mist Form e Possession. Sem Phylactery, `getMaxSouls()` retorna 4.
8. **Noble e Bloodknight alteram o settlement de sangue usando APIs/eventos de Vampirism.** Não bypassar `BloodDrinkEvent`, `VampirePlayer.drinkBlood`, `useBlood`, saturation ou exhaustion.
9. **Ectotherm possui uma referência estática a `ZEALOT_POISONED_STRIKE` no seu `onCrit`.** Como o Zealot handler também implementa Poisoned Strike, isso deve ser tratado como discrepância/QA cross-bloodline, não corrigido por inferência.
10. **Mudança de faction base remove a bloodline.** `PlayerFactionEvent.FactionLevelChanged` para level 0 ou troca de faction limpa o BloodlineManager e seus states.

## Joining/leaving confirmado

O README oficial e os hooks de source foram reconciliados:

- Noble: Vampire sem bloodline, Lord level mínimo configurável, Baron sob Weakness e abaixo do health threshold configurável, atacado com Lordslayer Injection; unique route pode ser desabilitada por config.
- Zealot: Vampire sem bloodline usa Zealot Ritual Catalyst no Zealot Altar; ritual server-side de 700 ticks, com join no tick restante 50; morrendo/interrompendo a entidade do player, o ritual aborta.
- Ectotherm: Vampire sem bloodline sob `Cold Blooded`, em água, sofrendo dano solar letal; o event é cancelado, `Cold Blooded` removido, Sunscreen aplicado e Ectotherm concedido.
- Bloodknight: Vampire sem bloodline que sobrevive até o término de `Heinous Curse`, quando a unique route está habilitada.
- Gravebound: Hunter sem bloodline sob `Soul Rending` + `Heinous Curse`, diante de dano letal e com Phylactery livre próxima; o dano é cancelado, a Phylactery recebe ownership e o novo Gravebound inicia com 10 souls.
- Leaving: a documentação oficial define Purity Injection como saída canônica; a remoção final deve sempre passar pelo `BloodlineManager`/helper do provider para limpar skills, points, state e Phylactery/possession corretamente.

## Documentos deste provider

- [`BLOODLINE-CATALOG.md`](./BLOODLINE-CATALOG.md): as cinco bloodlines, identity, joins, innate mechanics e recursos.
- [`SKILL-CATALOG.md`](./SKILL-CATALOG.md): inventário 101, custos/gates e topologias das cinco trees.
- [`ACTION-CATALOG.md`](./ACTION-CATALOG.md): registry 29/29, ownership e semântica auditada; números não revalidados ficam fail-closed.
- [`PROGRESSION-AND-TASKS.md`](./PROGRESSION-AND-TASKS.md): ranks, 22 tasks, rewards, repetibilidade e perk wallet.
- [`RESOURCE-AUTHORITY.md`](./RESOURCE-AUTHORITY.md): Vampirism blood vs Bloodlines bloodline points vs Gravebound souls/Phylactery.
- [`TECHNICAL-AUDIT.md`](./TECHNICAL-AUDIT.md): registries, attachment, events, mixins, discrepancies e QA gates.
- [`INTEGRATION-RULES.md`](./INTEGRATION-RULES.md): contrato Black Arcana ↔ Bloodlines/Vampirism.

## Estado de fechamento

O provider está source-pinned na build exata instalada e já possui registry, progressão, joining/leaving, trees, wallet e resource authority confirmados. O fechamento granular ainda exige concluir o detalhe de todas as 29 actions e números/config defaults relevantes, além de runtime QA da build instalada.

Não marcar `RUNTIME QA CONFIRMED`, não corrigir o dual-gate de points e não promover semântica de Vampire Spells Addon para Bloodlines antes da auditoria separada desse addon.