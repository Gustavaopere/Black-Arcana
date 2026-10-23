# Celestial Tether

**Dossiê documental — 23/10/2026.** `technical_perk_dossier: 1`; identidade `COUNTED_EXACT`; lógica `SOURCE_PINNED / SOURCE_CAUSALITY`; integração `CONTRATO_CONDICIONAL`; QA físico `PENDING`. **+0 identidades**: montaria, cancelamentos, contador e shatter são fases da mesma spell.

## Identidade e proveniência

Provider Asterism Arcanum (`mod_id=asterismarcanum`), spell **`asterismarcanum:celestial_tether`**, escola default Astral. Classe `com.birdie.asterismarcanum.spells.CelestialTetherSpell`; efeito filho `entity.spells.celestial_tether.CelestialTetherEntity`, registro **`asterismarcanum:celestial_tether_entity`**. [Registro][registry], [spell][spell], [entidade][entity], [EntityType][entity-registry].

JAR físico histórico #56 **`asterismarcanum-1.21.1-0.1.0.jar`**, SHA-1 `4a25ba80116168ddcc812f71467c0598127e774a`; [publisher8157080](https://www.curseforge.com/minecraft/mc-mods/asterism-arcanum/files/8157080) e [prova de registry/classe](../EXACT-0.1.0-BINARY-REGISTRY-AUDIT.md). Source oficial `BirdieVibes/Asterism-Arcanum@f1738c7813a85d31a6da10e6c9f2dbce18d2b583`, versão1.21.1-0.1.0, NeoForge21.1.215/Iron’s3.15.6; host consultado Iron’s3.16.3 `e4056af90302d37eb1739f5ff05020b020e6e252`. [Versões][versions]. Identidade exata não comprova todos os corpos de métodos source↔JAR/config efetiva. Polyform Shield: consulta/paráfrases/permalinks, sem importar implementação/assets. [Contratos comuns](../SPELL-PERK-BOUNDARIES-0.1.0.md).

A [descrição oficial][description], parafraseada, apresenta suspensão do caster e negação de ataques por tempo/contador. Obtenção segue escola Astral/pool do Astromancer e configuração Iron’s, sem criar receita ou garantir estado implantado. [Loot][loot].

## Pipeline causal

1. **Admissão/settlement:** INSTANT, Uncommon, níveis default1..8, sem seleção raycast ou precondição específica sobrescrita. Wrapper jogador Iron’s verifica seus gates e publica eventos/cobra mana antes do efeito. Não existe restituição local de HP/custo por “hits absorvidos”. [Defaults][spell], [host][host-cast].
2. **Spawn/montaria:** onCast cria uma entidade com owner=caster, posiciona no caster, guarda contador `n+1` e lifetime `int(getDuration)`, solicita addFreshEntity e `entity.startRiding(tether,true)`. Ambos retornos são ignorados; falha de spawn/mount não tem rollback local demonstrado. A entidade não é guardada em EntityCastData, portanto não confundir sua duração com o reset do cast instantâneo. [Cast][cast].
3. **Incoming damage:** o handler aceita a vítima cujo **vehicle é CelestialTetherEntity**, exige `source.getEntity()!=null` e **não friendly-fire** segundo `DamageSources.isFriendlyFireBetween`; cancela o evento e decrementa o contador da montaria. Não testa owner==vítima, amount>0, tipo específico, LOS ou hitbox da spell. Dano ambiental/ownerless fora dessa condição não recebe a mesma proteção. [Handler][handler], [friendly-fire][friendly].
4. **Tick/saída:** entidade testa `lifetime>=0 && tickCount>lifetime` e contador `<0`, chamando destroyTether. Contador zero ainda pode cancelar próximo evento; remoção só é decidida no tick. Anti-magic, kill e removePassenger também chamam destroyTether. Destruição server ejecta passageiros, produz som e discard; chamadas não provam cleanup único/reentrância segura em todos os contextos. [Tick][tick], [cleanup][cleanup], [anti-magic][anti].

## Matriz de parâmetros e alteração por perks

`n`=nível recebido; `P=getSpellPower(n,caster)` pelo host. Defaults/fórmulas são source, não configuração implantada.

