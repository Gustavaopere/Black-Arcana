# Astral Echo

**Dossiê documental — 23/10/2026.** `technical_perk_dossier: 1`; identidade `COUNTED_EXACT`; lógica `SOURCE_PINNED / SOURCE_CAUSALITY`; integração `CONTRATO_CONDICIONAL`; QA físico `PENDING`. **+0 identidades**: teleporte, sombra, retorno anti-magic e expiração pertencem à mesma raiz.

## Identidade e proveniência

Provider Asterism Arcanum (`mod_id=asterismarcanum`), spell **`asterismarcanum:astral_echo`**, escola default `asterismarcanum:astral`. Implementação `com.birdie.asterismarcanum.spells.AstralEchoSpell`; filho `entity.spells.starcutter.StarcutterEntity`, registro `asterismarcanum:starcutter_entity`. [Registry][registry], [spell][spell], [entidade][entity]. Não criar ID próprio para a tag `astral_echo_entity`.

JAR histórico #56 `asterismarcanum-1.21.1-0.1.0.jar`, SHA-1 `4a25ba80116168ddcc812f71467c0598127e774a`, [publisher 8157080](https://www.curseforge.com/minecraft/mc-mods/asterism-arcanum/files/8157080). [Prova binária de identidade](../EXACT-0.1.0-BINARY-REGISTRY-AUDIT.md), sem prova integral de corpos de métodos source↔JAR. Source oficial `BirdieVibes/Asterism-Arcanum@f1738c7813a85d31a6da10e6c9f2dbce18d2b583`, versão declarada 1.21.1-0.1.0/NeoForge 21.1.215/Iron’s 3.15.6; host consultado Iron’s 3.16.3 `e4056af90302d37eb1739f5ff05020b020e6e252`. Licença Polyform Shield: consulta/paráfrases/permalinks, sem importar implementação/assets. [Versões][versions], [contrato comum](../SPELL-PERK-BOUNDARIES-0.1.0.md).

A [descrição oficial][description], parafraseada, apresenta um teleporte que deixa uma marca breve; anti-magic sobre ela pode desfazer o deslocamento. Obtenção normal segue escola/config Iron’s e pool Astral do Astromancer, sem criar nova rota de aquisição ou garantir config implantada ([loot][loot]).

## Pipeline causal

1. **Admissão:** INSTANT, Rare, níveis default1..8; sem precondição/seleção local sobrescrita. Wrapper jogador Iron’s verifica gates/custo/cooldown e publica eventos antes do efeito. O source Asterism não cria reserva/refund próprios. [Defaults][spell], [host][host-cast].
2. **Dados/destino:** `onCast` faz cast direto de additionalCastData para `TeleportSpell.TeleportData`; null é aceito, tipo alheio pode falhar antes do spawn. Não sobrescreve `onServerPreCast` para produzir esse dado. Cria primeiro a sombra no ponto atual, tagueia e seta damage0, ignorando retorno de addFreshEntity. Usa destino do dado quando presente; caso contrário calcula destino no host. [Cast][cast].
3. **Seleção:** `TeleportSpell.findTeleportLocation` faz target-block ray pelo olhar até D e chama `solveTeleportDestination`. O solver usa bounding-box offset, ray de ledge até3 blocks, bloco acima/LOS e fallback de clip para baixo com altura da entidade. São testes geométricos, não comprovação de WorldEffectPolicy, claims, dimensão/chunk ou destino seguro em todo terreno. [Host solver][solver].
4. **Movimento:** desmonta se passenger, chama `Utils.handleSpellTeleport` e ignora seu retorno (true significa **cancelado**). O helper publica SpellTeleportEvent, permite cancelar/alterar coordenadas e só então teleportTo. Depois o spell sempre reseta fallDistance, produz FX/som no destino originalmente calculado, limpa cast data e chama super. Cancelamento não remove a sombra criada nem implica refund local; destino alterado pelo evento não é resolvido novamente pelo solver. [Cast][cast], [helper][teleport], [evento][teleport-event].
5. **Retorno/saída:** sombra não acompanha o caster. `StarcutterEntity#onAntiMagic` com tag e owner não-null chama **owner.setPos(anchor)** diretamente, sem o helper/evento de teleporte, dismount, reset de queda ou guarda server próprios, e seta tickCount30. Não troca dimensão por esse método. Próximo tick elegível pode executar a expiração. [Anti-magic][anti], [tick][tick].

