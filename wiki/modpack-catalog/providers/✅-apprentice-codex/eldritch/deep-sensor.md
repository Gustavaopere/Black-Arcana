# Deep Sensor

**Estado do contrato:** ✅ `COMPLETE_PERK_READY` — `STATIC_TECHNICAL_CATALOG_ONLY` · `SHA_EXACT_BINARY_BEHAVIOR` · `mutating_hook=NOT_VERIFIED` · `physical_qa=NOT_TESTED`.

> O ✅ cobre exclusivamente a documentação estática SHA-exata deste objeto. Não homologa hook mutador, execução no pack, configuração efetiva nem universo integral do provider.

## 1. Identidade e proveniência

| Campo | Valor verificado |
|---|---|
| Provider | Apprentice's Codex |
| Mod ID | `apprenticecodex` |
| Nome de exibição | Deep Sensor (nome funcional, não traduzido) |
| Registry ID | `apprenticecodex:deep_sensor` |
| Host | Iron's Spells 'n Spellbooks (`AbstractSpell`) |
| Escola | `SchoolRegistry.ELDRITCH_RESOURCE` (Eldritch) |
| Raridade mínima | `SpellRarity.LEGENDARY` |
| Níveis | 1–3 (`DefaultConfig.setMaxLevel(3)`) |
| Tipo de cast | `CastType.INSTANT` |
| Cooldown declarado | `100.0` s |
| Recurso | Mana do Iron's (`baseManaCost=60`, `manaCostPerLevel=20`) |
| JAR exato | `apprentice_codex-1.0.1.1-mc1.21.1.jar` |
| SHA-256 do JAR | `9C5244E75DBCA95BDAF48A85F0C189F8456149D1220BAD5FF339A86BCE04AC86` |
| SHA-1 do JAR | `A3F9C73EBD77D15B7E77AE14F4D0F695FEC3B7CF` |
| Ambiente | Minecraft 1.21.1 · NeoForge 21.1.250 · Java 21 (JDK 21.0.12 na inspeção) |
| Classe de implementação | `jp.aquafactory.apprenticecodex.spell.deepsensor.DeepSensor` |
| Evidência compartilhada | [`EXACT-TECHNICAL-CONTRACTS-1.0.1.1.md`](../EXACT-TECHNICAL-CONTRACTS-1.0.1.1.md) |

## 2. Localizadores para o Codex

| Elemento | Localizador |
|---|---|
| Registro | `SpellRegistry.reg("deep_sensor", DeepSensor::new)` |
| Config | `DeepSensor.config`: `LEGENDARY`, `ELDRITCH_RESOURCE`, `maxLevel=3`, `cooldownSeconds=100.0` |
| Coeficientes | `DeepSensor.<init>()`: `baseSpellPower=100`, `spellPowerPerLevel=50`, `baseManaCost=60`, `manaCostPerLevel=20`, `castTime=0` |
| Duração / alcance informativo | `DeepSensor.getDuration(int,LivingEntity)`, `DeepSensor.getRange()` → `24` |
| Aplicação | `DeepSensor.onCast(...)` → `EffectRegistry.SENSE_SENSOR` |
| Evento/vibração | `jp.aquafactory.apprenticecodex.spell.deepsensor.SenseSensorVibrationEvent` |
| Listener ativo | `SenseSensorVibrationEvent.ActiveListener` (`VibrationSystem`, `DynamicGameEventListener`) |
| Buffer | `jp.aquafactory.apprenticecodex.spell.deepsensor.DeepSensorObservationBuffer` |
| Cliente | `jp.aquafactory.apprenticecodex.spell.deepsensor.DeepSensorClientDisplay` |
| Efeito | `jp.aquafactory.apprenticecodex.effect.SenseSensor` |
| Rede | `jp.aquafactory.apprenticecodex.network.packet.DeepSensorObservationsPacket` |

Descritores e offsets JVM foram reconsultados no JAR 1.0.1.1: saída `scratch/javap1011_legacy.txt` (`javap -classpath <JAR> -p -s -c`, `EXIT=0`, 233.376 bytes, SHA-256 `F59E0944BA6C04BF5A2B3A28145C9403B225EDF7EEC8425D4A0B6E189F63CCF3`) e anotações/constantes em `scratch/javap1011_v.txt` (`EXIT=0`), não publicadas integralmente.

## 3. Casting / execução

