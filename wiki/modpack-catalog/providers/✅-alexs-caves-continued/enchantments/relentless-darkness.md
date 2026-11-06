# Relentless Darkness — `alexscaves:relentless_darkness` (1.0.10)

**Contrato técnico estático:** ✅ `STATIC_TECHNICAL_CATALOG_ONLY` / `SHA_EXACT_BINARY_BEHAVIOR`. **Hooks mutadores:** `NOT_VERIFIED`. **QA física:** `NOT_TESTED`. **Integração:** `NO_MUTATION`. O recorte conclui o encantamento e seus consumidores delimitados no Dreadbow; não conclui os outros encantamentos, factories externas, renderer, protocolo de rede ou provider integral.

## 1. Identidade e descrição original

- **Provider / versão:** Alex's Caves Continued / `alexscaves`, Minecraft 1.21.1; `alexscaves-1.0.10-neoforge+1.21.1.jar`, CurseForge projeto `1645389`, arquivo `8856293`, **75.279.314 bytes**.
- **JAR SHA-1:** `6960b299a39a039ac8a5eb9b07be4ad0e3e0a570`; **SHA-256:** `36ae0a3cbd028df466a37c671ba2fdf021c060ca1c9c1c32e9f2e95bffae0e7c`.
- **Recurso:** `data/alexscaves/enchantment/relentless_darkness.json`, 492 bytes; SHA-256 `94edb103571eba0d0ca503b8a9455d4643a0f414c758b4ca79d49bbcdf9f473e`.
- **Tag de item:** `data/alexscaves/tags/item/enchantable/dreadbow.json`; SHA-256 `f22db4f6335af0cc185f0478c482c3c666a86afa430f06bdabc78ccc662076d5`, contendo somente `alexscaves:dreadbow`.
- **Descrição literal de `en_us.json`:** “Dreadbow fires arrows directly ahead in a continuous stream”. Tradução explicativa: o Dreadbow dispara flechas à frente em um fluxo contínuo. Não há entrada própria no `pt_br.json` examinado; a descrição não define DPS ou frequência física garantida.
- **Produtor:** `server/item/DreadbowItem.class`, SHA-256 `b9cd6e843f923877775e38b89214e8649c10d4d5be704ed9dd377900439d44ae`. **Consumidor convertido:** `server/entity/item/DarkArrowEntity.class`, SHA-256 `089f0a65444078ca42fc1da2d5023384314ef5f5283ddf3fe8484bf31d4136ad`. Prefixo de classes: `com/github/alexmodguy/alexscaves/`.
- **Provas:** [manifesto individual](../EXACT-RELENTLESS-DARKNESS-CONTRACT-1.0.10.json), [reprodução](../EXACT-RELENTLESS-DARKNESS-CONTRACT-1.0.10.md), [equipamento Dreadbow](../equipment/dreadbow.md) e [Dark Arrow](../damage-types/dark-arrow.md).

A busca das classes do JAR por referência ao campo `RELENTLESS_DARKNESS` localizou o registro e o DreadbowItem; não exclui reflexão, transformações ou consumidores externos. A fonte pública `Codx-org/AlexsCavesContinued@523308608422ab8e31974befa7111ecdf495dd37` declara **1.1.1**, servindo apenas como corroboração adjacente. Os parâmetros desta ficha vêm dos bytes **1.0.10**.

## 2. JSON, nível, exclusividade e aquisição

| Campo | Valor publisher | Significado / limite |
|---|---|---|
| `description.translate` | `enchantment.alexscaves.relentless_darkness` | Chave de tradução |
| `supported_items` | `#alexscaves:enchantable/dreadbow` | Elegibilidade declarada do item |
| `weight` | `1` | Peso, não chance de acerto |
| `max_level` | `1` | Apenas I publicado; consumidor usa `L>0` |
| `min_cost` | base `1`, incremento por nível acima do primeiro `20` | Nível I: 1 |
| `max_cost` | base `41`, incremento `10` | Nível I: 41 |
| `anvil_cost` | `8` | Custo de encantamento, não custo por flecha |
| `slots` | `mainhand` | Slot declarado |
| `exclusive_set` | Precise Volley, Dark Nock, Twilight Perfection | IDs `alexscaves:precise_volley`, `alexscaves:dark_nock`, `alexscaves:twilight_perfection` |

