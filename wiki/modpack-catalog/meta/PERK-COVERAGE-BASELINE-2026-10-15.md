# Black Arcana — baseline de cobertura por habilidade e por provider (2026-10-15)

**Natureza:** snapshot de coordenação de catálogo e dos eixos de engenharia de perks, sem alterar os contadores canônicos. A fonte operacional dinâmica continua em `SEMANTIC-MAGIC-COVERAGE.md`, `CATALOG-COVERAGE-CURRENT.md` e `plans/STATUS.md`; atualizar esta ficha após reconciliação, sem assumir que é o último checkpoint.

## Current tranche override — fifteen causal dossiers (2026-10-15, PR #825 draft)

**Iron's Spells 'n Spellbooks 3.16.3 — 15/110 spells têm fichas suplementares de leitura causal source-pinned nesta PR (13,64% das identidades).** É métrica **estritamente documental de auditoria**, não porcentagem de APIs seguras, adapters implementados, física do JAR ou QA. As 110 fichas individuais da PR #795 continuam em draft e em trabalho separado. O mínimo do ledger global **permanece 1.856 objetos semânticos / 1.854 no escopo restrito**, pois nenhuma destas magias é identidade nova; **denominador global final desconhecido (—%)**. O checkpoint 12/110 abaixo fica como histórico.

Novos dossiês, sem sobrescrever as fichas existentes:

- [Gluttony — mana em `LivingEntityUseItemEvent.Finish`](../providers/✅-irons-spells/audits/CAUSAL-PERKS-GLUTTONY-3.16.3.md): alimento `FoodProperties` com status GLUTTONY, `nutrition × ratioForAmplifier`, server `MagicData.addMana`, cap superior `MAX_MANA`, `ChangeManaEvent` e sync; sem segundo crédito/cast.
- [Devour — mandíbula e Vigor por kill](../providers/✅-irons-spells/audits/CAUSAL-PERKS-DEVOUR-3.16.3.md): target single raycast 9 blocos, `DevourJaw` em 13 ticks, lifesteal de 15% do dano `LivingDamageEvent.Post`, heal no kill e vida máxima temporária via `VIGOR` com amplifier cap 9; não confundir retorno do hit com kill.
- [Ray of Siphoning — canalização e roubo de vida](../providers/✅-irons-spells/audits/CAUSAL-PERKS-RAY-OF-SIPHONING-3.16.3.md): scheduler de player `CONTINUOUS_CAST_TICK_INTERVAL=10`, custo por chamada nativa e reserva de 2× mana cost para continuação, raycast 12 blocos independente do nível, `SpellDamageSource.setLifestealPercent(1f).indirect()`; hits/heals recorrentes pertencem a um canal e não são casts independentes.

**Barreiras:** ✅ documentação com provenance fixa; ⚠️ sem verificação do artefato físico, `CastSource` efetivo, eventos de terceiros, stacking, save/reload ou QA multiplayer; ⛔ mudanças per-perk de `DevourJaw`, geometria, cadência de canalização, tipo de dano e recursos de outro provider permanecem bloqueadas sem hook público estável e testes. Black Arcana governa apenas seu runtime, RPG Skill Tree progressão/gates/perks, Iron's rege as próprias magias.

## Current tranche override — twelve causal dossiers (2026-10-15, PR #825 draft)

**Iron's Spells 'n Spellbooks 3.16.3: 12/110 spells com dossiê causal suplementar nesta PR** — **10,91% da fila de 110**; isso representa escopo de *auditoria documental source-pinned*, **não** completion de hooks per-perk, adapter implementado, verificação binária, GameTest ou execução real. A PR #795 continua distinta com as 110 fichas de origem em draft. O checkpoint de 9/110 abaixo permanece histórico. Nenhum novo ID mágico foi acrescentado: **1.856 objetos semânticos mínimos globais / 1.854 no escopo restrito**; denominador final do universo global continua **aberto (—%)**.

Novas fichas desta tranche, como complementos individuais sem sobrescrever arquivos da PR #795:

- [Frostbite — eventos de morte e fan-out](../providers/✅-irons-spells/audits/CAUSAL-PERKS-FROSTBITE-3.16.3.md): buff no atacante, exigência `isFullyFrozen` na vítima, criação de `FrozenHumanoid`, atraso de 100 ticks, impacto AOE e oito shards com `ICICLE_SPELL` como damage source; owner/shatter/persistência separados.
- [Echoing Strikes — event Post e anti-recursão](../providers/✅-irons-spells/audits/CAUSAL-PERKS-ECHOING-STRIKES-3.16.3.md): `LivingDamageEvent.Post`, seletor dano melee/arrow, exclusão de `SpellDamageSource`, `hitCount=level+2`, attachment codificado, espada AOE de raio 2 e flecha após delay 15 ticks.
- [Sacrifice — cast direto vs morte marcada](../providers/✅-irons-spells/audits/CAUSAL-PERKS-SACRIFICE-3.16.3.md): dois ingressos e fórmulas diferentes, `IMagicSummon` própria/mark de DeadKing, `AABB.ofSize(radius,radius,radius)` com **raio nominal e cubo de candidatos distintos**, queda de dano e potencial propagação de mortes marcadas.

