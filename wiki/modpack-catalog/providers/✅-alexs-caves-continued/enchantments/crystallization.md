# Crystallization — elegibilidade expandida da Galena Gauntlet (publisher 1.0.10)

**Estado:** ⚠️ ficha individual **parcial/condicionada**, com recursos publisher e consumidores JVM selecionados SHA-exatos. `NO_MUTATION` · `mutating_hook=NOT_VERIFIED` · `physical_qa=NOT_TESTED` · `perk_certification=NOT_CERTIFIED`. Nenhuma mutação de targeting, inventário, dano, cooldown ou mineração do provider está autorizada por esta ficha.

**Identidade semântica:** `alexscaves:crystallization` **não converte materiais em cristal**, não cria novo projétil nem uma magia independente. Ele permite que a **Galena Gauntlet** escolha um conjunto mais amplo de itens na **outra mão** para o mecanismo já existente de arma/item magnético controlado pelo jogador. O ataque, a mineração, o retorno do item e os modificadores de alcance pertencem à entidade nativa `MagneticWeaponEntity` e não são poderes exclusivos de Crystallization.

## 1. Release e evidência reprodutível

- **Provider:** Alex's Caves Continued (`alexscaves`), Minecraft **1.21.1 / NeoForge**.
- **JAR publisher exato:** `alexscaves-1.0.10-neoforge+1.21.1.jar`, **75.279.314 bytes**, SHA-1 `6960b299a39a039ac8a5eb9b07be4ad0e3e0a570`, SHA-256 `36ae0a3cbd028df466a37c671ba2fdf021c060ca1c9c1c32e9f2e95bffae0e7c`.
- **Recurso publisher:** `data/alexscaves/enchantment/crystallization.json`, SHA-256 `b2394e226f7d31843e6d459ef48e21bb955be3d174b3d63eb7ef0a66f0fee3da`, **386 bytes**.
- **Prova técnica:** [manifesto exato](../EXACT-CRYSTALLIZATION-1.0.10.json), [sonda somente leitura](../../../../../docs/qa/alexscaves_1010_crystallization_probe.py), [regressões sintéticas](../../../../../docs/qa/alexscaves_1010_crystallization_probe_test.py) e [workflow dedicado](../../../../../.github/workflows/alexscaves-1010-crystallization.yml).
- **Fonte pública adjacente:** `Codx-org/AlexsCavesContinued@523308608422ab8e31974befa7111ecdf495dd37` declara versão **1.1.1**. A descrição textual e o fluxo de referência ajudam a interpretar o efeito, mas **somente os hashes, os recursos e as janelas JVM extraídos do publisher 1.0.10** são prova dos parâmetros desta ficha. Não presumir paridade automática entre essas versões.
- **Clean-room:** não foi adicionado nenhum código, asset, runtime externo ou implementação proprietária ao Black Arcana; o manifesto armazena dados declarativos e janelas limitadas de interop.

## 2. Contrato de encantamento

| Campo do recurso `crystallization.json` | Valor comprovado no JAR 1.0.10 |
|---|---|
| `description.translate` | `enchantment.alexscaves.crystallization` |
| `supported_items` | `#alexscaves:enchantable/galena_gauntlet` |
| `weight` | `2` — peso de obtenção, **não** chance de controlar item |
| `max_level` | `1` (I); não há ganho incremental de força por nível na seleção observada |
| `min_cost` | `base=1`; `per_level_above_first=15` |
| `max_cost` | `base=41`; `per_level_above_first=10` |
| `anvil_cost` | `4` |
| `slots` | `mainhand` e `offhand` |
| `exclusive_set` | Não declarado no JSON físico |

**Item elegível para receber o encantamento:** `data/alexscaves/tags/item/enchantable/galena_gauntlet.json`, SHA-256 `5f8a2dfe1222c6631122855a11ab011d916bea83d285d6ecd886a177c058c4cb`, lista `alexscaves:galena_gauntlet`.

**Elegibilidade da outra mão quando Crystallization está presente:** `data/alexscaves/tags/item/galena_gauntlet_crystallization_items.json`, SHA-256 `a66bc2d0071dac61445130165f3acbd050694a8613113d47293237557167fd05`, contém **10 entradas declarativas**:

- `#alexscaves:ferromagnetic_items` — conjunto básico, por referência à tag, não cópia estática dos itens finais.
- `alexscaves:desolate_dagger`.
- `minecraft:diamond`, `minecraft:quartz` e `minecraft:amethyst_shard`.
- `minecraft:diamond_sword`, `minecraft:diamond_pickaxe`, `minecraft:diamond_axe`, `minecraft:diamond_shovel` e `minecraft:diamond_hoe`.

