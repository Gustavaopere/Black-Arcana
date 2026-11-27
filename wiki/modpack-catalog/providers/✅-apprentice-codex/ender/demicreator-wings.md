# Demi-creator Wings

**Estado do contrato:** ✅ `COMPLETE_PERK_READY` — `STATIC_TECHNICAL_CATALOG_ONLY` · `SHA_EXACT_BINARY_BEHAVIOR` · `mutating_hook=NOT_VERIFIED` · `physical_qa=NOT_TESTED`.

> O ✅ cobre exclusivamente a documentação estática SHA-exata deste objeto. Não homologa hook mutador, execução no pack, configuração efetiva, universo integral do provider nem QA físico.

## 1. Identidade e proveniência

| Campo | Valor verificado |
|---|---|
| Provider | Apprentice's Codex |
| Mod ID | `apprenticecodex` |
| Nome de exibição | Demi-creator Wings (nome funcional, não traduzido) |
| Registry ID | `apprenticecodex:demicreator_wings` |
| Host | Iron's Spells 'n Spellbooks (`AbstractSpell`) |
| Escola | `SchoolRegistry.ENDER_RESOURCE` (Ender) |
| Raridade mínima | `SpellRarity.EPIC` |
| Níveis | 1–3 (`DefaultConfig.setMaxLevel(3)`) |
| Tipo de cast | `CastType.LONG` |
| Cooldown declarado | `90.0` s |
| Recurso | Mana do Iron's (`baseManaCost=300`, `manaCostPerLevel=100`) |
| JAR exato | `apprentice_codex-1.0.1.1-mc1.21.1.jar` |
| SHA-256 do JAR | `9C5244E75DBCA95BDAF48A85F0C189F8456149D1220BAD5FF339A86BCE04AC86` |
| SHA-1 do JAR | `A3F9C73EBD77D15B7E77AE14F4D0F695FEC3B7CF` |
| Ambiente | Minecraft 1.21.1 · NeoForge · Java 21 (JDK 21.0.12 na inspeção) |
| Classe de implementação | `jp.aquafactory.apprenticecodex.spell.demicreatorwings.DemicreatorWings` |
| Evidência compartilhada | [`EXACT-TECHNICAL-CONTRACTS-1.0.1.1.md`](../EXACT-TECHNICAL-CONTRACTS-1.0.1.1.md) |

As versões 0.9.7.1 e 1.0.1 ficam registradas apenas como histórico; nenhum de seus valores foi reaproveitado sem confirmação no artefato físico 1.0.1.1.

## 2. Localizadores para o Codex

| Elemento | Localizador |
|---|---|
| Registro | `SpellRegistry.reg("demicreator_wings", DemicreatorWings::new)` |
| Config | `DemicreatorWings.config` (`new DefaultConfig().setMinRarity(EPIC).setSchoolResource(ENDER_RESOURCE).setMaxLevel(3).setCooldownSeconds(90.0).build()`) |
| Coeficientes | `DemicreatorWings.<init>()`: `baseSpellPower=800`, `spellPowerPerLevel=250`, `baseManaCost=300`, `manaCostPerLevel=100`, `castTime=40` |
| Área | `DemicreatorWings.getActivateArea(int,LivingEntity)` → `1 + Math.round(power/100.0F)` |
| Duração | `DemicreatorWings.getDuration(int,LivingEntity)` → `20 * Math.round(30.0F * power / 800.0F)` |
| Recast | `DemicreatorWings.getRecastCount(int,LivingEntity)` → `2` |
| Gate de cast | `DemicreatorWings.checkPreCastConditions(...)`: exige `Player`, recast de fechamento ou `ApprenticeCodexServerConfig.isDemicreatorWingsDimensionAllowed(...)` |
| Ciclo | `DemicreatorWings.onCast(...)` (abre/fecha), `onRecastFinished(...)`, `onServerCastComplete(...)` |
| Núcleo | `jp.aquafactory.apprenticecodex.spell.demicreatorwings.DemicreatorWingsCoreEntity` |
| Asa | `jp.aquafactory.apprenticecodex.spell.demicreatorwings.DemicreatorWingEntity` (`DemicreatorWingsWingEntity`) |
| Manager | `jp.aquafactory.apprenticecodex.spell.demicreatorwings.DemicreatorWingsManager` (`activate`, `deactivate`, `ensureFlightGranted`, `isInsideCoreArea`, `stripGrantedFlight`) |
| Evento de voo | `jp.aquafactory.apprenticecodex.spell.demicreatorwings.DemicreatorWingsFlightEvent` |
| Estado persistente | `capability.codexspelldata.spellstates.DemicreatorWingsState` (`active`, `coreEntityId`, `wingEntityId`, `grantedFlight`) |
| Config de dimensão | `config.spell.DemicreatorWingsServerConfig` → `SpellDimensionRestrictionServerConfig` |

