# Black Arcana — progresso de catalogação, cohort 2026-10-18

**Checkpoint documental com base em `Black-Arcana/main@511ec03f0da62ebfc1722825def50354594976c3` e modlist física indexada no `neoforge-rpg-skilltree/main@ed5b65b890767b406ce41127bcb793775263c7bd`.** Este arquivo distingue a cobertura dos objetos mágicos, a dos registros binários, o aprofundamento por campo e a habilitação real de perks.

## Barra 1 — universo de magias/rituais/ações sobrenaturais de todos os mods

**Total desconhecido — percentual global indeterminado.** O catálogo registra pelo menos **1.857 objetos semânticos na baseline de 13/10** (**1.855** no escopo mencionado naquele checkpoint), mas o universo final de objetos de todos os mods continua **sem denominador verificável**. Isto é um **piso**, não uma fração; não representar como `1857 / 1857 = 100%`. A PR draft #825 tem uma baseline operacional diferente, **mínimo 1.856 / 1.854**; reconciliar denominador e cortes antes de substituir uma baseline por outra.

Campanha de evidência física do recorte histórico **39 providers** na `main`: **25/39 = 64,1%** com prova binária exata no último checkpoint consolidado de 13/10; é uma **submétrica delimitada**, não a conclusão do catálogo global, não é cobertura de perks nem QA em cliente. PRs draft posteriores podem ter avançado a campanha mas não contam como `main`.

## Barra 2 — Somake Spells 1.0.9, provider trabalhado nesta tranche

**83/83 (100%)** — fichas de identidade de spells do release verificadas no registry exato e já presentes em `registry-1.0.9/`. **7/83 (8,43%)** — fichas que receberam **nesta tranche** um novo dossiê de gate de aquisição/perk por terem `allowCrafting()` próprio (3 retornos `false` constantes, 4 não constantes). **7/7 (100%)** — classes com overrides `allowCrafting()` cobertas por esse recorte de documentação. Isto não representa percentual de todas as fichas com hooks/perks implementáveis: a auditoria de causalidade dos efeitos e mecanismos para os outros 76 não foi aferida aqui.

`Somake 1.0.9` = ✅ catalogado estruturalmente, ⚠️ condicionado em configuração/reachability, ⛔ sem hook mutador homologado para a mudança destas skills. Nenhuma nova identidade estrita; nenhuma migração de runtime; Stage 06.05 continua 🟡 e Stage 09 depende da campanha física sob D035.

### Critérios de avanço, por mod

Para cada provider o acompanhamento deve sempre expor: `registrados confirmados / identificados`, `fichas com campos técnicos comprovados / objetos elegíveis`, `hooks mutadores validados / demandas de mutação` (quando houver denominador) e `QA físico`. Se qualquer denominador estiver aberto, usar **—%** e declarar explicitamente o escopo, sem completar com estimativas.

Fonte da tranche: [Somake — matriz de sete gates](../providers/✅-somake-spells/PERK-REACHABILITY-GATES-1.0.9.md). Fonte global: [catálogo canônico](CATALOGO-GLOBAL-MAGIAS.md), [pendências](PENDENCIAS-MAGICAS-ATUAIS.md) e [regras técnicas](PERK-READY-TECHNICAL-STANDARD.md).

## Continuação Somake — prova de métodos de crafting no JAR (18/10/2026)