**Avaliação de interoperabilidade:** ✅ observação de fonte fixa e mapeamento causal por spell; ⚠️ JAR/mundo efetivo, morte cancelada, callbacks de terceiros, i-frames, identidade de dano derivado, persistência e limites de proc não foram testados; ⛔ sem hook público seguro, manter bloqueadas alterações per-perk de spawn/shape/quantidade de projéteis/cadeias de morte. O RPG Skill Tree permanece provider de progressão/perks, sem assumir o runtime do Iron's ou do Black Arcana.

## Current tranche override — nine causal dossiers (2026-10-15, PR #825 draft)

A PR #825 passou de seis para **9/110 magias do Iron's com dossiê suplementar de auditoria causal source-pinned** (**8,18% desta categoria documental**). O novo grupo cobre **Root, Slow e Abyssal Shroud**. O checkpoint de seis arquivos abaixo é histórico, não substitui este estado mais recente. O universo semântico **não** aumentou: **1.856 objetos mágicos mínimos globais / 1.854 no escopo estrito** permanecem os mesmos do ledger canônico. Denominador global final **desconhecido (—%)**. Não confundir 9/110 fichas suplementares com implementação de perks, prova binária ou homologação da API. A PR #795 continua aberta com as 110 fichas individuais em outra branch.

- [Root 3.16.3](../providers/✅-irons-spells/audits/CAUSAL-PERKS-ROOT-3.16.3.md): alvo único 32 blocos, `CANT_ROOT` verificado na execução final, root invocada e montada como veículo, HP independente do nível, duração por power, dismount guard, antimagia e NBT.
- [Slow 3.16.3](../providers/✅-irons-spells/audits/CAUSAL-PERKS-SLOW-3.16.3.md): aquisição 32 blocos, duração por power, amplificador por entity power multiplier, quatro modificadores de atributo com impacto diferenciado para mineração e casting, sem dano direto.
- [Abyssal Shroud 3.16.3](../providers/✅-irons-spells/audits/CAUSAL-PERKS-ABYSSAL-SHROUD-3.16.3.md): defesa própria por `LivingIncomingDamageEvent` e `ProjectileImpactEvent`, bypass tags, precedência `EVASION`, tentativa de deslocamento que nem sempre se concretiza e ausência de `SpellTeleportEvent` nesse caminho direto.

**Riscos confirmados na leitura source-pinned, sem declarar bug de JAR/gameplay:** `RootSpell` pode cobrar o cast antes da verificação final `CANT_ROOT`, `RootEntity` não serializa `target` explicitamente na própria classe; `AbyssalShroudEffect.doEffect` retorna true após tentativas condicionais de movimento, permitindo veto de dano mesmo sem `teleportTo`, e contém chamada `Vec3.yRot` cujo resultado não é guardado. `SlowSpell` não usa spell level diretamente na fórmula de intensidade do amplificador, embora o nível influencie sua duração. Todos exigem QA.

**Estado:** ✅ nove dossiês suplementares source-pinned na PR #825; ⚠️ prova binária e testes provider-native não executados para os três novos; ⛔ sem adapter per-player seguro de alvo/área/posição não comprovado. Stage 06.05/09 sem promoção.

## Current tranche override — six causal dossiers (2026-10-15, PR #825 draft)

A branch mantém **6/110 spells do Iron's com fichas suplementares de auditoria causal source-pinned**: Fireball, Chain Lightning, Counterspell, **Firebolt, Wall of Fire e Teleport**. Isso é **5,45% das 110 identidades** com *este tipo específico* de aprofundamento nesta PR, **não** percentual de APIs mutáveis, implementação de perks ou QA. A tranche anterior 3/110 é preservada como checkpoint histórico abaixo. Nenhum novo objeto semântico mágico foi introduzido: o mínimo do ledger permanece **1.856 global / 1.854 no escopo restrito**, sem denominador global final (—%). As **110 fichas da PR #795** continuam em draft, num trabalho paralelo distinto.

Novos dossiês, sem sobrescrever fichas individuais em `main` nem na PR #795:

