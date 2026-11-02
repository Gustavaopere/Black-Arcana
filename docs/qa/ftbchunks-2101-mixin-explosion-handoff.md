# Continuidade — FTB Chunks 2101.1.22: metadados de mixins e callsites de explosão

**Base:** `Black-Arcana/main@71bd19c202f5c30fbbcd9e5021ab265f957b1aed`, após [PR #1011](https://github.com/Gustavaopere/Black-Arcana/pull/1011). O provider de claims da modlist física é `FTB Chunks (NeoForge)` **2101.1.22**, com loader NeoForge **21.1.250**. Não utilizar a branch atual do FTB Chunks como prova da versão física.

A PR #1011 identificou no JAR publisher de SHA-256 `4ba1b3352184fa7f6e2aa4bca76edd074867697d62344dfa50dcccdb4dab5217` o método `FTBChunks.explosionDetonate(Level, Explosion, List)`, `ignoreExplosion` e o helper `lambda$explosionDetonate$6` que consulta `allowExplosions`. A mesma auditoria não encontrou chamada JVM direta ao método entre as duas classes candidatas relacionadas a explosão e registrou `ftbchunks-common.mixins.json`. Nenhum listener `ExplosionEvent$Detonate` foi confirmado nesse recorte.

## Nova verificação SHA-exata

A [sonda read-only](ftbchunks_2101_mixin_registration_probe.py) inspeciona exclusivamente o publisher JAR verificado, usando Python 3.12 e `javap` Java 21:

1. Examina `META-INF/neoforge.mods.toml` e `ftbchunks-common.mixins.json` e verifica se a configuração de mixin está declarada nos metadados NeoForge.
2. Confere que as classes de mixin declaradas existem fisicamente no JAR; registra suas identidades SHA-256 e indicadores de string do arquivo compilado. Strings do classfile **não** equivalem a target/injeção comprovada.
3. Pesquisa a população completa, limitada, de arquivos `.class` do mesmo JAR para a referência nominal `explosionDetonate`; em seguida examina somente os candidatos com `javap`, distinguindo declaração do método e **invocação JVM direta**.
4. Exige a assinatura já observada `FTBChunks.explosionDetonate(Level,Explosion,List):void` para ancorar o resultado. Se não houver chamada direta, registra `0` sem extrapolar para mixins ou consumidores em outros artefatos.
5. Publica relatório com hashes e metadados limitados. A primeira [CI](../../.github/workflows/ftbchunks-2101-mixin-explosion.yml) é `UNSEALED DISCOVERY`. O manifesto `FTBCHUNKS-2101-MIXIN-REGISTRATION-ABI.json` deve ser preenchido com a evidência real, e validado novamente com `--seal` na HEAD final antes do merge.

O FTB Chunks tem licença `All Rights Reserved`; não transcrever código ou reproduzir arquivos do provider. A análise é de ABI, configuração e interoperabilidade, em regime clean-room.

## Descoberta no publisher JAR — CI exploratória #41466054105

A [execução inicial](https://github.com/Gustavaopere/Black-Arcana/actions/runs/41466054105) sobre o artefato Maven exato de **655.807 bytes** e SHA-256 `4ba1b3352184fa7f6e2aa4bca76edd074867697d62344dfa50dcccdb4dab5217` observou:

- `META-INF/neoforge.mods.toml` registra `ftbchunks-common.mixins.json`. O JSON do JAR possui SHA-256 `bd5f99632e804411285c53d1d5fc3cf90f938f265c62e2862b0fc790c00d5ad8`; o metadado TOML possui SHA-256 `9e626df21afb020a57812373e831aef52ca222c8728d58179c1fe651a3a6cde8`. A configuração declara compatibilidade `JAVA_17` e `defaultRequire=1`, não a mesma composição da branch pública mais recente.
- **12 classes de mixin declaradas e presentes**, sendo **9 comuns** (`ArmorStandMixin`, `BiomeMixin`, `BlockStateMixin`, `ChunkMapMixin`, `FireBlockMixin`, `FlowingFluidMixin`, `ItemFrameMixin`, `PistonBaseBlockMixin`, `VehicleEntityMixin`) e **3 client** (`ClientPacketListenerMixin`, `GuiMixin`, `UtilMixin`); nenhuma na lista `server`. Estas são declarações, não garantia de aplicação.
- Entre as classes mixin, os indicadores de strings do arquivo compilado **não encontraram** `explosionDetonate`, `destroyBlock`, `onBlockExploded` ou `Explosion`. O `BlockStateMixin` contém apenas o indicador genérico `BlockState` entre esses nomes. A ausência dessas strings é uma observação limitada de classfile, sem análise semântica completa das anotações e dos pontos de injeção.
- O censo examinado abrange **238 classfiles** do mesmo JAR. Apenas a classe proprietária `FTBChunks.class` contém o nome `explosionDetonate`. `javap` confirmou a assinatura publicada `(Level, Explosion, List)V`, e **zero invocações JVM diretas** a esse método entre as classes do JAR. Outras classes em dependências, transformações ou modpack real não foram examinadas nesse censo.

O [manifesto SHA-exato da descoberta](../../wiki/modpack-catalog/providers/✅-alexs-caves-continued/FTBCHUNKS-2101-MIXIN-REGISTRATION-ABI.json) fixa essa população, os hashes de cada classe mixin e os critérios de interpretação. **O resultado não demonstra que o método seja inalcançável:** só permite afirmar ausência de referências JVM diretas dentro do artefato investigado, segundo a seleção limitada por nome e `javap`. O próximo passo após selar a CI é obter prova de consumidor externo ou transformação efetiva e testar condições de claims/Blocos no servidor.

## Limites de interpretação

A presença de um mixin em JSON confirma apenas **declaração** de configuração pelo publisher, não prova que o mixin foi aplicado no servidor. A ausência de callsites JVM em classes do FTB Chunks **não prova ausência de invocação** por transformações, mods externos ou APIs reflexivas. A proteção de explosões pode operar por caminhos específicos de `Explosion.getToBlow` e `clearToBlow`; isso não autoriza assumir que intercepta `Level.destroyBlock` e `BlockState.onBlockExploded` do Tremorzilla. O estado real dos claims, o resultado de datapacks/mixins, a cobertura por bloco e `WorldEffectPolicy` permanecem não verificados.

**Status:** ⚠️ parcial/condicionado; `NO_MUTATION`; `NOT_CERTIFIED`; `physical_qa=NOT_TESTED`; +0 fichas e +0 hooks mutadores. Stage 06 permanece ativo. Faltam as provas de integração com servidor e claims por bloco.
