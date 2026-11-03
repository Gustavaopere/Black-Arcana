# Bouncing Bolt — ricochete nativo do Sea Staff (1.0.10)

**Estado:** ⚠️ ficha técnica **parcial/condicionada**; identidade, JSON publisher, produtores e consumidores selecionados comprovados pelo binário exato. **Não** é uma nova magia/cast independente. O comportamento modifica a mesma ação [Sea Staff — Water Bolt](../actions/sea-staff-water-bolt.md).

**Integração:** `mutating_hook=NOT_VERIFIED`, `physical_qa=NOT_TESTED`, `perk_certification=NOT_CERTIFIED`, `NO_MUTATION`. A certificação do contrato estático da *ação* Sea Staff não homologa automaticamente o encantamento para perks mutadoras.

## 1. Identidade, versão e autoridade

- Provider/mod ID: Alex's Caves Continued / `alexscaves`.
- Encantamento: `alexscaves:bouncing_bolt`; chave de tradução `enchantment.alexscaves.bouncing_bolt`. Nenhuma descrição textual do jogador foi revalidada na versão física.
- Item: `alexscaves:sea_staff`, declarado na tag `#alexscaves:enchantable/sea_staff`. Trigger da magia raiz: uso intencional do Sea Staff; o encantamento reage ao *settlement* de seus Water Bolts.
- JAR publisher da modlist física: `alexscaves-1.0.10-neoforge+1.21.1.jar`, 75.279.314 bytes. SHA-1 `6960b299a39a039ac8a5eb9b07be4ad0e3e0a570`; SHA-256 `36ae0a3cbd028df466a37c671ba2fdf021c060ca1c9c1c32e9f2e95bffae0e7c`.
- Manifesto selado da análise individual: [EXACT-BOUNCING-BOLT-1.0.10.json](../EXACT-BOUNCING-BOLT-1.0.10.json); gerado por [sonda read-only](../../../../../docs/qa/alexscaves_1010_bouncing_bolt_probe.py), com [testes de regressão sintética](../../../../../docs/qa/alexscaves_1010_bouncing_bolt_probe_test.py) e [workflow dedicado](../../../../../.github/workflows/alexscaves-1010-bouncing-bolt.yml).
- Contrato anterior da ação, sem duplicação de raiz: [EXACT-TECHNICAL-CONTRACTS-1.0.10.json](../EXACT-TECHNICAL-CONTRACTS-1.0.10.json) e [ficha Sea Staff](../actions/sea-staff-water-bolt.md).
- A árvore pública `Codx-org/AlexsCavesContinued@523308608422ab8e31974befa7111ecdf495dd37` declara versão **1.1.1**; não é autoridade para os números 1.0.10. A sonda extrai JSON e seleções de bytecode da release física.

## 2. Definição do encantamento — JSON exato

| Campo publisher | Valor verificado |
|---|---|
| Recurso | `data/alexscaves/enchantment/bouncing_bolt.json` |
| SHA-256 do recurso | `bc103328ad554dd97348becf898d5ecedd2867385d1ffbd756cf04ec302d24e7` |
| `supported_items` | `#alexscaves:enchantable/sea_staff` |
| `weight` | `2` — peso de geração/encantamento, não chance de ricochete |
| `max_level` | `1` |
| `min_cost` | `base=1`, `per_level_above_first=13` |
| `max_cost` | `base=41`, `per_level_above_first=10` |
| `anvil_cost` | `4` |
| `slots` | `mainhand` |
| `exclusive_set` | `["alexscaves:triple_splash"]` |

A tag publisher `data/alexscaves/tags/item/enchantable/sea_staff.json` (SHA-256 `22e45ab74b71d7152ccc531a633e5149df9c12eece40464c85c50f5a600fd80e`) lista `alexscaves:sea_staff`. O outro recurso auditado, `triple_splash.json` (SHA-256 `6946e2d21814f3e398925f2886a6284b140032b255a05f9598c8e00e2bc315be`), declara também nível máximo I e está no mesmo conjunto de itens; a **exclusão explícita de Triple Splash é declarada no JSON de Bouncing Bolt**. A aquisição real, o valor efetivo de tags de encantamento e a compatibilidade sob datapacks/editors permanecem `NOT_VERIFIED`.

**Os custos acima são custos de encantamento**, não cobrança de mana, duração, durabilidade por hit ou número de ricochetes. O uso normal do Sea Staff solicita 1 de durabilidade se o jogador não estiver em `instabuild`, conforme a [ação base](../actions/sea-staff-water-bolt.md). O encantamento **não demonstra um débito próprio de recurso por ricochete**.

## 3. Ativação no disparo, ownership e persistência da flag

**Produtor:** `com/github/alexmodguy/alexscaves/server/item/SeaStaffItem.class` (SHA-256 `cb3153a35e7f4c3ab23e68693aec110edf03ecd050c3b485e35ccbb257b4bbc6`).

