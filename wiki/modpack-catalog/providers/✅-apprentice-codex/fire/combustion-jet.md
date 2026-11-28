# Combustion Jet

**Estado do contrato:** ✅ `COMPLETE_PERK_READY` — `STATIC_TECHNICAL_CATALOG_ONLY` · `SHA_EXACT_BINARY_BEHAVIOR` · `mutating_hook=NOT_VERIFIED` · `mutation=NO_MUTATION` · `physical_qa=NOT_TESTED` · `perk_certification=NOT_CERTIFIED`.

> O ✅ cobre exclusivamente a documentação estática SHA-exata deste objeto. Não homologa hook mutador, execução no pack, configuração efetiva, universo integral do provider nem QA físico.

## 1. Identidade e proveniência

| Campo | Valor verificado |
|---|---|
| Provider | Apprentice's Codex |
| Mod ID | `apprenticecodex` |
| Registry ID | `apprenticecodex:combustion_jet` |
| Host | Iron's Spells 'n Spellbooks (`AbstractSpell`) |
| Interfaces | `CombustionJetWaveEntity` é `Projectile`/`AntiMagicSusceptible`/`CombatOwnerUuidHolder` da mesma raiz; renderer é apresentação |
| Escola | `SchoolRegistry.FIRE_RESOURCE` (Fire) |
| Raridade mínima declarada | `UNCOMMON` |
| Níveis declarados | 1–5 (`setMaxLevel(5)`) |
| Tipo de cast | `INSTANT` |
| Cooldown declarado | `8.0 s` |
| Recurso | Mana do Iron's (`baseManaCost=30`, `manaCostPerLevel=10`) |
| JAR exato | `apprentice_codex-1.0.1.1-mc1.21.1.jar` |
| SHA-256 do JAR | `9C5244E75DBCA95BDAF48A85F0C189F8456149D1220BAD5FF339A86BCE04AC86` |
| SHA-1 do JAR | `A3F9C73EBD77D15B7E77AE14F4D0F695FEC3B7CF` |
| Ambiente | Minecraft 1.21.1 · NeoForge · Java 21 (JDK 21.0.12 na inspeção) |
| Classe de implementação | `jp.aquafactory.apprenticecodex.spell.combustionjet.CombustionJet` |
| Auxiliares da mesma raiz | `CombustionJetWaveEntity`, `CombustionJetWaveRenderer`, `DamageTypes.COMBUSTION_JET` |
| Evidência compartilhada | [`EXACT-TECHNICAL-CONTRACTS-1.0.1.1.md`](../EXACT-TECHNICAL-CONTRACTS-1.0.1.1.md) |

As versões 0.9.7.1 e 1.0.1 permanecem como histórico; nenhum valor foi reaproveitado sem confirmação no artefato físico 1.0.1.1. Os coeficientes declarados não são os valores efetivos instalados: mana, cooldown, spell power, nível, raridade e multiplicadores do host permanecem `NÃO VERIFICADOS` (`AbstractSpell` lê `SpellConfigManager`, atributos, Curios e eventos).

## 2. Localizadores para o Codex

| Elemento | Localizador |
|---|---|
| Registro | `SpellRegistry.reg("combustion_jet", CombustionJet::new)` |
| Config | `UNCOMMON`, nível 5, cooldown `8.0`, `FIRE_RESOURCE`, `CastType.INSTANT` |
| Coeficientes | <init>: `baseSpellPower=400`, `spellPowerPerLevel=200`, `baseManaCost=30`, `manaCostPerLevel=10`, `castTime=0` |
| Dano | `getDamage` → `(1 + power/100) * damageMultiplier(COMBUSTION_JET)` |
| Queima | `getBurnDuration` → `max((spellLevel-1)*40, 10)` ticks |
| Alcance/velocidade | `getRange()=10.0F`; `SPEED=2.25`, `shoot` normaliza a direção |
| Volume orientado | `WaveVolume.halfExtents=(0.75 + movement.length()*0.5, 4.5, 0.5)`, centro `start + movement*0.5` |
| Constantes declaradas | `WAVE_WIDTH=9.0F`, `WAVE_HEIGHT=1.0F`, `WAVE_DEPTH=1.5F`, `KNOCKBACK_STRENGTH=1.0F`, `BLOCK_COLLISION_SIZE=0.5F` |
| Colisão/amostragem | `BLOCK_COLLISION_STEP=0.25`, `COLLISION_EPSILON=1.0E-7`, `makeBlockCollisionBox` com half size `0.25` |
| Dedupe | `victimUuids` persistido em NBT como `Victims`, mais `checkedTargetUuids` por tick |

