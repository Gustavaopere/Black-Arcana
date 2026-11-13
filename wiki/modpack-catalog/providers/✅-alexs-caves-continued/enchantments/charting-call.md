# Charting Call — ampliação condicionada das invocações Magic Conch (1.0.10)

**Estado:** ✅ **contrato técnico estático individual certificado** (`STATIC_TECHNICAL_CATALOG_ONLY` / `SHA_EXACT_BINARY_BEHAVIOR`) para Charting Call no publisher 1.0.10. Identidade, gatilho, famílias, limites de RNG, branches JVM, consumidores, custos, autoria, NBT e riscos foram reconciliados com o JAR. **O potencial erro de `nextInt(0)` permanece um risco estático, não um crash reproduzido.** `physical_qa=NOT_TESTED` · `mutating_hook=NOT_VERIFIED` · `NO_MUTATION`.

Este encantamento modifica o comportamento da única ação semântica [Magic Conch — Summon Deep Ones](../actions/magic-conch-summon-deep-ones.md). Não inaugura spell root, mana, tipo de dano nem runtime próprios; Deep One, Knight e Mage são participantes/variantes da mesma invocação provider-native.

## 1. Identidade e autoridade de versão

- **Mod:** Alex's Caves Continued (`alexscaves`), Minecraft 1.21.1, NeoForge.
- **Encantamento:** `alexscaves:charting_call`; tradução declarada `enchantment.alexscaves.charting_call`.
- **Item declarado:** `alexscaves:magic_conch`, tag publisher `#alexscaves:enchantable/magic_conch`.
- **JAR publisher exato da modlist:** `alexscaves-1.0.10-neoforge+1.21.1.jar`, **75.279.314 bytes**, SHA-1 `6960b299a39a039ac8a5eb9b07be4ad0e3e0a570`, SHA-256 `36ae0a3cbd028df466a37c671ba2fdf021c060ca1c9c1c32e9f2e95bffae0e7c`.
- **Manifesto desta ficha:** [EXACT-CHARTING-CALL-1.0.10.json](../EXACT-CHARTING-CALL-1.0.10.json), selado pela [sonda somente leitura](../../../../../docs/qa/alexscaves_1010_charting_call_probe.py), [8 regressões sintéticas](../../../../../docs/qa/alexscaves_1010_charting_call_probe_test.py) e [workflow publisher](../../../../../.github/workflows/alexscaves-1010-charting-call.yml).
- **Provas anteriores reutilizadas:** [EXACT-TECHNICAL-CONTRACTS-1.0.10.json](../EXACT-TECHNICAL-CONTRACTS-1.0.10.json) e a ficha de Magic Conch; esta ficha individual não replica a certificação da raiz.
- **Certificado causal SHA-exato:** [EXACT-CHARTING-CALL-CAUSAL-1.0.10.json](../EXACT-CHARTING-CALL-CAUSAL-1.0.10.json), gerado pela [sonda read-only JVM](../../../../../docs/qa/alexscaves_1010_charting_call_causal_probe.py), [testes sintéticos fail-closed](../../../../../docs/qa/alexscaves_1010_charting_call_causal_probe_test.py) e [workflow dedicado](../../../../../.github/workflows/alexscaves-1010-charting-call-causal.yml). O manifesto exige o JAR publisher, os hashes dos classfiles e os digests do selo anterior.
- **Clean-room:** `Codx-org/AlexsCavesContinued@523308608422ab8e31974befa7111ecdf495dd37` declara **1.1.1** e não substitui o JAR 1.0.10. Os dados e offsets abaixo vêm do binário 1.0.10 e não são código proprietário incorporado ao Black Arcana.

## 2. Definição do encantamento — dados exatos do publisher

