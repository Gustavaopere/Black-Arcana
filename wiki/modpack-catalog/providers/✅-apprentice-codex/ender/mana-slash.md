# Mana Slash

**Estado do contrato:** ✅ `COMPLETE_PERK_READY` — `STATIC_TECHNICAL_CATALOG_ONLY` · `SHA_EXACT_BINARY_BEHAVIOR` · `mutating_hook=NOT_VERIFIED` · `physical_qa=NOT_TESTED`.

> O ✅ cobre exclusivamente a documentação estática SHA-exata deste objeto. Não homologa hook mutador, execução no pack, configuração efetiva, universo integral do provider nem QA físico.

## 1. Identidade e proveniência

| Campo | Valor verificado |
|---|---|
| Provider | Apprentice's Codex |
| Mod ID | `apprenticecodex` |
| Registry ID | `apprenticecodex:mana_slash` |
| Host | Iron's Spells 'n Spellbooks (`AbstractSpell`) |
| Escola | `SchoolRegistry.ENDER_RESOURCE` (Ender) |
| Raridade mínima | `SpellRarity.RARE` |
| Níveis | 1 (`DefaultConfig.setMaxLevel(1)`) |
| Tipo de cast | `CastType.INSTANT` |
| Cooldown declarado | `0.0` s |
| Recurso | Mana do Iron's (`baseManaCost=30`, `manaCostPerLevel=0`) |
| Aquisição | `setAllowCrafting(false)`, `allowLooting()=false` — não é scroll comum |
| JAR exato | `apprentice_codex-1.0.1.1-mc1.21.1.jar` |
| SHA-256 do JAR | `9C5244E75DBCA95BDAF48A85F0C189F8456149D1220BAD5FF339A86BCE04AC86` |
| SHA-1 do JAR | `A3F9C73EBD77D15B7E77AE14F4D0F695FEC3B7CF` |
| Ambiente | Minecraft 1.21.1 · NeoForge · Java 21 (JDK 21.0.12 na inspeção) |
| Classe de implementação | `jp.aquafactory.apprenticecodex.spell.manaslash.ManaSlash` |
| Evidência compartilhada | [`EXACT-TECHNICAL-CONTRACTS-1.0.1.1.md`](../EXACT-TECHNICAL-CONTRACTS-1.0.1.1.md) |

As versões 0.9.7.1 e 1.0.1 permanecem como histórico; nenhum valor foi reaproveitado sem confirmação no artefato físico 1.0.1.1.

## 2. Localizadores para o Codex

| Elemento | Localizador |
|---|---|
| Registro | `SpellRegistry.reg("mana_slash", ManaSlash::new)` |
| Config | `ManaSlash.config` (`RARE`, nível 1, cooldown `0.0`, `setAllowCrafting(false)`) |
| Coeficientes | `ManaSlash.<init>()`: `baseSpellPower=50`, `spellPowerPerLevel=25`, `baseManaCost=30`, `manaCostPerLevel=0`, `castTime=0` |
| Dano | `ManaSlash.getDamage(int,LivingEntity,ItemStack)` → `max(1, resolveCatalystWeaponDamage(...) * getSpellPowerPercent(...) / 100) * getDamageMultiplier()` |
| Fallback | `Utils.getWeaponDamage(entity)` no mesmo `max(1, dano*power/100)*multiplier` quando não há catalyst |
| Multiplicador | `ApprenticeCodexServerConfig.damageMultiplier(DamageMultiplierKey.MANA_SLASH)` |
| Catalyst | `SwingcastStaffCastContext.getCastingStack(uuid,this)`, `matches(uuid, spellId)` |
| Atributo da arma | `resolveDisplayedAttributeValue` posta `ItemAttributeModifierEvent` e soma `ADD_VALUE`, `ADD_MULTIPLIED_BASE`, `ADD_MULTIPLIED_TOTAL` em `MAINHAND`/`ATTACK_DAMAGE` |
| Gate de cast | `ManaSlash.canBeCastedBy(...)`: com contexto Swingcast e sem catalyst → `FAILURE` `ui.apprenticecodex.mana_slash.missing_catalyst` |
| Projétil | `ManaSlashProjectileEntity` (`SPEED=1.0`, `EXPIRE_TIME_TICKS=20`, `FADE_DURATION_TICKS=10`, `INITIAL_RADIUS=0.5`, `MAX_RADIUS=5.0`, `RADIUS_GROWTH_PER_TICK=0.45`, `BLOCK_COLLISION_WIDTH/HEIGHT=0.5`, `BLOCK_COLLISION_STEP=0.25`) |
| Spawn | `entity.getEyePosition().add(entity.getLookAngle().scale(0.35))`, `projectile.shoot(entity.getLookAngle())` |
| Render | `ManaSlashProjectileRenderer` |

Bytecode: `scratch/javap1011_ender10.txt` (`javap -classpath <JAR> -p -s -c`, `EXIT=0`, SHA-256 `0095E23B21918E38B4BD7D6C47DA8C3503753F0F988C00AB04A786060E2C50E5`); decompilação: `scratch/ender10_sources.txt` (SHA-256 `F3953EB8FCFB793EC501694E054E3C3CBE187E557B09B6CF158828692A97A645`).

## 3. Casting / execução

