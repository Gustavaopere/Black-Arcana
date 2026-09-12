# Auditoria técnica — Gaze 1.1.7.1

## Evidence level

**EXACT HASH-MATCHED ARTIFACT / STRUCTURAL REGISTRY AUDIT CLOSED / DEPLOYED CONFIG + RUNTIME QA PENDING**.

O artefato físico `gaze-1.1.7.1.jar` / SHA-1 `a8cb3190bde157f78160ce65c202ce2d47fb2041` foi materializado a partir da versão Modrinth exata `od4ltbRo` em auditoria isolada. O workflow falha se o SHA-1 baixado não for idêntico ao da modlist física.

Evidência final:

- NON-MERGE PR #201;
- audit HEAD `2f4ff6536663b1c629a6a5ea92416765bea17b1e`;
- workflow run `34676660467` — GREEN;
- artifact `10292013626`;
- digest `sha256:fb69f353b672f7c8ec7b470c454d24d1c3110cb996a250076a16d2b053f23f71`.

Gaze é ARR. A inspeção foi clean-room e reteve apenas fatos estruturais necessários para catálogo/interoperabilidade: identidade criptográfica, registries, tipos/membros, resource paths e gates de controle estreitos. Nenhum corpo de implementação, asset, texto upstream, recipe ingredient list ou valor de balance foi copiado.

## Relação com Malum

Malum continua authority de Spirit Rite/Geas substrates, spirit resources e settlement. O artefato exato de Gaze registra/expõe addon identities sobre essa infraestrutura.

O registry exato fecha **26 `RiteHolder<SpiritRiteType>` distintos**. O progression setup do próprio provider referencia os 26 e usa páginas de Spirit Rite do Malum, provando que são identities player-facing/intencionais e não slots técnicos vazios.

O artefato também fecha **2 `GeasEffectType`** provider-owned:

- `pact_of_encroaching`;
- `domain_of_swords`.

Pela definição canônica da métrica semântica, Geas effect types continuam excluídos assim como os 37 base-Malum `GeasEffectType`: são effect/status-like types, não standalone spell/rite actions.

## Gate de config dos Rites

`com.strawberry.gaze.Config` registra `DISABLE_GAZE_RITES` / `disableGazeRites` como boolean de config **COMMON**. O default observado no artefato é `false`, mas default de código não é autoridade do valor efetivamente implantado.

O control flow exato do construtor principal mostra que, quando o valor resolvido é `true`, Gaze pula o bloco que registra/inicializa `GazeRiteRegistry.RITES`, `GazeSpiritRiteEffectTypes.EFFECTS` e `GazeRiteRegistry.init`.

O projeto/anexos atuais não contêm o COMMON config implantado com o valor efetivo. Consequência: os 26 Rites ficam **CONDITIONAL** e não entram no mínimo estrito nesta fase.

## Runes

O progression setup fecha oito rune items provider-owned. Eles têm identidade/progressão, mas continuam fora da métrica semântica porque são item/equipment/passive identities, não actions/spells/rites independentes.

## Compat Iron's

O artefato exato contém um `SpellRegistry` de compat com exatamente um `Supplier<AbstractSpell>`: `SOULWARD_SHIELD`.

`IronsCompat.init` testa `ModList.isLoaded("irons_spellbooks")`; com o provider presente, registra `SpellRegistry` e as demais superfícies de compat. O pack físico satisfaz esse gate:

- `irons_spellbooks-1.21.1-3.16.3.jar`;
- mod id `irons_spellbooks`;
- SHA-1 `017fd8140c477f9ae602cf95594f1c23bef1d6e3`.

Logo Soulward Shield é uma identidade de spell Gaze-owned registrada no conjunto físico atual e contribui **+1 `COUNTED_EXACT`**. Iron's continua authority do cast framework/settlement; Gaze não se torna owner do runtime Iron's.

## Deduplicação e authority

- não reinterpretar os dois Geas como Iron's spells;
- não duplicar os 26 Spirit Rites com uma segunda ritual state machine;
- não contar os oito runes como spells/rites;
- não duplicar spirit/Umbral/resource settlement;
- Soulward Shield é contado uma vez sob Gaze como identidade provider-owned; seu cast/settlement continua no host Iron's;
- qualquer bridge Black Arcana↔Gaze deve aguardar seam provider-native exato e preservar causalidade/deduplicação.

## Disposição semântica Phase 2BJ

- Soulward Shield: **+1 `COUNTED_EXACT`**;
- 26 Spirit Rites: **`CONDITIONAL`** por config efetivo ausente;
- 2 Geas types: **`EXCLUDED`** pela definição da métrica;
- 8 rune items: **`EXCLUDED`** pela definição da métrica.

Mínimo estrito corrente: **1250**. Provider-component closure: **57/100**, sem incremento porque o componente Gaze continua aberto enquanto os 26 Rites dependem do config implantado.

## QA pendente

- valor efetivo implantado de `disableGazeRites`;
- inputs/outputs/custos e resource mutation dos Rites;
- comportamento/settlement numérico dos Geas;
- mechanics/balance do Soulward Shield;
- server authority/idempotência/persistence em runtime completo;
- compatibilidade real com Malum `1.8.2`, Lodestone `1.8.2` e Iron's `3.16.3` no modpack;
- API/hook provider-native seguro para qualquer adapter futuro.

Registry identity/count e gates estruturais acima estão fechados; runtime mechanics que não foram explicitamente provados continuam **NÃO VERIFICADOS / fail-closed**.