1. `CastType.INSTANT`, `castTime=0`; Iron's owned mana/cooldown/nível.
2. `onCast` adiciona `EffectRegistry.SENSE_SENSOR` ao caster com duração `Math.round(spellPower*6)` ticks, amplifier `0`, `ambient=false`, `visible=false`, `showIcon=true`.
3. `SenseSensorVibrationEvent.onPlayerTick(Post)` cria um `SensorState` para `ServerPlayer` vivo com o efeito, usando o `ServerLevel` atual.
4. `SensorState` instancia `ActiveListener`: `DynamicGameEventListener` com `EntityPositionSource(owner, owner.getBbHeight()*0.5)` e raio `24`.
5. Mudança de dimensão, logout, morte ou perda do efeito remove o listener; mudança de dimensão também limpa estado; observações persistem apenas enquanto o state existir.
6. `finish` implícito: ao expirar o efeito e esvaziar o buffer, o estado é removido por UUID.

Som de cast: `SoundEvents.SCULK_SENSOR_PLACE`; animação: `SpellAnimations.TOUCH_GROUND_ANIMATION`.

Guardas e custos são owned pelo Iron's. No JAR físico do host, `AbstractSpell.getManaCost(int)` (`(I)I`, offsets 0–29) calcula `(baseManaCost + manaCostPerLevel*(level-1)) * MANA_MULTIPLIER` e trunca com `d2i`; `getSpellCooldown()` (`()I`, offsets 0–18) calcula `COOLDOWN_IN_SECONDS * 20.0d` e trunca com `d2i`; `getCastTime(int)` (`(I)I`, offsets 0–16) retorna `0` para `CastType.INSTANT`. `getSpellPower(int,Entity)` (`(ILnet/minecraft/world/entity/Entity;)F`, offsets 0–79) multiplica ainda por `AttributeRegistry.SPELL_POWER`, `SchoolType.getPowerFor(LivingEntity)` e `POWER_MULTIPLIER`; `getLevelFor(int,LivingEntity)` (`(ILnet/minecraft/world/entity/LivingEntity;)I`, offsets 0–64) aplica Curios e `ModifySpellLevelEvent`. Assim, `60`, `20`, `100`, `50`, `100.0` e `castTime=0` são coeficientes declarados pelo Apprentice Codex; mana, cooldown, power, duração e nível efetivos dependem da config instalada do Iron's, atributos e eventos, **NÃO VERIFICADOS**. Ver âncoras em [`EXACT-TECHNICAL-CONTRACTS-1.0.1.1.md`](../EXACT-TECHNICAL-CONTRACTS-1.0.1.1.md).

## 4. Targeting / geometria

| Propriedade | Valor e consumidor |
|---|---|
| Alvo | O próprio caster (`ServerPlayer`); nenhum alvo hostil é selecionado. |
| Raio do listener | `LISTENER_RADIUS = 24`; `VibrationUser.getListenerRadius()` retorna `24`. |
| Posição da fonte | `EntityPositionSource(owner, altura da hitbox * 0.5)`. |
| Travel time | `Mth.clamp(Mth.floor(distance), 1, 3)` ticks. |
| Chunks | `requiresAdjacentChunksToBeTicking() = true`. |
| Own vibrations | `canReceiveVibration` rejeita `sourceEntity == owner`, passageiro controlado, veículo raiz, projétil com `getOwner()==owner` e `ItemEntity` com `getOwner()==owner`. |
| Eventos silenciados | `STEP`, `SWIM`, `HIT_GROUND`, `SPLASH`, `ELYTRA_GLIDE`, `UNEQUIP`, `ENTITY_DISMOUNT`, `EQUIP`, `ENTITY_MOUNT`, `ENTITY_DAMAGE`; `VanillaGameEvent` é cancelado quando a causa é `LivingEntity` com o efeito. |
| AOE ofensiva | `N/A`: não há dano, caixa de ataque ou projétil. |

## 5. Resultado