- [Firebolt 3.16.3](../providers/✅-irons-spells/audits/CAUSAL-PERKS-FIREBOLT-3.16.3.md) — `0,5×0,5` hitbox, `1,75` bloco/tick, dano `0,5×power` e fire ticks 60.
- [Wall of Fire 3.16.3](../providers/✅-irons-spells/audits/CAUSAL-PERKS-WALL-OF-FIRE-3.16.3.md) — anchors/segmentos, `20` blocos por raycast, duração 240 ticks, risco de múltiplos hits/ticks, persistência e posição final a verificar.
- [Teleport 3.16.3](../providers/✅-irons-spells/audits/CAUSAL-PERKS-TELEPORT-3.16.3.md) — alcance com soft-cap e multiplicadores, dois ramos de destino, `SpellTeleportEvent` com veto e **setters de coordenadas herdados** comprovados no código-fonte NeoForge 1.21.1; equivalência física/API, revalidação de destino e VFX no veto continuam ⚠️.

**Status:** ✅ conteúdo documental source-pinned enviado à PR; ⚠️ paridade de comportamento com JAR físico, config efetiva, efeitos/client/server/Survival e hooks de adaptação não testados; ⛔ alterações de raio/target/hitbox/tempo de terceiros sem seam seguro. A autoridade runtime continua Black Arcana para seus spells e cada provider para sua própria execução; RPG Skill Tree é sibling de perks/progressão.

## Authority consultada para esta tranche

- `Black-Arcana/main@511ec03f0da62ebfc1722825def50354594976c3`.
- `Enshrouded/main@a41dbb51aacb94b7b5db6517f1514b0b7aee3e83`.
- `neoforge-rpg-skilltree/main@9e6436edb0049a8dcc4e47165db0f6850e5efa68`.
- O arquivo sibling `PROJECT-INSTRUCTIONS/modlist/modlist.md` certifica o último dump físico com **587 linhas top-level incluindo o modloader**. Duas adições pós-snapshot foram informadas, **sem novo JAR/dump físico certificado**; ordens de substituição também permanecem pendentes de refetch.
- Conferidos os PRs de Black Arcana em aberto, especialmente a **PR #795** (110 fichas Iron's source-pinned, **draft**) e tranches de prova binária independentes. Não tratar PR aberta como `main`.

## Progresso agregado

| Dimensão | Numerador confirmado | Denominador | Porcentagem admissível |
|---|---:|---:|---|
| Objetos mágicos semânticos estritamente reconstruíveis, universo geral | **1.856 (mínimo)** | Ainda aberto | **—%** |
| Objetos mágicos no escopo restrito registrado no ledger | **1.854 (mínimo)** | Ainda aberto | **—%** |
| Diretórios de provider classificados no checkpoint estrutural | **164** | **164 nesse checkpoint** | **100% estrutural do checkpoint**, não do universo semântico |
| Campanha focal de equivalência binária anotada no ledger em 15/10 | **35 exatos** | **39 da campanha** | **35/39**, não percentual global de catalogação |
| Magias com engenharia completa de perks, todos os mods | **não aferido** | **não aferido** | **—%** |

Os valores 1.856/1.854 e 35/39 são reproduzidos do topo corrente do ledger e do tracker de 15/10, sem deduzir magias novas. O histórico do `docs/catalog/GLOBAL-MAGIC-CATALOG.md` contém checkpoints anteriores 1.849/1.851, que não substituem o ledger mais recente.

## Medidores por provider — dimensões diferentes

| Provider / versão atual da evidência | Identidade ou ficha | Engenharia para perks | Situação |
|---|---|---|---|
| Iron's Spells 'n Spellbooks 3.16.3 | **110/110** fichas ativas já existem em `main`; a PR #795 propõe mapa source-pinned para **110/110** | A PR aprofundou a causalidade de 10 Blood e seis casos adicionais; **não** equivale a 110/110 hooks verificáveis; denominador de completude técnica pendente | ✅ inventário de identidades; 🟡 mapa técnico em PR **draft**; ⚠️ API/runtime |
| Ars Nouveau 5.13.1 | **109/109** identidades estáticas = 85 glyph parts + 24 rituais; registro compilado auditado | Matriz `PERK-ENGINEERING-MATRIX-5.13.1.md` localiza fonte para 85/85 partes; hooks e execução efetiva não homologados globalmente | ✅ IDs; ⚠️ perímetro de mutação |
| Epic Fight 21.17.3.1 | **43/43** skill IDs classificados; **3/3** ações sobrenaturais com ficha individual | Outras **40** habilidades não mágicas continuam relevantes ao RPG/perks; **não** converter 43/43 em cobertura técnica individual | ✅ classificação; ⚠️ perímetro de perks combate |
| Goety, Malum, Eidolon, addons e outros | Consultar ledger por versão física para denominadores exatos | Progressão por dossiê, sem porcentagem técnica fictícia | variável por provider |

