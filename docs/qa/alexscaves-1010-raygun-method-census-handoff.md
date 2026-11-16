# Raygun 1.0.10 — censo dos métodos declarados, descoberta independente

**Escopo:** `SHA_EXACT_1010_RAYGUN_ALL_26_DECLARED_METHODS_DISCOVERY_ONLY`. Análise técnica de interoperabilidade, **não** certificado estático concluído. Não altera a ficha `damage-types/raygun.md`, os índices, a contagem global, hooks ou Stage.

## Identidade

- Modlist física do RPG Skill Tree, item 019: `alexscaves-1.0.10-neoforge+1.21.1.jar`.
- Artefato publisher: **75.279.314 bytes**, SHA-1 `6960b299a39a039ac8a5eb9b07be4ad0e3e0a570`, SHA-256 `36ae0a3cbd028df466a37c671ba2fdf021c060ca1c9c1c32e9f2e95bffae0e7c`.
- Classe: `com/github/alexmodguy/alexscaves/server/item/RaygunItem.class`, SHA-256 `3fc60cb7ff8be2744becf8ac9e524799349996972708845a124f02650bfb344c`, JVM major 65 (Java 21).
- Fonte primária já certificada para o censo seletivo: [EXACT-RAYGUN-CONTROL-1.0.10.json](../wiki/modpack-catalog/providers/✅-alexs-caves-continued/EXACT-RAYGUN-CONTROL-1.0.10.json): 26 métodos declarados, **8** digests completos previamente selados, e 18 métodos selecionados para referências. **18 selecionados não são 18 digests integralmente certificados**.

## Resultado da execução física SHA-exata na PR #1099

- **Publisher SHA-256:** `OK` na CI.
- **Métodos declarados:** `26` corpos JVM completos inventariados; **8 hashes** confrontados com o selo anterior; **18 métodos** receberam digest na descoberta, ainda sem selo individual promovido.
- **Instruções JVM nos 26 corpos:** **1.111**.
- **Branches diretos com destino válido:** **107**.
- **Teste sintético:** **9 testes aprovados**.
- **Índices gerados:** **544 índices**, **2.393 fichas candidatas**, **zero divergências**.
- A saída `DISCOVERY_PASS_NOT_CERTIFIED` preserva a distinção entre o relatório gerado e certificação técnica estática. O resultado não reclassifica o Raygun; as inspeções de alvo e rede ainda têm pendências próprias.

## Nova auditoria e limites

O auditor [alexscaves_1010_raygun_method_census_probe.py](alexscaves_1010_raygun_method_census_probe.py) examina a versão exata usando `javap -c -p -s`, confronta os oito digests prévios, verifica a integridade de todos os destinos de branches diretos e emite o **roster dos 26 métodos** com assinatura JVM, contagem de instruções e branches, offsets de switches e hash SHA-256 do parse. Não exporta implementação compilada, disassembly integral ou código alheio. O método `onUseTick` deve conservar suas 523 instruções previamente registradas.

A [suíte de testes sintéticos](alexscaves_1010_raygun_method_census_probe_test.py) cobre ausência/duplicação de métodos, hashes anteriores alterados, branch inválido e JSON ambíguo. O [workflow](../../.github/workflows/alexscaves-1010-raygun-method-census.yml) valida o JAR exato e arquiva a evidência. **Os hashes dos métodos novos ainda não são selo histórico**: uma execução da CI nesta etapa é descoberta reproduzível, não certificação automática. O relatório precisa passar por revisão causal individual antes de promover Raygun.

## Próxima análise antes de certificado estático

1. Reconciliar caminhos `use`, `onUseTick`, `releaseUsing`, `inventoryTick`, carga/munição, targeting e seleção de efeitos no conjunto integral dos métodos, sem confundir os consumidores dos encantamentos `gamma_ray` e `x_ray`.
2. Vincular a fonte `ACDamageTypes.causeRaygunDamage`, requisições `ACCompat.hurt`, efeito `Irradiated`, filtros de owner/alvo/LOS/claim e aceitação física real. Distinguir intenção de dano, resultado da função e contabilização de Mastery.
3. Fechar separately o boundary C2S `UpdateItemTagMessage`/`UpdatesStackTags`: o inventário de branches não demonstra autenticação do `entityId` por remetente, autorização do `CUSTOM_DATA`, replay protection, ou segurança do payload.
4. Registrar NBT, persistência, sincronização, limites de custos/cooldown, configurações efetivas e comportamento de mods opcionais; na ausência de hook mutador real continuar **fail-closed**.

**Estados:** `static_perk_contract=NOT_CERTIFIED` · `mutating_hook=NOT_VERIFIED` · `physical_qa=NOT_TESTED` · `mutation=NO_MUTATION` · `provider_universe_closed=false`. A subpasta dos encantamentos poderá atingir 51/51 por trabalho independente de X-Ray; isso **não** conclui o Raygun nem o universo do provider.
