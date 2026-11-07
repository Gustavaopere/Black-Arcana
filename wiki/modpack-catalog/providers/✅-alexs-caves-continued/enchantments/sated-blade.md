# Sated Blade — `alexscaves:sated_blade` (1.0.10)

**Contrato técnico estático:** ✅ `STATIC_TECHNICAL_CATALOG_ONLY` / `SHA_EXACT_BINARY_BEHAVIOR`. **Hooks mutadores:** `NOT_VERIFIED`. **QA física:** `NOT_TESTED`. **Integração:** `NO_MUTATION`. O recorte conclui o encantamento e o consumidor condicional de saturação da adaga espectral; não conclui outros encantamentos, combate integrado ou o provider integral.

## 1. Identidade e descrição original

- **Provider / versão:** Alex's Caves Continued / `alexscaves`, Minecraft 1.21.1; `alexscaves-1.0.10-neoforge+1.21.1.jar`, CurseForge projeto `1645389`, arquivo `8856293`, **75.279.314 bytes**.
- **JAR SHA-1:** `6960b299a39a039ac8a5eb9b07be4ad0e3e0a570`; **SHA-256:** `36ae0a3cbd028df466a37c671ba2fdf021c060ca1c9c1c32e9f2e95bffae0e7c`.
- **Recurso:** `data/alexscaves/enchantment/sated_blade.json`, 368 bytes; SHA-256 `9f9857ce8d742c377ae7a88a1e4261825c3359a90311f5bfaa3d1a3c792fa86b`.
- **Tag de item:** `data/alexscaves/tags/item/enchantable/desolate_dagger.json`; SHA-256 `c350c3e59d1bbff4d9fd24fa54c96e5fa075682f862c9eba0081c4ef2b97b264`, contendo somente `alexscaves:desolate_dagger`.
- **Descrição literal de `en_us.json`:** “Ghostly dagger attack increases the food saturation level of the attacker”. Tradução explicativa: o ataque da adaga espectral aumenta a saturação alimentar do atacante. Essa descrição deve ser lida junto das condições de fonte/Player abaixo; não há entrada própria no `pt_br.json` examinado.
- **Produtor:** `server/item/DesolateDaggerItem.class`, SHA-256 `ca020279666b45f5d8ede7082ba20c026a870989a6d90166fd1587af921a95ef`. **Consumidor:** `server/entity/item/DesolateDaggerEntity.class`, SHA-256 `f82a3f5f1cc05bbe52dfb7e3742f33c2289cbc37810b069a53b45002cfeb4351`. Prefixo: `com/github/alexmodguy/alexscaves/`.
- **Provas:** [manifesto individual](../EXACT-SATED-BLADE-CONTRACT-1.0.10.json), [reprodução](../EXACT-SATED-BLADE-CONTRACT-1.0.10.md), [equipamento](../equipment/desolate-dagger.md), [entidade/dano](../damage-types/desolate-dagger.md) e [Impending Stab](impending-stab.md).

A busca das classes do JAR por referência ao campo `SATED_BLADE` localizou `ACEnchantmentRegistry` e `DesolateDaggerEntity`; isso não exclui reflexão, transformações ou consumidores externos. A fonte pública `Codx-org/AlexsCavesContinued@523308608422ab8e31974befa7111ecdf495dd37` declara **1.1.1**, sendo apenas corroboração adjacente. Os parâmetros abaixo vêm dos bytes **1.0.10**.

## 2. JSON, nível e aquisição

| Campo | Valor publisher | Significado / limite |
|---|---|---|
| `description.translate` | `enchantment.alexscaves.sated_blade` | Chave de tradução |
| `supported_items` | `#alexscaves:enchantable/desolate_dagger` | Elegibilidade declarada |
| `weight` | `10` | Peso, não chance de alimentação ou de hit |
| `max_level` | `2` | Domínio normal I–II |
| `min_cost` | base `1`, incremento por nível acima do primeiro `11` | I/II: 1/12 |
| `max_cost` | base `41`, incremento `10` | I/II: 41/51 |
| `anvil_cost` | `1` | Custo de encantamento, não débito por adaga |
| `slots` | `mainhand` | Slot declarado |
| `effects` / `exclusive_set` | Ausentes neste JSON | Não comprova compatibilidade global ou ausência de comportamento Java |

O registro liga `SATED_BLADE` à chave `sated_blade`. `ACCompat.enchantLevel` retorna o primeiro nível correspondente aos encantamentos atuais da stack, ou zero. Nem esse leitor nem o consumidor aplicam clamp ao máximo II ou revalidam tag/slot. Níveis/componentes forçados não são um domínio homologado de perks.

