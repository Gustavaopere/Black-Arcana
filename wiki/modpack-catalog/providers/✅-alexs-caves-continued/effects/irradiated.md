# Irradiated — irradiação

- Provider: **Alex's Caves Continued** (`alexscaves`), versão instalada **1.0.10**.
- Identidade: `alexscaves:irradiated`, campo `ACEffectRegistry.IRRADIATED`, classe `server.potion.IrradiatedEffect`.
- Autoridade: JAR publisher File **8856293**, 75.279.314 bytes, SHA-1 `6960b299a39a039ac8a5eb9b07be4ad0e3e0a570`, SHA-256 `36ae0a3cbd028df466a37c671ba2fdf021c060ca1c9c1c32e9f2e95bffae0e7c`.
- Contrato estático: **`VERIFIED_EXACT_BINARY`**; hook mutador **`NOT_VERIFIED`**; configuração efetiva **`NOT_VERIFIED`**; QA física **`NOT_TESTED`**.

## 1. Identidade e unidade catalogada

É um **status downstream**, aplicado por itens, alimentos, blocos e entidades; não constitui outro lançamento das oito ações mágicas já catalogadas. `ACEffectRegistry.<clinit>()V @71–85` registra `irradiated`; `lambda$static$3()Lnet/minecraft/world/effect/MobEffect;` instancia `IrradiatedEffect`. Seu construtor `()V @1–6` usa categoria `HARMFUL` e cor decimal `7853582` (`0x77D60E`). A fonte pública pinada `523308608422ab8e31974befa7111ecdf495dd37` declara **1.1.1**; não é autoridade de parâmetros da versão instalada.

## 2. Lifecycle, duração e amplifier

O efeito não possui duração universal: cada produtor constrói `MobEffectInstance`. `ACMobEffect.applyEffectTick(Lnet/minecraft/world/entity/LivingEntity;I)Z @0–7` passa o inteiro recebido diretamente para `tick` e retorna `true`; `shouldApplyEffectTickThisTick(II)Z @0–6` delega diretamente a `shouldTick`. Não há conversão `amplifier+1` nesses wrappers.

`IrradiatedEffect.shouldTick(II)Z @0–33` usa **amplifier bruto** `a`: se `a<=0`, retorna `false`; caso contrário calcula divisão inteira `j=200/a`. Se `j>1`, processa quando `duration % j == j/2`; se `j<=1`, retorna `true`. Exemplos estáticos: `a=1` produz período nominal 200 ticks, `a=2` 100, `a=3` 66; `a>=101` alcança o ramo de processamento a cada chamada elegível. **Amplifier 0 não executa o tick deste efeito**, embora a presença do status continue sendo consumida pelos eventos de cura e AI. Não interpretar nível visual I como um tick a cada 200 ticks.

Não há override próprio de encerramento ou modificador de atributo no efeito; `ACMobEffect.onEffectEnd(Lnet/minecraft/world/entity/LivingEntity;)V` é vazio. Persistência, combinação de instâncias e expiração dependem do ciclo nativo de `MobEffectInstance`; os métodos examinados não implementam um temporizador próprio, projétil ou AABB.

## 3. Dano, exaustão e equipamento

`tick(Lnet/minecraft/world/entity/LivingEntity;I)V @0–83` conta peças Hazmat por `HazmatArmorItem.getWornAmount(Lnet/minecraft/world/entity/LivingEntity;)I` e calcula `s=1F-0.25F*h`, com `h` no intervalo 0–4. O helper verifica os quatro itens exatos nas posições HEAD/CHEST/LEGS/FEET; qualquer armadura genérica não satisfaz essa contagem.

| Peças Hazmat | Dano solicitado por tick elegível | Condição aleatória `nextFloat() < s+0.1F` |
|---|---|---|
| 0 | `1F` | limite `1.1F`, sempre passa para o contrato `[0,1)` de `nextFloat` |
| 1 | `0.75F` | limite `0.85F` |
| 2 | `0.5F` | limite `0.6F` |
| 3 | `0.25F` | limite `0.35F` |
| 4 | `0F` | limite `0.1F`; ainda pode chamar `hurt` com zero |

