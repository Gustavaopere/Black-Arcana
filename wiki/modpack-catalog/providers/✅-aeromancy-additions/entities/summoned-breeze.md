# Summoned Breeze

- Registro: `aero_additions:summoned_breeze`, `EntityType<SummonedBreeze>`, categoria `CREATURE`, tamanho **0.6×1.77**, tracking **64**.
- Ativação: entidade **REGISTERED**, atributos e renderer ativos; produtor `SummonBreezeSpell` **NOT_REGISTERED**. Nenhuma das dez magias ativas cria este summon. A lógica é alcançável se a entidade existir por mecanismo externo; não demonstra aquisição normal. Contribuição estrita de magias **0**.
- Estado: `documentary=SOURCE_PINNED`; `mutating_hook=NOT_VERIFIED`; `physical_qa=NOT_TESTED`; identidade instalada **NOT_VERIFIED**; certificação **0**.

Source `snackerpirater/aero-additions@ae282b32d25ad76ef8d01c637ec05566a767ae4c`, versão `1.2.8`. [Prova comum](../SOURCE-CONTRACTS-1.2.8.md) · [manifesto](../SOURCE-CATALOG-MANIFEST-1.2.8.json) · [limites](../SOURCE-CATALOG-CLOSURE-1.2.8.md). SHA-1 instalado histórico de 35 caracteres permanece inválido/desconhecido. A magia inativa é analisada em [código não registrado](../systems/unregistered-spell-code.md).

## Owner, AI e ciclo

`SummonedBreeze extends Breeze implements IMagicSummon,RangedAttackMob`. O construtor `EntityType` põe XP reward **0**; o construtor `(Level,LivingEntity)` chama diretamente `super` e atribui owner via `SummonManager.setOwner`, sem repetir esse assignment de XP. Não assumir que ambos construtores têm exatamente o mesmo valor herdado de XP. O cérebro é criado com listas vazias de sensores/memórias. `createAttributes` parte de `Breeze.createLivingAttributes()` e adiciona `STEP_HEIGHT=1`, `FOLLOW_RANGE=32`; registro em `AAServerEvents.onAttributeCreate` é ativo. Follow range não é alcance garantido de tiro.

`setTarget` só delega se target não nulo, há owner e target não é owner; inclusive `setTarget(null)` não delega. `getTarget` retorna o campo target. Goals ativos: Float prioridade 0; ShootWindCharge prioridade 1 (speed modifier **1**, intervalo **40**, raio parâmetro **10**); follow-owner prioridade 7 (`0.9,15,5,false,25`); random stroll 8 (`0.8`); olhar player 9 (3,1) e mob 10 (8). Target goals usam helpers Iron's de owner hurt-by, hurt-target, copy-owner-target, hurt-by-alert e protect-owner, prioridades 1–5. Suas políticas de amizade/seleção pertencem ao host.

O goal ShootWindCharge roda a cada tick com alvo vivo. Navega ao alvo até distância²<=100 e `seeTime>=20`; depois strafe com troca aleatória de sentido a cada 20 ticks. **O tiro é disparado quando `--attackTime<=0`, fora do gate de LOS/distância**, com reset em 40; `attackTime` começa em −1, então pode disparar no primeiro tick elegível. LOS/range influenciam navegação, não são gates locais de disparo. O goal registra `LOGGER.info("atk time {}",attackTime)` por tick. A classe `LongJump` definida no mesmo arquivo não é adicionada aos goals; seu único `canUse` consulta target a distância²<=9.

Cada `performRangedAttack` cria [Magic Wind Charge](magic-wind-charge.md) com owner **o próprio Breeze**, D=**1**, mirando os pés do alvo (`target.position−eyePosition` normalizado×0.5); `shoot` multiplica por 1.5, velocidade nominal **0.75**, e adiciona ao mundo. O parâmetro float de ranged attack não é usado. Não transfere diretamente owner do projétil para o summoner neste método.

`hurt` ignora dano quando `IMagicSummon.shouldIgnoreDamage` indicar; `isAlliedTo` combina superclass com `isAlliedHelper`; death/removal chamam helpers. `onUnSummon` no server emite 25 POOF e descarta. `causeFallDamage` sempre false. Não há save/read NBT próprios: owner, duração e lifecycle de summon são herdados/delegados. O limite **12000 ticks (10 minutos)** aparece somente na magia **inativa** que chamaria `initSummon` e criaria recast de 2; não é TTL intrínseco desta entidade.