As quatro tags empacotadas `minecraft:in_enchanting_table`, `minecraft:non_treasure`, `minecraft:on_random_loot` e `minecraft:tradeable` contêm o ID. O loot `entities/underzealot.json` declara a Desolate Dagger condicionada a kill por jogador e chance base `0.025`; com Looting, chance linear de base `0.035` e incremento `0.01` por nível acima do primeiro. Isso descreve aquisição do item, sem garantir o drop, este encantamento na instância ou os dados efetivos do modpack.

## 3. Gatilho e cadeia até a saturação

`DesolateDaggerItem.hurtEnemy(stack,victim,attacker)` chama `SwordItem.hurtEnemy` e só solicita `acSpawnDaggers` se o callback herdado retorna true. Esse retorno não é uma confirmação independente de dano líquido aceito. O produtor atribui target ID, copia a posição do atacante e passa a stack à entidade, mas **não chama `setPlayerId`**.

A entidade só alcança o stab com alvo resolvido, no ramo **servidor** e quando STAB chega a 1. A espera usa `orbitFor` enquanto positivo e o alvo está vivo; depois progride STAB. O teste de vida nessa espera não é uma proibição separada de dano a alvo morto em outro ramo. Quantidade e espera são consumidores de Double Stab/Impending Stab, não parâmetros de Sated Blade.

No stab, `getPlayer()Entity` resolve o ID sincronizado; se null, a fonte escolhida é **a própria adaga**. Em seguida solicita dano com `causeDesolateDaggerDamage`/`ACCompat.hurt`. Somente retorno true entra no bloco de som e Sated; não há exigência de kill, seleção de cura, proc de Mastery ou confirmação por som.

```text
source = getPlayer()          // Entity, não valida classe Player aqui
if source == null: source = this
if hurt(target, source, requestedDamage):
    L = enchantLevel(getItemStack(), SATED_BLADE)
    if L > 0 and source instanceof Player:
        if source.foodData.getSaturationLevel() < 5F:
            source.foodData.setSaturation(currentSaturation + 0.1F * (float)L)
discard()                    // solicitado também se hurt/condições recusarem
```

Os localizadores do tick são: guarda servidor `@232–239`; fonte/fallback `@293–310`; dano `@312–347`; leitura Sated `@365–375`; nível positivo `@377–379`; Player `@382–395`; saturação/gate `@397–408`; adição/setter `@411–431`; descarte `@434–435`. O corpo continua com rotação/movimento após solicitar descarte; não há retry nativo só porque hurt ou o benefício foram recusados.

## 4. Magnitude, limite e tipo de resultado

| Nível lido no momento do benefício | Pedido de aumento, se todos os gates passarem |
|---|---:|
| 0 | Não entra no benefício |
| I | `0.1F` de saturação |
| II | `0.2F` de saturação |
| Positivo externo | `0.1F × (float)L`, sem clamp próprio ao máximo publicado |

**`saturation<5` é um gate antes da soma, não um clamp da soma.** Um valor atual 4,95 e nível II solicita aproximadamente 5,15 ao setter; o código não calcula `min(5,result)`. Tratamento efetivo de FoodData, eventos ou outros mods permanece na fronteira da engine e não foi medido em jogo.

O método altera **saturação**, não chama `heal`, não escreve food level, não modifica explicitamente exhaustion e não debita mana. Regen indireta por mecânicas de fome não é uma cura de HP emitida por esse bloco. O valor não depende do dano líquido, vida perdida, crítico, quantidade de kills ou número de peças equipadas.

Sated não modifica a fórmula de dano secundário `2F + 2F×level(IMPENDING_STAB)` nem troca `alexscaves:desolate_dagger`. O golpe primário e o stab são consumidores distintos. Não ampliar dano, vida, stamina ou XP multiplicando esse aumento de saturação por tentativas de spawn.

## 5. Beneficiário, targeting, tempo e persistência

`TARGET_ID` e **`PLAYER_ID` começam em −1**, STAB em 0, e a stack sincronizada inicial é uma Iron Sword. `getPlayer` usa ID inteiro no Level atual, retornando Entity ou null; a classe Player só é exigida no bloco do benefício. `setPlayerId(int)` escreve literalmente, sem estabelecer ownership, UUID persistente ou autorização para uma perk.

**A cadeia do produtor auditado não estabelece o vínculo Player exigido para o benefício.** Copiar posição e passar stack não equivalem a preencher PLAYER_ID. Não prometer alimentação ao atacante do melee a partir desses passos nem declarar uma falha física reproduzida. Outros produtores, transformações e integrações precisam provar sua própria atribuição e autoridade.

