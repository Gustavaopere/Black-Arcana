# Goety 3.1.4 — auditoria exata de ABI e referências simbólicas

**Data da evidência:** 26/10/2026
**Estado:** ⚠️ `EXACT_JAR_SHA_MATCHED / ABI_SYMBOLIC_CALLS_VERIFIED / EFFECT_SEMANTICS_NOT_VERIFIED / MUTATION_NOT_CERTIFIED`
**Stage:** auditoria documental/provider; **não** promove Stage 06.05 nem certificação de perks.

## Artefato, execução e isolamento

O alvo físico é `goety-3.1.4.jar`, mod ID `goety`, NeoForge/Minecraft 1.21.1, CurseForge project/file `586095/8689429`, SHA-1 **`a0770e180e4e8b1b87d8fa9c8356e9dbf34d82a7`**. O mesmo SHA consta da [auditoria de identidade](EXACT-3.1.4-ARTIFACT-AUDIT.md).

**Nova medição efetiva do JAR**, sem inferir equivalência de fonte:

- GitHub Actions: [execução #40344481668](https://github.com/Gustavaopere/Black-Arcana/actions/runs/40344481668); job `121647641120`, conclusão **`success`**.
- Branch deliberadamente **não destinada a merge:** `audit/goety-314-contract-surface-20261026`, HEAD `21688e6c9b6b1c1a2fc864ed0dec9f2044baaf86`. Workflow temporário `.github/workflows/goety-314-temporary-contract-audit.yml` executado apenas nessa branch; **não é runtime Black Arcana**.
- Evidência textual publicada: artifact `goety-314-contract-surface-evidence` ID `12659699310`, digest `sha256:e144832f9f9e279bbae2cab48094670f0d019738cf865167ab45dcc1e4706778` (retenção configurada de 30 dias). O [job](https://github.com/Gustavaopere/Black-Arcana/actions/runs/40344481668) contém as mesmas linhas de auditoria.
- Na execução, download CurseMaven, comparação `sha1sum -c`, busca de arquivos de classe no ZIP e `javap -p -s/-c` **limitado a coletar assinaturas e referências de chamadas**. O relatório **não publica nem transporta bytecode integral, corpos de métodos, constantes numéricas de balanceamento, assets ou reconstrução de código**.
- **18/18 classes solicitadas encontradas** nesse artefato. Este total é **somente o escopo de classes da auditoria**, não número de spells/skills nem contador de certificação.

## Superfícies realmente verificadas no JAR 3.1.4

A sintaxe `A.method → B.method` significa **referência simbólica da rotina A à rotina B no bytecode exato**. Não afirma que o caminho foi executado, qual ramo foi escolhido, quantas vezes ocorreu em uma conjuração ou que um listener pode modificar o resultado.

| Área | Fato de ABI/referência binária exata | O que continua desconhecido |
|---|---|---|
| **Classe do Focus** | `MagicFocus(ISpell)` e `MagicFocus.getSpell(): ISpell` existem. `MagicFocus.getSoulCost` referencia `ISpell.defaultSoulCost`. | Identidade por jogador, imutabilidade do objeto, permissões para substituir `ISpell`, custo liquidado. |
| **Eventos Goety** | `GoetyEventFactory` contém `onStartSpell(LivingEntity,ItemStack,ISpell)`, `onCastingSpell(LivingEntity,ItemStack,ISpell,int)`, `onCastSpell(LivingEntity,ISpell)`, `onStopSpell(LivingEntity,ItemStack,ISpell,int,int)` e `onSoulEnergyGain/Loss(Player,int)`. As classes `StartMagicEvent`, `CastingMagicEvent`, `CastMagicEvent`, `StopMagicEvent`, `ChangeSoulEnergyEvent` também existem. | Garantias de frequência, cancellability efetiva, thread, servidor/cliente, ordenação, eventos disparados só em cast válido e estabilidade como API pública. |
| **Entrada do ciclo de casting** | `DarkWand.onUseTick` referencia `GoetyEventFactory.onStartSpell` e `onCastingSpell`; `DarkWand.use` e `finishUsingItem` referenciam `onCastSpell`; `DarkWand.releaseUsing` referencia `onStopSpell`; `DarkWand.canCastTouch` referencia `onTouchBasedSpell`. | Se cada callback significa sucesso, se múltiplas invocações ocorrerão por cast, se cancelamentos revertem admissão/custo e como deduplicar Mastery. |
| **Custo Goety** | `DarkWand.MagicResults` referencia `ISpell.SpellResult`, `SEHelper.getSoulsAmount`, `SEHelper.decreaseSouls` e `SEHelper.addCooldown`; `DarkWand.SoulUse` referencia `SEHelper.soulDiscount`. `SEHelper.decreaseSouls` referencia `GoetyEventFactory.onSoulEnergyLoss`. | Fórmula/ordem de multiplicadores, valor efetivamente debitado, transação atômica, associação loss→cast, comportamento de totens/armaduras. |
| **ISpell básico** | Interfaces/métodos `ISpell.SoulCalculation`, `ISpell.spellCooldown(LivingEntity)`, `ISpell.startSpell`, `useSpell`, `stopSpell`, `SpellResult` estão presentes. | Se método é contrato suportado para intervenção em runtime, matching de spell ID e efeitos após listener. |
| **Banish** | `BanishSpell.touchResult(...,LivingEntity target,ItemStack,SpellStat)` presente; `conditionsMet` referencia `EventHooks.onEnderTeleport`; `touchResult` referencia `LivingEntity.randomTeleport`, `LivingEntity.stopRiding` e `SpellStat.getRange`. | **Não foi provado** que o alvo verificado em `conditionsMet` diverge do alvo tocado, nem a ordem dos checks, seleção de destino, cancelamento final ou segurança de claims. |
| **Blink** | `BlinkSpell.SpellResult` referencia `MobUtil.teleport`, `MobUtil.teleportTowards` e `SpellStat.getRange`; `BlinkSpell.enderTeleportEvent` referencia `EventHooks.onEnderTeleport` e `LivingEntity.teleportTo`. | Distância final, resolução segura do destino, retorno/cancelamento, efeitos de permissão e número de teleportes efetuados. |
| **Telekinesis** | `TelekinesisSpell` declara **`public Entity victim`**, `findVictim`, `startSpell`, `stopSpell` e `SpellResult`. `findVictim` referencia `MobUtil.getSingleTarget`, `Mob.getTarget` e `SpellStat.getRange`; `stopSpell` referencia `SEHelper.addCooldown`. | Se `victim` é compartilhado entre conjuradores na prática, execução de blacklist/HP, força por tick, colisões, cleanup e eventual correção no JAR exato. |
| **Shockwave** | `ShockwaveSpell.SpellResult` referencia `MobUtil.explosionDamage`, `SpellStat.getRadius` e `WandUtil.damageMultiply`; `defaultStats` referencia `SpellStat.setRadius`. | Fórmula numérica, caps de raio, confecção da AABB, alvo ou efeito extra após hooks externos. |
| **Weakening** | `WeakeningSpell.SpellResult` referencia `LivingEntity.addEffect` em **dois call-sites estáticos** e `SpellStat.getDuration/getRadius`. | Identidade/duração/amplifier efetivos dos dois efeitos, quantidade dinâmica de vítimas, imunidades/LOS/claims. |
| **Poison Dart** | `PoisonDartSpell.SpellResult` referencia `PoisonQuill.setOwner`, `setDuration` e `setExtraDamage`; `PoisonQuill.onHitEntity(EntityHitResult)` e `onHitBlock(BlockHitResult)` existem. | Dano/veneno efetivo, piercing, velocidade, descarte, efeitos de equipamento, alterações em listeners. |

**Observação de contagem:** “dois call-sites de `addEffect`” significa **dois locais de invocação estáticos encontrados**, não dois efeitos sempre aplicados nem dois hits por conjuração.

## Reconciliação com documentação anterior

As fichas `focuses/{blink,telekinesis,shockwave,banish,weakening,poison-dart}-focus.md` contêm análise semântica do source público **Goety 3.1.1** no commit `Vivideru/Goety-3@6c41a04f2d712097c4461f969a6bb8ee277149ef`. Esta nova prova **não transforma aquela implementação em fonte 3.1.4**. Deve-se ler as duas camadas separadamente:

1. **Exato 3.1.4 (AGORA verificado):** existência binária das classes, assinaturas selecionadas e referências simbólicas listadas na tabela; SHA-1 de identidade.
2. **Fonte 3.1.1 (referência adjacente):** fórmulas, defaults de configuração, brancheamento, geometria, durations, damage types, condições específicas; **não validados no JAR instalado** por esta auditoria.
3. **Runtime/CI do pack:** permaneceu **não ensaiado** para Goety nesta campanha. A conclusão `success` do workflow prova **apenas que o probe de ABI terminou com os asserts de SHA/class file aprovados**; não comprova execução em Minecraft/servidor.
4. **Hook seguro para perks:** **⛔ não homologado**, inclusive para os eventos cujos nomes/descritores foram confirmados. Existência ≠ contrato de mutação idempotente, ordem de settlement, compatibilidade com addons ou política de proteção.

## Próxima bateria de evidência necessária

- Contrato causal de exatamente uma conjuração por `DarkWand`: instantâneo, touch, contínuo, charging, cancelamento e falha sem gasto, em servidor real.
- `BanishSpell.conditionsMet` versus `touchResult`: comparar entidade e destino no **3.1.4**, incluir whitelist/blacklist, `EnderEntity`, claims e uma entidade protegida.
- Dois jogadores canalizando `TelekinesisSpell` com mesmo tipo de Focus, em paralelo; observar `victim`, troca de item, interrupção, logout e distância.
- `Shockwave`/`Weakening`: limites de radius, autorizações PVP, contagem de alvos e orçamento de scans/partículas com config real.
- `PoisonQuill`: modo perfurante, dano vanilla/mágico, dono, Wild Robe, persistência, chunk unload e efeitos.
- Custo Goety: equivalência de saldo verificado/debitado, ordenação de `ChangeSoulEnergyEvent.Loss`, equip discount, reset de cooldown e deduplicação de Mastery.

**Sem sete provas de certificação**, o manifesto `wiki/modpack-catalog/meta/PERK-READY-CERTIFICATIONS.json` e os índices automáticos continuam **intocados**: Goety **0/361 fichas certificadas**, global **109/2075** no último checkpoint confirmado. Estas seis fichas continuam ⚠️ condicionadas, embora tenham avançado de “apenas identidade + fonte 3.1.1” para “identidade + referência 3.1.1 + ABI/call-sites parciais do 3.1.4”.

**Clean-room:** nenhum bytecode ou implementação de terceiros é incorporado ao Black Arcana; relatório limitado a símbolos/descritores e relações necessárias à interoperabilidade. Goety conserva autoridade do próprio runtime, incluindo Soul Energy, casting e entidades.

## Continuidade — audit de chamadas internas e lifecycle por método (26/10/2026)

A [segunda auditoria do mesmo JAR 3.1.4 SHA-exato](EXACT-3.1.4-TARGET-SOUL-STRUCTURAL-AUDIT-20261026.md), workflow temporário run `40362689828`/artifact `12668033309`, ampliou os fatos **estruturais** de três pontos prioritários. Desta vez o parser resolveu referências a métodos da **própria classe**, não capturadas integralmente pela primeira filtragem.

- `BanishSpell.conditionsMet`: símbolos `entityResult` + `EventHooks.onEnderTeleport`; `touchResult`: `randomTeleport` e nenhuma **chamada direta** a `onEnderTeleport` no próprio método.
- `TelekinesisSpell.victim`: leituras/escritas binárias em `findVictim`, escrita em `startSpell/stopSpell` e leituras em `SpellResult`.
- `SEHelper.decreaseSouls`: referência interna a `soulDiscount` e externa a `onSoulEnergyLoss`; `DarkWand.SoulUse` referencia `soulDiscount` em pontos distintos. **Não certificar erro de débito nem isolamento entre casters apenas a partir dessas referências.**

Provenience, limitações, gates de teste e matriz de evidências: [relatório detalhado](EXACT-3.1.4-TARGET-SOUL-STRUCTURAL-AUDIT-20261026.md). Nenhum hook mutador, certificação de perk ou aprovação física decorre deste adendo.
