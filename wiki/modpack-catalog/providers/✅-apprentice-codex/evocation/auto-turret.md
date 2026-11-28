# Auto Turret

**Estado do contrato:** ✅ `COMPLETE_PERK_READY` — `STATIC_TECHNICAL_CATALOG_ONLY` · `SHA_EXACT_BINARY_BEHAVIOR` · `mutating_hook=NOT_VERIFIED` · `mutation=NO_MUTATION` · `physical_qa=NOT_TESTED` · `perk_certification=NOT_CERTIFIED`.

> O ✅ cobre exclusivamente a documentação estática SHA-exata deste objeto. Não homologa hook mutador, execução no pack, configuração efetiva, universo integral do provider nem QA físico.

## 1. Identidade e proveniência

| Campo | Valor verificado |
|---|---|
| Provider | Apprentice's Codex |
| Mod ID | `apprenticecodex` |
| Registry ID | `apprenticecodex:auto_turret` |
| Host | Iron's Spells 'n Spellbooks (`AbstractSpell`) |
| Interfaces | `IClientBlockTargetingSpell`, `IClientBlockTargetCaptureSpell`, `IClientPlacementPreviewSpell` |
| Escola | `SchoolRegistry.EVOCATION_RESOURCE` (Evocation) |
| Raridade mínima declarada | `RARE` |
| Níveis declarados | 1–3 (`setMaxLevel(3)`) |
| Tipo de cast | `LONG` |
| Cooldown declarado | `12.0 s` |
| Recurso | Mana do Iron's (`baseManaCost=80`, `manaCostPerLevel=20`) |
| JAR exato | `apprentice_codex-1.0.1.1-mc1.21.1.jar` |
| SHA-256 do JAR | `9C5244E75DBCA95BDAF48A85F0C189F8456149D1220BAD5FF339A86BCE04AC86` |
| SHA-1 do JAR | `A3F9C73EBD77D15B7E77AE14F4D0F695FEC3B7CF` |
| Ambiente | Minecraft 1.21.1 · NeoForge · Java 21 (JDK 21.0.12 na inspeção) |
| Classe de implementação | `jp.aquafactory.apprenticecodex.spell.autoturret.AutoTurret` |
| Auxiliares da mesma raiz | `AutoTurretEntity`, `AutoTurretPlacementHelper`, `AutoTurretRenderer`, `AutoTurretCastData` |
| Evidência compartilhada | [`EXACT-TECHNICAL-CONTRACTS-1.0.1.1.md`](../EXACT-TECHNICAL-CONTRACTS-1.0.1.1.md) |

As versões 0.9.7.1 e 1.0.1 permanecem como histórico; nenhum valor foi reaproveitado sem confirmação no artefato físico 1.0.1.1. Os coeficientes declarados não são os valores efetivos instalados: mana, cooldown, spell power, nível, raridade e multiplicadores do host permanecem `NÃO VERIFICADOS` (`AbstractSpell` lê `SpellConfigManager`, atributos, Curios e eventos).

## 2. Localizadores para o Codex

| Elemento | Localizador |
|---|---|
| Registro | `SpellRegistry.reg("auto_turret", AutoTurret::new)` |
| Config | `RARE`, nível 3, cooldown `12.0`, `EVOCATION_RESOURCE` |
| Coeficientes | <init>: `baseSpellPower=100`, `spellPowerPerLevel=40`, `baseManaCost=80`, `manaCostPerLevel=20`, `castTime=40` |
| Dano | `getDamage` → `4*power/100 * damageMultiplier(AUTO_TURRET)` |
| Munição/HP/restock | `8 + round(8*power/100)`, `20+(level-1)*10`, `getManaCost(level)/4` |
| Placement | `AutoTurretPlacementHelper`: captura/preview/servidor em `8` blocos; `hasNearbyTurret` usa `placementBox().inflate(0.1)` |
| Entidade | `PathfinderMob`/`GeoEntity`/`MonarchBondHealingTarget`; `WIDTH=0.9`, `HEIGHT=1.6`, AABB `0.9×1.6×0.9`, `FOLLOW_RANGE=24`, `DISCARD_DELAY_TICK=100` |
| Cadência | `CHARGE_TICK=15`, `COOLDOWN_TICK=8`, lock `10/60/20/40` |
| Persistência/restock | `shouldBeSaved=false`; apenas o owner repõe munição e recebe `SyncManaPacket` |

Bytecode: scratch/javap1011_evocation10.txt (`javap -classpath <JAR> -p -s -c`, 61 classes, EXIT=0, SHA-256 `B872A0B86732D7EAE026532ED358AD9BBDFB7B1D7BCFCA2C6B35F13EADD9A2D5`); decompilação de apoio: scratch/evocation10_sources.txt (44 fontes Vineflower 1.12.0, SHA-256 `BCAF5695AA5346DABC0D976D8EBFA327B7622570230DE48B4330396876448387`). Constantes e fórmulas decisivas foram confrontadas com o bytecode; em divergência, o bytecode prevalece.

## 3. Casting / execução

