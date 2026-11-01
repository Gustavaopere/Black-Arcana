# Raygun — tipo de dano `alexscaves:raygun` (1.0.10)

**Estado de catalogação:** ⚠️ `RESOURCE_JSON_VERIFIED` (recurso SHA-exato). **Contrato técnico estático para perks:** ⚠️ `NOT_CERTIFIED`. **Hooks mutadores:** `NOT_VERIFIED`. **QA física:** `NOT_TESTED`.

## Proveniência e identidade

- **Provider / mod ID:** `Alex's Caves Continued` / `alexscaves`.
- **Versão do artefato:** `alexscaves-1.0.10-neoforge+1.21.1.jar` (Minecraft 1.21.1).
- **JAR SHA-1:** `6960b299a39a039ac8a5eb9b07be4ad0e3e0a570`.
- **JAR SHA-256:** `36ae0a3cbd028df466a37c671ba2fdf021c060ca1c9c1c32e9f2e95bffae0e7c`.
- **Resource ID exato:** `alexscaves:raygun`.
- **Caminho ZIP:** `data/alexscaves/damage_type/raygun.json`.
- **SHA-256 do JSON:** `dc1095e92e0695b302100993af8fafd72c8d6b948d90717e667a6ced2ae1bc35`.
- **Manifesto verificável:** [snapshot dos recursos](EXACT-RESOURCE-MANIFEST-1.0.10.json) e [auditoria da CI](https://github.com/Gustavaopere/Black-Arcana/actions/runs/40985275338).

## Campos JSON confirmados no artefato

| Campo | Valor literal do recurso | Limite de interpretação |
|---|---|---|
| `message_id` | `raygun` | Chave de mensagem; não é sinônimo do registro nem classe de implementação |
| `scaling` | `never` | Campo `scaling` do tipo de dano; não fixa dano causado nem curva de perks |
| `exhaustion` | `0.3` | Valor do campo `exhaustion`; **não** é mana, stamina, custo do feitiço ou dano |

## Tags de tipo de dano declaradas diretamente

- `minecraft:bypasses_cooldown`
- `minecraft:is_explosion`
- `minecraft:is_projectile`

Essas são **entradas textuais diretas** dos seis arquivos `data/*/tags/damage_type/*.json` encontrados no JAR. Elas não comprovam as tags finais resolvidas depois de datapacks, outras dependências ou overrides. Uma referência a tag não prova que o ataque usado no jogo produza este `DamageSource`.
O tag `minecraft:bypasses_cooldown` corresponde à classificação de tipo de dano do Minecraft, **não** demonstra redução/bypass do cooldown de lançamento de magias.


## Superfícies necessárias para perks — ainda não auditadas

| Capacidade pretendida | Situação |
|---|---|
| Factory de `DamageSource` / chamadas JVM | ✅ localizadas estaticamente; comportamento e caminhos efetivos `NÃO VERIFICADO` |
| Origem, atacante, owner, attribution e condições de PvP | `NÃO VERIFICADO` |
| Fórmula de dano, mitigação, críticos e resistências | `NÃO VERIFICADO` |
| Alvos elegíveis, tipo target/área, alcance, raio e filtros | `NÃO VERIFICADO` |
| Entidades/projéteis, tamanho, velocidade, colisão e homing | `NÃO VERIFICADO` |
| Duração, intervalo de hits, custo de ação e cooldown de casting | `NÃO VERIFICADO` |
| Persistência, ordenação de eventos, server authority e deduplicação | `NÃO VERIFICADO` |
| Hook de mutação seguro na versão instalada | `NOT_VERIFIED` |
| QA real em modpack/multiplayer | `NOT_TESTED` |

## Boundary / decisão provisória

O *provider* mantém autoridade sobre a criação, classificação e aplicação de dano. Black Arcana não altera `DamageSource`, escola, dano, tags ou projéteis sem evidência dos consumidores Java e hooks seguros. O RPG Skill Tree fornece perks/atributos somente através de boundary verificada, sem double-processing. **Fail-closed:** `NO_MUTATION` até a auditoria dos consumidores e a validação específica.

**Contabilidade:** 1/11 recursos de tipo de dano documentados; **+0 raízes mágicas novas**. Este objeto não recebe status `COMPLETE_PERK_READY` apenas por existir como JSON.

## Evidência compilada 1.0.10 — factory e consumidores diretos

**Escopo:** `SHA_EXACT_STATIC_FACTORY_AND_DIRECT_CALLSITE_ONLY`. [Manifesto dos consumidores](EXACT-CONSUMERS-1.0.10.json) · [CI da auditoria](https://github.com/Gustavaopere/Black-Arcana/actions/runs/40993193816).

- **Classe de fábrica:** `com/github/alexmodguy/alexscaves/server/misc/ACDamageTypes.class`, SHA-256 `389fb88f8d6e1515e3dfe7f401a728bb33629666bd2319ae7e25668f710e4ef6`.
- **Método:** `ACDamageTypes.causeRaygunDamage`.
- **Descritor JVM:** `(Lnet/minecraft/core/RegistryAccess;Lnet/minecraft/world/entity/Entity;)Lnet/minecraft/world/damagesource/DamageSource;`.
- **Campo de DamageType lido:** `RAYGUN` (offset `19`).
- **Construtor de DamageSource referenciado:** `Method com/github/alexmodguy/alexscaves/server/misc/ACDamageTypes$DamageSourceRandomMessages."<init>":(Lnet/minecraft/core/Holder$Reference;Lnet/minecraft/world/entity/Entity;I)V`.
- **Parâmetros da factory:** `RegistryAccess` e `Entity` — não comprova autoria final.
- **Referências `invokestatic` encontradas:** 1 em 1 classes. Isso não representa quantidade de hits por ataque.

| Classe chamadora | Método chamador | Descritor JVM | Offset | Opcode |
|---|---|---|---:|---|
| `com/github/alexmodguy/alexscaves/server/item/RaygunItem.class` | `public void onUseTick(net.minecraft.world.level.Level, net.minecraft.world.entity.LivingEntity, net.minecraft.world.item.ItemStack, int)` | `(Lnet/minecraft/world/level/Level;Lnet/minecraft/world/entity/LivingEntity;Lnet/minecraft/world/item/ItemStack;I)V` | 1026 | `invokestatic` |

**Limites:** as invocações são referências estáticas no bytecode exato; não demonstram execução, alcance, área, cooldown, fórmula de dano, filtros de alvo, persistência, autoridade/attribution, proteção PvP nem segurança de intercepção. Chamadas indiretas, mixins, reflexão, datapacks e comportamento do modpack não estão comprovados. **`mutating_hook=NOT_VERIFIED`, `physical_qa=NOT_TESTED`, `NOT_CERTIFIED`**. Black Arcana e RPG Skill Tree devem preservar o settlement nativo, evitando processamento duplicado e aplicando `NO_MUTATION` sem contrato seguro.

## Auditoria de controle nativo — `RaygunItem` compilado 1.0.10

**Recorte novo:** `SHA_EXACT_1010_RAYGUN_SELECTED_METHOD_REFERENCES_AND_NUMERIC_OPERANDS_ONLY`. [Manifesto imutável de parâmetros e métodos](../EXACT-RAYGUN-CONTROL-1.0.10.json) · [probe e testes](https://github.com/Gustavaopere/Black-Arcana/blob/main/docs/qa/alexscaves_1010_raygun_control_probe.py) (a ligação à main só vale após merge) · [workflow de evidência](https://github.com/Gustavaopere/Black-Arcana/actions/runs/41256261358).

A inspeção automatizada baixou e validou a versão publisher **1.0.10** do JAR pelos SHA-1/SHA-256 e tamanho físico registrados acima, verificou a classe compilada `server/item/RaygunItem.class` (SHA-256 `3fc60cb7ff8be2744becf8ac9e524799349996972708845a124f02650bfb344c`), inspecionou **26 métodos declarados** e exportou **18 métodos selecionados**. O manifesto fixa digest de oito métodos e 14 âncoras numéricas/simbólicas; o resultado da CI não é teste de gameplay nem reconstrução completa do CFG.

### Alvo, range e geometria — não confundir conceitos

| Método e offset compilado | Evidência estática exata | Limite para perks |
|---|---|---|
| `onUseTick @11` | Calcula tempo utilizado a partir de `getUseDuration - remainingUseTicks` e inicializa um valor inteiro **15** no início de uma sequência de comparação/proporção. | `15` é um operando do cálculo de uso; não anunciar como alcance ou cooldown sem rastrear o resultado. |
| `onUseTick @35` | Literal **25.0f** em uma região inicial; mais adiante `getHitResultOnViewVector @69` e `LivingEntity.pick @80` recebem distâncias calculadas. | Há caminhos de ray trace distintos. O literal não basta para certificar o alcance efetivo de cada modo ou um parâmetro público modificável. |
| `onUseTick @44–50` | Consulta `ACEnchantmentRegistry.X_RAY` via `ACCompat.enchantLevel`. | Enchantment nativo participa da escolha dos caminhos; efeito sobre oclusão/alcance efetivo ainda não está completamente certificado. |
| `onUseTick @575–640` | Obtém a bounding box do usuário, executa `AABB.inflate` e usa `ProjectileUtil.getEntityHitResult` com vetores e predicado. | AABB de busca, distância do raio e vítima realmente elegível são medidas distintas; não converter caixa em raio circular ou área de dano. |
| `onUseTick @875–943` | Consulta `Level.isClientSide` e, no caminho de servidor observado, usa `Level.getEntities(source, AABB, Predicate)` para enumerar alvos. | Há um segundo domínio de seleção por entidades. Sem CFG/medidas completas, não declarar cone, número máximo de hits, LOS universal ou tamanho de hitbox. |
| `onUseTick @978–1008` | Verificações `Entity.is`, `Entity.isAlliedTo`, `LivingEntity.isAlliedTo` e `isPassengerOfSameVehicle`, com saídas de ramo antes de solicitar dano. | Não permitir que uma perk elimine exclusões de autocausação, aliados ou passageiros. Proteção/PvP externa permanece sem teste. |

O recorte de `onUseTick` exportado não mostra chamada simbólica direta a `Level.addFreshEntity`; os caminhos observados recorrem a ray traces, seleção de entidades e partículas. Isso **não** prova ausência de entidades em todos os caminhos indiretos, variantes ou interações com outros mods.

### Charge, uso e encantamentos

| Superfície exata | Dado identificado | Condição de integração |
|---|---|---|
| `getUseDuration(ItemStack,LivingEntity)` | Retorna literal inteiro **72000 ticks**. | Tempo máximo declarado para uso mantido, **não cooldown** nem duração obrigatória de cada disparo. |
| `getCharge / setCharge` | Armazenam/lêem tag de `ItemStack` **`ChargeUsed`**, com fallback de leitura zero quando não há tag. | Unidade de estado do item; não é mana Black Arcana. Persistência/migração real precisa de QA. |
| `hasCharge` | Compara `getCharge` com **1000** (`if_icmpge` salta para o falso). | O predicado indica elegibilidade enquanto `ChargeUsed < 1000` no método examinado. Não confundir valor gasto com energia disponível. |
| `use` | Consulta `hasCharge`, depois `findAmmo`, `Player.isCreative`, `ItemStack.isEmpty`, `ItemStack.shrink(1)` e `setCharge`, além de sons de início/recarga/sem munição. | Recarga nativa pode consumir item conforme os guards; não autorizar custo adicional em segundo pipeline. Tipo exato de munição e cada branch de consumo ainda requerem a auditoria do helper `findAmmo`. |
| `onUseTick @246–319` | Consulta `ENERGY_EFFICIENCY` e usa `Math.floor`, `Math.min`, `getCharge`, `setCharge`, o limite **1000** e literal **1.5f**. | Essa é a região de custo/consumo por tick; a fórmula completa e todos os guards ainda não estão selados para mudança de eficiência. |
| `onUseTick @332–352` | Consulta `GAMMA_RAY` via nível do encantamento e um sorteio booleano. | Não converter presença de encantamento em mudança garantida de dano/status; conferir branches e valores dos modos. |
| `setUseTime` | Tags `PrevUseTime` e `UseTime`. | Dados de animação/timing do item; não presumir que replicação ou salvamento prove autoridade do cliente. |
| `getBarWidth` | Usa literais **13.0f** e **1000.0f** junto de `getCharge`. | Escala do indicador visual, não alcance ou tamanho da colisão. |

Em `onUseTick` e `releaseUsing` são encontradas mensagens `UpdateItemTagMessage` enviadas por `sendMSGToServer`. A inspeção do **sender** não comprova autenticação no handler, integridade de `ChargeUsed`, antirreplay, autorização do ID de entidade nem enforcement de custos no servidor. Nenhuma perk pode tratar o pacote enviado como fonte autoritativa sem prova do receptor.

### Dano, owner e efeito secundário

- `RaygunItem.onUseTick @1013–1047` distingue `TremorzillaEntity` num ramo próprio, chama `ACDamageTypes.causeRaygunDamage(registryAccess, caster)` em `@1026` e solicita `ACCompat.hurt(target, damageSource, amount)` em `@1041`. Na decisão local imediatamente anterior a `hurt`, os operandos possíveis são **`2.0f`** e **`1.5f`**, condicionados a flag local `iload 18`. A origem completa da flag, o resultado de mitigação e a aceitação de cada hit não são certificados por esses números.
- O `DamageSource` recebe o *caster* como argumento da factory no trecho inspecionado; isso não garante crédito de kill, procs, Mastery ou políticas de PvP de mods externos. O retorno booleano de `ACCompat.hurt` participa dos guards posteriores; um evento visual ou um alvo dentro da AABB não certifica dano aceito.
- `onUseTick @1076–1119` verifica `ACTagRegistry.RESISTS_RADIATION`, referencia `ACEffectRegistry.IRRADIATED` e, em ramo condicionado, solicita `LivingEntity.addEffect` com `MobEffectInstance(..., **800 ticks**, amplifier local)`. Os 800 ticks são a duração **solicitada ao aplicar o efeito**, não duração universal do DamageType e nem prova de sucesso para todo hit. A ficha [Irradiated](../effects/irradiated.md) conserva o contrato de tick, exaustão e redução Hazmat.
- `onUseTick @1125–1154` monta `UpdateEffectVisualityEntityMessage`. Esse tráfego é downstream visual e não deve gerar um segundo proc de ataque ou ser usado como confirmação de aplicação do status.

### Requisitos antes de perks mutadoras

1. Fechar CFG e limites efetivos de distância/área, distinguir `X_RAY`, `GAMMA_RAY` e `ENERGY_EFFICIENCY` e os predicados usados nas buscas; não sobrescrever `ProjectileUtil` ou a filtragem de aliados.
2. Identificar `findAmmo`, custo completo de `ChargeUsed`, servidor autoritativo de tags e validação do `UpdateItemTagMessage`. Não duplicar recarga ou cobrança por feitiço.
3. Confirmar `ACCompat.hurt`, critérios de sucesso, hits múltiplos/por-tick, atribuição causal, escala de dano, imunidades, `Irradiated` e deduplicação de XP/procs.
4. Executar cliente/servidor dedicados com casos de níveis de enchantment, alvos aliados/mesmo veículo, Tremorzilla, resistência à radiação, `ItemStack` duplicado, save/reload e proteção de claims.

**Decisão:** a ficha continua `NOT_CERTIFIED`, `mutating_hook=NOT_VERIFIED`, `physical_qa=NOT_TESTED`, `NO_MUTATION`; nenhum `COMPLETE_PERK_READY`, avanço de 22/29, nova raiz mágica ou promoção de Stage. Os parâmetros acima são **observações estáticas compiladas**, não contratos de intervenção seguros.