`Player` sem nenhuma peça recebe `causeFoodExhaustion(0.4F)` **antes** do sorteio (`@14–35`). `RaycatEntity` é excluído do ramo de dano (`@38–42`). Não há guard próprio de lado servidor nem consulta ao tag `resists_radiation` dentro desse `tick`; não exportar as condições dos produtores para este consumidor.

O ramo chama `LivingEntity.hurt(ACDamageTypes.causeRadiationDamage(registryAccess), s)` (`@66–79`), sem usar o booleano retornado. O amplifier controla frequência, não multiplica diretamente `s`. `causeRadiationDamage(Lnet/minecraft/core/RegistryAccess;)Lnet/minecraft/world/damagesource/DamageSource; @0–31` usa o tipo `RADIATION` com `DamageSourceRandomMessages(holder,2)`, sem entidade atacante fornecida. `data/alexscaves/damage_type/radiation.json` declara `exhaustion:0.1`, `message_id:radiation`, `scaling:never`; isso não prova dano final, bypass universal de armadura ou compatibilidade com escolas do RPG.

## 4. Targeting e consumidores de presença

`CommonEvents.acLivingHeal(Lnet/neoforged/neoforge/event/entity/living/LivingHealEvent;)Z @0–48` retorna verdadeiro se a entidade tem o efeito e seu tipo **não** pertence a `ACTagRegistry.RESISTS_RADIATION`; `livingHeal` cancela esse evento com `setCanceled(true) @0–13`. Isso abrange as curas que passam por **LivingHealEvent**, sem filtro próprio de amplifier ou motivo; não é prova de bloqueio de toda alteração de vida.

O tag físico `data/alexscaves/tags/entity_type/resists_radiation.json` enumera Nucleeper, Radgill, Brainiac, Gammaroach, Raycat e Tremorzilla. É dado de datapack substituível; a presença nele não implementa imunidade global à aceitação do efeito. Gammaroach possui ainda seu próprio `canBeAffected(Lnet/minecraft/world/effect/MobEffectInstance;)Z @0–31` rejeitando Irradiated; o predicado `lambda$static$0(Lnet/minecraft/world/entity/LivingEntity;)Z @0–33` seleciona irradiados que não sejam Raycat. Seu `hurt` pode iniciar spray quando o atacante vivo não está irradiado.

`RadiationRemovingFoodItem.finishUsingItem(Lnet/minecraft/world/item/ItemStack;Lnet/minecraft/world/level/Level;Lnet/minecraft/world/entity/LivingEntity;)Lnet/minecraft/world/item/ItemStack; @0–80` verifica status e comida e chama diretamente `setHealth(min(maxHealth, health+ceil(nutrition*1.5F+1)))`. **Não chama `removeEffect` nesse método**; o nome da classe não certifica cura da irradiação. O super mantém a liquidação nativa do alimento.

`RaycatEntity.tick()V` cura `1F` a cada dez ticks quando irradiado (`@139–172`). A absorção concluída cura o gato `10F`, aplica a ele 200 ticks com amplifier anterior+1 (ou 0 se não possuía status), remove a instância da vítima e reaplica com duração restante e amplifier−1 quando o anterior era positivo (`@457–663`). Aquisição prioriza dono irradiado a distância `<20F`, senão o mais próximo entre não-Raycats irradiados em AABB própria inflada `9D` (`@195–377`); são limites dessa AI, não alcance do efeito. `TremorzillaEntity.tick()V @2846–2930` solicita cura `12F*(amplifier+1)` e remove o status. Não copiar essas conversões para jogadores.

## 5. Aplicações, custos e aquisição

O efeito não cobra mana, cooldown ou durabilidade por si. Esses custos pertencem ao produtor. Os locais abaixo fixam os argumentos das aplicações examinadas; não tornam equivalentes seus filtros, áreas ou obtenção dos respectivos itens.

