# Demon template pools — Acolyte 1.0.3

**Tipo:** quatro template pools auxiliares, sem configuração `worldgen/structure` própria correspondente. São referências de conteúdo, não quatro novas estruturas do total 18.

| ID do pool | Caminho exato no archive | Localizações dos elementos, com peso |
| --- | --- | --- |
| `acolyte:demon_archer` | `data/acolyte/worldgen/template_pool/demon_archer.json` | `acolyte:watchtower/demon_archer`, peso 1 |
| `acolyte:demon_mage` | `data/acolyte/worldgen/template_pool/demon_mage.json` | `acolyte:watchtower/demon_mage`, peso 1 |
| `acolyte:demon_warrior` | `data/acolyte/worldgen/template_pool/demon_warrior.json` | `acolyte:watchtower/demon_warrior`, peso 1 |
| `acolyte:demon_random` | `data/acolyte/worldgen/template_pool/demon_random.json` | `acolyte:watchtower/demon_archer`, `acolyte:watchtower/demon_warrior`, `acolyte:watchtower/demon_mage`, pesos 1/1/1 |

Todos declaram elemento `minecraft:single_pool_element`, projeção `rigid`, processadores `minecraft:empty` e fallback `minecraft:empty`. Entretanto os três caminhos `data/acolyte/structure/watchtower/demon_{archer,warrior,mage}.nbt` **não existem no publisher auditado**; as 28 entradas NBT existentes não incluem esses nomes. Não foi demonstrada uma ligação de jigsaw dos 28 templates publicados a esses quatro pools. A presença de um pool não comprova que ele seja alcançável, nem que produza um encontro no pack. Datapacks podem suprir recursos, mas isso não foi testado.

**Evidência exata:** quatro recursos da tabela e ausência dos três templates no inventário integral do archive. O consumidor previsto é o sistema de template pools de Minecraft; não há método mutador Acolyte ou spell ID próprio nesta superfície. Tratar como referência empacotada com resolução/reachability `NOT_VERIFIED`.

## Limite de integração e QA

Acolyte controla este contexto de encontro/configuração; Iron’s mantém a identidade e resolução das magias, scrolls e recompensas de seu namespace. A observação do JAR não valida um ponto mutador para Black Arcana. `mutating_hook=NOT_VERIFIED`; `physical_qa=NOT_TESTED`; `COMPLETE_PERK_READY=false`. Não foi comprovada igualdade de hash com o JAR instalado. Esta ficha resume fatos de interoperabilidade, sem reproduzir implementação, NBT ou assets.

**Base:** publisher `acolyte-1.0.3.jar`, CurseForge file `8098233`, SHA-1 `ad0abc821f3f8a6573ac19a50970fc1bc46b4275`; [contratos binários](../BINARY-CONTRACTS-1.0.3.md) e [manifesto](../ARTIFACT-CATALOG-MANIFEST-1.0.3.json).
