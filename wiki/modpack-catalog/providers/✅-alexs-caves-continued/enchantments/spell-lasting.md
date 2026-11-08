# Spell Lasting — duração da Sugar Staff Hex (`alexscaves:spell_lasting`, 1.0.10)

**Certificação:** ✅ contrato **técnico estático individual** `STATIC_TECHNICAL_CATALOG_ONLY` / `SHA_EXACT_BINARY_BEHAVIOR`, restrito ao recurso publisher, ao produtor `SugarStaffItem.use` e ao lifecycle/consumidores da `SugarStaffHexEntity` na versão física 1.0.10. **Hook mutador:** `NOT_VERIFIED` · **QA física:** `NOT_TESTED` · **política:** `NO_MUTATION` / fail-closed. Spell Lasting modifica a duração da ação [Sugar Staff — Hex Cast](../actions/sugar-staff-hex-cast.md), **não** cria um cast independente; não altera o ramo Peppermint.

## 1. Identidade, versão física e descrição

| Campo | Contrato |
|---|---|
| Provider e mod ID | Alex's Caves Continued · `alexscaves` |
| Ambiente instalado | Minecraft 1.21.1 · NeoForge · Java 21 |
| JAR físico e publisher | `alexscaves-1.0.10-neoforge+1.21.1.jar` · **75.279.314 bytes** |
| SHA-1 | `6960b299a39a039ac8a5eb9b07be4ad0e3e0a570` |
| SHA-256 | `36ae0a3cbd028df466a37c671ba2fdf021c060ca1c9c1c32e9f2e95bffae0e7c` |
| Identidade JVM | `ACEnchantmentRegistry.SPELL_LASTING` |
| Recurso | `data/alexscaves/enchantment/spell_lasting.json` · 365 bytes · SHA-256 `839c95095540d2c40624575ad74aada2df482d7b4364d86fd8ebc238593a47dc` |
| Tag | `data/alexscaves/tags/item/enchantable/sugar_staff.json` · 51 bytes · SHA-256 `eb9f84b401224aba54ba91a239e4dd5b775d82012cecf9b03e8f9608e12b11fc` |
| Item elegível | `alexscaves:sugar_staff` |
| Texto publisher `en_us` (paráfrase) | Hexes persistem mais três segundos por nível |
| `pt_br` | Nenhuma chave própria de Spell Lasting no arquivo auditado; esta ficha contém interpretação técnica em português, não tradução oficial |

