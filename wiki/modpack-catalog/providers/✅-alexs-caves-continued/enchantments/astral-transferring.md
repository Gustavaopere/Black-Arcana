# Astral Transferring — transferência do vínculo do Totem (1.0.10)

**Estado:** ⚠️ ficha técnica individual **parcial / condicionada**. Identidade, dados publisher e trecho compilado do consumidor confirmados no artefato instalado. **Contrato mutador não verificado; QA físico não executado; nenhuma homologação integral de perk.** Este encantamento modifica o controle nativo já catalogado como [Totem of Possession — Possession / Remote Control](../actions/totem-possession-remote-control.md), **não acrescenta uma nona ação mágica**.

## Identidade, versão e prova

- **Provider:** Alex's Caves Continued; mod ID `alexscaves`.
- **Enchantment:** `alexscaves:astral_transferring`; tradução publisher referenciada pela chave `enchantment.alexscaves.astral_transferring`. Nenhum texto de tooltip da versão instalada foi certificado nesta análise.
- **Item:** `alexscaves:totem_of_possession`; item elegível conforme `#alexscaves:enchantable/totem_of_possession`.
- **Binário:** `alexscaves-1.0.10-neoforge+1.21.1.jar`; 75.279.314 bytes; SHA-1 `6960b299a39a039ac8a5eb9b07be4ad0e3e0a570`; SHA-256 `36ae0a3cbd028df466a37c671ba2fdf021c060ca1c9c1c32e9f2e95bffae0e7c`.
- **Evidência estática selada:** [recursos e janelas JVM 1.0.10](../EXACT-ASTRAL-TRANSFERRING-1.0.10.json), reproduzidos por [sonda read-only](../../../../../docs/qa/alexscaves_1010_astral_transfer_probe.py) e [CI específica](../../../../../.github/workflows/alexscaves-1010-astral-transfer.yml).
- **Evidência de ação existente:** [contratos SHA-exatos das oito ações](../EXACT-TECHNICAL-CONTRACTS-1.0.10.md) e [ficha do Totem](../actions/totem-possession-remote-control.md).
- **Fonte pública adjacente:** `Codx-org/AlexsCavesContinued@523308608422ab8e31974befa7111ecdf495dd37` declara **1.1.1**, não sendo autoridade dos valores da release física 1.0.10.

A classe `com/github/alexmodguy/alexscaves/server/item/TotemOfPossessionItem.class` possui SHA-256 `bad9dd8b88eb621b558d1ede477d2b4ba6a21befdec31b4a0233adcac701773e`, idêntico ao contrato estático anterior. O `onUseTick(Level,LivingEntity,ItemStack,int)V` possui **478 instruções** e digest do parse JVM `4d366c998c89884f53bc9554f52c6477c5c6bbb8e6aea1bf0f93867dc1b41d39`. Os offsets abaixo pertencem **somente** a esse método e JAR.

## Definição publisher: custo e elegibilidade

| Campo do recurso `data/alexscaves/enchantment/astral_transferring.json` | Valor exato |
|---|---|
| SHA-256 do JSON | `41133c10af9c9e8d5e33d1b8339b734f81547b141f83fc0144aa9cf89f1f04c2` |
| `supported_items` | `#alexscaves:enchantable/totem_of_possession` |
| `weight` | `2` |
| `max_level` | `1` |
| `min_cost.base` / `per_level_above_first` | `1` / `12` |
| `max_cost.base` / `per_level_above_first` | `41` / `10` |
| `anvil_cost` | `4` |
| `slots` | `mainhand` |

O item tag publisher `data/alexscaves/tags/item/enchantable/totem_of_possession.json` contém `alexscaves:totem_of_possession` (SHA-256 `185a085206993877d91ca6d8c697273c14f945b1d55cb6179e3236c138c357cf`). O JSON de `detonating_death` declara `exclusive_set: ["alexscaves:astral_transferring"]` (SHA-256 `8402461954ff5b249ae675b51d7dcc23d933b2b06c494b327bf608371298646e`). A exclusividade declarada não comprova comportamento sob mods de encantamento não convencionais, edições de datapack ou níveis fora do padrão.

