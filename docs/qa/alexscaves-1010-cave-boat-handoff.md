# Alex's Caves Continued 1.0.10 — CaveBoatItem, protocolo de auditoria

**Estado:** 🟡 em implementação / ⚠️ parcial, descoberta do JAR SHA-exato sem certificação individual. `NO_MUTATION`; `mutating_hook=NOT_VERIFIED`; `physical_qa=NOT_TESTED`; `provider_universe_closed=false`. Não promover hooks, integração ou QA.

**Fonte:** `alexscaves-1.0.10-neoforge+1.21.1.jar`, CurseForge file 8856293, Minecraft 1.21.1 / NeoForge, Java 21; bytes 75.279.314; SHA-1 `6960b299a39a039ac8a5eb9b07be4ad0e3e0a570`; SHA-256 `36ae0a3cbd028df466a37c671ba2fdf021c060ca1c9c1c32e9f2e95bffae0e7c`. O sibling registra 1.0.10 na modlist, sem novo inventário direto de instalação.

## Prova anterior reaproveitada

A [descoberta original](../wiki/modpack-catalog/providers/✅-alexs-caves-continued/EXACT-BURROWING-CAVE-MAP-DISCOVERY-1.0.10.md) e [ACItemRegistry](../wiki/modpack-catalog/providers/✅-alexs-caves-continued/systems/item-registry.md) registram a classe `CaveBoatItem` class SHA-256 `92fc0840e49f71306bbcafbd3e5f4f5814acbf87846846430007310a2577c18d`, três corpos e quatro factories: `lambda$static$25` (Pewen sem baú), `$26` (Pewen com baú), `$145` (Thornwood sem baú), `$146` (Thornwood com baú). A entidade é `AlexsCavesBoatEntity` ou `AlexsCavesChestBoatEntity`, conforme `hasChest`.

`CaveBoatItem.use` recebe a stack da mão, solicita raycast `ClipContext.Fluid.ANY`, retorna PASS em MISS ou quando uma AABB de entidade próxima contém o olho do jogador; o vetor de seleção de entidades usa a direção de visão escalada por **5** e AABB inflada em **1**, sem provar que 5 seja o alcance do raycast. Em hit de bloco cria o barco no hit, aplica yaw do jogador, falha em `Level.noCollision=false`; no servidor solicita `addFreshEntity`, **descarta o Boolean**, solicita `ENTITY_PLACE` e depois `shrink(1)` se não `instabuild`. Não provar spawn aceito ou world safety só com a solicitação.

## Próxima evidência

O workflow captura os corpos reais do item, das duas entidades concretas, da enum `AlexsCavesBoat$Type` e do helper `ACCompat` por `javap -v -c -p -s` na versão SHA-exata. O artefato CI é temporário; o repositório receberá hashes duráveis, fichas individuais para as quatro identidades e avaliação da cadeia de consumidores antes de qualquer certificação.

**Limites:** aquisição/receitas, evolução das entidades após uso, baú/inventário/drops, persistência, controles, colisão, dimensões, sons, targeting e segurança externa ainda devem ser verificados. Não contar itens de transporte como raízes mágicas independentes.
