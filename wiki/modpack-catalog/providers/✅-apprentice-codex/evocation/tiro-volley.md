# Tiro Volley

**Estado do contrato:** ✅ `COMPLETE_PERK_READY` — `STATIC_TECHNICAL_CATALOG_ONLY` · `SHA_EXACT_BINARY_BEHAVIOR` · `mutating_hook=NOT_VERIFIED` · `mutation=NO_MUTATION` · `physical_qa=NOT_TESTED` · `perk_certification=NOT_CERTIFIED`.

> O ✅ cobre exclusivamente a documentação estática SHA-exata deste objeto. Não homologa hook mutador, execução no pack, configuração efetiva, universo integral do provider nem QA físico.

## 1. Identidade e proveniência

| Campo | Valor verificado |
|---|---|
| Provider | Apprentice's Codex |
| Mod ID | `apprenticecodex` |
| Registry ID | `apprenticecodex:tiro_volley` |
| Host | Iron's Spells 'n Spellbooks (`AbstractSpell`) |
| Interfaces | `ICastHighlightSpell`, `IMagiAgentSuitAffectedSpell`; `TiroVolleyMusketEntity`, `TiroVolleyCastData` e `DamageTypes.TIRO_VOLLEY` pertencem à mesma raiz |
| Escola | `SchoolRegistry.EVOCATION_RESOURCE` (Evocation) |
| Raridade mínima declarada | `RARE` |
| Níveis declarados | 1–3 (`setMaxLevel(3)`) |
| Tipo de cast | `CONTINUOUS` |
| Cooldown declarado | `20.0 s` |
| Recurso | Mana do Iron's (`baseManaCost=13`, `manaCostPerLevel=3`) |
| JAR exato | `apprentice_codex-1.0.1.1-mc1.21.1.jar` |
| SHA-256 do JAR | `9C5244E75DBCA95BDAF48A85F0C189F8456149D1220BAD5FF339A86BCE04AC86` |
| SHA-1 do JAR | `A3F9C73EBD77D15B7E77AE14F4D0F695FEC3B7CF` |
| Ambiente | Minecraft 1.21.1 · NeoForge · Java 21 (JDK 21.0.12 na inspeção) |
| Classe de implementação | `jp.aquafactory.apprenticecodex.spell.tirovolley.TiroVolley` |
| Auxiliares da mesma raiz | `TiroVolleyMusketEntity`, `TiroVolleyCastData`, `SummonedFirearmTools`, `GunSpellTracerPacket`, `DamageTypes.TIRO_VOLLEY` |
| Evidência compartilhada | [`EXACT-TECHNICAL-CONTRACTS-1.0.1.1.md`](../EXACT-TECHNICAL-CONTRACTS-1.0.1.1.md) |

As versões 0.9.7.1 e 1.0.1 permanecem como histórico; nenhum valor foi reaproveitado sem confirmação no artefato físico 1.0.1.1. Os coeficientes declarados não são os valores efetivos instalados: mana, cooldown, spell power, nível, raridade e multiplicadores do host permanecem `NÃO VERIFICADOS` (`AbstractSpell` lê `SpellConfigManager`, atributos, Curios e eventos).

## 2. Localizadores para o Codex

