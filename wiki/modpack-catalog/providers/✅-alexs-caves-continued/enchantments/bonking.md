# Bonking — loot extra por morte com Primitive Club (1.0.10)

**Estado:** ⚠️ **ficha técnica individual parcial/condicionada**. Identidade, JSON e referências/branches delimitados no JAR físico publisher **verificados**. `mutating_hook=NOT_VERIFIED`; `physical_qa=NOT_TESTED`; `perk_certification=NOT_CERTIFIED`; `NO_MUTATION`. Não cria uma raiz de cast nem representa uma magia de dano, stun ou projétil.

## Identidade e fonte exata

- **Mod/provider:** Alex's Caves Continued, `alexscaves`, Minecraft 1.21.1 / NeoForge.
- **Encantamento:** `alexscaves:bonking`; `description.translate=enchantment.alexscaves.bonking` (nenhum texto de tooltip da versão instalada foi certificado).
- **Item elegível:** `alexscaves:primitive_club`, dentro da tag publisher `#alexscaves:enchantable/primitive_club`.
- **Artefato:** `alexscaves-1.0.10-neoforge+1.21.1.jar` do publisher, 75.279.314 bytes, SHA-1 `6960b299a39a039ac8a5eb9b07be4ad0e3e0a570`, SHA-256 `36ae0a3cbd028df466a37c671ba2fdf021c060ca1c9c1c32e9f2e95bffae0e7c`.
- **Manifesto selado:** [EXACT-BONKING-1.0.10.json](../EXACT-BONKING-1.0.10.json), reproduzível pela [sonda de leitura JVM](../../../../../docs/qa/alexscaves_1010_bonking_probe.py), [testes sintéticos](../../../../../docs/qa/alexscaves_1010_bonking_probe_test.py) e [CI publisher](../../../../../.github/workflows/alexscaves-1010-bonking.yml).
- **Autoridade:** dados e bytes JAR 1.0.10; a árvore pública `Codx-org/AlexsCavesContinued@523308608422ab8e31974befa7111ecdf495dd37` declara **1.1.1**, usada somente como pista para localizar consumidores, não para atribuir números à build 1.0.10.

## Definição do encantamento (recurso publisher 1.0.10)

| Campo | Valor estático confirmado |
|---|---|
| Recurso | `data/alexscaves/enchantment/bonking.json` |
| SHA-256 do JSON | `f03c4e8c2f8b00b3668b8d7bf14276647b3e0324c159c6336b189a258571a86a` |
| `supported_items` | `#alexscaves:enchantable/primitive_club` |
| `weight` | `1` — peso de encantamento, **não** chance de ativação |
| `max_level` | `1` |
| `min_cost` | `base=1`, `per_level_above_first=18` |
| `max_cost` | `base=41`, `per_level_above_first=10` |
| `anvil_cost` | `8` |
| `slots` | `mainhand` |

A tag publisher `data/alexscaves/tags/item/enchantable/primitive_club.json`, SHA-256 `71829c384be93b8cef1e090b6afafa621dcd4eeb520c7a66ab0e6524e8a6ae43`, lista o único item `alexscaves:primitive_club`. A resolução de tags e disponibilidade de enchanting no pack podem diferir por datapacks/mods. Custo de bigorna e valores da tabela **não** correspondem a mana, durabilidade por proc nem cooldown.

## Gatilho e processamento na morte

**Consumer SHA-exato:** `com/github/alexmodguy/alexscaves/server/event/CommonEvents.class`, SHA-256 `d132caad67ecab68844091ee396d37fecc4860440d338dcd82384f1555f8ad43`.

**Método:** `livingDie(Lnet/neoforged/neoforge/event/entity/living/LivingDeathEvent;)V`, **229 instruções**, digest do parse `03c56101acdb5aa18c6d253f49b914bef1c1f2723aa5de548b126d4d864020dd`. Os offsets a seguir são do bytecode da versão exata, não nomes de API prometida.

