# Wind's Spellbooks — catálogo canônico

## Evidência estrutural dos efeitos nativos — 24/10/2026

[Wind CI #40136512061](https://github.com/Gustavaopere/Black-Arcana/actions/runs/40136512061) inspecionou as 64 classes da versão `wind_spellbooks-1.0.5.jar` (SHA-1 `8744886899bc245ae147a44baa2b183689cec7da`) e reportou **9 classes candidatas** por nome/referência de registry (não nove novos spells). Dentre elas, foram localizadas classes compiladas `net.raptorzizi.wind_spellbooks.effect.TailwindEffect` e `...AeropicEffect`.

**TailwindEffect:** métodos `applyEffectTick` (movimento/delta e escrita em `fallDistance`), `onEffectStarted` (atributo `JUMP_STRENGTH` e operação `ADD_MULTIPLIED_TOTAL`), `onEffectRemoved` (referências a `JUMP_STRENGTH` e `MOVEMENT_SPEED`, `removeModifier`). **AeropicEffect:** métodos `applyEffectTick`, `onEffectAdded`, `onEffectRemoved` referenciam `AbstractSpell.getRecastCount`, componentes de `PlayerRecasts` e cleanup, além de símbolos de dano/queda.

**Ponto crítico de interoperabilidade:** o `AeropicEffect` referencia a assinatura de **classe-base** `AbstractSpell.getRecastCount`, não diretamente `AeropicSpell.getRecastCount`, o que explica a limitação da busca de `invoke*` específica do PR #886. Isso ainda não comprova dispatch efetivo ou argumento aplicado. Os getters de percentual do Tailwind continuam sem chamadas qualificadas externas nesta release, mas há lógica de movimento/atributo no efeito; **não** classificá-los como puramente visuais.

Consulte os dossiês [Tailwind](wind/tailwind.md), [Aeropic](wind/aeropic.md) e [gate de evidência](../../../../docs/qa/winds-105-effect-boundary-evidence.md). Nenhuma fórmula de modificador, regra de recast, retorno do cast ou hook mutador é homologada. **7/7 spells** e **9/9 getters selecionados** sem incremento; `Stage 06.05` 🟡 e QA físico do Stage 09 pendente.

## Scanner de consumidores entre 64 classes — 24/10/2026

**✅ Evidência binária exata:** [Wind CI #40135302517](https://github.com/Gustavaopere/Black-Arcana/actions/runs/40135302517), JAR `wind_spellbooks-1.0.5.jar` com SHA-1 `8744886899bc245ae147a44baa2b183689cec7da`. A análise examinou **64 classes** no namespace do próprio provider e encontrou **16 instruções `invoke*` diretas** relativas aos nove getters escalares previamente selecionados. **Zero das 16** tem origem em outra classe Wind's; as 16 estão nas classes declarantes.

**⚠️ Restrição importante:** isso não torna Tailwind nem Aeropic puramente visuais, não certifica caminhos herdados, classes de host Iron's/IronSable, eventos, calls indiretas/reflexão/Mixin, nem fluxo `getter → argumento do setter → gameplay`. Ver [gate técnico com escopo explícito](../../../../docs/qa/winds-105-cross-class-callers-gate.md). Estado de perks mutadoras **⛔ `SEM_HOOK_SEGURO`**; 7/7 magias documentadas, nove getters selecionados, zero novas identidades e Stages inalterados.

## Chamadores diretos JVM para getters selecionados — 24/10/2026

**✅ 9/9** getters escalares já selecionados tiveram seus chamadores diretos identificados **dentro das classes dos próprios spells** na versão 1.0.5 (SHA-1 `8744886899bc245ae147a44baa2b183689cec7da`), incluindo 6/7 classes: [auditoria de arestas](../../../../docs/qa/winds-105-getter-consumer-evidence.md) e [workflow binário #40130495377](https://github.com/Gustavaopere/Black-Arcana/actions/runs/40130495377). Isso complementa **7/7 fichas de magias**, não cria nove magias nem mede todos os getters possíveis.

**Distinção relevante para perks:** `getRecastCount` de Aeropic e os dois percentuais de Tailwind são invocados diretamente por `getUniqueInfo`, mas não pelo `onCast` da classe examinada. Outros efeitos/classes/host podem consumi-los: não declarar cosmético nem sem efeito gameplay. Os seis getters restantes do conjunto são chamados diretamente por `onCast`; `getJumpStrength` de Wind Jump também por `getJumpHeight`. Todos os fluxos getter → setter, duração efetiva, raio real e mutations de perks **continuam `NOT_PROVEN` / `SEM_HOOK_SEGURO`**. A co-presença de chamada e setter no mesmo método não comprova argumento nem destinatário.

## Getters escalares com AST aritmética exata — 24/10/2026

**9/9 getters selecionados** com pilha JVM integral interpretada: quatro do [PR #882](../../../../docs/qa/winds-105-spell-parameter-gate.md) e cinco da [auditoria de mobilidade](../../../../docs/qa/winds-105-mobility-getters-gate.md), ver CI [#40126898432](https://github.com/Gustavaopere/Black-Arcana/actions/runs/40126898432). Esta contagem corresponde exclusivamente aos **nove métodos de retorno escalar selecionados**; não implica 9/9 spells, que são **7/7** identidades, nem prova de completude de todas as fórmulas do provider.

Novos métodos do recorte: Almighty Push `getRange`, Iron Slash `getDistance`, Tailwind `getPercentAirSpeed`/`getPercentJump` e Wind Jump `getJumpStrength`. Cada fórmula, unidades não provadas e limites ficam nas fichas `wind/*.md`. O scanner verifica o JAR 1.0.5 por SHA-1 exato; [contrato de regressão](../../../../docs/qa/winds-105-mobility-getters-gate.md) rejeita divergência de constantes, fluxo numérico e identidade binária.

**Estado técnico:** ⚠️ 9/9 getters selecionados com expressão binária, ⛔ hooks mutadores sem contrato, ⚠️ targeting/dano/consumidores/configuração/Survival pendentes. A autoridade de Iron's, Wind's, Black Arcana e RPG Skill Tree permanece separada. Nenhuma perk ou comportamento de gameplay foi alterado.

## Verificação de consumidores compilados — 24/10/2026

**7/7 fichas** agora incluem assinaturas e arestas de chamadas obtidas por `javap` Java 21 sobre o JAR 1.0.5 com SHA-1 físico/publicador idêntico. [CI exato #40118955224](https://github.com/Gustavaopere/Black-Arcana/actions/runs/40118955224): inspeção das sete classes e testes sintéticos `SUCCESS`. Os métodos incluem superfícies de `getDamage`, `getRadius`, `getRange`, `getRecastCount`, entidades e projectiles conforme a classe, **sem atribuir valores, alvos, fórmula ou hooks a partir do nome**. Consulte as sete fichas em `wind/`.

**Percentuais não somáveis:** identidade binária **7/7**; fichas com consumidores simbólicos **7/7**; fórmulas completas, parâmetros configurados, hook mutador, client/Survival e settled gameplay **⚠️/⛔ não certificados**. **+0 magias**, Stage 06.05 🟡 e Stage 09 ⚠️. Usar os resultados como insumo para futura análise de operandos e contrato provider-native; não instalar adapter com base em `javap` isolado.


## Estado

- Mod ID: `wind_spellbooks`
- JAR instalado: `wind_spellbooks-1.0.5.jar`
- Versão instalada: `1.0.5`
- Runtime alvo: NeoForge 1.21.1
- Provider base: Iron's Spells 'n Spellbooks
- Escola própria: Wind
- Release exata: CurseForge file `8485822`, publicada em 2026-07-22
- Catálogo: **7/7 spells ativos documentados**
- Estado de evidência: `COUNTED_EXACT` para sete identidades binárias estáticas; mecânicas, config e Survival ⚠️

A página oficial da release 1.0.5 descreve o addon como uma escola completa de Wind com **sete spells upgradáveis**, armor de mago, staff, spellbook, Windmill e Aeromancer. Os logs reais do pack confirmam exatamente sete registrations `wind_spellbooks:*` e expõem as classes carregadas pelo runtime.

## Prova binária exata

[Auditoria do JAR 1.0.5](EXACT-BINARY-SPELLS-1.0.5.md) ([run #38312284152](https://github.com/Gustavaopere/Black-Arcana/actions/runs/38312284152)) confirmou hash físico/publicador, sete registros estáticos e bootstrap. `ACROBATICS_SPELL` corresponde ao ID `aeropic`, não a um oitavo spell. Campanha **6/39 exatos / 33/39 pendentes**, **+0** novos; mínimos **1851/1849**. QA real não realizado.

## Inventário 7/7

1. [Wind Jump](wind/wind-jump.md) — `wind_spellbooks:wind_jump`
2. [Tornado](wind/tornado.md) — `wind_spellbooks:tornado`
3. [Iron Slash](wind/iron-slash.md) — `wind_spellbooks:iron_slash`
4. [Aeropic](wind/aeropic.md) — `wind_spellbooks:aeropic`
5. [Almighty Push](wind/almighty-push.md) — `wind_spellbooks:almighty_push`
6. [Wind Blade](wind/wind-blade.md) — `wind_spellbooks:wind_blade`
7. [Tailwind](wind/tailwind.md) — `wind_spellbooks:tailwind`

## Evidência runtime do pack

O analisador ASM carregado no próprio modpack observou as classes e fingerprints abaixo:

| Spell | Classe runtime | Fingerprint observado |
|---|---|---|
| Wind Jump | `WindJumpSpell` | entity + `ImpulseCastData` + projectile + effect |
| Tornado | `TornadoSpell` | entity + projectile + raycast |
| Iron Slash | `IronSlashSpell` | potentiation + entity + impulse + teleport + effect |
| Aeropic | `AeropicSpell` | recasts + impulse + effect |
| Almighty Push | `AlmightyPushSpell` | entity + effect |
| Wind Blade | `WindBladeSpell` | shoot + entity + projectile |
| Tailwind | `TailwindSpell` | effect |

Esse fingerprint prova o uso estrutural desses mechanisms, mas **não prova sozinho valores, hit rules, duração, alcance ou fórmulas**. Esses campos permanecem `NÃO VERIFICADO` até extração do JAR/source exato.

## Progressão / obtenção

A release oficial confirma o ecossistema próprio de Wind, incluindo Windmill, Aeromancer, staff e spellbook. O changelog histórico 1.0.1 registra Aeromancer loot table, Wind staff recipe, Book of Tempests advancement e correção de fall damage de Tailwind.

A rota exata de obtenção de cada um dos sete scrolls, pesos de loot, crafting, níveis máximos e raridades não foi provada pelo artefato/source nesta auditoria e fica `NÃO VERIFICADO`.

## Deduplicação

Os sete contracts ocupam, no mínimo, estes espaços mecânicos comprovados:

- mobilidade por impulso com projectile/effect (`Wind Jump`);
- tornado targetado/raycast com entity/projectile (`Tornado`);
- ataque/mobilidade com potentiation + teleport/impulse (`Iron Slash`);
- mobilidade recast-based (`Aeropic`);
- push-themed spell com entity/effect (`Almighty Push` — settlement exato pendente);
- projectile Wind disparado (`Wind Blade`);
- buff/effect Wind com interação histórica com fall damage (`Tailwind`).

IronSable registra seus próprios `maelstrom`, `tempests_grasp` e `downburst` e apenas os classifica como Wind quando este addon está instalado. Esses três **não pertencem** ao inventário 7/7 de Wind's Spellbooks.

## Regra de fail-closed

A prova binária de registro não autoriza inventar mana, cooldown, dano, range, recast count, friendly-fire, PvP ou APIs para esses spells. Integrações futuras devem usar IDs/runtime hooks comprovados e manter o provider como authority do efeito.

Ver [TECHNICAL-AUDIT.md](TECHNICAL-AUDIT.md).

## Hierarquia/registry exatos de Aeropic e Tailwind — 24/10/2026

Na execução [Wind #40139355055](https://github.com/Gustavaopere/Black-Arcana/actions/runs/40139355055), cinco classes escolhidas foram inspecionadas em suas assinaturas e referências JVM dentro das **64 classes** do JAR 1.0.5 SHA-1 `8744886899bc245ae147a44baa2b183689cec7da`.

`AeropicSpell` e `TailwindSpell` declaram **`extends AbstractSpell`**; `AeropicEffect` e `TailwindEffect` declaram **`extends MagicMobEffect implements ISyncedMobEffect`**. A ABI `AeropicSpell.getRecastCount(int, LivingEntity)` corresponde ao descritor que `AeropicEffect` referencia em `AbstractSpell`, mas **receiver e despacho virtual não foram provados**.

`ModMobEffectRegistry.static {}` contém strings `aeropic`/`tailwind`, fields `ACROBATICS`/`TAILWIND`, dois sites `invokedynamic` e chamada a `DeferredRegister.register(String, Supplier)`. Os métodos auxiliares `lambda$static$0` e `lambda$static$1` contêm construções de `AeropicEffect` e `TailwindEffect`, respectivamente. **Não é prova causal ainda de qual supplier alimenta cada campo**: falta inspeção da tabela `BootstrapMethods` e rastreio da pilha.

Gate detalhado: [auditoria de registry e dispatch](../../../../docs/qa/winds-105-registry-dispatch-gate.md). Nenhum spell novo, nenhum hook homologado, nenhuma alteração de Stages ou de runtime; **7/7** identidades, **9/9** getters selecionados.

## Associação compilada dos efeitos `ACROBATICS` e `TAILWIND` — 24/10/2026

Nova prova binária [Wind CI #40143051496](https://github.com/Gustavaopere/Black-Arcana/actions/runs/40143051496) (JAR Wind's 1.0.5 SHA-1 `8744886899bc245ae147a44baa2b183689cec7da`): os dois `DeferredHolder` foram associados a `Supplier` específicos por análise conservadora de `ModMobEffectRegistry.<clinit>` + `BootstrapMethods`.

- `ACROBATICS`: chave `aeropic` → site `#0` → factory `lambda$static$0` → classe `AeropicEffect`.
- `TAILWIND`: chave `tailwind` → site `#1` → factory `lambda$static$1` → classe `TailwindEffect`.

**✅ Ligação compilada**, antes marcada `NOT_PROVEN` nas notas antigas. **⚠️ Instanciação em runtime, cliente/modpack físico e magnitudes seguem `NOT_TESTED`**; `AbstractSpell.getRecastCount` não teve despacho dinâmico certificado e hooks mutadores continuam **⛔ `SEM_HOOK_SEGURO`**. Ver [gate com evidência exata](../../../../docs/qa/winds-105-bootstrap-registry-gate.md). O total de magias Wind's permanece **7/7**, sem nova habilidade ou avanço de Stage.

## Opcodes exatos de recast do Aeropic — 24/10/2026

Na auditoria [Wind CI #40144903731](https://github.com/Gustavaopere/Black-Arcana/actions/runs/40144903731), o `AeropicEffect` da release 1.0.5 tem **duas** invocações explícitas `invokevirtual` do owner simbólico `AbstractSpell.getRecastCount(int, LivingEntity)`: uma em `applyEffectTick`, outra em `onEffectAdded`. O primeiro método possui chamadas de `PlayerRecasts` e `RecastInstance`, mas sem prova de fluxo de operandos ou execução.

**ABI de herança ✅; opcode estático ✅; receptor/override dinamicamente escolhido ⚠️ não provados.** A ficha [Aeropic](wind/aeropic.md) e o [gate de QA](../../../../docs/qa/winds-105-aeropic-recast-invoke-gate.md) preservam `SEM_HOOK_SEGURO`. Não houve novas magias, novos perks ou alteração de estágio.

## Host Iron’s 3.16.3 — ABI publicada compatível com Aeropic — 24/10/2026

Na execução [host ABI CI #40146984360](https://github.com/Gustavaopere/Black-Arcana/actions/runs/40146984360), a distribuição oficial Modrinth `irons_spellbooks-1.21.1-3.16.3.jar` (SHA-1 `e8832385c01db56b9fcb19c48fcedc76a3a70d92`, SHA-512 no [gate](../../../../docs/qa/irons-3163-aeropic-recast-host-gate.md)) confirmou **5/5 descritores JVM de recast** referenciados pelo `AeropicEffect` do Wind's 1.0.5, incluindo `AbstractSpell.getRecastCount` e chamadas `PlayerRecasts`/`RecastInstance`.

**⚠️ Distinção de identidade:** o artefato oficial auditado mede 13.890.045 bytes; outra listagem pública da mesma release informa 13.890.046. Não certificar coincidência com o JAR **instalado** sem o checksum do arquivo físico. ABI publicada ✅, receiver/dispatch e runtime ⚠️ `NOT_PROVEN`, perks mutadoras ⛔ `SEM_HOOK_SEGURO`. Não altera o número 7/7 de magias catalogadas, hooks ou Stages.

## Aeropic: contexto do receptor e consumidor de recast — 24/10/2026

Nova auditoria [Wind #40153009971](https://github.com/Gustavaopere/Black-Arcana/actions/runs/40153009971) (SHA-1 Wind's 1.0.5 congelado) encontrou os símbolos compilados `ModSpellRegistry.ACROBATICS_SPELL`, `Supplier.get()` e `AbstractSpell` próximos ao `invokevirtual getRecastCount` de `onEffectAdded`. Em `applyEffectTick`, encontrou referências a `MagicData.getPlayerRecasts` e `hasRecastForSpell` antes, e `RecastInstance.<init>`/`PlayerRecasts.addRecast` depois da chamada. Isso **não prova** origem do receptor ou consumo do retorno.

O [gate de operandos](../../../../docs/qa/winds-105-aeropic-recast-operand-provenance.md) e a [ficha Aeropic](wind/aeropic.md) preservam `NOT_TRACED`/`SEM_HOOK_SEGURO`. Apenas a vizinhança de símbolos foi fixada por regressão no JAR exato, sem novos spells, hooks, mudanças de Stages ou aceitação física.

## Aeropic — limite da prova do receptor JVM — 24/10/2026

A [auditoria Wind #40156532292](https://github.com/Gustavaopere/Black-Arcana/actions/runs/40156532292) examinou duas chamadas `AbstractSpell.getRecastCount` no JAR 1.0.5. A sequência de cinco produtores não corresponde a nenhum dos dois métodos; o modelo de bloco único foi bloqueado por fluxo de controle em `applyEffectTick` e não estabeleceu ligação do Supplier ao receiver em `onEffectAdded`. **Não se comprovou o receptor; isso não refuta a existência de recasts em gameplay.**

Estado: origem, despacho e destino do retorno ⚠️ `NOT_PROVEN`; perks mutadoras ⛔ `SEM_HOOK_SEGURO`. [Evidência e limitações](../../../../docs/qa/winds-105-aeropic-direct-supplier-slice-gate.md). Cobertura Wind's 7/7 e Stages inalterados.
