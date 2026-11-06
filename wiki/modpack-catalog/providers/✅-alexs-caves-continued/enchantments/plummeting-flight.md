# Plummeting Flight — `alexscaves:plummeting_flight` (Alex's Caves Continued 1.0.10)

**Contrato técnico individual:** ✅ no escopo **estático** `STATIC_TECHNICAL_CATALOG_ONLY` / `SHA_EXACT_BINARY_BEHAVIOR`, sujeito à validação final da PR e dos índices. **Mutating hook:** `NOT_VERIFIED`; **QA física:** `NOT_TESTED`; **mutação:** `NO_MUTATION`. Este dossiê não afirma homologação de perks executáveis, integração no Black Arcana ou comportamento físico comprovado no modpack.

## 1. Identidade, versão e fonte

- **Provider:** Alex's Caves Continued, `mod_id=alexscaves`, versão publisher **1.0.10**, Minecraft 1.21.1 / NeoForge / Java 21. Confirmação: [modlist física sibling](https://github.com/Gustavaopere/neoforge-rpg-skilltree/blob/main/PROJECT-INSTRUCTIONS/modlist/modlist.md), entrada 019.
- **Artefato exato:** `alexscaves-1.0.10-neoforge+1.21.1.jar`, CurseForge projeto `1645389`, arquivo `8856293`; **75.279.314 bytes**, SHA-1 `6960b299a39a039ac8a5eb9b07be4ad0e3e0a570`, SHA-256 `36ae0a3cbd028df466a37c671ba2fdf021c060ca1c9c1c32e9f2e95bffae0e7c`.
- **Enchantment ResourceKey:** `alexscaves:plummeting_flight`; JSON `data/alexscaves/enchantment/plummeting_flight.json` (**374 bytes**, SHA-256 `163b032e37c716f0ef172a37b739a6d61340dab7c629c070698f8543999ec830`).
- **Inglês literal do `en_us.json`:** “Extinction Spear Subterranodon attack carries foes higher and for longer”. Tradução explicativa: o ataque Subterranodon da Extinction Spear carrega os alvos mais alto e por mais tempo. Não apareceu uma entrada específica desse encantamento no `pt_br.json` do JAR examinado.
- **Arma elegível:** `#alexscaves:enchantable/extinction_spear`. O recurso `data/alexscaves/tags/item/enchantable/extinction_spear.json` contém apenas `alexscaves:extinction_spear`, SHA-256 `950e56b0643bb55cb9acab23c3eecdfd75f6ee7ae3f1253d9866c3f2f7fdf5e7`.

Fonte primária: sonda [`alexscaves_1010_plummeting_flight_probe.py`](../../../../../docs/qa/alexscaves_1010_plummeting_flight_probe.py), que verificou SHA/tamanho do JAR e os recursos; [manifesto Spirit Dinosaur 1.0.10](../EXACT-SPIRIT-DINOSAUR-CONTRACT-1.0.10.json), com métodos completos do produtor e consumidor; [selo individual](../EXACT-PLUMMETING-FLIGHT-CONTRACT-1.0.10.json) e [escopo/reprodução](../EXACT-PLUMMETING-FLIGHT-CONTRACT-1.0.10.md). A fonte pública `Codx-org/AlexsCavesContinued@523308608422ab8e31974befa7111ecdf495dd37` declara **1.1.1**, portanto não foi usada para fixar parâmetros da versão 1.0.10.

## 2. JSON, níveis, custos e slots

| Campo | Publisher 1.0.10 | Limite de interpretação |
|---|---|---|
| `description.translate` | `enchantment.alexscaves.plummeting_flight` | Chave de tradução, não hook |
| `supported_items` | `#alexscaves:enchantable/extinction_spear` | Tag empacotada contém Extinction Spear |
| `weight` | **2** | Peso declarativo; não mede chances de hit |
| `max_level` | **3** | Níveis I–III publicados; leitura Java não é um clamp seguro |
| `min_cost` | base **1**, incremento **13** | I/II/III: **1 / 14 / 27** |
| `max_cost` | base **41**, incremento **10** | I/II/III: **41 / 51 / 61** |
| `anvil_cost` | **4** | Custo de encantamento, não durabilidade por impacto |
| `slots` | `["mainhand"]` | Slot declarado; validação de mão ativa pertence à engine |
| `effects` / `exclusive_set` | Ausentes do JSON | Não equivale a provar ausência de lógica Java ou compatibilidade universal |

O enchantment **não** é uma ação mágica nova. Sua leitura ocorre no caminho de um impacto aceito da **Extinction Spear arremessada**. A descrição inglesa não comprova valores finais de altura, duração de efeito, dano por queda ou colisão.

## 3. Ingresso: impacto aceito da Extinction Spear