## Parâmetros e matriz de alteração por perks

`n` é nível entregue ao consumidor; `E=POWER_MULTIPLIER×SPELL_POWER×AstralPower`, pelo host `getEntityPowerMultiplier`. `S(x)=x` se x≤1.5, senão `2−0.25/(x−1)`. Defaults/fórmulas abaixo não são valores implantados.

| Eixo | Valor / consumidor / fase | Mutabilidade e limite | QA |
|---|---|---|---|
| Alcance / power | **`D=9+3.5n×S(E)` blocks**; neutro E1:12.5..37 para n1..8. BaseSpellPower4 e por nível1 existem no constructor, mas **não** entram nessa fórmula. [Distância][distance], [E][power], [soft-cap][softcap]. | Atributos genérico/Astral e config power **NATIVE**, mudam E. Sem setter local de D; fórmula não tem floor/cap geométrico próprio. Valores negativos/extremos não são homologados. | Q1/Q2 |
| Targeting / proteção | Teleporte self orientado por target-block ray e solver, ou Vec3 já presente no cast data. Sem seleção de aliado/entidade ou AOE de transporte. [Solver][solver], [cast][cast]. | **⛔ SEM_HOOK_SEGURO** para single→grupo/filtro/proteção. Dado externo não é API de destino segura por si. | Q1/Q2 |
| Destino inicial | SpellTeleportEvent herda setTargetX/Y/Z e cancelamento; helper consome coords após evento. [Helper][teleport], [evento][teleport-event]; [prova de host](../SPELL-PERK-BOUNDARIES-0.1.0.md). | **HOOK_VERIFICADO** pré-teleport, integração **CONDITIONAL**: requer validar novas coords/claims/chunk/sync. Não altera automaticamente sombra, VFX, custo ou retorno anti-magic. | Q2/Q3 |
| Tempo / cooldown | INSTANT0; cooldown default12s=240ticks, antes de modifiers; sem recast próprio. Sombra duration privada30ticks, expira em tickCount>30 (31º tick nominal). WarmupFX em2. [Defaults][spell], [entidade][entity], [tick][tick]. | Config cooldown/evento host **NATIVE/HOOK_VERIFICADO** no caminho do host; duração privada/anti-magic **⛔ SEM_HOOK_SEGURO** para knob isolado. | Q3/Q4 |
| Mana / settlement | `(int)((15+5(n−1))×MANA_MULTIPLIER)`; neutro15..50. Evento host antes de débito e override; não cobra outra mana pela sombra/retorno. [Defaults][spell], [host][host-cast]. | Config global **NATIVE**; SpellOnCastEvent#setManaCost pré-débito **HOOK_VERIFICADO**, integração **CONDITIONAL**. Não é refund pós-cancelamento do teleporte. | Q1/Q3 |
| Entidade / hitbox / visual | 1 sombra solicitada na origem; registry nominal1×1, mas getDimensions usa **0.8r×0.8r**, r default1. Nenhum shoot/movimento próprio neste tick. Projétil balístico/speed/pierce: **N/A** para o deslocamento do caster. [Registry][entity-registry], [dimensions][dimensions]. | AABB efetiva depende de refreshDimensions/update: default r1 pode não disparar alteração do dado, portanto a fórmula não atesta AABB final0.8. Escala/raio não são alcance do teleporte. setRadius server limita apenas máximo1; não chamado por Echo. **⛔ SEM_HOOK_SEGURO** para resize seguro por perk. | Q2/Q4 |
| Expiração / dano / área | Shadow recebe damage0, mas herda terminal Starcutter: área até10r, AABB + teste distância²/LOS e falloff; usa DamageSources.applyDamage com **SpellID STARCUTTER**, não Echo. [Cast][cast], [terminal][terminal]. | Zero inicial não significa “só VFX”: eventos/listeners podem observar/alterar tentativa0. Não criar segundo dano ou XP por esse child. Tipo/área isolados **⛔ SEM_HOOK_SEGURO**; conferir [Starcutter](starcutter.md). | Q3/Q4 |
| Retorno anti-magic | Se tag/owner: owner.setPos(position); tickCount=30. Não há gate local de dimensão, vida, proteção ou destino válido. [Anti][anti]. | Fluxo diferente do SpellTeleportEvent inicial; **⛔ SEM_HOOK_SEGURO** para prometer veto/retarget genérico no retorno. Nenhum anchor BA paralelo. | Q2/Q3 |
| Persistência / ownership | Owner vem de Projectile; override NBT salva Radius/Age/Duration e não salva damage0; novo objeto tem damage default1. [NBT][nbt], [fields][entity]. | Dano0 persistente não demonstrado; reload/owner/tag e efeitos de listeners **CONDITIONAL**. Sem token de cast próprio por sombra. | Q4/Q5 |
| Cura / summons / mundo | Sem cura, summon com AI, blocos, ticket ou rollback próprio. Sombra é efeito filho, não segunda magia. [Cast][cast]. | **N/A** para cura/summon e recursos extras. Black Arcana não substitui o lifecycle do provider. | Q5 |

