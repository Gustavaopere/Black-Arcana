# Vanilla Backport 1.1.7.10 — alvos nomeados nos mapeamentos Mojang Minecraft 1.21.1

**18/10/2026 · ✅ `OFFICIAL_VERSION_PINNED_NAMED_METHOD_DECLARATIONS` (sete assinaturas em dois mapping sets) · ⚠️ NeoForge patched target e `@At` callsites · ⛔ perks/adapters sem contrato.**

## Proveniência e independência das fontes

- **Minecraft exato:** `1.21.1` (não generalizar para versões próximas ou 1.21.11). A [version_manifest_v2 da Mojang](https://piston-meta.mojang.com/mc/game/version_manifest_v2.json) seleciona a release `id=1.21.1`; o teste confere o SHA-1 do JSON específico, exigindo `downloads.server_mappings` e `downloads.client_mappings` oficiais e SHA-1 exato dos dois documentos baixados, antes de consultar nomes.
- **CI de prova:** [#39170006472](https://github.com/Gustavaopere/Black-Arcana/actions/runs/39170006472) **SUCCESS** no HEAD `a68ea14717bd816ff4fb1cc94605601aba785ba0`, **8/8 autotestes**, status `PASS_MINECRAFT_1211_OFFICIAL_TARGET_MAPPINGS`, `deviations=[]`. [JSON de evidências #12152385800](https://github.com/Gustavaopere/Black-Arcana/actions/runs/39170006472/artifacts/12152385800), [script fail-closed](../../../../docs/qa/minecraft_1211_mojang_mixin_target_mappings.py), [workflow](../../../../.github/workflows/minecraft-1211-mixin-target-mappings.yml). Os arquivos de mapeamento e JAR vanilla não são commitados ou anexados; somente a evidência estruturada é publicada.
- **Artefato de provider distinto:** o [Vanilla Backport NeoForge 1.1.7.10](EXACT-BINARY-VANILLABACKPORT-MIXIN-INJECTION-SELECTORS-1.1.7.10.md) foi certificado no JAR publisher file 8229724, SHA-256 `ecd807ac358e243ede17819455788c7b7a0ce5e0af4aecee82c1c62c586d818d`; o gate de mapeamentos certifica **Minecraft vanilla**, não estabelece identidade do host NeoForge transformado.
- **Relação com outras provas:** os sete `@Inject/@ModifyArg/@WrapOperation/@ModifyReturnValue` da distribuição foram inspecionados por `javap -p -v` em [#39169078531](https://github.com/Gustavaopere/Black-Arcana/actions/runs/39169078531). Esta auditoria compara os **nomes e assinaturas de métodos correspondentes nos mapeamentos oficiais**, sem afirmar que cada `@At` está presente ou será acionado.

## Assinaturas nomeadas certificadas

Estas sete assinaturas constam **tanto nos mapeamentos de cliente quanto nos de servidor** oficiais de Minecraft 1.21.1, verificadas por comparação dos nomes completos dos tipos, argumentos e tipo de retorno:

| Classe vanilla que declara a assinatura | Método nomeado | Parâmetros | Retorno | Utilidade no selector do provider |
|---|---|---|---|---|
| `net.minecraft.world.entity.Entity` | `move` | `MoverType, Vec3` | `void` | método onde o mixin captura movimento |
| `Entity` | `collide` | `Vec3` | `Vec3` | alvo nominal de `@WrapOperation` |
| `Entity` | `tryCheckInsideBlocks` | nenhum | `void` | alvo nominal do `@Inject` de restituição |
| `Entity` | `setDeltaMovement` | `double, double, double` | `void` | assinatura do método recebido por `LivingEntity` via herança; **não** prova callsite/ordinal na classe derivada |
| `net.minecraft.world.entity.LivingEntity` | `travel` | `Vec3` | `void` | método onde o provider modifica movimento |
| `LivingEntity` | `createLivingAttributes` | nenhum | `AttributeSupplier.Builder` | retorno interceptado para incluir três atributos |
| `LivingEntity` | `handleRelativeFrictionAndCalculateMovement` | `Vec3, float` | `Vec3` | alvo nominal de `@ModifyArg index=1` |

A classe `net.minecraft.world.entity.ai.attributes.RangedAttribute` também aparece nos dois mapping sets. Seu construtor `<init>(String,double,double,double)V` **não é registrado como método comum no mapping ProGuard**, portanto este gate atesta apenas a **classe**, não o descritor do construtor. O bytecode do mixin [já certificou](EXACT-BINARY-VANILLABACKPORT-MIXIN-INJECTION-SELECTORS-1.1.7.10.md) que ele *declara* `@Inject(<init>,TAIL)`, mas a existência do construtor no alvo vanilla/NeoForge exige análise separada de classfile.

## Avanço posterior — contagem efetiva de invocações no cliente vanilla 1.21.1

O [gate Java21 #39170808679](https://github.com/Gustavaopere/Black-Arcana/actions/runs/39170808679) obteve o JAR **cliente Mojang** verificado por SHA-1/tamanho oficiais, resolveu o obfuscation mapping e inspecionou os métodos com `javap -p -c -s`. O [dossiê de callsites](EXACT-MOJANG-1211-VANILLA-CLIENT-CALLSITES.md) certifica **4 chamadas de `setDeltaMovement(DDD)` em `LivingEntity.travel`**, com a quarta em **PC 1240** e `ordinal=3` possível no **cliente vanilla**. Os outros três edges nominalmente verificados têm **uma chamada cada**, e `RangedAttribute.<init>(String,double,double,double)` está presente no classfile. **Isso não demonstra que NeoForge 21.1.250 e demais mixins preservem os callsites nem que a injeção tenha sido aplicada.** É prova mais forte que mapeamento simples, ainda abaixo de aceitação física.

## Fronteiras e riscos

- **O que passou:** nomes, parâmetros e retornos definidos pela distribuição oficial do Minecraft **1.21.1** em **dois conjuntos** de mapeamento (cliente e servidor), além da classe `RangedAttribute`. O script falha se houver classe, overload, tipo de argumento ou retorno esperado ausente; baixa por hosts oficiais da Mojang e verifica hashes publicados.
- **O que NÃO passou por execução:** resolução de `@At(INVOKE)` em bytecode alvo, presença de **quatro** chamadas de `LivingEntity.setDeltaMovement(DDD)V` no contexto específico de `travel`, identidade do quarto callsite `ordinal=3`, acesso/herança após patches NeoForge, ordem de mixins concorrentes, sucesso do transformador, semântica do método `RangedAttribute.<init>`, dados de usuário em servidor/jogador. O mapeamento não conta invokes.
- **Interoperabilidade:** `Entity.move` e `LivingEntity.travel` são alvo de múltiplos potenciais modificadores de movimento do modpack. Não usar o sucesso dos mapeamentos como permissão para mixin próprio, getter com escrita, listener duplicado, alteração de `bounciness` ou envio de Mastery sem contrato.
- **Authority:** Mojang/Minecraft e Vanilla Backport definem movimento/atributos, Backported Spellbooks controla `slime_aspect` e Slime Boots, Iron's controla cast/custos, RPG Skill Tree somente progressão/perks via boundary real, Black Arcana apenas o runtime mágico próprio.

## Próxima aceitação técnica

1. Inspecionar o **bytecode do Minecraft 1.21.1 mapeado** ou classfiles transformados do NeoForge 21.1.250 quanto às chamadas de `Entity.collide`, `tryCheckInsideBlocks`, `handleRelativeFrictionAndCalculateMovement` e especialmente `setDeltaMovement(DDD)V` na ordem real do método `LivingEntity.travel`. O mapeamento sozinho não demonstra `ordinal=3`.
2. Checar `RangedAttribute.<init>(String,double,double,double)` em classfile da distribuição aplicável e a aplicação efetiva de `@Mixin` no conjunto de mods do perfil.
3. Validar em cliente e servidor com Platform 1.3.3, Vanilla Backport 1.1.7.10, Backported Spellbooks 0.1.2 e Iron's 3.16.3, incluindo Slime Aspect, Slime Boots, ambos e nenhum, com atributos finais e física observada.

**Métricas:** a prova de mapeamentos cobre **7/7 assinaturas vanilla selecionadas nos dois mapping sets**, não os sete handlers por execução física nem o universo Minecraft/NeoForge. Backported Spellbooks continua **6/6 identidades mágicas, 6/6 fichas, 6/6 magias com ao menos um método compilado delimitado**; esta etapa adicionou **+0 magias e +0 adapters**. Global com piso anterior **1.857 objetos semânticos / 1.855 estritos**, denominador ainda aberto (**—%**). Stage 06.05 🟡 e Stage 09 ⚠️ físico pendente. PR #825 draft; sem merge por este gate.
