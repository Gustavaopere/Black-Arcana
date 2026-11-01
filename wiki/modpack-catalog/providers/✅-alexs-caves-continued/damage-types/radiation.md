# Radiation — tipo de dano `alexscaves:radiation` (1.0.10)

**Estado de catalogação:** ⚠️ `RESOURCE_JSON_VERIFIED` (recurso SHA-exato). **Contrato técnico estático para perks:** ⚠️ `NOT_CERTIFIED`. **Hooks mutadores:** `NOT_VERIFIED`. **QA física:** `NOT_TESTED`.

## Proveniência e identidade

- **Provider / mod ID:** `Alex's Caves Continued` / `alexscaves`.
- **Versão do artefato:** `alexscaves-1.0.10-neoforge+1.21.1.jar` (Minecraft 1.21.1).
- **JAR SHA-1:** `6960b299a39a039ac8a5eb9b07be4ad0e3e0a570`.
- **JAR SHA-256:** `36ae0a3cbd028df466a37c671ba2fdf021c060ca1c9c1c32e9f2e95bffae0e7c`.
- **Resource ID exato:** `alexscaves:radiation`.
- **Caminho ZIP:** `data/alexscaves/damage_type/radiation.json`.
- **SHA-256 do JSON:** `e280db38a17bd5728ef6bbc061d6a4b1a849e062d6e17dedfbf256c7922612d1`.
- **Manifesto verificável:** [snapshot dos recursos](EXACT-RESOURCE-MANIFEST-1.0.10.json) e [auditoria da CI](https://github.com/Gustavaopere/Black-Arcana/actions/runs/40985275338).

## Campos JSON confirmados no artefato

| Campo | Valor literal do recurso | Limite de interpretação |
|---|---|---|
| `message_id` | `radiation` | Chave de mensagem; não é sinônimo do registro nem classe de implementação |
| `scaling` | `never` | Campo `scaling` do tipo de dano; não fixa dano causado nem curva de perks |
| `exhaustion` | `0.1` | Valor do campo `exhaustion`; **não** é mana, stamina, custo do feitiço ou dano |

## Tags de tipo de dano declaradas diretamente

- Nenhuma entrada direta para este ID nos seis arquivos `tags/damage_type/*.json` encontrados no artefato.

Essas são **entradas textuais diretas** dos seis arquivos `data/*/tags/damage_type/*.json` encontrados no JAR. Elas não comprovam as tags finais resolvidas depois de datapacks, outras dependências ou overrides. Uma referência a tag não prova que o ataque usado no jogo produza este `DamageSource`.

## Superfícies necessárias para perks — ainda não auditadas

| Capacidade pretendida | Situação |
|---|---|
| Factory de `DamageSource` / chamadas JVM | ✅ localizadas estaticamente; comportamento e caminhos efetivos `NÃO VERIFICADO` |
| Origem, atacante, owner, attribution e condições de PvP | ⚠️ factory sem parâmetro de entidade confirmada; atribuição causal/PvP ainda não verificados |
| Fórmula de dano, mitigação, críticos e resistências | ⚠️ cálculo de dano **solicitado** no consumidor `IrradiatedEffect.tick` documentado abaixo; aceitação/mitigação não verificadas |
| Alvos elegíveis, tipo target/área, alcance, raio e filtros | ⚠️ alvo no tick é a entidade que já possui o status; filtros de aplicação são específicos dos produtores; alcance/área genéricos não existem no `DamageType` |
| Entidades/projéteis, tamanho, velocidade, colisão e homing | ⚠️ nenhum projétil pertence à factory de `radiation`; emissores indiretos não estão encerrados |
| Duração, intervalo de hits, custo de ação e cooldown de casting | ⚠️ frequência `shouldTick` documentada para `Irradiated`; duração/custo/cooldown variam por produtor, sem contrato global |
| Persistência, ordenação de eventos, server authority e deduplicação | `NÃO VERIFICADO` |
| Hook de mutação seguro na versão instalada | `NOT_VERIFIED` |
| QA real em modpack/multiplayer | `NOT_TESTED` |

## Boundary / decisão provisória

O *provider* mantém autoridade sobre a criação, classificação e aplicação de dano. Black Arcana não altera `DamageSource`, escola, dano, tags ou projéteis sem evidência dos consumidores Java e hooks seguros. O RPG Skill Tree fornece perks/atributos somente através de boundary verificada, sem double-processing. **Fail-closed:** `NO_MUTATION` até a auditoria dos consumidores e a validação específica.

**Contabilidade:** 1/11 recursos de tipo de dano documentados; **+0 raízes mágicas novas**. Este objeto não recebe status `COMPLETE_PERK_READY` apenas por existir como JSON.

## Evidência compilada 1.0.10 — factory e consumidores diretos

**Escopo:** `SHA_EXACT_STATIC_FACTORY_AND_DIRECT_CALLSITE_ONLY`. [Manifesto dos consumidores](EXACT-CONSUMERS-1.0.10.json) · [CI da auditoria](https://github.com/Gustavaopere/Black-Arcana/actions/runs/40993193816).

- **Classe de fábrica:** `com/github/alexmodguy/alexscaves/server/misc/ACDamageTypes.class`, SHA-256 `389fb88f8d6e1515e3dfe7f401a728bb33629666bd2319ae7e25668f710e4ef6`.
- **Método:** `ACDamageTypes.causeRadiationDamage`.
- **Descritor JVM:** `(Lnet/minecraft/core/RegistryAccess;)Lnet/minecraft/world/damagesource/DamageSource;`.
- **Campo de DamageType lido:** `RADIATION` (offset `19`).
- **Construtor de DamageSource referenciado:** `Method com/github/alexmodguy/alexscaves/server/misc/ACDamageTypes$DamageSourceRandomMessages."<init>":(Lnet/minecraft/core/Holder$Reference;I)V`.
- **Parâmetros da factory:** apenas `RegistryAccess` — nenhum argumento `Entity` na assinatura da factory.
- **Referências `invokestatic` encontradas:** 1 em 1 classes. Isso não representa quantidade de hits por ataque.

| Classe chamadora | Método chamador | Descritor JVM | Offset | Opcode |
|---|---|---|---:|---|
| `com/github/alexmodguy/alexscaves/server/potion/IrradiatedEffect.class` | `public void tick(net.minecraft.world.entity.LivingEntity, int)` | `(Lnet/minecraft/world/entity/LivingEntity;I)V` | 74 | `invokestatic` |

**Limites:** as invocações são referências estáticas no bytecode exato; não demonstram execução, alcance, área, cooldown, fórmula de dano, filtros de alvo, persistência, autoridade/attribution, proteção PvP nem segurança de intercepção. Chamadas indiretas, mixins, reflexão, datapacks e comportamento do modpack não estão comprovados. **`mutating_hook=NOT_VERIFIED`, `physical_qa=NOT_TESTED`, `NOT_CERTIFIED`**. Black Arcana e RPG Skill Tree devem preservar o settlement nativo, evitando processamento duplicado e aplicando `NO_MUTATION` sem contrato seguro.

## Contrato cruzado — aplicação real de `radiation` pelo status `Irradiated` (2026-10-31)

**Escopo:** contrato estático **do consumidor direto** observado no JAR exato 1.0.10. A ficha [Irradiated](../effects/irradiated.md) possui auditoria binária individual certificada no [manifesto de efeitos](../EXACT-EFFECT-CONTRACTS-1.0.10.md). A relação entre o efeito e o tipo de dano provém do callsite `IrradiatedEffect.tick → ACDamageTypes.causeRadiationDamage → LivingEntity.hurt`, não de uma inferência baseada nos nomes. Isso **não** promove automaticamente esta ficha de tipo de dano a `COMPLETE_PERK_READY`.

### Unidade causal e identidade de quem causa dano

- `ACDamageTypes.causeRadiationDamage(RegistryAccess)` constrói `DamageSourceRandomMessages(holder, 2)` para `RADIATION`. A assinatura **não recebe `Entity` atacante, projétil ou owner**. Perks que dependem da origem de kills, lifesteal, Mastery, dano do jogador ou PvP **não podem reconstruir autoria a partir dessa factory**.
- O consumidor `IrradiatedEffect.tick(LivingEntity, int)` passa a própria entidade afetada para `LivingEntity.hurt`; o `int` deste método é o amplifier do efeito, **não o dano infligido**.
- A chamada de `hurt` ignora o boolean de retorno no bytecode observado. Logo, `hurt` chamado, dano aceito, dano líquido e kill são eventos diferentes; não contabilizar proc/XP sem causalidade própria e deduplicação.
- A factory está relacionada ao **dano periódico do status**; a aquisição da irradiação pode ocorrer por itens, blocos, bosses, nuvens, explosões ou Raygun, sob gates distintos. `radiation.json` não define área, range, cooldown, custo ou geometria.

### Frequência, proteção Hazmat e custo — valores do consumidor

`IrradiatedEffect.shouldTick(duration,a)` retorna `false` quando `a<=0`. Para `a>0`, computa `j = 200 / a` com divisão inteira; se `j>1`, o tick é elegível quando `duration % j == j/2`; caso contrário é elegível a cada chamada. Exemplos de **período nominal**, não garantias de dano aceito: `a=1 → j=200`, `a=2 → j=100`, `a=3 → j=66`, `a>=101 → j<=1`. O amplifier não multiplica diretamente o dano por hit.

O consumidor conta peças **exatas** de Hazmat nos quatro slots (`h=0..4`), computa `s=1F-0.25F*h` e, para alvo que não é `RaycatEntity`, sorteia `nextFloat() < s+0.1F` para pedir `hurt(radiationSource, s)`.

| Peças Hazmat `h` | `s` passado a `hurt` | Probabilidade nominal de passar o sorteio |
|---:|---:|---:|
| 0 | 1,00 | 100% (limiar 1,10) |
| 1 | 0,75 | 85% |
| 2 | 0,50 | 60% |
| 3 | 0,25 | 35% |
| 4 | 0,00 | 10% (ainda pode chamar `hurt` com zero) |

O `Player` com **zero** peças Hazmat recebe `causeFoodExhaustion(0.4F)` antes do sorteio de dano. Esse gasto específico de alimentação **não** é o campo `exhaustion:0.1` do `DamageType`; não somar os dois como custo de mana/stamina do BA. Mitigação, imunidades efetivas, multipliers do modpack e resultado físico de `hurt(0)` continuam desconhecidos.

### O que o status afeta além de `hurt`

- A presença de `Irradiated` é consultada por `CommonEvents.acLivingHeal`: o `LivingHealEvent` é cancelado quando o alvo tem o efeito **e** seu tipo não está no tag dinâmico `ACTagRegistry.RESISTS_RADIATION`. Essa condição não depende do amplifier e **não prova bloqueio de qualquer mudança arbitrária de vida**.
- O `IrradiatedEffect.tick` **não executa diretamente** uma checagem `RESISTS_RADIATION`; os produtores têm filtros próprios. Não transformar o tag em imunidade universal ao dano, nem assumir que ter o efeito garante dano no amplifier zero.
- `RaycatEntity` é excluído do ramo de dano deste consumidor, mas usa `Irradiated` em sua própria AI e em efeitos de absorção/cura; `TremorzillaEntity` também possui tratamento específico. São consumidores de efeitos, **não novos damage types nem casts**.

### Exemplos de duração/área do produtor, não do tipo de dano

| Aplicador exato | Evidência observada | Fronteira |
|---|---|---|
| `UnrefinedWasteBlock.entityInside` | instância por 4.000 ticks, amplifier 0 | aplicação não implica dano periódico por `shouldTick` |
| `NuclearFurnaceComponentBlock.entityInside` | 2.000 ticks, amplifier 3 | produtor possui gates próprios |
| `RaygunItem.onUseTick` | 800 ticks com amplifier `radiationLevel` calculado pelo item, após hit aceito em alvo elegível | alcance do Raygun não é propriedade do `DamageType radiation` |
| `NuclearExplosionEntity.tick` | 48.000 ticks, amplifier 1 ou 2 dependendo de tamanho/ramo | não confundir duração do status com vida da explosão; rota nuclear segue bloqueada para mutação |
| `NuclearFurnaceBlockEntity.destroyWhileCritical` | nuvem com instância-base 9.600 ticks; raio 8F; vida da nuvem 12.000 ticks | raio é da `AreaEffectCloud`, não do dano periódico |
| `RadioactiveItem.acInventoryTick` | 1.800 ticks, amplifier 0, sujeito ao sorteio e Hazmat | item e efeito possuem authorities e condições separadas |

### Perks, QA e decisão

- **Potenciais eixos de perk a pesquisar**: resistência ao status; alteração de frequência e dano periódico; modulação de Hazmat; chance de aplicação por produtor; cura em `LivingHealEvent`; propagação por nuvens e explosões.
- **Status real dos mutadores:** nenhum desses eixos possui hook provider-native validado para o JAR 1.0.10. `NO_MUTATION`, sem injetar `LivingEntity.hurt` ou `MobEffectInstance` em paralelo e sem gerar perks ofensivas a partir de ticks de backlash.
- **QA requerida:** verificar amplifier 0 e >0, quatro peças Hazmat, `hurt(0)`, cancelamento de cura, donos/atribuição, emissões por vários produtores, override de tags, reinício, servidor dedicado e multiplayer. Nenhum cenário é declarado `PASS` nesta revisão.
- **Contabilidade preservada:** `damage-types/radiation.md` continua ⚠️ `NOT_CERTIFIED`; `effects/irradiated.md` já tinha certificado estático específico. Nenhum novo objeto, alteração de índices, Stage, hook ou contagem global.

**Fontes locais:** [efeito e offsets](../effects/irradiated.md) · [evidência binária de efeitos](../EXACT-EFFECT-CONTRACTS-1.0.10.md) · [factory/consumidores diretos](../EXACT-CONSUMERS-1.0.10.json).
