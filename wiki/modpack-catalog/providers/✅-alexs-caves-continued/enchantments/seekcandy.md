# Seekcandy — aquisição e perseguição de alvo pela Sugar Staff (Alex's Caves Continued 1.0.10)

**Estado do contrato técnico individual:** ✅ `STATIC_TECHNICAL_CATALOG_ONLY` / `SHA_EXACT_BINARY_BEHAVIOR`, **condicionado à verificação de CI da PR**. **Hook mutador:** `NOT_VERIFIED`; **QA física:** `NOT_TESTED`; **integração:** `NO_MUTATION` / `fail-closed`. Este certificado delimita o fluxo nativo de `SugarStaffItem`, `SeaStaffItem.getClosestLookingAtEntityFor` e `SpinningPeppermintEntity`. Não certifica um provider completo, mapa de todos os addons, comportamento efetivo de dano/target ou API para perks.

## 1. Identidade, versão física e descrição

| Campo | Evidência |
|---|---|
| Mod / ID | Alex's Caves Continued / `alexscaves` |
| Ambiente | Minecraft 1.21.1 · NeoForge · Java 21 |
| JAR instalado | `alexscaves-1.0.10-neoforge+1.21.1.jar`, 75.279.314 bytes |
| SHA-1 | `6960b299a39a039ac8a5eb9b07be4ad0e3e0a570` |
| SHA-256 | `36ae0a3cbd028df466a37c671ba2fdf021c060ca1c9c1c32e9f2e95bffae0e7c` |
| Enchantment / registro | `alexscaves:seekcandy` · `ACEnchantmentRegistry.SEEKCANDY` |
| Recurso | `data/alexscaves/enchantment/seekcandy.json` — 361 bytes, SHA-256 `7e564925928b90368d9042f1b722f89464bfbd708abf69ced0d785b5871f0a74` |
| Item tag | `#alexscaves:enchantable/sugar_staff` → `alexscaves:sugar_staff` · SHA-256 `eb9f84b401224aba54ba91a239e4dd5b775d82012cecf9b03e8f9608e12b11fc` |
| Descrição nativa em `en_us` | Peppermints criados pelo bastão procuram entidades observadas pelo atacante (*paráfrase*). O seletor real abaixo tem restrições que a descrição não explicita. |

**Dados declarativos exatos:** `weight=2`, `max_level=1` (I), `min_cost={base:1,per_level_above_first:16}`, `max_cost={base:41,per_level_above_first:10}`, `anvil_cost=4`, `slots=["mainhand"]`. Não há `exclusive_set` no JSON instalado. Esses são metadados de aquisição/compatibilidade do encantamento, **não custos de mana, escalas de dano ou tempo de recarga do cast**.

**Prova individual:** [manifesto exato selado](../EXACT-SEEKCANDY-STATIC-1.0.10.json), [relatório de certificação](../EXACT-SEEKCANDY-STATIC-1.0.10.md), [sonda de JAR read-only](../../../../../docs/qa/alexscaves_1010_seekcandy_static_probe.py) e [regressões semânticas](../../../../../docs/qa/alexscaves_1010_seekcandy_cards_test.py). O [corpus de Multiple Mint](../EXACT-MULTIPLE-MINT-CONTRACT-1.0.10.json) já contém âncoras completas dos principais métodos da mesma versão e é confrontado pelo probe. Nenhum valor foi extrapolado da fonte adjacente pública 1.1.1.

## 2. Grafo técnico, escopo e evidência

A inspeção de **1.555 classfiles** do publisher encontrou a referência binária direta `SEEKCANDY` apenas em `ACEnchantmentRegistry.class` e `SugarStaffItem.class`. Isso é um censo de referência compilada, não um teorema sobre datapacks, reflexão ou mods externos.

