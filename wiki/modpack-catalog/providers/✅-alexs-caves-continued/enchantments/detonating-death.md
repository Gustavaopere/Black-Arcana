# Detonating Death — explosão de encerramento da possessão (publisher 1.0.10)

**Estado:** ⚠️ **ficha individual parcial/condicionada** de `alexscaves:detonating_death`. O recurso, o consumidor `TotemOfPossessionItem` e a entidade de explosão `TotemExplosion` já possuem evidência de JAR SHA-exata no contrato existente da ação de possessão. Esta ficha detalha o encantamento e suas implicações para perks; **não promove certificado técnico individual, hook, Stage nem QA física**. `mutating_hook=NOT_VERIFIED` · `physical_qa=NOT_TESTED` · `perk_certification=NOT_CERTIFIED` · `NO_MUTATION`.

**Descrição funcional:** quando o Totem of Possession entra no caminho de encerramento por perda/morte do alvo vinculado **ou esgotamento da durabilidade**, o encantamento pode detonar uma explosão na posição da entidade controlada, **se a entidade ainda for resolvida pelo código**. A explosão é atribuída ao usuário, escala seu raio pela **largura** do controlado, produz dano e knockback próprios e solicita `BlockInteraction.KEEP`. Isso é uma ramificação da **mesma ação provider-native de possessão**, não um cast autônomo nem uma nova raiz mágica.

## 1. Artefato, identidade e fonte de autoridade

| Fonte | Evidência |
|---|---|
| Provider / alvo | Alex's Caves Continued, `alexscaves`, Minecraft **1.21.1** / NeoForge |
| JAR publisher | `alexscaves-1.0.10-neoforge+1.21.1.jar`, **75.279.314 bytes** |
| SHA-1 | `6960b299a39a039ac8a5eb9b07be4ad0e3e0a570` |
| SHA-256 | `36ae0a3cbd028df466a37c671ba2fdf021c060ca1c9c1c32e9f2e95bffae0e7c` |
| Recurso de encantamento | `data/alexscaves/enchantment/detonating_death.json`; SHA-256 **`8402461954ff5b249ae675b51d7dcc23d933b2b06c494b327bf608371298646e`** |
| Tag de suporte | `data/alexscaves/tags/item/enchantable/totem_of_possession.json`; SHA-256 `185a085206993877d91ca6d8c697273c14f945b1d55cb6179e3236c138c357cf` |
| Consumer compilado | `server/item/TotemOfPossessionItem.class`; SHA-256 `bad9dd8b88eb621b558d1ede477d2b4ba6a21befdec31b4a0233adcac701773e` |
| Explosão compilada | `server/entity/util/TotemExplosion.class`; SHA-256 `b798d95de5adf72f517a224331675da78277e0ae0e03435b2c8ac72f799cd815` |

O JAR foi auditado anteriormente e suas provas permanecem em [`EXACT-TECHNICAL-CONTRACTS-1.0.10.json`](../EXACT-TECHNICAL-CONTRACTS-1.0.10.json), [memorial do contrato](../EXACT-TECHNICAL-CONTRACTS-1.0.10.md) e na ação [Totem of Possession — Possession / Remote Control](../actions/totem-possession-remote-control.md). Esta ficha usa **os mesmos classfiles, offsets e semântica auditados**, sem baixar/decompilar novamente o JAR nem copiar a implementação do provider.

A fonte pública adjacente `Codx-org/AlexsCavesContinued@523308608422ab8e31974befa7111ecdf495dd37` declara **1.1.1**, não a versão instalada. Ela não deve ser usada para atribuir parâmetros ao binário 1.0.10 sem igualdade de bytes comprovada. A documentação abaixo distingue o contrato estático SHA-exato de resultados em gameplay ainda desconhecidos.

## 2. Definição JSON — nível, custo e exclusão

| Campo declarativo | Valor no artefato publisher 1.0.10 |
|---|---|
| `description.translate` | `enchantment.alexscaves.detonating_death` |
| `supported_items` | `#alexscaves:enchantable/totem_of_possession` |
| `weight` | `2` — peso de encantamento, **não** probabilidade de explosão |
| `max_level` | `1` (I); a condição do consumer testa apenas se o nível é positivo |
| `min_cost` | `base=1`, `per_level_above_first=11` |
| `max_cost` | `base=41`, `per_level_above_first=10` |
| `anvil_cost` | `4` |
| `slots` | `mainhand` |
| `exclusive_set` | `alexscaves:astral_transferring` |