O classfile `server/entity/item/ExtinctionSpearEntity.class` (SHA-256 certificado no [manifesto Spirit Dinosaur](../EXACT-SPIRIT-DINOSAUR-CONTRACT-1.0.10.json)) implementa `onHitEntity(EntityHitResult):void`. Seu contrato é distinto do `ExtinctionSpearItem.acHurtEnemy` de golpe corpo a corpo, que invoca **Tremorsaurus** e consulta `CHOMPING_SPIRIT`, não Plummeting Flight.

Sequência observada no bytecode da lança arremessada:

1. Obtém a entidade atingida (`@0–4`) e calcula `damageRequest=10F+ACCompat.damageBonus` **somente se o alvo for LivingEntity** (`@5–33`). O valor é pedido nativo, não dano efetivo.
2. Resolve owner e `ACDamageTypes.causeSpiritDinosaurDamage` (`@34–61`), marca `dealtDamage=true` antes da aceitação, solicita `igniteForSeconds(5F)` antes de `ACCompat.hurt` (`@81–95`).
3. **Só no ramo em que `ACCompat.hurt` retorna true** (`@95–98`) prossegue aos efeitos posteriores. Se o alvo for **Enderman**, retorna em `@108` sem invocar o espírito.
4. Quando há owner não nulo (`@148–150`), solicita `ACCompat.createEntity(DINOSAUR_SPIRIT,level)` e configura a entidade espiritual `SUBTERRANODON` (`@153–204`). Posiciona no X/Z do alvo e em Y correspondente à altura dele (`target.getY()+target.getBbHeight()`, `@176–198`).
5. Grava UUID do owner como Player UUID (`@207–214`) e o **ID runtime** da entidade atingida como attacking entity (`@217–223`). `lookAt` mira na posição ocular do owner (`@226–236`).
6. **Só então lê Plummeting Flight** do campo `spearItem` da lança via `ACCompat.enchantLevel(stack, PLUMMETING_FLIGHT)` (`@239–248`) e envia o inteiro ao `DinosaurSpiritEntity.setEnchantmentLevel` (`@251`); solicita `Level.addFreshEntity` em `@271–280` e descarta seu booleano.

O nível não altera `10F + damageBonus`, a seleção de DamageType, o período de ignição ou a probabilidade de o hit original ser aceito. Um `hurt` recusado, o retorno especial do Enderman ou owner ausente impedem o ingresso normal observado. A criação e inserção **não têm confirmação de sucesso utilizada** no trecho; não transformar cada hit aceito em espírito ou transporte garantido.

## 4. O nível governa aceleração Y e tempo de transporte

O consumer `server/entity/item/DinosaurSpiritEntity.class`, método `tickSubterranodon(Player):void`, relê seu dado sincronizado `ENCHANTMENT_LEVEL` em dois cálculos separados:

```text
verticalDeltaAddition = 0.03D + 0.005F × enchantmentLevel
movementDelta = movementDelta + (0, verticalDeltaAddition, 0)

while (attackingEntity != null && duration < (40 + 5 × enchantmentLevel)):
    target.setDeltaMovement(Vec3.ZERO)
    target.setPos(spirit.pos - (0, target.getBbHeight(), 0))
    duration += 1
else:
    setFading(true)
```

A estrutura acima é apenas **pseudocódigo explicativo**, não implementação incorporada ao Black Arcana. `getAttackingEntity()` usa ID local de entidade via `level.getEntity(id)`, não UUID persistido nem busca global. O método adiciona aceleração ao próprio delta de movimento **antes** de checar se o alvo existe.

| Nível lido | Adição Y ao delta por tick `0,03+0,005×L` | Limite `duration < 40+5×L` |
|---:|---:|---:|
| 0 — sem encantamento | 0,030 | 40 |
| I | 0,035 | 45 |
| II | 0,040 | 50 |
| III | 0,045 | 55 |

A adição Y está sujeita a movimento anterior, damping, colisões e ao estado da entidade. Em `DinosaurSpiritEntity.tick`, o `move(SELF,delta)` ocorre em `@235–243` e o damping multiplica o delta por aproximadamente `0,9` em `@246–257`, **antes** do dispatch `tickSubterranodon @304–306`. Portanto **0,035/0,040/0,045 não são blocos de altura por tick**. E **45/50/55 são limites de contador de atualização do transporte**, não duração de levitação garantida em segundos ou tempo de vida absoluto do espírito.

No ramo de transporte, `attackingEntity` precisa estar resolvida. O método zera o delta da entidade atingida e redefine `setPos` para a posição atual do espírito menos sua altura (`@52–100`), então incrementa `duration`. Não há chamada adicional de `hurt` nesse método. Ao atingir limite ou perder o alvo, solicita `setFading(true)`, sem demonstrar dano de queda ou controle de aterrissagem. Não adicionar novo dano, imunidade a queda, teleporte adicional nem Mastery por tick.

