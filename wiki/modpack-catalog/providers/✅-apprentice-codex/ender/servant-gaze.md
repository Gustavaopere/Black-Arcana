# Servant Gaze

**Estado do contrato:** ✅ `COMPLETE_PERK_READY` — `STATIC_TECHNICAL_CATALOG_ONLY` · `SHA_EXACT_BINARY_BEHAVIOR` · `mutating_hook=NOT_VERIFIED` · `physical_qa=NOT_TESTED`.

> O ✅ cobre exclusivamente a documentação estática SHA-exata deste objeto. Não homologa hook mutador, execução no pack, configuração efetiva, universo integral do provider nem QA físico.

## 1. Identidade e proveniência

| Campo | Valor verificado |
|---|---|
| Provider | Apprentice's Codex |
| Mod ID | `apprenticecodex` |
| Registry ID | `apprenticecodex:servant_gaze` |
| Host | Iron's Spells 'n Spellbooks (`AbstractSpell`) |
| Escola | `SchoolRegistry.ENDER_RESOURCE` (Ender) |
| Raridade mínima | `SpellRarity.UNCOMMON` |
| Níveis | 1–5 (`DefaultConfig.setMaxLevel(5)`) |
| Tipo de cast | `CastType.LONG` |
| Cooldown declarado | `150.0` s |
| Recurso | Mana do Iron's (`baseManaCost=75`, `manaCostPerLevel=0`); mana adicional por disparo da staff |
| JAR exato | `apprentice_codex-1.0.1.1-mc1.21.1.jar` |
| SHA-256 do JAR | `9C5244E75DBCA95BDAF48A85F0C189F8456149D1220BAD5FF339A86BCE04AC86` |
| SHA-1 do JAR | `A3F9C73EBD77D15B7E77AE14F4D0F695FEC3B7CF` |
| Ambiente | Minecraft 1.21.1 · NeoForge · Java 21 (JDK 21.0.12 na inspeção) |
| Classe de implementação | `jp.aquafactory.apprenticecodex.spell.servantgaze.ServantGaze` |
| Evidência compartilhada | [`EXACT-TECHNICAL-CONTRACTS-1.0.1.1.md`](../EXACT-TECHNICAL-CONTRACTS-1.0.1.1.md) |

As versões 0.9.7.1 e 1.0.1 permanecem como histórico; nenhum valor foi reaproveitado sem confirmação no artefato físico 1.0.1.1.

## 2. Localizadores para o Codex

| Elemento | Localizador |
|---|---|
| Registro | `SpellRegistry.reg("servant_gaze", ServantGaze::new)` |
| Config | `ServantGaze.config` (`UNCOMMON`, nível 5, cooldown `150.0`) |
| Coeficientes | `ServantGaze.<init>()`: `baseSpellPower=500`, `spellPowerPerLevel=200`, `baseManaCost=75`, `manaCostPerLevel=0`, `castTime=50` |
| Dano | `ServantGaze.getDamage(int,LivingEntity)` → `spellPower/100 * ApprenticeCodexServerConfig.damageMultiplier(DamageMultiplierKey.SERVANT_GAZE)` |
| Raio | `ServantGaze.getRadius()` → `20.0` |
| Custo por disparo | `ServantGaze.getConsumeManaPerAttack(int)` → `15 + 5*(level-1)` |
| Duração / recast | `ServantGaze.getDuration()` → `12000`; `getRecastCount(...)` → `2` |
| Dados de cast | `ServantGaze.ServantGazeCastData` (`spellLevel`, `damage`, `radius`, `attackManaCost`) |
| Manager | `ServantGazeManager.initialize`, `configure`, `validate`, `finishRecast`, `getActiveRecast` |
| Staff | `ServantGazeStaffEntity` (`ATTACK_INTERVAL=40`, `SHOT_DELAYS={0,3,6}`, `FIRE_POSITION_OFFSET=(0,1.7,0)`, `selectTargets`, `firePendingShot`) |
| Projétil | `ServantGazeProjectileEntity` |
| Câmera/efeitos | `SoundRegistry.CLOUD_OF_REGEN_LOOP` (início), `SoundRegistry.VANILLA_SUMMON_MAGICAL_ENTITY` (fim) |
| Talismã | `ItemRegistry.GREATER_CONJURERS_TALISMAN` suprime `super.onRecastFinished` em `TIMEOUT` |

Bytecode: `scratch/javap1011_ender10.txt` (`javap -classpath <JAR> -p -s -c`, `EXIT=0`, SHA-256 `0095E23B21918E38B4BD7D6C47DA8C3503753F0F988C00AB04A786060E2C50E5`); decompilação: `scratch/ender10_sources.txt` (SHA-256 `F3953EB8FCFB793EC501694E054E3C3CBE187E557B09B6CF158828692A97A645`).

## 3. Casting / execução

1. `AbstractSpell` resolve mana/cooldown/nível; `castTime=50`, `CastType.LONG`.
2. `onCast`: sem recast ativo para a spell, em `ServerLevel` com `ServerPlayer`, cria `ServantGazeStaffEntity`; se `addFreshEntity` sucede, monta `ServantGazeCastData(spellLevel, damage, radius, manaPerAttack)` e `ServantGazeManager.initialize(player, staff, 12000, castData)`.
3. `initialize` define `setLifecycleOwner(owner)`, `setExpirationGameTime(gameTime + duration)`, `configure(...)` e `castData.bindStaff(staff)`.
4. A staff segue o owner (`getStandbyPosition` usa `RotationTools.calculateBehindPosition(owner, -0.75, 0.9, -0.2)`) e, em `tickOnServer`, valida o ciclo de vida.
5. `onRecastFinished` → `ServantGazeManager.finishRecast`; em `RecastResult.TIMEOUT` com `GREATER_CONJURERS_TALISMAN` equipado, não chama o caminho padrão de conclusão de summon.