A tag básica física `data/alexscaves/tags/item/ferromagnetic_items.json`, SHA-256 `d56b9514fe890d6b4eb1e256fd418683e7ec9aeb7032592168671f6851548dbf`, tem **82 entradas declaradas** (incluindo referências a tags). **82 não é contagem de itens resolvidos em jogo**: referências, datapacks, aliases, sobrescritas e outros mods podem alterar o conjunto efetivo.

O encantamento **escolhe uma tag alternativa**; não altera seu conteúdo, não concede uma nova regra de dano ou uma classe de projétil, e não fornece garantia de que todos os itens aceitos sejam armas eficazes ou ferramentas aptas a minerar blocos. Os custos de encantamento não são mana, durabilidade por cast ou cooldown.

## 3. Aquisição no `GalenaGauntletItem` — método `use`

**Classfile** `com/github/alexmodguy/alexscaves/server/item/GalenaGauntletItem.class`, SHA-256 `5a74328a7130704a4e2dca9e607bed4dc3a468b8bbcb6d4e238b4d2d962573b0`. Método `use(Level,Player,InteractionHand)InteractionResultHolder`, descritor JVM `(Lnet/minecraft/world/level/Level;Lnet/minecraft/world/entity/player/Player;Lnet/minecraft/world/InteractionHand;)Lnet/minecraft/world/InteractionResultHolder;`, **47 instruções parseadas**, digest `14afa5ada8379f8f6706aa4cc713055fb43d5b154465ef5351f3c4f6e8fb8ac1`.

1. Lê a stack da Gauntlet e o item na **mão oposta**. Resolve `ACEnchantmentRegistry.CRYSTALLIZATION @35` com `ACCompat.enchantLevel @38`, usando `E>0` como condição booleana.
2. Escolhe `GALENA_GAUNTLET_CRYSTALLIZATION_ITEMS @58` se encantada; caso contrário, `MAGNETIC_ITEMS @64`. A verificação efetiva é `ItemStack.is(TagKey) @67`. **Não há fórmula de alcance, velocidade, dano ou duração por `E` neste seletor**.
3. Se a outra stack não pertence à tag escolhida, chega à resposta `useFail @100`. Se é elegível e o jogador **não** é criativo, solicita **1 ponto de durabilidade da Gauntlet** via `ACCompat.hurtAndBreakUsedHand @84`; em seguida solicita `Player.startUsingItem @89` e `useConsume @94`.
4. A ordem é importante: o desgaste é solicitado **na ativação**, antes da tentativa posterior de materializar a entidade em `onUseTick`. Não há reembolso nessa janela se a inserção falhar; o resultado final dependerá da engine e do ambiente.

**Limites:** `E` 1 habilita a nova tag; nível acima de I não é certificado nem deve ser promovido a atributo escalável. `mainhand/offhand` no JSON é informação de suporte, não um hook para duplicar itens/controles. A interação real de mãos, cooldowns herdados e tags carregadas precisa de QA física.

## 4. Canalização e transferência de inventário — `onUseTick`

Mesmo owner/classfile; método `onUseTick(Level,LivingEntity,ItemStack,int)V`, descriptor `(Lnet/minecraft/world/level/Level;Lnet/minecraft/world/entity/LivingEntity;Lnet/minecraft/world/item/ItemStack;I)V`, **120 instruções**, digest `fa87f2565ad1df622d3fe09b806541663f1bb787d84caec4e7b5e949e2781523`.

- A rotina consulta novamente `CRYSTALLIZATION @67` e a tag especial `@90` ou a tag base `@96` antes de trabalhar com a stack da mão oposta; o ramo de exclusão não cria uma nova ação.
- Para evitar empilhar mais de uma instância **identificada no recorte**, consulta entidades `MagneticWeaponEntity` dentro de uma **AABB do `LivingEntity` inflada em 64 unidades nos três eixos**: constantes `64D @112/@115/@118`, `AABB.inflate @121` e `Level.getEntitiesOfClass @124`. **Não é raio esférico de ataque, alcance de raycast ou garantia de deduplicação global/multichunk**. A identificação do controller depende de um owner válido; instâncias fora da caixa ou de outro nível não são cobertas por essa consulta.
- Caso não encontre outra arma elegível sob controle, copia `otherStack` `@193`, zera a stack original por `ItemStack.setCount(0) @201`, solicita `ACCompat.createEntity @216`, transfere a cópia por `setItemStack @228`, posiciona a entidade acima do usuário, escreve seu UUID em `setControllerUUID @252` e tenta `Level.addFreshEntity @258`.
- **Risco de inventário (estático):** `setCount(0)` ocorre **antes** de `addFreshEntity`, e o booleano desta última é descartado (`pop @261`). A cadeia selecionada não mostra rollback da stack nesse ponto. Isso **não confirma perda de itens real** em servidor ou cliente, mas impede uma perk que refaça, reproduza, aumente o número de entidades ou reordene a transferência de inventário sem contrato transacional verificado.
- O recorte não certifica guarda global de lado, permissão de claims, aceitação de spawn, null safety do factory, proteção de inventários, desconexão, colisões ou restituição ao jogador. A entidade e a engine são autoridades dessas transições.

