# Vanilla Backport 1.1.7.10 — vínculo NeoForge/mixins de atributos de movimento no JAR

**18/10/2026 · ✅ `EXACT_PUBLISHER_PACKAGED_CONFIG_AND_CLASS_PRESENCE` · ⚠️ transformação efetiva, host instalado, gameplay/integração · ⛔ hook de perk sem contrato.**

## Artefato e limites

- **Publisher confirmado:** Vanilla Backport 1.1.7.10 para NeoForge Minecraft 1.21.1, CurseForge projeto `417430`, arquivo oficial [#8229724](https://www.curseforge.com/minecraft/mc-mods/vanillabackport/files/8229724), `VanillaBackport-neoforge-1.21.1-1.1.7.10.jar`.
- **Tamanho/hash medidos no GitHub Actions:** **54.902.084 bytes**, SHA-1 `eb30efe569cbd5186abf9e5d1e64d4a84895b346`, SHA-256 `ecd807ac358e243ede17819455788c7b7a0ce5e0af4aecee82c1c62c586d818d`.
- **Evidência objetiva:** [#39164766070](https://github.com/Gustavaopere/Black-Arcana/actions/runs/39164766070) **SUCCESS**, **12/12 autotestes de manifesto**, `PASS_VANILLABACKPORT_11710_MIXIN_MANIFEST_BOUNDARY` com `deviations=[]`; no mesmo JAR, **10/10 testes de atributos e consumidores** `PASS_VANILLABACKPORT_11710_BOUNDED_MOBILITY_BYTECODE`. [JSON com duas evidências #12150455560](https://github.com/Gustavaopere/Black-Arcana/actions/runs/39164766070/artifacts/12150455560); [verificador de manifesto](../../../../docs/qa/vanillabackport_11710_mixin_manifest.py), [verificador de movimento](../../../../docs/qa/vanillabackport_11710_mobility_bytecode.py) e [workflow](../../../../.github/workflows/vanillabackport-11710-mobility-bytecode.yml). Nenhum JAR de terceiros arquivado.
- **Evidência de fonte complementar (não prova de build source↔JAR):** [`vanillabackport.mixins.json`](https://github.com/ItsBlackGear/VanillaBackport/blob/adb579d205a05bcc7d1f34ce402cea6f1335a760/common/src/main/resources/vanillabackport.mixins.json) e [`META-INF/neoforge.mods.toml`](https://github.com/ItsBlackGear/VanillaBackport/blob/adb579d205a05bcc7d1f34ce402cea6f1335a760/neoforge/src/main/resources/META-INF/neoforge.mods.toml), commit oficial `adb579d205a05bcc7d1f34ce402cea6f1335a760`, marcado como `1.1.7.10`.
- **Autoridade física:** a modlist identifica filename/versão, **não fornece SHA do JAR local VanillaBackport**. Esta prova testa o publisher *da mesma versão nominal*, ainda não o binário instalado no computador.

## Resultado posterior: alvos de `@Mixin` e handlers compilados (18/10/2026)

✅ [CI #39169078531](https://github.com/Gustavaopere/Black-Arcana/actions/runs/39169078531) **SUCCESS** (12/12 regressões de seletores, [JSON #12151413141](https://github.com/Gustavaopere/Black-Arcana/actions/runs/39169078531/artifacts/12151413141)) prova [sete handlers compilados e seus targets/`@At`/`ordinal`/`index`](EXACT-BINARY-VANILLABACKPORT-MIXIN-INJECTION-SELECTORS-1.1.7.10.md) por `RuntimeVisibleAnnotations` de método, além dos `@Mixin` por `RuntimeInvisibleAnnotations` de classe. Isso amplia a prova de **manifesto declarado** para **selectors compiled**, mas **não** valida aplicação de mixin em jogo, ordem de outros mixins, players, client/dedicated server ou hook de perks.

## Ligação no JAR de publicação

O verificador leu o conteúdo do ZIP e aprovou os seguintes fatos **no artefato exato**:

| Camada | Entrada de arquivo / valor | Estado |
|---|---|---|
| Loader | `META-INF/neoforge.mods.toml`, `modLoader=javafml` | ✅ pacote |
| Mod ID | `vanillabackport` | ✅ metadata |
| Versão da distribuição no TOML | `1.1.7.10` | ✅ metadata |
| Entrada NeoForge mixin | `[[mixins]] config="vanillabackport.mixins.json"` | ✅ pacote |
| Arquivo Mixin | `vanillabackport.mixins.json` | ✅ pacote |
| Mixin obrigatório | `required=true` | ✅ declaração |
| Linguagem | `compatibilityLevel=JAVA_21` | ✅ declaração |
| Mixin injectors | `defaultRequire=1` | ✅ declaração |

O arquivo de mixins, cujo package compilado é `com.blackgear.vanillabackport.core.mixin`, inclui **uma vez cada** na lista comum `mixins` (e não em `client`):

1. `common.entities.EntityMixin` → alvo nominal `net.minecraft.world.entity.Entity` no [source pin](https://github.com/ItsBlackGear/VanillaBackport/blob/adb579d205a05bcc7d1f34ce402cea6f1335a760/common/src/main/java/com/blackgear/vanillabackport/core/mixin/common/entities/EntityMixin.java);
2. `common.entities.LivingEntityMixin` → `net.minecraft.world.entity.LivingEntity` no [source pin](https://github.com/ItsBlackGear/VanillaBackport/blob/adb579d205a05bcc7d1f34ce402cea6f1335a760/common/src/main/java/com/blackgear/vanillabackport/core/mixin/common/entities/LivingEntityMixin.java);
3. `common.attributes.RangedAttributeMixin` → `net.minecraft.world.entity.ai.attributes.RangedAttribute` no [source pin](https://github.com/ItsBlackGear/VanillaBackport/blob/adb579d205a05bcc7d1f34ce402cea6f1335a760/common/src/main/java/com/blackgear/vanillabackport/core/mixin/common/attributes/RangedAttributeMixin.java).

As três classes `.class` correspondentes existem no ZIP. **A terceira é um mixin de `RangedAttribute` com código específico de knockback resistance na fonte pinada; sua presença não é prova de que ela implemente o teto de `BOUNCINESS`.** Os consumidores de bounce e drag localizam-se nas duas primeiras classes, auditadas separadamente. As classes foram compiladas; este gate **não analisou suas anotações de injeção nem executou Mixin**.

## Dependências do TOML físico de publicação

As três linhas abaixo foram confirmadas como **`type=required` e `side=BOTH`** e tiveram o `versionRange` verificado pelo gate, sem executar o loader:

| Dependência obrigatória | Version range do JAR | Snapshot modlist |
|---|---|---|
| `neoforge` | `[21.1,)` | `21.1.250`, linha #001 ✅ identidade |
| `minecraft` | `[1.21.1,)` | `1.21.1` ✅ plataforma-alvo |
| `platform` | `[1.3.3,)` | `Platform-neoforge-1.21.1-1.3.3.jar`, linha #445 ✅ identidade |

A correspondência de versão/faixa **não prova** que o modloader aplicou todos os mixins sem conflitos, nem certifica SHA local do Platform. A distinção entre **compatibilidade nominal declarada** e **teste carregado** é intencional.

## Por que isso importa aos perks de Slime Aspect e Slime Boots

- [`Slime Aspect`](EXACT-BINARY-SLIME-ASPECT-0.1.2.md) configura `BOUNCINESS +0.5 ADD_VALUE`, `JUMP_STRENGTH +0.15 ADD_MULTIPLIED_TOTAL` e `AIR_DRAG_MODIFIER -0.10 ADD_MULTIPLIED_TOTAL`.
- [`Slime Boots`](EXACT-BINARY-SLIME-BOOTS-FALL-0.1.2.md) configura quatro modifiers próprios: bounciness `+2.5 ADD_VALUE`, jump `+0.10 ADD_MULTIPLIED_BASE`, friction `+0.30 ADD_MULTIPLIED_BASE`, air drag `-0.50 ADD_MULTIPLIED_BASE`; sua proteção de queda tem outro handler.
- [`Vanilla Backport` runtime *declarado em classes compiladas*](EXACT-BINARY-VANILLABACKPORT-MOBILITY-HOST-1.1.7.10.md) estabelece `bounciness` com default 0, faixa [0,1], e usa `EntityMixin`/`LivingEntityMixin` para ler e processar atributos, incluindo `clamp(1−(1−friction)×modifier,0,1)`.

**NÃO CATALOGAR** cada modifier como novo feitiço, não assumir bounciness final 2.5 e não mapear campo de movimento para hook de escrita de perk sem evidência de API. A presença do mixin na lista comum não garante que ele tenha sido aplicado, que método alvo tenha aceitado injeção ou que o resultado do movimento seja o esperado.

## Aceitação física ainda necessária

Executar no modpack com **NeoForge 21.1.250 + Platform 1.3.3 + Vanilla Backport 1.1.7.10 + Backported Spellbooks 0.1.2 + Iron's 3.16.3**:

- Log de startup NeoForge/loader para presença dos mods, versão e eventuais falhas de mixin; dedicated server e cliente conectado.
- Verificar a transformação efetivamente aplicada dos mixins comuns; não inferir sucesso por ausência de stacktrace ou por JSON.
- Em jogador: sem magia/botas, apenas Slime Aspect, apenas Slime Boots, ambos; registrar atributos resolvidos, salto, colisão/bounce, drag, fricção, queda e dano.
- Config efetiva, amplificador, stacking, recast, relog e equipamento retirado/reativado; conflito com outros modificadores e variantes de movimento/flying.
- Se houver erro de registro, falha do host ou ausência de uma API/hook, **⛔ fail-closed** para adapter. Não acionar o runtime mágico do Black Arcana para reproduzir a física provider-owned.

**Status do catálogo:** Backported Spellbooks **✅ 6/6** identidades de magia e fichas, **⚠️ métodos auditados parcialmente** (ao menos um caminho por magia). A análise de host/equipamento é adicional, **+0 novas magias / +0 adapters**. Total global mantém piso anterior **1.857 objetos semânticos / 1.855 estritos**, universo total aberto (**—%**). **Stage 06.05 🟡 / Stage 09 ⚠️ físico pendente**, PR #825 draft; não autorizado merge ou promoção por este gate.
