# Ferrous Haste — velocidade de ataque e mineração do Galena Gauntlet (1.0.10)

**Estado:** ⚠️ ficha individual **parcial/condicionada**. Definição JSON, tags, classfiles e janelas JVM críticas foram verificados no **JAR publisher SHA-exato 1.0.10**. A documentação é read-only: **não** demonstra hook mutador seguro, CFG integral, execução real do jogo, resultado efetivo de ataques/mineração ou QA física. Contratos: \`mutating_hook=NOT_VERIFIED\`, \`physical_qa=NOT_TESTED\`, \`perk_certification=NOT_CERTIFIED\`, \`mutation=NO_MUTATION\`.

**Síntese funcional:** \`alexscaves:ferrous_haste\` acelera dois caminhos **nativos** da entidade \`MagneticWeaponEntity\` controlada por jogador com \`alexscaves:galena_gauntlet\`: a janela/cooldown entre tentativas de ataque e o incremento do progresso de quebra. Não é feitiço autônomo, não cria outra arma magnética e não transfere o ataque ou a mineração à autoridade do Black Arcana.

## 1. Fontes de autoridade

| Objeto | Evidência física da versão |
|---|---|
| Mod/versão instalada | Alex's Caves Continued, \`alexscaves-1.0.10-neoforge+1.21.1.jar\`, conforme [modlist sibling](https://github.com/Gustavaopere/neoforge-rpg-skilltree/blob/main/PROJECT-INSTRUCTIONS/modlist/modlist.md), entrada #019 |
| Ambiente | Minecraft 1.21.1 / NeoForge / Java 21 |
| Artefato publisher | **75.279.314 bytes**, SHA-1 \`6960b299a39a039ac8a5eb9b07be4ad0e3e0a570\`; SHA-256 \`36ae0a3cbd028df466a37c671ba2fdf021c060ca1c9c1c32e9f2e95bffae0e7c\` |
| Recurso JSON | \`data/alexscaves/enchantment/ferrous_haste.json\`, **384 bytes**, SHA-256 \`38db83ed098b276532ad99d652f0614a4ec85b23c1dacb1f17d614a9a3d2f819\` |
| Tag física | \`data/alexscaves/tags/item/enchantable/galena_gauntlet.json\`, **55 bytes**, SHA-256 \`5f8a2dfe1222c6631122855a11ab011d916bea83d285d6ecd886a177c058c4cb\` |
| Classe de item | \`com/github/alexmodguy/alexscaves/server/item/GalenaGauntletItem.class\`, SHA-256 \`5a74328a7130704a4e2dca9e607bed4dc3a468b8bbcb6d4e238b4d2d962573b0\` |
| Classe consumidora | \`com/github/alexmodguy/alexscaves/server/entity/item/MagneticWeaponEntity.class\`, SHA-256 \`a26794c9eba89c554e812078886beda6129d5298219f685f6d0e2be315fbf071\` |
| Registry | \`ACEnchantmentRegistry.class\`, SHA-256 \`60006fab1b3b29f5f93c8365416815a12770cf8877a059298cb4ee82f7a92f32\`, símbolos \`FERROUS_HASTE\` / \`ferrous_haste\` verificados |

**Prova nova:** [manifesto SHA-exato](../EXACT-FERROUS-HASTE-1.0.10.json), extraído pela [sonda de auditoria read-only](https://github.com/Gustavaopere/Black-Arcana/blob/main/docs/qa/alexscaves_1010_ferrous_haste_probe.py), com [regressões sintéticas](https://github.com/Gustavaopere/Black-Arcana/blob/main/docs/qa/alexscaves_1010_ferrous_haste_probe_test.py) e [workflow próprio](https://github.com/Gustavaopere/Black-Arcana/blob/main/.github/workflows/alexscaves-1010-ferrous-haste.yml). Gate SHA-1/SHA-256/tamanho do publisher, SHA dos três classfiles, validação de recursos e igualdade integral no modo \`--seal\`. São **janelas limitadas de instruções compiladas**, não uma decompilação integral, API pública, execução do cliente ou prova de hook.

**Referências preexistentes:** [Crystallization — ficha](crystallization.md) e [manifesto exato Crystallization](../EXACT-CRYSTALLIZATION-1.0.10.json) já demonstravam, como evidência auxiliar, \`FERROUS_HASTE @608\` na entidade magnética. A sonda nova isola as ramificações de ataque e mineração e associa o ID do encantamento ao recurso publisher, sem duplicar a ação semântica \`Galena Gauntlet\`.

O snapshot público \`Codx-org/AlexsCavesContinued@523308608422ab8e31974befa7111ecdf495dd37\` declara **versão 1.1.1**, não autoridade para números ou classfiles da 1.0.10. As constantes registradas nesta ficha derivam somente da evidência do JAR 1.0.10.

## 2. JSON do encantamento

| Campo | Valor exato |
|---|---|
| \`description.translate\` | \`enchantment.alexscaves.ferrous_haste\` |
| \`supported_items\` | \`#alexscaves:enchantable/galena_gauntlet\` |
| \`weight\` | **2**, peso de seleção de encantamento, não chance de ataque |
| \`max_level\` | **1** |
| \`min_cost\` | \`base=1\`, \`per_level_above_first=15\` |
| \`max_cost\` | \`base=41\`, \`per_level_above_first=10\` |
| \`anvil_cost\` | **4** |
| \`slots\` | \`["mainhand","offhand"]\` |
| \`exclusive_set\` | Não consta nesse JSON; não certifica compatibilidades em datapacks/ambientes alterados |

A tag publisher contém apenas \`alexscaves:galena_gauntlet\` em \`values\`. Os campos de \`cost\` são custos de aquisição/encantamento, **não** débito de durabilidade, mana, cooldown, consumo de ferramenta controlada ou tempo de mineração.

## 3. Gatilho e autoridade — \`MagneticWeaponEntity.tick()V\`

A classe \`MagneticWeaponEntity\` tem **744 instruções** no método \`tick()V\` conforme parse da sonda. O caminho verificado procura o controller e verifica o item de uso ativo:

1. \`tick @579\`: \`LivingEntity.getUseItem()\` obtém o stack efetivamente usado.
2. \`@582–596\`: compara com \`ACItemRegistry.GALENA_GAUNTLET\`; somente nesse ramo acessa os encantamentos da gauntlet.
3. \`@608\`: \`getstatic ACEnchantmentRegistry.FERROUS_HASTE\`, seguido de \`ACCompat.enchantLevel @611\`.
4. \`@614–622\`: resultado **positivo** vira flag booleana \`haste=true\`; nível 0 (ou não positivo) vira false. Não há multiplicador progressivo por nível nesse ramo; o JSON publisher permite até nível I.
5. \`FIELD_EXTENSION @626\` é consultado **separadamente** por \`ACCompat.enchantLevel @629\`; \`@639–644\` acrescenta \`5F × nível\` a outro escalar, usado no \`ProjectileUtil.getHitResultOnViewVector @659\`.

**Cuidado com targeting e range:** \`FIELD_EXTENSION\` é outro encantamento. Ferrous Haste não altera diretamente \`getHitResultOnViewVector\` na região selada. A janela comprova o acréscimo \`5F×nível(FIELD_EXTENSION)\` e a passagem de um valor à consulta de alvo; não se deve atribuir esse ganho a Ferrous Haste, nem tratar qualquer alcance de raycast como área de dano ou raio de mineração.

### 3.1. Tentativa de ataque — cooldown escolhido

O ramo de acerto selecionado verifica \`EntityHitResult @666–669\`, \`playerUseCooldown == 0 @680–683\`, proximidade segundo \`distanceTo\` e \`getBbWidth()+1.5F @720–736\` e \`strikeProgress\` (incremento local **0.35F** quando menor que 1, \`@739–760\`). Quando a progressão já permite, solicita \`hurtEntity(player,entity) @771\`; em seguida atribui o cooldown:

| Caminho do booleano \`haste\` | Constantes e operação JVM | Valor solicitado a \`playerUseCooldown\` |
|---|---|---|
| Ferrous Haste ativo | \`@775–781\`: \`iload 7\`, teste e \`iconst_3\` | **3** |
| Sem Ferrous Haste | \`@784–796\`: \`iconst_5\`, \`RandomSource.nextInt(5)\`, soma | **5 + inteiro aleatório de 0 a 4** (5–9) |

A passagem de \`hurtEntity\` antes de escrever o cooldown **não prova** que a vítima sofreu dano, que o ataque foi aceito pelas proteções, que houve XP/Mastery ou que o cooldown final percebido no cliente é exatamente 3 ticks. O método \`tick\` tem outras regras de decremento e condições de aquisição. **Não** multiplicar 20 TPS por um intervalo escolhido para anunciar ataques por segundo ou DPS garantido.

O método downstream \`hurtEntity(LivingEntity,Entity)V\` possui **141 instruções** e consulta \`ACCompat.hurt @99\`, \`ACCompat.postAttackEffects @115\`, \`damageItem @120\` e \`ItemStack.hurtEnemy @239\`. Esses são caminhos de dano/efeito/desgaste de item; não um novo tipo de dano produzido por Ferrous Haste. Não inferir sucesso de dano, aplicação de efeito pós-ataque ou conservação do item apenas pela presença de um callsite.

### 3.2. Mineração — divisor da progressão do bloco

Na rota do mesmo \`tick\`, após seleção de bloco e outros guards:

- \`BlockState.getDestroySpeed @1013\` fornece o escalar de dureza \`f\`; \`MagneticWeaponEntity.getDigSpeed(player,state,pos) @1025\` obtém o parâmetro de velocidade de mineração do item controlado, \`itemDestroySpeed\`.
- \`itemDestroySpeed > 1.0F\` é exigido pelo ramo compilado \`@1030–1034\`.
- \`@1114–1133\` calcula \`incremento = (itemDestroySpeed / f) / divisor\`, com \`divisor = 8\` se \`haste\`, ou \`divisor = 10\` sem ele.
- \`@1135–1143\` acumula o incremento em \`destroyBlockProgress\`; \`@1160–1168\` emite atualização visual \`Level.destroyBlockProgress\` com escala \`×10F\`.
- Só ao alcançar \`destroyBlockProgress >= 1F @1171–1177\`, e **em servidor** (\`isClientSide @1181–1187\`), o restante do caminho pode solicitar dano de durabilidade, \`ItemStack.mineBlock @1213\` e operações nativas de \`Level.destroyBlock\` (\`@1290\` para um ramo de Shulker Box, \`@1329\` em outro caminho).
- \`getDigSpeed(Player,BlockState,BlockPos)F\` possui **80 instruções** e contém \`getDestroySpeed @9\`, \`miningEfficiencyBonus @26\`, \`submergedMiningFactor @157\` e \`getBreakSpeed @183\`: a velocidade efetiva depende de ferramenta/efeitos/água e outros filtros, e não só do encantamento.

**Comparação condicional:** se os demais termos forem fixos e válidos, usar divisor 8 em vez de 10 torna o **incremento do progresso por processamento elegível 10/8 = 1,25 vezes** o baseline (25% maior). Isso **não** é garantia de mineração concluída 25% mais rápido: dureza, velocidade do item, TPS, falhas de permissão, reset de bloco, regras de drops e callbacks do engine podem alterar o resultado. Também não garante que \`destroyBlock\` retornou true. A escolha booleana não cria um cast separado nem acelera arbitrariamente todos os tipos de mineração do Minecraft.

## 4. Ciclo nativo, custos, persistência e riscos

| Dimensão | Evidência técnica | Limite para perks |
|---|---|---|
| Origem da entidade | \`GalenaGauntletItem.use\` / \`onUseTick\` — \`createEntity @216\`, \`setItemStack @228\`, \`setControllerUUID @252\`, \`addFreshEntity @258\` | Reutilizar controle provider-native; chamadas de spawn **não comprovam** inserção nem duplicação segura |
| Controle simultâneo | Busca \`getEntitiesOfClass @124\` no \`onUseTick\` da gauntlet; [ficha Crystallization](crystallization.md) detalha AABB 64D | Não introduzir novo scan global/tick, segundo controller ou item duplicado |
| Ativação | \`getUseItem\` deve identificar a gauntlet em uso no ramo \`tick\`; \`haste\` é flag positiva | Não aplicar o bônus a armas sem gauntlet ativa, todos os mobs ou todos os golpes do jogador |
| Ataque | \`hurtEntity @771\`; cooldown \`3\` versus \`5+nextInt(5)\` | Sem prova de DPS final, hit efetivo, autoria/Mastery, cancelamento e dedupe |
| Mineração | \`getDigSpeed\`, \`getDestroySpeed\` e divisor \`8/10\`; \`Level.destroyBlock\` downstream | Não burlar claims, blacklist de blocos, drops, \`WorldEffectPolicy\` ou guards do server |
| Desgaste | \`damageItem\` e \`hurtAndBreakUsedHand\` presentes em métodos próprios; \`releaseUsing\` da gauntlet solicita cooldown **5** na liberação, segundo [Crystallization](crystallization.md) | Não confundir cooldown de liberação com cooldown de ataque; não cobrar mana ou durabilidade duas vezes |
| Alvo e área | \`getHitResultOnViewVector\` e \`FIELD_EXTENSION\` são rota de targeting separada; minério depende do bloco selecionado | Não confundir alcance de visão, raio AoE, AABB de controle e hitbox |
| Persistência | Overrides de \`MagneticWeaponEntity\` incluem \`WeaponStack\` e \`ControllerUUID\`, além da superclasse | \`playerUseCooldown\`, \`destroyBlockProgress\`, alvo, ownership, return/cleanup e estados após reload **não homologados como restaurados** |
| Mundo e rede | Operações de dano e quebra são provider/engine-native, com event hooks e possibilidade de veto | Multiplayer, claims, PvP, antirreplay, item stacks forjados e efeito sob TPS reduzido exigem aceitação física |

**Autoridade:** Black Arcana mantém seu casting, domínios, Corruption, Strain, Arcane Danger, world safety e budgets; a gauntlet e a entidade magnética permanecem sob o provider. RPG Skill Tree pode informar progressão/perks/Mastery/gates somente mediante contrato real. Não há adapter mutador certificado, e alterar propriedades da ferramenta controlada pode gerar dano, mineração ou drops não autorizados. Em caso de dúvida: **NO_MUTATION / fail-closed**.

## 5. Pendências antes de homologar perks

1. Reconstruir o CFG completo do consumidor e a ordem de decremento de cooldowns, transições de alvo, resets, escolha de ferramenta e cancelamento de \`hurtEntity\` / \`destroyBlock\`.
2. Homologar um hook de alteração seguro (com timing e autoridade do servidor), caps por tick, compatibilidade com progressão do RPG Skill Tree e controle de dupla execução.
3. QA em modpack **1.0.10** com gauntlet encantada/normal, mão principal/secundária, Crystalization e Field Extension, ferramenta magnética incompatível, PvP, aliados, mobs, claims, blocos protegidos, drops, Mining Fatigue/Haste, Creative, quebra/cancelamento e servidores dedicados.
4. Testar save/reload, transferência de dimensão, devolução ou drop da ferramenta, perda do owner, mudança de mão, múltiplas entidades, packets, desconexão, edge TPS e contabilização de XP/Mastery sem duplicar proc.
5. Não promover \`perk_certification\` ou Stage somente por o JSON existir, pela CI de inspeção estática passar ou por a fonte pública 1.1.1 sugerir comportamento semelhante.

**Resultado:** \`SHA_EXACT_RESOURCE_AND_SELECTED_JVM_CONSUMER\` + \`PARTIAL_ENCHANTMENT_DOSSIER\`. **+1 ficha parcial; +1 manifesto nominal localizado, +0 contratos estáticos certificados adicionais, +0 hooks mutadores, +0 raízes mágicas e +0 promoção de Stage.** Próxima identidade alfabética: \`alexscaves:field_extension\`.
