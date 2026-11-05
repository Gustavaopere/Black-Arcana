# Impending Stab — `alexscaves:impending_stab` (1.0.10)

**Contrato técnico estático:** ✅ `STATIC_TECHNICAL_CATALOG_ONLY` / `SHA_EXACT_BINARY_BEHAVIOR`. **Hooks mutadores:** `NOT_VERIFIED`. **QA física:** `NOT_TESTED`. **Integração:** `NO_MUTATION`. O recorte cobre o encantamento e o pipeline delimitado de criação/ataque das dagas; não encerra o equipamento inteiro, Double Stab, Sated Blade ou o universo do provider.

## 1. Identidade e descrição original

- **Provider / versão:** Alex's Caves Continued / `alexscaves`, Minecraft 1.21.1; `alexscaves-1.0.10-neoforge+1.21.1.jar`, CurseForge projeto `1645389`, arquivo `8856293`, **75.279.314 bytes**.
- **JAR SHA-1:** `6960b299a39a039ac8a5eb9b07be4ad0e3e0a570`; **SHA-256:** `36ae0a3cbd028df466a37c671ba2fdf021c060ca1c9c1c32e9f2e95bffae0e7c`.
- **Recurso:** `data/alexscaves/enchantment/impending_stab.json`; SHA-256 `bb3918b0fdf897ad70897952d15094e04d8af905b3e2f2db0d2159b762f5ffbc`.
- **Tag de item:** `data/alexscaves/tags/item/enchantable/desolate_dagger.json`; SHA-256 `c350c3e59d1bbff4d9fd24fa54c96e5fa075682f862c9eba0081c4ef2b97b264`.
- **Descrição literal de `en_us.json`:** “Ghostly dagger attack is delayed and deals increased damage”. Tradução explicativa: o ataque da adaga espectral é adiado e solicita mais dano. A descrição própria não está presente no `pt_br.json` examinado.
- **Produtor:** `server/item/DesolateDaggerItem.class`; **consumidor:** `com/github/alexmodguy/alexscaves/server/entity/item/DesolateDaggerEntity.class`, SHA-256 `f82a3f5f1cc05bbe52dfb7e3742f33c2289cbc37810b069a53b45002cfeb4351`.
- **Provas:** [selo individual](../EXACT-IMPENDING-STAB-CONTRACT-1.0.10.json) e [reprodução](../EXACT-IMPENDING-STAB-CONTRACT-1.0.10.md), reaproveitando [equipamento Desolate Dagger](../equipment/desolate-dagger.md) e [entidade/dano](../damage-types/desolate-dagger.md).

A varredura dos 1.555 class entries por referência ao campo `IMPENDING_STAB` encontrou o registro `ACEnchantmentRegistry`, o item produtor e a entidade consumidora. Isso não exclui reflexão, mixins ou mods externos. A fonte pública `Codx-org/AlexsCavesContinued@523308608422ab8e31974befa7111ecdf495dd37` declara **1.1.1** e serve apenas como corroboração adjacente; os parâmetros abaixo vêm dos bytes 1.0.10.

## 2. JSON, exclusividade e aquisição

| Campo | Valor literal publisher | Limite de interpretação |
|---|---|---|
| `description.translate` | `enchantment.alexscaves.impending_stab` | Chave de tradução |
| `supported_items` | `#alexscaves:enchantable/desolate_dagger` | Tag empacotada contém somente `alexscaves:desolate_dagger` |
| `weight` | `10` | Peso declarado, não chance medida |
| `max_level` | `3` | Limite publicado, sem clamp correspondente no leitor Java |
| `min_cost` | `base=1`, `per_level_above_first=6` | I/II/III: 1/7/13 pelo modelo do JSON |
| `max_cost` | `base=41`, `per_level_above_first=10` | I/II/III: 41/51/61 pelo modelo do JSON |
| `anvil_cost` | `1` | Custo de encantamento, não mana por stab |
| `slots` | `mainhand` | Slot declarado no recurso |
| `exclusive_set` | `alexscaves:double_stab` | Declara exclusividade com Double Stab |

