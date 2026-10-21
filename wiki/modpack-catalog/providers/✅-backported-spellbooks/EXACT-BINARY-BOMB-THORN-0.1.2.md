# Backported Spellbooks 0.1.2 — Sulfur Bomb e Pale Thorn: geometria, alcance e dano no bytecode

**18/10/2026 · ✅ `EXACT_PUBLISHER_BOUND_METHOD_OPERANDS` em dois spells e duas entidades · ⚠️ host, dano real e sobrevivência não observados · ⛔ adapters de perks/Mastery não autorizados.**

## JAR, verificador e limites

- `backportedspellbooks-0.1.2.jar` publicado em CurseForge **1543731 / 8158731**, 209.868 bytes; mod ID `backportedspellbooks`, metadata embutida `0.1.0` preservada em vez de corrigida por suposição. SHA-1 **`747847c1f38c73250ebac05ea06b41a381187850`** idêntico ao hash já certificado do snapshot físico. A publicação foi baixada pelo runner, não releitura do diretório local do jogador.
- [GitHub Actions Java21 #39133252975](https://github.com/Gustavaopere/Black-Arcana/actions/runs/39133252975) **SUCCESS**: 10/10 autotestes da nova verificação, `PASS_BACKPORTED_012_BOMB_THORN_BOUNDED_BYTECODE`, `deviations=[]`. O job antigo das outras três skills também concluiu no mesmo workflow, com integridade publisher verificada.
- [Artefato JSON #12138732504](https://github.com/Gustavaopere/Black-Arcana/actions/runs/39133252975/artifacts/12138732504) publica provas reduzidas, **não** o JAR de terceiros; [verificador read-only](../../../../docs/qa/backported_012_bomb_thorn_bytecode.py) e [workflow](../../../../.github/workflows/backported-spellbooks-012-perk-bytecode.yml).
- O verificador exige **nomes de métodos, operadores e constantes** no JAR exato. Testes negativos rejeitam raio 4 no lugar de 3, coeficiente 0.18 no lugar de 0.185, duração de status 180 no lugar de 200, alcance 14 no lugar de 15, atributo incorreto, calls duplicadas e ordem invertida. A análise é **bounded javap**; não demonstra execução de ramo em runtime, todos os caminhos de bytecode, config Iron's, hook público ou quantidade final de dano.

## Sulfur Bomb — do cast até o dano radial

| Método físico | Operandos/callsites confirmados | Uso correto para perk |
|---|---|---|
| `SulfurBombSPell.getRadius` | `3.0f`, `getEntityPowerMultiplier(caster)`, `fadd` | raio declarado no supplier é `3+multiplier`, não raio final medido em servidor |
| `SulfurBombSPell.getDamage` | `baseSpellPower`, `getEntityPowerMultiplier`, `fmul` | a base de dano depende de config/atributos do host |
| `SulfurBombSPell.getAOEDamage` | `getSpellPower`, `0.185f`, `fmul` | é um **segundo parâmetro**, enviado à entidade de gás; não duplicar no impacto |
| `SulfurBombProjectile.getSpeed` | `1.15f` e `freturn` | velocidade declarativa do projétil, sujeita ao uso pela infraestrutura de host |
| `SulfurBombProjectile.onHitEntity` | guard `Level.isClientSide`, `createFireField`, `impactParticles`, `getExplosionRadius`, `AABB.inflate(radius)`, `Level.getEntities`, `raycastForBlock`, `Entity.distanceToSqr`, guarda `distanceSq<radius²`, `canHitEntity` e `hasLineOfSight` antes de dano | **AABB expandida seleciona candidatos**; distância Euclidiana ao impacto e LOS são filtros adicionais. Isso não constitui raio de colisão garantido para qualquer alvo |
| `onHitEntity` — quantidade | `ddiv`, `dsub`, `getfield damage`, `dmul`, `DamageSources.applyDamage` | expressão source-aligned `damage × (1 − distanceSq/radiusSq)`; resultados dependem de distância e provider/host, não HP final |
| `onHitEntity` — status | depois de `applyDamage`, callsites `MobEffects.WITHER` e `MobEffects.CONFUSION`, ambos `sipush 200` ticks e `LivingEntity.addEffect`; depois `discard` | parâmetros de status são distintos de dano; nenhum teste provou efeitos realmente aplicados |
| `SulfurBombProjectile.createFireField` | novo `SulfurGasCloud`, `setDuration(200)`, `setDamage(aoeDamage)`, `setRadius(explosionRadius)`, `Level.addFreshEntity` | nuvem é entidade secundária do **mesmo cast**; a duração 200 é configurada no método, não prova de lifetime real sob efeitos do host |
| `SulfurBombProjectile.onHitBlock` | `createFireField`, 3 callsites de `setDeltaMovement` em ramos de face, incrementa `bounces`, compara com `3` e descarta | o limite de três é o **contador de colisões no ramo de bloco**; não é quantidade máxima de vítimas ou de nuvens em toda situação |

**Risco de integração encontrado:** `onHitEntity` itera candidatos retornados por `Level.getEntities` e contém `checkcast LivingEntity` depois de `DamageSources.applyDamage`. Isso **não** prova `ClassCastException` para alvo não vivo: `canHitEntity` e demais regras podem filtrar candidatos; o comportamento real precisa de teste isolado. O código-fonte oficial do dia da release também aplica status nesse caminho, mas a observação binária não testou o fluxo com entidades vivas/não vivas.

**Causalidade:** a conjuração cria um projétil; colisões podem criar nuvens, aplicar dano e status. Não aumentar Mastery por cada `applyDamage`, `addFreshEntity` ou `addEffect`. Uma perk de raio/dano/tipo/duração precisa de boundary provider-native e não pode repetir a explosão pelo Black Arcana.

Referências oficiais source-adjacent da publicação (apenas interpretação e nomes, a release **não** foi reproduzida byte a byte): [`SulfurBombSPell.java`](https://github.com/RedReaper28/BackportedSpellbooks-1.21.1/blob/07cb65efca0c264762a21c2d6bce0f83e3947226/src/main/java/net/redreaper/backported_spellbooks/spells/nature/SulfurBombSPell.java), [`SulfurBombProjectile.java`](https://github.com/RedReaper28/BackportedSpellbooks-1.21.1/blob/07cb65efca0c264762a21c2d6bce0f83e3947226/src/main/java/net/redreaper/backported_spellbooks/entities/spell/sulfur_bomb/SulfurBombProjectile.java), [`SulfurGasCloud.java`](https://github.com/RedReaper28/BackportedSpellbooks-1.21.1/blob/07cb65efca0c264762a21c2d6bce0f83e3947226/src/main/java/net/redreaper/backported_spellbooks/entities/spell/sulfur_bomb/SulfurGasCloud.java). O tratamento interno de dano/ticks do `SulfurGasCloud` ainda não foi gateado neste teste.

## Pale Thorn — seleção de alvo, status e entidade visual

| Método físico | Operandos/callsites confirmados | Uso correto para perk |
|---|---|---|
| `PaleThornSpell.getRange` | retorna `15.0f` diretamente | **alcance configurado no método**, não garantia de detectar entidade até 15 blocos |
| `PaleThornSpell.getDuration` | `getSpellPower`, `100.0f`, `fmul`, `f2i` | duração do efeito (ticks) trunca o float; não converter em duração da animação/VFX |
| `PaleThornSpell.getDamage` | se caster nulo: `getSpellPower*1.5f`; se não nulo, lê `NATURE_SPELL_POWER`, `ELDRITCH_SPELL_POWER`, coeficientes `5.0`, `0.4f` convertido a double e `0.5` por atributo | correspondência à expressão source-adjacent `5 + 0.4 × spellPower × (0.5 × Nature + 0.5 × Eldritch)`; não confundir com percentuais de buffs ou tipo de dano final |
| `PaleThornSpell.onCast` | `getRange`, `false`, `0.15f`, `Utils.raycastForEntity`, cria `PaleThornVisualEntity`, `Level.addFreshEntity`, depois ramifica por `HitResult.Type.ENTITY` | VFX é gerada antes do switch de hit; no ramo ENTITY existe apenas um `DamageSources.applyDamage`, não uma nova conjuração |
| `onCast` — efeito | `getDuration`, `getDamage`, `applyDamage`, `PARANOIA`, construtor `MobEffectInstance` e `LivingEntity.addEffect`, seguido de ramo BLOCK de partículas | duração do status e vida da VFX são entidades de medição diferentes |
| `PaleThornVisualEntity.tick` | compara `tickCount` ao limite `30` com `if_icmple`, então `discard` | visual descartável após ultrapassar 30 ticks nesse método, não range nem duração do Paranoia |

No método `PaleThornSpell.onCast` **não foi observado um callsite direto** a `DamageSources.isFriendlyFireBetween`; a função de raycast e o helper de dano podem aplicar filtros próprios **não testados**, portanto não classificar automaticamente como falha de PvP. `0.15f` é argumento de `Utils.raycastForEntity`, não um hitbox override exposto ao modpack. A classificação e o tratamento de entidades não-vivas em raycast, buffs e dano precisam de QA real.

Referências source-adjacent: [`PaleThornSpell.java`](https://github.com/RedReaper28/BackportedSpellbooks-1.21.1/blob/07cb65efca0c264762a21c2d6bce0f83e3947226/src/main/java/net/redreaper/backported_spellbooks/spells/nature/PaleThornSpell.java), [`PaleThornVisualEntity.java`](https://github.com/RedReaper28/BackportedSpellbooks-1.21.1/blob/07cb65efca0c264762a21c2d6bce0f83e3947226/src/main/java/net/redreaper/backported_spellbooks/entities/spell/pale_thorn/PaleThornVisualEntity.java).

## Fronteiras e próximos gates

**Iron's** continua responsável pelo `onCast` host, configurações efetivas, mana, cooldown, `getSpellPower`, damage helper e raycast. **Backported Spellbooks** controla seus projéteis, nuvem, efeitos e identidade. **Black Arcana** conserva o runtime mágico próprio; **RPG Skill Tree** somente perks/atributos/Mastery/gates por contrato real. Não criar segundo processador de dano, novo projectile ou cast de retorno por simetria temática.

Ainda ⚠️: propriedades completas de `SulfurGasCloud` sob Iron's 3.16.3; linha de visão, friendly-fire/claims e multiplicador real; aplicação e duração de Paranoia/Wither/Confusion; ataques em cliente e Survival; compatibilidade com o NeoForge físico do perfil; performance e ticks/clean-up; hooks e APIs de extensão. Sem boundary, ⛔ para novas perks.

**Cobertura:** seis registros ✅, seis fichas source-pinned ✅, agora **cinco spells distintas** com partes do código compilado verificadas (Sulfur Clouds, Sulfur Release, Resin Spray, Sulfur Bomb e Pale Thorn); Slime Aspect permanece apenas com identidade binária e parâmetros source-pinned. **5/6 não significa 83% de gameplay ou de integração.** +0 raízes/novas magias, +0 adapters. Piso global 1.857 semânticos / 1.855 estritos, denominador total —%. Stage 06.05 🟡; Stage 09 físico PENDING; PR #825 em draft, sem merge.