A consulta em AABB 64 ocorre no ciclo de uso e é **um custo/scan nativo**. Black Arcana não deve acrescentar outro scan por tick nem espelhar essa lógica sem budget e interface explícitos.

## 5. Movimento, aquisição de alvo e efeitos da entidade

A entidade `com/github/alexmodguy/alexscaves/server/entity/item/MagneticWeaponEntity.class` possui SHA-256 `a26794c9eba89c554e812078886beda6129d5298219f685f6d0e2be315fbf071`.

| Método JVM delimitado | Evidência exata |
|---|---|
| `tick()V` | **744 instruções**, digest `b68e9174310dc32ea5ce7bbe627955d18e92db9e1c087d741a63cfb4ea251f41` |
| `hurtEntity(LivingEntity,Entity)V` | **141 instruções**, digest `81ce00054738e5b73fac709f467f51156ff6868c9d0098b7e96cc2b27318c193` |
| `getController()Entity` | **34 instruções**, digest `4fffb40a928b5b2ac381dfd60cddfce43551ae3b064f9f81a5f6f48ab76169bd` |
| `getTarget()Entity` | **17 instruções**, digest `8057ae056c4f46ea485047967eda6a4ab09962ee9d17bb3c9ff8e6796318bb69` |

As janelas do `tick` localizam **`FERROUS_HASTE @608`**, **`FIELD_EXTENSION @626`** e `ProjectileUtil.getHitResultOnViewVector @659`. `FIELD_EXTENSION` carrega uma constante `5.0F @639`; a fonte **adjacente 1.1.1** usa `30F + 5F×nível(FIELD_EXTENSION)` para a distância de busca, mas **a equação integral de 1.0.10 não foi reconstruída pelo manifesto seletivo**. Por isso, não registrar esse alcance como valor final certificado de Crystallization. O encantamento catalogado **não** aparece como seletor de raycast, multiplicador de range ou velocidade nessa região; ele atua anteriormente, na tag de item.

Duas solicitações `hurtEntity` ocorrem em ramos do `tick` (`@382` e `@771`), mas não significam dois ataques por uso. O método `hurtEntity` solicita `damageSources().mobAttack(holder)`, aplica `ACCompat.hurt @99`, seguido condicionalmente por `postAttackEffects @115` e `damageItem(1) @120` quando o booleano de dano é positivo. O path do item controlado também tem `ItemStack.hurtEnemy @239`. **Não há dano fixo, `DamageType` novo nem AoE fornecidos por Crystallization**; status e dano realmente aceitos, bônus de itens e eventos externos requerem validação própria.

O `tick` selecionado contém chamadas de `Level.destroyBlock @1290/@1329` e manipulação de `destroyBlockProgress`; são **mecânicas de mineração da arma magnética**, não uma autorização de Crystallization a quebrar blocos via Black Arcana. Integração destrutiva própria continua sujeita ao `WorldEffectPolicy` do projeto.

`getController` distingue recuperação de controller por identidade e lado, enquanto `getTarget` usa `TARGET_ID` da `Level` local. Os métodos `addAdditionalSaveData`/`readAdditionalSaveData` possuem referências a `WeaponStack` e `ControllerUUID` (digests próprios no manifesto). A presença desses campos **não garante** recuperação íntegra após crash, devolução de item, autoria de dano, dedupe de Mastery ou compatibilidade em multiplayer.

## 6. Custo, cooldown e riscos

O método publisher `GalenaGauntletItem.releaseUsing(ItemStack,Level,LivingEntity,int)V` possui **25 instruções**, digest `f955156370b46a5319ec67b325a149136682c5e4b23a564c5c8ed639d0b5bbf0`; quando é Player, solicita `ACCompat.addCooldown(player,stack,5) @26`. **Cinco ticks é argumento do cooldown na liberação**, não duração da entidade, vida de projétil, intervalo de cada ataque ou custo adicional exclusivo de Crystallization.