Double Stab não repete esse campo no seu JSON. Isso não demonstra coexistência permitida na engine: a resolução efetiva é do sistema de encantamentos e dos dados carregados. Os corpos Java auditados não revalidam exclusividade, tag, slot ou max_level ao ler a stack. `ACCompat.enchantLevel` devolve o primeiro inteiro cujo Holder corresponde à chave, ou zero; níveis/componentes forçados podem sair do domínio normal.

Impending Stab aparece diretamente nas quatro tags publisher `minecraft:in_enchanting_table`, `minecraft:non_treasure`, `minecraft:on_random_loot` e `minecraft:tradeable`. São declarações de aquisição, não obtenção executada ou tags finais resolvidas no modpack.

O loot `entities/underzealot.json` inclui Desolate Dagger no pool `underzealot_dagger`, um roll, `killed_by_player` e chance sem Looting `0.025`; a chance encantada é linear, base `0.035`, incremento `0.01` por nível acima do primeiro. O advancement observa posse do item, sem provar como a instância foi obtida. Os dados Better Combat empacotados referenciam `parent=bettercombat:dagger`, sem alcance numérico próprio; essa referência não certifica integração carregada de combate.

## 3. Gatilho e duas leituras distintas de nível

O callback `DesolateDaggerItem.hurtEnemy(stack,vítima,atacante)` tem ABI `(Lnet/minecraft/world/item/ItemStack;Lnet/minecraft/world/entity/LivingEntity;Lnet/minecraft/world/entity/LivingEntity;)Z`. Chama `super.hurtEnemy`; somente retorno true solicita `acSpawnDaggers`. Esse retorno de callback não é uma nova confirmação de dano líquido aceito. O corpo não tem guarda própria de lado lógico, permissão, LOS, distância ou exigência de Player; a engine e os sistemas de combate decidem quando o chamam.

**No produtor:** `acSpawnDaggers` lê Impending uma vez antes do loop (`@0–7`) e define, para cada tentativa:

```text
cachedL = enchantLevel(stack, IMPENDING_STAB)
orbitFor = (cachedL > 0 ? 40 : 20) + attacker.random.nextInt(10)
```

**No stab posterior:** a entidade consulta novamente o nível do seu `getItemStack()` (`tick @312–327`) e calcula:

```text
requestedDamage = 2F + 2F * (float)enchantLevel(entityStack, IMPENDING_STAB)
```

| Nível lido, se estável | Contador inicial solicitado `orbitFor` | Dano solicitado no stab |
|---|---|---:|
| 0 — sem encantamento | 20–29 ticks | 2F |
| I | 40–49 ticks | 4F |
| II | 40–49 ticks | 6F |
| III | 40–49 ticks | 8F |

**O atraso não cresce por nível positivo.** I/II/III escolhem a mesma faixa inicial; a magnitude é outra leitura em outro momento. A stack é passada a `setItemStack` sem `ItemStack.copy()` no caller ou setter, que escreve SynchedEntityData. Não presumir snapshot imutável do nível entre produção e stab, nem que o comportamento de sync/reload preserve essa referência em todos os lados.

O loop usa **`1 + level(DOUBLE_STAB)`**, relendo Double Stab a cada comparação. Para nível estável, zero gera uma tentativa e o máximo publicado `1` gera duas; exclusividade do JSON não é rechecagem nesse loop. Impending não aumenta a quantidade por si só. Factory `EntityType.create` não tem fallback local de null; `addFreshEntity` tem o resultado descartado. São tentativas, não entidades/impactos garantidos. Não há deduplicador de cast no callback.

## 4. Targeting, geometria e tempo até o stab

O produtor fornece `targetId=vítima.getId()`, copia a posição do atacante e passa a stack. **Não chama `setPlayerId`.** `TARGET_ID` e `PLAYER_ID` começam em `−1`; getters resolvem IDs inteiros no Level local, sem UUID ou aquisição automática de outro alvo. O método chamado `getPlayer` retorna Entity, sem validar classe Player nesse resolver.