**Método `use(Level,Player,InteractionHand)InteractionResultHolder`:** 189 instruções JVM, digest do parse `fc071fd36310ddb6a082d46113930b78fa89d1f0b4a1a9bfc749d2bd11c1ba7c`. A região relevante contém:

1. `ACEnchantmentRegistry.BOUNCING_BOLT @299`.
2. `ACCompat.enchantLevel @302`, `ifle @305 → 314`: nível positivo abre o ramo do encantamento.
3. `iconst_1 @310`, `putfield WaterBoltEntity.ricochet @311`: habilita a flag no Water Bolt principal.

O contrato anterior da ação estabelece disparo somente pelo ramo servidor, `owner` atribuído pelo Sea Staff, velocidade inicial baseline 2F no projétil central, imprecisão 12F e aquisição inicial de alvo por rayclip até 128D. Esses valores pertencem ao **cast principal**, não ao raio de ricochete. A presença simultânea de Triple Splash em stacks não convencionais não foi testada; o `exclusive_set` é um contrato de dados, não uma proibição absoluta em cenários alterados.

A flag `ricochet` não tem confirmação de persistência pelos overrides NBT `readAdditionalSaveData`/`addAdditionalSaveData` do Water Bolt; esses métodos gravam apenas `Bubbling` no recorte certificado. Não prometer restauração de um ricochete pendente após reload.

## 4. Seleção de hit, consumo da flag e passagem ao novo bolt

**Consumidor:** `com/github/alexmodguy/alexscaves/server/entity/item/WaterBoltEntity.class`, SHA-256 `342c011b0178e1f65cd2e6ef315fe6bad49bd5ead237b2274e822560e2eac401`.

**Método `damageMobs()V`:** 105 instruções, digest do parse `5a74cbf8fa1793ffeb6f0107be742e82cf2035d27f96f238e0a672ce005e653d`.

- O processo de impacto pesquisa `LivingEntity` na caixa do Water Bolt inflada **2D por eixo**; exclui owner, aliados e `DeepOneBaseEntity`, conforme o contrato da ação. A solicitação de dano é `3F` usando `mobProjectile(this, owner living ou null)`, não a confirmação de dano aceito.
- Na região selecionada, `ACCompat.hurt @139` é seguido por um branch `ifeq @142 → 216`. O antigo contrato do Sea Staff assinala que o último candidato elegível é referenciado **antes** do retorno de `hurt`. A seleção de origem do ricochete não é, portanto, uma prova de que o dano daquela entidade foi aceito.
- Ao final da iteração, `getfield ricochet @220` e `ifeq @223 → 242` condicionam o único handoff. A região `@228–239` testa alvo de referência, escreve `ricochet=false @233` e chama `onRicochetHit(Entity) @239`.
- O consumo da flag impede que o mesmo Water Bolt reexecute a mecânica em chamadas posteriores à rotina, nas condições analisadas. O fato **não** prova que um filho sempre apareça, porque existe novo filtro de candidato e um spawn cujo retorno não foi certificado.

**Não confundir:** `BUBBLED` é um efeito distinto, condicionado a `Enveloping Bubble` e aceitação do efeito. O ricochete não reaplica dano automaticamente no mesmo ponto de impacto nem representa área extra de `32` blocos.

## 5. Busca do alvo secundário e construção do projétil filho

**Método `onRicochetHit(Entity)V`:** 122 instruções, digest do parse `5b9bcc73dc65afc1e728f864f733cb297af322e6bba32bc1f9988a19a7ac3fad`.

1. `getOwner @1`; `Entity.getBoundingBox @6`; `AABB.inflate(32D,32D,32D) @9–18`; `Level.getEntitiesOfClass(LivingEntity.class, AABB) @32`. A expansão é **da AABB da entidade atingida** e produz candidatos; **não** altera o tamanho da hitbox do projétil, sua velocidade, alcance total nem o raio de dano.
2. Filtros compilados incluem `isAlliedTo @67/@106`, exclusão de `DeepOneBaseEntity`, teste `entity.is @84/@97`, distância relativa `distanceTo @115/@134/@140` e comparação com limite estrito `>3D @119–123`. O contrato anterior descreve seleção do candidato mais próximo **da entidade atingida**, não do caster nem de um ponto fixo.
3. A presença de um destino secundário e de `owner instanceof LivingEntity` antecede a criação do filho, com ramos `ifnull @156 → 270` e `ifeq @163 → 270`. Sem owner vivo/resolvido ou sem outro candidato, o método não prova um novo projétil.
4. O método cria `WaterBoltEntity(Level,LivingEntity) @182`, copia a posição da entidade original (`copyPosition @190`), atribui `setArcingTowards(UUID) @200`, forma uma direção normalizada a partir da posição do alvo acrescida de deslocamento vertical, com constante `0.3F @209`, soma essa direção à velocidade nativa e solicita `setDeltaMovement @248`.
5. Copia a flag visual `Bubbling` por `isBubbling @254` / `setBubbling @257` e tenta `Level.addFreshEntity @266`. **Uma chamada de spawn não comprova retorno de sucesso, chegada ao alvo ou dano aceito.**