Bytecode reconsultado no JAR 1.0.1.1: saída `scratch/javap1011_ender10.txt` (`javap -classpath <JAR> -p -s -c`, `EXIT=0`, 38 classes, SHA-256 `0095E23B21918E38B4BD7D6C47DA8C3503753F0F988C00AB04A786060E2C50E5`) e decompilação Vineflower consolidada em `scratch/ender10_sources.txt` (55 arquivos, SHA-256 `F3953EB8FCFB793EC501694E054E3C3CBE187E557B09B6CF158828692A97A645`).

## 3. Casting / execução

1. `AbstractSpell` resolve intenção, mana, cooldown e nível; `castTime=40` e `CastType.LONG`.
2. `checkPreCastConditions` exige `Player`. Com recast ativo: se o jogador não é `ServerPlayer` ou possui core ativo, grava `DemicreatorWingsCastData.closeCast()` e aprovoca o cast de fechamento; se o recast está obsoleto sem core, remove com `RecastResult.USED_ALL_RECASTS`. Sem recast, rejeita dimensões não permitidas pela config e grava `openCast()`.
3. `onCast` em `ServerPlayer`: `closeCast` → `DemicreatorWingsManager.deactivate(server,true)`; caso contrário `activate(server, spellLevel, castSource, playerMagicData, spell)`.
4. `activate` chama `deactivate(player,false)`, cria `DemicreatorWingsCoreEntity` com `getActivateArea(...)` e `getDuration(...)`, posiciona no jogador, cria `DemicreatorWingsWingEntity`, grava IDs/estado e registra `RecastInstance` com `getRecastCount(...)=2` e duração `getDuration(...)`.
5. `onRecastFinished` → `deactivate(player,false)`; `onServerCastComplete` limpa `additionalCastData`.

Coeficientes herdados de `AbstractSpell` (mana/cooldown/cast time/spell power) são declarados pelo addon; valores efetivos dependem da config instalada do Iron's, atributos, Curios e eventos — **NÃO VERIFICADOS**.

## 4. Targeting / geometria

| Propriedade | Valor e consumidor |
|---|---|
| Área de ativação | `1 + round(power/100)`; nominal **9 / 12 / 14** nos níveis 1–3 sem modificadores. Passada como `allowedRadius` ao `DemicreatorWingsCoreEntity`. |
| Duração | `20 * round(30*power/800)` ticks; nominal **600 / 780 / 980 ticks (30 / 39 / 49 s)**. Consumida pela entidade core e pelo `RecastInstance`. |
| Interpretação geométrica | `DemicreatorWingsManager.isInsideCoreArea(ServerPlayer,core)` testa `abs(player.x-core.x) <= core.getAllowedRadius()` **e** `abs(player.z-core.z) <= core.getAllowedRadius()`. **Não há condição Y nesse método**: a fronteira examinada é quadrada em X/Z, não esfera/volume 3D certificado. Regras de colisão da entidade core exigem auditoria separada. |
| Entidades gerenciadas | core + asa, ambas com owner (`TraceableEntity` no core) e IDs persistidos no estado. |

O valor de área é uma grandeza do manager; rotulá-lo como raio ou diâmetro sem evidência do consumidor não é permitido.

## 5. Resultado

- **Licença de voo:** `DemicreatorWingsManager.ensureFlightGranted` só opera com `state.active=true`, fora de `instabuild` e espectador; quando necessário marca `abilities.mayfly=true`, chama `onUpdateAbilities()` e registra `state.grantedFlight=true`.
- **Tick de voo:** `DemicreatorWingsFlightEvent.onPlayerTick(PlayerTickEvent.Pre)` desativa se o core não existe ou o jogador sai da área, revalida a asa e zera `fallDistance`.
- **Limpeza:** `deactivate` descarta core/asa, chama `stripGrantedFlight` e remove recast quando solicitado. `stripGrantedFlight` define `flying=false` e `mayfly=false` **somente se** `state.grantedFlight` estava ligado; não há negociação com outras fontes de `mayfly` nesse corpo. Login, logout, troca de dimensão e morte acionam limpeza.
- **Apresentação:** SoundRegistry `VANILLA_POWER_TUNING` (início) e `VANILLA_POWER_ACTIVATE` (fim); partículas da entidade core/asa pertencem ao provider.
- Limites do manager: `ALERT_THRESHOLD_TICKS=200`, `ALERT_FAST_THRESHOLD_TICKS=60`, `ALERT_INTERVAL_TICKS=20`, `ALERT_FAST_INTERVAL_TICKS=10`.

