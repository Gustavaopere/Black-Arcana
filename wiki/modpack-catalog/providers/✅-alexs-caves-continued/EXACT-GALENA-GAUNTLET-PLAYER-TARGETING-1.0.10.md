# Galena Gauntlet — alcance do raycast, cooldown e devolução da arma (publisher 1.0.10)

**Estado:** ⚠️ subcontrato técnico **estático SHA-exato**, leitura somente. `alexscaves:galena_gauntlet` permanece **`static_contract=NOT_CERTIFIED`**, `mutating_hook=NOT_VERIFIED`, `physical_qa=NOT_TESTED`, `NO_MUTATION`; universo do provider aberto. Esta auditoria **não cria novo cast**, não certifica perks, não testa combate/mineração e não reproduz código proprietário.

## 1. Identidade, autoridade e evidências

- **Modpack declarado:** Minecraft **1.21.1**, **NeoForge 21.1.248**, Java **21**; Alex's Caves Continued **1.0.10**, ID `alexscaves`, JAR `alexscaves-1.0.10-neoforge+1.21.1.jar`, SHA-1 da modlist sibling `6960b299a39a039ac8a5eb9b07be4ad0e3e0a570`. A paridade byte-a-byte com o JAR da instalação atual permanece `NOT_VERIFIED`.
- **Artefato publisher examinado:** 75.279.314 bytes, SHA-256 `36ae0a3cbd028df466a37c671ba2fdf021c060ca1c9c1c32e9f2e95bffae0e7c`; classe `GalenaGauntletItem` SHA-256 `5a74328a7130704a4e2dca9e607bed4dc3a468b8bbcb6d4e238b4d2d962573b0`; `MagneticWeaponEntity` SHA-256 `a26794c9eba89c554e812078886beda6129d5298219f685f6d0e2be315fbf071`.
- **Prova read-only pré-existente:** [discovery do item/entidade](EXACT-GALENA-GAUNTLET-DISCOVERY-1.0.10.md), [manifesto dos 17 + 24 métodos nativos](EXACT-GALENA-GAUNTLET-DISCOVERY-1.0.10.json), [workflow #44934418449](https://github.com/Gustavaopere/Black-Arcana/actions/runs/44934418449) e [artefato #14719225697](https://github.com/Gustavaopere/Black-Arcana/actions/runs/44934418449/artifacts/14719225697). O relatório completo `report.json` possui **1.780.492 bytes** e SHA-256 `c91a48f9892be09c4ab951c8083703b0c5ffbb026fc43e7d808c2033dde8bba9`.
- **Novo recorte certificado somente quanto à observação estática:** quatro métodos executáveis da `MagneticWeaponEntity` (`tick`, `isOwnerWearingGauntlet`, `plopItem`, `getTarget`) com classe, descritores, Code SHA, instruction SHA, lista completa de offsets e **68 pivôs** verificados por [manifesto](EXACT-GALENA-GAUNTLET-PLAYER-TARGETING-1.0.10.json), [checker causal](../../../../docs/qa/alexscaves_1010_galena_gauntlet_tick_checks.py), [testes negativos](../../../../docs/qa/alexscaves_1010_galena_gauntlet_tick_negative.py) e [CI](../../../../.github/workflows/alexscaves-1010-galena-gauntlet-tick-causal.yml). Verificar CI na HEAD final antes de declarar PASS. Os **demais 20 métodos** da entidade e a engine não recebem certificação por transitividade.

## 2. Condições para controlar a arma

`isOwnerWearingGauntlet():boolean` verifica o controller @1, exige que seja `LivingEntity` @6, que `LivingEntity.getUseItem()` corresponda a `ACItemRegistry.GALENA_GAUNTLET` @18–32, que o controller esteja **vivo** @39 e que `returnFlag` seja **false** @46–49. Retorna `true` exclusivamente no ramo favorável @52; todos os demais retornam `false` @56. **Portar a luva no inventário ou tê-la meramente equipada não basta:** essa rota verifica o item atualmente em uso.

No `MagneticWeaponEntity.tick():void`, a ramificação de controller Teletor (`instanceof TeletorEntity` @170) é distinta da ramificação do jogador (`instanceof Player` @471). Para jogador, a rotina ajusta `comingBack` com base em `isOwnerWearingGauntlet` @519–530; quando a verificação falha @540–544, avança para a lógica de retorno @1416. Portanto os números seguintes descrevem a **rota do player com gauntlet ativa**, não a arma de Teletor.

## 3. Alcance do raycast: fórmula observada

Na ramificação do jogador, a variável de distância do raycast recebe **`30.0f`** @552. Se o controller for `LivingEntity` e seu `getUseItem()` corresponder à `GALENA_GAUNTLET` @577–596, o método lê o nível de `ACEnchantmentRegistry.FIELD_EXTENSION` via `ACCompat.enchantLevel` @624–632, converte o nível `int` para `float` e calcula os operadores JVM @634–644.

**Distância nominal passada ao helper:**

\[
R_{\text{raycast}} = 30.0f + 5.0f\times E_{\text{Field Extension}}
\]

- **Unidade:** distância usada na chamada a `ProjectileUtil.getHitResultOnViewVector` @649–659, convertida para `double` com `f2d`, não raio de AOE, dano, alcance de contato ou distância garantida de impacto.
- **Origem de `E`:** retorno de `ACCompat.enchantLevel` para a stack de Gauntlet em uso. O método local **não executa clamp próprio** nesse cálculo; níveis efetivos autorizados por registries, datapacks e a engine não foram verificados.
- **Sem gauntlet em uso no teste local de @593:** o incremento do encantamento não é aplicado e a variável conserva **30.0f**, mas a função `isOwnerWearingGauntlet` pode impedir que a rota ativa seja alcançada.
- **Filtro do raycast:** o método passa um `Predicate` construído por `invokedynamic` @651 ao helper. O destino/bootstrap do predicado, a semântica de exclusão de aliados/creativo/PvP e o comportamento interno de `ProjectileUtil` **não foram auditados nesta etapa**. A fórmula acima é **argumento de chamada**, não prova de alvo realmente válido.

O valor **64** da `AABB.inflate(64,64,64)` no `GalenaGauntletItem.onUseTick` é apenas o espaço de procura por outras instâncias da arma; não deve substituir o `R` do raycast da entidade.

## 4. Ataque, progresso e cooldown condicional

O método `tick` entra no ramo de `EntityHitResult` @664–669 somente se o helper produzir esse tipo. No momento da avaliação da arma, o campo `playerUseCooldown` precisa ser **zero** para alcançar a lógica de alvo (@679–683). Para o alvo obtido, pede `distanceTo(target)` @720–723 e compara o resultado com `target.getBbWidth() + 1.5f` @726–736: o ataque local exige estritamente **distância menor que largura do alvo + 1,5**, não raio de 1,5 bloco nem teste de hitbox já comprovado como aceito.

Se `strikeProgress < 1.0f`, solicita progresso `Math.max(0.0f, strikeProgress + 0.35f)` @739–763. Essa janela **não faz clamp superior explícito a 1**. Quando `strikeProgress >= 1.0f` e os guardas anteriores permitem, chama `hurtEntity(player,target)` @766–771. O resultado da aplicação de dano não é devolvido diretamente a esse `tick`; o callback `hurtEntity` tem validação própria e deve ser auditado separadamente.

Para a arma do player que usa a Gauntlet, `FERROUS_HASTE` é lido de `getUseItem()` @606–622. O ramo aceita presença positiva do encantamento (`E>0`) como booleano, **não escala linearmente com o nível** no cálculo local de cooldown. Após o pedido de `hurtEntity`:

| Condição da Gauntlet em uso | Valor solicitado a `playerUseCooldown` |
|---|---|
| `FERROUS_HASTE > 0` | **3 ticks** |
| Sem nível positivo | **`5 + RandomSource.nextInt(5)`**, intervalo inteiro **5–9 ticks** |

Offsets causais @774–796; a contagem decresce em uma unidade por `tick` enquanto positiva @1554–1568. **Não confundir com o cooldown de 5 ticks da própria Gauntlet em `releaseUsing`**, nem com um intervalo físico garantido de ataques. A rotina de Teletor possui um callback diferente @382 e não recebe automaticamente essa regra de player.

## 5. Mineração e efeitos de mundo — somente a fronteira

Na seleção de bloco, `tick` consulta `BlockState.getDestroySpeed` @1013 e `getDigSpeed(player,state,pos)` @1025. O ramo local só prossegue para a janela principal de progresso quando `getDigSpeed > 1.0f` @1030–1034. A tentativa de mineração em `tick` contém **dois** sites `Level.destroyBlock` (@1290, @1329), mas estão condicionados a caminhos e guardas diferentes; isso **não comprova duas quebras por tick, contorno de proteções ou sucesso de ambas**. Outras verificações de dureza, estado/permissions do bloco, ferramentas, drops, efeitos de mineração e eventos precisam ser conciliadas com a engine e com `getDigSpeed` integralmente auditado.

`NO_MUTATION`: o Black Arcana não deve interceptar esses sites para substituir `WorldEffectPolicy` ou contornar permissões do provider. Nenhuma prova de mutação segura, XP/perk ou integração world-safety decorre desta auditoria.

## 6. Retorno, inventário e descarte

Quando o controller player deixa de usar uma Gauntlet elegível, o ramo de retorno @1416 solicita aumentar `returnProgress` por **`Math.min(1.0f, returnProgress + 0.2f)`** @1417–1438 (não implica linearidade temporal real sem ticks medidos). Para tentativa de devolução por inventário, exige distância ao controller **menor que 1,4** no teste @1483–1493, que a entidade ainda não esteja removida e que `spawnedItem` seja falso. Então chama `Player.addItem(getItemStack())` @1510–1519:

- **Se `addItem` retornar `true`:** solicita `spawnedItem=true` @1522–1524 e `remove(DISCARDED)` @1527–1531.
- **Se a devolução falhar ou o ramo `spawnedItem` já tiver sido tratado:** existe o percurso que chama `plopItem()` @1537–1538. Não inferir sucesso de spawn ou ausência de duplicação/loss pela presença do ramo.
- **`plopItem` observado:** se `spawnedItem` ainda é falso, marca verdadeiro @7–9, solicita `ACCompat.spawnAtLocation(this,getItemStack())` @12–17, e se o retorno de `ItemEntity` não for nulo solicita `setNoPickUpDelay()` @21–26; em todo caso solicita `remove(DISCARDED)` @29–33. Resultado físico de drop/inventário, eventos externos e persistência **não foram testados**.
- **Target sincronizado:** `getTarget()` lê `TARGET_ID`; sentinela inteiro **−1** devolve `null` @17–23, caso contrário solicita `Level.getEntity(id)` @26–31. A presença de um ID não prova vida, alcance nem identidade persistente do alvo.

Os controles de owner/retorno também dependem de `ControllerUUID` e do estado sincronizado do entity type auditados na [ficha base](equipment/galena-gauntlet.md); o desenho completo de reinserção após reload/dimensão continua aberto.

## 7. Vetores de perks e pendências de certificação

**Potenciais parâmetros de design** (não hooks): distância nominal do raycast `R`; progresso até contato; cooldown de ataques da entidade; degradação da stack controlada; velocidade de retorno; duração de uso; targeting permitido e condições de mineração. Black Arcana não pode assumir que é seguro alterar nenhum desses parâmetros sem localizar um boundary *real e autorizado*; RPG Skill Tree atua apenas sobre progressão/atributos/Mastery/gates por contrato, sem alterar a lógica de `MagneticWeaponEntity`.

**Pendente:** ligação do `Predicate` invokedynamic, efeitos finais de `ProjectileUtil`, computação e aplicação de dano/PvP, ramificações completas de Teletor, caminho integral de mineração/drops, integridade do inventário em falha de spawn, sincronização/reload, mods/claims externos, paridade do JAR físico e QA cliente/dedicated-server/modpack. Não validar `addFreshEntity`, destruição de blocos nem cooldown real por mera leitura do classfile.

O novo relatório é reutilizado **sem reutilizar certificação de consumidor**; esta observação estática é auditável individualmente pelo manifesto e testes adversariais. **Sem fechamento do contrato integral da Galena Gauntlet, sem atualização de `PERK-READY-CERTIFICATIONS.json`, sem alteração de índices gerados, sem nova raiz mágica e sem runtime modificado.**
