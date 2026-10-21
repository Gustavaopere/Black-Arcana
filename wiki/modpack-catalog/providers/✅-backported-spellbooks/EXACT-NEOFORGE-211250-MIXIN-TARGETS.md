# NeoForge 21.1.250 — callsites reais no alvo de servidor instalado

**18/10/2026 · ✅ `EXACT_INSTALLER_GENERATED_PATCHED_SERVER_BYTECODE_ONLY` · ⚠️ transformações finais/mixins do modpack e cliente real · ⛔ adapters de perks sem contrato.**

## Proveniência e release exata

- **Autoridade física do perfil:** a modlist certificada do sibling `Gustavaopere/neoforge-rpg-skilltree` contém **Minecraft 1.21.1 / NeoForge 21.1.250**; Black Arcana `main` ainda usa baseline de build NeoForge 21.1.248, distinção que **não** foi apagada nem convertida em upgrade.
- **Distribuição oficial:** [NeoForge Maven 21.1.250](https://maven.neoforged.net/releases/net/neoforged/neoforge/21.1.250/). O workflow baixou `neoforge-21.1.250-installer.jar` e comparou seu SHA-256 ao arquivo `.jar.sha256` do **próprio repositório Maven oficial**, antes de invocar `java -jar ... --installServer`. Procedimento de instalação conforme [documentação NeoForged](https://docs.neoforged.net/user/docs/server/).
- **Instalador exato:** **6.972.109 bytes**, SHA-256 `0e47a91ba2139a8db4bf7627af081f7b5789b508bb039ee8dea1272b79693d60`, ZIP íntegro, `--installServer` com **exit 0**. Os JARs gerados foram encontrados por varredura das classes-alvo, não inferidos da versão do outro projeto.
- **Primeira descoberta:** [GitHub Actions #39176088200](https://github.com/Gustavaopere/Black-Arcana/actions/runs/39176088200), **SUCCESS**. O inventário identificou as duas camadas de classes que compõem o target instalado:
  - `libraries/net/neoforged/neoforge/21.1.250/neoforge-21.1.250-server.jar`: SHA-256 `1808fab692dc44b2d474295d1cdd9f1fe8a7dceab4f594210873646fafdf1359`. **Contém `Entity.class` e `LivingEntity.class` com patches do NeoForge**.
  - `libraries/net/minecraft/server/1.21.1-20240808.144430/server-1.21.1-20240808.144430-srg.jar`: SHA-256 `26ca9c40d7e1681190b428583c38816852218e78df3f8bdb60a59a78503aec71`. **Contém `RangedAttribute.class`**, ausente do primeiro JAR. A auditoria conserva essa distinção de owner físico.
- **Gate compilado:** [GitHub Actions #39176290939](https://github.com/Gustavaopere/Black-Arcana/actions/runs/39176290939), **SUCCESS**, HEAD `50a00fb1cbf8dbfdc68a80e989a2a9dfc35eaca0`, **7/7 autotestes**, `PASS_NEOFORGE_211250_PATCHED_SERVER_TARGET_CALLSITES`, `deviations=[]`. [Artefato JSON #12154062671](https://github.com/Gustavaopere/Black-Arcana/actions/runs/39176290939/artifacts/12154062671), [verificador fail-closed](../../../../docs/qa/neoforge_211250_target_bytecode.py), [workflow](../../../../.github/workflows/neoforge-211250-target-discovery.yml). Nenhum JAR ou bytecode completo de terceiros foi incorporado ao repositório ou artefato publicado.

## Relações reais de invocação no JAR NeoForge 21.1.250 de servidor

O gate localizou as classes dentro das duas camadas citadas, selecionou os métodos com descritores JVM completos por `javap -p -c -s`, e só contou chamadas `invoke*` com o método e descritor esperados:

| Método caller efetivo | Callee/descriptor verificado | Invocações |
|---|---|---:|
| `Entity.move(MoverType,Vec3)V` | `Entity.collide(Vec3):Vec3` | **1** |
| `Entity.move(MoverType,Vec3)V` | `Entity.tryCheckInsideBlocks():void` | **1** |
| `LivingEntity.travel(Vec3)V` | `LivingEntity.handleRelativeFrictionAndCalculateMovement(Vec3,float):Vec3` | **1** |
| `LivingEntity.travel(Vec3)V` | `Entity/LivingEntity.setDeltaMovement(double,double,double):void` | **4** |

**O índice zero-based `ordinal=3` existe no método `LivingEntity.travel` do JAR de patches do servidor**; a quarta instrução possui **PC 1314**. O scanner exige **exatamente** quatro chamadas e falha fechado se a quantidade ou os descritores mudarem.

Para contraste, no [cliente vanilla 1.21.1](EXACT-MOJANG-1211-VANILLA-CLIENT-CALLSITES.md) o gate #39170808679 havia identificado também quatro chamadas, mas quarta instrução no **PC 1240**. Essa diferença de PC demonstra que os bytes/offsets não são intercambiáveis, mesmo quando a cardinalidade do seletor é igual. Não generalizar para **NeoForge client** sem sua auditoria específica.

O construtor `net.minecraft.world.entity.ai.attributes.RangedAttribute.<init>(Ljava/lang/String;DDD)V` foi certificado no **classfile do SRG base** gerado pela instalação de servidor; o `RangedAttributeMixin` do Vanilla Backport declara `@Inject(TAIL)` nele, mas esse gate não aplicou a transformação Mixin.

## Causalidade conjunta e fronteira de evidência

1. **Provider:** [Vanilla Backport 1.1.7.10](EXACT-BINARY-VANILLABACKPORT-MIXIN-INJECTION-SELECTORS-1.1.7.10.md) contém `@WrapOperation` anotado sobre `LivingEntity.travel` → `setDeltaMovement(DDD)V`, **`ordinal=3`**, além de `@ModifyArg index=1` sobre `handleRelativeFrictionAndCalculateMovement`; o JAR do provider foi auditado em #39169078531.
2. **Minecraft vanilla:** os [mapeamentos oficiais](EXACT-MOJANG-1211-MIXIN-TARGET-SIGNATURES.md) e a [prova do cliente vanilla](EXACT-MOJANG-1211-VANILLA-CLIENT-CALLSITES.md) identificaram os nomes e quatro callsites nominais.
3. **NeoForge alvo servidor:** este gate **independente** confirmou as mesmas quatro relações e o quarto `setDeltaMovement` no alvo **servidor patchado 21.1.250**, antes de iniciar o modpack e aplicar transformações adicionais.
4. **Ainda ⚠️:** cópia física do NeoForge e do Vanilla Backport no computador, aplicação do Mixin Vanilla Backport no loader, conflitos com mixins de outros mods, cardinalidade após **todas** as transformações e registro de atributos já no runtime, compatibilidade NeoForge client, jogador real e multiplayer. Não inferir ausência de conflito apenas pela existência do quarto invoke no target inicial.
5. **Ainda ⛔:** nenhum setter/hook autorizado para Black Arcana ou RPG Skill Tree modificar parâmetros nativos de `Slime Aspect`/`Slime Boots`, criar efeitos duplicados, processar cooldown/queda paralelamente, conceder Mastery por tick/colisão ou transferir autoridade de física ao Black Arcana.

**Próximos gates físicos:** instrumentar observação do classloader após transformação no dedicated server e no cliente; confirmar que `EntityMixin` e `LivingEntityMixin` foram aplicados e que a seleção `ordinal=3` apontou ao invoke desejado; validar sem magia/botas, apenas magia, apenas botas e ambos; coletar atributos finais, salto, air drag, colisão/bounce, dano de queda, relog e efeito de outros mods. Somente um teste carregado e compatível do perfil pode encerrar essas linhas.

**Métricas e escopo:** Backported Spellbooks mantém **6/6 magias e fichas** e **6/6 magias com pelo menos um consumer compilado delimitado**, não métodos completos. Nova prova = **4/4 relações de callsites** do alvo NeoForge patchado 21.1.250 (uma delas com quatro invokes) e construtor de RangedAttribute; **+0** novas magias, **+0** adapters. Universo global mínimo documental **1.857 objetos semânticos / 1.855 estritos**, denominador aberto (**—%**). Stage 06.05 🟡; Stage 09 físico PENDING; PR #825 permanece draft, sem merge nesta evidência.