- `record` guarda `BlockPos`, distância, `gameTime`, `expiresAtGameTime = receipt + 40`, `sourceUuid`, `projectileOwnerUuid` e `ResourceLocation` do game event.
- Chave de dedup: `ObservationKey.forEntity(sourceUuid)` quando há fonte; senão `forPosition(position)`.
- Capacidade: `OBSERVATION_LIFETIME_TICKS=40`, `MAX_RETAINED_OBSERVATIONS=64`, `MAX_DISPLAYED_OBSERVATIONS=8`; trim remove o mais antigo por `receivedGameTime`.
- `selectForDisplay`: poda expirados, mantém o mais recente por posição, descarta distância zero ao centro do observador, ordena por distância crescente e `receivedGameTime` decrescente, limita a 8.
- Heartbeat: `100` ticks enquanto houver observações visíveis; som `SoundEvents.SCULK_CLICKING` ao aparecer/heartbeat e `SCULK_CLICKING_STOP` ao desaparecer/limpar.
- Sync: `Networks.sendToPlayer(owner, new DeepSensorObservationsPacket(dimension, displayed))`.
- Cliente: só substitui se a dimensão do pacote coincidir; direção visual normalizada `× 4.0` blocos; pulso com 4 estágios; intervalo `Math.round(lerp(clamp((distance-8)/16,0,1),4,10))` ticks; cor HSV com hue `lerp(..., 0.0, 0.75)`; core `0.1` e alpha `0.75`; renderização através de paredes.

## 6. Scaling e caps

| Parâmetro | Fórmula literal | Unidade / ownership |
|---|---|---|
| Spell power | `100 + 50*(level-1)` conforme `AbstractSpell` | provider host |
| Mana | `60 + 20*(level-1)` | Iron's mana; default declarado |
| Duração | `Math.round(spellPower * 6)` | ticks |
| Raio | `24` constante | blocos |
| Travel | `clamp(floor(distance),1,3)` | ticks |
| Buffer | `40` ticks / `64` registros / `8` exibidos | constantes verificadas |
| Heartbeat | `100` ticks | constante verificada |
| Cooldown | `100.0` s | `DefaultConfig` |

Nenhum multiplicador de servidor para alcance ou duração foi localizado neste escopo.

## 7. Possibilidades de perks

- **A — atributo nativo:** spell power/mana/cooldown via `AbstractSpell`; não é hook de mutação demonstrado.
- **B — evento/callback verificado:** `VanillaGameEvent` cancelado e `DeepSensorObservationsPacket` sincronizado são provider-owned. Não foi demonstrado ponto seguro para perk alterar raio, filtro de eventos, buffer ou visual. **NO_MUTATION / fail-closed**.
- **C — adapter condicionado:** estender raio/duração ou adicionar eventos exigiria substituir `ActiveListener` e o protocolo de sync com preservação de dimension/UUID. **CONDICIONADO**.
- **D — sem hook demonstrado:** transformar sensor em dano, revelar entidades além do pacote ou duplicar observações não tem API/mixin seguro comprovado neste escopo.
- `mutating_hook = NOT_VERIFIED`.

## 8. Causalidade

`um cast → efeito SENSE_SENSOR → listener server-side por tick → vibração recebida → registro com delay → buffer podado/ordenado → pacote para o cliente → pulso/heartbeat`.

O heartbeat e os pulsos não são casts nem procs ofensivos. Black Arcana não deve awardar mastery por observação, nem tratar eventos silenciados como dano evitado pelo jogador.

## 9. Concepção de nova magia

Assinatura ocupada: "efeito de detecção por vibração com raio 24, filtro de eventos e visual através de paredes". Uma magia original Black Arcana precisaria de semântica materialmente distinta (por exemplo, eco mágico com retardo fixo e sem listener vanilla, ou detecção de mana em vez de game events) para não duplicar esta identidade. Nenhuma implementação foi realizada.

## 10. Verificação e pendências

- ✅ Identidade, versão e hash do JAR; registro e classe; coeficientes; duração; raio; eventos; buffer; protocolo e render; limites de validação.
- ⚠️ Configuração efetiva do pack não lida; nenhum valor de config foi promovido.
- ⚠️ `physical_qa=NOT_TESTED`: sem cliente, servidor, Survival, PvP ou modpack real.
- ⚠️ `SenseSensor` como efeito autônomo não auditado além do registration/consumo pelo listener; comportamento de IA/hostilidades não observado.
- ⚠️ Universo integral do provider não encerrado: recorte observado de 15 fichas.

## Localizadores para Codex — resumo operacional

- Não confundir `getRange()` informativo com raio de dano: aqui ambos são `N/A` ofensivo e `24` de listener.
- Não tratar eventos cancelados ou pacotes como ponto de mutação por perk sem contrato demonstrado.
- Consultar [`EXACT-TECHNICAL-CONTRACTS-1.0.1.1.md`](../EXACT-TECHNICAL-CONTRACTS-1.0.1.1.md) para hashes, comandos e limites da prova.