A entidade mantém também rotas nativas para atacar, minerar, retornar à mão ou soltar o item. Os caminhos de `plopItem`/`WeaponStack`/`ControllerUUID` foram selecionados, mas nem sucesso de retorno, nem rollback, nem conservação de inventário foram reproduzidos em mundo físico.

**Atenção para o design de perks:** uma perk que permita mais tipos de itens poderia, em tese, ampliar a tag elegível **se a API/datapack e a versão exata suportarem essa configuração**; porém, alterar tags e inventário não é automaticamente um hook de runtime seguro. Nenhuma mutação foi testada. Não interceptar `setCount`/`addFreshEntity`, não duplicar `MagneticWeaponEntity`, nem submeter itens de outros mods a mineração e dano sem compatibilidade/segurança comprovadas.

## 7. Matriz para RPG Skill Tree / Black Arcana

| Eixo de perk | Informação útil observada | Limite atual |
|---|---|---|
| **Elegibilidade e tipo de alvo** | Seleção entre `MAGNETIC_ITEMS` e `GALENA_GAUNTLET_CRYSTALLIZATION_ITEMS` baseada em `E>0`; outras stacks na offhand/mainhand | ⛔ Não converter item-alvo em entidade-alvo/AoE ou adicionar tags sem validação |
| **Range / aquisição** | Scan de controle: AABB inflada `64D`; raycast da entidade nativa; `FIELD_EXTENSION` é outro encantamento | ⛔ Não aplicar multiplicador de alcance a Crystallization nem repetir scan |
| **Dano e tipo** | `mobAttack(holder)` de `MagneticWeaponEntity`, efeitos e bônus do item | ⛔ Não estabelecer dano fixo, nova escola ou proc por item controlado |
| **Projétil, velocidade e quantidade** | Cria `MagneticWeaponEntity` que carrega uma cópia de `ItemStack`; não um projétil cristalino | ⛔ Sem resize/hitbox, duplicação de entidade, disparo extra ou velocidade por nível |
| **Tempo e cooldown** | `releaseUsing` solicita cooldown de `5`; tick da arma tem estado e controles próprios | ⛔ Sem segundo cooldown, prorrogação arbitrária ou replay |
| **Custo e inventário** | `hurtAndBreakUsedHand(...,1)` antes do uso, `setCount(0)` antes de `addFreshEntity` | ⛔ **Risco de perda** sob spawn falho; não implementar mutação ou refund sem settlement |
| **Mining / world safety** | Código nativo `destroyBlock`/`destroyBlockProgress` da entidade | ⛔ Não autoriza quebrar blocos fora do `WorldEffectPolicy` |
| **Mastery / autoria / persistência** | Controller UUID, alvo via ID, `WeaponStack` NBT e comandos nativos `hurt`/`hurtEnemy` | ⛔ Sem XP por tick/entidade/colisão, sem autoria segura ou dedupe de hits sem contrato |

**Fronteiras:** Black Arcana controla seu próprio runtime mágico e segurança do mundo. RPG Skill Tree fornece progressão, atributos, Mastery, perks e gates **através de contratos reais**. Crystallization continua sendo um efeito provider-native de **seleção de item**, não um novo cast nem um runtime de magia independente.

## 8. Limites da certificação e contadores

**Comprovado no JAR 1.0.10:** hash do publisher; quatro recursos declarativos/tag e seus hashes; identity/level/slots/custos; seleção das tags; consulta em AABB 64; transferência de stack por cópia com limpeza anterior ao spawn; player UUID; cooldown solicitado; owners/classes e digests; janelas delimitadas de consumo da arma magnética, alvo, dano, mineração, retorno/persistência.

**Não testado/verificado:** funcionamento real do encantamento I nos dois slots; datapacks e tags resolvidas; controle com cada item da lista; acesso a inventários e transferência em negação de spawn; crash/restart; itens perdidos; client/server side; permissões; proteção de chunks; PvP; alvos, tiro e mineração reais; uso simultâneo; Mastery e atribuição de kills; mutating hooks e testes de integração no modpack. Nenhuma linha física recebe `PASS` por causa da CI.

**Estados:** `VERIFIED_EXACT_BINARY_SELECTED_WINDOWS`; `mutating_hook=NOT_VERIFIED`; `physical_qa=NOT_TESTED`; `perk_certification=NOT_CERTIFIED`; `NO_MUTATION`.

**Contabilidade:** **+1 ficha individual parcial**; **+0 certificado estático novo no ledger**; **+0 raízes mágicas próprias**; **+0 providers com catálogo encerrado**. Próxima entrada alfabética: `alexscaves:dark_nock`.
