# Handoff — FTB Chunks 2101.1.22: `FireBlockMixin` e `FlowingFluidMixin`

## Autoridade e escopo

Continuação da auditoria do `BlockStateMixin` da [PR #1013](https://github.com/Gustavaopere/Black-Arcana/pull/1013), integrada a `Black-Arcana/main@80256e4ef535bb6f1c41d209f3aff91089834c90`. O modpack registra FTB Chunks NeoForge **2101.1.22**, e a inspeção segue o JAR exato publisher SHA-256 `4ba1b3352184fa7f6e2aa4bca76edd074867697d62344dfa50dcccdb4dab5217`.

A [PR #1012](https://github.com/Gustavaopere/Black-Arcana/pull/1012) comprovou 12 classes de mixin declaradas no JAR. Entre os mixins comuns: `FireBlockMixin.class` (SHA-256 `670463ce84b03d26852ba333370f15f0edf69eae89d8a89d504167b14caa41e2`) apresentou a string `Redirect`, e `FlowingFluidMixin.class` (SHA-256 `24ffbe40205ff6db02093f18cdc96bb23c54e80e9afd29e769c8067b0a85d971`) apresentou `Inject` e `BlockState`. Strings de classfile são indicadores, **não** interpretação de alvos/injeções.

## Evidência planejada

A [sonda read-only](ftbchunks_2101_fire_fluid_mixins_probe.py) reutiliza o parser de anotações/classfile da PR #1013 para extrair da versão **exata**: anotação `@Mixin` e classe-alvo, assinaturas JVM, metadados de métodos e de `@Inject`/`@Redirect` quando presentes, e hashes dos métodos compilados. O resultado não contém código nem assets do FTB Chunks; é uma análise clean-room voltada à interoperabilidade.

A [CI](../../.github/workflows/ftbchunks-2101-fire-fluid-mixins.yml) executa regressões sintéticas negativas e examina o JAR publisher publicado no Maven. A primeira execução coleta evidência `UNSEALED DISCOVERY` e não é suficiente para merge. Dados verificados serão fixados no `FTBCHUNKS-2101-FIRE-FLUID-MIXINS-ABI.json` e submetidos a nova execução com `--seal` sobre a HEAD final, acompanhada da CI completa.

## Observação SHA-exata — primeira CI #41500527241

O [workflow de descoberta](https://github.com/Gustavaopere/Black-Arcana/actions/runs/41500527241) aprovou **12 testes sintéticos** e extraiu metadados das classes `FireBlockMixin.class` e `FlowingFluidMixin.class` do publisher JAR 2101.1.22. O [manifesto da observação](../../wiki/modpack-catalog/providers/✅-alexs-caves-continued/FTBCHUNKS-2101-FIRE-FLUID-MIXINS-ABI.json) fixa SHA-256 da classe, métodos, descritores, anotações e digests de bytecode; não inclui corpos de implementação.

| Classe | `@Mixin` alvo compilado | Anotação de método observada | Alvo do ponto de transformação |
|---|---|---|---|
| `FireBlockMixin` | `net.minecraft.world.level.block.FireBlock` | `@Redirect` em `ftbc$getIgniteOdds(FireBlock,LevelReader,BlockPos,BlockPos):int` | `method=[tick]`, `@At(value=INVOKE, target=FireBlock.getIgniteOdds(LevelReader,BlockPos):int)` |
| `FlowingFluidMixin` | `net.minecraft.world.level.material.FlowingFluid` | `@Inject` em `onGetSpread(Level,BlockPos,BlockState,CallbackInfoReturnable,Map):void` | `method=[getSpread]`, `@At(value=RETURN)` |

O `FireBlockMixin` declara **três métodos**: `<init>()V`, `getIgniteOdds(LevelReader,BlockPos):int` marcado como `@Shadow` (sem `Code` no classfile), e `ftbc$getIgniteOdds` marcado como `@Redirect`. O método de redirecionamento tem **20 bytes** de código compilado, SHA-256 `01389285af24fc055acf9de6a1cf74d4922114773223d090e7787b784459cb68`.

O `FlowingFluidMixin` declara **dois métodos**: `<init>()V` e `onGetSpread` com `@Inject`. Este último contém **8 bytes** de código compilado, SHA-256 `034c82c80aa97b282fcd6c5f1bcf43ec043b2ea12a2f7dca28b26debb2144281`. A leitura de anotações não examina de forma semântica as invocações desse bytecode: a existência da injeção não certifica que ele faça veto, consulte claims ou seja aplicado no servidor.

**Conclusão de interoperabilidade:** estas classes declaradamente incidem sobre `FireBlock.tick`/`getIgniteOdds` e `FlowingFluid.getSpread`. Não foi demonstrada por elas interceptação anotada de `Level.destroyBlock`, `BlockState.onBlockExploded` ou `Explosion.getToBlow` do Tremorzilla. Mesmo que as transformações sejam aplicadas corretamente, seu alcance é específico aos métodos listados. O caminho de `WorldEffectPolicy`, acesso a claims resolvidos e a validação física continuam pendentes.

**Gate:** a primeira CI é de descoberta. O manifesto será validado por `--seal` em execução posterior, além da CI principal e GameTests, antes de considerar merge. Não promover a ficha de 28/30, nem Stage 06.

## Limites obrigatórios

Ainda que se prove uma injeção para propagação de fogo ou fluxo de fluidos, seu alvo é uma rota específica; não fornece autorização territorial genérica para **`TremorzillaEntity.breakBlocksAround`**, `Level.destroyBlock`, `BlockState.onBlockExploded` ou `Explosion.getToBlow`. O runtime Black Arcana conserva `WorldEffectPolicy` e não delega essa autoridade a event handlers alheios sem contrato validado.

**Status:** ⚠️ parcial/condicionado; `NO_MUTATION`, `NOT_CERTIFIED`, `physical_qa=NOT_TESTED`, `mutating_hook=NOT_VERIFIED`. Sem nova ficha, sem hooks homologados ou promoção do Stage 06.