| Produtor exato | Aplicação observada no JAR |
|---|---|
| `RadioactiveItem` / `RadioactiveBlockItem.acInventoryTick` | Sem lado cliente, entidade viva, jogador não criativo, sem status; sorteio `<count*randomChanceOfRadiation*(1-hazmat/4F)`; 1.800 ticks, amplifier 0 (`@0–166`) |
| `UnrefinedWasteBlock.entityInside` | 4.000 ticks, amplifier 0 (`@54–81`); produtor consulta resistência |
| `NuclearFurnaceComponentBlock.entityInside` | 2.000 ticks, amplifier 3 (`@108–136`); produtor consulta resistência |
| `BrainiacEntity.postAttackEffect` | 400 ticks, amplifier 0 (`@12–39`) |
| `NuclearFurnaceBlockEntity.destroyWhileCritical(Z)V` | Nuvem com instância 9.600 ticks e amplifier `getCriticality()`; raio da nuvem `8F`, duração 12.000 ticks (`@371–415`) |
| `RadioactiveOnDestroyedBlockItem.onDestroyed` | Nuvem com instância 9.600 ticks, amplifier 1, raio `2F`, duração 12.000 ticks (`@70–107`) |
| `NuclearExplosionEntity.tick` | Exceto ramo Intentional Game Design, 48.000 ticks; amplifier 1 se `size<=1.5F`, senão 2 (`@646–701`) |
| `RaygunItem.onUseTick` | Após dano aceito, alvo vivo sem resistência: 800 ticks com `radiationLevel` calculado pelo item (`@1054–1157`); não é duração de canalização |
| `GammaroachEntity.tick` | Nuvem com instância 2.000 ticks, amplifier 0, raio `2.3F`, duração de nuvem 200 ticks (`@91–129`) |
| `ACFoods.lambda$static$2/$3` | Radgill cru/cozido constroem respectivamente 2.000/1.000 ticks, amplifier 0; duração não prova aplicação garantida de toda comida |

A duração de uma instância colocada numa `AreaEffectCloud` é o argumento da instância base, não promessa de duração efetivamente recebida de splash/nuvem. Não há poção Irradiated declarada entre as 12 variantes de `ACEffectRegistry` deste artefato. A criação por comando ou outro mod continua possível.

## 6. Integração por perks e fronteiras

Os pontos úteis são: frequência/amplifier no efeito, redução por peças Hazmat, aceitação nos produtores, cura via evento e conversões específicas de entidades. Mudar um deles não altera automaticamente os demais. Um futuro adapter deve preservar autoria do dano, aceitação de `hurt`, tags dinâmicos, authority servidor e comportamento de alimentos; nenhuma assinatura examinada foi homologada como hook mutador do Black Arcana/RPG Skill Tree.

`getCurativeItems()Ljava/util/List; @0–3` retorna lista vazia, mas esse método sozinho não prova que o caminho de cura por leite da versão 1.21.1 o consulta. `PotionColorMixin.ac_irradiated(Ljava/lang/Iterable;)Z @0–55` identifica amplifier `>=4` para a distinção visual azul; a cor não muda a fórmula de dano. `UpdateEffectVisualityEntityMessage` e os renderizadores são consumidores separados; tráfego visual não é prova de settlement de dano.

## 7. Evidência e validação pendente

A [auditoria estática reproduzível](../EXACT-EFFECT-CONTRACTS-1.0.10.md) sela esta ficha, classes e métodos do JAR exato com descritores JVM e offsets. O roster de referências de campos serve para localizar consumidores; as conclusões acima dependem dos corpos examinados, não apenas da existência de uma referência. Os demais contratos completos de armas, AI, alimentos e explosões continuam no escopo aberto do provider.

QA física necessária: amplifier 0 e 1, diferentes durações residuais, quatro peças Hazmat, dano zero, múltiplas fontes, cancelamento de cura, alimentação, absorção de Raycat, conversão de Tremorzilla, unload/reload e reprodução multiplayer. Nenhum desses resultados foi declarado testado no modpack.
