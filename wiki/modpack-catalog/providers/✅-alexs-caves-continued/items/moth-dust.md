# Moth Dust

**Estado:** ⚠️ PARCIAL / STATIC_DISCOVERY_ONLY. `static_contract=NOT_CERTIFIED; mutating_hook=NOT_VERIFIED; physical_qa=NOT_TESTED; NO_MUTATION`. Não constitui nova raiz semântica certificada.

**Autoridade:** Alex's Caves Continued (`alexscaves`) 1.0.10, Minecraft 1.21.1 / NeoForge / Java 21. Modlist sibling #19; publisher `alexscaves-1.0.10-neoforge+1.21.1.jar`, SHA-1 `6960b299a39a039ac8a5eb9b07be4ad0e3e0a570`, SHA-256 `36ae0a3cbd028df466a37c671ba2fdf021c060ca1c9c32e9f2e95bffae0e7c`. [Replay](https://github.com/Gustavaopere/Black-Arcana/actions/runs/45653331096/job/139343330423), HEAD `b5bc7f2d5f70fe485036dc7e79285fa96ae7867b`, duas saídas idênticas de 335.054 bytes, SHA-256 `a9afad89d2771265dfbb4f86c2981bba8d204943e053d4364af82af69c5a7f41`. [Dossiê](../EXACT-MARINE-FISH-MOTH-1.0.10.md). Sem novo dump físico ou configuração efetiva.

## Identidade e descrição funcional

`alexscaves:moth_dust`; owner `MothDustItem`; factory `ACItemRegistry.lambda$static$122`, Code SHA-256 `20fac1a05d60f7390148c4a90e14a151511ba918fb57388a09b978b7dbcd4948`. [Registro](../systems/item-registry.md). Item carregável que induz mobs elegíveis a perseguir uma entidade atingida. Descrição interpretativa do binário. Modelo `assets/alexscaves/models/item/moth_dust.json`, SHA-256 `293ac1ab9c1db699f5e385954e7f773e2d899347f0351a1cf4bb7e428d06c4e0`, apenas apresentação.

## Ativação, targeting e parâmetros

use inicia uso e retorna consume; animação BOW; duração máxima 72.000 ticks. releaseUsing exige Player. elapsed=getUseDuration−remaining; t=elapsed/20F; power=min(1,(t²+2t)/3), sem clamp inferior explícito. Raycast solicita 5F×power blocos via ProjectileUtil.getHitResultOnViewVector @47 e Entity.canBeHitByProjectile. Sem gate de carga mínima explícito.

Se EntityHitResult contém LivingEntity que canBeSeenAsEnemy, consulta AABB centrada na posição do hit ±32 em X/Y/Z (64 de lado, não esfera), getEntities @340, mesmo predicado de hit. Exclui alvo inicial, aliados em ambas direções e passageiros do mesmo veículo. Exige tag MOTH_DUST_ENRAGES e Mob; setTarget(alvo) @448 e setLastHurtByMob(alvo) @455. O alvo induzido é a entidade atingida, não caster. A tag empacotada contém vesper, corrodent, underzealot, forsaken e watcher; overrides não auditados. Sem limite próprio de quantidade, dano direto, debuff de duração fixa, summon ou guarda explícita de lado demonstrados.

Apresentação: ceil(3×alcance solicitado) iterações; offsets nextFloat−0,5 por eixo no hit e olho, vetor normalizado escalado por 5×power. Partículas não comprovam colisão ou sucesso de controle.

## Custos, estado e integração

shrink(1) fora de creative @471 inclusive sem alvo elegível. Não há mana/cooldown próprios demonstrados. Alvo e memória last-hurt pertencem à AI dos mobs; não atribuir kill/XP ao caster pela mera ativação. Perks conceituais de alcance, volume de busca, filtros e custo; duração e persistência da AI, engine raycast, targeting, PvP e eventos não fechados. NO_MUTATION: não repetir release, alterar alvo ou duplicar Mastery sem boundary real. Tag `data/alexscaves/tags/entity_type/moth_dust_enrages.json` SHA-256 `5d7807c49608ec6c6250dd376c42519d74a317dd4f844b7b6382568eb8c8a402`.

## Localizadores de evidência

Classfile SHA-256 `ce046ddfe30a9c860570332b04b63b619ad29d3f87b170b935b7b2dbd3db3faf`.

