# Seapairing — `alexscaves:seapairing` (1.0.10)

**Contrato técnico estático:** ✅ `STATIC_TECHNICAL_CATALOG_ONLY` / `SHA_EXACT_BINARY_BEHAVIOR`. **Hooks mutadores:** `NOT_VERIFIED`. **QA física:** `NOT_TESTED`. **Integração:** `NO_MUTATION`. O recorte conclui o encantamento e seu consumidor passivo de durabilidade do Sea Staff; não conclui outros encantamentos, o setter da engine, inventários externos ou o provider integral.

## 1. Identidade e descrição original

- **Provider / versão:** Alex's Caves Continued / `alexscaves`, Minecraft 1.21.1; `alexscaves-1.0.10-neoforge+1.21.1.jar`, CurseForge projeto `1645389`, arquivo `8856293`, **75.279.314 bytes**.
- **JAR SHA-1:** `6960b299a39a039ac8a5eb9b07be4ad0e3e0a570`; **SHA-256:** `36ae0a3cbd028df466a37c671ba2fdf021c060ca1c9c1c32e9f2e95bffae0e7c`.
- **Recurso:** `data/alexscaves/enchantment/seapairing.json`, 360 bytes; SHA-256 `e814c593b935bca5a9b84f2ae3aa56d137d9bd099a9e7334b7d4a47fcccfbc57`.
- **Tag de item:** `data/alexscaves/tags/item/enchantable/sea_staff.json`, 49 bytes; SHA-256 `22e45ab74b71d7152ccc531a633e5149df9c12eece40464c85c50f5a600fd80e`; contém somente `alexscaves:sea_staff`.
- **Descrição literal de `en_us.json`:** “Sea Staff can occasionally regain durability when in the inventory of a submerged entity”. Tradução explicativa: o Sea Staff pode ocasionalmente recuperar durabilidade no inventário de uma entidade submersa. O consumidor também testa chuva/bolhas; a descrição não fixa quantidade de reparo ou tempo de espera. Não há entrada própria no `pt_br.json` examinado.
- **Consumidor:** `server/item/SeaStaffItem.class`, SHA-256 `cb3153a35e7f4c3ab23e68693aec110edf03ecd050c3b485e35ccbb257b4bbc6`. **Despacho:** `mixin/ItemStackTickMixin.class`, SHA-256 `260fff4418e426eb5b3b9a02032cc0d5ebb73444aa1b16d7d578f4660e33a6b6`. Prefixo de classes: `com/github/alexmodguy/alexscaves/`.
- **Provas:** [manifesto individual](../EXACT-SEAPAIRING-CONTRACT-1.0.10.json), [reprodução](../EXACT-SEAPAIRING-CONTRACT-1.0.10.md) e [ação Water Bolt do Sea Staff](../actions/sea-staff-water-bolt.md).

A busca de referências ao campo `SEAPAIRING` nas classes do JAR localizou `ACEnchantmentRegistry` e `SeaStaffItem`; não exclui reflexão, transformações ou consumidores externos. A fonte pública `Codx-org/AlexsCavesContinued@523308608422ab8e31974befa7111ecdf495dd37` declara **1.1.1** e é apenas corroboração adjacente. Os parâmetros abaixo vêm do binário/dados **1.0.10**.

## 2. JSON, nível e aquisição

| Campo | Valor publisher | Significado / limite |
|---|---|---|
| `description.translate` | `enchantment.alexscaves.seapairing` | Chave de tradução |
| `supported_items` | `#alexscaves:enchantable/sea_staff` | Elegibilidade declarada |
| `weight` | `1` | Peso, não probabilidade do reparo |
| `max_level` | `1` | Apenas I publicado |
| `min_cost` | base `1`, incremento por nível acima do primeiro `10` | Nível I: 1 |
| `max_cost` | base `41`, incremento `10` | Nível I: 41 |
| `anvil_cost` | `8` | Custo de encantamento, não XP debitado por proc |
| `slots` | `mainhand` | Declaração de dados; não é um teste de slot neste callback |
| `effects` / `exclusive_set` | Ausentes neste JSON | Não prova compatibilidade global ou ausência de comportamento Java |

O registro liga `SEAPAIRING` à chave `seapairing`. `ACCompat.enchantLevel` lê os encantamentos atuais da stack e retorna o primeiro nível correspondente ou zero, sem clamp ao máximo I nem validação própria de slot/tag. O consumidor só pergunta se o resultado é positivo: níveis forçados II ou maiores não escalam chance, valor do setter ou cadência nesse corpo.

