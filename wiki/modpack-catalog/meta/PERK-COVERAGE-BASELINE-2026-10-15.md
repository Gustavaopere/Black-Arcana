# Black Arcana — baseline de cobertura por habilidade e por provider (2026-10-15)

**Natureza:** snapshot de coordenação de catálogo e dos eixos de engenharia de perks, sem alterar os contadores canônicos. A fonte operacional dinâmica continua em `SEMANTIC-MAGIC-COVERAGE.md`, `CATALOG-COVERAGE-CURRENT.md` e `plans/STATUS.md`; atualizar esta ficha após reconciliação, sem assumir que é o último checkpoint.

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