| Classe / assinatura | Papel e SHA-exato do método compilado |
|---|---|
| `SugarStaffItem.use(Level,Player,InteractionHand)` | Produtor de cast/target; 226 instruções, digest `76ba0a5bbf219e25f809c5e4d512fab3503f3e4dd99721e628787a7bde37d475` |
| `SeaStaffItem.getClosestLookingAtEntityFor(Level,Player,double)` | Seleção de alvo reutilizada; 119 instruções, digest `9c5f594f399ca3ace5b9d65ad5f4db7f53ddd5e01d1c4654bd951bdaf1a04306` |
| `SpinningPeppermintEntity.tick()` | Movimento, resolução do alvo e ciclo de vida; 373 instruções, digest `acf4390aed5a2b3f26af31e982ccabec5a0d245d8bea5c594344e4d299f21937` |
| `SpinningPeppermintEntity.hurtEntities()` | Filtros de dano, knockback e descarte; 90 instruções, digest `f7580b92bc9585191e0b831f5aeb332e4a94ad95cfc173a74a157d543858dbfc` |
| `SpinningPeppermintEntity.getSeekingEntityId/setSeekingEntityId` | Leitura/escrita de `SynchedEntityData.SEEKING_ENTITY`; default -1 |
| `SpinningPeppermintEntity.getOwner/setOwner` | Owner de instância e UUID; recuperação lazy no `ServerLevel` |
| `SpinningPeppermintEntity.addAdditionalSaveData/readAdditionalSaveData` | NBT próprio, tempo restante, geometria e Owner; **não grava SeekingEntityId** |
| `ACCompat.enchantLevel/addCooldown/hurtAndBreakUsedHand/hurt` | Abstração nativa para nível, cooldown de item, desgaste e dano |

Todas as classes têm hashes de classfile independentes no manifesto, assim como os métodos selecionados. A inspeção compara **todas as âncoras existentes** dos métodos com o manifesto Multiple Mint na mesma versão e sela os digests completos do `javap`. A referência antiga não certificava Seekcandy por associação: este consumidor recebe validação individual.

## 3. Ativação e aquisição inicial de alvo

`SugarStaffItem.use` obtém a stack de `Player.getItemInHand` e guarda o corpo do cast atrás de `!Level.isClientSide()` (@7–11). Ainda antes do teste de agachamento, chama `SeaStaffItem.getClosestLookingAtEntityFor(level,player,32D)` (@25–33). O argumento **32D pertence à seleção**, não a um raio máximo de voo dos peppermints. `isShiftKeyDown()` escolhe o cast de Hex quando verdadeiro (@35–37), onde `SEEKCANDY` não é consumido; somente o ramo não agachado emite peppermints a partir de @186.

A rotina de aquisição usa `getEyePosition`, `getLookAngle`, `ClipContext(Block.VISUAL, Fluid.NONE, player)` e `Level.clip` (@3–43). Possui um ramo de `EntityHitResult` e um ramo alternativo que usa a posição de impacto, constrói AABB centrada em `±0.5D`, aplica `inflate(15D)` e depois `inflate(32D)`, consultando `Level.getEntitiesOfClass(LivingEntity.class,...)` (@114–174). O filtro exige entidade distinta do jogador, sem alianças em ambas as direções, do tipo `Mob` e com `Player.hasLineOfSight` (@206–247). Entre candidatos elegíveis, compara distância **quadrática ao ponto de impacto do raytrace** (@250–275). O ramo `EntityHitResult` também exige `Mob` e linha de visão (@45–111).

Portanto a descrição localizada sobre «qualquer entidade observada» **não significa que qualquer LivingEntity/Player seja selecionável**, nem certifica perseguição física em 32 blocos, linha direta de tiro ou aquisição em qualquer condição de mundo.

## 4. Ativação de Seekcandy e efeitos no produtor

O Peppermint Cast solicita `N=3+level(MULTIPLE_MINT)` instâncias, independentemente do nível de Seekcandy (@186–212). Cada entidade é criada com posição inicial em `player.position()+(0,0.45×getBbHeight(),0)` (@215–257). O ramo de `PEPPERMINT_PUNTING` pode selecionar `setStraight(true)`, yaw de direção e `setSpinSpeed(8F)`, cooldown `20`; sem Punting, seleciona `setStraight(false)`, yaw alternativo, `setSpinSpeed(12F)`, cooldown inicialmente `80` (@262–339).

**Gatilho exato de Seekcandy:** `target != null` (@342–344) **e** `ACCompat.enchantLevel(stack,SEEKCANDY)>0` (@347–355). Se os guardas passam, **para cada peppermint** o produtor:
- chama `setSeekingEntityId(target.getId())` (@358–365);
- solicita `setSpinSpeed(50F)` (@368–372);
- redefine o cooldown local do cast para **50 ticks** (@375–377).