| Campo de `data/alexscaves/enchantment/charting_call.json` | Evidência |
|---|---|
| SHA-256 do JSON | `352ec52d0e21298a921cc10fe5253b0484c0b273adf3fc5713bce046758ccacd` |
| `supported_items` | `#alexscaves:enchantable/magic_conch` |
| `weight` | `10` — peso de encantamento, **não** chance de invocação |
| `max_level` | `4` (IV) |
| `min_cost` | `base=1`, `per_level_above_first=7` |
| `max_cost` | `base=41`, `per_level_above_first=10` |
| `anvil_cost` | `1` |
| `slots` | `mainhand` |
| `exclusive_set` | Não declarado no recurso Charting Call |

A tag `data/alexscaves/tags/item/enchantable/magic_conch.json`, SHA-256 `730151144ab45cb149cf6adfdf5d9cfb69b450238ff126f7f1ac33a0406d2cd8`, contém o item `alexscaves:magic_conch`. Compatibilidade com `lasting_morale` e `taxing_bellow` não se transforma automaticamente em autorização para alterar seus efeitos. Estes outros recursos possuem hashes publishers independentes; Taxing Bellow declara incompatibilidade com Unbreaking e Mending, **não Charting Call**.

Os custos de bigorna/enchanting **não são** mana, cooldown, carga consumida nem custo de reputação. Tabelas efetivas após datapacks/mods e obtenção de nível IV em jogo permanecem não verificadas.

## 3. Origem e seleção do nível na invocação

**Consumer versionado:** `com/github/alexmodguy/alexscaves/server/item/MagicConchItem.class`, SHA-256 `4cfad894baabc9540b09de8df8eaf263952292e9c7cc06f86d288cecfb833ce2`.

**Método:** `releaseUsing(ItemStack,Level,LivingEntity,int)V`; descriptor JVM `(Lnet/minecraft/world/item/ItemStack;Lnet/minecraft/world/level/Level;Lnet/minecraft/world/entity/LivingEntity;I)V`, **211 instruções parseadas**, digest `f8a7f97d8a15e513a06cf81e0c4cb2fde5fad9a100b1a3187a9ab4f4f9dd7894`.

- O método lê o tempo segurado e **somente `charge > 25 ticks`** entra no ramo de custo/cast. O som de liberação antecede o guard; não é prova de summon.
- Debita durabilidade normal **antes** de entrar no guard explícito de servidor `Level.isClientSide @104` / `ifne @107 → 418`. `Taxing Bellow`, se presente, usa seu ramo alternativo de desgaste/reputação; não é efeito de Charting Call.
- Calcula a duração `1200 + 400 × level(LASTING_MORALE)`, referenciada em `@86–101`. **Charting Call não altera essa duração na região auditada**.
- Após o guard de servidor, lê `ACEnchantmentRegistry.CHARTING_CALL @111` e `ACCompat.enchantLevel @114`, guardando um **nível inteiro `L`**. Não há clamp próprio desse `L` ao `max_level=4` no trecho consumidor.
- O método solicita contagens por categoria **antes** dos laços de posicionamento: três chamadas `RandomSource.nextInt(1)` em `@126`, `@138`, `@150`, depois uma ramificação condicionada a `L>0` (`ifle @160 → 223`) com outras três chamadas a RNG. O binário apresenta **seis callsites `nextInt`** nesse método.
- Em cada família há até **99 tentativas de posicionamento**, com contador incrementado para retorno não nulo de `summonDeepOne`; não é número garantido de entidades aceitas. Som, cooldown e stat pertencem ao item nativo.

## 4. Fórmula das três famílias de invocados

Defina `L=level(CHARTING_CALL)`. No ramo base (nível zero), os limites de pedido são **3 Deep Ones / 2 Deep One Knights / 1 Deep One Mage**, pois `nextInt(1)` retorna zero em uma fonte que respeite o contrato usual de `RandomSource`.

No ramo `L>0`, o bytecode constrói:

| Família | Limite inteiro de **pedido**, não spawn aceito | Offsets exatos do RNG |
|---|---|---|
| Deep Ones | `3 + nextInt(max(L−1, 2))` | `Math.max @172`, `nextInt @175` |
| Deep One Knights | `2 + nextInt(max(L−2, 0))` | `Math.max @192`, `nextInt @195` |
| Deep One Mages | `1 + nextInt(max(L−3, 0))` | `Math.max @212`, `nextInt @215` |