[CI SHA-exata #39186593493](https://github.com/Gustavaopere/Black-Arcana/actions/runs/39186593493): **7/7 métodos de `allowCrafting()` com classe/descritor comprovados, 7/7 testes sintéticos**, incluindo quatro dependentes de três campos `Config.DISABLE_*` identificados no bytecode e três constantes `false`. Evidência estritamente estática/clean-room; [matriz compilada](../providers/✅-somake-spells/EXACT-BINARY-CRAFTING-METHOD-SEAMS-1.0.9.md). Barras inalteradas em seu escopo: global —% (denominador aberto), Somake identidades 83/83 (100%), aprofundamento **7/83 = 8,43% no recorte de métodos de aquisição**. Nenhuma QA física Survival, API de perk ou implementação nova inferida.

## Somake 1.0.9 — segundo eixo: descobertas compiladas de execução

[Java21 #39192999780](https://github.com/Gustavaopere/Black-Arcana/actions/runs/39192999780) **SUCCESS**, SHA-1 físico/publisher verificado. O novo probe compilado cobriu as **7/7 classes desta campanha**, encontrou 116 declarações de métodos (101 com nomes de interesse para inspeção), incluindo onCast, onServerCastTick, pre-cast, getters de dano/cura/raio/duração e referências a entidades downstream. A [matriz causal estática](../providers/✅-somake-spells/EXACT-BINARY-CAST-CALLSITES-1.0.9.md) e as sete fichas foram atualizadas. O primeiro run #39192927218 falhou pelo teto de 250 caracteres para uma referência JVM, corrigido para 2048 com teste negativo; a execução seguinte passou.

**Barras invariantes:** global **—%** (universo ainda sem denominador); Somake **83/83 = 100% identidades**. A campanha limitada de **métodos de cast/efeito cobre 7/83 = 8,43%** das fichas atuais, sem equivaler a profundidade causal de runtime, fórmula completa ou perks homologadas. Identidades novas +0; adapters +0; Stage 06.05 🟡; validações físicas/Survival ainda pendentes.

## Somake 1.0.9 — terceira camada: auditoria de entidades

**Fonte:** [GitHub Actions #39195233005](https://github.com/Gustavaopere/Black-Arcana/actions/runs/39195233005), Java 21, JAR Somake 1.0.9 com SHA-1 exata `171841ac9f802be9309ecc166c1d972ac6d404c0`, `SUCCESS`, **8 testes sintéticos**. O gate de cast dependente [#39195233020](https://github.com/Gustavaopere/Black-Arcana/actions/runs/39195233020) também passou. Inspeção estática, não QA de jogador/mundo.

- **Barra geral:** —% (denominador final do universo de todos os providers e ações semânticas ainda aberto). O checkpoint histórico de 1.857 objetos globais é piso, sem promoção desta campanha.
- **Somake — identidade de registry:** 83/83 = **100%**, mantido; novas identidades: **0**.
- **Somake — métodos de spell/casting:** 7/83 = **8,43%** das fichas receberam exploração de assinaturas/referências no lote anterior; não representa fórmula completa.
- **Somake — entidades downstream:** 5/83 = **6,02%** das fichas agora possuem nova referência binária de entidade específica auditada; **5/5 = 100% deste recorte fechado** (21 + 28 + 23 + 18 + 15 = 105 declarações e 15 + 22 + 17 + 15 + 9 = 78 métodos de interesse). A existência dessas cinco entidades não implica que as 78 rotinas tenham execução efetiva comprovada.
- **Hooks mutadores por jogador validados neste lote:** 0 (não inferir percentual sem denominador de demandas de perks). **Survival/provider-loaded/real-client**: ⚠️ pendentes; **perks de mutação**: ⛔ FAIL_CLOSED.

O scanner evidencia `LivingEntity.hurt` direto no Fragmented Sword Rain versus `DamageSources.applyDamage` no Vortex/Bell, além de filtragem de aliados/alvos e efeitos Wither/Blessing. Estes são símbolos compilados, não provas de que `SpellDamageEvent` seja consumido em todos os caminhos, de hitbox/raio numericamentes modificáveis ou de equivalência com o pack real. [Matriz exata](../providers/✅-somake-spells/EXACT-BINARY-ENTITY-CALLSITES-1.0.9.md).

**Próximo gate:** `FuneralBloomBudEntity` e `pulseDamage`/`tick` com dataflow, caps e coexistência de eventos; preservar autoridade do Somake, Iron's e RPG Skill Tree sem dupla cobrança/dano/Mastery. Stage 06.05 continua 🟡; Stage 09 preserva todos os gates físicos.

## Somake 1.0.9 — quarta camada: bud e impacto secundário (19/10/2026)

**Evidência auditada:** [Java21 #39197671447](https://github.com/Gustavaopere/Black-Arcana/actions/runs/39197671447) `SUCCESS`, **10 testes sintéticos**, classfile `FuneralBloomBudEntity` SHA-1 `171841ac9f802be9309ecc166c1d972ac6d404c0`, **26 métodos JVM** inspeccionados com o inicializador estático isolado. A primeira execução #39197533908 não é usada para a atribuição final de símbolos por possível contaminação da última rotina pelo `<clinit>`.

- **Barra global de todo o conteúdo mágico:** **—%**, denominador não determinado; piso histórico de pelo menos 1.857 objetos semânticos não recebe nova raiz por esta entidade.
- **Barra Somake — identidades da registry:** **83/83 = 100%** inventariadas no release, independente de reachability/castability.
- **Somake — fichas com auditoria de entidades downstream:** **5/83 = 6,02%** das identidades tiveram no mínimo uma entidade analisada no lote anterior; a Funeral Bloom é **a mesma identidade** enriquecida novamente, portanto o percentual não sobe.
- **Subescopo de classfiles downstream inspecionados:** seis classes distintas: `FragmentedSwordRainEntity`, `FuneralBloomControllerEntity`, `WitheredRoseVortexEntity`, `CustodiaCaeliSigilEntity`, `BellEntity` e agora `FuneralBloomBudEntity`. Uma sétima classe conhecida, `FuneralBloomImpactEntity`, foi referenciada pelo bud e **não** está inspecionada. Esse conjunto é apenas a cadeia descoberta até agora; não apresenta percentual global de todas as entidades do mod.
- **0** novos spells, **0** adapters mutadores homologados. Dano/Wither/cura/impulso/NBT foram identificados como símbolos do bud, não há fórmula numérica ou execução física comprovada.

**Autoridades e gates:** Somake mantém runtime do provider; Iron's mantém host/recursos/dano host; RPG Skill Tree atributos/perks/Mastery por boundary efetivo; Black Arcana rege seu próprio runtime. Stage 06.05 🟡, Stage 09 físico PENDING sob D035. [Dossiê do bud](../providers/✅-somake-spells/EXACT-BINARY-FUNERAL-BLOOM-BUD-1.0.9.md).

## Somake 1.0.9 — quinta camada: entidade Funeral Bloom Impact (19/10/2026)

- [Java21 #39198753251](https://github.com/Gustavaopere/Black-Arcana/actions/runs/39198753251) `SUCCESS`, publisher File 8867079/ SHA-1 `171841ac9f802be9309ecc166c1d972ac6d404c0`, **sete testes sintéticos**, classe `FuneralBloomImpactEntity` com **8 métodos nomeados** (Scale sincronizado, `setScale` com `Mth.clamp`, abertura com `tickCount/smoothstep`, `tick/discard`, NBT de Scale).
- **Global —%**: número total de magias/rituais/ações e universo de mods ainda não denominados; não promover completude do catálogo.
- **Somake — registry 83/83 = 100% identidades**; **5/83 = 6,02%** das fichas com pelo menos uma auditoria de entidade downstream, sem alteração. A Funeral Bloom continua sendo a mesma magia.
- **7 classfiles downstream distintos inspecionados** neste recorte acumulado: cinco do primeiro lote, `FuneralBloomBudEntity` e agora `FuneralBloomImpactEntity`. Não é prova de que todas as entidades mágicas do Somake foram encontradas.
- **0 novas identidades; 0 adapters mutadores certificados**. Nenhum callsite direto de dano, cura ou status apareceu nos oito métodos da entidade de impacto, o que não exclui execução herdada/delegada. A natureza exclusivamente visual permanece hipótese.

**Gates:** custos e cooldown permanecem owner Iron's; Black Arcana conserva apenas seu runtime; RPG Skill Tree fornece perks/Mastery por contrato real. Stage 06.05 🟡, Stage 09 físico pendente sob D035. Próxima prioridade é análise de constantes, dataflow de `FuneralBloomBudEntity.impact`/controller e perfil real provider-loaded. [Dossiê exato](../providers/✅-somake-spells/EXACT-BINARY-FUNERAL-BLOOM-IMPACT-1.0.9.md).

## Somake 1.0.9 — sexta camada: prova aritmética JVM da Funeral Bloom (19/10/2026)

- **Fonte física exata:** CurseForge File 8867079, `somakespells-1.0.9-1.21.1.jar`, SHA-1 `171841ac9f802be9309ecc166c1d972ac6d404c0`; sibling modlist `neoforge-rpg-skilltree/main@ed5b65b890767b406ce41127bcb793775263c7bd`.
- **Auditoria numérica Java21 [#39201393631](https://github.com/Gustavaopere/Black-Arcana/actions/runs/39201393631):** `SUCCESS` em 15 testes sintéticos/integrados, 4 classfiles e 17 métodos. As cinco provas de getter `int` são derivadas por avaliador JVM estritamente linear, com fluxos ramificados/não suportados rejeitados. O HEAD final será atualizado com snapshots de fórmulas para fail-closed.
- **Fórmulas comprovadas** para `L=clamp(level,1,5)`: `getMaxTargets=4+L`, `getDuration=240+20*(L-1)`, `getWaveInterval=18-L`, `getWitherDuration=60+12*L`. `getTelegraphTicks=max(9,13-jvm_idiv(level,2))` usa `level` sem clamp e semântica de divisão inteira Java.
- **Limites de clamp diretamente demonstrados** em callsites: `FuneralBloomSpell.getRadius` passa 10.0/15.0 como segundo/terceiro argumentos, `FuneralBloomImpactEntity.setScale` passa 0.65/1.6, `getOpenProgress` passa 0/1 em duas chamadas. Isto **não** é prova da dimensão final ou da possibilidade de perk alterar o método.
- **Barra global:** —% (denominador completo de mods/magias/ações mágicas ainda sem prova); piso histórico 1.857 objetos não alterado.
- **Barra Somake — registry:** **83/83 = 100%** identidades; **5/83 = 6,02%** fichas com auditoria de uma ou mais entidades downstream; 7 classfiles distintos permanecem no acumulado. O novo probe examina 4 classes **já conhecidas**, sem aumentar as contagens.
- **0** novas magias, **0** adapters de mutação homologados, **0** validações Survival/cliente provadas neste incremento.

**Critérios pendentes:** aplicar as expressões aos consumidores da versão exata, identificar unidade de duração/raio/ticks, dados de SpellPower/escola/branch, proteger contra duplicação de dano/cura/Mastery, e executar QA provider-loaded/multiplayer/Survival do modpack. Stage 06.05 segue 🟡; Stage 09 condicionado conforme D035. [Dossiê numérico](../providers/✅-somake-spells/EXACT-BINARY-FUNERAL-BLOOM-NUMERIC-1.0.9.md).

## Somake 1.0.9 — sétima camada: dataflow float de dano da Funeral Bloom (19/10/2026)

- Artefato: `somakespells-1.0.9-1.21.1.jar`, publisher CurseForge File 8867079, SHA-1 `171841ac9f802be9309ecc166c1d972ac6d404c0` (modlist sibling `neoforge-rpg-skilltree/main@ed5b65b890767b406ce41127bcb793775263c7bd`).
- [Auditoria Java21 #39243467444](https://github.com/Gustavaopere/Black-Arcana/actions/runs/39243467444): `SUCCESS`, **10 testes** de interpretação abstrata tipada (inclui Java compilado), prova integral do **retorno float** de `FuneralBloomSpell.getImpactDamage(int,LivingEntity)` como `1.5f + (getSpellPower(level_input,caster)*0.75f)` (0 branches, 1 chamada externa tipada); `getRadius` retorna `NOT_PROVED / branch_or_throw` por ter 2 branches, embora clamp 10.0f/15.0f esteja identificado.
- A PR também inclui regressões de snapshot negativas para impedir que uma mudança no JAR seja interpretada como prova do mesmo retorno; o gate final do HEAD será verificado separadamente.
- **Barra global:** —% (universo de spells/rituais/poderes e providers não fechado; piso histórico >=1857 ações/objetos não é denominador).
- **Barra Somake — identidades:** 83/83 = **100%** catalogadas. **5/83 = 6,02%** fichas com auditoria de pelo menos uma entidade downstream, sem incremento; sete classes downstream acumuladas (não novas magias). A análise presente adiciona profundidade a `somakespells:funeral_bloom`, não cobertura de novos IDs.
- **Perks de alteração de dano/área aprovadas:** **0**; `FAIL_CLOSED` até API/evento/callback per-player versionado e prova de causalidade downstream. Sem alterações em Black Arcana runtime, host Iron's, RPG Skill Tree, Mastery, custo ou cooldown.

**Pendências:** CFG completo de `getRadius`/`SchoolType.getPowerFor`, origem e configuração de `getSpellPower` no host 3.16.3, consumo do `impactDamage` pelo bud, dano efetivo/Wither/cura/knockback, bounds, FPS/carga, cliente/multiplayer/Survival e modpack físico (D035). Stage 06.05 permanece 🟡; Stage 09 condicionado. [Dossiê float](../providers/✅-somake-spells/EXACT-BINARY-FUNERAL-BLOOM-FLOAT-DATAFLOW-1.0.9.md).

## Somake 1.0.9 — oitava camada: CFG do raio e assinatura do host Iron's (19/10/2026)

- [Java21 #39246133056](https://github.com/Gustavaopere/Black-Arcana/actions/runs/39246133056) `SUCCESS` — nove testes sintéticos e dois JARs de release específica. Somake File 8867079 SHA-1 `171841ac9f802be9309ecc166c1d972ac6d404c0`; API Iron's 3.16.3 SHA-256 `69e81104a9fd31a402d9c89ab09c2a6b2fd6d2ab98db5a37bb159517363ee9ad`. CI final de PR será registrado separadamente.
- ✅ `getImpactDamage` do Somake chama `getSpellPower(int,Entity):float`; assinatura encontrada no `AbstractSpell` da API oficial. ⚠️ Corpo do método API referencia `SpellConfigManager.getSpellConfigValue`, `SchoolType.getPowerFor` e `LivingEntity.getAttributeValue`, sem prova de fórmula/config/atributo real do RPG Skill Tree.
- ✅ CFG estrutural de `getRadius`: 28 instruções alcançáveis, `ifnonnull` + `goto`, uma junção/retorno e clamp 10.0f/15.0f. ⚠️ Condição concreta e fórmula integral do raio permanecem sem prova.
- **Barra global:** —% (denominador não estabelecido; piso histórico de >=1.857 objetos semânticos, sem aumento). **Barra Somake:** 83/83 identidades = 100% inventariadas; 5/83 (6,02%) fichas com auditoria downstream, sete classfiles distintos anteriormente examinados. Esta rodada aprofunda a mesma magia, não acrescenta IDs ou classfiles de efeito.
- **Hooks per-player validados nesta rodada:** 0; ⛔ `FAIL_CLOSED`. Black Arcana mantém apenas seu runtime; Somake efeitos provider-native; Iron's host; RPG Skill Tree somente progressão com contrato real. Stage 06.05 🟡 e Stage 09 condicionado sob D035.

[Relatório técnico de CFG/host](../providers/✅-somake-spells/EXACT-BINARY-FUNERAL-BLOOM-RADIUS-IRONS-1.0.9.md).

## Somake 1.0.9 — nona camada: duas fórmulas de ramo do raio (19/10/2026)

- [Java21 #39259507432](https://github.com/Gustavaopere/Black-Arcana/actions/runs/39259507432) `SUCCESS`, dez testes sintéticos/negativos e fixture Java21, JAR Somake File 8867079 SHA-1 `171841ac9f802be9309ecc166c1d972ac6d404c0`: o interpretador JVM tipado validou os 28 opcodes do `getRadius` nos dois caminhos de `ifnonnull(caster)`, guard `caster == null` ou `caster != null`.
- ✅ Retorno de raio: `clamp_f32((9.5 + i2f(level)*0.82) + max_f32(0, P-1)*0.65, 10,15)` para caster não nulo, com `P=d2f(SchoolType.getPowerFor(caster))`; mesmo cálculo com `P=1` para caster nulo. São representações matemáticas das operações float32 do JAR; sem prova de raio/hitbox/alcance aplicados em jogo.
- ✅ Agora há **sete getters com expressões JVM de retorno examinadas nesta cadeia específica da Funeral Bloom**: cinco inteiros, `getImpactDamage` float e `getRadius` float por dois caminhos. Não contar os dois ramos como duas magias ou duas identidades independentes.
- **Barra global:** —%, denominador final não comprovado; piso histórico de pelo menos 1.857 objetos semânticos sem variação neste incremento.
- **Barra Somake (identidades):** **83/83 = 100%** dos IDs da registry; **5/83 = 6,02%** fichas com entidades downstream auditadas (cohort anterior), sete classfiles distintos de entidades já examinados; não houve nova magia nem nova classe nesta PR.
- **Integração:** 0 adapters mutadores per-player homologados. ⛔ `FAIL_CLOSED` para perks de área/dano/tempo/targets até provar consumidores/eventos/atributos/config e QA provider-loaded; Stage 06.05 🟡; Stage 09 condicionado sob D035.

[Dossiê tipado de ramo e raio](../providers/✅-somake-spells/EXACT-BINARY-FUNERAL-BLOOM-RADIUS-TYPED-1.0.9.md).

## Somake 1.0.9 — décima camada: consumidores de área da Funeral Bloom (19/10/2026)

- [Java21 #39262591589](https://github.com/Gustavaopere/Black-Arcana/actions/runs/39262591589), **SUCCESS / 9 testes**: inspeção SHA-exata de `FuneralBloomSpell`, `FuneralBloomControllerEntity`, `FuneralBloomBudEntity` em seis métodos. Somake File 8867079, SHA-1 `171841ac9f802be9309ecc166c1d972ac6d404c0`.
- `Spell.onCast`: 81 instruções, chamada `getRadius(int,LivingEntity)` e construção da controller com dois argumentos float. `Controller.tick`: 156 instruções, chama `getRadius()` e `launchWave`. `Controller.launchWave`: 196 instruções, `getRadius()`, `AABB.inflate`, `ServerLevel.getEntitiesOfClass` e construção de buds. `Bud.impact`: 279 instruções, outra `AABB.inflate`, query de entidades, `DamageSources.applyDamage`, `SpellHealEvent`/`heal`, sem chamada direta `getRadius`.
- ⚠️ **Não concluir** que o getter determina ambas as AABB: callsites por método não demonstram dataflow do float nos construtores, operandos `inflate`, ramificações nem efeito recebido por entidade. `invokedynamic` permanece sem destino de callback reconstruído.
- **Barra global:** —% (denominador de todos mods/actions ainda aberto); piso histórico >=1857 objetos semânticos sem aumento.
- **Barra Somake:** **83/83 = 100%** identidades registry, **5/83 = 6,02%** fichas com entidades downstream auditadas na campanha, sete classfiles de entidades distintos já conhecidos. Novo lote de callsites em três classes **existentes**, sem nova magia ou entidade adicional.
- **Perks mutadoras homologadas:** 0. ⛔ `FAIL_CLOSED`; Stage 06.05 🟡 e Stage 09 condicionado (D035). RPG Skill Tree fornece progressão sem controlar casting/efeitos do Black Arcana ou dos providers.

[Dossiê de consumidores do raio](../providers/✅-somake-spells/EXACT-BINARY-FUNERAL-BLOOM-RADIUS-CONSUMERS-1.0.9.md).

## Somake 1.0.9 — décima primeira camada: tentativa de vínculo construtor → raio (19/10/2026)

- [Auditoria exata #39286470816](https://github.com/Gustavaopere/Black-Arcana/actions/runs/39286470816): `SUCCESS` com 13 testes Java21 e SHA-1 físico Somake 1.0.9 `171841ac9f802be9309ecc166c1d972ac6d404c0`.
- **Resultado da prova:** `FuneralBloomControllerEntity.getRadius()` não é o getter direto de três opcodes esperado pelo scanner (`NOT_PROVED`). Por consequência, ainda não foi demonstrado qual dos dois floats do construtor (slots JVM 3 e 8) origina o getter. Esta é uma rejeição **restrita ao padrão direto**, não uma incompatibilidade do mod.
- **Revisão subsequente na PR #837:** agrega metadados estruturais (contagens, campos `float` e referências) para determinar a próxima auditoria; a execução no HEAD final ainda precisa ser comprovada.
- **Barra global:** —% (denominador total indisponível; piso histórico >=1.857 objetos semânticos sem alteração). **Somake:** 83/83 identidades = 100%; 5/83 fichas com entidades downstream = 6,02%; as sete classes downstream conhecidas e o conjunto de magias permanecem inalterados.
- **Integração:** zero novas interfaces mutadoras; ⛔ `FAIL_CLOSED`; Stage 06.05 🟡 e Stage 09 condicionado sob D035. Sem promover status com base em testes sintéticos ou na presença de callsites.

[Dossiê de auditoria do construtor/raio](../providers/✅-somake-spells/EXACT-BINARY-FUNERAL-BLOOM-CONTROLLER-RADIUS-1.0.9.md).

## Somake 1.0.9 — décima segunda camada: `DATA_RADIUS` sincronizado (19/10/2026)

- **JAR exato** File 8867079 SHA-1 `171841ac9f802be9309ecc166c1d972ac6d404c0`. [Java21 #39288405552](https://github.com/Gustavaopere/Black-Arcana/actions/runs/39288405552), `SUCCESS` 16 testes, prova do caminho `FuneralBloomControllerEntity.getRadius():float → SynchedEntityData.get(DATA_RADIUS) → Float.floatValue()`. O getter possui sete instruções, 0 branches, 0 operações aritméticas e um único retorno.
- [Varredura de 30 métodos #39289130886](https://github.com/Gustavaopere/Black-Arcana/actions/runs/39289130886), `SUCCESS`: `defineSynchedData`, `getRadius`, `setRadius(float)` referenciam o accessor; `setRadius` também possui referências a `Float.valueOf` e `SynchedEntityData.set`. A escrita direta no construtor e a interpretação completa do setter continuam `NOT_PROVED`.
- **Contagens inalteradas:** global —% (denominador desconhecido; piso histórico >=1.857 objetos); Somake **83/83 (100%)** identidades, **5/83 (6,02%)** fichas com entidades downstream auditadas e sete classfiles downstream no conjunto anterior. Novo trabalho aprofunda a mesma entidade e não adiciona ID de magia.
- **Bloqueios:** `0` adapters de alteração do raio homologados; ⛔ `FAIL_CLOSED` para perks sem contrato; Stage 06.05 🟡 e Stage 09 condicionado conforme D035. [Dossiê](../providers/✅-somake-spells/EXACT-BINARY-FUNERAL-BLOOM-CONTROLLER-RADIUS-1.0.9.md).

## Continuação da campanha — Somake Funeral Bloom: construtor → raio interno (19/10/2026, PR #838)

**Barra geral — magias, rituais e ações sobrenaturais de todos os mods:** **—%** porque o denominador global segue aberto. Pisos históricos divergem entre **1.856** (reconciliação Requiem) e **1.857** objetos; usar conservadoramente `>=1.856`, sem somar entidades, helpers ou as mesmas magias repetidas. Nenhuma nova raiz foi identificada neste lote.

**Barra Somake 1.0.9 — identidades de spells:** **83/83 = 100%** da registry física, não 100% dos dados causais nem de perks. **Profundidade de efeitos downstream no recorte acumulado:** **5/83 = 6,02%** fichas de origem com entidade auditada, sete classfiles downstream distintos observados; esta prova aprofunda a Funeral Bloom já contada, sem aumentar 5/83. **Perks de mutação homologadas: 0**; percentual de cobertura de mutações permanece —% por falta de denominador de demandas/hook testado.

**Nova evidência de artefato exato:** [workflow SHA-exato #39292948277](https://github.com/Gustavaopere/Black-Arcana/actions/runs/39292948277), `SUCCESS`, Java 21, 31 testes até HEAD `db24ea457eaa24c977d990ddf199ff4bc968c60c`. JAR Somake File 8867079 SHA-1 `171841ac9f802be9309ecc166c1d972ac6d404c0`.

- ✅ `FuneralBloomControllerEntity.<init>(Level,LivingEntity,float,int,int,int,int,float,int,int)`: primeiro `float` no slot JVM **3** passado diretamente à chamada interna `setRadius(float)`; segundo `float` slot **8** não é associado ao raio pela presente prova.
- ✅ `setRadius(float)`: caminho linear integral de **10 opcodes** com `Mth.clamp:(FFF)F` e limites **6.0f / 18.0f**, `Float.valueOf` e `SynchedEntityData.set(DATA_RADIUS,...)`.
- ✅ `getRadius():float`: `SynchedEntityData.get(DATA_RADIUS)`, `Float.floatValue()` (prova de leitura antecedente preservada).
- ⚠️ Não aferidos o stack dos argumentos de `FuneralBloomSpell.onCast`, uso do valor nos operandos `AABB.inflate` de controller/bud, configuração e targeting/raio de impacto reais.
- ⛔ Sem hook oficial de mutação per-player, adapter do RPG Skill Tree ou QA real do modpack: **FAIL_CLOSED**. Stage 06.05 🟡, Stage 09 físico PENDING sob D035.

As três relações locais acima **superam o resultado negativo anterior referente ao setter de sete opcodes**, sem invalidar o registro histórico de sua rejeição. Testes negativos adicionais da PR #838 e o CI do HEAD final exigem observação separada, antes de merge. [Dossiê](../providers/✅-somake-spells/EXACT-BINARY-FUNERAL-BLOOM-CONTROLLER-RADIUS-1.0.9.md) e [ficha individual](../providers/✅-somake-spells/registry-1.0.9/funeral-bloom.md).

## Continuação Somake — proveniência do raio a partir de `onCast` (19/10/2026, PR #839)

- **Barra geral de todas as magias/rituais/ações sobrenaturais:** **—%**, universo/denominador definitivo ainda aberto. Adotar piso histórico conservador `>=1.856` enquanto os checkpoints `1.856 / 1.857` não forem integralmente reconciliados. A análise de callsite **não acrescenta uma identidade**.
- **Barra Somake 1.0.9 (identidades registradas):** **83/83 = 100%**. **Subbarra de fichas com auditoria downstream nesta campanha:** **5/83 = 6,02%**. Esta prova é da mesma Funeral Bloom, já contada; não aumenta a segunda barra. Mutadores per-player homologados: **0** (sem denominador total de demandas verificadas, percentual —%).
- [Java21 SHA-exata #39296264174](https://github.com/Gustavaopere/Black-Arcana/actions/runs/39296264174): `SUCCESS`, **45 testes**. Scanner de pilha JVM com janela estrita de **31 instruções** comprovou que o retorno de `FuneralBloomSpell.getRadius(int,LivingEntity):float` é diretamente o **primeiro argumento float (ordinal 3)** da `FuneralBloomControllerEntity`. Somado às provas anteriores (#838), encerra a causalidade estática **callsite getter → construtor float slot 3 → setter clamp 6–18 → SynchedEntityData.DATA_RADIUS → getter da controller**. A prova independente do `getRadius` do spell documenta clamp `10–15` no retorno para entradas finitas.
- **Pendências mantidas:** `onCast` origem efetiva dos parâmetros do getter e do segundo float, operandos de `AABB.inflate` em `launchWave` e `bud.impact`, efeitos/dano/cura por alvo, configs efetivas/Survival, cliente, multiplayer/claims e contrato público de mudança por perk. ⛔ `FAIL_CLOSED`; Stage 06.05 🟡, Stage 09 físico PENDING; nenhuma promoção de Stage.

Provas por método em [dossiê de radius controller](../providers/✅-somake-spells/EXACT-BINARY-FUNERAL-BLOOM-CONTROLLER-RADIUS-1.0.9.md) e [ficha individual](../providers/✅-somake-spells/registry-1.0.9/funeral-bloom.md). Esta evidência é estática/clean-room, sem exportar código ou bytecode de terceiros.