A entidade estende Entity, não AbstractArrow. O registro declara categoria MISC, dimensões **0.6F×0.6F**, velocity updates true e update interval `1`. Impending não altera esses valores nem cria dano em área. O alvo é um ID preatribuído; não existe range de busca autônoma a ampliar por esse nível.

Com alvo resolvido, o tick define noPhysics e calcula movimento usando o **STAB anterior ao incremento servidor**: base `target.position+(0,target.height*0.25F,0)`; reseed de Random por ID da dagger; offset que usa altura/largura da vítima e `1F−STAB`, rotacionado pelo ângulo orbitOffset. Escreve delta `destino−posição`, sem cap próprio de velocidade/distância nesse cálculo. Não é prova de órbita circular uniforme ou contato com a vítima no momento do ataque.

No servidor, se **`orbitFor>0 && target.isAlive()`**, decrementa o contador. Senão, escreve **`STAB=min(STAB+0.2F,1F)`**. Com valor inicial `0`, cinco incrementos chegam a 1; se o alvo morrer mas continuar resolvido, o contador positivo não mantém a espera. As faixas da tabela são contadores iniciais, não duração física total garantida ou uma promessa de espera mínima em todas as situações.

Quando `STAB>=1F`, o ramo servidor solicita o ataque, sem novo teste próprio de distância, LOS, AABB da vítima, aliança, tipo Player, PvP ou colisão por contato. Impending não redefine o tipo de alvo para área, nem dá autorização para atacar entidades protegidas. Com alvo nulo e `tickCount>3`, solicita descarte, sem return imediato; movimento/arrasto continuam nesse corpo.

Após o processamento, move por delta e aplica arrasto `0.8999999761581421D` (`0.9F` alargado). Interpolação, partículas e render usam estado próprio; uma imagem da adaga próxima ao alvo não é comprovação de hit físico. O renderer não lê Impending diretamente para aumentar modelo, hitbox ou dano.

## 5. Tipo de dano, autoria e resultado

No stab, `getPlayer()` é resolvido; se null, a fonte usa **a própria entidade dagger**. A factory `ACDamageTypes.causeDesolateDaggerDamage(RegistryAccess,Entity)` seleciona `alexscaves:desolate_dagger`, cujo JSON publica `scaling=never`, `exhaustion=0.3` e `message_id=desolate_dagger`. A entrada direta `minecraft:bypasses_cooldown` é classificação de dano, não bypass de cooldown de casting. Não mesclar com Dark Arrow só por compartilhar conteúdo de recurso.

`ACCompat.hurt` encaminha a `Entity.hurt` e devolve o booleano. `2+2L` é dano solicitado, antes de mitigação/recusa e consumidores externos; não usa por si só o dano-base da espada, crítico ou velocidade. O acerto primário do melee e o stab posterior são consumidores separados.

Se hurt retorna true, o caminho solicita som e pode consultar Sated Blade, condicionado à fonte resolvida ser Player, nível positivo e saturação `<5`. Esse resultado é saturação, não cura de HP nem custo. O produtor auditado não estabelece o vínculo PLAYER_ID, portanto não se inventa alimentação, crédito de kill ou Mastery ao atacante a partir de `copyPosition`.

**Após a tentativa, `discard @435` é solicitado inclusive quando hurt retorna false.** Não há uma nova tentativa nativa programada para o próximo tick nesse ramo apenas por recusa. Também não há return imediato: rotação/movimento/arrasto posteriores ainda executam. Isso não é um token global contra callbacks reentrantes, nem contagem de impactos medida em jogo.

## 6. Custos, componentes e persistência

