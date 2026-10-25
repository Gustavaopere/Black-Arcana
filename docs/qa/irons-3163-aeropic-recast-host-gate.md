# Host Iron's Spellbooks 3.16.3 — recast ABI para Aeropic

**Data:** 24/10/2026 · **Estado:** ✅ ABI da distribuição Modrinth verificada; ⚠️ igualdade bit a bit com JAR local ainda não comprovada, sem hook homologado.

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

- Dezesseis fixtures sintéticas de seleção ABI, além de doze fixtures independentes de SHA/contrato (hashes, metadata, identity, URLs, tamanho, classes/métodos/descritores JVM, métodos `static`/`abstract` não admissíveis).
- GitHub Actions Java 21 executa download **do distribuidor identificado**, verifica SHA-512 e SHA-1 emitidos pelo metadata da versão, inspeciona ABI em `javap -s -p` e publica somente JSON `host-recast-abi.json`. Requer revisão do JSON no fim; pode ser necessário *pin* adicional do hash ao primeiro resultado antes do merge.
- CI geral `verify` e `stage05_qa_companion_smoke` no HEAD final; 0 behind, diff e SHA antes de merge. Sem inventar sucesso nem promover Stages.

**Preservar:** Wind's 7/7 magias, nove getters selecionados, campanha de identidade binária 38/39, catálogo global ≥1.856 e denominador —%; Stage 06.05 🟡 e validação física Stage 09 pendente.

## Evidência efetivamente coletada — distribuição oficial `slKLosTb`

Fonte de primeira ordem: [GitHub Actions Iron's host ABI #40146984360](https://github.com/Gustavaopere/Black-Arcana/actions/runs/40146984360), `SUCCESS`; `host-recast-abi.json` extraído e inspecionado. Metadados de projeto/release/arquivo, tamanho, SHA-1 e SHA-512 foram comparados com **o arquivo realmente baixado**, sem executar código do provider.

- **Release e ambiente publicados:** `s4OWxYQQ` / `slKLosTb`, `irons_spellbooks-1.21.1-3.16.3.jar`, NeoForge 1.21.1; tamanho **13.890.045 bytes**.
- **SHA-1 (distribuição Modrinth):** `e8832385c01db56b9fcb19c48fcedc76a3a70d92`.
- **SHA-512 (distribuição Modrinth):** `fd782f98c6c59b193c4832f33775291d2a7e639e1e23dd47510bfb494d99d182bec1253566b9394f96c733a0d0108be34bd729614b82dc29e55e096fdeb96f5b`.

O artefato confirmou **5/5 assinaturas ABI referenciadas pelo Wind**: `AbstractSpell.getRecastCount`, `PlayerRecasts.addRecast`, `hasRecastForSpell(String)`, `decrementRecastCount(String)` e `RecastInstance` construtor de seis argumentos. Todas foram encontradas como declarações não `abstract`/não `static` quando aplicável. `MagicData` foi localizada no arquivo, mas não foi homologado novo método nessa classe. A sobrecarga de `hasRecastForSpell` exigiu filtragem pelo **descritor JVM integral**, não pelo nome isolado.

### Atenção à identidade física

**⚠️ Uma listagem CurseForge-adjacente informa 13.890.046 bytes para arquivo com o mesmo nome**, enquanto o metadata e os bytes baixados da distribuição Modrinth têm 13.890.045. Esta campanha valida a **distribuição Modrinth específica com hash congelado**, não demonstra que o modpack já contenha exatamente esses mesmos bytes. Não confundir coincidência de versão, nome ou ABI com identidade binária local. Para promovê-la a 'JAR instalado exato', obter o SHA-1/SHA-512 do arquivo físico e confrontar.

### Conclusões admitidas

- ✅ `ABI do host publicada 3.16.3` é compatível com os símbolos que `AeropicEffect` referencia no JAR Wind's 1.0.5.
- ⚠️ `AeropicEffect` continua com **dois** `invokevirtual AbstractSpell.getRecastCount` no provider Wind, mas o receptor no operand stack não foi traçado; override executado `NOT_PROVEN`.
- ⚠️ Não houve prova de `getRecastCount → RecastInstance → PlayerRecasts` nem de limites, recargas ou persistência reais.
- ⛔ `SEM_HOOK_SEGURO`: não adicionar listener/ledger paralelo ou override à API host sem contrato real e QA provider-native.

### Contract SHA-congelado

`docs/qa/irons_3163_aeropic_host_contract.py` compara independentemente o SHA-1/SHA-512 e os cinco descritores do JSON recém-gerado com os valores congelados acima. Doze fixtures de mutação rejeitam derivação indevida de receiver, override, consumo do retorno, hooks e release drift. O workflow novo executa os validadores antes e depois da inspeção do host.
