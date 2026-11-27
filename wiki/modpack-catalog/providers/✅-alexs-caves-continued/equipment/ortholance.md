# Ortholance

**Estado:** ⚠️ PARCIAL / STATIC_DISCOVERY_ONLY. `static_contract=NOT_CERTIFIED; mutating_hook=NOT_VERIFIED; physical_qa=NOT_TESTED; NO_MUTATION`. Não constitui nova raiz semântica certificada.

**Autoridade:** Alex's Caves Continued (alexscaves) 1.0.10, Minecraft 1.21.1 / NeoForge / Java 21; modlist sibling #19. Publisher `alexscaves-1.0.10-neoforge+1.21.1.jar`, SHA-1 `6960b299a39a039ac8a5eb9b07be4ad0e3e0a570`, SHA-256 `36ae0a3cbd028df466a37c671ba2fdf021c060ca1c9c1c32e9f2e95bffae0e7c`. [Replay](https://github.com/Gustavaopere/Black-Arcana/actions/runs/45745854148/job/139661611420), HEAD `41b0080f4a161c9fa82fdb3dc5ed57c3b77f0d82`, dois relatórios byte-idênticos de 384.061 bytes, SHA-256 `4c9aefbfedf99868ae394f1a77dfaaa85cd3c5e8b6d1554b44ed41a902d569b1`. [Dossiê](../EXACT-ORTHOLANCE-MIXTURE-CLUB-1.0.10.md). Sem novo dump físico ou configuração efetiva.

## Identidade e descrição funcional

`alexscaves:ortholance`; owner `OrtholanceItem`; factory `ACItemRegistry.lambda$static$110`, Code SHA-256 `8b877c684803c7473ec03238d4f62a31f2125d8b896b31340e2bd3894d3db0da`. [Registro](../systems/item-registry.md). Arma de ataque corpo a corpo e impulso carregado com ondas. Descrição interpretativa do binário.

## Ativação, parâmetros, targeting e efeitos

Factory durabilidade 340, UNCOMMON. Modificadores MAINHAND ADD_VALUE ATTACK_DAMAGE +5D e ATTACK_SPEED −2.4000000953674316D; enchantment value 1. Animação BOW; uso máximo 72000 ticks. use falha quando damageValue>=maxDamage−1. Release aceita LivingEntity; C=clamp(72000−remaining,0,60), F=nível Flinging, P=0.1F×C+0.1F×F. V=movimento anterior+view normalizado multiplicado por (P, P×0.15F,P). C=0 retorna; C positivo solicita movimento final V+(0,(onGround?0.2F:0)+0.1F×F,0). C<10 e client pulam som, desgaste, ondas e ataque direto, não movimento. Ramo servidor elegível pede som ORTHOLANCE_WAVE e desgaste 1.

B=C/5 (inteiro); normal tenta 2B ondas, lifespan 3+trunc((1−i/B)×3), yaws base ±(60−15i), escala basal 1, espera 0. Second Wave tenta 2×max(1,B−1) adicionais com espera 8. Tsunami substitui B por 5, tenta uma onda lifespan20, escala5, espera2, pula ambos laços. [Flinging](../enchantments/flinging.md), [Tsunami](../enchantments/tsunami.md), [Second Wave](../enchantments/second-wave.md) e [Sea Swing](../enchantments/sea-swing.md) documentam geometria, offsets e downstream. Retornos de spawn ignorados.

Ataque direto: AABB entre posição do usuário e posição+V×B, inflada por 1D; LivingEntity, exclui aliados e próprio usuário, exige LOS. mobAttack(usuário) com soma de amount dos modificadores MAINHAND ATTACK_DAMAGE via ACCompat.attackDamageBonus; não equivale ao dano final ou atributo total. @824 hurt (retorno descartado), @830 stopRiding mesmo se dano falha. Movimento final @866. WaveEntity tem dimensões-base 0.9×0.9, escaladas por waveScale; sua caixa de dano inflada 0.5 por eixo não é a AABB de ataque direto. Ver contratos dos encantamentos para owner, vida, impacto e filtros; não replicar wave tick ou dano.