1. `AbstractSpell` resolve mana/cooldown/nível; `castTime=0`, `CastType.INSTANT`, cooldown declarado `0`.
2. `canBeCastedBy` verifica contexto Swingcast: se existe contexto mas `resolveCatalystStack` está vazio, falha com mensagem de catalyst ausente; caso contrário segue o caminho padrão do host.
3. `onCast` cria `MANA_SLASH_PROJECTILE`, posiciona na posição dos olhos deslocada `0.35 * lookAngle`, dispara na direção do olhar e grava o dano calculado.
4. Com catalyst: `resolveCatalystWeaponDamage` usa `entity.getAttributeBaseValue(ATTACK_DAMAGE)` e resolve o valor exibido da stack via `ItemAttributeModifierEvent`; se `displayDamage <= baseDamage`, subtrai o base. Sem catalyst: `Utils.getWeaponDamage(entity)`.
5. `level.addFreshEntity(projectile)`; o projétil cresce de `0.5` a `5.0` a `0.45` por tick, expira em `20` ticks e desvanece em `10` ticks.

## 4. Dano / geometria

| Propriedade | Valor e consumidor |
|---|---|
| Dano bruto | `max(1, referencedWeaponDamage * spellPowerPercent / 100)` |
| Dano final | bruto × `damageMultiplier(MANA_SLASH)` (server config; valor instalado **NÃO VERIFICADO**) |
| Spell power percent | `getSpellPower(spellLevel, entity)` (host aplica atributos) |
| Origem | olhos + `look*0.35` |
| Direção | `lookAngle` normal do casador |
| Velocidade | `SPEED=1.0` no projétil |
| Raio | `0.5` inicial, `+0.45`/tick, cap `5.0` |
| Hitbox de bloco | `0.5 × 0.5`, passo `0.25` |
| Vítimas | `victimIds` evita dano repetido na mesma entidade |
| Expiração | `20` ticks; fade `10` ticks |

Não há alvo automático: o disparo é na direção da visão do casador.

## 5. Resultado

- O projétil carrega `damage` e `animationSeed`; a cada tick incrementa raio e processa colisões com `victimIds`.
- `AntiMagicSusceptible`: anti-magia do Iron's pode afetar o projétil; o desfecho exato depende do host e não foi testado.
- Render pertence ao provider; não é uma entidade semântica nova.

## 6. Scaling e caps

| Parâmetro | Fórmula literal | Unidade / ownership |
|---|---|---|
| Spell power | `50 + 25*(level-1)` | nível único, efetivo `50` sem atributos |
| Mana | `30 + 0*(level-1)` | Iron's mana |
| Dano | `max(1, weaponDamage * power / 100) * multiplier` | referência de arma, não valor fixo |
| Multiplicador | `ApprenticeCodexServerConfig.damageMultiplier(MANA_SLASH)` | config do servidor **NÃO VERIFICADA** |
| Raio do projétil | `min(5.0, 0.5 + 0.45*t)` | blocos |
| Cooldown | `0.0` s | `DefaultConfig` |

## 7. Possibilidades de perks

- **A — atributo nativo:** spell power e mana via `AbstractSpell`; o dano depende também da arma/catalyst e da config do servidor.
- **B — evento verificado:** `ItemAttributeModifierEvent` é usado para **ler** o dano exibido da arma; publicar um modificador externo pode alterar o valor lido, mas isso é contrato de atributo do Minecraft/NeoForge, não hook de mutação da spell. `canBeCastedBy` e `onCast` são execução do provider.
- **C — adapter condicionado:** mudar spawn, raio, dano ou o gate de catalyst exigiria substituir `ManaSlash.onCast` e `ManaSlashProjectileEntity` com contrato de dano e colisão. **CONDICIONADO**.
- **D — sem hook demonstrado:** não há API segura comprovada para redirecionar o ataque para área, alterar o multiplicador sem config ou duplicar o projétil. **NO_MUTATION / fail-closed**.
- `mutating_hook = NOT_VERIFIED`.

## 8. Causalidade

`um cast → um projétil → dano de arma referenciado, crescimento de área e colisão única por vítima`.

Todos os efeitos pertencem à raiz `mana_slash`; o catalyst é insumo, não novo cast. Black Arcana não deve re-liquidar dano nem adicionar Mastery por tick de projétil.

## 9. Concepção de nova magia

Assinatura ocupada: "slash de mana projetado cujo dano referencia a arma/catalyst". Nenhuma implementação foi realizada.

## 10. Verificação e pendências

- ✅ Identidade/hash, coeficientes, fórmula de dano, gate de catalyst, atributos resolvidos e constantes do projétil confirmados no bytecode 1.0.1.1.
- ⚠️ Multiplicador instalado, contexto Swingcast em gameplay real e aquisição do item catalyst não certificados.
- ⚠️ `physical_qa=NOT_TESTED`: sem servidor Survival, PvP, anti-magia ou item real.
- ⚠️ Universo integral do provider não encerrado.

## Localizadores para Codex — resumo operacional

- `getWeaponDamage` é fallback; com contexto Swingcast, a stack é obrigatória.
- O dano não é constante: deriva de `ATTACK_DAMAGE` resolvido via evento NeoForge.
- Nenhum ponto de mutação segura demonstrado; manter fail-closed.
- Consultar [`EXACT-TECHNICAL-CONTRACTS-1.0.1.1.md`](../EXACT-TECHNICAL-CONTRACTS-1.0.1.1.md).