O contrato estático do Sea Staff também registra que o **filho não copia a flag `ricochet`**, utiliza o default `seekAmount=0.3F` do construtor, não herda a modificação do encantamento `Soak Seeking` e não gera um novo cast deliberado de jogador. Esses defaults foram certificados no escopo da ação base e são reutilizados, **sem duplicar a contagem de magia**.

A busca do ricochete não possui chamada própria de linha de visão no método selecionado; isso não demonstra comportamento de colisão durante o trajeto do projétil filho nem autoriza ignorar proteção, chunks ou filtros de outros mods.

## 6. Matriz de parâmetros para perks — fronteiras de segurança

| Eixo | Dado estático que pode orientar design | Estado de integração |
|---|---|---|
| **Número de ricochetes** | Flag booleana consumida em `damageMobs`, filho com defaults nativos | ⛔ Sem hook seguro para múltiplos saltos; não copiar spawn nem rearmar flag externa |
| **Alvo secundário** | `getEntitiesOfClass` sobre AABB do hit, filtros de owner/aliança e `DeepOneBaseEntity`; busca de candidato próximo da origem | ⛔ Sem reclassificação de alvos, critérios de exclusão ou preferência manipulados por perk sem contrato |
| **Range da busca** | `AABB.inflate(32D,32D,32D)`, independente dos 128D de aquisição inicial e 2D de dano | ⛔ Sem alteração certificada do range; `32D` não é raio de dano, nem distância máxima de voo |
| **Dano / tipo** | `damageMobs` solicita `3F` com fonte `mobProjectile`; filho usa pipeline nativo | ⛔ Não aplicar segundo `hurt`, alterar `DamageSource` ou creditar kill/XP por spawn |
| **Velocidade / trajetória** | Filho recebe direção normalizada ao destino somada ao vetor de movimento | ⛔ Sem hook server-authoritative de parametrização, físico e replay |
| **Hitbox / área** | Impacto `inflate 2D` vs busca do ricochete `inflate 32D` são operações distintas | ⛔ Não confundir expansão da consulta com área de dano; tamanho do projétil não foi alterado |
| **Duração / cooldown** | Nenhum cooldown individual de ricochete identificado nos métodos selecionados; `dieIn=5` é do lifecycle da ação | ⚠️ Não concluir ausência de cooldown externo; lifetime pós-reload e cadence não homologados |
| **Custo / recursos** | Sea Staff usa a durabilidade normal do cast; enchanting tem custo de bigorna 4 | ⛔ Não cobrar nem devolver durabilidade/mana por alvo secundário sem owner e settlement certificados |
| **Mastery / proc** | Um cast gera um ou mais settlements pertencentes à mesma raiz | ⛔ Não emitir Mastery/XP por projétil secundário sem dedupe e causalidade comprovados |
| **Compatibilidade** | Exclusividade de dados com Triple Splash; Enveloping Bubble é efeito visual/status separado | ⛔ Sem contornar exclusividade ou replicar efeitos sob modded stacks |

Black Arcana mantém seu runtime mágico próprio e **não** assume o settlement nativo do Sea Staff. RPG Skill Tree é apenas sibling/provider de progressão, perks, atributos e Mastery via boundary real. Se uma perk exigir um ponto mutador seguro para modificar range/alvo/velocidade, manter **fail-closed** até haver API/hook sustentado por evidência e testes no modpack.

## 7. Limites, testes e contabilização

**Comprovado:** identidade e JSON do JAR 1.0.10, exclusividade declarada, bytes de duas classes e SHA-256, três métodos com descritores, hashes JVM, offsets e janelas delimitadas, testes de parser/fail-closed e reconciliação com ação Sea Staff já certificada.

**Ainda não comprovado:** grafo de controle total; taxas efetivas de acerto; danos aceitos, número real de hits; spawn aceito; persistência de owner/alvo no reload; concorrência de múltiplos hits; acesso servidor/cliente sob todos os eventos; proteção PvP/claims; datapacks efetivos; aplicabilidade de mixins/hook externo; QA física de combate.

**Estados:** `VERIFIED_EXACT_BINARY_SELECTED_WINDOWS` para os fatos estáticos; `NOT_VERIFIED` para hook mutador; `NOT_TESTED` para QA em jogo; `NOT_CERTIFIED` para homologação integral de perk; `NO_MUTATION`.

Para eventual homologação, executar cenário real em servidor + cliente: cast com/sem Bouncing Bolt, Triple Splash em stack convencional e modificado, alvo único e múltiplo, tipos aliados/resistentes, hits negados, impacto em bloco/entidade, valores de ricochete sob ameaça, persistência/reload, chunks, owner desconectado, proteção PvP, custo/durabilidade e duplicação de Mastery. Repetir com outros mods que interceptam projéteis.

**Contabilidade desta ficha:** **+1 ficha individual parcial de encantamento**, **+0 contratos estáticos certificados**, **+0 raízes mágicas**, **+0 providers encerrados**. O próximo recurso alfabético a abordar é `alexscaves:bouncy_ball`.