1. `captureClientBlockTarget` e `getClientPlacementPreview` usam alcance `8.0`; o preview é uma coluna única centrada no bloco resolvido.
2. `checkPreCastConditions` resolve a posição no servidor (`AutoTurretPlacementHelper.resolveServer`) e recusa se `hasNearbyTurret` encontrar outra torre na caixa inflada em `0.1`.
3. `onCast` restaura a posição do `AutoTurretCastData` ou resolve novamente, cria `AutoTurretEntity`, aplica `setAnchorPos`, `setDamage`, `setRestockData(projectileCount, manaCost/4)` e `setTurretMaxHealth`.
4. A torre usa `FOLLOW_RANGE=24` para alvos válidos/hostis; carrega por `15` ticks e dispara com `8` ticks de cooldown. A cada disparo, `restBulletCount` é decrementado; ao chegar a zero, `discardDelayTick=100` inicia a contagem de descarte.
5. `mobInteract` permite somente ao owner: `tryRestock` debita `getManaCost(level)/4`, envia `SyncManaPacket` e zera o atraso de descarte; não-owner retorna `NOT_OWNER`.
6. `shouldBeSaved=false` e `removeWhenFarAway=false` definem comportamento de persistência distinto; não inferir sobrevivência a restart.

## 4. Targeting / geometria

| Propriedade | Valor e consumidor |
|---|---|
| Alcance de placement | `8.0` blocos, cliente e servidor |
| Caixa de placement | `0.9 × 1.6 × 0.9` centrada no bloco, suporte exigido abaixo |
| Colisão entre torres | `placementBox().inflate(0.1)` |
| Alcance de alvo | `Attributes.FOLLOW_RANGE=24.0` (fallback `24.0`) |
| Carga/cadência | `15` ticks de carga, `8` de cooldown |
| Perda de alvo | `20` ticks sem linha de visão limpam `autoTarget` (`KEEP_LOCK_ON_TICK_IN_LOST_LOR`); isso **não** inicia o descarte |
| Fim da munição | `restBulletCount<=0` após um disparo ativa `discardDelayTick=100`; `tryRestock` volta para `-1` |
| Dano de interface | `DamageTypes.AUTO_TURRET` + `applySpellDamage(...,KNOCKBACK.DEFAULT)` |

## 5. Resultado

- A torre dispara dano direto; a munição é contada localmente e sincronizada via dados da entidade.
- `MonarchBondHealingTarget` conecta a torre ao charm de cura do Iron's; não é uma invocação independente.
- A reposição é transação mana↔munição do owner, com action bar e partículas; sem owner, a torre descarta.

## 6. Scaling e caps

| Parâmetro | Fórmula literal | Unidade / ownership |
|---|---|---|
| Spell power | `100 + 40*(level-1)` | float declarado |
| Dano | `4*power/100 * damageMultiplier(AUTO_TURRET)` | config **NÃO VERIFICADA** |
| Munição | `8 + round(8*power/100)` | projéteis |
| HP | `20 + 10*(level-1)` | pontos de vida |
| Restock | `getManaCost(level)/4` | mana |
| Mana/cooldown/cast | `80+20*(level-1)` / `12.0` s / `40` ticks | host + config **NÃO VERIFICADA** |

## 7. Possibilidades de perks

- **A — atributo nativo:** dano, munição e HP respondem ao poder; restock acompanha `getManaCost`.
- **B — evento verificado:** `mobInteract`/`tryRestock` são pontos de decisão do provider, sem API pública de modificação de parâmetros.
- **C — adapter condicionado:** alterar geometria de placement ou cadência exigiria substituir `AutoTurret`, `AutoTurretPlacementHelper` e a entidade. **CONDICIONADO**.
- **D — sem hook demonstrado:** não há hook seguro para converter a torre em AOE permanente, ignorar o limite de uma torre por caixa ou remover custo de restock. **NO_MUTATION** / fail-closed.

- `mutating_hook = NOT_VERIFIED`; `mutation = NO_MUTATION` (fail-closed).

## 8. Causalidade

`um cast → validação de placement → uma torre com munição/HP → disparos periódicos → restock pelo owner ou descarte`.


## 9. Concepção de nova magia

Assinatura ocupada: "torre de placement com munição e restock por mana". Nenhuma implementação foi realizada.

## 10. Verificação e pendências

- ✅ identidade/hash, placement 8, inflate 0.1, munição/HP/restock, constantes da entidade, FOLLOW_RANGE 24, cadência 15/8 e restock somente owner confirmados no bytecode 1.0.1.1.
- ⚠️ multiplicador instalado, mana efetiva, preview em lag e persistência real não certificados.
- ⚠️ `physical_qa=NOT_TESTED`: sem servidor Survival, PvP, portais, montarias, recast em combate real ou teleportes.
- ⚠️ Universo integral do provider não encerrado; homologação integral permanece `NOT_CERTIFIED`.


## Localizadores para Codex — resumo operacional

- `8` é o alcance de placement; `24` é o alcance de alvo da entidade.
- A torre não é salva (`shouldBeSaved=false`); restock é mana do owner com `SyncManaPacket`.
- `inflate(0.1)` impede duas torres na mesma caixa.
- Nenhum ponto de mutação segura demonstrado; manter fail-closed.

- Consultar [`EXACT-TECHNICAL-CONTRACTS-1.0.1.1.md`](../EXACT-TECHNICAL-CONTRACTS-1.0.1.1.md).