Bytecode: scratch/fire5_evidence/javap1011_fire6.txt (`javap -classpath <JAR> -p -s -c`, 28 classes, 1.095.867 bytes, EXIT=0, SHA-256 `F5491A50DCF3A8F7EBF1E9C035EFE0723490C97475DE501FC3AF6C1580E17EDB`, SHA-1 `53C2C327705603172618C84CFFEFC41412683190`); decompilação de apoio: scratch/fire5_sources.txt (fontes Vineflower 1.12.0 das cinco raízes legadas e auxiliares, 188.994 bytes, SHA-256 `F8BE6DF48A22522FC1B23FBA362D8FD0F2637A2759D65739F25A723A2903A448`). Constantes e fórmulas decisivas foram confrontadas com o bytecode; em divergência, o bytecode prevalece.

## 3. Casting / execução

1. `onCast` cria a onda na posição do olho, chama `moveToCollisionLimitedSpawnPosition(direction)`, aplica dano/queima/alcance e dispara `shoot`.
2. `tick` trunca o movimento ao alcance restante; sem movimento, descarta. No servidor, varre colisão de bloco, afeta entidades e descarta se houver impacto.
3. `affectEntities` constrói `WaveBasis` e `WaveVolume`, consulta `level.getEntities` no AABB projetado e filtra por validade, dedupe global, dedupe do tick, interseção orientada e `hasClearPathToTarget`.
4. `affectEntity` cria dano `DamageTypes.COMBUSTION_JET` preservando o combat owner, aplica queima quando menor, chama `CombatTools.applySpellDamage` com `NO_KNOCKBACK` e então aplica `knockback(1.0, -forward.x, -forward.z)` horizontal.
5. `hasClearPathToTarget` projeta o ponto mais próximo da caixa da vítima no segmento de movimento e exige `clip` do tipo `MISS`.
6. `scanBlockCollision` avança em passos de no máximo `0.25` bloco; ao detectar colisão, usa o `BlockHitResult` ou fabrica um com a direção oposta ao movimento.
7. A onda é descartada ao atingir `10.0` blocos de distância acumulada ou por `onAntiMagic`; NBT guarda dano, queima, distância e vítimas.

## 4. Targeting / geometria

| Propriedade | Valor e consumidor |
|---|---|
| Alvo | Entidades no volume orientado da onda em cada movimento de tick |
| Filtro | `isValidCombatTarget` contra owner, exclusão do owner, UUID global e do tick, e linha livre até a caixa |
| Geometria | `WaveVolume` orientado: avante `0.75 + passo*0.5`, lateral `4.5`, vertical `0.5`; AABB mundial é projeção conservadora |
| Constantes de apresentação | `9.0/1.0/1.5` aparecem como largura/altura/profundidade; o volume de dano usa os half extents acima |
| Knockback | `NO_KNOCKBACK` no `applySpellDamage` e recuo horizontal manual de força `1.0` |
| Colisão | Varredura em passos `0.25` com caixa de half size `0.25` |
| Persistência | NBT com `Damage`, `BurnDuration`, `MaxTravelDistance`, `TraveledDistance`, `Victims` e combat owner |

## 5. Resultado