A entidade não debita mana, stamina, fome, durabilidade, stack ou cooldown no tick de stab. O item delega o custo do melee à superclasse; seus corpos próprios não somam uma despesa por dagger gerada nem por nível de Impending. O construtor declara durabilidade **360**, tier DIAMOND e raridade DEMONIC. São propriedades/argumentos nativos, não dano total, DPS ou desgaste fixo confirmado da espada.

Reparo adicional aceita Pure Darkness nesse override, sem fallback ao reparo de tier; quantidade reparada e XP de bigorna são externos. Não confundir custo de encantamento no JSON, durabilidade do golpe base e saturação posterior de Sated Blade.

`DesolateDaggerEntity.readAdditionalSaveData` e `addAdditionalSaveData` são corpos próprios vazios. Não serializam localmente target/player IDs, stack sincronizada, STAB, orbitFor ou orbitOffset. A Entity base pode salvar estado genérico; isso não demonstra persistência dos campos customizados. Não garantir atraso, autoria, nível ou reexecução equivalentes após save/reload.

Os setters de IDs, STAB e stack não validam alvo/dono, nível, exclusividade ou domínio seguro. O método `getItemStack` e o campo `daggerRenderStack` têm papéis distintos; a fórmula usa a stack sincronizada, não a stack de apresentação. Mudanças de equipamento/componentes e consumers externos continuam fronteiras explícitas de QA.

## 7. Integração e evidência

| Perk / sistema pretendido | Contrato a preservar | Estado |
|---|---|---|
| Dano / nível | Releitura da stack no stab e fórmula float `2F + 2F × L` | Hook `NOT_VERIFIED`; não aplicar o mesmo bônus ao hit primário sem contrato próprio |
| Atraso / duração | Cache positivo inicial, orbitFor condicionado ao alvo vivo e progresso STAB | Não transformar `40–49` em atraso por nível ou lifetime universal |
| Quantidade / exclusividade | Loop de Double Stab e exclusive_set publicado | Não duplicar o produtor, nem presumir que o corpo rejeita componentes forçados |
| Targeting / área | ID local preatribuído, ausência de busca/AoE e sem novo teste de contato no stab | Nenhum alcance, LOS ou proteção PvP homologados por alterar o nível |
| Autoria / Mastery | PLAYER_ID não preenchido pelo produtor, fallback dagger e retorno de hurt | Não atribuir procs/XP por simples spawn, som ou posição copiada |
| Black Arcana / Enshrouded / RPG Skill Tree | Custo/callback/settlement e persistência nativos | Sem adapter mutador, DamageType novo, Stage ou integração executável promovidos |

O [manifesto individual](../EXACT-IMPENDING-STAB-CONTRACT-1.0.10.json) reaproveita a [prova Desolate Dagger](../EXACT-DESOLATE-DAGGER-CONTRACTS-1.0.10.json), que permanece inalterada. Inclui JSON, registro, métodos/descritores e checkpoints do produtor/consumidor; classes e recursos relacionados não certificam os demais encantamentos ou equipamento inteiro. [Testes semânticos](../../../../../docs/qa/alexscaves_1010_impending_stab_cards_test.py) protegem as leituras em momentos distintos, faixa de espera, dano, autoria, descarte e exclusividade.

**Contabilidade:** uma ficha individual de encantamento; **+0 raízes mágicas novas**. `STATIC_TECHNICAL_CATALOG_ONLY` / `SHA_EXACT_BINARY_BEHAVIOR`; `mutating_hook=NOT_VERIFIED`, `physical_qa=NOT_TESTED`, `NO_MUTATION`, provider integral aberto. Os vinte dossiers parciais anteriores permanecem parciais.

QA física pendente: momento/quantidade de callbacks de combate vanilla/Epic Fight/Better Combat, spawn recusado/null, níveis alterados entre spawn e stab, combinação forçada com Double Stab, alvo morto/descarregado/ID reutilizado, distância/obstáculos, autoria e Sated Blade, dano recusado, reentrada, cliente/servidor e save/reload. Próxima identidade sem ficha na fila: `alexscaves:lasting_morale`.
