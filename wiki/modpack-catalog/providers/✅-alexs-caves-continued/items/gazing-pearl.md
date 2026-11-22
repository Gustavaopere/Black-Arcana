# Gazing Pearl — indicador passivo de reputação dos Deep Ones (1.0.10)

**Estado: ⚠️ PARCIAL.** Identificação e recorte causal SHA-exatos do publisher, sem certificação técnica individual integral. NO_MUTATION; mutating_hook=NOT_VERIFIED; physical_qa=NOT_TESTED; perks_executable=NOT_CERTIFIED; universo integral OPEN. Não é um novo spell/cast nem concede uma nova raiz mágica.

## Identidade, descrição e proveniência

**Provider:** Alex's Caves Continued, mod ID alexscaves, Minecraft 1.21.1/NeoForge/Java 21; runtime 1.0.10. **Item:** alexscaves:gazing_pearl / ACItemRegistry.GAZING_PEARL, classfile com/github/alexmodguy/alexscaves/server/item/GazingPearlItem. **JAR publisher observado:** alexscaves-1.0.10-neoforge+1.21.1.jar, 75.279.314 bytes, SHA-1 6960b299a39a039ac8a5eb9b07be4ad0e3e0a570, SHA-256 36ae0a3cbd028df466a37c671ba2fdf021c060ca1c9c1c32e9f2e95bffae0e7c. Novo dump do artefato instalado não foi comparado. **SHA-256 da classe:** 2519bc5aed494deccc0423053ea42904314511094b29cd1e4025cc65a08a5a07; cinco corpos, zero campos próprios e três owners consumidores tipados (ClientProxy, ACItemRegistry e própria classe).

**Descrição funcional:** item de informação que armazena temporariamente na stack um retrato da reputação Deep One do UUID da entidade portadora, apresentando-o por tooltip e cor HSB animada. A classe da pérola não altera a reputação armazenada no mundo. A árvore pública de outra revisão (1.1.1) foi apenas referência de descoberta; os hashes acima são do publisher 1.0.10.

## Ativação, condições, tempo e estado

**acInventoryTick(ItemStack,Level,Entity,boolean)**, 46 instruções: exige servidor (Level.isClientSide @1–4); lê LastReputationTimestamp (long). Se timestamp <=0 ou se gameTime−timestamp **>100 ticks** (comparação estrita), consulta ACWorldData.get(level). Se retornar dados não nulos, solicita putLong(LastReputationTimestamp,gameTime), putBoolean(HasReputation,true), putInt(Reputation,ACWorldData.getDeepOneReputation(entity.getUUID())) e ACCompat.setTag(stack,tag). Sem dados de mundo, a rotina não escreve esse snapshot nesta janela. O dispatcher ACTickingItem é documentado separadamente em [ticking-item](../systems/ticking-item.md). Não há guarda própria Player, held ou selected no corpo da Gazing Pearl; a entidade recebida pelo callback fornece o UUID.

**appendHoverText**, 38 instruções: lê HasReputation e Reputation da stack, chama DeepOneReaction.fromReputation, seleciona chave de tradução pela categoria em minúsculas Locale.ROOT, solicita Component.translatable cinza/itálico e delega ao ancestral. Sem flag verdadeira, o texto específico não é adicionado. Valor traduzido final e frequência de atualização visual no cliente dependem da engine/instalação.

**getPearlColor(ItemStack):int**, **73 instruções**: fórmula HSB do publisher agora auditada estaticamente e reproduzida pelo [checker SHA-exato](../../../../../docs/qa/alexscaves_1010_gazing_pearl_color_checks.py), sem certificar apresentação física. Com tag e `HasReputation=true`, lê `Reputation=R` e calcula a **matiz `H=float(100-R)/200.0F`**, com subtração inteira antes da conversão, `S=0.7F+0.3F * ((float)(1+sin((double)((float)t/4000.0F)))*0.5F)` e brilho `B=1.0F`; chama `java.awt.Color.HSBtoRGB(H,S,B)` @63. Sem a flag, usa `H=float(t1%10000L)/10000.0F` e a mesma fórmula de saturação com uma **segunda leitura independente** de `currentTimeMillis()` (`t2`); `HSBtoRGB` @110. Não há clamp explícito de H/S no método, nem limite baseado em Mastery. A conversão JVM `l2f` ocorre antes de dividir milissegundos por 4000: em 22/11/2026, a distância entre valores `float32` adjacentes da época Unix é **131.072 ms** (conferência numérica Java 21), podendo produzir mudanças visuais em degraus. **Resultado de renderização e sincronismo entre clientes NOT_TESTED**. Ver [dossiê](../EXACT-GAZING-PEARL-DISCOVERY-1.0.10.md).

