# Purple Soda Bottle Rocket

**Estado:** ⚠️ PARCIAL / STATIC_DISCOVERY_ONLY. `static_contract=NOT_CERTIFIED; mutating_hook=NOT_VERIFIED; physical_qa=NOT_TESTED; NO_MUTATION`. Sem nova raiz semântica certificada.

## Identidade e autoridade
`alexscaves:purple_soda_bottle_rocket`, owner `SodaBottleRocketItem`, factory `ACItemRegistry.lambda$static$191`, Code SHA-256 `4dc589cd486b67dc65677e0388911cb53182ffdfb49ca2459bf226a07bb96d72`. [Registro](../systems/item-registry.md). Alex's Caves Continued 1.0.10, Minecraft 1.21.1/NeoForge/Java21, modlist sibling #19; JAR publisher `alexscaves-1.0.10-neoforge+1.21.1.jar`, SHA-1 `6960b299a39a039ac8a5eb9b07be4ad0e3e0a570`, SHA-256 `36ae0a3cbd028df466a37c671ba2fdf021c060ca1c9c1c32e9f2e95bffae0e7c`, 75.279.314 bytes. [Dossiê](../EXACT-LATE-CONCRETE-ITEMS-1.0.10.md), [run/job](https://github.com/Gustavaopere/Black-Arcana/actions/runs/45794089694/job/139820167569), HEAD `27c5bbc7780abbb2efe9bf2c4db615be5d0e7b3c`, dois replays byte-idênticos 425337 bytes, SHA-256 `aa6b3b052b975590f56dd2fa62773fe907346495093ef1842b0405de17b585a2`. Sem dump físico novo.

## Ativação e custo
Construtor Item.Properties default. useOn(UseOnContext) servidor: stack, click location C e face normal d, cria SodaBottleRocketEntity(level,player,C+0.15D*d,stack) @87; addFreshEntity @95 retorno descartado; getPlayer().isCreative() @103 sem guarda explícita de null, shrink(1) se não criativo; sidedSuccess. use(Level,Player,Hand): se !isFallFlying retorna usePass; caso contrário no servidor cria SodaBottleRocketEntity(level,stack,player) @30, addFreshEntity @33 retorno ignorado, shrink1 se !instabuild; useSidedSuccess. Rotas possuem gates de lado distintos e ambas debito condicionado à criatividade, não à aceitação de spawn. Parâmetros de aceleração/voo, detonação, alcance, targeting, AOE, dano e tipo, owner, lifecycle, colisão, persistência e efeito de mundo estão na entidade downstream ainda não fechada. Sem mana/cooldown próprios. Perks de propulsão apenas conceituais; não duplicar entidade, débito ou XP; NO_MUTATION.

## Recursos e evidência reproduzível
- `assets/alexscaves/models/item/purple_soda_bottle_rocket.json` SHA-256 `5a55d5e37caa97ec7770df46f53651c7675c66f1d8367ab2ee4e6415e2df14b0`.
- `data/alexscaves/recipe/purple_soda_bottle_rocket.json` SHA-256 `7717bf0d3c751da91753396ce37b5f7cfed578b139c956c11b5e490139ad7962`; resultado 3 unidade(s).
Classfile SHA-256 `bbc633c61e6226a10cbf00bce158c2a272d3a7f1ee40dd03b3a049d8c957fb42`.

| Método e descritor | Instruções | Code SHA-256 |
|---|---:|---|
| `<init>()V` | 6 | `8be36d6241481f2aa744705cb8bf58543a3d2d603628b0a2626b73949973458c` |
| `useOn(Lnet/minecraft/world/item/context/UseOnContext;)Lnet/minecraft/world/InteractionResult;` | 62 | `c5221cffe368acde6d7703a50cdac5d9ea5b8ff4419e09330f4d42c697a1d488` |
| `use(Lnet/minecraft/world/level/Level;Lnet/minecraft/world/entity/player/Player;Lnet/minecraft/world/InteractionHand;)Lnet/minecraft/world/InteractionResultHolder;` | 38 | `1c75677a6269c8119f804f5fac20e9acfc4cbf61f66758045b3dd49bdc3a9159` |

Limites gerais: inspeção estática do publisher, sem prova de runtime transformado, aceitação de chamadas, compatibilidade ou proteção de mundo. `NO_MUTATION / FAIL_CLOSED / PHYSICAL_QA_NOT_TESTED`.

## Downstream nativo — #1236