`AAServerEvents.windShieldDeflection` tem ramo ativo que reverte projéteis que a atinjam e usa summoner como owner na deflexão; [Wind Shielded](../effects/wind-shield.md) detalha sua precedência. Renderer ativo é o `BreezeRenderer` vanilla.

## Matriz para perks

| Eixo | Consumidor real | Fronteira de mutação |
|---|---|---|
| Spawn/tempo/quantidade | Somente `SummonBreezeSpell` inativa produz summon no source | Não ofertar summon ativo por presença do registry. Hook por jogador **NOT_VERIFIED**. |
| Tiro/range | `ShootWindCharge.tick`, `performRangedAttack` | Intervalo 40 e raio de navegação 10 não são CDR/range de magia auditados; LOS não bloqueia tiro local. |
| Owner/crédito | `SummonManager`, `IMagicSummon`, owner do charge=Breeze | Atribuição downstream ao jogador e friendly fire precisam prova; spawn/AI não provam hit. |
| Proteção/lifecycle | Helpers de summon, deflexão, imunidade a queda | Policies de entidade não equivalem a WorldEffectPolicy/skill adapter. |
| Persistência | NBT/owner do host, sem schema local | Não alterar attachment de outro provider nem criar TTL a partir da magia inativa. |

QA: construtores/XP, owner ausente, limpar alvo, tiro através de barreiras, lifecycle/reload/unsummon, crédito do charge, deflexão e dano friendly fire. Nenhum adapter certificado.

## Localizadores fixos

- [AASpells.java — registro L95–99](https://github.com/snackerpirater/aero-additions/blob/ae282b32d25ad76ef8d01c637ec05566a767ae4c/src/main/java/com/snackpirate/aeromancy/spells/AASpells.java#L95-L99); [AASpells.java — spell comentado L74–78](https://github.com/snackerpirater/aero-additions/blob/ae282b32d25ad76ef8d01c637ec05566a767ae4c/src/main/java/com/snackpirate/aeromancy/spells/AASpells.java#L74-L78).
- [SummonedBreeze.java — construtores/AI L31–77](https://github.com/snackerpirater/aero-additions/blob/ae282b32d25ad76ef8d01c637ec05566a767ae4c/src/main/java/com/snackpirate/aeromancy/spells/summon_breeze/SummonedBreeze.java#L31-L77); [proteção/lifecycle/tiro L79–123](https://github.com/snackerpirater/aero-additions/blob/ae282b32d25ad76ef8d01c637ec05566a767ae4c/src/main/java/com/snackpirate/aeromancy/spells/summon_breeze/SummonedBreeze.java#L79-L123).
- [SummonedBreezeGoals.java — estado/condições L13–64](https://github.com/snackerpirater/aero-additions/blob/ae282b32d25ad76ef8d01c637ec05566a767ae4c/src/main/java/com/snackpirate/aeromancy/spells/summon_breeze/SummonedBreezeGoals.java#L13-L64); [tick e LongJump L66–145](https://github.com/snackerpirater/aero-additions/blob/ae282b32d25ad76ef8d01c637ec05566a767ae4c/src/main/java/com/snackpirate/aeromancy/spells/summon_breeze/SummonedBreezeGoals.java#L66-L145).
- [AAServerEvents.java — atributos L61–64](https://github.com/snackerpirater/aero-additions/blob/ae282b32d25ad76ef8d01c637ec05566a767ae4c/src/main/java/com/snackpirate/aeromancy/AAServerEvents.java#L61-L64); [deflexão L76–88](https://github.com/snackerpirater/aero-additions/blob/ae282b32d25ad76ef8d01c637ec05566a767ae4c/src/main/java/com/snackpirate/aeromancy/AAServerEvents.java#L76-L88); [AAClientEvents.java — renderer L45–52](https://github.com/snackerpirater/aero-additions/blob/ae282b32d25ad76ef8d01c637ec05566a767ae4c/src/main/java/com/snackpirate/aeromancy/AAClientEvents.java#L45-L52).