As quatro tags empacotadas `minecraft:in_enchanting_table`, `minecraft:non_treasure`, `minecraft:on_random_loot` e `minecraft:tradeable` contêm o ID. O loot `gameplay/deep_one_mage_barter.json` inclui **o item Sea Staff**, com peso 12 em um pool de um roll; não garante obtenção, este encantamento na instância ou dados efetivos do modpack.

## 3. Despacho e condições do callback passivo

SeaStaffItem implementa `ACTickingItem`; não declara override próprio de `inventoryTick`. `ItemStackTickMixin.ac_inventoryTick(Level,Entity,int,boolean,CallbackInfo)V` intercepta `ItemStack.inventoryTick` em HEAD, obtém o Item, testa a interface e chama `acInventoryTick(stack,level,entity,selected)`. O slot inteiro não é encaminhado. A interface é abstrata, sem corpo executável. `alexscaves.mixins.json` lista o mixin e o TOML do JAR declara essa configuração; isso é conexão estática, não frequência de execução medida ou seam externo de perks homologado.

O consumidor `SeaStaffItem.acInventoryTick(ItemStack,Level,Entity,boolean)V` tem 42 instruções, offsets `0–91`, com esta ordem:

1. Calcula `usingThisStack = entity instanceof LivingEntity && living.getUseItem().equals(stack)` em `@0–30`. Chama `Object.equals`; não chama `isUsingItem` nem implementa comparação de componentes nesse corpo. Não substituir essa condição por um estado de cast deduzido do HUD.
2. Retorna no cliente (`@32–36`). O cálculo da igualdade precede a guarda, mas o pedido de reparo permanece no ramo servidor.
3. Lê o nível na stack e retorna se `L<=0` (`@39–46`); retorna também se `usingThisStack` (`@49–51`). O argumento `selected`, local 4, **não é lido**. Não é uma exigência de slot selecionado ou mainhand em execução.
4. Consulta `Level.getRandom().nextFloat()` e só prossegue se `<0.02F` (`@54–67`). Esse sorteio vem **antes** do teste ambiental.
5. Exige `entity.isInWaterRainOrBubble()` (`@70–74`). O teste recebe o argumento Entity do callback; isso não estabelece que itens soltos ou qualquer inventário externo recebam esse callback.
6. Pede `stack.setDamageValue(Math.min(0,stack.getDamageValue()-1))` (`@77–88`) e retorna.

```text
if !level.isClientSide && enchantLevel(stack, SEAPAIRING)>0 && !usingThisStack:
    if level.getRandom().nextFloat()<0.02F:
        if entity.isInWaterRainOrBubble():
            stack.setDamageValue(min(0, stack.getDamageValue()-1))
```

Um callback elegível por nível/uso ainda consome RNG quando o portador está seco, pois o teste ambiental vem depois. Não há contador acumulado de tentativas, garantia a cada 50 ticks ou multiplicador por nível. O threshold nominal 0,02 é **por callback elegível**, sem prometer distribuição observada, espera média ou reparos por segundo no modpack.

## 4. Pedido de durabilidade e limite da prova

**O literal é `Math.min`, não `Math.max`.** Não reinterpretar a operação como um reparo fixo de um ponto:

| Damage atual D, no domínio normal não negativo | Argumento inteiro pedido ao setter |
|---|---:|
| 0 | −1 |
| 1 | 0 |
| 40 | 0 |
| Qualquer D≥1 | 0 |

Não há `isDamaged`, `D>0`, `getMaxDamage` ou clamp próprio `max(0,D−1)` antes dessa escrita. O consumidor não mede quanto foi efetivamente reparado. **Valor armazenado, clamp, componente de damage, sincronização e durabilidade visível pertencem à fronteira Minecraft ItemStack/engine**, não comprovada por este JAR de provider. A divergência de expectativa não é uma falha reproduzida em jogo, nem é corrigida nesta contribuição.

O estado lido e escrito é o damage da mesma stack. Não há alvo de cura, HP, food level, saturação, mana ou stamina alterados nesse consumidor. O peso do encantamento, seu custo de bigorna, o threshold RNG e o argumento do setter são mecanismos distintos.

## 5. Equipamento, custo e persistência

O registro do Sea Staff (`ACItemRegistry`/`lambda$static$108`) declara durabilidade **850** e raridade **UNCOMMON**. Enchantability é **1**; `isEnchantable` aceita contagem de stack igual a 1. Essas propriedades não quantificam o reparo observado.