A região auditada verifica `LivingDeathEvent.getSource`, `DamageSource.getDirectEntity @117`, mão principal do atacante direto `@137–157` e tipo de item `ACItemRegistry.PRIMITIVE_CLUB @143`. O caminho superior da rotina exige morte de um `Mob` e lado não cliente, conforme os testes compilados que desembocam na condição de item. Um atacante direto pode ser `LivingEntity`; **não** foi certificado requisito explícito de `Player` no ramo de Bonking. Não confundir `getDirectEntity` com `DamageSource.getEntity` nem assumir autoria de outro projétil.

1. `ACEnchantmentRegistry.BONKING @167`; `ACCompat.enchantLevel @170`; `ifle @173 → 432`: exige nível positivo no stack atualmente consultado.
2. RNG do mundo: `Level.getRandom @183`, `nextFloat @186`, `ldc 0.33F @191`, `fcmpg @193`, `ifge @194 → 432`: **a condição de entrada é aproximadamente 33% por oportunidade elegível**, se a fonte produzir uma distribuição uniforme. Não é prova de chance final de crânio, drop em inventário ou recompensa confirmada.
3. Tenta construir `EntityType.CREEPER` por `ACCompat.createEntity @197–204`; uma referência nula evita o caminho posterior (`ifnull @214 → 432`). Isso não prova a criação de um creeper no mundo.
4. Quando o nível é `ServerLevel`, tenta construir `EntityType.LIGHTNING_BOLT @241–246`, testa referência nula, marca `LightningBolt.setVisualOnly(true) @262` e chama `Creeper.thunderHit @271` no Creeper temporário. O uso de raio visual **não comprova raio lançado ou dano elétrico ao alvo**.
5. Cria uma origem de dano do tipo `DamageSources.mobAttack(fakeCreeper) @283` para a rotina de loot, sem alterar por si a `DamageSource` que encerrou a vida da vítima.
6. Para cada slot de `EquipmentSlot.values @303`, salva a chance anterior de drop com `ac_getEquipmentDropChance @338` e `HashMap.put @346`, depois ajusta a chance de equipamento para `0F` por `ac_setDropChance @355`.
7. Invoca uma chamada específica de loot `EntityDropChanceAccessor.ac_dropCustomDeathLoot(fakeCreeperDamage,0,false) @372`. Na sequência, `EquipmentSlot.values @377`, `HashMap.get @412`, `Float.floatValue @418` e `ac_setDropChance @421` descrevem a **tentativa de restaurar as chances de equipamento previamente capturadas**.

Esse caminho busca um efeito de loot semelhante ao cenário de morte por Creeper eletrificado, mas **o contrato estático não certifica um crânio garantido, tipo de drop específico, porcentagem real de sucesso, quantidade, dupla execução, ordenação com outros mods de loot ou comportamento sob exceções**. O RNG em `0.33F` é apenas um guard do código nativo. A leitura não demonstra uma transação atômica ou um bloco `finally` protegendo a restauração do estado.

## Bridge de loot e fronteira de mixins

A ponte usada pelo consumer é `com/github/alexmodguy/alexscaves/server/entity/util/EntityDropChanceAccessor`; o classfile `com/github/alexmodguy/alexscaves/mixin/MobMixin.class` tem SHA-256 `38381f9b5b3908e813711f031161a1e25b46e68d220ed34c137948e6b59dac3e`.

| Método do bridge compilado | Evidência delimitada |
|---|---|
| `ac_getEquipmentDropChance(EquipmentSlot)F` | 4 instruções; delega ao `getEquipmentDropChance` nativo; digest `9c004cd74e9b2aa09c5a1033e467f5dbf48ccd182f66123d839a19778f2b22b7` |
| `ac_setDropChance(EquipmentSlot,F)V` | 5 instruções; delega a `setDropChance`; digest `1b5000cb0d36f76808d2563f07a1649e72f7994d84a8b774fd97aea62d75c40b` |
| `ac_dropCustomDeathLoot(DamageSource,int,boolean)V` | 8 instruções; invoca `dropCustomDeathLoot(ServerLevel,DamageSource,boolean)` após consulta ao nível; digest `f020a1c8aee5b8524c287cbb7bdabc4434b5ded87f0d114fd902d58553e70ca2` |

O JAR contém essas classes e métodos, mas a sonda **não certifica que o Mixin foi aplicado com sucesso na instância efetiva, nem seu posicionamento no pipeline de outros mods**. Alterações paralelas em loot, cancelamento da morte, entidades de outros mods, datapacks e proteções de servidor exigem teste real.

