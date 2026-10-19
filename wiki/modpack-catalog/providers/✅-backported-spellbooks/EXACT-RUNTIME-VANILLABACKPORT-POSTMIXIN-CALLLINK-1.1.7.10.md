# Vanilla Backport 1.1.7.10 — sete invocações de handlers em classes pós-Mixin exportadas

**18/10/2026 · ✅ `EXPORTED_POST_MIXIN_CLASSFILE_BOUNDED_CALLSITE_LINKAGE` · ⚠️ callbacks exercitados em jogador, cliente e modpack real · ⛔ adapters sem hook oficial.**

## Fonte de prova, ambiente e integridade

- **Ambiente:** GitHub Actions Java21, servidor dedicado mínimo isolado, Minecraft **1.21.1**, NeoForge **21.1.250**, **Platform 1.3.3** e **Vanilla Backport 1.1.7.10**. Não inclui Iron's Spellbooks 3.16.3, Backported Spellbooks 0.1.2, Epic Fight, perfil completo ou mundo do usuário.
- **Identidades de publisher verificadas antes do boot:** installer NeoForge 21.1.250 SHA-256 `0e47a91ba2139a8db4bf7627af081f7b5789b508bb039ee8dea1272b79693d60`; Platform NeoForge 1.3.3 SHA-256 `2d7175e43943d22cbb4f8d4533f0ad620f87a3ac12c77a4f15c3a35d965c4f18`; Vanilla Backport 1.1.7.10 SHA-256 `ecd807ac358e243ede17819455788c7b7a0ce5e0af4aecee82c1c62c586d818d`. Essas medições se referem aos **JARs oficiais baixados no runner**, não a uma medição física do perfil instalado.
- **Prova de diagnóstico anterior:** [run #39179955064](https://github.com/Gustavaopere/Black-Arcana/actions/runs/39179955064), **SUCCESS**. O [script de exportação](../../../../docs/qa/vanillabackport_11710_postmixin_export.py) localizou em `.mixin.out/class` os classfiles válidos de `Entity`, `LivingEntity` e `RangedAttribute`, anotou seus hashes e inspecionou headers/calls com `javap -p -c -s`. [JSON #12156071262](https://github.com/Gustavaopere/Black-Arcana/actions/runs/39179955064/artifacts/12156071262). Resultado `DISCOVERY_ONLY_POST_MIXIN_EXPORTS` **não prova sozinho** ligação de cada handler ao caller.
- **Gate posterior efetivo:** [run Java21 #39180390922](https://github.com/Gustavaopere/Black-Arcana/actions/runs/39180390922), **SUCCESS**, **7/7 autotestes de regressão do gate de invocação**, `PASS_VB_11710_MINIMAL_POSTMIXIN_HANDLER_INVOKE_LINKAGE`, `verified=7`, `deviations=[]`; [JSON #12155268844](https://github.com/Gustavaopere/Black-Arcana/actions/runs/39180390922/artifacts/12155268844). [Verificador fail-closed](../../../../docs/qa/vanillabackport_11710_postmixin_invoke_gate.py), [workflow](../../../../.github/workflows/vanillabackport-11710-minimal-server-bootstrap.yml).
- **Técnica:** o Mixin executou com `mixin.debug.export=true` e filtro `net.minecraft.world.entity.**`; o verificador leu **as classes exportadas pós-transformação**, confirmou magic `CAFEBABE`, localizou cada handler declarado por família/sufixo exato e descritor JVM, localizou seu método-alvo por nome+descritor JVM e exigiu **uma instrução `invoke*` para aquele handler, dentro do método-alvo esperado**. O resultado não depende de comparar o PC anterior à transformação com o PC posterior: números de instrução e sufixos sintéticos de injeção podem variar.
- **Clean-room:** nenhum JAR/classfile exportado ou código de terceiro foi incorporado à branch ou uploaded ao artefato. Apenas script próprio de diagnóstico e evidência JSON limitada a nomes, descritores, deslocamentos, hashes e contagens.

## Sete ligações demonstradas no bytecode pós-transformação do dedicated server mínimo

| Classe-alvo exportada | Método-alvo pós-transformação | Handler do Vanilla Backport encontrado e invocado 1× |
|---|---|---|
| `Entity` | `move(MoverType, Vec3):void` | `vb$earlyCapture` (`@Inject HEAD`) |
| `Entity` | `move(MoverType, Vec3):void` | `vb$capture` (`@WrapOperation collide(Vec3)`) |
| `Entity` | `move(MoverType, Vec3):void` | `vb$RestituteMovementAfterCollisions` (`@Inject` antes de `tryCheckInsideBlocks`) |
| `LivingEntity` | `createLivingAttributes():AttributeSupplier.Builder` | `createLivingAttributes` (wrapper `@ModifyReturnValue`) |
| `LivingEntity` | `travel(Vec3):void` | `vb$handleMovementFriction` (`@ModifyArg index=1`) |
| `LivingEntity` | `travel(Vec3):void` | `vb$applyAirDrag` (`@WrapOperation ordinal=3`) |
| `RangedAttribute` | `<init>(String,double,double,double)` | `vb$fixKnockbackResistanceRange` (`@Inject TAIL`) |

A origem de cada `@At`, `ordinal` e `index` é a [prova anterior das anotações compiladas no JAR do provider](EXACT-BINARY-VANILLABACKPORT-MIXIN-INJECTION-SELECTORS-1.1.7.10.md), não a interpretação do método exportado. A prova **nova** acrescenta a presença do **handler e seu `invoke` no caller específico depois do processamento Mixin**, com cardinalidade 1 por vínculo. Nenhum dos sete handlers foi exercitado mediante movimento de jogador ou um cast real.

**Observação específica sobre `RangedAttributeMixin`:** o handler atua, no source pinado, sobre nomes de `knockback_resistance`; sua chamada no construtor **não** implementa nem demonstra como é calculado o teto registral de `bounciness` 1.0.

## Boundary de implementação e aceitação restante

- ✅ **Certificado neste recorte:** configuração e bytecode do provider; method targets e callsites do cliente vanilla e servidor patchado NeoForge; bootstrap isolado, três relatos exatos de target mixing; agora sete invocações efetivas de handlers em **classes pós-Mixin exportadas**, com seus métodos-alvo.
- ⚠️ **Não verificado:** a execução desses sete handlers em fluxo real de movimentação; a resolução efetiva dos atributos no jogador; `Slime Aspect` e Slime Boots com/sem efeito simultâneo; perduração, amplifier, stacking e equipamento; dedicated server com **Iron's 3.16.3 + Backported Spellbooks 0.1.2**; cliente conectado; modificadores de Epic Fight/ParCool, demais mixins da modlist; igualdade SHA com JARs instalados e compatibilidade do perfil completo.
- ⛔ **Não autoriza perk adapter:** nenhuma permissão de escrita no host, hook público, setter, callback seguro ou alteração de custo/dano/physics foi demonstrada. Black Arcana conserva seu runtime mágico, RPG Skill Tree somente provider de progressão/perks por contrato.
- **Stage e contagens:** Stage 06.05 🟡, Stage 09 físico PENDING. Backported Spellbooks continua **✅ 6/6 magias catalogadas** no critério de raízes/fichas e ao menos um método binário delimitado por raiz; `Slime Boots` continua item, não magia extra. Este gate fornece **7/7 vínculos pós-transformação apenas no escopo**. **+0 magias, +0 adapters**. Piso global **1.857 objetos semânticos / 1.855 estritos**, universo aberto (**—%**). PR #825 permanece draft, nenhum merge por esta prova.