**Nota de escopo:** `COUNTED_EXACT` atesta as propriedades demonstradas na prova binária (por exemplo, identidade estática/recipe empacotada), não garante range, dano, custo, consumo, loaded registry ou mutabilidade por API. A tabela explicita deliberadamente quando a fração de engenharia ainda não pode ser calculada.

## Tranche causal adicional — 15/10/2026 (PR #825, draft)

O trio de magias do Iron's Spellbooks 3.16.3 **Fireball, Chain Lightning e Counterspell** recebeu fichas **suplementares** por spell com execução/raycast/efeitos downstream, fórmulas, tipos de parâmetros e source links permanentes. A ordem geral de quatro eventos de perks também foi documentada. Essas alterações estão na **PR #825**, **não na main** nem na PR #795. Não surgiram novas identidades mágicas.

- **3/110** magias do Iron's têm **esta tranche específica** de leitura causal aprofundada, com fichas extra na branch; é uma métrica de execução deste lote, não uma estimativa da completude de todas as 110 fichas nem do trabalho concurrente. O total de engenharia plenamente verificada para perks **continua não aferido**. As 110 fichas da PR #795 permanecem um mapeamento source-pinned, em PR paralela.
- Fireball: [cálculo de dano/raio, projétil, colisão, world explosion](../providers/✅-irons-spells/audits/CAUSAL-PERKS-FIREBALL-3.16.3.md).
- Chain Lightning: [precast 32 blocos vs jump range, ondas de 6 ticks e caps](../providers/✅-irons-spells/audits/CAUSAL-PERKS-CHAIN-LIGHTNING-3.16.3.md).
- Counterspell: [raycast de 80 blocos, evento cancelável, anti-magic alvo](../providers/✅-irons-spells/audits/CAUSAL-PERKS-COUNTERSPELL-3.16.3.md).
- Cross-cutting: [ModifySpellLevel / PreCast / OnCast / SpellDamage / CounterSpell — ordem e riscos](../providers/✅-irons-spells/audits/CAUSAL-PERKS-EVENT-ORDER-3.16.3.md).

**Nova evidência crítica:** `SpellDamageEvent.setAmount` tem efeito antes do `hurt` em `LivingEntity` com `SpellDamageSource`. `SpellOnCastEvent.setManaCost` ocorre **depois** do gate de mana; desconto pós-gate não libera automaticamente casts originalmente inviáveis. `ModifySpellLevelEvent` é observado em `getLevelFor`, porém cobertura de todas as origens de casting ainda não está comprovada. **Nenhuma dessas descobertas autoriza anunciar adapter RPG implementado/testado, mudança de hitbox, alteração arbitrária de `DamageType` ou single-target→AOE.**

## Regra das duas barras nas respostas de catalogação

1. **Barra global:** `% da catalogação técnica completa`, somente com denominador completo e regra homogênea. Enquanto aberto, renderizar barra neutra, `—%` e mínimo estrito 1.856 como valor **não percentual**; não converter o mínimo em 100%.
2. **Barra do mod sendo trabalhado:** explicitar o eixo e o numerador/denominador, preferencialmente `fichas individuais com engenharia causal suficiente / objetos aplicáveis`; quando o eixo técnico não está fechado, exibir **subbarra de identidade** verificável (ex.: Iron's 110/110) junto de `engenharia pendente`. Na UI, dizer se a prova está na `main` ou apenas em PR.
3. Em mods como Epic Fight, manter **dois conjuntos**: 3/3 mágicos para o mínimo Black Arcana; 43/43 habilidades RPG a documentar, sem duplicar os três no numerador global.
4. Ao mudar versão, modlist física, datapacks, config ou source pin, não transportar percentual anterior sem reconciliação.

**Próxima ação específica:** não duplicar a PR #795 de Iron's; revisar causalidade/mutabilidade em seus casos prioritários, mantendo foco em targeting/range/damage/cooldown/hitbox e registrando explicitamente `SEM_HOOK_SEGURO`. Em paralelo, desenvolver uma trilha **RPG skill-card** para Epic Fight separada do numerador de magia. O uso desse baseline não autoriza antecipar o Stage 07 enquanto 06.05/Stage 09 mantêm seus gates.

Contratos aplicáveis: [padrão técnico](PERK-TECHNICAL-CATALOG-CONTRACT.md), [ledger semântico](SEMANTIC-MAGIC-COVERAGE.md), [cobertura atual](CATALOG-COVERAGE-CURRENT.md), [Epic Fight skills](../providers/✅-epic-fight/skills/SKILL-DISPOSITION-21.17.3.1.md), [Ars matrix](../providers/✅-ars-nouveau/PERK-ENGINEERING-MATRIX-5.13.1.md) e [PR #795](https://github.com/Gustavaopere/Black-Arcana/pull/795).
