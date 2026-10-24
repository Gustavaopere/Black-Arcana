# Wind's Spellbooks — catálogo canônico

## Chamadores diretos JVM para getters selecionados — 24/10/2026

**✅ 9/9** getters escalares já selecionados tiveram seus chamadores diretos identificados **dentro das classes dos próprios spells** na versão 1.0.5 (SHA-1 `8744886899bc245ae147a44baa2b183689cec7da`), incluindo 6/7 classes: [auditoria de arestas](../../../../docs/qa/winds-105-getter-consumer-evidence.md) e [workflow binário #40130495377](https://github.com/Gustavaopere/Black-Arcana/actions/runs/40130495377). Isso complementa **7/7 fichas de magias**, não cria nove magias nem mede todos os getters possíveis.

**Distinção relevante para perks:** `getRecastCount` de Aeropic e os dois percentuais de Tailwind são invocados diretamente por `getUniqueInfo`, mas não pelo `onCast` da classe examinada. Outros efeitos/classes/host podem consumi-los: não declarar cosmético nem sem efeito gameplay. Cinco outros getters do conjunto são chamados diretamente por `onCast`; `getJumpStrength` de Wind Jump também por `getJumpHeight`. Todos os fluxos getter → setter, duração efetiva, raio real e mutations de perks **continuam `NOT_PROVEN` / `SEM_HOOK_SEGURO`**. A co-presença de chamada e setter no mesmo método não comprova argumento nem destinatário.

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