A stack é fornecida a `setItemStack` sem cópia própria no caller/setter. Sated é relido **depois de hurt aceito**, no stack atual da entidade; não há snapshot imutável do nível capturado pelo produtor. IDs de jogador/alvo e mudanças de componente/equipamento têm momentos distintos de leitura.

O alvo é o ID preatribuído pelo golpe, sem nova busca/AoE do encantamento. O registro da adaga declara dimensões **0.6F×0.6F**; Sated não escala projétil, raio, velocidade, duração ou tipo de alvo. Não existe alcance de alimentação independente para ampliar: o beneficiário é a fonte resolvida, sujeito aos gates. O ramo de stab não adiciona novo teste próprio de distância, linha de visão, PvP ou proteção territorial.

Os corpos próprios `readAdditionalSaveData` e `addAdditionalSaveData` são apenas `return`. Não salvam target/player IDs, stack sincronizada, STAB, orbitFor ou orbitOffset; a persistência genérica de Entity é outra superfície. Não garantir owner/benefício, atraso ou nível equivalentes após reload ou ID reutilizado.

## 6. Custos e integração com o equipamento

O item declara durabilidade **360**, tier DIAMOND e raridade DEMONIC; o callback base conserva a autoridade sobre custo do melee. O bloco Sated não cobra desgaste adicional, stack, cooldown, mana, stamina ou fome por benefício, nem reaplica o custo por tick. Reparação Pure Darkness e aquisição pertencem ao equipamento, sem se tornarem redução de custo desse encantamento.

O tempo até o stab é da adaga/encantamentos irmãos: com nível estável e não negativo, o produtor usa `1+level(DOUBLE_STAB)` tentativas; esse nível é relido a cada comparação do loop. O contador inicial é `orbitFor=(Impending>0 ?40:20)+nextInt(10)`. As faixas iniciais 40–49 ou 20–29 não são duração do benefício nem garantia física de prazo. Sated não altera esse loop ou o contador. Múltiplas tentativas não comprovam benefícios múltiplos aceitos.

## 7. Integração e evidência

| Perk / sistema pretendido | Contrato a preservar | Estado |
|---|---|---|
| Saturação / magnitude | Leitura tardia, `0.1F×L`, gate anterior `<5`, setter nativo | Hook `NOT_VERIFIED`; não transformar gate em clamp ou HP |
| Targeting / beneficiário | Alvo ID e fonte resolvida são diferentes; Player exige binding próprio | Não preencher PLAYER_ID como correção implícita ou atribuir benefício por posição copiada |
| Dano / Mastery | Hurt aceito é pré-condição; não é uma kill ou crédito de XP | Não duplicar hurt, cura ou procs a partir de spawn/som |
| Quantidade / duração / tamanho | Double Stab, Impending, estado e dimensões são outros consumidores | Não converter saturação em AoE ou multiplicador de cada projétil |
| Custo / persistência | Melee herdado e campos próprios sem NBT | Reentrada, reload e lado lógico exigem QA própria |
| Black Arcana / Enshrouded / RPG Skill Tree | Provider conserva golpe, fonte, dano, saturação e remoção | `NO_MUTATION`; nenhum adapter executável ou Stage promovido |

O [manifesto individual](../EXACT-SATED-BLADE-CONTRACT-1.0.10.json) reaproveita Desolate Dagger/Impending Stab, preservando as provas anteriores e completando checkpoints do bloco de saturação dentro do mesmo budget. Os [testes semânticos](../../../../../docs/qa/alexscaves_1010_sated_blade_cards_test.py) protegem gates, fonte, soma, leitura tardia, ausência de binding no produtor, servidor/descarte e NBT. O tick inteiro permanece evidência delimitada, não CFG completo.

**Contabilidade:** uma ficha individual; **+0 raízes mágicas novas**. `STATIC_TECHNICAL_CATALOG_ONLY` / `SHA_EXACT_BINARY_BEHAVIOR`; `mutating_hook=NOT_VERIFIED`, `physical_qa=NOT_TESTED`, provider integral aberto. As vinte fichas parciais anteriores permanecem parciais.

QA física pendente: hurt aceito/recusado, níveis 0/I/II e externos, saturação antes/depois de 5, identificação do beneficiário, callbacks de combate, troca de stack, IDs reutilizados, alvo morto/descarregado, reentrada, cliente/dedicado, reload e integração Mastery/perks. Próxima identidade sem ficha individual: `alexscaves:seapairing`.