O arquivo `PrimitiveClubItem.class` SHA-256 `92bfb58cb5ed2c84dd6f989afad22c98209542889e30b6214c502dbff42fa1ac` possui 16 métodos parseados; **não há referência direta a `ACEnchantmentRegistry.BONKING` nesses métodos**, segundo a busca de símbolos realizada no classfile exato. O stun básico do Primitive Club e `Dazing Sweep` são mecânicas distintas e não devem ser atribuídos a Bonking. A sonda não enumera todos os possíveis consumidores adicionais de mods externos.

## Parâmetros de perks e limites

| Eixo | Evidência observada | Status de modificação |
|---|---|---|
| **Chance / proc** | Guard `nextFloat() < 0.33F` no death handler | ⛔ Sem hook estável para mudar probabilidade; não interceptar/reexecutar evento e duplicar loot |
| **Alvo / tipo** | Vítima `Mob`, atacante direto `LivingEntity` com Primitive Club na mão principal | ⛔ Sem alteração segura de categoria, autoria de kill ou regras de arma |
| **Quantidade / tipo de loot** | Chamada nativa `ac_dropCustomDeathLoot` e hipótese Creeper eletrificado | ⛔ Resultado e tabela efetiva não certificados; não conceder drops diretamente |
| **Área / alcance / projétil** | Não são operações de alcance, AoE, nem de projétil de Bonking no consumer auditado | N/A para parâmetros próprios; **não** inferir que a arma não tenha outros efeitos |
| **Dano / tipo de dano** | `mobAttack(fakeCreeper)` é origem simulada usada na rotina de loot | ⛔ Não mudar dano do golpe real nem associar dano extra a esse encantamento |
| **Tempo / cooldown** | Evento de morte; não há cooldown próprio no trecho auditado | ⚠️ Ausência de cooldown no trecho não certifica todo o runtime |
| **Custo / equipamento** | Dados de enchanting, item `primitive_club`, slot principal; chances de drop temporariamente alteradas | ⛔ Sem contrato para converter custos de encantamento em mana/durabilidade, nem para editar drop-chances de mobs |
| **Mastery / XP / duplicidade** | Causalidade: evento nativo de morte e tentativa de gerar loot próprio | ⛔ Não emitir proc de perícia/XP sem prova de concessão e deduplicação |

O **Black Arcana** só poderá observar resultados confirmados do provider, sem reproduzir a chamada de loot ou simular outro Creeper. O **RPG Skill Tree** permanece provider de progressão, atributos, Mastery e gates por contratos reais, não a autoridade desse evento. Modificação que exija hook de loot/causalidade deve falhar fechado enquanto não houver contrato e testes de compatibilidade.

## Limites de prova e aceite futuro

- **Identidade/JSON publisher:** `VERIFIED_EXACT_BINARY`.
- **Consumer e bridges selecionados:** `VERIFIED_EXACT_BINARY_SELECTED_WINDOWS`.
- **CFG completo, exceções, odds finais, loot aceito, Mixin em execução, interação com loot tables de terceiros, datapacks e PvP/claims:** `NOT_CERTIFIED` / `NOT_VERIFIED`, conforme o tópico.
- **Mutação:** `NO_MUTATION`, hook `NOT_VERIFIED`. **QA física:** `NOT_TESTED`. **Perk completa:** `NOT_CERTIFIED`.

Para avançar, executar teste real com kills de tipos de mobs elegíveis e não elegíveis, atacante direto vs projéteis, DeathEvent cancelado, mão principal alterada, morte múltipla, drop normal vs extra, interação com `MobMixin` e outros mods de loot, resultados de loot para Creeper eletrificado, equipamentos com chances customizadas antes/depois, exceções, carregamento de chunks e múltiplos jogadores. Não marcar `PASS` sem evidências.

**Contabilidade:** uma nova ficha individual **parcial**; **+0** contratos estáticos certificados; **+0** novas ações mágicas; **+0** providers encerrados. Próximo ID alfabético do roster: `alexscaves:bouncing_bolt`.
