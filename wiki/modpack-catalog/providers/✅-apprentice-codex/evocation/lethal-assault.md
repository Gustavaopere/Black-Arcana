# Lethal Assault

**Estado do contrato:** ✅ `COMPLETE_PERK_READY` — `STATIC_TECHNICAL_CATALOG_ONLY` · `SHA_EXACT_BINARY_BEHAVIOR` · `mutating_hook=NOT_VERIFIED` · `mutation=NO_MUTATION` · `physical_qa=NOT_TESTED` · `perk_certification=NOT_CERTIFIED`.

> O ✅ cobre exclusivamente a documentação estática SHA-exata deste objeto. Não homologa hook mutador, execução no pack, configuração efetiva, universo integral do provider nem QA físico.

## 1. Identidade e proveniência

| Campo | Valor verificado |
|---|---|
| Provider | Apprentice's Codex |
| Mod ID | `apprenticecodex` |
| Registry ID | `apprenticecodex:lethal_assault` |
| Host | Iron's Spells 'n Spellbooks (`AbstractSummonWeaponSpell<LethalAssaultRifleEntity>`) |
| Interfaces | `IMagiAgentSuitAffectedSpell` |
| Escola | `SchoolRegistry.EVOCATION_RESOURCE` (Evocation) |
| Raridade mínima declarada | `UNCOMMON` |
| Níveis declarados | 1–5 (`setMaxLevel(5)`) |
| Tipo de cast | `INSTANT` |
| Cooldown declarado | `1.5 s` |
| Recurso | Mana do Iron's (`baseManaCost=20`, `manaCostPerLevel=5`) |
| JAR exato | `apprentice_codex-1.0.1.1-mc1.21.1.jar` |
| SHA-256 do JAR | `9C5244E75DBCA95BDAF48A85F0C189F8456149D1220BAD5FF339A86BCE04AC86` |
| SHA-1 do JAR | `A3F9C73EBD77D15B7E77AE14F4D0F695FEC3B7CF` |
| Ambiente | Minecraft 1.21.1 · NeoForge · Java 21 (JDK 21.0.12 na inspeção) |
| Classe de implementação | `jp.aquafactory.apprenticecodex.spell.lethalassault.LethalAssault` |
| Auxiliares da mesma raiz | `LethalAssaultRifleEntity`, `LethalAssaultRifleRenderer`, `GunSpellTracerPacket` |
| Evidência compartilhada | [`EXACT-TECHNICAL-CONTRACTS-1.0.1.1.md`](../EXACT-TECHNICAL-CONTRACTS-1.0.1.1.md) |

As versões 0.9.7.1 e 1.0.1 permanecem como histórico; nenhum valor foi reaproveitado sem confirmação no artefato físico 1.0.1.1. Os coeficientes declarados não são os valores efetivos instalados: mana, cooldown, spell power, nível, raridade e multiplicadores do host permanecem `NÃO VERIFICADOS` (`AbstractSpell` lê `SpellConfigManager`, atributos, Curios e eventos).

## 2. Localizadores para o Codex

| Elemento | Localizador |
|---|---|
| Registro | `SpellRegistry.reg("lethal_assault", LethalAssault::new)` |
| Config | `UNCOMMON`, nível 5, cooldown `1.5`, `EVOCATION_RESOURCE` |
| Coeficientes | <init>: `baseSpellPower=500`, `spellPowerPerLevel=200`, `baseManaCost=20`, `manaCostPerLevel=5`, `castTime=0` |
| Dano/alcance | `getDamage` → `power/300 * damageMultiplier(LETHAL_ASSAULT)`; `getRange()=48`; `getBurstCount()=3` |
| Rifle | `MAX_RECOIL_TICK=2`, disparos nos ticks `5/8/11`, descarte no tick `20` |
| Raycast | `RaycastTools.raycastFromEye(owner,48,0.5,isValidCombatTarget)`; mira com largura `1.0` |
| Tracer | `GunSpellTracerPacket(firePosition,target,24.0F,8.0F)` |
| Suit | `canBeInterrupted` delega a `canBeInterruptedWithMagiAgentSuit` |

Bytecode: scratch/javap1011_evocation10.txt (`javap -classpath <JAR> -p -s -c`, 61 classes, EXIT=0, SHA-256 `B872A0B86732D7EAE026532ED358AD9BBDFB7B1D7BCFCA2C6B35F13EADD9A2D5`); decompilação de apoio: scratch/evocation10_sources.txt (44 fontes Vineflower 1.12.0, SHA-256 `BCAF5695AA5346DABC0D976D8EBFA327B7622570230DE48B4330396876448387`). Constantes e fórmulas decisivas foram confrontadas com o bytecode; em divergência, o bytecode prevalece.