## 6. Scaling e caps

| Parâmetro | Fórmula literal | Unidade / ownership |
|---|---|---|
| Spell power | `800 + 250*(level-1)` | float; internamente `AbstractSpell.getSpellPower` aplica atributo, escola e multiplicador |
| Mana | `300 + 100*(level-1)` | Iron's mana; default declarado |
| Área | `1 + round(power/100)` | valor do manager; consumido como `allowedRadius` em X/Z |
| Duração | `20 * round(30*power/800)` | ticks |
| Recast | `2` | contagem Iron's |
| Cooldown | `90.0` s | `DefaultConfig` |
| gate de dimensão | `DemicreatorWingsServerConfig.isDimensionAllowed` | config do servidor; conteúdo instalado **NÃO VERIFICADO** |

## 7. Possibilidades de perks

- **A — atributo nativo:** spell power/mana/cooldown via `AbstractSpell`; contrato do host, não hook de mutação deste objeto.
- **B — evento/callback verificado:** `PlayerTickEvent.Pre` e os handlers de login/logout/morte são observadores do provider; a existência deles **não** autoriza alterar a área, a duração ou a licença de voo. `setForGameTest` de `DemicreatorWingsServerConfig` é utilitário de teste, não contrato de perk em runtime.
- **C — adapter condicionado:** mudar área/duração/recast exigiria substituir `DemicreatorWingsManager`/`DemicreatorWingsCoreEntity` com contrato explícito de owner, recast e limpeza de `mayfly`. **CONDICIONADO**.
- **D — sem hook demonstrado:** não há API/mixin seguro comprovado para transformar a licença de voo em área maior, estender duração ou conceder voo extra sem duplicar `mayfly`. **NO_MUTATION / fail-closed**.
- `mutating_hook = NOT_VERIFIED`.

## 8. Causalidade

`um cast → um core + uma asa → estado de voo → recast/timeout/saída da área → limpeza`.

Voo, ticks em voo e recast são uma sessão provider-owned. Black Arcana não deve criar segundo flag de voo nem duplicar duração/recast; RPG não deve pagar Mastery por tick de voo. A ausência de negociação com outras fontes de `mayfly` é risco real a testar, não bug universal comprovado.

## 9. Concepção de nova magia

Assinatura ocupada: "zona temporária limitada de voo criativo atrelada a core/recast". Uma magia Black Arcana original precisaria de semântica materialmente distinta (por exemplo, mobilidade sem concessão de `mayfly` ou sem núcleo persistente) para não duplicar esta identidade. Nenhuma implementação foi realizada.

## 10. Verificação e pendências

- ✅ Identidade/hash do JAR, registro, classe, construtor, fórmulas de área/duração, recast, geometria X/Z, licença de voo e limpeza confirmados no bytecode 1.0.1.1.
- ⚠️ Configuração efetiva de dimensão e multiplicadores instalados não lidos.
- ⚠️ `physical_qa=NOT_TESTED`: sem cliente, servidor, Survival, PvP, outras fontes de voo ou modpack real.
- ⚠️ Universo integral do provider não encerrado: recorte observado de 15 fichas Ender neste lote.

## Localizadores para Codex — resumo operacional

- `getActivateArea`/`getDuration` são métodos package-private da spell; não presumir setters mutáveis por perk.
- `isInsideCoreArea` é X/Z sem Y: qualquer alteração de geometria precisa demonstrar o consumidor e a autoridade do core.
- `stripGrantedFlight` só atua quando `state.grantedFlight=true`; não sobrescrever `mayfly` de terceiros.
- Consultar [`EXACT-TECHNICAL-CONTRACTS-1.0.1.1.md`](../EXACT-TECHNICAL-CONTRACTS-1.0.1.1.md) para hashes, comandos e limites da prova.
