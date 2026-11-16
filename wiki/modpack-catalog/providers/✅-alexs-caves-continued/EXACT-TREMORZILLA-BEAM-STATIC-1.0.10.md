# Tremorzilla Beam — certificado técnico estático individual (1.0.10)

**Status: ✅ contrato estático do tipo de dano alexscaves:tremorzilla_beam.** O escopo é o recurso DamageType, sua factory de DamageSource, seus produtores e consumidores diretos no JAR físico. Não corresponde à habilidade inteira do Tremorzilla, à validação do feixe em jogo nem à aprovação para alterar dano, área, mundo ou recursos por perks.

## Identidade e proveniência

- Artefato: Alex's Caves Continued 1.0.10, alexscaves-1.0.10-neoforge+1.21.1.jar, instalado conforme modlist #019 do RPG Skill Tree. Minecraft 1.21.1, NeoForge físico 21.1.250, Java 21.
- JAR publisher: 75.279.314 bytes, SHA-1 6960b299a39a039ac8a5eb9b07be4ad0e3e0a570, SHA-256 36ae0a3cbd028df466a37c671ba2fdf021c060ca1c9c1c32e9f2e95bffae0e7c.
- Recurso data/alexscaves/damage_type/tremorzilla_beam.json: SHA-256 a059d2c010509db8d56f984d6d403a8901d1442d0ba47eff2f009c6998b58e9a; campos message_id=tremorzilla_beam, scaling=never, exhaustion=0.3. Nenhuma referência direta em tags/damage_type do JAR publisher; tags finais de datapack não verificadas.
- Factory ACDamageTypes.causeTremorzillaBeamDamage(RegistryAccess, Entity):DamageSource — 13 instruções JVM, SHA de método 4be31969b91f514afc0624e4dbc28af58a360ba3fdd6def9e9ba86fe03d759b6. Lê TREMORZILLA_BEAM e constrói DamageSourceRandomMessages com a entidade como argumento. Não comprova crédito final de morte ou Mastery.
- Hashes de classe: TremorzillaEntity.class = e1ac60a8005f9414dde1d25a92a2110df65cef145c3225e9c2557c96672fe8dc; ACDamageTypes.class = 389fb88f8d6e1515e3dfe7f401a728bb33629666bd2319ae7e25668f710e4ef6.

## Corpos completos e produtores

A [auditoria read-only](../../../../docs/qa/alexscaves_1010_tremorzilla_beam_static_audit.py) certifica **12 métodos completos e 2.808 instruções JVM** (não todos os 116 métodos declarados de TremorzillaEntity). Métodos: hurtEntitiesAround (169), tickBreath (306), canEntityBeHurtByBeam (27), breakBlocksAround (166), tick (1664), stompEffect (176), tickBeamTargeting (160), createInitialBeamVec (106), getBeamShootFrom (12), getCharge (7), getMaxBeamBreakLength (8), setMaxBeamBreakLength (7). Os digests individuais constam em [EXACT-TREMORZILLA-BEAM-STATIC-1.0.10.json](EXACT-TREMORZILLA-BEAM-STATIC-1.0.10.json), reconciliados com os três manifestos históricos de Beam, World/LOS e Normal-CFG.

O mesmo helper hurtEntitiesAround recebe dez chamadas nativas diretas: sete de tick (offsets 1455/1537/1558/1579/1599/1619/1863), uma de stompEffect (357) e duas de tickBreath (552/578). Somente as duas de tickBreath fornecem a primeira flag boolean como verdadeira, selecionando causeTremorzillaBeamDamage no offset 76. As outras usam a seleção de DamageSources.mobAttack no offset 87; **não são ataques do tipo de dano Tremorzilla Beam**.

O lado servidor executa o segmento de dano de tickBreath; seu ciclo de amostras exige endpoint não nulo e beamTime % 3 == 0. O trajeto avança por vetor normalizado, com passo baseado em 1,5 vezes o raio local, sob o limite getMaxBeamBreakLength. Os dois pontos pedem **20.0F de dano**, sem comprovar aceitação, cadência garantida por alvo ou DPS. O endpoint usa raio de seleção 6.0F; as amostras utilizam um raio variável incrementado em um. Os resultados booleanos do helper são descartados no emissor (pop nos offsets 555 e 581).