Os custos de enchanting para o **único nível declarado** são **1–41**. Os coeficientes `per_level_above_first` não autorizam níveis II+; não se transformam em mana, durabilidade por explosão, probabilidade de proc ou alcance.

O item base é `alexscaves:totem_of_possession`. O encantamento **não substitui** o vínculo por UUID, a resistência de entidades, a restrição configurável de controlar Players ou o critério de linha de visão do Totem. A exclusão com **Astral Transferring** é declarativa. O sistema efetivo de combinação/override por datapacks e stacks artificialmente encantadas permanece não verificado; não assumir que ambos sejam sempre impossíveis no runtime.

## 3. Causalidade — `TotemOfPossessionItem.onUseTick`

**Owner JVM exato:** `com.github.alexmodguy.alexscaves.server.item.TotemOfPossessionItem`.

**Assinatura:** `onUseTick(Level,LivingEntity,ItemStack,int)V`; descriptor:
`(Lnet/minecraft/world/level/Level;Lnet/minecraft/world/entity/LivingEntity;Lnet/minecraft/world/item/ItemStack;I)V`.

O contrato SHA-exato divide os offsets da rotina em `0–142` (encerramento), `143–229` (gates de parada), `230–272` (desgaste no cliente), `275–648` (movimento), `651–714` (partículas) e `717–1084` (ataques/transferências no servidor). No ramo inicial são localizáveis `Explosion.BlockInteraction.KEEP @87`, `TotemExplosion.explode() @97` e `TotemExplosion.finalizeExplosion(true) @103`.

**Sequência condicionada:**

1. O item obtém a entidade controlada com o contrato de `getControlledEntity`, cuja resolução por UUID é limitada ao `ServerLevel` corrente. O corpo testa a existência do vínculo, a vida da entidade e a durabilidade da stack. **Perda/morte da entidade vinculada ou desgaste máximo** podem alcançar o ramo de encerramento.
2. A explosão só é criada quando o nível de `DETONATING_DEATH` é **positivo** **e** a entidade `controlledEntity` ainda é **não nula**. Uma entidade morta ainda resolvível pode entrar na condição; uma entidade ausente/não resolvível não fornece posição para criar a explosão.
3. Usa **`controlledEntity.getX/Y/Z`** como origem, o **usuário do Totem** como fonte, e raio `R = 2F + floor(controlledEntity.getBbWidth())`. A dimensão é a **largura do controlado**, não sua altura, não um alcance entre usuário e controlado.
4. Instancia `TotemExplosion` com `BlockInteraction.KEEP`, chama `explode()` e `finalizeExplosion(true)`. Esse percurso não implementa o mesmo predicado de alianças usado nos ataques normais da possessão.
5. Ao encerrar, a rotina desmarca o alvo resolvido quando aplicável, limpa dados de vínculo na stack, interrompe o uso e envia atualização de tag pelo caminho nativo. **Não** é seguro supor que o alvo esteja sempre resolvido para limpeza de marker, ou que um novo adapter deva tentar reproduzir essa operação.

**Nuances:** perder de vista o controlado, parar voluntariamente o uso ou ser rejeitado pelo gate configurado pode interromper comandos sem atingir a mesma explosão; **não** modelar Detonating Death como `onUseRelease` incondicional. O ramo inspecionado de detonação não tem guarda explícita de `!level.isClientSide`. Isso é uma **lacuna de autoridade estática**, não prova de explosão duplicada em cliente/servidor.

A descrição do encantamento pode mencionar morte em combate, mas o código **também** considera **esgotamento de durabilidade**; e a resolução nula pode impedir o evento. Portanto, "explode sempre que morre" é falso como contrato do item.

## 4. Geometria, targeting, dano e consequências

O provider cria uma explosão **centrada no corpo da entidade controlada**, não no jogador, no ponto visado pelo raycast nem na última posição salva em `BoundEntityTag`.

