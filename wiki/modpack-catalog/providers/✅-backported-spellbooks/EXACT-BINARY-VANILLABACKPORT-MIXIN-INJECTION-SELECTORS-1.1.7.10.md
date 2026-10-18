# Vanilla Backport 1.1.7.10 — seletores compilados dos mixins de movimento

**18/10/2026 · ✅ `EXACT_PUBLISHER_VERBOSE_CLASSFILE_INJECTION_ANNOTATIONS` · ⚠️ transformação do alvo ainda não observada · ⛔ adapters/perks externos não autorizados.**

## Proveniência e resultado

- **Distribuição exata:** `VanillaBackport-neoforge-1.21.1-1.1.7.10.jar`, CurseForge projeto 417430, arquivo 8229724, 54.902.084 bytes, SHA-1 `eb30efe569cbd5186abf9e5d1e64d4a84895b346`, SHA-256 `ecd807ac358e243ede17819455788c7b7a0ce5e0af4aecee82c1c62c586d818d`. São hashes do **publisher**, não de uma cópia instalada física medida no computador.
- **Java 21:** [workflow #39169078531](https://github.com/Gustavaopere/Black-Arcana/actions/runs/39169078531) **SUCCESS**; no mesmo artefato publicado, testes de movimento **10/10**, manifesto NeoForge **12/12**, anotações e seletores de injeção **12/12**. Marcadores `PASS_VANILLABACKPORT_11710_BOUNDED_MOBILITY_BYTECODE`, `PASS_VANILLABACKPORT_11710_MIXIN_MANIFEST_BOUNDARY` e **`PASS_VANILLABACKPORT_11710_COMPILED_MIXIN_INJECTION_DECLARATIONS`**, `deviations=[]`. [JSON #12151413141](https://github.com/Gustavaopere/Black-Arcana/actions/runs/39169078531/artifacts/12151413141).
- **Verificador de classfile:** [`docs/qa/vanillabackport_11710_mixin_injections.py`](../../../../docs/qa/vanillabackport_11710_mixin_injections.py), consumindo `javap -p -v` depois de certificar SHA-256/SHA-1/tamanho e [manifesto no JAR](EXACT-BINARY-VANILLABACKPORT-MIXIN-DECLARATION-1.1.7.10.md). Exige anotação `@Mixin` **`RuntimeInvisibleAnnotations` da classe** e a anotação de cada handler em **`RuntimeVisibleAnnotations` do método**, não apenas tokens existentes no constant pool.
- **Fonte oficial de referência**, pin `ItsBlackGear/VanillaBackport@adb579d205a05bcc7d1f34ce402cea6f1335a760`, sem equivalência source↔build comprovada: [EntityMixin.java](https://github.com/ItsBlackGear/VanillaBackport/blob/adb579d205a05bcc7d1f34ce402cea6f1335a760/common/src/main/java/com/blackgear/vanillabackport/core/mixin/common/entities/EntityMixin.java), [LivingEntityMixin.java](https://github.com/ItsBlackGear/VanillaBackport/blob/adb579d205a05bcc7d1f34ce402cea6f1335a760/common/src/main/java/com/blackgear/vanillabackport/core/mixin/common/entities/LivingEntityMixin.java), [RangedAttributeMixin.java](https://github.com/ItsBlackGear/VanillaBackport/blob/adb579d205a05bcc7d1f34ce402cea6f1335a760/common/src/main/java/com/blackgear/vanillabackport/core/mixin/common/attributes/RangedAttributeMixin.java).

## Relação com mapeamento Mojang 1.21.1 oficial — sem prova de invocação

✅ [Workflow #39170006472](https://github.com/Gustavaopere/Black-Arcana/actions/runs/39170006472) verificou os hashes publicados pela Mojang e encontrou, em ambos os mapping sets, **sete métodos-alvo vanilla com nomes, parâmetros e retornos**; [dossiê de assinaturas](EXACT-MOJANG-1211-MIXIN-TARGET-SIGNATURES.md) e [JSON #12152385800](https://github.com/Gustavaopere/Black-Arcana/actions/runs/39170006472/artifacts/12152385800). `Entity.setDeltaMovement(DDD)V` existe no owner `Entity`, mas **não foi certificado** que `LivingEntity.travel` contém quatro chamadas correspondentes ou a quarta é o alvo correto. `RangedAttribute` existe no mapeamento, porém seu construtor não é coberto como método comum. Ainda exige bytecode alvo NeoForge/Mixin aplicado e QA físico para qualquer conclusão de compatibilidade. Não promove Stage nem altera contagem.

## Avanço posterior — contagem efetiva de invocações no cliente vanilla 1.21.1

O [gate Java21 #39170808679](https://github.com/Gustavaopere/Black-Arcana/actions/runs/39170808679) obteve o JAR **cliente Mojang** verificado por SHA-1/tamanho oficiais, resolveu o obfuscation mapping e inspecionou os métodos com `javap -p -c -s`. O [dossiê de callsites](EXACT-MOJANG-1211-VANILLA-CLIENT-CALLSITES.md) certifica **4 chamadas de `setDeltaMovement(DDD)` em `LivingEntity.travel`**, com a quarta em **PC 1240** e `ordinal=3` possível no **cliente vanilla**. Os outros três edges nominalmente verificados têm **uma chamada cada**, e `RangedAttribute.<init>(String,double,double,double)` está presente no classfile. **Isso não demonstra que NeoForge 21.1.250 e demais mixins preservem os callsites nem que a injeção tenha sido aplicada.** É prova mais forte que mapeamento simples, ainda abaixo de aceitação física.

## Loader real isolado — três target-mixing reports do Vanilla Backport (18/10/2026)

✅ [#39178310071](https://github.com/Gustavaopere/Black-Arcana/actions/runs/39178310071) confirmou em servidor mínimo NeoForge 21.1.250 + Platform 1.3.3 + Vanilla Backport 1.1.7.10, após validação de SHA-256 dos JARs, três logs **exatos** `Mixing ... from vanillabackport.mixins.json into ...`: `EntityMixin→Entity`, `LivingEntityMixin→LivingEntity`, `RangedAttributeMixin→RangedAttribute`. [Dossiê e limites](EXACT-RUNTIME-VANILLABACKPORT-MINIMAL-SERVER-1.1.7.10.md), `Done (10.039s)`, 10/10 regressões e zero desvios. Diferenciar **aplicação reportada pelo serviço Mixin** de verificação pós-transformação em bytecode e de callbacks executados: ambos últimos seguem ⚠️. Nem Iron's nem Backported Spellbooks foram carregados nesse servidor mínimo.

## Sete seletores `@Mixin` validados no classfile

| Classe mixin e destino de `@Mixin` | Handler compilado | Tipo de injeção | Método alvo no metadata | `@At` / selector |
|---|---|---|---|---|
| `EntityMixin` → `net.minecraft.world.entity.Entity` | `vb$earlyCapture` | `@Inject` | `move(MoverType,Vec3)V` | `HEAD` |
| `EntityMixin` → `Entity` | `vb$capture` | `@WrapOperation` | `move(MoverType,Vec3)V` | `INVOKE Entity.collide(Vec3):Vec3` |
| `EntityMixin` → `Entity` | `vb$RestituteMovementAfterCollisions` | `@Inject` | `move(MoverType,Vec3)V` | `INVOKE Entity.tryCheckInsideBlocks()V` |
| `LivingEntityMixin` → `net.minecraft.world.entity.LivingEntity` | `createLivingAttributes` | `@ModifyReturnValue` | `createLivingAttributes():AttributeSupplier.Builder` | `RETURN` |
| `LivingEntityMixin` → `LivingEntity` | `vb$handleMovementFriction` | `@ModifyArg` | `travel(Vec3)V` | `INVOKE LivingEntity.handleRelativeFrictionAndCalculateMovement(Vec3,float):Vec3`, **`index=1`** |
| `LivingEntityMixin` → `LivingEntity` | `vb$applyAirDrag` | `@WrapOperation` | `travel(Vec3)V` | `INVOKE LivingEntity.setDeltaMovement(double,double,double)V`, **`ordinal=3`** |
| `RangedAttributeMixin` → `net.minecraft.world.entity.ai.attributes.RangedAttribute` | `vb$fixKnockbackResistanceRange` | `@Inject` | `<init>(String,double,double,double)V` | `TAIL` |

As descrições Java simplificadas são **rótulos**, não novas assinaturas inferidas: o gate compara os **descritores JVM completos**, com namespace, tipo de retorno, selector `@At`, e `index`/`ordinal` quando presentes. `@Mixin` e `@At` são definidos pelo provider em classes compiladas; não são hooks públicos para Black Arcana.

## Consequências para a arquitetura de perks

1. **Colisão e rebote:** o `EntityMixin` declara captura em `move` antes da colisão e interceptação de `Entity.collide`; o cálculo de restituição se posiciona antes de `tryCheckInsideBlocks`. O bytecode de consumo dos atributos já foi verificado em [auditoria de movimento](EXACT-BINARY-VANILLABACKPORT-MOBILITY-HOST-1.1.7.10.md). A transformação real de `Entity.move` não foi executada.
2. **Fricção e arrasto:** `LivingEntityMixin` declara três seletores em `createLivingAttributes` e `travel`. O **ordinal 3** de `setDeltaMovement(DDD)V` é um ponto de compatibilidade sensível a mudanças no alvo/overwrites de terceiros; **não** é prova de sucesso ou exclusividade na instalação.
3. **Limites de atributos:** o limite de `bounciness` [0,1] já consta da `RangedAttribute` criada em `ModAttributes`. O `RangedAttributeMixin` injetado em `<init>` atua, no **código-fonte pinado**, sobre nomes de `knockback_resistance`; não é a implementação do teto de `bounciness`. A classe foi anotada e seu método alvo certificado; a lógica de knockback não foi certificada por este gate.
4. **Composição das fontes:** `Slime Aspect` `+0.5 ADD_VALUE bounciness`, `+0.15 ADD_MULTIPLIED_TOTAL jump`, `−0.10 ADD_MULTIPLIED_TOTAL air drag`; `Slime Boots` `+2.5 ADD_VALUE bounciness`, `+0.10 ADD_MULTIPLIED_BASE jump`, `+0.30 ADD_MULTIPLIED_BASE friction`, `−0.50 ADD_MULTIPLIED_BASE air drag`. Nenhuma dessas constantes prova valor efetivo/stacking/amplificador em jogador.
5. **Boundary:** o host Vanilla Backport/Minecraft implementa a física, Backported Spellbooks implementa magia/equipamento, Iron's controla cast e custos, RPG Skill Tree é provider de perks/progressão e Black Arcana controla apenas seu runtime. Não fazer injecção paralela, inscrição de Mixin própria, alteração externa de coeficiente, listener duplicado de queda ou XP/Mastery de tick sem contrato causal real.

## Validação ainda necessária — não promover Stage

- ⚠️ SHA física da cópia Vanilla Backport no perfil, bootstrap NeoForge com Platform 1.3.3, execução real de transformação e verificação do método-alvo/ordinal no ambiente completo; possíveis conflitos de mixins com outros providers.
- ⚠️ Player real em dedicated server com os 4 cenários: sem buff/botas; buff somente; botas somente; ambos. Para cada cenário, medir atributos resolvidos, salto, atrito, air drag, colisão/restituição e queda; incluir amplificador, relog, respawn, troca de equipamento, supressão de bounce, alterações de movimento e efeitos de outros mods.
- ⛔ Adapter de perks sem hook público validado e configuração de causalidade server-authoritative/sem duplicação. O gate não faz `java -jar` do modpack nem faz transformador Mixin executar o código.

**Métricas preservadas:** Backported Spellbooks **✅ 6/6** raízes, **✅ 6/6** fichas, **✅ 6/6** identidades com ao menos um método compilado delimitado, mas compatibilidade runtime ⚠️; host **✅ 3/3 mixins de movimento/atributos com annotations verificadas** e 7/7 handlers **dentro desse escopo**, não cobertura integral de todos os mixins do mod. +0 raízes mágicas, +0 adapters. Catálogo global mínimo **1.857 objetos / 1.855 estritos**, denominador aberto (**—%**). Stage 06.05 🟡, Stage 09 PENDING; PR #825 permanece draft, sem merge.
