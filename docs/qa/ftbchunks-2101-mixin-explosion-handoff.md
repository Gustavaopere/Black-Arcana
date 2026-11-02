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

## Limites de interpretação

A presença de um mixin em JSON confirma apenas **declaração** de configuração pelo publisher, não prova que o mixin foi aplicado no servidor. A ausência de callsites JVM em classes do FTB Chunks **não prova ausência de invocação** por transformações, mods externos ou APIs reflexivas. A proteção de explosões pode operar por caminhos específicos de `Explosion.getToBlow` e `clearToBlow`; isso não autoriza assumir que intercepta `Level.destroyBlock` e `BlockState.onBlockExploded` do Tremorzilla. O estado real dos claims, o resultado de datapacks/mixins, a cobertura por bloco e `WorldEffectPolicy` permanecem não verificados.

**Status:** ⚠️ parcial/condicionado; `NO_MUTATION`; `NOT_CERTIFIED`; `physical_qa=NOT_TESTED`; +0 fichas e +0 hooks mutadores. Stage 06 permanece ativo. Faltam as provas de integração com servidor e claims por bloco.
