# Boogie Woogie

**Dossiê documental — 24/10/2026.** `technical_perk_dossier: 1`; identidade `COUNTED_EXACT`; lógica `SOURCE_PINNED / SOURCE_CAUSALITY`; integração `CONTRATO_CONDICIONAL`; QA físico `PENDING`. **+0 identidades/+0 strict**: troca, Confusion e recasts pertencem à spell existente.

## Identidade e proveniência

Provider **Discerning The Eldritch**, `mod_id=discerning_the_eldritch`; spell **`discerning_the_eldritch:boogie_woogie`**, escola default `irons_spellbooks:evocation`. Classe `net.acetheeldritchking.discerning_the_eldritch.spells.evocation.BoogieWoogieSpell`; registro `SpellRegistries#registerSpell(new BoogieWoogieSpell())`. [Registro][registry], [defaults][defaults].

Pack MC 1.21.1/NeoForge, JAR histórico **`discerning_the_eldritch-1.4.4-1.21.jar`**, SHA-1 `cf35c225aced23b705d1e0fd1bc5c62d96540e0c`, publisher [CF8816497](https://www.curseforge.com/minecraft/mc-mods/discerning-the-eldritch/files/8816497), 22098930 bytes; [prova binária estática](../EXACT-BINARY-SPELLS-1.4.4-1.21.md). Source oficial `AceTheEldritchKing/Discerning_The_Eldritch@7bbd81f902c65a4452f47656ebd948cae8cd5833`, versão declarada 1.4.4-1.21, build Iron's 3.16.2/NeoForge 21.1.244/Azure 3.1.0/Ace's 1.2.7.2; pack Iron's 3.16.3/NeoForge 21.1.250/Azure 3.1.11/Ace's 1.2.7.2. Host source Iron's 3.16.3 `e4056af90302d37eb1739f5ff05020b020e6e252`; identidade/versão não equiparam todos os métodos/JARs. `mod_license=MIT` versus TEMPLATE_LICENSE PolyForm Shield é conflito de sinais: fatos/paráfrases/permalinks, sem copiar implementação/assets. [Versões][versions], [contratos comuns](../SPELL-PERK-BOUNDARIES-1.4.4-1.21.md).

O [guia oficial][guide] só exclama o nome; o [comentário do registro][registry], parafraseado, descreve trocar de posição com um alvo. O executor abaixo fecha a mecânica. Sem override local de crafting/loot/learning: seguem gates host/config; scroll/rota Survival **NÃO VERIFICADOS**. [Elegibilidade host][host-acquisition]. Echo Vibration Ring aumenta casts, não concede a spell: a [receita source][ring-recipe] combina Echo Shard e Silver Ring; obtenção efetiva dos ingredientes requer QA.

## Pipeline causal e parâmetros

1. **Admissão server:** `#checkPreCastConditions` chama `Utils.preCastTargetHelper(range=15+L, aimAssist=0.15)`. No host, ray do olho/look termina no primeiro bloco COLLIDER/sem fluidos, usa filtro pickable/alive/não spectator e escolhe primeiro hit por distância. Helper resolve Living, passenger de PreventDismount ou parent Living de PartEntity, e guarda UUID em TargetEntityCastData. Sem filtro DTE adicional de time/aliado/PvP/claims. [Pre-cast][precast], [helper][target-helper], [ray][ray], [filtro][filter].
2. **Custo/evento:** admissão antecede início; wrapper publica SpellOnCastEvent e debita mana antes de onCast. Alterar nível nesse evento não refaz o range já adquirido nem recalcula mana automaticamente. Anúncio não confirma chegada. [Host][host-cast], [evento][cast-event].
3. **Recast:** sem recast ativo, onCast tenta inserir `RecastInstance(id,L,total,80ticks,castSource,null)` **antes de conferir target**. Total1 normal ou1+L com ring. Host guarda remaining=total−1; total1 não fica ativo, embora haja tentativa de inserção. Wrapper não cobra mana novamente em recast já ativo nesse caminho; após onCast decrementa e renova janela80 quando restam casts. Término/timeout e cooldown são host-owned. Não é “L recasts além do inicial” para todos equipamentos. [Spell][swap], [count][count], [instância][recast-instance], [manager][recasts].
4. **Troca:** só com TargetEntityCastData e UUID resolvido no ServerLevel atual captura posições de pés, chama **caster.teleportTo(targetPos)** e depois **target.teleportTo(casterPos)**. Depois tenta Confusion60ticks, amp0, ambient/particles/icon=true no target; retorno ignorado. Não revalida range/LOS/equipe ali. Dados ausentes/target nulo ainda chamam super.onCast; sem refund próprio. [Swap][swap], [UUID][target-data].
5. **Consequências:** são dois teleportTo diretos, sem `Utils.handleSpellTeleport`/SpellTeleportEvent ou resolver local de destino livre. Não há transação/rollback, claims, preservação de passageiros/velocidade ou passagem entre dimensões demonstrados. Patches/eventos Minecraft/NeoForge downstream continuam possíveis; ausência do helper não prova ausência de todos eventos. Confusion não depende de comprovar as duas chegadas aceitas. Clap/som são apresentação. [Swap][swap], [apresentação][presentation].

| L default | Mana neutra | Range adquirido (blocks) | Total normal / com ring | Recasts extras com ring |
|---|---|---|---|---|
| 1 | 20 | 16 | 1 / 2 | 1 |
| 2 | 25 | 17 | 1 / 3 | 2 |
| 3 | 30 | 18 | 1 / 4 | 3 |
| 4 | 35 | 19 | 1 / 5 | 4 |
| 5 | 40 | 20 | 1 / 6 | 5 |

Mana real `int((20+5(L−1))×MANA_MULTIPLIER)`; Rare, max default5, INSTANT0ticks, cooldown default10s=200ticks antes de modifiers. Base/per-level power1/1 declara `P=L×SPELL_POWER×EVOCATION_SPELL_POWER×POWER_MULTIPLIER`, mas **nenhum consumer desta troca lê P**: power não aumenta range, recasts ou Confusion. Defaults não são config implantada. [Defaults][defaults], [fórmulas][formulas].

## Matriz para perks

| Eixo | Valor / consumidor / fase | Boundary real / limite | QA |
|---|---|---|---|
| Dano / tipo / cura | Sem hurt/heal/DOT/SpellDamageSource no onCast; escola Evocation não prova dano. [Swap][swap]. | Dano/type/crit **N/A**; dano paralelo não modifica este consumer. | Q1/Q3 |
| Alcance / targeting |15+L blocks, inflação0.15, um Living/UUID adquirido antes do evento de cast. [Pre-cast][precast], [helper][target-helper]. | Sem setter de range/target. Evento de nível **HOOK_VERIFICADO** genérico, mas seleção já ocorreu; adapter **CONTRATO_CONDICIONAL**. Retarget/multi-target **⛔ SEM_HOOK_SEGURO**. | Q2/Q3 |
| Área / movimento | Duas posições capturadas, sem raio/área de aterrissagem/validação de corpo livre local. [Swap][swap]. | Sem seam transacional ou rollback verificado. SpellTeleportEvent do helper Iron's não é consumido neste caminho; destino/área por perk **⛔ SEM_HOOK_SEGURO**. | Q2/Q3 |
| Projétil / summon | Ray é aquisição; nenhuma entidade lançada/invocada. [Pre-cast][precast], [swap][swap]. | Hitbox/speed/pierce/lifetime/AI/summon cap **N/A**. | Q2 |
| Cast / cooldown | INSTANT0; cooldown default10s. [Defaults][defaults], [host][formulas]. | Cooldown **CONFIG_NATIVE**/atributo nativo e evento pré-inserção no contrato comum; não são knobs da janela80 ou status60. Integração **CONTRATO_CONDICIONAL**. | Q1/Q4 |
| Mana / recasts | Fórmula acima; total1 ou1+L, janela80, dados null; wrapper paga inicialmente conforme origem/creative. [Count][count], [swap][swap], [host][host-cast]. | `SpellOnCastEvent#setManaCost/setSpellLevel` **HOOK_VERIFICADO** pré-onCast; não recalcula target/custo em cadeia. Ring é equipamento nativo, não API de perk; count/janela independentes **⛔ SEM_HOOK_SEGURO**. | Q1/Q4 |
| Status / duração | Confusion60ticks=3s, amp0 no target após os dois teleportTo; retorno ignorado. [Swap][swap]. | Literal, sem scaling P/setter local; veto/merge/resist do effect pertencem ao host. Duração/amplificador por perk **⛔ SEM_HOOK_SEGURO**. | Q3/Q4 |
| Persistência / mundo / cleanup | TargetEntityCastData tem UUID/reset vazio; recast salva instâncias ativas, mas castData do recast é null. Sem bloco/fuel/HP/stamina. [Target][target-data], [recasts][recasts]. | Sem token local de troca ou compensação parcial. Save/load de recast não prova target preservado no próximo ingresso. Dedup/sync/passenger/claims **PENDING**; sem ledger paralelo. | Q3/Q4 |

## Ownership, dedup e verificação

DTE/Iron's/Minecraft possuem alvo, mana, recast, movimento e status. RPG Skill Tree não credita dois teleportTo como dois casts; BA não repete swap/rollback por heurística. Enshrouded mantém Shroud/exposure: posição/escola não concede bridge. Assinatura ocupada: transposição caster↔alvo com Confusion e recasts por equipamento; magia original precisaria contrato próprio de chegada/rollback.

- **Q1:** config física/learning/scroll Survival, CastSource/creative, mana inicial, cooldown normal/timeout, níveis fora default, sem segunda cobrança/XP.
- **Q2:** primeiro bloco, inflação0.15, partes/passenger/morto/spectator/aliado/PvP/claims, UUID removido, range/LOS alterados depois do pre-cast.
- **Q3:** falha/veto de cada teleportTo, colisão/chunks/dimensão, passageiros/velocidade/queda/morte entre chamadas, Confusion bloqueada/mesclada e dedup.
- **Q4:** ring equip/desequip entre casts, total1/2..6, janela80 renovada, timeout/logout/restart/sync e target do recast. **Todos PENDING**, sem adapter/runtime novo.

[registry]: https://github.com/AceTheEldritchKing/Discerning_The_Eldritch/blob/7bbd81f902c65a4452f47656ebd948cae8cd5833/src/main/java/net/acetheeldritchking/discerning_the_eldritch/registries/SpellRegistries.java#L121-L125
[defaults]: https://github.com/AceTheEldritchKing/Discerning_The_Eldritch/blob/7bbd81f902c65a4452f47656ebd948cae8cd5833/src/main/java/net/acetheeldritchking/discerning_the_eldritch/spells/evocation/BoogieWoogieSpell.java#L27-L59
[versions]: https://github.com/AceTheEldritchKing/Discerning_The_Eldritch/blob/7bbd81f902c65a4452f47656ebd948cae8cd5833/gradle.properties#L11-L30
[guide]: https://github.com/AceTheEldritchKing/Discerning_The_Eldritch/blob/7bbd81f902c65a4452f47656ebd948cae8cd5833/src/main/resources/assets/discerning_the_eldritch/lang/en_us.json#L158-L162
[ring-recipe]: https://github.com/AceTheEldritchKing/Discerning_The_Eldritch/blob/7bbd81f902c65a4452f47656ebd948cae8cd5833/src/main/resources/data/discerning_the_eldritch/recipe/echo_vibration_ring.json#L1-L16
[precast]: https://github.com/AceTheEldritchKing/Discerning_The_Eldritch/blob/7bbd81f902c65a4452f47656ebd948cae8cd5833/src/main/java/net/acetheeldritchking/discerning_the_eldritch/spells/evocation/BoogieWoogieSpell.java#L71-L74
[count]: https://github.com/AceTheEldritchKing/Discerning_The_Eldritch/blob/7bbd81f902c65a4452f47656ebd948cae8cd5833/src/main/java/net/acetheeldritchking/discerning_the_eldritch/spells/evocation/BoogieWoogieSpell.java#L76-L85
[swap]: https://github.com/AceTheEldritchKing/Discerning_The_Eldritch/blob/7bbd81f902c65a4452f47656ebd948cae8cd5833/src/main/java/net/acetheeldritchking/discerning_the_eldritch/spells/evocation/BoogieWoogieSpell.java#L87-L110
[presentation]: https://github.com/AceTheEldritchKing/Discerning_The_Eldritch/blob/7bbd81f902c65a4452f47656ebd948cae8cd5833/src/main/java/net/acetheeldritchking/discerning_the_eldritch/spells/evocation/BoogieWoogieSpell.java#L61-L69
[formulas]: https://github.com/iron431/irons-spells-n-spellbooks/blob/e4056af90302d37eb1739f5ff05020b020e6e252/src/main/java/io/redspace/ironsspellbooks/api/spells/AbstractSpell.java#L160-L257
[host-cast]: https://github.com/iron431/irons-spells-n-spellbooks/blob/e4056af90302d37eb1739f5ff05020b020e6e252/src/main/java/io/redspace/ironsspellbooks/api/spells/AbstractSpell.java#L263-L346
[cast-event]: https://github.com/iron431/irons-spells-n-spellbooks/blob/e4056af90302d37eb1739f5ff05020b020e6e252/src/main/java/io/redspace/ironsspellbooks/api/events/SpellOnCastEvent.java#L20-L69
[target-helper]: https://github.com/iron431/irons-spells-n-spellbooks/blob/e4056af90302d37eb1739f5ff05020b020e6e252/src/main/java/io/redspace/ironsspellbooks/api/util/Utils.java#L665-L710
[ray]: https://github.com/iron431/irons-spells-n-spellbooks/blob/e4056af90302d37eb1739f5ff05020b020e6e252/src/main/java/io/redspace/ironsspellbooks/api/util/RaycastBuilder.java#L20-L124
[filter]: https://github.com/iron431/irons-spells-n-spellbooks/blob/e4056af90302d37eb1739f5ff05020b020e6e252/src/main/java/io/redspace/ironsspellbooks/api/util/Utils.java#L459-L461
[target-data]: https://github.com/iron431/irons-spells-n-spellbooks/blob/e4056af90302d37eb1739f5ff05020b020e6e252/src/main/java/io/redspace/ironsspellbooks/capabilities/magic/TargetEntityCastData.java#L12-L39
[recast-instance]: https://github.com/iron431/irons-spells-n-spellbooks/blob/e4056af90302d37eb1739f5ff05020b020e6e252/src/main/java/io/redspace/ironsspellbooks/capabilities/magic/RecastInstance.java#L27-L35
[recasts]: https://github.com/iron431/irons-spells-n-spellbooks/blob/e4056af90302d37eb1739f5ff05020b020e6e252/src/main/java/io/redspace/ironsspellbooks/capabilities/magic/PlayerRecasts.java#L46-L212

[host-acquisition]: https://github.com/iron431/irons-spells-n-spellbooks/blob/e4056af90302d37eb1739f5ff05020b020e6e252/src/main/java/io/redspace/ironsspellbooks/api/spells/AbstractSpell.java#L594-L630
