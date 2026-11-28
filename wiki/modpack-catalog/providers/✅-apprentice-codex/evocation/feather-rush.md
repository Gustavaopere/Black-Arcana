# Feather Rush

**Estado do contrato:** ✅ `COMPLETE_PERK_READY` — `STATIC_TECHNICAL_CATALOG_ONLY` · `SHA_EXACT_BINARY_BEHAVIOR` · `mutating_hook=NOT_VERIFIED` · `mutation=NO_MUTATION` · `physical_qa=NOT_TESTED` · `perk_certification=NOT_CERTIFIED`.

> O ✅ cobre exclusivamente a documentação estática SHA-exata deste objeto. Não homologa hook mutador, execução no pack, configuração efetiva, universo integral do provider nem QA físico.

## 1. Identidade e proveniência

| Campo | Valor verificado |
|---|---|
| Provider | Apprentice's Codex |
| Mod ID | `apprenticecodex` |
| Registry ID | `apprenticecodex:feather_rush` |
| Host | Iron's Spells 'n Spellbooks (`AbstractSummonWeaponSpell<FeatherRushWingEntity>`) |
| Interfaces | sem interface adicional declarada |
| Escola | `SchoolRegistry.EVOCATION_RESOURCE` (Evocation) |
| Raridade mínima declarada | `EPIC` |
| Níveis declarados | 1–5 (`setMaxLevel(5)`) |
| Tipo de cast | `CONTINUOUS` |
| Cooldown declarado | `12.0 s` |
| Recurso | Mana do Iron's (`baseManaCost=4`, `manaCostPerLevel=2`) |
| JAR exato | `apprentice_codex-1.0.1.1-mc1.21.1.jar` |
| SHA-256 do JAR | `9C5244E75DBCA95BDAF48A85F0C189F8456149D1220BAD5FF339A86BCE04AC86` |
| SHA-1 do JAR | `A3F9C73EBD77D15B7E77AE14F4D0F695FEC3B7CF` |
| Ambiente | Minecraft 1.21.1 · NeoForge · Java 21 (JDK 21.0.12 na inspeção) |
| Classe de implementação | `jp.aquafactory.apprenticecodex.spell.featherrush.FeatherRush` |
| Auxiliares da mesma raiz | `FeatherRushWingEntity`, `FeatherRushProjectileEntity`, `FeatherRushGravityControlEvent`, `FeatherRushState` |
| Evidência compartilhada | [`EXACT-TECHNICAL-CONTRACTS-1.0.1.1.md`](../EXACT-TECHNICAL-CONTRACTS-1.0.1.1.md) |

As versões 0.9.7.1 e 1.0.1 permanecem como histórico; nenhum valor foi reaproveitado sem confirmação no artefato físico 1.0.1.1. Os coeficientes declarados não são os valores efetivos instalados: mana, cooldown, spell power, nível, raridade e multiplicadores do host permanecem `NÃO VERIFICADOS` (`AbstractSpell` lê `SpellConfigManager`, atributos, Curios e eventos).

## 2. Localizadores para o Codex

| Elemento | Localizador |
|---|---|
| Registro | `SpellRegistry.reg("feather_rush", FeatherRush::new)` |
| Config | `EPIC`, nível 5, cooldown `12.0`, `EVOCATION_RESOURCE` |
| Coeficientes | <init>: `baseSpellPower=100`, `spellPowerPerLevel=75`, `baseManaCost=4`, `manaCostPerLevel=2`, `castTime=100` |
| Dano | `getDamage` → `(1 + 2.5*power/100) * damageMultiplier(FEATHER_RUSH)` |
| RPM | `power 100→400` gera RPM linear `300→900` (`TICKS_PER_MINUTE=1200.0`); burst mínimo `2` ticks e `2` projéteis |
| Cone | `RaycastTools.randomRotateInCone(look,45.0F,random)`; yaw `35±22.5°`, pitch `0–60°` |
| Projétil | `LIFE_TICKS=100`, recuo `10` ticks a `0.05`, avante `1.75`, `DamageTypes.FEATHER_RUSH` |
| Asas/estado | `FIRE_SIDE_OFFSET=0.5`, `ACTIVE_TICK_GRACE=2`, `FeatherRushGravityControlEvent` zera `fallDistance` e aplica gravidade zero |

Bytecode: scratch/javap1011_evocation10.txt (`javap -classpath <JAR> -p -s -c`, 61 classes, EXIT=0, SHA-256 `B872A0B86732D7EAE026532ED358AD9BBDFB7B1D7BCFCA2C6B35F13EADD9A2D5`); decompilação de apoio: scratch/evocation10_sources.txt (44 fontes Vineflower 1.12.0, SHA-256 `BCAF5695AA5346DABC0D976D8EBFA327B7622570230DE48B4330396876448387`). Constantes e fórmulas decisivas foram confrontadas com o bytecode; em divergência, o bytecode prevalece.

## 3. Casting / execução