**Tabela do intervalo de argumentos RNG (dados estáticos, não resultados testados em jogo):**

| L | Limite de Deep Ones | Limite de Knights | Limite de Mages | Condição crítica |
|---:|---:|---:|---:|---|
| 0 | `nextInt(1)` | `nextInt(1)` | `nextInt(1)` | Base 3/2/1 |
| I (1) | `nextInt(2)` | `nextInt(0)` | `nextInt(0)` | **Limite zero para Knights** |
| II (2) | `nextInt(2)` | `nextInt(0)` | `nextInt(0)` | **Limite zero para Knights** |
| III (3) | `nextInt(2)` | `nextInt(1)` | `nextInt(0)` | **Limite zero para Mages** |
| IV (4) | `nextInt(3)` | `nextInt(2)` | `nextInt(1)` | Limites positivos: pedidos até 3–5 / 2–3 / 1 |

**Risco estático crítico:** `nextInt(0)` tem um argumento inválido para a semântica padrão de RNG bounded. O classfile exato contém a chamada com possível zero; ela é feita **durante a preparação das quantidades**, depois de entrar no ramo de custo, e antes dos laços de posicionamento. A auditoria **não reproduziu uma exceção, crash, encerramento de cast ou consumo parcial efetivo** no servidor/modpack. Evitar registrar um bug de gameplay como confirmado sem execução física em 1.0.10. Os níveis acima de IV, valores negativos e stacks modificados também não foram testados.

**Consequência para perks:** nenhuma perk deve aumentar `L`, substituir limites de RNG, emitir a rotina novamente ou criar summons adicionais usando esta inferência. O risco de execução de `nextInt(0)` e a ausência de hook seguro impedem certificar manipulação de quantidade. A invocação original também não é um contrato de contagem bem-sucedida.

## 5. Posicionamento, identidade e tempo de vida

A rotina `MagicConchItem.summonDeepOne(EntityType,LivingEntity,int)DeepOneBaseEntity` tem **134 instruções**, digest `c355ab39634de12bb46dd45a2286aca99dcacd1843c98c80d4fe6723fbdf6d25`. Os pontos SHA-exatos selecionados incluem `setSummonedBy @234`, `ACCompat.finalizeSpawn @268`, `checkSpawnObstruction @278`, `Level.addFreshEntity @290`, `DeepOneBaseEntity.copyTarget @297`.

- Posição: tentativa com deslocamento X/Z aleatório entre **−10 e +9**, Y inicial **+7**; percorre condições de água/células vazias e exige posição compatível com água ou apoio. Um retorno não nulo não certifica que `addFreshEntity` aceitou o membro.
- Alvo após criação: `copyTarget` preserva target existente ou considera `getLastHurtMob`, senão `getLastHurtByMob`, com exclusões de owner, aliados, tipos Deep One e validade do alvo. Não há um novo cursor/raycast nem área de dano de Charting Call.
- Classe `DeepOneBaseEntity.class`, SHA-256 `185df23946292e403300849222018480a3cc1397ee6d6d60e0b28abc40e97470`. Método `setSummonedBy(LivingEntity,int)V` (**11 instruções**, digest `af63ee72cd7a7cb9c6b4e4c18a505acabe91c29cee1eea133b71ebf13138c4eb`) marca summoned, guarda `summonerUUID` e escreve `summonTime`. O método `tick()V` (**360 instruções**, digest `c516c6be2701165765a41da407bf7205b7e3660429c854c55557b0b2c584bc81`) contém o decréscimo do tempo no servidor e posterior remoção/expiração, documentados na [ficha raiz](../actions/magic-conch-summon-deep-ones.md).
- Persistência publisher da entidade usa `ConchSummoned`, `ConchUUID`, `ConchTime` em save/load. Não é autorização para um adapter editar tags, atribuir outro dono ou despawnar entidades externas.
- O cooldown nativo é `ACCompat.addCooldown(Player,ItemStack,time) @448`, mediado pelo item. Uma condição excepcional anterior pode interferir na chegada à rotina final; **não inferir cooldown efetivo** nem consumo/refund sem QA.