Melee hurtEnemy encaminha acHurtEnemy: pede desgaste 1 MAINHAND e, Sea Swing positivo, cria uma onda lifespan5 em (atacante.x, alvo atingido.y, atacante.z), yaw a partir da visão. A altura usa a vítima original, não a altura do atacante (Sea Swing, @40–54). Não há gate explícito de lado nesse corpo. mineBlock pede desgaste 2 para destroySpeed !=0. Weapon attributes empacotado declara parent bettercombat:lance (SHA `69fc57cd5ba21e6a471af953dda526dd1f6e5c93fc14e15ff4de5844f9724edd`); não certifica Better Combat instalado/ativo nem alcance externo. Aquisição por barter Deep One Knight, weight10 (ver Tsunami); ausência de receita no recorte de filename não prova impossibilidade.

## Integração e pendências

Sem mana, cooldown fixo, distância percorrida ou débito de XP próprios demonstrados. Candidatos conceituais: impulso, carga, onda, dano e desgaste; limites reais de engine/Better Combat, owner/lifecycle completo de onda e liquidação de custo ainda não fechados neste contrato de arma. Não reexecutar release/hit, ampliar AABB sem budget ou creditar Mastery por tentativa.

## Localizadores de evidência

Classfile SHA-256 `996b208a60f2c26c275e60e5d0e3a2fd0090cfb0ba1687907cac242de9a17d09`.

| Método e descritor | Instruções | Code SHA-256 |
|---|---:|---|
| `<init>(Lnet/minecraft/world/item/Item$Properties;)V` | 30 | `af6f5fea728f38268b4d857741f77f205560d3d4775b97832dc5604fe31d4d5b` |
| `getUseAnimation(Lnet/minecraft/world/item/ItemStack;)Lnet/minecraft/world/item/UseAnim;` | 2 | `8cc2d19c6b9a7fea4e1998f92ff83a6b941bfda472caf1d1aeabb5b6159b45bb` |
| `acModifiers(Lnet/minecraft/world/entity/EquipmentSlot;Lnet/minecraft/world/item/ItemStack;)Lcom/google/common/collect/Multimap;` | 8 | `713afd60cedfafa0d4efcf1c6c587065448336750da17a8cb3a581aefdd14fa4` |
| `getDefaultAttributeModifiers(Lnet/minecraft/world/item/ItemStack;)Lnet/minecraft/world/item/component/ItemAttributeModifiers;` | 8 | `f95dc42065c9c3b0c91e41b41a56b453158e436c52477e4af0c2b3dc4f4988ef` |
| `getEnchantmentValue()I` | 2 | `95ef737cd8a13db65e3eb3c18e8816a5179dcbdf341309522ab00e95d5aae6d2` |
| `getUseDuration(Lnet/minecraft/world/item/ItemStack;Lnet/minecraft/world/entity/LivingEntity;)I` | 2 | `22adfa93c1990e86b181cc4c4f00dd351a08b5f49eea2bf5c8ec101dcd815cba` |
| `releaseUsing(Lnet/minecraft/world/item/ItemStack;Lnet/minecraft/world/level/Level;Lnet/minecraft/world/entity/LivingEntity;I)V` | 435 | `7907f2c2548c0a0293292f1bf11117d4fbf259a48352cfea26841d16dc08404a` |
| `use(Lnet/minecraft/world/level/Level;Lnet/minecraft/world/entity/player/Player;Lnet/minecraft/world/InteractionHand;)Lnet/minecraft/world/InteractionResultHolder;` | 20 | `2328ae75bbaf879ac36a72f701f642dccd474ebead27baeb26bb755312d40f8b` |
| `hurtEnemy(Lnet/minecraft/world/item/ItemStack;Lnet/minecraft/world/entity/LivingEntity;Lnet/minecraft/world/entity/LivingEntity;)Z` | 6 | `ac802930f911f185c2f28a5af886cde2b6f6eecd12b5f2389ebfb2a436057161` |
| `acHurtEnemy(Lnet/minecraft/world/item/ItemStack;Lnet/minecraft/world/entity/LivingEntity;Lnet/minecraft/world/entity/LivingEntity;)Z` | 49 | `21f2dd419fc5ca2885ebdc7ea2867ce3e099c036e84c6988515696ba5f52e381` |
| `mineBlock(Lnet/minecraft/world/item/ItemStack;Lnet/minecraft/world/level/Level;Lnet/minecraft/world/level/block/state/BlockState;Lnet/minecraft/core/BlockPos;Lnet/minecraft/world/entity/LivingEntity;)Z` | 15 | `8b8b5c3f4c19c992507be2f913e34fc65fecceb7178b6e0f2c801f1763cd880d` |
| `initializeClient(Ljava/util/function/Consumer;)V` | 6 | `e5b472f09c165b99fddb1ca278e23b470a76c5387449ced55e02919ea752a6c3` |
| `lambda$getDefaultAttributeModifiers$0(Lnet/minecraft/world/item/ItemStack;)Lnet/minecraft/world/item/component/ItemAttributeModifiers;` | 4 | `184a9946f83c46d04cb26217e65639c42c1b91aa3974bec2b0b665c9c004d21c` |