## 3. Casting / execução

1. `onCastNoWeapon` cria `LethalAssaultRifleEntity`; `onInitialCastWithWeapon` chama `weapon.startFiring(getDamage(...))`, zerando `firingTick` e `released`.
2. `tickOnServer` segura a posição de standby `(-0.8,1.1,0.1)`, mira com raycast de largura `1.0` e incrementa `firingTick`.
3. `shouldFire` dispara nos ticks `5`, `8` e `11`; no tick `20` a entidade é descartada e no tick `11` ela é liberada (`released=true`).
4. `fire` faz raycast de `48` blocos com largura `0.5`, aplica `DamageTypes.LETHAL_ASSAULT` via `applySpellDamage(...,NO_KNOCKBACK)` ao alvo válido e envia partículas de muzzle/tracer.
5. `recoilTick=2` é sincronizado; o renderer interpola recuo com deslocamento `0.25` e ângulo `8.0°`.
6. `onCastCompleteWithWeapon` retorna `KEEP_WEAPON` somente sem cancelamento; `onAntiMagic` descarta o rifle; `IMagiAgentSuitAffectedSpell` altera apenas a interrompibilidade.

## 4. Targeting / geometria

| Propriedade | Valor e consumidor |
|---|---|
| Alcance | `48` blocos para disparo e mira |
| Raycast de disparo | largura `0.5`, validação `isValidCombatTarget` |
| Raycast de mira | largura `1.0` |
| Burst | `3` disparos nos ticks `5/8/11` |
| Recuo | `2` ticks, `0.25` bloco e `8.0°` no renderer |
| Tracer | velocidade `24.0`, comprimento `8.0` |

## 5. Resultado

- Cada disparo é um hit-scan; não há projétil persistente catalogado nesta raiz.
- O dano é o mesmo valor calculado no cast para os três disparos.
- `KEEP_WEAPON`/`RELEASE_WEAPON` controlam a retenção da arma dentro da mesma raiz.

## 6. Scaling e caps

| Parâmetro | Fórmula literal | Unidade / ownership |
|---|---|---|
| Spell power | `500 + 200*(level-1)` | float declarado |
| Dano por disparo | `power/300 * damageMultiplier(LETHAL_ASSAULT)` | config **NÃO VERIFICADA** |
| Burst | `3` disparos | constante |
| Mana/cooldown/cast | `20+5*(level-1)` / `1.5` s / `0` ticks (`INSTANT`) | host + config **NÃO VERIFICADA** |

## 7. Possibilidades de perks

- **A — atributo nativo:** dano responde ao poder; mana/cooldown ao `AbstractSpell`.
- **B — evento verificado:** `IMagiAgentSuitAffectedSpell` altera interrompibilidade, não parâmetros de disparo.
- **C — adapter condicionado:** mudar burst, cadência ou alcance exigiria substituir raiz e entidade, com `GunSpellTracerPacket`. **CONDICIONADO**.
- **D — sem hook demonstrado:** não há contrato seguro para transformar o hit-scan em projétil persistente ou remover a janela de recuo. **NO_MUTATION** / fail-closed.

- `mutating_hook = NOT_VERIFIED`; `mutation = NO_MUTATION` (fail-closed).

## 8. Causalidade

`um cast instantâneo → rifle → três hit-scans nos ticks 5/8/11 → tracer/recuo → descarte no tick 20`.


## 9. Concepção de nova magia

Assinatura ocupada: "rajada de rifle hit-scan com recuo". Nenhuma implementação foi realizada.

## 10. Verificação e pendências

- ✅ identidade/hash, coeficientes 500/200/20/5/0, burst 3, alcance 48, ticks 5/8/11/20, tracer 24/8 e `IMagiAgentSuitAffectedSpell` confirmados no bytecode 1.0.1.1.
- ⚠️ multiplicador/mana efetivos, acerto real em PvP e sincronia de tracer em lag não certificados.
- ⚠️ `physical_qa=NOT_TESTED`: sem servidor Survival, PvP, portais, montarias, recast em combate real ou teleportes.
- ⚠️ Universo integral do provider não encerrado; homologação integral permanece `NOT_CERTIFIED`.


## Localizadores para Codex — resumo operacional

- `castTime=0` é coerente com `CastType.INSTANT`.
- Os três disparos usam o mesmo dano calculado no cast.
- `KEEP_WEAPON` mantém o rifle até o descarte no tick 20.
- Nenhum ponto de mutação segura demonstrado; manter fail-closed.

- Consultar [`EXACT-TECHNICAL-CONTRACTS-1.0.1.1.md`](../EXACT-TECHNICAL-CONTRACTS-1.0.1.1.md).