A reputação `−2` do ramo de `Taxing Bellow` e os custos de durabilidade são pertencentes ao cast da Conch. **Charting Call não deve contabilizar créditos de XP/Mastery a partir de tentativas de colocação ou de participantes variantes**, pois isso duplicaria a raiz semântica.

## 6. Matriz de interoperabilidade / perks

| Eixo | Evidência estática | Estado de mutação |
|---|---|---|
| **Quantidade / grupo** | Três limites `nextInt(max(...))`, contagem por família; 99 tentativas por tipo | ⛔ **Bloqueado**: possíveis limites zero e sem hook estável, spawn aceito não certificado |
| **Targeting / retarget** | `copyTarget` na entidade, preferências last-hurt com exclusões | ⛔ Sem mudança de tipo de alvo, alvo remoto, LOS ou filtros sem contrato |
| **Dano / área / range** | Conch não inflige `DamageSource` própria; membros atacam pelo AI nativo e spawnam por offset X/Z | ⛔ Não converter quantidade em hitbox, AoE, dano de summon ou distância de target |
| **Duração** | `1200+400×LastingMorale`; ciclo `summonTime` na entidade | ⛔ Não aplicar o encantamento Charting Call para aumentar tempo, nem reescrever NBT |
| **Cooldown / custos** | `charge>25`, durabilidade/Taxing Bellow, cooldown por item após loops | ⛔ Evitar segundo débito, segundo cooldown, refund ou overwrite do provider |
| **Mastery / progressão** | Um cast com participantes múltiplos, possibilidade de falha no RNG/placement | ⛔ Sem XP por tentativa, entidade ou exceção; exigir evento de settlement e dedupe |
| **Lados / persistência** | Guard de servidor `@104–107` para count/spawn; entidade tem lifecycle próprio | ⛔ Sem alteração client-authoritative, reparo de falha ou replay de invocação |

O **Black Arcana** conserva autoridade sobre seu casting, policies, hazards, persistência e segurança. O **RPG Skill Tree** é somente provider/sibling de progressão, Mastery, atributos e gates conforme contrato explícito. Não introduzir novos handlers em release/cast nem interceptar `RandomSource` por suposição.

## 7. Reconciliação JVM causal e inventário de consumidores

A auditoria específica no JAR exato conferiu **81 métodos declarados** em duas classes: `MagicConchItem` (**9 métodos**) e `DeepOneBaseEntity` (**72 métodos**, incluindo **três declarações abstratas sem bytecode**, registradas como tais e nunca tratadas como métodos executáveis). O classfile `CHARTING_CALL` aparece diretamente no `ACEnchantmentRegistry` e no `MagicConchItem`; esse censo de tokens entre classfiles do artefato não cobre reflection, mixins de outros JARs ou interceptações externas.

| Método nativo principal | Instruções JVM | Branches diretos (`if`/`goto`) | Switches |
|---|---:|---:|---:|
| `MagicConchItem.releaseUsing` | 211 | 20 | 0 |
| `MagicConchItem.summonDeepOne` | 134 | 8 | 0 |
| `DeepOneBaseEntity.setSummonedBy` | 11 | 0 | 0 |
| `DeepOneBaseEntity.tick` | 360 | 46 | 0 |

Os **74 branches diretos** tiveram destinos validados na tabela de offsets do método correspondente. Os hashes e descritores dos quatro métodos foram confrontados com `EXACT-CHARTING-CALL-1.0.10.json`; sete métodos auxiliares (`use`, `getUseDuration`, `copyTarget`, `isAlliedTo`, `getReactionTo` e os dois overrides de NBT) também têm fingerprints individuais e referências relevantes no manifesto causal.