| Eixo | Valor / consumidor / fase | Boundary e mutabilidade | QA |
|---|---|---|---|
| Cast / cooldown / custos | INSTANT0; cooldown30s=600ticks; mana `int((30+15(n−1))×MANA_MULTIPLIER)`, neutro30..135. Sem recast próprio. [Spell][spell], [host][host-cast]. | Config/eventos host pré-débito/inserção **NATIVE/HOOK_VERIFICADO** genéricos, integração **CONDITIONAL**; não criar reserva/segunda mana por absorção. | Q1/Q2 |
| Duração / power | `getDuration=(80+10P)×4=320+40P ticks`, truncada int ao gravar lifetime. P neutro5..12 →520..800ticks=26..40s. Expiração strict `tickCount>lifetime`; nominal primeiro tick após o limite. [Duração][duration], [tick][tick]. | Poder genérico/Astral/config **NATIVE**, afeta duração. `setLifetime(int)` público sem validação/sync próprio é superfície **CONDITIONAL**, não contrato per-player pronto. | Q1/Q3 |
| Hits / tooltip | Inicial `n+1` em campo float; setter recebe int; cada evento qualificado subtrai1. Tooltip mostra `int(P)+1`, não o mesmo cálculo. Sequência nominal com tick entre eventos sugere `n+2` cancelamentos, **não cap rígido**: mais eventos podem ser cancelados antes do tick que vê `<0`. [Info/defaults][spell], [cast][cast], [decremento][counter], [handler][handler]. | `setAbsorbedHitsRemaining(int)` público não cria API de charge/cancelamento atômico; **CONDITIONAL**. Alterar P não altera contador inicial, enquanto alterar n pode mudar ambos. Sem segunda pool BA. | Q2/Q3 |
| Target / alcance / área | Caster solicita montagem self na origem. Proteção depende da vítima estar nessa montaria, não de um raio esférico/AOE. Não há seleção de terceiros ou filtro de claims local. [Cast][cast], [handler][handler]. | Sem seam seguro de self→grupo/retarget. **⛔ SEM_HOOK_SEGURO** para resolver diferente; custos/segurança continuam do host/provider. | Q2/Q4 |
| Dano / tipo / crítico | Não cria DamageSource, dano, cura ou absorção numérica de HP. Handler cancela **LivingIncomingDamageEvent**, exigindo causingEntity e friendly-fire policy. [Handler][handler]. | Cancelamento é API real usada pelo provider, mas observar o evento não identifica token de cast nem libera duplicar shield. Conversão de DamageType/cura **N/A**. | Q2/Q4 |
| Entidade / hitbox / visual | Registry1×1, tracking64. Com primeiro passenger LivingEntity: `hScale=width+0.4`, `vScale=(height+0.2+hScale)/2`; dimensões base são escaladas por esses valores. Sem passenger usa1/1. Não é área de proteção. [EntityType][entity-registry], [dimensions][dimensions]. | refresh ao adicionar passenger; sync/pose/culling são host-dependent. Resize **⛔ SEM_HOOK_SEGURO** sem contrato. Projétil, speed, pierce, spread: **N/A**. | Q3/Q4 |
| Movimento / estados | positionRider fixa passenger em XYZ da entidade; getPassengerRidingPosition retorna posição; não empurrada por fluid, não desmonta underwater, não senta. Entidade é pickable/collidable e push é vazio. [Rider][rider], [dimensions/collision][dimensions]. | Suspensão via montaria, não speed attribute, anti-gravity permanente ou teleporte. Sem setter per-player seguro de offset/destino. | Q3/Q4 |
| Lifecycle / ownership | Owner UUID+cachedEntity; getOwner pode resolver UUID no ServerLevel corrente. Tick não consulta owner.isAlive diretamente. NBT salva Owner, age, lifetime, absorbed_hits_remaining; defineSynchedData vazio. [Owner][owner], [NBT][nbt]. | Persistência declarada não comprova retorno/montaria/client sync após reload. **CONTRATO_CONDICIONAL**; não criar owner registry ou timer paralelo. | Q3/Q5 |
| Summon / mundo / cleanup | Uma entidade de efeito, sem AI/summon combatente, bloco/ticket/rollback. removePassenger e anti-magic destroem provider-native; lifetime negativo desliga apenas esse teste de expiração. [Cleanup][cleanup], [anti][anti]. | N/A summoncount/AI/heal. Não aprovar setter de lifetime negativo para perk sem lifecycle/caps. Fail-closed para duplicação/reownership. | Q3/Q5 |

## Causalidade, concepção e pendências

Cast, UUID da montaria, vítima/passenger, source e fase de incoming event precisam ser correlacionados. Contador decrementado/cancelamento não são casts adicionais nem dano/XP de defesa automaticamente válido. Iron’s/Asterism possuem custo e efeito; RPG só altera por contrato real; Black Arcana/Enshrouded não repetem cancelamento, montaria ou restituição de vida. Assinatura ocupada: suspensão self com defesa por eventos qualificados, duração e contador separados; novo visual/nome não cria outra habilidade.

- **Q1:** fingerprint/config/níveis/P efetivos, truncamento e extremos, cooldown/mana/fontes de cast e aquisição real.
- **Q2:** n1/n8, tooltip vs contador, vários hits no mesmo tick, amount0, melee/projétil/ownerless/environmental, aliados/PvP e outros listeners cancelando.
- **Q3:** expiração strict/contador negativo, anti-magic/kill/removePassenger, mount/spawn recusado, owner removido/morto, reentrância e sync cliente.
- **Q4:** poses/dimensões de passageiros, água/colisão/obstáculos, troca de montaria e proteção/claims, caster diferente do passenger.
- **Q5:** unload/restart/relog, Owner/contador/timer e montaria persistidos, coexistência e servidor/Survival/multiplayer. **PENDING**, nenhum runtime/adapter/perk ou Stage promovido.