| Método e descritor | Instruções | Code SHA-256 |
|---|---:|---|
| `<init>()V` | 6 | `8be36d6241481f2aa744705cb8bf58543a3d2d603628b0a2626b73949973458c` |
| `getUseAnimation(Lnet/minecraft/world/item/ItemStack;)Lnet/minecraft/world/item/UseAnim;` | 2 | `dfb9aff16602b7340870ab7fc902b22294f662e441389a5a6c3b983791acee04` |
| `use(Lnet/minecraft/world/level/Level;Lnet/minecraft/world/entity/player/Player;Lnet/minecraft/world/InteractionHand;)Lnet/minecraft/world/InteractionResultHolder;` | 10 | `be2d1d78173630b6745f5890c9ac0bcee6fe32c2fb3906c8d416cb45bca71be5` |
| `releaseUsing(Lnet/minecraft/world/item/ItemStack;Lnet/minecraft/world/level/Level;Lnet/minecraft/world/entity/LivingEntity;I)V` | 201 | `5f73541a31cf91fb222b685ee4eb456b7ffc2b91c19c29420a1311880f2f99fe` |
| `getUseDuration(Lnet/minecraft/world/item/ItemStack;Lnet/minecraft/world/entity/LivingEntity;)I` | 2 | `b8aee7c99ad68ca4f9bded1dd23b0ec788cfe9329b0d036d54e7e6c95cb79b51` |
| `getPowerForTime(I)F` | 23 | `171bb48bcef90c7751d8b427a556bc04c5896001df0fcc9eab39585c8ab9af69` |


## Continuação individual — targeting, memória de agressão e autoridade

Base Black Arcana `81dbec3021492e8862b36bb6bbb844d956d742d9`; modlist sibling `b05e2536461bc0a9c526dc47a38e3b9af62d941c`, NeoForge 21.1.250 e Alex's Caves 1.0.10. Releitura da prova publisher [45653331096/job 139343330423](https://github.com/Gustavaopere/Black-Arcana/actions/runs/45653331096/job/139343330423) confirma os pivôs individuais:

- use: Player.getItemInHand @2, startUsingItem @9, ACCompat.useConsume @14; duração declarada 72000 ticks, animação BOW. releaseUsing testa Player @4; não-player segue ao retorno @474 sem custo. Para Player, elapsed = duração - remaining @21; getPowerForTime @26, 5F × power @35, raycast @47. Fórmula Code `171bb48bcef90c7751d8b427a556bc04c5896001df0fcc9eab39585c8ab9af69`: t=elapsed/20F, (t²+2t)/3F, clamp superior 1F, sem clamp inferior explícito. Exemplos nominais elapsed=0 -> 0; 5 -> 0.1875 (alcance 0.9375); 10 -> 5/12 (alcance 25/12); 20 -> 1 (alcance 5). São cálculos da fórmula, não medidas de colisão. O raycast não é um projétil persistente. Sem mana própria, sem mínimo explícito de carga.
- releaseUsing Code `5f73541a31cf91fb222b685ee4eb456b7ffc2b91c19c29420a1311880f2f99fe`: os dois predicates @39 (raycast) e @335 (consulta de entidades) são handles kind 5 Entity.canBeHitByProjectile()Z, bootstrap #0. Hit location @54. Partículas antes da verificação de EntityHitResult @253; loop ceil(3×alcance) @71, vetor visual @183/192; não evidência de controle bem-sucedido.
- EntityHitResult -> LivingEntity -> canBeSeenAsEnemy @287; AABB @325 com offsets -32/+32 em cada eixo, Level.getEntities @340. Para cada candidato, LivingEntity.is @376 (excluir alvo inicial), target.isAlliedTo @386, candidate.isAlliedTo @396, isPassengerOfSameVehicle @406, tipo/Holder.is(MOTH_DUST_ENRAGES) @423, instanceof Mob @434. setTarget @448 seguido de setLastHurtByMob @455. Setter não é confirmação de aquisição de alvo, ataque, dano, kill ou XP. Alvo induzido é entidade atingida, não o jogador; não substituir autoria de dano/last-hurt por caster. Não há limite numérico local de candidatos.
- Player.isCreative @463, shrink(1) @471 em noncreative, também quando MISS/bloco/alvo inválido ou nenhum mob elegível. Não pressupor consumo atômico com aquisição de agressividade. Sem cooldown próprio demonstrado; gates upstream e intervenções externas podem existir.

### Coleta distribuída preparada (não executada nesta revisão)
[Sonda](../../../../../docs/qa/alexscaves_1010_moth_dust_targeting_probe.py) `fa575f125f1dd0ab661267ff732047514e3eaa56` e [workflow](../../../../../.github/workflows/alexscaves-1010-moth-dust-targeting.yml) `195f87ac7e0969591142785ba38343fbc548b9bb`: preserva publisher, tag/model e sete Code pins; seleciona raycast ProjectileUtil/AABB/clip, predicados Entity/LivingEntity, Mob.setTarget, last-hurt, target goals e cancelamento NeoForge, cadeia de uso/soltura e custos. Censo de Fieldref/recursos e candidatos de classe pelos nomes da tag; nome de classe não prova registro de EntityType. Não presumir cobertura dos goals internos nem duração efetiva antes de verificar. Replays duas vezes, orçamento e filtros; sem integração mutadora ou novo root. `NOT_CERTIFIED / NO_MUTATION / NOT_TESTED`.