O fluxo de `releaseUsing` mostra a guarda de charge em `@41`, a verificação de servidor em `@104–107`, a leitura de `CHARTING_CALL @111–114`, os três pedidos base `nextInt(1) @126/138/150`, o salto de `L<=0` em `@160` e **três cadeias `Math.max`→`nextInt` em `@172–175`, `@192–195`, `@212–215`**. A sonda verifica também as instruções exatas `isub`, os constantes `2/0/0` e as somas aos limites de pedido. Assim, os argumentos zero para Knights (L=I–II) e Mages (L=I–III) são *contratos estáticos do bytecode*, não resultados de gameplay. Não há evidência de um clamp protetor adicional do consumidor antes dessas chamadas.

A rotina de posicionamento liga `setSummonedBy @234`, `finalizeSpawn @268`, `checkSpawnObstruction @278`, `addFreshEntity @290` e `copyTarget @297`. A entidade salva e lê em seus métodos próprios os campos `ConchSummoned`, `ConchUUID` e `ConchTime`; os respectivos métodos têm **56 e 62 instruções**, hashes `706bb7abc272442901c913e02c65076edce56946458c453dcb59601457df396a` e `8a25d29425e8ee5480ce5c04bb03c534f1ed205cd629c9d2f9a936c94ba30408`. Isso comprova as rotas locais de serialização, mas **não valida fisicamente** reload, atribuição de autoria após retorno ao mundo, aceitação de spawn ou comportamento pós-crash.

**Escopo de certificação:** o contrato estático individual é fechado no recorte observado, inclusive o risco de limites zero. A exceção efetiva do RNG, o encerramento do cast, a aplicação de desgaste/cooldown em casos excepcionais, o comportamento de engines/mixins externos e a QA física continuam não verificados. O risco torna a **mutação de quantidade bloqueada**; não alterar a implementação nativa, contadores, níveis ou parâmetros sem uma API segura e evidências próprias.

## 8. Prova, pendências e contabilização

**Confirmado no exato 1.0.10:** hashes publisher, JSON/limites de enchanting, tags físicas, classfiles, descritores, método `releaseUsing` e seus seis `nextInt`, três `Math.max`, 3 consumidores de summon, rotinas selecionadas de criação, owner e lifetime. O manifesto inicial contém janelas JVM delimitadas; a reconciliação causal adicional certifica os **branches diretos dos quatro métodos selecionados e o inventário de 81 métodos declarados**, mas não reconstrói o CFG interprocedural/de exceções, toda a IA ou os efeitos de terceiros.

**Pendente:** gameplay com Charting Call 0/I/II/III/IV e logs de exceções/RNG, inventário/loot após datapacks, validação de custo/durabilidade/cooldown nos ramos excepcionais, falha de entidade, chunks/bioma, estado por cliente/servidor, PvP/claims, reputação, persistência, múltiplos usuários, dedup de XP, hook/ABI mutadora, colisões e integração com perks. Nada disso foi marcado como `PASS`.

**Estados:** contrato técnico estático individual `COMPLETE_PERK_READY` sob `STATIC_TECHNICAL_CATALOG_ONLY`; JVM/recursos `VERIFIED_EXACT_BINARY_DIRECT_CFG`; `mutating_hook=NOT_VERIFIED`; `physical_qa=NOT_TESTED`; `NO_MUTATION`. A denominação do certificado **não** autoriza perk mutadora, não resolve o risco de RNG e não promove Stage.

**Contabilidade desta certificação:** **+0 novas fichas**, **+1 contrato técnico estático certificado**, **+0 raízes mágicas**, **+0 providers concluídos**. No recorte observado de Alex’s Caves, **36/51 encantamentos** e **64/81 objetos** têm contrato estático certificado; o universo integral do provider continua não comprovado. Próxima ficha parcial na ordem alfabética: `alexscaves:chomping_spirit`.