**Esses são custos de encantamento do jogo, não mana/custo por cast**. O controle do Totem tem durabilidade declarada 1.000 e lógica de desgaste própria (com pendência relevante de autoridade do desgaste em cliente/servidor): não equiparar o peso, custo de bigorna ou `min_cost` a consumo por transferência. Valores e exclusividades efetivos após datapacks/mods continuam `NOT_VERIFIED`.

## Predicados e efeito da transferência

O consumidor compilado `TotemOfPossessionItem.onUseTick` identifica `ACEnchantmentRegistry.ASTRAL_TRANSFERRING @920` e chama `ACCompat.enchantLevel @923`, seguido por `ifle @926 → 1081`. Isso exige nível **positivo** no stack do Totem para entrar no trecho subsequente.

A cadeia local comprovada é:

1. O caminho de ataque do **Mob já controlado** usa `Mob.setTarget @871` e `Mob.setLastHurtByMob @878` para candidatos da consulta ao redor da entidade controlada. A seleção inicial, guardas de amizade e exclusões são detalhados na [ficha do Totem](../actions/totem-possession-remote-control.md). O encantamento **não** cria uma nova busca global de alvos.
2. O contador de uso é dividido por quatro: `iconst_4 @883`, `irem @884`, `ifne @885 → 1081`; apenas a iteração de resto zero prossegue no ramo local. Não equivale a cooldown persistido de quatro ticks, nem a limite de quatro segundos.
3. Lê `LivingEntity.getHealth @890` do candidato e `Mob.getHealth @895` do controlado; `fcmpl @898` e `ifle @899 → 1081` exigem **vida atual estritamente maior** para prosseguir (em valores normais finitos). É comparação de vida atual, **não** da vida máxima nem de nível, atributos ou raridade.
4. Consulta o tipo de entidade e `ACTagRegistry.RESISTS_TOTEM_OF_POSSESSION @910`; `Holder.is @913` seguido por `ifne @916 → 1081` bloqueia a transferência para o alvo resistente.
5. Exige nível do encantamento `>0`, depois chama `setPossessed(candidate,true) @932`, lê `BoundEntityUUID @943`, `getUUID @948` e `ACCompat.putUUID @951`.
6. Serializa o novo candidato com `ACPlatform.serializeEntity @956`, adiciona o ID do tipo ao `CompoundTag` (`"id" @963`), grava `BoundEntityTag @987–992` e persiste via `ACCompat.setTag @999`. Em seguida solicita o som `TOTEM_OF_POSSESSION_USE @1002–1014`.
7. O ramo específico de atualização `@1017–1048` chama `updateEntityIdFromServer(ServerLevel,Player,ItemStack)` quando as verificações de tipos alcançam a chamada. O helper lê o vínculo UUID, resolve o ID da entidade pelo `ServerLevel`, atualiza tag e pode enviar `UpdateItemTagMessage` para sincronização. Não prova entrega, autenticação de pacote ou save/reload efetivo.

O helper `setPossessed(Entity,boolean)` apresenta 16 instruções e alterna a marca persistente `TotemPossessed` no alvo selecionado; o `updateEntityIdFromServer` possui 49 instruções. Ambos têm hashes de método registrados no [manifesto selado](../EXACT-ASTRAL-TRANSFERRING-1.0.10.json).

## Área de busca, restrições e lifecycle

Na [ação Totem](../actions/totem-possession-remote-control.md), a seleção de candidatos para ataques usa a **bounding box do controlado inflada em 3 blocos por eixo**, com filtros para entidades `LivingEntity` aptas à colisão de projéteis, usuário, aliados, alvo atual e passageiros. Não se deve equiparar isso a um raio de dano mágico de três blocos, nem ao raio do look gate do usuário. O comando de navegação tem outro parâmetro, `32 × ramp`, que **não define** o alcance de Astral Transferring.

O JSON exato da tag `data/alexscaves/tags/entity_type/resists_totem_of_possession.json` (SHA-256 `6ae5d98cd4b12739d3d1d7dc78d37053b2e5b0eb3b1093e3f8a9a6d9768df209`) declara, como defaults publisher: `#c:bosses`, `minecraft:warden`, `minecraft:armor_stand`, `alexscaves:hullbreaker`, `alexscaves:forsaken`, `alexscaves:atlatitan` e `alexscaves:tremorzilla`. O conjunto **efetivo** varia conforme a resolução do tag `#c:bosses` e datapacks carregados; não afirmar que essa lista é exaustiva no modpack.