O cast Water Bolt já tem seu próprio pedido de desgaste **1**, condicionado a `!instabuild`, via `ACCompat.hurtAndBreak`/slot da mão. Seapairing não repete esse cast, não gera projétil e não modifica o custo nessa rotina. Reparo passivo e desgaste do uso podem ocorrer em callbacks e momentos diferentes; não prometer saldo líquido por unidade de tempo.

Não há débito próprio de material, stack, XP, fome ou cooldown no callback passivo. Ele não mantém timer, charges, owner UUID ou estado adicional de persistência de Seapairing: relê o nível e o damage atuais em cada execução. Persistência do damage/componente e alterações por outros sistemas continuam sob autoridade da stack/engine; não criar uma segunda contabilização de reparo ao salvar/carregar.

## 6. Targeting, tempo e outros parâmetros de perks

| Superfície | Contrato deste encantamento |
|---|---|
| Portador / elegibilidade | Não exige Player no consumidor; só usa LivingEntity para a igualdade com getUseItem. Distribuição real do callback a inventários/entidades é uma fronteira externa |
| Slot / uso | `selected` ignorado; igualdade com a stack de uso bloqueia. Estar selecionado, ter item na mão e estar usando não são testes intercambiáveis |
| Ambiente | `isInWaterRainOrBubble`, não underwater-only, biome, raio ou nova tag de fluido |
| Chance / nível | Threshold fixo `0.02F`, habilitado por `L>0`; não há escala com níveis positivos |
| Duração / intervalo | Sem duração, cooldown ou contador próprio. Cadência depende dos callbacks nativos |
| Dano / tipo de alvo / área / tamanho / velocidade | N/A como modificadores próprios: é manutenção passiva da stack, sem hurt, spawn, raycast ou mudança de hitbox |

Os parâmetros do Water Bolt e dos encantamentos irmãos conservam seus próprios consumers. A presença deles no corpo completo de `use` não transforma este certificado individual em homologação desses modificadores, de todo o projétil ou do equipamento inteiro.

## 7. Integração e evidência

| Perk / sistema pretendido | Contrato a preservar | Estado |
|---|---|---|
| Chance / ritmo | RNG do Level, threshold por callback e ordem antes do ambiente | Hook `NOT_VERIFIED`; não converter em agenda fixa ou duplicar tentativas |
| Quantidade de reparo | Argumento `min(0,D−1)` separado do valor aplicado pela engine | Não corrigir silenciosamente para max nem prometer um ponto por proc |
| Slot / portador / ambiente | Uso por equals, selected não lido e predicate do portador | Não impor Player/mainhand-only por inferência do JSON |
| Custo / XP / Mastery | Ausência de débito próprio não é crédito ou proc liquidado | Não atribuir XP por callback/RNG/setter antes de resultado autorizado |
| Persistência / múltiplas cópias | Estado pertence à stack e nível é relido | Reload, outras instâncias e reentrada precisam de QA |
| Black Arcana / Enshrouded / RPG Skill Tree | Provider conserva despacho, RNG e escrita; engine conserva componente | `NO_MUTATION`; nenhum adapter executável ou Stage promovido |

O [manifesto individual](../EXACT-SEAPAIRING-CONTRACT-1.0.10.json) e os [testes semânticos](../../../../../docs/qa/alexscaves_1010_seapairing_cards_test.py) ligam identidade, callback completo, despacho, reader, custo delegado e limites estáticos. A [prova comum](../EXACT-TECHNICAL-CONTRACTS-1.0.10.json), os contratos anteriores e Sea Swing permanecem preservados. Mixin/assinatura/setter observados não são, sozinhos, um hook suportado para perks.

**Contabilidade:** uma ficha individual; **+0 raízes mágicas novas**. `STATIC_TECHNICAL_CATALOG_ONLY` / `SHA_EXACT_BINARY_BEHAVIOR`; `mutating_hook=NOT_VERIFIED`, `physical_qa=NOT_TESTED`, provider integral aberto. As vinte fichas parciais anteriores permanecem parciais.

QA física pendente: valor aplicado em D0/D1/Dalto, níveis 0/I/externos, portador molhado/seco/chuva/bolhas, using versus selected, mãos/inventários transformados, múltiplas cópias e RNG, creative, cliente/dedicado, sincronização e unload/reload. A fila atual é mantida no [crosswalk alfabético](../ENCHANTMENT-PERK-CROSSWALK-1.0.10.md).
