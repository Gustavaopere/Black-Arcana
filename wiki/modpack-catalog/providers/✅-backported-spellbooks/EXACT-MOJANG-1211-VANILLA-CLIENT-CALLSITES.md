# Minecraft 1.21.1 — callsites nos classfiles do cliente vanilla oficial

**18/10/2026 · ✅ `OFFICIAL_HASH_VERIFIED_VANILLA_CLIENT_CLASSFILE_CALLSITES` · ⚠️ alvo NeoForge 21.1.250 não verificado · ⛔ perks sem boundary.**

## Estado posterior do alvo NeoForge servidor (18/10/2026)

✅ O [JAR patchado de servidor NeoForge 21.1.250](EXACT-NEOFORGE-211250-MIXIN-TARGETS.md) foi **auditado posteriormente** no [workflow Java21 #39176290939](https://github.com/Gustavaopere/Black-Arcana/actions/runs/39176290939): 7/7 testes, 4 `setDeltaMovement(DDD)` em `LivingEntity.travel`, quarta instrução PC **1314**. A condição de "alvo NeoForge não verificado" descrita no snapshot abaixo se refere ao **checkpoint anterior**; agora a contagem de servidor patchado está certificada. **Ainda permanecem ⚠️ não certificados** aplicação do mixin Vanilla Backport, cardinalidade após todos os mods, dedicated server conectado e cliente NeoForge.

## Evidência binária, não inferência de mapeamento

- **Distribuição:** `Minecraft 1.21.1` **client JAR oficial Mojang, sem patches NeoForge**, recuperado do `downloads.client` do JSON da release selecionada por [`version_manifest_v2.json`](https://piston-meta.mojang.com/mc/game/version_manifest_v2.json). O gate compara o SHA-1 e tamanho do JAR baixado com a metadata Mojang, verifica a integridade ZIP e utiliza exclusivamente `client_mappings` também validados pelo SHA-1 oficial. A identificação dos nomes originais ↔ obfuscados é derivada desse arquivo exato de mapeamento, não de classes supostas.
- **Teste Java21/Python3.12:** [GitHub Actions #39170808679](https://github.com/Gustavaopere/Black-Arcana/actions/runs/39170808679), **SUCCESS** no HEAD `52e35df40aa6cb9ad4fff75e8c03407e8e56d56c`. **8/8 autotestes de mapeamentos** + **8/8 regressões de callsites**, com `PASS_MINECRAFT_1211_OFFICIAL_TARGET_MAPPINGS` e **`PASS_MINECRAFT_1211_VANILLA_CLIENT_CALLSITE_INSPECTION`**, `deviations=[]`. [Artefato JSON #12152825567](https://github.com/Gustavaopere/Black-Arcana/actions/runs/39170808679/artifacts/12152825567).
- **Reprodutibilidade:** [`docs/qa/minecraft_1211_vanilla_target_callsites.py`](../../../../docs/qa/minecraft_1211_vanilla_target_callsites.py) e [workflow](../../../../.github/workflows/minecraft-1211-mixin-target-mappings.yml). `javap -p -c -s` sobre as classes ofuscadas `Entity`, `LivingEntity` e `RangedAttribute`; método selecionado por nome ofuscado, descritor JVM completo e overload exato. Os nomes dos métodos de entrada e invocados provêm do mapeamento hash-pinned. Inspeção limitada a quatro edges, sem redistribuição dos classfiles, mappings ou JAR.
- **Histórico RED/GREEN:** [run #39170758433](https://github.com/Gustavaopere/Black-Arcana/actions/runs/39170758433) falhou antes da inspeção real por uma **asserção sintética de tipo errado** no teste Python (comparação de uma string com lista de linhas); a asserção foi corrigida. O sucessor #39170808679 passou os 16 autotestes e analisou o JAR. A falha inicial **não constitui incompatibilidade de Minecraft**.

## Contagens de invocações compiladas — vanilla cliente 1.21.1

| Owner da instrução (deobfuscado via mapping) | Alvo esperado | Quantidade de callsites compilados correspondente |
|---|---|---:|
| `net.minecraft.world.entity.Entity.move(MoverType,Vec3):void` | `Entity.collide(Vec3):Vec3` | **1** |
| `Entity.move(MoverType,Vec3):void` | `Entity.tryCheckInsideBlocks():void` | **1** |
| `net.minecraft.world.entity.LivingEntity.travel(Vec3):void` | `LivingEntity.handleRelativeFrictionAndCalculateMovement(Vec3,float):Vec3` | **1** |
| `LivingEntity.travel(Vec3):void` | `Entity.setDeltaMovement(double,double,double):void` (owner do método via classe base; callsite em contexto de `LivingEntity`) | **4** |

O gate encontrou **quatro** instruções `invoke*` cuja resolução de método/descritor coincide com `setDeltaMovement(DDD)V` no bloco `LivingEntity.travel`. O alvo compilado de índice **zero-based `ordinal=3`** existe nesse bytecode, com quarta instrução no PC **1240**. Esse resultado **reforça o alinhamento declarativo** do seletor `@WrapOperation(ordinal=3)` observado no [JAR Vanilla Backport 1.1.7.10](EXACT-BINARY-VANILLABACKPORT-MIXIN-INJECTION-SELECTORS-1.1.7.10.md), mas não prova que a mesma posição sobrevive aos patches de loader e outros mixins.

O método `RangedAttribute` foi testado separadamente: o **construtor de JVM `(Ljava/lang/String;DDD)V` existe no classfile do cliente vanilla**, resolvendo a pendência que o mapping ProGuard sozinho não podia satisfazer. Seu `@Inject(<init>,TAIL)` do addon é anotação compilada do **provider**, não injeção física observada.

## Status da matriz de causalidade

- **✅ Mojang vanilla:** download exato 1.21.1 com hashes do próprio manifesto, mapeamento ofuscado→nomeado, assinaturas e quatro edges com contagem; **ordinal 3 presente no cliente vanilla** e construtor do `RangedAttribute` encontrado.
- **✅ Provider Vanilla Backport publisher:** JAR 1.1.7.10 hash certificado, mixin JSON e três classfiles compilados, sete handlers anotados, `index=1` e `ordinal=3`; conjunto de provas independente.
- **⚠️ Ainda NÃO demonstrado:** bytecode transformado de `LivingEntity.travel` e `Entity.move` pelo **NeoForge 21.1.250**, ordem/compatibilidade com outros mixins, chamada alvo no dedicated server, aplicação real de `@WrapOperation` no momento de bootstrap, resolução de registros e dos atributos numéricos em jogo, SHA física do host instalado.
- **⛔ Boundary de perk:** sem hook/API real, não alterar parâmetros nativos, não duplicar o handler de queda, não cobrar recursos em duplicidade ou conceder Mastery por tick/colisão.

**Propriedade do runtime:** vanilla/NeoForge e Vanilla Backport possuem o movimento/atributos; Backported Spellbooks possui Slime Aspect/Slime Boots/queda; Iron's possui cast/custos; RPG Skill Tree fornece apenas atributos/progressão/perks por boundary verdadeiro; Black Arcana somente seu runtime mágico.

**Contagens preservadas:** Backported Spellbooks **6/6 magias** estáticas, 6/6 fichas técnicas, 6/6 magias com pelo menos um método compilado certificado. Os **4 calls** de `setDeltaMovement` são invocações técnicas do Minecraft e **não quatro magias/efeitos novos**. Global ainda com mínimo documental **1.857 objetos semânticos (1.855 estritos)**, universo total aberto (—%). **+0 magias, +0 adapters**, Stage 06.05 🟡 e Stage 09 físico pendente. Nenhum merge/promover Stage a partir de callsites vanilla.
