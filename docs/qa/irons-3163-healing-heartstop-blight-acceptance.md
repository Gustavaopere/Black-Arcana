# Iron's 3.16.3 — protocolo físico de cura, Blight e dano diferido Heartstop

**Status:** ⚠️ matriz de aceitação **não executada** no modpack; fonte de comportamento fixada, Java 21 e NeoForge 21.1.248 alvo. **Não** promove Stage 06.05 e **não** habilita Mastery/perks. Versão documental de Iron's **3.16.3**; fingerprint físico do perfil **não fornecido**.

## Fontes de verdade

- [Heartstop](../../wiki/modpack-catalog/providers/✅-irons-spells/audits/CAUSAL-PERKS-HEARTSTOP-3.16.3.md), [Heal](../../wiki/modpack-catalog/providers/✅-irons-spells/audits/CAUSAL-PERKS-HEAL-3.16.3.md), [Greater Heal](../../wiki/modpack-catalog/providers/✅-irons-spells/audits/CAUSAL-PERKS-GREATER-HEAL-3.16.3.md) e [Blight](../../wiki/modpack-catalog/providers/✅-irons-spells/audits/CAUSAL-PERKS-BLIGHT-3.16.3.md) são **quatro identidades já presentes** no catálogo Iron's de 110. 39 âncoras de fonte verificadas em 11 arquivos upstream no commit `iron431/irons-spells-n-spellbooks@e4056af90302d37eb1739f5ff05020b020e6e252`.
- `docs/qa/irons_3163_heal_heartstop_blight_bytecode.py` examina classfiles do **JAR publicado** `irons_spellbooks-1.21.1-3.16.3.jar` sob SHA-256 `13d644474ddba4f8478b4ce68294687fd509c994b3f344a224142b102dbe6f73`, somente metadados. A [Actions Java 21 #38834814254](https://github.com/Gustavaopere/Black-Arcana/actions/runs/38834814254) terminou **SUCCESS**, conferiu o SHA-256 e inspecionou **9 classfiles** ([relatório binário](./irons-3163-healing-heartstop-blight-bytecode-evidence.md)); isso é prova estática, **não** execução real do provider.
- O relatório do JAR publicado **não** prova a equivalência com o arquivo **instalado**. Registrar SHA-256, tamanhos e mod IDs do pack carregado, versão NeoForge realmente usada, configurações, Java, addon order e condições do mundo. Não extrapolar a modlist documental para JAR físico sem prova.

## Ensaio de cura — evento proposto versus HP útil

| Cenário | Medição requerida | Aceitação ou recusa |
|---|---|---|
| Heal nível 1 e 8 | `SpellOnCastEvent`, `SpellHealEvent.getHealAmount`, `LivingHealEvent.getAmount`, HP antes/depois | Confirmar que evento é intenção anterior ao `heal`; atribuir cura útil somente ao delta positivo medido |
| Heal em vida cheia | Mesmo logging + mana/cooldown | Nunca premiar valor nominal de `SpellHealEvent` como HP útil recuperado |
| Greater Heal pós-LONG | Tempo de preparação, término/interrupção, evento, HP, packet FX | Distinguir início de canal, 1 cast consumado, 1 evento de intenção e cura efetiva |
| Greater Heal a 95% de vida | `getMaxHealth`, heal proposal, `LivingHealEvent`, HP final | Rejeitar caso o parser conte `getMaxHealth` como HP ganho, ou conte o packet como segunda cura |
| Ambas com Blight | Amplifier 0–7 do alvo, `LivingHealEvent` antes/depois de modificadores e HP final | Medir composição real de listeners: fórmula source é `1-0,1×level`, não resultado in-game garantido |
| Outros providers de cura | Poção/alimento/efeito de mod que usa `LivingEntity.heal` | Verificar se Blight afeta o `LivingHealEvent` geral sem atribuir casts do Iron's indevidamente |

**Risco de dupla contagem:** `SpellHealEvent`, `LivingHealEvent` e `HP delta` podem representar fases de **uma única recuperação**, não três magias. O evento fonte de cura não publica um UUID canônico de sessão; instrumentar correlação por cast server-owned real, sem inventá-lo no RPG Skill Tree.

## Ensaio Blight — quem está afetado

1. Aplicar Blight nível 1 e 8 num **alvo que será curado**; registrar antes/depois de `LivingHealEvent`, HP líquido e ordem de listeners. A fonte nominal produz 0,90× e 0,20× do valor que chega ao listener.
2. Aplicar Blight nível 1 e 8 **no atacante**; registrar `LivingIncomingDamageEvent` e `LivingDamageEvent.Post`. Fórmula nominal 0,95× e 0,60×; nunca confundir com dano recebido pelo alvo.
3. Usar `DamageSource` sem entidade causadora LivingEntity e ataque derivado de summon/projétil para distinguir `getEntity` do `getDirectEntity`; não inventar atribuição do caster.
4. Remover/reaplicar o efeito, testar logout, nível de amplificador, PvP/teams/claims e outros multiplicadores. Manter falha fechada quando ordem dos eventos/target não for determinada.

## Ensaio Heartstop — protocolo de risco alto

**Isolamento obrigatório:** executar só em cópia controlada de QA, sem inventário/personagens/regiões permanentes e com backups. O método de remoção do provider contém um ramo `kill()` para entidades `tickCount<=60` **sem condicional explícita de acumulador**, identificado por fonte. Não liberar perks de redução de duração, retirada do efeito ou cancelamento de Heartstop até terminar este ensaio.

| Condição | Procedimento seguro | Evidência exigida |
|---|---|---|
| Caster com `tickCount>60` | Cast Heartstop, tomar dano controlado conhecido, expirar naturalmente | Sequência `LivingDamageEvent.Pre` → `getOriginalDamage×0,5` → `setNewDamage(0)` → `onEffectRemoved` → `hurt(HEARTSTOP,accumulated)`, efeitos realmente aceitos e delta HP |
| Caster recém-spawnado, `tickCount<=60` | Teste descartável e sem ativos persistentes; observar remoção, incluindo zero golpes | Verificar se `kill()` de fato executa e se outro guard impede morte; **não inferir morte só da fonte** |
| Reaplicação e dispel | Adicionar/remover o mesmo efeito com lifecycle visível | Confirmar quantos callbacks terminais ocorrem; não dobrar dano terminal nem conceder Mastery por expiração/removal |
| Dano parcialmente cancelado | Registradores em `LivingDamageEvent.Pre`/`Post`, cancelamentos, buffs e shields | Distinguir dano original acumulado, novo dano zerado e efeito pós-processado |
| NBT/relog | Backup do mundo, desconectar/reconectar com efeito ativo, cruzar dimensões | Medir continuidade do `heartStopAccumulatedDamage` e callback único sem corrida |
| Morte e respawn | Conta de teste, snapshot de inventory e efeito | Excluir duplicação de expiração, reward XP e efeitos em entidades que não têm MagicData apropriado |

**Proibir como PASS:** classe encontrada no JAR, ausência de crash, log sintetizado, mana observada, screenshot isolado ou valor do evento sem delta HP e sem causa temporal. Cada item desses é evidência parcial, não aprovação de lifecycle.

## Entrega de evidência e gates

Anexar à PR #825 apenas relatórios redigidos, versões/SHAs e logs com identificação pessoal removida, resultados por cenário, timestamp/tick, screenshots quando necessário e versão exata de addons do pack. Nunca publicar JAR/bytecode terceirizado.

✅ Identidades e fonte fixadas; 🟡 dossiês em auditoria; ⚠️ binário específico/CI conforme run, servidor QA, casts reais, eventos e persistência pendentes; ⛔ setter de Blight/dano Heartstop, dupla mana, Mastery por evento derivado até existir contrato com authority/provider. **Stage 06.05 permanece 🟡; Stage 09 continua pendente**. O RPG Skill Tree não assume o pipeline mágico.