`ACEnchantmentRegistry` liga o campo à chave `relentless_darkness`. `ACCompat.enchantLevel` lê o primeiro nível correspondente na stack ou retorna zero, sem clamp próprio a I. Qualquer valor positivo seleciona o mesmo modo; níveis forçados maiores não criam uma escala nativa de dano, quantidade ou velocidade. Exclusividade de dados e guards Java são contratos diferentes: o modo contínuo não revalida os três IDs excluídos em cada tentativa.

As quatro tags empacotadas `minecraft:in_enchanting_table`, `minecraft:non_treasure`, `minecraft:on_random_loot` e `minecraft:tradeable` contêm o ID. A receita `data/alexscaves/recipe/dreadbow.json` usa o padrão `" VS"`, `"P S"`, `" VS"`: 1 Pure Darkness, 2 Vesper Wings e 3 Shadow Silk para um Dreadbow. Isso não garante obtenção do encantamento nem resolução desses dados no pack real.

## 3. Gatilho e separação entre modo, carga visual e cadência

O gate inicial `DreadbowItem.use` aceita início de uso com **creative ou munição não vazia**, guarda o tipo de flecha de apresentação e chama `startUsingItem`. Shaded Respite não participa desse gate. `getUseDuration=72000` é duração máxima declarada de uso, não carga mínima de 72000 ticks; animação BOW. O modo Relentless não instala uma chamada independente de cast ou cooldown.

| Consumidor | `L<=0` | `L>0` |
|---|---|---|
| `releaseUsing` | Pode seguir para a chuva normal, conforme seus outros gates | Retorna antes da salva normal (`@14–20`) |
| `onUseTick` | Não entra no disparo Relentless | Exige Player e `remainingUseTicks % 3 == 0` |
| `getMaxLoadTime` | `40−8×level(DARK_NOCK)` | Retorna `5` |
| Incremento visual em `acInventoryTick` | `UseTime+1` | `UseTime+3`, seguido de reset em outro ramo baseado no valor antigo |

**A cadência não é o limite visual 5.** `onUseTick(Level,LivingEntity,ItemStack,int)V` chama o super, exige Player, consulta `L>0` e testa o **argumento restante** `%3`; não exige `UseTime>=M`, potência de release ou tempo transcorrido mínimo nesse corpo. Não prometer o instante do primeiro disparo nem uma taxa de DPS/segundo a partir desse módulo. Alterar duração/callbacks pode mudar a fase do teste restante.

O callback de inventário está ligado via `ACTickingItem`/`ItemStackTickMixin`; suas escritas próprias de carga estão no ramo **cliente**. Captura `oldUseTime`; enquanto usando e `old<M`, escreve `old+3` com Relentless. O reset usa **o valor capturado antes do incremento**, quando `old>=M`, e escreve zero. Não é um clamp de `newUseTime` a 5. `getPullingAmount` e interpolação alimentam apresentação, não autorização nem contagem de disparos no servidor.

Twilight Perfection pode ter outros consumidores de janela cliente quando componentes externos forçam combinações; o corpo de `onUseTick` não consulta Precise Volley ou Twilight, não lê `PerfectShotTicks` para disparar e não chama `setPerfectShot`. Uma animação ou tag positiva não comprova tiro perfeito ou dano aceito no modo Relentless.

## 4. Projéteis, direção, quantidade e targeting

O callback seleciona munição e calcula a elegibilidade Shaded Respite: nível positivo e `!DarknessIncarnateEffect.isInLight(player,11)`. No ramo elegível, stack de munição vazio pode ser substituído por flecha comum. `createArrow` usa o ArrowItem selecionado ou a factory de `Items.ARROW` e pode depender de vanilla/outro mod. O callback não repete o gate inicial de munição, não chama `stopUsingItem` por falta dela e não tem o retorno antecipado de null do release normal. Não declarar disparos gratuitos ou criação sempre válida a partir desse fallback.