| Elemento | Localizador |
|---|---|
| Registro | `SpellRegistry.reg("tiro_volley", TiroVolley::new)` |
| Config | `RARE`, nível 3, cooldown `20.0`, `EVOCATION_RESOURCE` |
| Coeficientes | <init>: `baseSpellPower=100`, `spellPowerPerLevel=100`, `baseManaCost=13`, `manaCostPerLevel=3`, `castTime=200` |
| Dano | `getDamage(power)` → `(4.0F + power/1000.0F) * damageMultiplier(TIRO_VOLLEY)` |
| Cadência | `getMusketsPerSecond` → `clamp(2.0 + (power-100)*0.015, 1.0, 10.0)` |
| Agendamento | `BASE_FIRE_DELAY_TICKS=20`, `ticksPerMusket=20/musketsPerSecond`, `Math.round(index*ticksPerMusket)`, máximo `32` spawns por chamada |
| Alvo olhado | `LOOK_TARGET_CHANCE=0.6666666666666666`, `LOOK_TARGET_RANGE=32.0` |
| Fallback | `NEAREST_TARGET_RANGE=12.0` (`dist²<=144` + LoS), senão caixa frontal `RANDOM_TARGET_RANGE=32.0`, meia-largura `8.0`, meia-altura `5.0` |
| Spawn | `MIN_SPAWN_DISTANCE_FROM_CASTER=1.5` (`dist²>=2.25`), raio `sqrt(rand)*4`, frente `1.6..3.6`, até `8` tentativas |
| Dano no disparo | `createCombatDamageSource(DamageTypes.TIRO_VOLLEY)` + `CombatTools.applySpellDamage(...,NO_KNOCKBACK)` |
| NBT do mosquete | `Damage`, `SpellLevel`, `FireDelayTick`, `RecoilTick`, `Fired`, `Target` |

Bytecode: scratch/javap1011_evocation7.txt (`javap -classpath <JAR> -p -s -c`, 94 classes, EXIT=0, SHA-256 `AF225F42FA1A0295D7339542D49620FBA0D0BE6599147EEDF69B75744730DB41`); decompilação de apoio: scratch/evocation7_sources.txt (46 fontes Vineflower 1.12.0, SHA-256 `05090319D9206171C8C4C38ED1A33479F0F1313F9135B5D70146F5559EB80DB1`). Constantes e fórmulas decisivas foram confrontadas com o bytecode; em divergência, o bytecode prevalece.

## 3. Casting / execução

1. `onCast` inicializa `TiroVolleyCastData` com `startGameTick`, `nextSpawnIndex=0` e `initialized=true`, e chama `spawnDueMuskets`.
2. `spawnDueMuskets` calcula `elapsedTick = max(0, gameTime - startGameTick)` e `ticksPerMusket = 20 / musketsPerSecond`.
3. Para até `32` mosquetes por chamada, `scheduledTick = round(nextSpawnIndex * ticksPerMusket)`; se `scheduledTick > elapsedTick`, interrompe; senão `fireDelay = max(1, (int)(20 + scheduledTick - elapsedTick))`.
4. `spawnMusket` escolhe posição segura com `pickSpawnPosition`, resolve alvo inicial via `findInitialTarget`, chama `setup(damage, level, fireDelay, target)` e adiciona a entidade.
5. `findInitialTarget` usa `resolveAssistedAim` em `32.0` com chance `2/3`; senão tenta o alvo mais próximo em `12.0` com LoS e, por fim, um alvo aleatório na caixa frontal `32.0/8.0/5.0`.
6. `tickOnServer` decrementa `fireDelayTick`; ao chegar a zero, `tryFire` valida alvo, `hasClearShot`, aplica dano com `NO_KNOCKBACK`, envia tracer `32.0/16.0`, marca `Fired` e inicia `10` ticks de recuo, ou descarta o mosquete.
7. `resolveCurrentDamage` recalcula dano com o poder atual quando `spellLevel>0`; `onServerCastComplete` limpa o cast data.

## 4. Targeting / geometria

| Propriedade | Valor e consumidor |
|---|---|
| Alvo olhado | `resolveAssistedAim` em `32.0` blocos, chance `2/3` |
| Alvo próximo | Caixa `inflate(12.0)`, `dist²<=144`, `isValidCombatTarget`, LoS, menor distância |
| Alvo aleatório | `z 0..32`, `|x|<=8`, `|y|<=5` no espaço de visão, LoS, `inflate(40.0)` para varredura |
| Spawn | Até `8` tentativas; `dist²>=2.25` do olho; AABB com `inflate(0.05)` e `noCollision` |
| Empurrão de segurança | `t = 0..0.8` em passos `0.1` em direção ao olho; fallback `eye + forward*1.6` |
| Linha de tiro | `level.clip` `COLLIDER`/`Fluid.NONE` do cano ao alvo; aceita `MISS` ou hit além do alvo |
| Persistência | `TiroVolleyCastData` com `StartGameTick`, `NextSpawnIndex`, `Initialized`; mosquetes com NBT completo |