**Riscos de estado já identificados:** no recorte de transferência, `setPossessed(new,true)` e a atualização do novo vínculo não exibem uma limpeza equivalente do marcador persistente do alvo anterior. O loop de candidatos da ação também não executa `break` após uma transferência bem-sucedida. Assim, múltiplos candidatos em uma iteração podem provocar novas sobrescritas; não afirmar um único novo alvo escolhido pela proximidade ou transação atômica. O comportamento de limpeza posterior, unload, troca de dimensão, duas cópias do item, morte/respawn e reconciliação de dados persistidos necessita de QA adicional.

O contrato de controle geral interrompe o uso quando o alvo deixa de existir ou quando o item se esgota, ou quando falham os gates de visão/posse; a transferência não substitui essas condições. O ramo local da transferência não comprova uma checagem independente de `totem_of_possession_works_on_players`; uma transferência para `Player` sob configuração proibitiva não deve ser considerada segura somente pela exclusão de mobs resistentes, pois o gate do próximo tick pode encerrar o uso.

## Fronteira de integração com perks

| Eixo de perk | Fato reutilizável do provider | Condição para implementação |
|---|---|---|
| Alvos / seletor | Alvo próximo ao controlado; filtros da ação; vida atual maior; tag de resistência | ⛔ Sem ponto seguro verificado para modificar elegibilidade ou escolher alvo; preservar owner, allies, Player gate e ordem do loop |
| Range / AoE | Busca na AABB inflada por 3; comando visual a `32×ramp` | ⛔ Não usar alcance de comando como alcance de transferência nem estender box sem API estável |
| Taxa de proc / cooldown | Predicado `contador % 4 == 0` | ⛔ Sem hook para mudar intervalo ou impor cooldown transacional sem reexecutar o processamento |
| Dano / tipo de dano | `Mob.setTarget` / `setLastHurtByMob`; ataques normais do controlado | ⛔ Sem dano próprio de Astral Transferring evidenciado; não duplicar `hurt` nem alterar `DamageSource` |
| Estado / duração / ownership | UUID, `BoundEntityTag`, `TotemPossessed`, `ControllingEntityID` | ⛔ Não escrever tags de outro provider nem tomar controle do vínculo por perk sem resolver concorrência, restart e autorização |
| Custo / Mastery | JSON de encantamento e durabilidade nativa do Totem | ⛔ Não converter custos do enchanting em mana por uso nem emitir proc/XP por cada novo candidato sem cadeia nativa verificada |
| Cliente, PvP, claims | Helper de sincronização e resolução de UUID no `ServerLevel` | ⛔ Exige prova de autoridade do lado servidor, atualização do destinatário, proteção de jogadores e replay before any adapter |

A autoria do runtime de possessão pertence ao provider. O Black Arcana não deve reexecutar a transferência ou o dano para aplicar uma perk; o RPG Skill Tree é apenas authority de progressão/Mastery/gates sob contrato real.

## Certificação e próximos testes

**Identidade/JSON:** `VERIFIED_EXACT_BINARY`. **Guardas e referências do consumidor:** `VERIFIED_EXACT_BINARY_SELECTED_WINDOWS`; o grafo de controle completo, o estado efetivo de datapack e a cadeia de autoridade de servidor **não** foram certificados integralmente. **Hook mutador:** `NOT_VERIFIED`. **QA físico:** `NOT_TESTED`. **Mutação:** `NO_MUTATION`. **Certificação para perk:** `NOT_CERTIFIED`.

Para homologar futuras modificações, testar em jogo real: cada cadência de quatro ticks, comparação de vida atual, filtros de owner/aliados e tags reais, configuração de Player, múltiplos alvos, persistência de `TotemPossessed`, vínculo antigo, competição entre totems, recarregamento/teleporte e comportamento PvP; correlacionar eventos do cliente e servidor antes de admitir qualquer mutação.

**Contagem:** adiciona **uma ficha individual parcial de encantamento** ao universo observado; **zero** novos contratos estáticos certificados; **zero** novas raízes mágicas; **zero** providers concluídos. A próxima identidade em ordem alfabética é `alexscaves:bonking`.
