# Spawn eggs — dez registros de suporte

**Release auditada:** Acolyte 1.0.3, publisher file `8098233`; SHA-256 `73fe745bbb0016fbc00af9ba14c0ecfe0a1d8a7d72a7892557739182b3486256`.
**Estado:** documentação de contrato binário; mutação `NOT_VERIFIED`; pack físico `NOT_TESTED`; igualdade do hash instalado não comprovada; certificações **0**.

Fonte: [contratos e proveniência](../BINARY-CONTRACTS-1.0.3.md) e [manifesto](../ARTIFACT-CATALOG-MANIFEST-1.0.3.json). Referências PC indicam offsets de método no publisher, não código reproduzido. O conflito publisher ARR / metadado TOML MIT permanece aberto; só fatos de interoperabilidade são retidos.

## Universo de registros e destinos

Esta ficha agrega **10** itens de spawn administrativos. Oito usam o mesmo `DeferredSpawnEggItem` NeoForge; dois são itens customizados de spawn aleatório. Não representam spells ou dez habilidades próprias.

| Item `acolyte:` | Destino/ação |
|---|---|
| `demon_mage_spawn_egg` | `ModEntityRegistry.DEMON_MAGE` |
| `demon_warrior_spawn_egg` | `DEMON_WARRIOR` |
| `demon_archer_spawn_egg` | `DEMON_ARCHER` |
| `demon_spawn_egg` | `DemonSpawner.spawnRandom` |
| `human_mage_spawn_egg` | `HUMAN_MAGE` |
| `human_warrior_spawn_egg` | `HUMAN_WARRIOR` |
| `human_archer_spawn_egg` | `HUMAN_ARCHER` |
| `human_spawn_egg` | `HumanSpawner.spawnRandom` |
| `horn_merchant_spawn_egg` | `HORN_MERCHANT` |
| `lieutenant_spawn_egg` | `LIEUTENANT` |

## Trigger, custo e ownership

Os oito ovos convencionais recebem `ItemPropertiesHelper.material().stacksTo(64)` e a entidade supplier; targeting, consumo, checagens e comportamento em spawner/dispenser são herdados de NeoForge, não certificados por esta auditoria do provider.

`demon_spawn_egg` e `human_spawn_egg` são `ModItemsRegistry$1` e `$2`, respectivamente, ambos subclasses diretas de `Item`, não `DeferredSpawnEggItem`. `useOn` usa a posição clicada deslocada pela face; no `ServerLevel`, chama o spawner aleatório da família e reduz a stack em 1 se `getPlayer().isCreative()` for falso. O resultado do spawn é ignorado antes do débito: uma falha pode consumir o item. `getPlayer()` é dereferenciado sem guarda de null; uso automatizado não é seguro por inferência. Retorna SUCCESS no servidor e sidedSuccess no caminho restante. Não transfere owner, não recruta nem debita mana/cooldown local.

Não há persistência de item/owner customizada nesses dois itens. Distribuição por arquétipo/bioma é responsabilidade dos spawners e loadouts, não uma lista fixa inventada pelo ovo.

## Evidência reproduzível

- `ModItemsRegistry.<clinit>` PC 356–526: dez registros; `lambda$static$21…30`: suppliers.
- `ModItemsRegistry$1.useOn`, `$2.useOn` PC 0–67: alvo de bloco adjacente, lado, spawn, consumo e null-player boundary.
- Suppliers convencionais PC 0–22: entidades e stack de 64; suppliers `$24`/`$28` PC 0–14: criação dos dois itens customizados.

## Boundary de integração e validação

Acolyte possui o item e sua política local; Iron's possui atributos, efeitos, recipientes e magias do host; Minecraft/NeoForge possui inventário, equipamento e liquidação vanilla. Não há hook mutador homologado. Nomes de métodos/registries são candidatos de observação, sem garantia de API estável. Perks não devem alterar mana, repetir consumo, aplicar atributos em outro slot ou liquidar recompensas por esta ficha.

`NOT_TESTED`: conferir o hash instalado, uso/equipamento no servidor dedicado, criativo/sobrevivência, troca de slot, relog, morte e multiplayer; confirmar uma única aplicação e um único consumo no pack real. Ausência de cooldown explícito na classe não certifica ausência de cooldown herdado/do host.