## Reconciliação de evidências e fronteiras — aprofundamento da arma

Reuso de [Flinging](../enchantments/flinging.md), [Tsunami](../enchantments/tsunami.md), [Second Wave](../enchantments/second-wave.md), [Sea Swing](../enchantments/sea-swing.md) e [manifesto estático de WaveEntity](../EXACT-SEA-SWING-STATIC-1.0.10.md). Não reclassificar os quatro encantamentos nem criar uma nova raiz. WaveEntity class SHA-256 `93fdaee0239cc4985b351a6c2ac1edd23a51cf0088cb1172f983d0f869d9e42e`.

- O ataque direto consulta LivingEntity em AABB inflada 1D, exclui próprio usuário/aliados e exige LOS; não possui filtro próprio Deep One. Dano solicitado via mobAttack e soma dos amounts MAINHAND; stopRiding ocorre após hurt mesmo se falso. Não confundir o vetor V, que inclui movimento anterior, com alcance fixo.
- A onda usa outra fonte (`mobProjectile(onda, campo owner)`), AABB própria inflada 0.5D, exclui aliados, DeepOneBaseEntity e owner/aliados quando conhecido; não demonstra LOS ou dedupe próprio por vítima. Defina A=getSlamAmount(1F), S=2A+1+waveScale: dano solicitado S+1; knockback solicitado 0.1D+0.5D×S. Escala normal 1: 3+2A de dano e 1.1+A de knockback; Tsunami escala 5: 7+2A e 3.1+A. Hurt booleano descartado antes de slam/knockback; não constitui recibo de dano.
- Defaults sincronizados: SLAMMING=false, LIFESPAN=10, WAITING_TICKS=0, Y_ROT=0F, WAVE_SCALE=1F. Escala altera dimensões; waiting positivo retorna cedo e só decrementa no servidor. Tick pede ataque no ramo servidor, gravidade condicional −0.04, arrasto 0.9 e multiplicador pós-movimento (0.99,0.98,0.99). O contador de vida e slam condicionam descarte; duração solicitada não é duração efetiva.
- NBT próprio salva Owner UUID (se presente) e Lifespan; não salva waiting/scale/slam nesses overrides. Getter resolve UUID no ServerLevel, mas attackEntities lê campo owner diretamente. Risco de alteração de targeting e autoria após reload, requer QA.
- Desgaste do release: ACCompat.hurtAndBreakUsedHand seleciona MAINHAND/OFFHAND pela mão de uso; melee pede MAINHAND. Uma solicitação por uso elegível, não por onda ou vítima. Nenhum reembolso ligado a spawn aceito demonstrado. Flinging modifica movimento; não multiplica diretamente o dano. Tsunami pula a consulta de Second Wave.
- Aquisição: barter Deep One Knight, weight 10, recurso `data/alexscaves/loot_table/gameplay/deep_one_knight_barter.json`, SHA-256 `57c4a14e6a92f963e726ed92136034a091bdf8929398e8ba2b9d94a6c302c818`; não representa chance percentual. Exclusividade Tsunami/Second Wave declarativa. Nível Flinging lido sem clamp próprio; não assumir máximo do JSON como clamp runtime.

### Coleta complementar

[Sonda read-only](../../../../../docs/qa/alexscaves_1010_ortholance_engine_probe.py) e [workflow](../../../../../.github/workflows/alexscaves-1010-ortholance-engine.yml): pinam publisher e distribuição NeoForge 21.1.250, reutilizam ClassReader/projection e provas anteriores, selecionam todos os métodos próprios de OrtholanceItem/WaveEntity e consumidores de atributos, desgaste, dano, LOS, movimento, entidade, aquisição de owner e registro de onda. Dois relatórios devem ser idênticos; digest ainda não observado. A seleção de helpers da engine é delimitada e não certifica runtime transformado. Nenhum certificado ou contador promovido nesta coleta. `NOT_CERTIFIED / NO_MUTATION / fail-closed`.
