# Client and server config specs — Acolyte 1.0.3

**Tipo:** dois specs registrados e vazios no publisher 1.0.3. `ModClientConfigs` e `ModServerConfigs` declaram apenas builder e `SPEC`; ambos constroem o spec sem nenhuma chamada `define`, `defineInRange` ou opção pública de gameplay. Não há knobs client/server a catalogar neste release.

| Escopo | Arquivo registrado | Classe no archive | Evidência |
| --- | --- | --- | --- |
| `CLIENT` | `acolyte-client.toml` | `net/raptorzizi/acolyte/config/ModClientConfigs.class` | `<clinit>()V` PCs 0–19 |
| `SERVER` | `acolyte-server.toml` | `net/raptorzizi/acolyte/config/ModServerConfigs.class` | `<clinit>()V` PCs 0–19 |

O registro está em `net/raptorzizi/acolyte/AcolyteMod.class`, `<init>(Lnet/neoforged/bus/api/IEventBus;Lnet/neoforged/fml/ModContainer;)V`: PCs 101–122 para `SERVER` e 125–146 para `CLIENT`. O spec `COMMON` contém apenas as famílias [placement](village-tavern-placement.md) e [weights](village-tavern-weights.md). As cinco regras de spawning pertencem a [gamerules](../systems/gamerules.md), não a opções inventadas de TOML.

O registro de um nome de arquivo não comprova que o arquivo físico foi gerado ou carregado no pack montado.

## Limite de integração e QA

Acolyte controla este contexto de encontro/configuração; Iron’s mantém a identidade e resolução das magias, scrolls e recompensas de seu namespace. A observação do JAR não valida um ponto mutador para Black Arcana. `mutating_hook=NOT_VERIFIED`; `physical_qa=NOT_TESTED`; `COMPLETE_PERK_READY=false`. Não foi comprovada igualdade de hash com o JAR instalado. Esta ficha resume fatos de interoperabilidade, sem reproduzir implementação, NBT ou assets.

**Base:** publisher `acolyte-1.0.3.jar`, CurseForge file `8098233`, SHA-1 `ad0abc821f3f8a6573ac19a50970fc1bc46b4275`; [contratos binários](../BINARY-CONTRACTS-1.0.3.md) e [manifesto](../ARTIFACT-CATALOG-MANIFEST-1.0.3.json).
