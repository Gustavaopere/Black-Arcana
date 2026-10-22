# Weapons of Miracles 2.0.178 — limites técnicos e evidência exata

**Checkpoint: 21/10/2026.** ⚠️ 64 IDs com ficha individual e evidência estática; downstream, mutadores por jogador e QA físico continuam parciais. A barra 64/64 mede fichas dedicadas, não implementação de perks nem homologação do provider.

## Identidade e fonte de verdade

| Superfície | Evidência |
|---|---|
| Modlist física | RPG Skill Tree `ed5b65b890767b406ce41127bcb793775263c7bd`, row #568; WeaponsOfMiracles-2.0.178.jar |
| JAR publisher | [CurseForge project/file 918614/8829395](https://www.curseforge.com/minecraft/mc-mods/weapons-of-miracles-epicfight/files/8829395), via [Maven](https://cursemaven.com/curse/maven/weapons-of-miracles-918614/8829395/weapons-of-miracles-918614-8829395.jar) |
| Bytes / SHA-1 | 20.941.584 / `b507eb376778cfd1cbecec2841c38891b26a7349` |
| SHA-256 | `0c36ba17bc812c65f5e37f9227d8b6a5185aac70b82a88d1bf52ee13103592cc` |
| Host Epic Fight exato | 21.17.3.1; SHA-1 `fb199b7bbea2fc402da28ab586e73f47e32f8fc0`; SHA-256 `8b882554cf10086398340fbdc741819ee72a801a3adce516c7f4768326a39526`; 8.578.288 bytes |
| Ambiente físico declarado | Minecraft 1.21.1 / NeoForge 21.1.250 / Java 21. O build Black Arcana tem seu próprio contrato; esta auditoria não o altera. |
| Metadados do WOM | `modId=wom`, `version=2.0.178`, Minecraft `[1.21.1,1.22)`, Epic Fight `[21.14.1,)`; mínimo de metadata não substitui o host exato do pack. `loaderVersion=[4,)` e dependency neoforge `[4,)` são dados literais do provider, não nova versão testada. |
| Fonte Java | Metadata aponta `https://github.com/Reascer/WeaponsOfMinecraft/issues`. Consulta pública do repositório em 21/10 retornou 404; não se conclui inexistência global de código. Nenhum source de outra versão é promovido a source exato deste JAR. |
| Licença e clean room | Metadata `All RIGHTS RESERVED`. Retidos somente fatos de interoperabilidade, hashes, parâmetros, assinaturas, referências, offsets e síntese original. Sem JAR, assets, corpos de implementação ou tooltips redistribuídos. |

Equivalência física significa correspondência ao hash documentado na modlist; a instalação em execução não foi lida nesta rodada. A evidência anterior está em [EXACT-2.0.178-ARTIFACT-AUDIT](../EXACT-2.0.178-ARTIFACT-AUDIT.md).

## Registro, recursos e o que a contagem mede

[Manifesto](individual-skill-cards-2.0.178.json): **64 IDs únicos / 64 caminhos de ficha**, 51 novos + 13 enriquecidos. O verificador exige ID literal no `<clinit>` → `invokedynamic` → índice `BootstrapMethods`/`LambdaMetafactory` → supplier tipado → `DeferredRegister.register` → holder correspondente. O nome público histórico de 27 skills não entra no denominador.

Há **58 JSONs próprios**, incluindo objetos vazios para `ruine_passive`, `torment_passive` e `solar_passive`. Seis IDs não têm arquivo próprio:

- `wom:avatar_of_might`;
- `wom:herrscher_passive`;
- `wom:lunar_echo_passive`;
- `wom:napoleon_passive`;
- `wom:evil_tachi_passive`;
- `wom:unbreakable_passive`.

Arquivo ausente, objeto vazio e `consumption=0` são três estados diferentes. A classificação continua **12 COUNTED_EXACT + 1 CONDITIONAL + 51 EXCLUDED**. Todos os 51 excluídos da métrica mágica fazem parte do trabalho técnico; nenhum novo root é criado por esta rodada. Nova/Flash Mutilation continua condicional pela aquisição normal não fechada.

## Consumidores do host exato 21.17.3.1

Os seguintes fatos foram lidos no bytecode do host hash-exato, sem extrapolar a fonte adjacente 21.17.3:

| Campo / builder | Consumidor compilado | Consequência para integração |
|---|---|---|
| `consumption` | `Skill.loadDatapackParameters(CompoundTag)` → `getFloat` → float `consumption` | Não identifica sozinho recurso ou custo líquido; callbacks podem sobrescrever/consumir valores diferentes. |
| `max_duration` | Mesmo loader → `getInt` → int `maxDuration` | Configura contador base; não prova duração final, unidade em segundos ou lifetime de projétil. |
| `max_stacks` | Mesmo loader → `contains`, `getInt`, fallback literal 1 → `maxStackSize` | Capacidade de stacks, não máximo de alvos. Fallback é dessa rotina quando chamada; não inventar recurso JSON ausente. |
| `penalizer` | `GuardSkill.loadDatapackParameters` → loader base → `getFloat` → `penalizer` | Coeficiente usado pela guarda; input, impacto, dano e recursos compõem o resultado. |
| `attribute_modifiers` | Loader limpa mapa e faz `ATTRIBUTE_ENTRY_CODEC.parse(NbtOps, list).result().ifPresent(...)` | `Skill.lambda$static$0` compõe `Attribute.CODEC` e `AttributeModifier.MAP_CODEC`. Registro legado Voodoo não foi certificado por execução de codec nesta rodada. |
| `xp_requirement` | Não lido pelo loader base acima | RAW de progressão; consumidor final, config implantada e coexistência com o owner RPG ainda exigem prova. |
| Builder genérico | `SkillBuilder(Function)` inicia `ONE_SHOT` e `Resource.NONE` | Categoria PASSIVE/IDENTITY/MOVER não converte automaticamente o recurso em stamina. |
| Builder dodge | `DodgeSkill.createDodgeBuilder` define DODGE, ONE_SHOT, STAMINA | Explica recurso declarado dos dodges; não elimina débitos extras. |
| Builder guard | `GuardSkill.createGuardBuilder` define GUARD, HELD, STAMINA | Aplicável aos quatro WOM guards que usam esse builder; Soul Protection/Shulker Cloak usam genérico NONE. |
| Builder innate | `WeaponInnateSkill.createWeaponInnateBuilder` e `ConditionalWeaponInnateSkill.createConditionalWeaponInnateBuilder` definem WEAPON_CHARGE | Gasto explícito de STAMINA continua possível no método da skill. |
| Satsujin passive | Supplier WOM define ONE_SHOT e COOLDOWN | Não aplicar desconto de stamina a cooldown ou a todo campo chamado consumption. |

## Casos que alteram a decisão de uma perk

| Skill | Fato localizado | Limite prático |
|---|---|---|
| Time Travel | JSON 0; `executeOnServer` PC 29 chama STAMINA/12; retorno descartado no PC seguinte | Não anunciar skill gratuita nem inferir resultado a partir do preflight. |
| Avatar of Might | Sem JSON; `lambda$onInitiate$0` PC 119 chama STAMINA/12; caixa 20³ no PC 429 | Custo e geometria vêm de código/estado. Caixa de consulta não é raio/hit garantido. |
| Charybdis | Builder WEAPON_CHARGE, mas `executeOnServer` PC 12 chama STAMINA/consumption; iniciação e update fixam 6 | Override isolado do JSON pode ser sobrescrito. Não aplicar dois descontos. |
| Spider Techniques | Loader próprio força consumption=0,2 depois da base; update consome STAMINA | O parâmetro ativo pode vir de código mesmo sem consumption no JSON. |
| Heart Shield | `updateContainer` grava MAX_SHIELD=20; usa ADD_VALUE em MAX_ABSORPTION; onRemoved remove modifier | Não afirmar absorção final de jogador nem oferecer knob JSON fictício. |
| Voodoo Magic | PC 409 de update usa STAMINA/-1,5; callback de consumo usa -amount×0,8 em outro `consumeForSkill` | Preservar sinal, causa e skill identity; interação com normalização RPG é pendência, não bug confirmado. |
| Críticos/cura | Vampirize usa `getModifiedDamage×0,2→heal`; Critical Knowledge usa modifiers e encantamentos | Valor entregue a consumer não é HP final nem chance medida em gameplay. |
| Áreas | AABB 20³ (Bulwark/Proximity/Avatar), 50³ (black hole), 200³ em alguns callbacks lunares/Sakura | `ofSize` recebe dimensões totais. Filtros/distância/hitbox/dano final precisam ser seguidos; não chamar esses números de raio. |

As fichas preservam descritores JVM, estados e referências específicas; o manifesto guarda o primeiro PC de cada referência selecionada por método. Nem todos os callbacks do provider, colisores e ramos estão reconstruídos. Mesmo um setter público como `setPenalizer(float)` altera o objeto de skill; escopo/lifecycle e sincronização não foram certificados como seguros por jogador. Não usá-lo como API de perk apenas pela visibilidade.

## RPG, Black Arcana e Enshrouded

[Contrato RPG existente](../../✅-epic-fight/skills/RPG-SIBLING-BOUNDARIES-ed5b65b.md): main `ed5b65b890767b406ce41127bcb793775263c7bd` já registra `CONSUME_SKILL`, `ON_DODGE`, `DELIVER_DAMAGE_PRE` e `DELIVER_DAMAGE_POST`. Stamina é ajustada por `event.setAmount` apenas para player servidor elegível e evento STAMINA. Esse contrato genérico pode incidir sobre ações de addons que passem pelo host; não há prova de que toda skill WOM siga um único caminho.

**Voodoo requer teste de composição:** o sibling normaliza `max(0,event.amount)` antes de aplicar política. WOM usa montantes negativos para recuperação e pode criar evento de consumo a partir de outro consumo, excluindo this do próprio callback. Isso estabelece uma possível interação por código; ordem entre listeners, eventos realmente recebidos, cancelamento, valor debitado/recuperado e saúde final **NÃO foram medidos**. Não declarar compatibilidade plena, nem corrigir o sibling sem reproduzir o contrato.

RPG continua owner de progressão/atributos/Mastery/perks/gates; WOM/Epic Fight de efeitos, recursos, animações e settlement. Black Arcana mantém casting/domains/rituais/world safety/Arcane Danger; Enshrouded mantém seu Shroud/exposure. Source Enshrouded consultado: main `a41dbb51aacb94b7b5db6517f1514b0b7aee3e83`; nenhuma bridge nova foi inferida por tema. Não duplicar dano, custo, cura, teleporte ou Mastery.

## Reprodução e aceitação

[Verificador](../../../../../docs/qa/wom_20178_catalog_binary.py) / [workflow](../../../../../.github/workflows/wom-20178-catalog-binary.yml) conferem hashes, registro/BootstrapMethods, 58 JSONs, seis ausências, assinaturas/referências selecionadas e existência/unicidade das 64 fichas. Também inspecionam consumidores base no host exato. Publicam somente fatos e resultados, sem JAR ou disassembly.

```bash
python3 docs/qa/wom_20178_catalog_binary.py --self-test
python3 docs/qa/wom_20178_catalog_binary.py \
  --jar /caminho/WeaponsOfMiracles-2.0.178.jar \
  --epic-jar /caminho/epic-fight-21.17.3.1.jar \
  --output /tmp/wom-catalog-evidence.json
```

O resultado estático não verifica datapack implantado, atributos de player conectado, custo líquido, gates efetivos, animação/hitbox em runtime, PvP/claims ou full pack. Stage 06.05 e Stage 09 físico permanecem pendentes. [Índice individual](INDIVIDUAL-SKILL-CARDS-2.0.178.md) · [progresso](../../../meta/PROGRESSO-CATALOGO-ATUAL.md).