1. `onCastNoWeapon` cria `FeatherRushWingEntity`; `onCastTickWithWeapon` calcula `BurstSettings` a cada tick e dispara quando `weapon.tickCount % fireIntervalTicks == 0`.
2. `getBurstSettings` escolhe o par (intervalo, projéteis) que minimiza o erro contra o RPM alvo (`300→900`), com piso `2` ticks e `2` projéteis.
3. Cada projétil recebe `setDamage(getDamage(...))`, direção de avanço em cone de `45°` em torno do olhar e direção inicial "para trás" com viés de yaw `35°` e aleatoriedade `45°/60°`.
4. `setStraightFlightDirections(..., random.nextInt(1,4))` estende o recuo para `10–13` ticks; o projétil recua a `0.05` e então avança a `1.75` com direção travada pelo olhar do dono.
5. `FeatherRushProjectileEntity.tick` descarta após `100` ticks, usa `ProjectileUtil.getHitResultOnMoveVector` e aplica `CombatTools.applySpellDamage(...,DamageTypes.FEATHER_RUSH,KnockbackTypes.DEFAULT)` somente a alvos válidos.
6. `FeatherRushGravityControlEvent` mantém gravidade zero enquanto a asa é válida, zera `fallDistance`, cancela velocidade Y negativa e limpa o estado ao shift/água/voo/expiração (`ACTIVE_TICK_GRACE=2`).
7. `onCastCompleteWithWeapon` sempre retorna `RELEASE_WEAPON`; a asa é componente da mesma raiz.

## 4. Targeting / geometria

| Propriedade | Valor e consumidor |
|---|---|
| Direção de dano | Cone de `45°` em torno de `lookAngle` |
| Direção inicial | Recuo com yaw `35±22.5°` e pitch `0–60°`, aleatório |
| Origem | `RotationTools.calculateBehindPosition(wing, 0.0, ±0.5, -0.5+(rand-0.5)*0.125)` |
| Projéteis | `2` mínimo por burst; vida `100` ticks |
| Velocidades | Recuo `0.05` por `10+delay` ticks; avante `1.75` |
| RPM | `300→900` entre poder `100→400`, quantizado pelo par intervalo/projéteis |
| Controle aéreo | Gravidade zero, `fallDistance=0`, somente fora d'água/elytra/voo criativo |

## 5. Resultado

- Cada projétil causa dano direto uma vez, com `KnockbackTypes.DEFAULT`.
- As penas voltam e avançam; não são projéteis perfurantes nem AOE persistente.
- O evento de gravidade é parte da mesma raiz: sem asa válida, o controle aéreo é desligado.

## 6. Scaling e caps

| Parâmetro | Fórmula literal | Unidade / ownership |
|---|---|---|
| Spell power | `100 + 75*(level-1)` | float declarado |
| Dano | `(1 + 2.5*power/100) * damageMultiplier(FEATHER_RUSH)` | config **NÃO VERIFICADA** |
| RPM alvo | `max(1, round(300 + 600*(power-100)/300))`, **sem clamp superior** | disparos/minuto; convertido em pares discretos |
| Burst | `min 2` projéteis, `min 2` ticks | par discretizado |
| Mana/cooldown/cast | `4+2*(level-1)` / `12.0` s / `100` ticks | host + config **NÃO VERIFICADA** |

## 7. Possibilidades de perks

- **A — atributo nativo:** dano e RPM respondem ao poder; mana/cooldown ao `AbstractSpell`.
- **B — evento verificado:** `PlayerTickEvent.Pre` controla gravidade do jogador, sem API de configuração de parâmetros de disparo.
- **C — adapter condicionado:** mudar cone, velocidade ou contagem de projéteis exigiria substituir raiz, asa, projétil e evento. **CONDICIONADO**.
- **D — sem hook demonstrado:** não há contrato seguro para converter a rajada em área contínua ou remover o piso de 2 projéteis. **NO_MUTATION** / fail-closed.

- `mutating_hook = NOT_VERIFIED`; `mutation = NO_MUTATION` (fail-closed).

## 8. Causalidade

`um cast contínuo → asa → rajadas quantizadas → projéteis com recuo/avante → controle aéreo enquanto a asa existir`.


## 9. Concepção de nova magia

Assinatura ocupada: "rajada de penas com controle de gravidade". Nenhuma implementação foi realizada.

## 10. Verificação e pendências

- ✅ identidade/hash, coeficientes 100/75/4/2/100, dano `(1+2.5*power/100)`, RPM 300→900, cone 45°, constantes do projétil e evento de gravidade confirmados no bytecode 1.0.1.1.
- ⚠️ multiplicador instalado, RPM real em servidor e sincronia de `FeatherRushState` em lag não certificados.
- ⚠️ `physical_qa=NOT_TESTED`: sem servidor Survival, PvP, portais, montarias, recast em combate real ou teleportes.
- ⚠️ Universo integral do provider não encerrado; homologação integral permanece `NOT_CERTIFIED`.


## Localizadores para Codex — resumo operacional

- RPM é alvo contínuo convertido em pares discretos (intervalo, projéteis).
- `10+delay` ticks de recuo e `1.75` de avante são grandezas distintas.
- Controle de gravidade exige asa válida; Shift cancela.
- Nenhum ponto de mutação segura demonstrado; manter fail-closed.

- Consultar [`EXACT-TECHNICAL-CONTRACTS-1.0.1.1.md`](../EXACT-TECHNICAL-CONTRACTS-1.0.1.1.md).