**Autoria/guards:** `DinosaurSpiritEntity.tick` consulta `getUsingPlayer`; se falhar, marca fading e não executa o dispatch para Subterranodon. No servidor, o Player é resolvido pela PlayerList por UUID, no cliente pela Level local. O subtype **não possui guarda isolada de lado lógico** nas operações `setPos`/movimento do alvo; a autoridade final, replicação, validação de claims/PvP e consistência do mundo requerem QA específica.

## 5. Estados, persistência, custos e consequências

A entidade possui `ENCHANTMENT_LEVEL` sincronizado, inicializado em **0** em `defineSynchedData @71–82`; getter e setter consultam `SynchedEntityData`, e não uma API de perk homologada. Outros estados incluem `ATTACKING_ENTITY_ID` (default **−1**), `PLAYER_ID` opcional, `DINOSAUR_TYPE`, fading, delay, `duration`, delta, rotação e progresso visual.

Os métodos de NBT próprios gravam/leem **`UsingPlayerUUID` e `DinosaurType`**; não gravam diretamente `ENCHANTMENT_LEVEL`, attacking entity ID, duration, fading ou o target original. Não interpretar isso como comprovação de perda ou restauração física exata: camadas genéricas de `Entity`, reload e codecs externos estão fora desse recorte. Não certificar continuação do transporte depois de save/restart.

`DinosaurSpiritEntity.tick` possui atraso/fade e não retorna imediatamente após `discard` na rota `fading && fade<=0`. Também executa movimento anterior e damping antes do dispatch por subtipo. Isso limita qualquer perk que tente aumentar duração de transporte editando apenas o nível, ignorando o ciclo de vida, presença do owner e o target ID.

**Economia da lança:** `ExtinctionSpearItem.releaseUsing` calcula potência com o tempo de carga e, no ramo `power>0.1`, solicita desgaste **1** da stack na `MAINHAND`, lança `ExtinctionSpearEntity` com potência dependente de `3,5F×power`, registra som/stat e pode diminuir a stack em 1 fora de creative. A lógica de arremesso é distinta do encantamento e a inserção é solicitada, com booleano descartado. O custo individual `anvil_cost=4` não representa consumo por acerto, Soul Energy, mana, cooldown ou stamina. O encantamento não instala um custo por tick no transporte.

A fonte de dano inicial pertence à lança (`causeSpiritDinosaurDamage`), não ao Espírito que apenas transporta a entidade. O percurso de `ExtinctionSpearEntity.onHitBlock` e TephraExplosion é outra rota nativa, sem novo efeito de Plummeting Flight aqui comprovado. A proteção Grottoceratops por evento NeoForge é de **Herd Phalanx**, outro encantamento; o ataque Tremorsaurus de `acHurtEnemy` usa **Chomping Spirit**, sem promover esses comportamentos nesta ficha.

## 6. Possíveis campos para perks e limites de integração

Campos técnicos observáveis para planejamento: `vertical_delta_addition`, `max_transport_updates`, `transport_target_id`, `current_duration`, `owner_UUID`, `spear_item_level_source`, `on_hit_accepted`, `fading_state`, `native_damage_source`, `fall_and_collision_result` e `server_authority`. A única parametrização nativa comprovada de Plummeting Flight neste recorte é **`0,03+0,005×L` e `40+5×L`**; isso não certifica possibilidade de alterar L por hook/modder API, nem distância total, altura máxima, alcance do golpe ou tempo de controle efetivo.

Qualquer perk futura sobre altura, tempo de transporte, alvo, dano, área, ataque aéreo ou recursos exige hook realmente acessível, guarda server-side, caps, causa única, proteção PvP/claims, sem duplicação do `hurt` e validação de reentrada, despawn, falha de spawn, jogador desconectado, mudanças de dimensão, reload e integridade do dado sincronizado. **Black Arcana** continua autoritativo apenas sobre seu próprio runtime e não substitui o comportamento nativo da Extinction Spear; **RPG Skill Tree** só fornece progressão/gates sob boundary real.

Evidência reproduzível: [JSON físico e hashes de classes](../EXACT-PLUMMETING-FLIGHT-CONTRACT-1.0.10.json), [Spirit Dinosaur 1.0.10](../EXACT-SPIRIT-DINOSAUR-CONTRACT-1.0.10.json), [regressões de pivôs](../../../../../docs/qa/alexscaves_1010_plummeting_flight_cards_test.py), [sonda do recurso](../../../../../docs/qa/alexscaves_1010_plummeting_flight_probe.py). Sem QA física, **`STATIC_TECHNICAL_CATALOG_ONLY`**, `mutating_hook=NOT_VERIFIED`, `physical_qa=NOT_TESTED`, `NO_MUTATION`, `provider_universe_closed=false`.
