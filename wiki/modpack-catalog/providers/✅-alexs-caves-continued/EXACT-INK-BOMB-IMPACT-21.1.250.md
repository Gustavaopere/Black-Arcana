# Ink Bomb e Glow Ink Bomb — impacto, targeting, geometria e registro de efeitos (21.1.250)

**DISCOVERY_ONLY / NO_MUTATION.** Publisher 1.0.10, SHA-1 `6960b299a39a039ac8a5eb9b07be4ad0e3e0a570`, SHA-256 `36ae0a3cbd028df466a37c671ba2fdf021c060ca1c9c32e9f2e95bffae0e7c`, 75.279.314 bytes. Minecraft 1.21.1, Java 21, NeoForge oficial 21.1.250. Sem dump instalado novo.

## Escopo e lacuna

Reusa [prova publisher](EXACT-HOLOCODER-HOT-CHOCOLATE-INK-BOMB-1.0.10.md), [downstream](EXACT-FOUR-ITEMS-DOWNSTREAM-21.1.250.md), [aquisição](EXACT-FOUR-ITEMS-ACQUISITION-1.0.10.md), [AI](EXACT-INK-BOMB-DEEP-ONE-INGRESS-1.0.10.md) e [defaults](EXACT-ITEM-ENTITY-DEFAULTS-21.1.250.md). O recorte novo fecha a projeção tipada dos corpos locais, seleção/deflexão do projétil e geometria do cloud, com janelas de registro de BLINDNESS/GLOWING/NIGHT_VISION/CONDUIT_POWER e THROWN. Classes cliente são candidatas opcionais; a ausência na distribuição server não prova ausência no cliente. Sem reimplementação de código publisher.

A sonda `docs/qa/alexscaves_1010_ink_bomb_impact_250_probe.py` usa oito pins de classe e nove Code hashes previamente observados. Exige distribuição e JAR exatos, método requerido presente, duas saídas idênticas, janelas de registry com escrita única de cada campo. A projeção não executa classes do jogo nem encerra todos os consumidores de status de Minecraft. Replay observado e selado abaixo.

Fichas [Ink Bomb](items/ink-bomb.md) e [Glow Ink Bomb](items/glow-ink-bomb.md) continuam parciais; sem novo certificado, raiz, hook ou QA física.

## Replay observado e selo