## Targeting e consequências condicionais

hurtEntitiesAround usa AABB centrada no argumento Vec3 com semiextensão float recebida. Se a última flag é verdadeira, a caixa ajusta Y entre a altura do Tremorzilla menos um e a altura dos olhos mais três; isso é volume de busca, não o alcance universal do feixe. Level.getEntitiesOfClass recebe NO_CREATIVE_OR_SPECTATOR. O helper rejeita o próprio mob, aliados, entidades do mesmo tipo e distância ao quadrado maior que raio²; uma segunda flag seleciona exclusão de KaijuMob.

Quando a flag de beam está ativa, canEntityBeHurtByBeam faz Level.clip usando Block.COLLIDER e Fluid.NONE até a região central do alvo e devolve verdadeiro **somente se o tipo do resultado é MISS**. O raycast é requisito local, não prova de PvP/claims ou de outros transformers. ACCompat.hurt recebe o float de dano e seu retorno falso encerra o processamento do candidato. Apenas após retorno verdadeiro é solicitada a aplicação de knockback. Só no ramo beam, com o retorno positivo, há verificação de alvo Enemy e saúde <= 0 para incrementar killCountFromBeam; também é solicitado efeito Irradiated de **6000 ticks e amplifier 2**. A resposta booleana de LivingEntity.addEffect é descartada. Dano aceito não implica morte real ou efeito aplicado com sucesso.

## Custos, persistência e mundo

O DamageType não tem nível, mana, cast, munição ou cooldown próprios (**N/A por natureza do recurso**); exhaustion=0.3 é metadado de tipo de dano, não custo Black Arcana. Charge, beamTime, beamServerTarget, MAX_BEAM_BREAK_LENGTH e killCountFromBeam são estado da entidade provider. O contrato cobre getters SynchedEntityData e consumidores selecionados, mas não certifica persistência NBT, save/reload, C2S, ownership final de XP ou física.

breakBlocksAround contém early return para isBaby, ACPlatform.canEntityGrief negado e lado cliente, além de filtros nuke-proof, resistência, geometria e RNG. Ele pode solicitar Level.destroyBlock, onBlockExploded, criação de NuclearBombEntity e Level.addFreshEntity. A configuração devastatingTremorzillaBeam diferencia raios e a rota de destruição adicional, mas um caminho da amostragem ainda chama breakBlocksAround com raio reduzido quando ela está falsa. Essa cadeia **não** comprova proteção de claims por bloco ou WorldEffectPolicy. A auditoria histórica FTB Chunks 2101.1.22 identificou a tag padrão de mob griefing apenas para enderman; listeners/datapacks reais permanecem não verificados.

## Replay e limites

Reproduzir com Java 21, o JAR publisher SHA-exato e:

1. python3 docs/qa/alexscaves_1010_tremorzilla_beam_static_audit_test.py -v
2. python3 docs/qa/alexscaves_1010_tremorzilla_beam_static_audit.py --jar CAMINHO_DO_JAR --javap javap --seal wiki/modpack-catalog/providers/✅-alexs-caves-continued/EXACT-TREMORZILLA-BEAM-STATIC-1.0.10.json
3. python3 scripts/catalog/check_perk_ready_indexes.py
4. python3 scripts/catalog/generate_perk_ready_indexes.py --check

O workflow SHA-exato verificou 12 corpos íntegros, 2.808 instruções, factory de 13 instruções, **46 pivôs causais**, dez callsites e sete testes sintéticos negativos. Escopo **STATIC_TECHNICAL_CATALOG_ONLY**. Marcas independentes: mutating_hook=NOT_VERIFIED; physical_qa=NOT_TESTED; mutation=NO_MUTATION; provider_universe_closed=false; gameplay_hit_damage=NOT_CERTIFIED; pvp_claims=NOT_VERIFIED; world_effect_policy=NOT_VERIFIED; effective_datapack_tags=NOT_VERIFIED.

A autoridade do runtime mágico próprio permanece no Black Arcana. RPG Skill Tree apenas provê progressão/perks/Mastery mediante boundary real. Nenhum código, cast ou root de terceiro foi copiado/implementado.