**Construtor** (10 instruções) solicita stacksTo(1) e Rarity.UNCOMMON. **shouldCauseReequipAnimation** (16) retorna false quando ambas as stacks são Gazing Pearl; eventuais effects externos do render/engine permanecem não verificados. Duração de status, cooldown, mana, dano, projétil, alcance e AOE próprios: **N/A nos cinco métodos locais**; não confundir com contratos dos Deep Ones.

## Reação nativa, targeting e consumidores

**DeepOneReaction** classfile SHA-256 5898cd4286885ad85e92065f68bff883131e921af295b781b806e076ff1e54dc: nove métodos, sete campos e sete consumidores. O fromReputation(int) usa os limiares JVM −10, 10 e 30:

| Reputação inteira | Resultado |
|---|---|
| até −10 | AGGRESSIVE |
| −9 a 10 | STALKING |
| 11 a 30 | NEUTRAL |
| 31 ou mais | HELPFUL |

A classificação é o dado que o tooltip consulta. Os métodos de IA validPlayer/getMinDistance/getMaxDistance e consumidores DeepOneReactToPlayerGoal, DeepOneTargetHostilePlayersGoal e DeepOneBaseEntity pertencem a **outro** contrato de reação dos mobs. Distância/hostilidade nativas não são buffs da pérola nem autorização para perk de manipulação de IA.

**Target:** UUID da entidade portadora recebido pelo callback; não há seleção de entidade por mira, hitbox, área ou cálculo de alcance no item. **Owner:** a stack armazena snapshot Reputation/HasReputation e timestamp; não persiste um owner UUID próprio no recorte. **Persistência:** ACCompat acessa tag da stack; reload, desconexão, passagem entre dimensões, relógio recuado, datapacks, multiusuário e sincronização de ItemStack estão **NOT_TESTED**. A consulta é temporalmente defasável durante o intervalo de >100 ticks.

## Custos, recursos e fronteiras de perk

O publisher inclui receita shapeless **1 Gazing Pearl + 1 Marine Snow → 1 Pearl** em data/alexscaves/recipe/pearl_from_gazing_pearl.json, SHA-256 663ecb4f1b80e92a251e541e6a9b2c312efecccfd322f959d81ecc2e8b4e14d2 (282 bytes). A receita **consome a Gazing Pearl como ingrediente**, não demonstra sua aquisição inicial nem crafting efetivo no pack. Modelo de item em assets/alexscaves/models/item/gazing_pearl.json, SHA-256 a1fd223aa8c09ce52ff113c20cbeb6efec3f1b027297254f28c9303c43930d03. Nenhum gasto de mana, cooldown, desgaste por tick ou consumo por consulta é solicitado nos corpos do item.

**Perks de reputação:** ACWorldData.getDeepOneReputation(UUID) é fonte do snapshot; não há setter mutador autorizado nesta ficha. Alterar o NBT da pérola não altera reputação real. **Perks de cadência:** não duplicar dispatcher ACTickingItem nem escrever timestamp para simular progresso. **Atributos, alvo e Mastery:** nenhum evento de dano/cast/kills da pérola; não premiar XP por leitura ou cor. Black Arcana mantém autoridade do runtime mágico e world safety, e RPG Skill Tree integra progressão/Mastery somente por boundary real. Sem hook confirmado: **NO_MUTATION/fail-closed**.

## Evidências, hashes e gates

[Dossiê causal](../EXACT-GAZING-PEARL-DISCOVERY-1.0.10.md), [manifesto SHA-exato de 14 métodos](../EXACT-GAZING-PEARL-DISCOVERY-1.0.10.json), [sonda read-only](../../../../../docs/qa/alexscaves_1010_gazing_pearl_discovery.py) e [workflow](../../../../../.github/workflows/alexscaves-1010-gazing-pearl-discovery.yml). Run [44936198921](https://github.com/Gustavaopere/Black-Arcana/actions/runs/44936198921), job 136943226304 PASS, report SHA-256 d73959ca968bd23e57240d2fb3943e400362af9da92940af7343e93f47ff01c5; artefato 14719307762, ZIP SHA-256 99adb9c94f95711e5cac1a80c8156a5476e467ddf5761e222ef2ec5a8592ce02, expiração declarada 05/12/2026.

**Pendente para ✅:** verificar interproceduralmente ACWorldData, aplicação e reação da IA quando relevante, recursos/traduções e ItemStack herdado; checar renderer e efeitos aceitos; novos bytes da instalação, QA física e hooks. A sonda de hash não certifica resultados no mundo. Clean-room: não foram copiados bytecode/assets/implementações de terceiros ao runtime.