`isConvertibleArrow` exige `instanceof Arrow` e `getColor()==−1`, não um teste de ID `minecraft:arrow`. A decisão de conversibilidade é capturada antes do loop:

| Parâmetro | Conversível | Não conversível |
|---|---|---|
| Iterações solicitadas | `1+nextInt(2)`: 1 ou 2 | 1 |
| Entidade usada | Novo `DarkArrowEntity(level,player)` em cada iteração | Protótipo da factory do ArrowItem |
| Dano configurado pelo item | `setShadowArrowDamage(2F)` | Não recebe essa propriedade |
| Tiro perfeito | Não chama setter; default próprio de DarkArrow é false | Não aplica a duplicação do release perfeito nesse corpo |
| Direção | `player.getViewVector(1F)` | A mesma |
| Speed solicitado | `4F+3F×random`, nominal `[4,7)` | O mesmo |
| Inaccuracy | 0.5F na primeira; aumenta 2F após cada iteração, ficando 2.5F na segunda | 0.5F na única iteração |

A posição recebe jitter nominal **[−0.5,0.5)** por eixo em relação à posição inicial da entidade de flecha. Não usa o centro elevado, a caixa de chuva 16×4×16 ou os raycasts `128p`/`42p` do release normal. Neste modo, a direção é o olhar, sem lock persistente de entidade ou raio próprio de AoE. `getDefaultProjectileRange=64` é metadado da arma, não alcance máximo certificado de voo.

Antes da possível conversão, o objeto atual recebe `pickup=ALLOWED`; a conversão o substitui por um DarkArrow novo. Após solicitar `addFreshEntity`, cujo booleano é descartado, recria outro protótipo e o marca `CREATIVE_ONLY`; no início de outra iteração ele recebe ALLOWED novamente. Isso também ocorre após a última tentativa. Não inferir aceitação de spawn, recuperação de cada seta convertida, política de loot ou custo por hit desses passos.

O DarkArrow declara dimensões **1.1F×0.5F**, sem escala por nível de Relentless. Dimensões de entidade, modelo visual e alcance de voo são distintos; para flechas não convertidas, a entidade externa conserva suas próprias propriedades. Movimento/colisões são herdados de AbstractArrow, com intervenções nativas do provider. Trocar target→área, homing, tamanho, alcance ou filtros PvP não é uma consequência de ativar esse nível.

## 5. Dano, autoria e ciclo de vida

O impacto próprio de DarkArrow lê `shadowArrowDamage`, multiplica por 2 somente se a flag perfeita estiver true, constrói `alexscaves:dark_arrow` e solicita `ACCompat.hurt`. O ramo Relentless escreve **2F** e não marca perfeito: esse é um pedido de dano-base armazenado, não dano líquido, multiplicação por velocidade ou bônus escalado por nível. Alterações externas na flag/entidade não são certificadas por este consumidor.

Com owner não nulo, o impacto exclui owner e aliança nos dois sentidos; se `startFading` já está true, não solicita hurt. Hurt aceito marca fading; hurt recusado não consome esse gate. Os filtros herdados/mixins de colisão ocorrem antes, e a regra não é uma autorização de PvP/claims. A factory de dano usa o owner consultado no impacto, não um par separado projétil/atirador; não atribuir Mastery ou procs por simples spawn, tag `is_projectile` ou som.

DarkArrow chama o tick herdado primeiro. Chão ou impacto aceito podem ativar fading; ele aplica noPhysics, escala o movimento por `0.7F` alargado e descarta quando o **valor anterior** de fadeOut é maior que 5. Isso não é uma duração fixa desde o lançamento. Não há um lifetime de Relentless que se possa ampliar como se fosse cooldown ou carga. A classe não tem serialização própria de shadow damage, perfect flag e fading; estado sincronizado não prova persistência integral após reload.

## 6. Custos, componentes e autoridade

