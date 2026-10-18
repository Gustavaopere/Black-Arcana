# Vanilla Backport 1.1.7.10 — host físico dos atributos de Slime Aspect e Slime Boots

**18/10/2026 · ✅ `EXACT_PUBLISHER_BYTECODE_HOST_OPERANDS_AND_CALLSITES` (atributos + três classfiles) · ⚠️ mixins aplicados/atributos resolvidos/cliente/modpack · ⛔ perk adapter sem contrato.**

## Identidade física de referência e fontes

- **Modlist certificada:** `VanillaBackport-neoforge-1.21.1-1.1.7.10.jar` (#560), Minecraft 1.21.1, NeoForge 21.1.250 (#001). Iron's Spellbooks `3.16.3` (#342), Backported Spellbooks `0.1.2` (#063).
- **Publicador:** [CurseForge 417430 / arquivo 8229724](https://www.curseforge.com/minecraft/mc-mods/vanillabackport/files/8229724), release NeoForge 1.21.1 de **11/06/2026**. Não substituir por Vanilla Backport 1.2 ou outro loader, mesmo que exista lançamento posterior.
- **JAR official baixado no runner:** **54.902.084 bytes**, SHA-1 `eb30efe569cbd5186abf9e5d1e64d4a84895b346`, SHA-256 `ecd807ac358e243ede17819455788c7b7a0ce5e0af4aecee82c1c62c586d818d`. Os hashes são **do publisher baixado**: a modlist contém filename/versão, mas nenhuma nova medição SHA física deste JAR foi realizada no perfil local. Não alegar igualdade de hashes com uma instalação não medida.
- **Gate Java 21:** [workflow #39156441117](https://github.com/Gustavaopere/Black-Arcana/actions/runs/39156441117), **SUCCESS**, 10/10 testes sintéticos, marcador `PASS_VANILLABACKPORT_11710_BOUNDED_MOBILITY_BYTECODE`, `deviations=[]`. [JSON #12147207357](https://github.com/Gustavaopere/Black-Arcana/actions/runs/39156441117/artifacts/12147207357), [script de verificação fail-closed](../../../../docs/qa/vanillabackport_11710_mobility_bytecode.py), [workflow](../../../../.github/workflows/vanillabackport-11710-mobility-bytecode.yml). A rodada exploratória [#39155981925](https://github.com/Gustavaopere/Black-Arcana/actions/runs/39155981925) primeiro estabeleceu hash/tamanho e existência das classes; as rodadas RED intermediárias identificaram erros na seleção dos métodos `javap` do verificador, **não** bugs do provider.
- **Source ceiling oficial:** [`ItsBlackGear/VanillaBackport@adb579d205a05bcc7d1f34ce402cea6f1335a760`](https://github.com/ItsBlackGear/VanillaBackport/tree/adb579d205a05bcc7d1f34ce402cea6f1335a760) (commit denominado `1.1.7.10`, de 11/06/2026). Existe alteração posterior no mesmo dia, `0cf196650b65dada85339f1ebe5f2e1ee9bdaf90`; portanto não há prova de que o JAR tenha sido gerado **exatamente** daquele tree/commit. A evidência binária abaixo é do JAR, independente da suposição source↔build.

## Registro compilado dos atributos

A classe exata `com.blackgear.vanillabackport.common.registries.ModAttributes` registra, via `CoreRegistry.holder`, três atributos no namespace **`minecraft`**. Seus suppliers de `RangedAttribute` contêm os seguintes argumentos para `(String, double default, double min, double max)` e chamada `setSyncable(true)`:

| Registro | Default | Limites declarados | Fonte pinada |
|---|---:|---:|---|
| `minecraft:bounciness` | 0.0 | [0.0, **1.0**] | [`ModAttributes.java`](https://github.com/ItsBlackGear/VanillaBackport/blob/adb579d205a05bcc7d1f34ce402cea6f1335a760/common/src/main/java/com/blackgear/vanillabackport/common/registries/ModAttributes.java) |
| `minecraft:air_drag_modifier` | 1.0 | [0.0, 2048.0] | mesmo arquivo |
| `minecraft:friction_modifier` | 1.0 | [0.0, 2048.0] | mesmo arquivo |

**Ponto de risco:** `SlimeBootsArmorItem` possui `+2.5 ADD_VALUE` em `BOUNCINESS`, enquanto `SlimeAspect` declara `+0.5 ADD_VALUE`. O **teto de registro de 1.0 é compilado no host**, mas esta prova **não executou** `AttributeInstance` e `RangedAttribute.sanitizeValue` nem mediu o valor após aplicar os dois conjuntos. A hipótese de saturação acima de 1.0 depende da semântica de resolução do host e precisa de teste conectado. Não interpretar 2.5 como restituição final.

## Consumidores de movimento compilados

- [`EntityMixin.java`](https://github.com/ItsBlackGear/VanillaBackport/blob/adb579d205a05bcc7d1f34ce402cea6f1335a760/common/src/main/java/com/blackgear/vanillabackport/core/mixin/common/entities/EntityMixin.java): `vb$earlyCapture` lê `BOUNCINESS` antes das colisões; `vb$RestituteMovementAfterCollisions` usa `LivingEntity.isSuppressingBounce`, valor `BOUNCINESS`, consulta `vb$getAirDrag`, `Mth.lerp` e `setDeltaMovement`. Possui referência a `GameEvent.HIT_GROUND`, mas **nenhum movimento observado**.
- `EntityMixin.vb$getAirDrag` consulta `AIR_DRAG_MODIFIER` e em caminho distinto `FRICTION_MODIFIER`, inclusive constantes de base `0.98f` e `0.91f` e helper de atrito. Não extrapolar um único valor de velocidade no ar para todas as modalidades/entidades.
- [`LivingEntityMixin.java`](https://github.com/ItsBlackGear/VanillaBackport/blob/adb579d205a05bcc7d1f34ce402cea6f1335a760/common/src/main/java/com/blackgear/vanillabackport/core/mixin/common/entities/LivingEntityMixin.java): `createLivingAttributes` acrescenta três `AttributeSupplier.Builder.add` na ordem Air Drag, Bounciness, Friction; `vb$handleMovementFriction` consulta `FRICTION_MODIFIER` e `AttributeInstance.getValue`; `vb$applyAirDrag` lê `FRICTION_MODIFIER`, `AIR_DRAG_MODIFIER`, constantes `0.91f` e `0.98f` e usa `vb$computeModifiedFriction`.
- `LivingEntityMixin.vb$computeModifiedFriction` contém a sequência aritmética binária equivalente, no recorte de instruções `float`, a **`Mth.clamp(1 − (1 − friction) × modifier, 0, 1)`**. Este é o **coeficiente de atrito calculado**, não o atributo `FRICTION_MODIFIER` em si. Não confundir clamp do coeficiente com o teto do atributo nem com fricção/arrasto resultantes em todos os ambientes.

A instrumentação e a integração mixin ainda precisam de verificação no host real; esta prova só confirma **classfiles compilados e seus callsites/operandos**, não a aplicação do Mixin config e incompatibilidades com outros mods.

## Matriz de composição — sem números finais inventados

| Conjunto ativado | Bounciness declarado | Jump Strength declarado | Friction declarado | Air Drag declarado | QA final |
|---|---|---|---|---|---|
| Sem magia, sem botas | Default host 0.0 | baseline Vanilla | default host 1.0 | default host 1.0 | ⚠️ não medido |
| Apenas `slime_aspect` | `+0.5 ADD_VALUE` | `+0.15 ADD_MULTIPLIED_TOTAL` | sem modifier da magia | `−0.10 ADD_MULTIPLIED_TOTAL` | ⚠️ não medido |
| Apenas `slime_boots` | `+2.5 ADD_VALUE` | `+0.10 ADD_MULTIPLIED_BASE` | `+0.30 ADD_MULTIPLIED_BASE` | `−0.50 ADD_MULTIPLIED_BASE` | ⚠️ não medido |
| Ambos | Ambos os conjuntos | Modos `ADD_MULTIPLIED_BASE` e `ADD_MULTIPLIED_TOTAL` diferentes | Somente boots | Modos base × total distintos | ⚠️ não medido |

As regras de scaling do `MobEffect` com amplificador e as operações finais de `AttributeInstance` **não foram comprovadas por teste combinado**. Um perk que altere `spellPower` pode afetar duração de `slime_aspect`, mas não possui neste escopo um hook seguro documentado para alterar coeficientes, targeting, cooldown ou essa cadeia do VanillaBackport.

## QA, autoridade e critérios de promoção

- **Prioridade QA física:** 4 combinações (nenhum, magia, botas, ambos) × níveis da magia; verificar `/attribute` ou leitura servidor dos três atributos, duração pós-cast, consumo/cooldown, salto, desaceleração, colisão, bounce, suppression e dano de queda com/sem botas, relog, respawn e equip/unequip; repetir com mods de movimento/armaduras ativos no modpack.
- **Exceções:** `LivingFallEvent` é cancelado por `ServerEvents.onFallEvent` **quando o jogador usa Slime Boots**, conforme [prova binária do item](EXACT-BINARY-SLIME-BOOTS-FALL-0.1.2.md). Isso não é o mesmo que elasticidade do feitiço e o gate atual não executou evento.
- **Authority:** VanillaBackport/Minecraft sobre definição dos três atributos e movimento; Backported Spellbooks sobre `slime_aspect`, Slime Boots e `onFallEvent`; Iron's sobre cast, mana e cooldown; RPG Skill Tree apenas progressão/perks via boundary comprovada; Black Arcana apenas runtime próprio. Nunca aplicar segundo dano, buff, XP/Mastery, cancelamento de queda ou reembolso de recurso sem contrato.
- **Status:** ✅ registros/callsites compilados do JAR **publisher**; ⚠️ hash físico do host, instalação do Mixin, valores resolvidos, client/server, stacking e gameplay; ⛔ mudanças por perk sem hook/API verificadas. Não é aprovação Stage 09.

**Contagem conservadora:** Backported Spellbooks permanece **6/6** feitiços `COUNTED_EXACT`, **6/6** fichas e **6/6** com ao menos um método compilado delimitado. Os atributos e o equipamento não adicionam mágicas: **+0** raízes / **+0** adapters. Global mantém piso documental **1.857 objetos semânticos / 1.855 estritos** com denominador aberto (**—%**). Stage 06.05 🟡; Stage 09 físico PENDING; PR #825 segue draft, sem merge.