Isso **não aumenta N**, não cria novo cast nem confirma a velocidade final. A stack do item, o som, `setSpinRadius(3.5F)`, `setOwner(player)`, `setStartAngle(i×360/N)` e `setLifespan(80)` continuam no mesmo pipeline nativo (@379–412). `Level.addFreshEntity` é chamado para cada tentativa (@418) e seu retorno booleano é ignorado (@421). Ao fim do loop, o método solicita `ACCompat.addCooldown(player,stack,cooldown)` (@461) e `ACCompat.hurtAndBreakUsedHand(stack,1,player)` (@468). **Seekcandy não adiciona cobrança própria por projétil nem transforma tentativas em spawns aceitos.**

## 5. Consumidor: perseguição, rotação, raio e movimento

O consumidor `SpinningPeppermintEntity.tick` faz `Entity.tick`, inicializa `despawnsIn` do `getLifespan()` caso esteja -1, decrementa um por tick quando positivo e solicita `discard()` no servidor quando esgotado (@0–62). Logo após, **sobrescreve `setSpinRadius(3F)` e `setSpinSpeed(7F)` em cada tick** (@62–71). Assim, os valores iniciais **3.5F** e **50F** do produtor não equivalem a raio ou velocidade persistentes da entidade.

Para `owner instanceof Player`, `getSeekingEntityId()` lê o ID sincronizado, cujo default é **-1**; se diferente, `Level.getEntity(id)` tenta resolver o alvo (@323–380). Se um alvo existe, a entidade forma vetor `target.getEyePosition()-peppermint.position()`, normaliza apenas quando seu comprimento supera **1D**, e reescreve o centro orbital para `peppermint.position()+vetor` (@382–453). Sob esse mesmo caminho, o raio é solicitado como

`spinRadius = 4F - 4F × min(1F, tickCount/30F)`

(@418–440), podendo chegar a zero após 30 ticks **se esse ramo continuar elegível**. Com ID inexistente ou alvo não resolvido, a entidade segue o centro derivado da posição do jogador (@460–462). `owner instanceof Mob` tem caminho separado para target de Mob, **sem necessariamente depender do enchantment Seekcandy**.

**Bifurcação importante:** `isStraight()` é avaliado somente depois do cálculo do centro (@465–469). Em modo straight (como Punting positivo), a física do caminho @482–599 usa rotação/yaw, velocidade e `move(SELF,delta)`, sem utilizar o centro orbital atualizado naquele trecho. Já no ramo não-straight (@602–733), o centro e raio alimentam `destino = centro + vetorCircular`; a entidade solicita `deltaMovement=(destino-posicao)×(0.05D×getSpinSpeed())` e aumenta o spinAngle com getSpinSpeed. **Logo, `setSeekingEntityId` não garante homing funcional quando o mesmo peppermint está em modo straight.** A interação exata Seekcandy+Punting precisa de QA física; não a converter em uma perk de mira automática sem hook verificável.

O `tick()` termina chamando `hurtEntities()` (@736–737). Não presumir que todos os efeitos aceitos ocorram apenas por esse consumer, que exista um raio universal fixo ou que `50F` se mantenha sem sobrescrita.

## 6. Dano, targeting efetivo, owner e descarte

`hurtEntities()` constrói `DamageSource.mobProjectile(peppermint,owner)` usando **o campo `owner` diretamente** (@5–17), e busca `LivingEntity` na AABB corrente do projectile (@20–27). Exclui aliados segundo `isAlliedTo`, owner nulo ou idêntico, e tem condições específicas de friendly fire envolvendo `LicowitchEntity.isFriendlyFire` (@59–140). Para um candidato elegível, solicita `ACCompat.hurt(entidade,damageSource,3F)` (@140–148). **Somente quando o retorno é verdadeiro**, registra hit, solicita knockback com força **0.30000001192092896D** (@151–178). Ao final do loop, se houve **qualquer hit aceito** e `getSeekingEntityId()!=-1`, solicita `discard()` (@184–197). Isso não comprova que o hit foi no alvo originalmente adquirido e não multiplica o dano por nível de Seekcandy.

O `getOwner()` recompõe sob demanda uma referência a LivingEntity a partir de `ownerUUID` apenas em `ServerLevel`, mas o dano usa `owner` diretamente. Questões de crédito de Mastery/XP, reentrada em mundo e compatibilidade PvP exigem validação física; não presumir que salvar UUID garante todos os filtros após reload. O `Level.getEntity(id)` de Seekcandy é por ID numérico da entidade, sem UUID do alvo salvo nesse consumer.

