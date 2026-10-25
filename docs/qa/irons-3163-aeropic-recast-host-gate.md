# Host Iron's Spellbooks 3.16.3 — recast ABI para Aeropic

**Data:** 24/10/2026 · **Estado:** 🟡 auditoria da versão host exata em execução; nenhum hook homologado.

## Proveniência e escopo

- Fonte primária da presença: modlist atual em `Gustavaopere/neoforge-rpg-skilltree`, posição **342**, `irons_spellbooks-1.21.1-3.16.3.jar`, Minecraft 1.21.1/NeoForge, Java 21. Wind's `wind_spellbooks-1.0.5.jar` está na posição 571 e possui SHA-1 `8744886899bc245ae147a44baa2b183689cec7da` previamente congelado.
- Distribuição identificada em página de lançamento do autor: Modrinth projeto `s4OWxYQQ`, versão `slKLosTb`, nome de JAR idêntico ao registrado na modlist. Seu metadata JSON **precisa** confirmar projeto, versão, game_version, loader, URL do publisher e tamanho e fornecer SHA-1/SHA-512 completos. O JAR baixado é aceito apenas se seu hash SHA-512 e SHA-1 coincidirem com o metadata oficial.
- Também conferir tamanho exato **13.890.045 bytes** da distribuição **Modrinth slKLosTb**, medido nos metadados oficiais antes de abrir o ZIP. Essa dimensão é um gate separado do hash publicado; não substitui o digest. **Discrepância de origem:** outra listagem da release informa 13.890.046 bytes. Não equiparar distribuição Modrinth, distribuição CurseForge e JAR fisicamente instalado apenas pelo nome; a identidade binária do arquivo local continua condicionada à obtenção de seu próprio SHA.
- Clean-room: não copiar/descompilar implementação ou recursos nem redistribuir o JAR. Publicar apenas JSON de declarações JVM, descritores e proveniência de hashes.

## ABI específica verificada pelo workflow

`docs/qa/irons_3163_aeropic_host_abi.py` exigirá as classes *declaradas* `AbstractSpell`, `PlayerRecasts`, `RecastInstance` e `MagicData` **dentro da versão host exata**, e procurará descritores compilados:

| Declarante no host | Método consumidor relevante | Descritor exigido |
|---|---|---|
| `AbstractSpell` | `getRecastCount` | `(ILnet/minecraft/world/entity/LivingEntity;)I` |
| `PlayerRecasts` | `addRecast` | `(Lio/redspace/ironsspellbooks/capabilities/magic/RecastInstance;Lio/redspace/ironsspellbooks/api/magic/MagicData;)Z` |
| `PlayerRecasts` | `hasRecastForSpell` | `(Ljava/lang/String;)Z` |
| `PlayerRecasts` | `decrementRecastCount` | `(Ljava/lang/String;)V` |
| `RecastInstance` | `<init>` | `(Ljava/lang/String;IIILio/redspace/ironsspellbooks/api/spells/CastSource;Lio/redspace/ironsspellbooks/api/spells/ICastDataSerializable;)V` |

Essas são as **referências simbólicas Wind's já observadas no JAR 1.0.5** (PRs #887 e #890), não afirmações ainda provadas sobre a implementação do host. Se a versão host não declarar os métodos ou tiver descriptors diferentes, o workflow falha fechado e a divergência deve ser catalogada; não remover testes apenas para obter PASS.

## Limites

**Uma assinatura ABI compatível nunca comprova que o `AeropicEffect` possua um receiver real de `AeropicSpell`, que o override seja executado ou que o retorno alimenta `PlayerRecasts`.** O Iron's permanece autoridade do cast/recast, Wind's dos seus efeitos, Black Arcana apenas do seu runtime; RPG Skill Tree apenas progressão/perks/gates por contrato real.

Mesmo se a ABI exata do host for verificada, ficam explicitamente `aeropic_effect_receiver = NOT_PROVEN`, `aeropic_override_execution = NOT_PROVEN`, `recast_flow_to_host_state = NOT_PROVEN`, `safe_black_arcana_or_rpg_mutator = NOT_PROVEN` e `gameplay_validation = NOT_TESTED`. Perks mutadoras ⛔ `SEM_HOOK_SEGURO`.

## Testes e critérios

- Quinze fixtures sintéticas (hashes, metadata, identity, URLs, tamanho, classes/métodos/descritores JVM, métodos `static`/`abstract` não admissíveis).
- GitHub Actions Java 21 executa download **do distribuidor identificado**, verifica SHA-512 e SHA-1 emitidos pelo metadata da versão, inspeciona ABI em `javap -s -p` e publica somente JSON `host-recast-abi.json`. Requer revisão do JSON no fim; pode ser necessário *pin* adicional do hash ao primeiro resultado antes do merge.
- CI geral `verify` e `stage05_qa_companion_smoke` no HEAD final; 0 behind, diff e SHA antes de merge. Sem inventar sucesso nem promover Stages.

**Preservar:** Wind's 7/7 magias, nove getters selecionados, campanha de identidade binária 38/39, catálogo global ≥1.856 e denominador —%; Stage 06.05 🟡 e validação física Stage 09 pendente.