O Dreadbow declara durabilidade **500**, raridade DEMONIC, enchantability **1** e `isEnchantable` para stack de contagem 1. No fim de **cada callback que chegou ao disparo**, fora creative, pede **1 de desgaste** salvo Shaded Respite elegível, e reduz munição em **1**, salvo flecha comum `Items.ARROW` com essa elegibilidade. Munição especial continua consumida. A cobrança é por callback, não por cada uma das 1/2 entidades, e não depende de inserções aceitas ou hits. Não é uma garantia transacional diante de factory null, exceção, reentrada ou consumidores externos.

Não há cooldown, mana, stamina ou fome debitados explicitamente nesse callback; `anvil_cost=8`, desgaste, munição, temporizador de uso e cadência são mecanismos separados. Nem `use`, `releaseUsing` nem `onUseTick` têm uma guarda global própria server-only nos corpos auditados. Isso não prova spawn duplicado ou execução cliente efetiva: lado real dos callbacks, factories e Level continuam fronteiras de QA.

`UseTime`, `PrevUseTime`, `PerfectShotTicks` e `LastUsedArrowType` passam por `CUSTOM_DATA`. Setters gravam componentes; não validam uma perk, uma sessão de uso ou um dono. O transporte existente `UpdateItemTagMessage` resolve entidade e mão por tipo do item, sem demonstrar identidade entre entidade e sender ou reconstrução legítima da carga nesse corpo. A [ficha Dreadbow](../equipment/dreadbow.md) conserva essa fronteira estática; não há homologação de um setter/tag/mensagem como hook seguro.

## 7. Integração e evidência

| Perk / sistema pretendido | Contrato a preservar | Estado |
|---|---|---|
| Cadência / carga | Módulo do argumento restante, modo contínuo e animação cliente são distintos | Hook `NOT_VERIFIED`; não usar M=5 como intervalo nativo de tiros |
| Quantidade / custo | 1/2 tentativas convertíveis; cobrança final por callback | Não duplicar loops, mana, desgaste ou munição por entidade |
| Precisão / alcance / tamanho | Olhar, jitter, speed/inaccuracy e dimensões próprias | Não importar raycasts/chuva do release nem prometer AoE ou acerto |
| Dano / Mastery | Propriedade 2F, owner, hurt aceito e fading | Não tratar criação ou flag de apresentação como hit liquidado |
| Exclusividade / nível | JSON máximo I e predicado positivo, com desvio do release | Componentes forçados não certificam compatibilidade ou escala adicional |
| Persistência / rede | CUSTOM_DATA, sincronização e campos da entidade têm owners próprios | Reload, multiplayer e autorização continuam pendentes |
| Black Arcana / Enshrouded / RPG Skill Tree | Provider conserva uso, projéteis, custo, dano e remoção | `NO_MUTATION`; nenhum adapter executável ou Stage promovido |

O [manifesto individual](../EXACT-RELENTLESS-DARKNESS-CONTRACT-1.0.10.json) reaproveita o [contrato Dreadbow/Dark Arrow](../EXACT-DREADBOW-CONTRACTS-1.0.10.json), preservando provas e fichas anteriores. Os [testes semânticos](../../../../../docs/qa/alexscaves_1010_relentless_darkness_cards_test.py) protegem modo/cadência, visual/carga, custo e relação com projéteis. Métodos extensos têm checkpoints delimitados, sem promessa de CFG completo ou autorização de runtime.

**Contabilidade:** uma ficha individual de encantamento; **+0 raízes mágicas novas**. `STATIC_TECHNICAL_CATALOG_ONLY` / `SHA_EXACT_BINARY_BEHAVIOR`; `mutating_hook=NOT_VERIFIED`, `physical_qa=NOT_TESTED`, provider integral aberto. As vinte fichas parciais anteriores permanecem parciais.

QA física pendente: início/uso/release e fase do timer, consumo com/sem munição e Shade/luz, creative e duas mãos, callbacks/client/dedicado, factories externas/null/spawn recusado, combinações forçadas, colisão/PvP/claims, persistência e autoria de kills. Próxima identidade sem ficha individual: `alexscaves:sated_blade`.