[Run 45797529084/job 139831910862](https://github.com/Gustavaopere/Black-Arcana/actions/runs/45797529084/job/139831910862), HEAD `39127f8fbc3fcf51c82e00956ea785f97d75df28`: dois relatórios SHA-256 `f8d679937def972ac001dd8d9517fb46d3f7f5a4a0580db4e128e5b21cd94557`, 1.535.579 bytes. [Dossiê](../EXACT-PROJECTILE-MACHINE-DOWNSTREAM-1.0.10.md).

Owner SodaBottleRocketEntity, class SHA-256 `73a4d9bb64f255503ffeca52e8576aa4570052a75ba7c87767bb9ff8b9d53877`, FireworkRocketEntity, 8/8 métodos próprios. tick()V Code `bd67a7ad6729d27559db4d396e51b3e0ce1c4a44a4327adbf31103d5e909ec7f` chama super.tick @1, incrementa phageAge, no cliente solicita cinco partículas PURPLE_SODA_BUBBLE; não equivale a propulsão. handleEntityEvent(B)V Code `96191cb135d3dc51c8fbf3edb9a38a7bcdc1b65774daf5deff2953112796838a` trata evento 17 com apresentação FROSTMINT_EXPLOSION, SNOWFLAKE, PURPLE_SODA_BUBBLE e som de foguete dependente da câmera; não comprova dano, AOE ou congelamento real. getItem retorna stack PURPLE_SODA_BOTTLE_ROCKET. Pendem construtores e dados herdados de FireworkRocketEntity, propulsão, explosão, duração, owner/attachment, NBT e liquidação do uso. Não transformar efeitos visuais em status ou dano adicional.

Estado mantido: STATIC_DISCOVERY_ONLY / NOT_CERTIFIED / NO_MUTATION / NOT_TESTED. Sem nova raiz ou hook.

## Reconciliação de fronteiras distribuídas

Receita shapeless direta (SHA-256 `7717bf0d3c751da91753396ce37b5f7cfed578b139c956c11b5e490139ad7962`): três purple_soda_bottle mais um frostmint, saída três foguetes. Isso não prova dano, duração de propulsão nem componentes de explosão. Herança de FireworkRocketEntity deve ser auditada separadamente de apresentação de partículas e de lançamento de ThrowableProjectile. Não incrementar Mastery por efeito cosmético.

Evidência compartilhada: [matriz de reconciliação](../EXACT-CATALOG-INHERITED-BOUNDARIES-1.0.10.md). Mantidos NOT_CERTIFIED, NO_MUTATION e NOT_TESTED; nenhuma promoção por herança isolada.

## Continuação individual — construção, tempo de vida e vínculo

Releitura direta dos registros SEMANTIC e CONSUMER_SITE de [run 45797529084/job 139831910862](https://github.com/Gustavaopere/Black-Arcana/actions/runs/45797529084/job/139831910862) (dois replays já registrados acima; não é nova extração). Base Black Arcana `81dbec3021492e8862b36bb6bbb844d956d742d9`; modlist sibling `b05e2536461bc0a9c526dc47a38e3b9af62d941c` permanece vigente nesta coleta (#001 NeoForge 21.1.250; #019 publisher 1.0.10).

| Construtor próprio de SodaBottleRocketEntity | Code SHA-256 | Contrato observado |
|---|---|---|
| (EntityType,Level)V | `7de8b3e8daac56a645f684d85df8875e311764a8a4fff3baa330aa7eb80a9e3f` | super @3; phageAge=0 @8. Não demonstra a inicialização completa dos dados herdados. |
| (Level,DDD,ItemStack)V | `2593b82d9b9bca3de8485f870d73f147a564a5f279e14ee5b04ab373ea23b298` | SODA_BOTTLE_ROCKET @1, super @13, phageAge=0 @18, setPos @27; copia stack para DATA_ID_FIREWORKS_ITEM @58 somente se não vazia e ACCompat.hasTag=true (@32/@40); setDeltaMovement @91; lifetime @109. |
| (Level,Entity,DDD,ItemStack)V | `7ffc2d8bbe23e21a6b9b0346247bfa61eedce1417d434af83b979c10d7488a89` | delega ao anterior @9, setOwner(entity) @14. |
| (Level,ItemStack,LivingEntity)V | `5c463c17dd0de5e0ecc289fafc0bbbf05c39954370e195a43f37c373143c1dab` | lê X/Y/Z da entidade @4/8/12; delega ao construtor com owner @16; DATA_ATTACHED_TO_TARGET = OptionalInt.of(entity.getId()) @23–33. |

Velocidade inicial solicitada: X/Z = chamadas independentes nextGaussian() multiplicadas por 0,001D (pivôs @66/71/74 e @82/87/90); Y = 0,05D (@75). Trata-se de vetor inicial de movimento, não velocidade final de voo do jogador. Lifetime inicial = 18 + RandomSource.nextInt(14), @95–109, portanto 18–31 ticks nominais (0,90–1,55 s a 20 TPS). O valor não demonstra o comparador de expiração ou a duração efetiva de boost; colisões, carga de estado e tick herdado ainda devem ser examinados. Owner e attachment são canais distintos; o attachment usa ID de entidade, não UUID nesse construtor. Não assumir sobrevivência do vínculo após reload ou dimensão.

A janela de ACEntityRegistry.<clinit> (Code `710e51c9e0ec3ea0d80a5b00223bcd46ea73ac9f7c123542efccd93e4b65568c`) mostra DEF_REG @1401, literal soda_bottle_rocket @1404, bootstrap #197 @1407 (handle lambda$static$81) e SODA_BOTTLE_ROCKET @1415. A geometria e demais parâmetros da factory ainda exigem leitura do corpo, não do nome.

O gate ACCompat.hasTag não demonstra presença do componente FIREWORKS. A implementação de getItem() cria uma nova ItemStack do item registrado, não retorna a cópia DATA_ID_FIREWORKS_ITEM. É necessário distinguir getItem de qualquer consumidor direto do dado sincronizado antes de inferir explosão, potência ou dano. O pacote de spawn é delegado a ACPlatform.getEntitySpawningPacket @2 (Code `8b5dfced1a06468618f061569501e97bb8d2abdc33d4cbe8284fcabfecb9cc81`), sem prova de equivalência de estado após round-trip.

### Perks e consumidores pendentes

Propulsão, duração, alcance, detonação, dano, raio e autoria exigem a análise de FireworkRocketEntity distribuído em NeoForge 21.1.250, do contexto de dados/componentes e dos gates de colisão. Não usar lifetime nominal como janela garantida de Mastery, nem partículas como receipt de dano. Não duplicar setOwner, boost, spawn ou débito; `NO_MUTATION`. A coleta complementar deve resolver a factory, os métodos herdados, a identidade de FIREWORKS e os eventos que controlam settlement. Mantidos NOT_CERTIFIED e NOT_TESTED.

[Coleta complementar](../../../../../docs/qa/alexscaves_1010_soda_rocket_engine_probe.py) e [workflow](../../../../../.github/workflows/alexscaves-1010-soda-rocket-engine.yml) preparados: pinam os arquivos distribuídos do engine 21.1.250, publisher e cinco classes, três Code SHA; projetam todos os corpos de SodaBottleRocketEntity, SodaBottleRocketItem e FireworkRocketEntity, além de consumidores selecionados e as duas factories. O resultado da execução e os dois replays ainda são PENDENTES. Métodos opcionais ausentes devem ser tratados como descoberta, não como prova de ausência de comportamento. Nenhuma promoção de índice ou ledger.

### Coleta distribuída aprovada — propulsão, explosão e persistência

[Run 46097983726 / job 140833674942](https://github.com/Gustavaopere/Black-Arcana/actions/runs/46097983726/job/140833674942), HEAD `57f5ccb512e8c14f782b8ef941fe7482db69a778`: todas as etapas do job específico success, dois relatórios byte-idênticos de 1.197.906 bytes, SHA-256 `f56618d748fc913907bc8feee7f79f92eaa72c45995526c0cccc8744b1457bf6`. Publisher e engine distribuídos pinados; FireworkRocketEntity overlay SHA `66368afc3aeeb1327e84d16119d0b5d833a45999bc1fc6e199ec0eb74e230b14`, 28 métodos projetados. Não equivale a runtime transformado.

**Registry e dimensões:** ACEntityRegistry.lambda$static$81 Code `643da61f9c7652ab180c4c86ca022a1dcebd44a446f3ad27a55a09d71cbac04e`: MobCategory.MISC @5, sized(0.5F,0.5F) @17, setUpdateInterval(1) @21, setShouldReceiveVelocityUpdates(true) @25, ID soda_bottle_rocket @28. São parâmetros declarados de entidade, não raio de dano ou alcance garantido.

**Movimento:** FireworkRocketEntity.tick Code `678aff9e949d44e9262201132c212393ada24dadb10567059672d129c2c14680`. Se attachment presente e referência em memória nula, tenta resolução pelo ID em Level.getEntity (lambda$tick$0 Code `bebc05555a0710bf238499e22faa2416368bc90117aa3bd2fe503fc4460eef41`, exige LivingEntity). Se entidade resolvida está em fall-flying, para cada eixo i com direção da visão L e velocidade v, solicita v'_i=v_i+0,1 L_i+0,5(1,5 L_i−v_i)=0,5v_i+0,85L_i (aritmética @90–170; setDeltaMovement @173). Não é aceleração linear ilimitada. Sem voo, não aplica essa fórmula. Posição do foguete segue entidade/offset visual, e seu movimento copia o da entidade @231/242. Para foguete sem attachment e não shot-at-angle, multiplica X/Z por 1,15 (1 se horizontalCollision), Y por 1, e adiciona (0,0,04,0) @278–289. Depois move SELF e restaura vetor @302/307. O tick chama hitTargetOrDeflectSelf se !noPhysics; vida incrementa @394, expira no servidor apenas quando life>lifetime @495–499. Não confundir lifetime inicial com duração garantida.

**Dano condicional e geometria:** getExplosions Code `2e020dd37db4f351f39e52543aadb20b7ca0be351c1d3daaf8b4411d406109fc` lê diretamente DATA_ID_FIREWORKS_ITEM e seu DataComponents.FIREWORKS, retorna explosions ou lista vazia. Não chama getItem() sobrescrito pelo publisher. ACCompat.hasTag Code `28c8bd600a77622471bf1b63b3660521f22f8815ae9b0dc3cde938d71486df68` exige CUSTOM_DATA não nulo e não vazio; FIREWORKS sozinho não satisfaz o gate de cópia do construtor. O default sincronizado da superclasse (getDefaultItem Code `6165131a71094d386980ecccb63f738d7dbd37e03b2242b1af15782b00e40d73`) cria Items.FIREWORK_ROCKET; sua composição efetiva precisa ser verificada, não presumida pelo nome.

dealExplosionDamage Code `b01ca9427665af1bee57cec4d4cec2c01efd05ba5fccc4e9f8cd180725ecef4d`: com N=0 explosões, dano base 0 e não entra no ramo de dano; com N>0, base B=5+2N HP. Se attachment resolvido, solicita B ao próprio alvo vinculado @72. Para demais LivingEntity: consulta AABB inflada 5D, exclui attachment, exige distância²≤25, testa dois raios até getY(0,5*i), i=0,1, COLLIDER/NONE, e ao menos um MISS. Solicita B*sqrt((5−d)/5) HP @270–293, d distância até alvo. DamageSources.fireworks Code `585ad81cdda89e95d71ce921affc5da632490b1e78a546e75675639611820fe9` usa DamageTypes.FIREWORKS com foguete e owner. Retornos hurt descartados; sem garantia de dano final, PvP ou efeito aceito. Não há chamada Level.explode nesse corpo. O evento EXPLODE e partículas não provam destruição de blocos ou congelamento.

**Detonação:** explode Code `f825963728650286300e572276fcdd958e145fbc5fb865ddd6309f81bfad5512` emite entity event 17, GameEvent.EXPLODE com owner, solicita dealExplosionDamage e discard. onHitEntity Code `c18cb7205fdd7b2d6aec2ef7d81ba2b03fb9e6a8bf1d2d3f2dc061926e083c96` explode no servidor; onHitBlock Code `aa6964768f817f05d4504cbdfa1f26974209477b33aa0517bf904fb18f4eae17` solicita BlockState.entityInside e só explode no servidor se hasExplosion. onHit Code `cdaa831300f95fbe8671b27f38a608c0be253db31cc9ad59be265d1667d74785` consulta EventHooks.onProjectileImpact para hit não MISS; event Code `73d4643328b80654ff348007520af4325a82f42a21a5fc83d0d0d25edfe67746` posta evento e retorna isCanceled. Falta fechar dispatch de hitTargetOrDeflectSelf e consumidores do bloco/transformações reais.

**Persistência e autoria:** Projectile.setOwner Code `d1664e477b42f0eeee1c4eb21092f1f7c23dfab91864a6bab86186abf1c7604e` grava UUID e cache para owner não nulo; getOwner Code `f5de42fb9fd31774bb671c81007ee52e1d02776e42d42992af5cecf3fe28177b` reutiliza cache não removido ou busca por UUID no ServerLevel. NBT Projectile grava Owner condicional, LeftOwner e HasBeenShot; read restaura e limpa cache no ramo Owner. FireworkRocketEntity.addAdditionalSaveData Code `0fb2e83f009cd961efa4f02eb5b6d499409089380046313c28b73dcfdd50ea2f` grava Life, LifeTime, FireworksItem via getItem() virtual @32, ShotAtAngle; read Code `0ac18716d34e617bca2d97068a0936e1e662876f1b44e2cf03d2a10a34522058` restaura dados e usa default em ausência/falha. Como SodaBottleRocketEntity.getItem() cria uma stack nova do item registrado, a cópia customizada em DATA_ID_FIREWORKS_ITEM não é diretamente serializada por esse getter. Não há gravação explícita de attachment ou phageAge nesses corpos; não presumir restauração do boost ou preservação dos componentes após reload.

**Limites para perks:** movimento, lifetime, owner, raio e dano são parâmetros identificáveis no caminho distribuído, não hooks mutadores homologados. Falta fechar o componente FIREWORKS padrão, dispatch/impacto efetivo, censo de consumidores e aceitação de dano/mundo. NO_MUTATION; não duplicar boost, dano, eventos, consumo ou XP. A coleta específica passou; nenhum certificado, índice ou QA física promovido.