## 7. Persistência, networking e diferenças após reload

`SEEKING_ENTITY` é um `EntityDataAccessor` sincronizado com inteiro default **-1** (método `defineSynchedData`). `getSeekingEntityId/setSeekingEntityId` leem/escrevem a `SynchedEntityData`; **não** constituem API pública segura para mutações por perks.

Os overrides próprios de `addAdditionalSaveData` / `readAdditionalSaveData` gravam/recuperam **DespawnsIn, Straight, Owner (UUID quando existe), AroundX/Y/Z, SpinSpeed, SpinRadius, StartAngle, SpinAngle e Lifespan**. **Não gravam/recuperam `SeekingEntityId`**. O método de leitura ainda usa a chave `AroundZ` duas vezes para os argumentos Y e Z da `Vec3` (@107/@114); isso deve ser tratado como comportamento compilado 1.0.10, não «corrigido» por inferência. O efeito sobre trajetória após reload permanece sujeito ao engine e QA física. O `tick` reescreve speed/radius de qualquer forma.

## 8. Matriz de integração futura: perks, atributos e Mastery

| Aspecto | Contrato nativo rastreado | Limites e riscos |
|---|---|---|
| Gatilho | `target!=null && level(SEEKCANDY)>0` no Peppermint Cast não agachado | Não reexecutar seleção/cast por perk; registro de aquisições deve ser idempotente |
| Número de projéteis | `3+level(MULTIPLE_MINT)` tentativas | Seekcandy **não** aumenta esse número; não criar projéteis duplicados |
| Aquisição | raytrace VISUAL / NONE + AABB e filtros de `Mob`, aliados, linha de visão | Não converter arg 32D em alcance garantido ou permitir dano PvP sem política |
| Alvo | `Entity.getId()` no campo sincronizado `SEEKING_ENTITY` | ID numérico não persistido em NBT próprio; não prometer tracking entre reloads |
| Direção/área | centro orbital e raio de convergência `4-4min(1,tick/30)` | `isStraight()` escolhe outro movement path; raio não é AOE de dano |
| Velocidade | produtor escreve `50F`, tick sobrescreve `7F` | Não prometer speed permanente ou alcance sem observar movimento |
| Dano/owner | `ACCompat.hurt(...,3F)`, knockback 0.3 se aceito, owner capturado | Não multiplicar dano por nível nem creditar XP por spawn/tentativa |
| Cooldown/desgaste | cooldown selecionado **50 ticks** quando alvo+Seekcandy; desgaste único **1** | Cobrança é do item/cast, não por peppermint; efeitos aceitos não comprovados |
| Persistência | campos de NBT e SynchedData são distintos | Não presumir que `SeekingEntityId` sobreviva a unload/reload |
| Hooks mutadores | **`NOT_VERIFIED`** | **`NO_MUTATION`** até API/boundary nativo real e seguro |

## 9. Reprodução, certificação e pendências

Reproduzir pelo workflow `alexscaves-1010-seekcandy-static.yml`: download do JAR publicado, verificação de SHA-1/SHA-256/tamanho, hash exato de recursos e classfiles, **censo de 1.555 classes**, confronto de todas as âncoras do manifesto Multiple Mint com `javap` Java 21, digest completo dos métodos e comparação `--seal` com [o manifesto individual](../EXACT-SEEKCANDY-STATIC-1.0.10.json). Executar também `docs/qa/alexscaves_1010_seekcandy_cards_test.py`, `scripts/catalog/check_perk_ready_indexes.py` e `scripts/catalog/generate_perk_ready_indexes.py --check`.

Certificação limitada ao **contrato estático do fluxo Seekcandy→Peppermint da versão física instalada**. Permanecem **`NOT_VERIFIED`/ `NOT_TESTED`**: hook mutador, QA física client/server, PvP, claim/world safety, alvos com ID reciclado, alterações de datapack, efeitos efetivamente aceitos de `hurt`/spawn, colisões após reload, compatibilidade real com Punting e creditamento de Mastery. Não declarar provider totalmente catalogado nem mover estágios de implementação. O Black Arcana conserva autoridade sobre seu próprio runtime; não duplica pipelines da Sugar Staff.