A [modlist autoritativa](https://github.com/Gustavaopere/neoforge-rpg-skilltree/blob/main/PROJECT-INSTRUCTIONS/modlist/World%20Gen/%E2%9C%85-alexs-caves-continued%20v1.0.10.md) identifica o runtime 1.0.10. A [auditoria original do artefato](../EXACT-1.0.10-ARTIFACT-AUDIT.md) comprova a identidade física; a [sonda individual read-only](../../../../../docs/qa/alexscaves_1010_spell_lasting_static_probe.py) confirmou o JAR, o JSON, a tag, os hashes de classe e os métodos compilados, gerando o [manifesto SHA-exato](../EXACT-SPELL-LASTING-STATIC-1.0.10.json). O repositório público de versão 1.1.1 **não** é fonte numérica desta ficha.

## 2. Aquisição e parâmetros declarativos

| Campo JSON | Valor no JAR 1.0.10 | Significado |
|---|---|---|
| `description.translate` | `enchantment.alexscaves.spell_lasting` | Chave do nome |
| `supported_items` | `#alexscaves:enchantable/sugar_staff` | Tag declarativa que contém Sugar Staff |
| `weight` | **10** | Peso de aquisição; não é chance de dano ou proc |
| `max_level` | **3** (I–III) | Níveis normais do recurso, sem clamp próprio demonstrado no cálculo JVM |
| `min_cost` | base 1; incremento 8 | `1+8(L−1)` → I=1, II=9, III=17 |
| `max_cost` | base 41; incremento 10 | `41+10(L−1)` → I=41, II=51, III=61 |
| `anvil_cost` | **1** | Metadado de anvil, não mana do cast |
| `slots` | `mainhand` | Declaração do encantamento |
| `exclusive_set` / `effects` | Não presentes no recurso | Não estabelece compatibilidade global nem comportamento runtime nulo |

Não confundir custo para obtenção do encantamento com custo por uso. O `SugarStaffItem.use` não valida a tag, o slot ou `max_level` na expressão de duração; usa o inteiro devolvido por `ACCompat.enchantLevel`. Nível forçado/sobrescrito por datapack continua fora da aquisição homologada.

## 3. Gatilho, causalidade e fórmulas

O jogador seleciona deliberadamente **agachar + usar** o Sugar Staff (`SugarStaffItem.use(Level,Player,InteractionHand)`). O ramo é executado no servidor (`Level.isClientSide` no início), cria a `SugarStaffHexEntity` no solo calculado por `ACMath.getGroundBelowPosition`, atribui o owner, define escala e solicita `Level.addFreshEntity` em `@124`. O método segue com a atribuição de lifespan **depois da solicitação de spawn**, `@156–172`, e com cooldown da ação em `@175–180`.

**Expressão JVM certificada:**

`Lifespan = 100 + 60 × ACCompat.enchantLevel(stack, SPELL_LASTING)` **ticks**, gravado por `SugarStaffHexEntity.setLifespan(int)` (`SugarStaffItem.use @158/160/164/167/170/171/172`). O literal 100 é o valor-base, o literal 60 é o acréscimo inteiro por nível. `setLifespan` não recebe fator da escala `HUMUNGOUS_HEX`.

| Nível | Lifespan atribuído | Tempo nominal se 20 ticks/s |
|---|---:|---:|
| Zero / sem Spell Lasting | 100 ticks | 5 s |
| I | 160 ticks | 8 s |
| II | 220 ticks | 11 s |
| III | 280 ticks | 14 s |

A conversão em segundos é nominal, não medição de relógio real/TPS. A fórmula JVM não aplica clamp ao resultado antes de `setLifespan`; **níveis negativos ou fora de 0–3 não estão certificados como seguros**. O publisher limita a aquisição normal até III.

**Outro ramo da mesma arma:** sem agachar, o item gera entidades `SpinningPeppermintEntity`, configuradas com `setLifespan(80)` em `@410–412`; não aplica `SPELL_LASTING` a essas entidades. Perks de duração da Hex não devem estender Peppermints por analogia.

## 4. Lifecycle exato e consumidores downstream

`SugarStaffHexEntity` inicia `despawnsIn=-1` e possui dado sincronizado `Lifespan` com valor-base 100 no registro da entidade. O setter `setLifespan(I)V` altera o dado sincronizado; **não recalcula diretamente o contador**. Em `SugarStaffHexEntity.tick()V` (`@4–49`):

1. Se `despawnsIn==-1`, consulta `getLifespan()` e copia o valor para `despawnsIn` (`@5–17`).
2. Salva o contador em `prevDespawnsIn` (`@20–25`).
3. Se `despawnsIn>0`, subtrai 1 (`@28–42`); caso contrário solicita `discard()` (`@48–49`).
4. O método **continua executando após `discard`**; não há `return` imediato no ramo visto.

No mesmo `tick`, após processar o ramo visual cliente, o método chama `hurtEntities(despawnsIn<5)` em `@285–299`. Assim, o valor de duração determina quantas oportunidades de efeito periódico há e quando começa a **janela final** de `despawnsIn<5`; não é um multiplicador direto de dano. O corpo `hurtEntities(Z)V` já comprovado na auditoria Sugar Staff solicita dano mágico indireto nominal **1F** em janela normal ou **6F** na final e knockback final nominal **0.9F** (ampliado para double). Cada chamada é uma **tentativa**; seleção de vítimas, `hurt` efetivo, armaduras/imunidades, friendly fire e contagem real de hits não são implicitamente certificados pela duração.

O alvo usa `LivingEntity` dentro da AABB atual da Hex e filtro adicional `distanceTo(hex)<=4F`. Exclui alvos aliados/owner; a `LicowitchEntity` emprega a regra própria `isFriendlyFire`. A escala física tem contrato separado, `width = 4F×getHexScale()`, e não é alterada por Spell Lasting; AOE, targeting, largura, knockback, velocidade e projéteis novos são **N/A para o encantamento de duração**, porque ele não introduz esses mecanismos. O `SugarStaffItem.use` cria a Hex com owner, mas `Level.addFreshEntity` retorna booleano cuja aceitação não é validada por esta auditoria.

**Correção importante sobre a contagem de ticks:** o budget de lifespan inicializa no primeiro `tick`, sofre o primeiro decremento nesse próprio tick e o descarte só é solicitado quando o contador já não é positivo no início da iteração seguinte. Portanto os valores 100/160/220/280 são o **budget gravado**, não uma garantia de igual número de chamadas completas ou tempo físico exato.

## 5. Cooldown, custo e outras dimensões

| Dimensão | Contrato estático | Proveniência |
|---|---|---|
| Cooldown do Hex | **100 ticks**, independente do nível de Spell Lasting | `SugarStaffItem.use @178–180` → `ACCompat.addCooldown` |
| Durabilidade por cast | Solicita **1** ponto, não escala com Spell Lasting | `SugarStaffItem.use @464–468` → `ACCompat.hurtAndBreakUsedHand` |
| Mana/stamina própria do Spell Lasting | **N/A** no callback compilado auditado | O encantamento altera `Lifespan`, não o recurso do Black Arcana |
| Alcance de aquisição do Hex | Posição no terreno calculada nativamente | `ACMath.getGroundBelowPosition`; não é alvo radial criado por Spell Lasting |
| Dano / DamageSource | Não modificado diretamente | `SugarStaffHexEntity.hurtEntities` usa `indirectMagic(this,owner)` |
| AOE/hitbox | Não modificado diretamente | `getDimensions` e `hurtEntities` seguem contrato da Hex/Humungous Hex |
| Target count / status | Não definidos por Spell Lasting | Consumidor permanece na Hex; não confundir janela maior com novos efeitos |
| Projectiles / velocidade / orientação | **N/A** como novos objetos do encantamento | O cast Hex conserva o pipeline da entidade original |
| Multiplicador de duração | **+60 ticks por nível** sobre 100 | Fórmula independente do cooldown, durabilidade e escala |

O mesmo Sugar Staff permite o ramo Peppermint com cooldown dinâmico e entidades próprias, mas Spell Lasting não consulta nem altera esses parâmetros na cadeia direta observada.

## 6. Owner, dados sincronizados, NBT e reload

O produtor atribui owner ao objeto Hex no servidor. `SugarStaffHexEntity.addAdditionalSaveData(CompoundTag)` escreve `DespawnsIn` inteiro, `Lifespan` inteiro (lido pelo getter) e `Owner` UUID quando não nulo. `readAdditionalSaveData` lê `DespawnsIn` apenas se a chave existe, sempre obtém `Lifespan` e chama `setLifespan`, e captura `Owner` UUID se presente. O contador salvo permite restituir o **tempo restante**, enquanto a duração nominal do encantamento fica em `Lifespan`.

O campo de escala `HEX_SCALE` **não** é serializado nesses métodos; o campo `owner` em memória e o `ownerUUID` armazenado não têm equivalência automaticamente comprovada após reinicialização. `getOwner()` pode resolver o UUID do servidor, mas o método `hurtEntities` lê o campo de owner diretamente. Persistência de targeting, autoria do dano e aceitação de hits após save/reload: **`NOT_TESTED`**. O NBT da entidade não é fonte de autoridade de mana, XP ou cooldowns do Black Arcana.

O hexadecimal de Spell Lasting opera em entidades já criadas, de modo que uma perk que alterasse somente `setLifespan` **após a primeira inicialização de `despawnsIn`** poderia mudar o dado sincronizado sem prolongar o contador corrente. Esse é um risco concreto de integração, não uma autorização para mutar o provider.

## 7. Grafo técnico e evidência SHA-exata

A sonda percorreu **1.555 classfiles** do JAR SHA-exato: o símbolo direto `SPELL_LASTING` aparece em `ACEnchantmentRegistry.class` e `SugarStaffItem.class`. Isso não prova ausência de reflection, datapacks ou terceiros. No ramo do item, a resolução de nível é via `ACCompat.enchantLevel`, seguida de `setLifespan`; o restante do ciclo usa campo/dado sincronizado sem referenciar o nome do encantamento.

| Classe / método | SHA-256 compilado |
|---|---|
| `SugarStaffItem.class` | `d670f887debdfb95f93a52b0c58b3033154a9aa20777fb8bd2a1673ee1407c3f` |
| `SugarStaffItem.use` · 226 instruções | `76ba0a5bbf219e25f809c5e4d512fab3503f3e4dd99721e628787a7bde37d475` |
| `SugarStaffHexEntity.class` | `39f8d11595654ccebcb78540a2772106f0ae30507490570ac6b2cbe28de8e89c` |
| `SugarStaffHexEntity.tick` · 161 instruções | `7e74eb07baffa9564591754a76e56ec237eee0bbae08e84497cff3bedeeea9fa` |
| `SugarStaffHexEntity.getLifespan` · 7 instruções | `2f6d0e3d2ab32b9eb34e3c5f39beac1690845a2885c89739b93f9155c02f7727` |
| `SugarStaffHexEntity.setLifespan` · 7 instruções | `86ceb63b3ac2cd312739e0937c0a6034dc5bf04bcf9e589e06f2c24461e44578` |
| `SugarStaffHexEntity.hurtEntities` · 88 instruções | `83b41481b0f5fcd819c2ea7590bb244e16954e728ee734f2c22a34d7b7f73ee9` |
| `SugarStaffHexEntity.readAdditionalSaveData` · 24 instruções | `09c94be5b7344f66796c5bf14afc1a884974c844e081f1a2ee75d6f6131f1f50` |
| `SugarStaffHexEntity.addAdditionalSaveData` · 19 instruções | `eea7becd8a33a9d01920a0254f9ffb48563151b1f492fa98ec23cf1833e02d5f` |

O arquivo [`EXACT-SPELL-LASTING-STATIC-1.0.10.json`](../EXACT-SPELL-LASTING-STATIC-1.0.10.json) registra recursos/traduções/classes, 35 âncoras pré-certificadas de `SugarStaffItem.use`, 9 de `Hex.tick`, 11 de `Hex.hurtEntities`, 4 de `Hex.readAdditionalSaveData` e as janelas de bytecode. Os **5 métodos do item** e os **18 da entidade Hex** foram enumerados no JAR; a sonda sela os métodos causalmente selecionados, não exporta implementação de terceiros. [Resumo da prova](../EXACT-SPELL-LASTING-STATIC-1.0.10.md).

## 8. Perks, atributos, Mastery e contrato fail-closed

| Intenção de perk | Interseção com o comportamento nativo | Exigência antes de implementar |
|---|---|---|
| Aumentar duração por atributo/Mastery | `100+60L`, `setLifespan`, `despawnsIn` | Boundary real server-owned no instante correto; sincronizar budget e contador, sem duplicar a entidade |
| Prolongar Hex existente | `setLifespan` não muda `despawnsIn` | Hook de lifecycle, range/clamp, persistência e deduplicação comprovados; `NO_MUTATION` hoje |
| Reaplicar janela final | `despawnsIn<5` → `hurtEntities(true)` | Não introduzir chamadas extras de dano, procs de XP nem contornar aliados/claims/PvP |
| Aumentar área ao mesmo tempo | `HUMUNGOUS_HEX` é outro encantamento | Contrato separado de escala, AABB e cap radial; não associar escala a Spell Lasting |
| Reduzir cooldown/custo | `100 ticks` e um ponto de durabilidade por Hex | Esses valores pertencem ao item/provider, não mudam no callback de Spell Lasting |
| Integrar progressão RPG Skill Tree | Contexto de nível do encantamento, duração e eventos próprios | Usar somente contrato/boundary real; progressão não assume autoridade do cast |
| Mastery por acerto/tick | `hurtEntities` pode ser executado repetidas vezes | XP/proc deduplicados pelo cast/efeito aceito; jamais tratar cada frame/tick como spell novo |

**Não há hook mutador seguro certificado**, mesmo que métodos/setters internos existam. Black Arcana mantém autoridade sobre seu próprio runtime, e Sugar Staff/Hex sobre seu comportamento nativo. A implementação de perks que mutem duração fica **⛔ bloqueada**.

## 9. Validação, reprodução e limites

- [Sonda de auditoria exata](../../../../../docs/qa/alexscaves_1010_spell_lasting_static_probe.py) e [12 testes sintéticos fail-closed](../../../../../docs/qa/alexscaves_1010_spell_lasting_static_probe_test.py).
- [Workflow dedicado](../../../../../.github/workflows/alexscaves-1010-spell-lasting-static.yml) baixa o JAR publisher SHA-exato, executa auditoria Java 21 e confere o [manifesto](../EXACT-SPELL-LASTING-STATIC-1.0.10.json) e os índices; nenhum JAR ou implementação alheia é importado à `main`.
- Reprodução: `python3 docs/qa/alexscaves_1010_spell_lasting_static_probe.py --jar /caminho/alexscaves-1.0.10-neoforge+1.21.1.jar --javap javap --seal wiki/modpack-catalog/providers/✅-alexs-caves-continued/EXACT-SPELL-LASTING-STATIC-1.0.10.json`.

**Escopo limitado:** não prova spawn aceito, tempo real/TPS, comportamento de nível inválido, estado de datapack ativo, tolerância a reload/cliente/servidor, autorização de hooks, PvP, claimed land, mob immunity, persistência de owner/restauração de escala, QA física ou fechamento integral do provider. `mutating_hook=NOT_VERIFIED`, `physical_qa=NOT_TESTED`, `NO_MUTATION`.