[Run 45535313661, job 138940354765](https://github.com/Gustavaopere/Black-Arcana/actions/runs/45535313661/job/138940354765): cinco checks, 59 corpos executáveis únicos em 17 classes; duas projeções idênticas, 465.320 bytes, SHA-256 `642a25a85314108c189a2fc717e6e6678d122c2603e7fb4c5db6effacc135691`. A primeira tentativa falhou por erro de transcrição de um hash; corrigido por comparação com a saída upstream selada, sem flexibilizar a guarda. O workflow exige o digest e tamanho reproduzidos.

## Contrato de impacto corrigido

- `InkBombEntity.onHitEntity` Code `3bb50e81c9e4f051f4bfed310339d9c019ea5303032053120765181722e1a48f`: hurt 0F @22, retorno descartado. `DamageSources.thrown` Code `6b46209a49fb0bb1ec39473978a8f425b03edc561f4fa5f6413a42f07093170b` solicita THROWN com projétil direto e owner; inicializador DamageTypes Code `54bad67d9044ae58ea0aee27384362666a9a4444d30fcfa5d4758d29d9214a43` literal thrown @557 → default namespace @559 → key @562 → THROWN @565: minecraft:thrown.
- Submarine: lights=false @45, primeiro passageiro @49; se Player, Blindness @81, Glowing @106 só com flag true, remoção Night Vision/Conduit Power @121/129 se não criativo. Ramo direto: LivingEntity @139, Blindness @163, instanceof Player @168; não-Player segue @171→186, Player criativo @183→202 (salta remoções), Player não criativo cai em @186; remove @190/198. Assim **também remove os dois efeitos em LivingEntity não-Player**. Não há Glowing direto neste ramo, mesmo na variante Glow. Status não depende do retorno de hurt; não confundir ausência de dano nominal com ausência de callbacks.
- `onHit` Code `b6d048fa7c327f7b64e3417fc776f9dee6d30cf62e68a0d954774a5c30821436` chama ancestral, ramo server cria nuvem após discard; flag controla partícula e Glowing, Blindness sempre solicitada. Construtor MobEffectInstance(Holder,I) pinado no dossiê downstream: amplifier 0, 100 ticks Blindness, 300 Glowing. Nuvem sem atribuição explícita de owner; addFreshEntity não prova spawn.

## Targeting, geometria, efeitos e persistência

| Corpo e Code SHA-256 | Fronteira observada |
|---|---|
| ProjectileUtil.getHitResultOnMoveVector `05bfaca7efca85062520a23cf5b4b8f536ba7993e66bfbb84591fdd707758630` | posição + delta, COLLIDER, margem 0.3F |
| ProjectileUtil.getHitResult `2cc7c9aec892ea906224389223919cddde437560032779d2cdc64a7224bff43b` | clip FLUID NONE, endpoint do bloco limita segmento; caixa expandTowards(delta).inflate(1D) |
| ProjectileUtil.getEntityHitResult (F) `8736ca0f2a85862907755435928f16926b060877c495345975255d1a6143d30b` | AABB.inflate(margem), clip, menor distância quadrada estrita; não importar pickRadius da overload D |
| Projectile.hitTargetOrDeflectSelf `a8efc3ef15eccd3b64830896f27554f86c9e62313aa2f89ac9a2c7777a239c83` | deflexão não-NONE pode evitar onHit; lastDeflectedBy guarda repetição |
| Projectile.deflect `f54cdf38f613b83702014b039c54ec71379accfc33b31f01cbdeb457323b9fe0` | servidor pede deflexão, setOwner e onDeflection; não congelar autoria no jogador inicial |
| AreaEffectCloud.getDimensions `b34f5152e4e7f88bc325ba24f30c835827dfbb99a572b9c82777f1054900cdeb` | width 2r, height 0.5F |
| AreaEffectCloud.onSyncedDataUpdated `9be9dd185ee63bd9b62a8a8d72d26c6439800eb538f40f3c34883c75503357f7` | DATA_RADIUS chama refreshDimensions, depois super |
| LivingEntity.isAffectedByPotions `1584def60c8d0b2e42a9c48d97a3e7cf04eef66e86e1d642db7be8f987d20192` | default !isDeadOrDying, overrides e eventos em aberto |
| ThrowableItemProjectile.setItem `342ca58804f1d89ec96ff7c5359e827563c025ca2af343d8ae8c8d6c252aa621` | copia count 1 para DATA_ITEM_STACK; setter da flag usa stack nova default após a primeira no uso manual e após leitura ancestral de Item; dispenser Glow inverte ordem |

AABB nominal da nuvem: largura 2r, altura 0.5 blocos, filtro horizontal r; não esfera. Modelo temporal anterior mantém descarte nominal age 65, nove consultas e até três seleções da mesma entidade continuamente elegível, sem garantia de aceitação.

MobEffects.<clinit> Code `9a80a4e242dd9ce9a7522771c169b4ce8c1486aed1a8ea4d1b1b7a10ddf3793b`: blindness HARMFUL, glowing NEUTRAL, night_vision e conduit_power BENEFICIAL; instâncias base sem modificador registrado nessas janelas. LocalPlayer.canStartSprinting Code `bf06395fccd53b985746a3c188684e97d89340ae37221a9cd290a3b54947b15e`: BLINDNESS impede início de sprint nessa decisão cliente, não prova cancelamento de sprint existente no servidor. FogRenderer$BlindnessFogFunction.setupFog Code `a7be33f3081deab822ef6f65addf26a711dc2cbb66927c4dfdea28c5303de456`: infinito d=5; finito d=lerp(min(1,duração/20F), primeiro argumento float, 5F); FOG_SKY início 0/fim 0.8d, outro início 0.25d/fim d. Distância de fog não é alcance de combate. LivingEntity.isCurrentlyGlowing Code `64f1ffe6c84ab3b2671c50ca8aa908acdca6678aa11e14e3c20cfe83b9c9ef8e`: servidor hasEffect(GLOWING) ou ancestral; updateGlowingStatus Code `fdefd83eba58ccbb69faf1f2c3c0b67ccccc716d020f51e964febb137102f33d` atualiza shared flag 6 se diferente. Classes cliente presentes no artefato distribuído, não dump cliente instalado.

Limites: sem handlers efetivos de outros mods, spawn/hit/remoção real, QA física ou contrato de mutação. Nenhuma nova raiz semântica.