| Campo | Semântica verificada estaticamente |
|---|---|
| Raio de referência `R` | `2 + floor(largura do controlado)`; sem aumento pela quantidade de níveis I/II nem atributo do RPG Skill Tree |
| Distância de candidatos | Usa a normalização `q = distance/(2R)` e processa candidatos elegíveis com `q<=1`. A área de consulta/efeito não equivale à esfera nominal de `R` sem considerar a expressão `2R` |
| Exposição | `e` é a exposição ao bloco/ambiente na função de explosão; `b = (1-q)×e`. Geometria, obstrução e efeitos de mundo pertencem à implementação de `TotemExplosion` |
| Dano solicitado | `floor(((b²+b)/2) × 7 × 2R + 1)`, com `b` acima; **não é vida final retirada**, nem dano fixo por alvo ou por tick |
| Knockback | Vetor dependente de distância e exposição; não tratar como teleporte, fear, stun ou força independente do owner |
| Filtros especiais | O código da explosão exclui o **usuário fonte** da seleção, delega imunidade de explosões a `ACPlatform.ignoreExplosion` e pula explicitamente `Luxtructosaurus` |
| Aliados e PvP | Não reaproveita as exclusões recíprocas de aliados do ataque normal do Totem. Proteção, PvP, outros addons e fontes de imunidade exigem QA específica |
| Blocos | `Explosion.BlockInteraction.KEEP` no callsite. Este caminho **não solicita destruição de blocos por sua interação de explosão**; não presumir inexistência de outros efeitos laterais em todos os mods |
| Dano/tipo/atribuição | Usa o settlement do `TotemExplosion`, não um novo tipo inventado por Black Arcana. A origem fornecida é o usuário, mas a autoria completa de kills/XP e event bus deve ser comprovada antes de perks |
| Falha geométrica | A direção de comprimento zero do centro até os olhos de um candidato é pulada (TNT usa Y dos pés). Não garantir dano num alvo geometricamente coincidente |

A largura efetiva do controlado pode variar entre mobs, atributos e outros mods. **Não** inventar um valor numérico universal de `R`, dano, vítimas ou raio máximo do modpack. Mesmo que o JSON só permita nível I, o valor de `R` depende da entidade, não do nível.

A explosão ocorre dentro da **mesma ação semântica de possessão**. Não confundir a área de explosão com a AABB `inflated(3)` usada para selecionar alvos de ataque normal, nem com o alcance do raycast de movimento. O Totem não cria um "projétil Detonating Death" neste caminho; a entidade `TotemExplosion` é uma operação de explosão local, com seus próprios efeitos.

## 5. Recursos, encerramento e riscos de integração

O Totem mantém `BoundEntityUUID`, `BoundEntityTag` e `ControllingEntityID` na stack, além do marker persistente `TotemPossessed` na entidade. O encadeamento de cliente/servidor e a falta de garantia de limpeza uniforme já foram auditados na [ficha principal da possessão](../actions/totem-possession-remote-control.md).

A durabilidade pode terminar o controle, mas o consumidor de **Detonating Death não debita uma segunda carga exclusiva pela explosão** na região catalogada. A documentação existente aponta desgaste em ramo de cliente e atualização de `CUSTOM_DATA`, que **não são prova de settle seguro no servidor dedicado**. Não declarar custo de mana nem cooldown específico adicional.

Uma perk que altere explosão, raio, dano, tipo de alvo, chance, knockback, duração do controle, número de controlados ou quantidade de detonações precisaria de **seam real e server-authoritative**. O projeto não tem contrato comprovado para mudar `R`, interpor filtro de aliados, cancelar/aplicar novamente `hurt`, forçar `finalizeExplosion` ou reexecutar reset de binding.

**Riscos estáticos que exigem fail-closed:**