[versions]: https://github.com/BirdieVibes/Asterism-Arcanum/blob/f1738c7813a85d31a6da10e6c9f2dbce18d2b583/gradle.properties#L9-L24
[registry]: https://github.com/BirdieVibes/Asterism-Arcanum/blob/f1738c7813a85d31a6da10e6c9f2dbce18d2b583/src/main/java/com/birdie/asterismarcanum/registries/ASARSpellRegistry.java#L28-L31
[spell]: https://github.com/BirdieVibes/Asterism-Arcanum/blob/f1738c7813a85d31a6da10e6c9f2dbce18d2b583/src/main/java/com/birdie/asterismarcanum/spells/CelestialTetherSpell.java#L23-L47
[cast]: https://github.com/BirdieVibes/Asterism-Arcanum/blob/f1738c7813a85d31a6da10e6c9f2dbce18d2b583/src/main/java/com/birdie/asterismarcanum/spells/CelestialTetherSpell.java#L70-L79
[duration]: https://github.com/BirdieVibes/Asterism-Arcanum/blob/f1738c7813a85d31a6da10e6c9f2dbce18d2b583/src/main/java/com/birdie/asterismarcanum/spells/CelestialTetherSpell.java#L82-L85
[entity]: https://github.com/BirdieVibes/Asterism-Arcanum/blob/f1738c7813a85d31a6da10e6c9f2dbce18d2b583/src/main/java/com/birdie/asterismarcanum/entity/spells/celestial_tether/CelestialTetherEntity.java#L27-L44
[owner]: https://github.com/BirdieVibes/Asterism-Arcanum/blob/f1738c7813a85d31a6da10e6c9f2dbce18d2b583/src/main/java/com/birdie/asterismarcanum/entity/spells/celestial_tether/CelestialTetherEntity.java#L56-L80
[counter]: https://github.com/BirdieVibes/Asterism-Arcanum/blob/f1738c7813a85d31a6da10e6c9f2dbce18d2b583/src/main/java/com/birdie/asterismarcanum/entity/spells/celestial_tether/CelestialTetherEntity.java#L63-L90
[tick]: https://github.com/BirdieVibes/Asterism-Arcanum/blob/f1738c7813a85d31a6da10e6c9f2dbce18d2b583/src/main/java/com/birdie/asterismarcanum/entity/spells/celestial_tether/CelestialTetherEntity.java#L94-L121
[cleanup]: https://github.com/BirdieVibes/Asterism-Arcanum/blob/f1738c7813a85d31a6da10e6c9f2dbce18d2b583/src/main/java/com/birdie/asterismarcanum/entity/spells/celestial_tether/CelestialTetherEntity.java#L123-L151
[rider]: https://github.com/BirdieVibes/Asterism-Arcanum/blob/f1738c7813a85d31a6da10e6c9f2dbce18d2b583/src/main/java/com/birdie/asterismarcanum/entity/spells/celestial_tether/CelestialTetherEntity.java#L155-L183
[nbt]: https://github.com/BirdieVibes/Asterism-Arcanum/blob/f1738c7813a85d31a6da10e6c9f2dbce18d2b583/src/main/java/com/birdie/asterismarcanum/entity/spells/celestial_tether/CelestialTetherEntity.java#L170-L199
[dimensions]: https://github.com/BirdieVibes/Asterism-Arcanum/blob/f1738c7813a85d31a6da10e6c9f2dbce18d2b583/src/main/java/com/birdie/asterismarcanum/entity/spells/celestial_tether/CelestialTetherEntity.java#L201-L240
[anti]: https://github.com/BirdieVibes/Asterism-Arcanum/blob/f1738c7813a85d31a6da10e6c9f2dbce18d2b583/src/main/java/com/birdie/asterismarcanum/entity/spells/celestial_tether/CelestialTetherEntity.java#L242-L245
[entity-registry]: https://github.com/BirdieVibes/Asterism-Arcanum/blob/f1738c7813a85d31a6da10e6c9f2dbce18d2b583/src/main/java/com/birdie/asterismarcanum/registries/ASAREntityRegistry.java#L122-L129
[handler]: https://github.com/BirdieVibes/Asterism-Arcanum/blob/f1738c7813a85d31a6da10e6c9f2dbce18d2b583/src/main/java/com/birdie/asterismarcanum/events/ServerEvents.java#L40-L48
[description]: https://github.com/BirdieVibes/Asterism-Arcanum/blob/f1738c7813a85d31a6da10e6c9f2dbce18d2b583/src/main/resources/assets/asterismarcanum/lang/en_us.json#L42-L43
[loot]: https://github.com/BirdieVibes/Asterism-Arcanum/blob/f1738c7813a85d31a6da10e6c9f2dbce18d2b583/src/main/resources/data/asterismarcanum/loot_table/entities/astromancer.json#L1
[host-cast]: https://github.com/iron431/irons-spells-n-spellbooks/blob/e4056af90302d37eb1739f5ff05020b020e6e252/src/main/java/io/redspace/ironsspellbooks/api/spells/AbstractSpell.java#L160-L325
[friendly]: https://github.com/iron431/irons-spells-n-spellbooks/blob/e4056af90302d37eb1739f5ff05020b020e6e252/src/main/java/io/redspace/ironsspellbooks/damage/DamageSources.java#L134-L163