## Autoria, deduplicação e QA

Iron’s/Asterism possuem mana/cooldown, movimento e sombra; RPG mantém somente progressão/perks contratadas. Um SpellOnCastEvent pré-efeito não prova deslocamento, chegada, retorno ou dano terminal. Dedup deve correlacionar cast, caster, UUID da sombra, fase e alvo; tag e owner não bastam para distinguir todas as ações Starcutter/Echo. A assinatura existente é mobilidade self com âncora breve reversível por anti-magic; nova magia precisa regra causal própria, sem copiar implementação/assets.

- **Q1:** JAR/config/atributos efetivos, níveis/powers extremos e gates reais de ingresso; sobrevivência/receitas.
- **Q2:** obstáculos/ledge/void/claims/chunks, destino alterado pelo evento, mounts, outras dimensões e owner já deslocado antes de anti-magic.
- **Q3:** veto do teleporte, repetição de anti-magic, ordem dos listeners, mana/cooldown/queda/sombra residual; damage0 e parentSpellID.
- **Q4:** unload/reload/restart, Age/Duration/radius/load de damage e tag/owner, expiração natural/forçada, cliente/multiplayer.
- **Q5:** casts simultâneos, logout/morte, estado por caster e coexistência RPG/Enshrouded. Tudo físico permanece **PENDING**, sem novo adapter/perk/runtime nem promoção de Stage.