- **Multiplicação de dano/proc:** repetir a explosão a partir de tick, evento de morte ou evento de quebra da stack pode gerar **duplo settlement** no provider. A contagem de Mastery por tentativa de trigger não é a de explosões realmente aceitas.
- **Alvo e autoridade:** ao associar a explosão ao player, não inferir autorização PvP/claims, linha de visão, ownership único do vínculo ou proteção automática de aliados.
- **Servidor e replay:** o callsite não traz guarda explícita por lado; a prova ainda não assegura at-most-once entre cliente/dedicado, nem idempotência após transferência/reload.
- **Mundo:** `KEEP` é propriedade nativa observada. Se um efeito **próprio** de Black Arcana viesse a modificar blocos ou hazards, teria de passar por `WorldEffectPolicy` e budgets; isso não permite reimplementar a explosão do provider.
- **Persistência:** desconexão, dimensão, entidade descarregada, morte, stacks duplicadas/transferidas e reset da stack não têm homologação específica. O marker `TotemPossessed` não carrega uma identidade de dono segura para fins de gates.
- **Desempenho:** a explosão executa consulta e exposição por entidade. Não acrescentar nova varredura ou explosão por tick sem limites, autorização e responsabilidade de custos.

## 6. Matriz para perks e siblings

| Perk potencial | Observação útil | Condição atual |
|---|---|---|
| Aumentar `R` / área | `R=2+floor(width)` e consulta efetiva em função de `2R` | ⛔ Sem hook mutador verificado; área não pode escalar sem cap/budget |
| Aumentar dano/knockback | Dano solicitado depende de `R`, `q` e exposição `e` | ⛔ Sem modificação safe de `TotemExplosion` e sem autorreferência a eventos |
| Reduzir custo / prolongar controle | Consumidor depende do lifetime/stack durability do Totem | ⛔ Sem prova de custo transacional e durabilidade servidor |
| Alterar alvos / poupar aliados | Seleção da explosão usa exceções específicas diferentes das do ataque normal | ⛔ Sem seam autorizado de targeting/PvP/claims |
| Duplicar explosões / expandir controlados | Um callsite `explode` + `finalizeExplosion` no ramo de encerramento | ⛔ Sem dedupe, at-most-once e limites de entidades |
| Melhorar dano-tipo / school | Settlement de `TotemExplosion`, não school próprio de Black Arcana | ⛔ Não classificar/escrever `DamageType` sem bridge real |
| Conferir Mastery | Posição/controlado/usuário são disponíveis no fluxo nativo, mas atribuição final é desconhecida | ⚠️ Leitura futura apenas se um evento provider-owned e idempotente existir; não contar ticks |
| UI/descrição | JSON nível I, raio dependente de largura e pré-condição de término | ⚠️ Informativo; não confundir a descrição com autoridade de runtime |

**Fronteira de arquitetura:** Black Arcana é autoridade de seu próprio casting, hazards, persistência e políticas de mundo. RPG Skill Tree é sibling/provider de **progressão, atributos, Mastery, perks e gates** mediante contratos reais; não assume o runtime do Totem. `minecraft-mod-factory` é uma possível referência de tooling futura, **não** uma autorização para portar métodos ou assets do provider.

## 7. Estados e verificação pendente

**Comprovado estaticamente no publisher 1.0.10:** ID e JSON, item suportado e exclusão, nível/custos, owner classfile e offsets de encerramento, seleção da posição/raio, `KEEP`, criação/finalização, fórmula do dano e filtros nativos descritos no contrato da ação.

**Não verificado fisicamente:** morte natural e combate, esgotamento da durabilidade, entidade morta mas resolvida, entidade descarregada ou em outra dimensão, null e fallback, ambos os lados do runtime, zero/uma/múltiplas detonações, aliados/PvP, proteção de claims, exposições/knockback/dano real, passivos/efeitos de mods, coexistência com Astral, custos/XP/loot, crash/reload e multiplayer.

**Resultado atual:** `resource_and_selected_JVM_evidence=EXACT_EXISTING`; `individual_static_certification=NOT_CERTIFIED`; `mutating_hook=NOT_VERIFIED`; `physical_qa=NOT_TESTED`; `provider_catalog_closed=false`; `perk_certification=NOT_CERTIFIED`; `NO_MUTATION`.

**Contabilidade desta ficha:** **+1 documento individual parcial**, **+0 contratos estáticos novos certificados**, **+0 raízes de magia**, **+0 providers concluídos**. Próximo recurso em ordem alfabética: **`alexscaves:double_stab`**.