## 5. Resultado

- Cada mosquete aplica um dano direto com `DamageTypes.TIRO_VOLLEY` e `KnockbackTypes.NO_KNOCKBACK`.
- O agendamento é por mosquete, não por cast; `fireDelay` inclui `20` ticks base mais a diferença entre o tick agendado e o decorrido.
- `resolveCurrentDamage` recalcula o dano no disparo a partir do poder atual quando `spellLevel>0`, portanto o valor de `Damage` no `setup` pode ser substituído no disparo.
- Tracer, partículas e som `MUSKET` são feedback; nenhum projétil com hitbox independente (`N/A` com justificativa).

## 6. Scaling e caps

| Parâmetro | Fórmula literal | Unidade / ownership |
|---|---|---|
| Spell power | `100 + 100*(level-1)` declarado; efetivo **NÃO VERIFICADO** |
| Dano | `(4.0 + power/1000) * damageMultiplier(TIRO_VOLLEY)` — config **NÃO VERIFICADA** |
| Cadência | `clamp(2 + (power-100)*0.015, 1, 10)` mosquetes/segundo |
| Intervalo | `20 / musketsPerSecond` ticks por mosquete; `scheduledTick=round(index*interval)` |
| Delay de disparo | `max(1, (int)(20 + scheduledTick - elapsedTick))` ticks |
| Limite de spawn | `32` mosquetes por chamada de `onCast` |
| Mana | `13 + 3*(level-1)` declarado; efetivo **NÃO VERIFICADO** |
| Cooldown | `20.0` s declarado; `castTime=200` com `CastType.CONTINUOUS` |

## 7. Possibilidades de perks

- **A — atributo nativo:** dano e cadência respondem ao poder; `resolveCurrentDamage` usa o poder no momento do disparo.
- **B — evento verificado:** `ICastHighlightSpell` é visual; `IMagiAgentSuitAffectedSpell` apenas altera interrompibilidade.
- **C — adapter condicionado:** mudar cadência, quantidade ou geometria de spawn exigiria substituir `TiroVolley`/`TiroVolleyMusketEntity` com risco de duplicar dano e spawns. **CONDICIONADO**.
- **D — sem hook demonstrado:** nenhuma API segura para transformar a saraivada em AOE persistente ou alterar o agendamento sem duplicar tiros. **NO_MUTATION** / fail-closed.

- `mutating_hook = NOT_VERIFIED`; `mutation = NO_MUTATION` (fail-closed).

## 8. Causalidade

`cast contínuo → agendamento por tick → spawn de mosquetes com alvo → delay → disparo com dano recalculado → recuo/descarte → limpeza do cast data`.


## 9. Concepção de nova magia

Assinatura ocupada: saraivada contínua de mosquetes conjurados com agendamento por tick e alvos múltiplos. Nenhuma implementação foi realizada.

## 10. Verificação e pendências

- ✅ identidade/hash, construtor `100/100/13/3/200`, dano `4+power/1000`, cadência `clamp(2+(power-100)*0.015,1,10)`, `20` ticks base, `32` spawns, chance `2/3`, caixas `32/8/5` e `12`, spawn `1.5`, recuo `10`, `NO_KNOCKBACK`, NBT e agendamento confirmados no bytecode 1.0.1.1.
- ⚠️ multiplicador instalado, mana/cooldown efetivos, `MagiAgentSuit` real e cadência em execução contínua permanecem `NÃO VERIFICADOS`.
- ⚠️ `physical_qa=NOT_TESTED`: sem Survival, PvP, lag, portais ou saraivada real observada.
- ⚠️ Universo integral do provider não encerrado; homologação integral permanece `NOT_CERTIFIED`.


## Localizadores para Codex — resumo operacional

Assinatura ocupada: saraivada contínua de mosquetes conjurados com agendamento por tick e alvos múltiplos. Nenhuma implementação foi realizada.

- Consultar [`EXACT-TECHNICAL-CONTRACTS-1.0.1.1.md`](../EXACT-TECHNICAL-CONTRACTS-1.0.1.1.md).