- Dano contínuo por varredura, mas cada UUID é atingido no máximo uma vez pela onda (`victimUuids`).
- Aplica queima vanilla e recuo manual; `DamageTypes.COMBUSTION_JET` é o tipo de dano.
- A onda não cria invocação persistente nem AOE estacionário.
- Sem cura ou efeitos de status além da queima (`N/A` com justificativa: `applyEffect` não é chamado neste fluxo).

## 6. Scaling e caps

| Parâmetro | Fórmula literal | Unidade / ownership |
|---|---|---|
| Spell power | `400 + 200*(level-1)` declarado; efetivo **NÃO VERIFICADO** |
| Dano | `(1 + power/100) * damageMultiplier(COMBUSTION_JET)` — config **NÃO VERIFICADA** |
| Queima | `max((level-1)*40, 10)` ticks |
| Mana | `30 + 10*(level-1)` declarado; efetivo **NÃO VERIFICADO** |
| Cooldown | `8.0` s declarado; efetivo **NÃO VERIFICADO** |
| Cast time | `0` ticks, coerente com `CastType.INSTANT` |
| Velocidade/alcance | `2.25` blocos/tick e `10.0` blocos de distância acumulada |
| Recuo | `1.0` de força manual na direção horizontal oposta ao avanço |

## 7. Possibilidades de perks

- **A — atributo nativo:** dano responde a `getSpellPower`; queima depende somente do nível.
- **B — evento verificado:** `EventHooks.onProjectileImpact` pode cancelar o impacto de bloco, mas não expõe mutador de parâmetros.
- **C — adapter condicionado:** alterar `WaveVolume`, dedupe, knockback ou colisão exigiria substituir a entidade da onda com risco de duplicar dano. **CONDICIONADO**.
- **D — sem hook demonstrado:** nenhuma API segura para transformar a onda em área persistente ou alterar geometria sem duplicar cast. **NO_MUTATION** / fail-closed.

- `mutating_hook = NOT_VERIFIED`; `mutation = NO_MUTATION` (fail-closed).

## 8. Causalidade

`cast instantâneo → onda 2.25 blocos/tick → volume orientado por tick → dano COMBUSTION_JET com dedupe, queima e recuo → descarte em 10 blocos, colisão ou anti-magia`.

## 9. Concepção de nova magia

Assinatura ocupada: jato/onda orientada em movimento com dano único por vítima, queima e recuo. Nenhuma implementação foi realizada.

## 10. Verificação e pendências

- ✅ identidade/hash, construtor `400/200/30/10/0`, `UNCOMMON/5/8.0`, dano `(1+power/100)*multiplier`, burn `max((level-1)*40,10)`, `SPEED=2.25`, alcance `10`, `halfExtents=(0.75+movement*0.5,4.5,0.5)`, passo `0.25`, dedupe UUID e NBT confirmados no bytecode 1.0.1.1.
- ✅ `NO_KNOCKBACK` no dano e `knockback(1.0,...)` manual confirmados como etapas distintas.
- ⚠️ `WAVE_WIDTH/HEIGHT/DEPTH` e `BLOCK_COLLISION_SIZE` são constantes declaradas; a geometria efetiva de dano é o `WaveVolume` orientado.
- ⚠️ multiplicador, mana/cooldown efetivos e DPS real em execução permanecem `NÃO VERIFICADOS`.
- ⚠️ `physical_qa=NOT_TESTED`: sem Survival, PvP, colisão real ou teste de anti-magia.
- ⚠️ Universo integral do provider não encerrado; homologação integral permanece `NOT_CERTIFIED`.


## Localizadores para Codex — resumo operacional

Assinatura ocupada: jato/onda orientada em movimento com dano único por vítima, queima e recuo. Nenhuma implementação foi realizada.

- Consultar [`EXACT-TECHNICAL-CONTRACTS-1.0.1.1.md`](../EXACT-TECHNICAL-CONTRACTS-1.0.1.1.md).