Valores efetivos de mana/cooldown, multiplicador de dano e configuração **NÃO VERIFICADOS**.

## 4. Combate / geometria

| Propriedade | Valor e consumidor |
|---|---|
| Dano | `spellPower/100 * damageMultiplier(SERVANT_GAZE)`; nominal **5 / 7 / 9 / 11 / 13** sem multiplicador instalado |
| Raio de seleção | `20.0` blocos; candidatos dentro de `getBoundingBox().inflate(radius)` e `distanceToSqr <= radius²` |
| Prioridade de alvo | ordena por `getHealth()` **decrescente**, desempata por `Entity.getId()`; exige `CombatTools.canBeHostileToMe` e `hasLineOfSight` (`ClipContext` com `Block.COLLIDER`, `Fluid.NONE`) |
| Mana por disparo | `15 + 5*(level-1)` = **15 / 20 / 25 / 30 / 35**; debitada de `MagicData` do owner **por alvo selecionado**, antes do disparo |
| Número máximo de alvos por rodada | `SHOT_DELAYS.length = 3` |
| Intervalo de seleção | `ATTACK_INTERVAL=40` ticks (`tickCount % 40 == 0`), com `attackSetTick < 0` |
| Atrasos de disparo | `SHOT_DELAYS={0,3,6}` ticks, um projétil por alvo pendente |
| Origem do tiro | `position + (0, 1.7, 0)` |
| Duração da sessão | `12000` ticks = 10 min |
| Recast | `2` |

O débito de mana acontece em `selectTargets`, não no `firePendingShot`. Se o alvo desaparecer antes do disparo, o custo já foi debitado — risco a validar em QA, não bug comprovado.

## 5. Resultado e persistência

- `ServantGazeManager.validate` rejeita staff sem `expirationGameTime`, expirada ou com owner ausente/morto/em outra dimensão/recast divergente.
- A staff é `PersistentSummonWeaponEntity` com `shouldBeSaved=false` e `isAlwaysTicking=true`; `onAntiMagic`/`remove` tratam cancelamento e descarte. **Não presumir persistência após restart**.
- `ServantGazeEvents` e o manager tratam limpeza e conclusão de sessão; remoção do casador pode remover a staff pelo ciclo de vida do provider.
- `ServantGazeProjectileEntity` pertence à mesma raiz semântica; tiros não são casts novos.

## 6. Scaling e caps

| Parâmetro | Fórmula literal | Unidade / ownership |
|---|---|---|
| Spell power | `500 + 200*(level-1)` | float; host aplica atributos |
| Dano exibido | `power/100 * damageMultiplier(SERVANT_GAZE)` | float; multiplicador de servidor **NÃO VERIFICADO** |
| Mana base | `75 + 0*(level-1)` | Iron's mana |
| Mana por disparo | `15 + 5*(level-1)` | por alvo selecionado |
| Raio | `20.0` | blocos |
| Duração | `12000` | ticks |
| Recast | `2` | Iron's recast |
| Cooldown | `150.0` s | `DefaultConfig` |
| Cadência | `40` ticks + atrasos `0/3/6` | provider |

## 7. Possibilidades de perks

- **A — atributo nativo:** spell power e mana base via `AbstractSpell`; multiplicador de dano e custo por disparo são server config/contrato do provider.
- **B — evento verificado:** `tickOnServer`, `selectTargets` e `ServantGazeManager` são execução do provider; não há hook de mutação segura demonstrado para alterar cadência, alvos ou custo por disparo.
- **C — adapter condicionado:** mudar o comportamento da torre exigiria substituir staff/manager/projétil com contrato de owner, mana, limpeza e recast. **CONDICIONADO**.
- **D — sem hook demonstrado:** não há API comprovada para converter a staff em familiar Black Arcana ou premiar Mastery por tick/scan sem risco de duplo processamento. **NO_MUTATION / fail-closed**.
- `mutating_hook = NOT_VERIFIED`.

## 8. Causalidade

`um cast → uma staff owner-bound → seleção periódica de alvos → projéteis com mana do casador → expiração/recast/cleanup`.

A staff autônoma não é familiar Black Arcana por padrão. RPG/Black Arcana não devem conceder Mastery por tick de torre, scan ou disparo; crédito causal de hit/kill exigiria contrato explícito de atribuição de progressão.

## 9. Concepção de nova magia

Assinatura ocupada: "torre autônoma de longa duração vinculada ao owner que gasta mana do casador por disparo". Nenhuma implementação foi realizada.

## 10. Verificação e pendências

- ✅ Identidade/hash, coeficientes, dano, raio, prioridade de alvo, custo por disparo, cadência, atrasos, duração, recast e limpeza confirmados no bytecode 1.0.1.1.
- ⚠️ Multiplicador de dano efetivo, prioridade percebida em multiplayer, logout/teleport e custo agregado de múltiplas staffs não certificados.
- ⚠️ `physical_qa=NOT_TESTED`: sem servidor real, PvP, talismã equipado, death/dispel ou restart.
- ⚠️ Universo integral do provider não encerrado.

## Localizadores para Codex — resumo operacional

- `selectTargets` debita mana antes de `firePendingShot`; não inferir custo apenas do número de projéteis emitidos.
- `shouldBeSaved=false`: staff não é persistente across restart.
- Nenhum ponto de mutação segura demonstrado; manter fail-closed.
- Consultar [`EXACT-TECHNICAL-CONTRACTS-1.0.1.1.md`](../EXACT-TECHNICAL-CONTRACTS-1.0.1.1.md).