[registry]: https://github.com/BirdieVibes/Asterism-Arcanum/blob/f1738c7813a85d31a6da10e6c9f2dbce18d2b583/src/main/java/com/birdie/asterismarcanum/registries/ASARSpellRegistry.java#L53-L56
[spell]: https://github.com/BirdieVibes/Asterism-Arcanum/blob/f1738c7813a85d31a6da10e6c9f2dbce18d2b583/src/main/java/com/birdie/asterismarcanum/spells/AstralEchoSpell.java#L30-L58
[cast]: https://github.com/BirdieVibes/Asterism-Arcanum/blob/f1738c7813a85d31a6da10e6c9f2dbce18d2b583/src/main/java/com/birdie/asterismarcanum/spells/AstralEchoSpell.java#L81-L110
[distance]: https://github.com/BirdieVibes/Asterism-Arcanum/blob/f1738c7813a85d31a6da10e6c9f2dbce18d2b583/src/main/java/com/birdie/asterismarcanum/spells/AstralEchoSpell.java#L112-L118
[entity]: https://github.com/BirdieVibes/Asterism-Arcanum/blob/f1738c7813a85d31a6da10e6c9f2dbce18d2b583/src/main/java/com/birdie/asterismarcanum/entity/spells/starcutter/StarcutterEntity.java#L26-L43
[anti]: https://github.com/BirdieVibes/Asterism-Arcanum/blob/f1738c7813a85d31a6da10e6c9f2dbce18d2b583/src/main/java/com/birdie/asterismarcanum/entity/spells/starcutter/StarcutterEntity.java#L45-L51
[tick]: https://github.com/BirdieVibes/Asterism-Arcanum/blob/f1738c7813a85d31a6da10e6c9f2dbce18d2b583/src/main/java/com/birdie/asterismarcanum/entity/spells/starcutter/StarcutterEntity.java#L65-L129
[terminal]: https://github.com/BirdieVibes/Asterism-Arcanum/blob/f1738c7813a85d31a6da10e6c9f2dbce18d2b583/src/main/java/com/birdie/asterismarcanum/entity/spells/starcutter/StarcutterEntity.java#L108-L128
[dimensions]: https://github.com/BirdieVibes/Asterism-Arcanum/blob/f1738c7813a85d31a6da10e6c9f2dbce18d2b583/src/main/java/com/birdie/asterismarcanum/entity/spells/starcutter/StarcutterEntity.java#L133-L163
[nbt]: https://github.com/BirdieVibes/Asterism-Arcanum/blob/f1738c7813a85d31a6da10e6c9f2dbce18d2b583/src/main/java/com/birdie/asterismarcanum/entity/spells/starcutter/StarcutterEntity.java#L165-L181
[entity-registry]: https://github.com/BirdieVibes/Asterism-Arcanum/blob/f1738c7813a85d31a6da10e6c9f2dbce18d2b583/src/main/java/com/birdie/asterismarcanum/registries/ASAREntityRegistry.java#L103-L108
[versions]: https://github.com/BirdieVibes/Asterism-Arcanum/blob/f1738c7813a85d31a6da10e6c9f2dbce18d2b583/gradle.properties#L9-L24
[description]: https://github.com/BirdieVibes/Asterism-Arcanum/blob/f1738c7813a85d31a6da10e6c9f2dbce18d2b583/src/main/resources/assets/asterismarcanum/lang/en_us.json#L48-L49
[loot]: https://github.com/BirdieVibes/Asterism-Arcanum/blob/f1738c7813a85d31a6da10e6c9f2dbce18d2b583/src/main/resources/data/asterismarcanum/loot_table/entities/astromancer.json#L1
[host-cast]: https://github.com/iron431/irons-spells-n-spellbooks/blob/e4056af90302d37eb1739f5ff05020b020e6e252/src/main/java/io/redspace/ironsspellbooks/api/spells/AbstractSpell.java#L160-L325
[solver]: https://github.com/iron431/irons-spells-n-spellbooks/blob/e4056af90302d37eb1739f5ff05020b020e6e252/src/main/java/io/redspace/ironsspellbooks/spells/ender/TeleportSpell.java#L109-L133
[teleport]: https://github.com/iron431/irons-spells-n-spellbooks/blob/e4056af90302d37eb1739f5ff05020b020e6e252/src/main/java/io/redspace/ironsspellbooks/api/util/Utils.java#L167-L175
[softcap]: https://github.com/iron431/irons-spells-n-spellbooks/blob/e4056af90302d37eb1739f5ff05020b020e6e252/src/main/java/io/redspace/ironsspellbooks/api/util/Utils.java#L177-L184
[power]: https://github.com/iron431/irons-spells-n-spellbooks/blob/e4056af90302d37eb1739f5ff05020b020e6e252/src/main/java/io/redspace/ironsspellbooks/api/spells/AbstractSpell.java#L234-L242
[teleport-event]: https://github.com/iron431/irons-spells-n-spellbooks/blob/e4056af90302d37eb1739f5ff05020b020e6e252/src/main/java/io/redspace/ironsspellbooks/api/events/SpellTeleportEvent.java#L7-L18
