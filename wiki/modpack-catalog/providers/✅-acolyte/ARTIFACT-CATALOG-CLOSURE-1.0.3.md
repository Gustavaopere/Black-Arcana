# Acolyte 1.0.3 — fechamento documental do publisher

```text
CATALOG_PUBLISHER_ARTIFACT_SCOPE_ONLY
version=1.0.3
artifact_sha1=ad0abc821f3f8a6573ac19a50970fc1bc46b4275
artifact_sha256=73fe745bbb0016fbc00af9ba14c0ecfe0a1d8a7d72a7892557739182b3486256
artifact_size_bytes=621837
installed_artifact_identity=NOT_VERIFIED
physical_qa=NOT_TESTED
mutating_hook=NOT_VERIFIED
```

## Universo documentado

O [manifesto](ARTIFACT-CATALOG-MANIFEST-1.0.3.json) relaciona **todos os 359 arquivos** do publisher exato a fichas ou a suporte justificado, incluindo **93 classes**. O ZIP tem 469 entradas: 110 são diretórios. Os hashes fixam o conteúdo dos arquivos e das **74 fichas individuais**; os diretórios não aumentam o universo de objetos.

| Frente | Fichas | Escopo |
|---|---:|---|
| Entidades | 10 | Oito registros de NPC e duas bases compartilhadas, sem fabricar registros `human`/`demon` |
| Goals | 5 | Casting single-use, ranged, melee, voo e ordem stay |
| Perfis | 6 | Seis chaves consumidas, 50 entradas com stats/pesos/equipamento/spells e limites de biome/skin |
| Itens | 22 | 21 IDs de equipamento/consumíveis e uma ficha com os dez eggs e seu dispatch |
| Economia | 12 | Factories de ofertas, pools, moedas, usos, custos e chamadas de host |
| Encontros | 12 | 14 marcadores com BlockItems pareados, spawning, 18 superfícies configuradas/tavernas, pools e loot |
| Sistemas | 4 | Recrutamento, protocolo/menu, carregamento de archetypes e cinco gamerules |
| Configuração | 3 | Placement/weights de tavernas e specs client/server vazias, sem inventar knobs |

As fichas desmembram o inventário agregado anterior. Não são 74 novas magias: **0 spells standalone próprios** continuam registrados sob Acolyte. As [31 referências explícitas Iron's](EXACT-1.0.3-HOST-SPELL-REFERENCES.md) e seleções dinâmicas preservam a propriedade semântica do host.

Agrupar variantes sob um contrato não elimina identidades: todos os 31 itens diretos, 14 blocos/BlockItems, oito EntityTypes, seis chaves de perfis e 18 superfícies de encontro são mantidos nos rosters/tabelas. Dez eggs não criam dez EntityTypes; os dois eggs genéricos despacham os papéis existentes. Os 28 NBT incluem apoio, ruas e casas e não são contados como 28 estruturas registradas.

## Suporte com disposição explícita

| Grupo no manifesto | Justificativa |
|---|---|
| `AGGREGATE:bootstrap-and-metadata` | Inicialização, registro de config/registros/tela, aba criativa e metadados do JAR são suporte aos consumidores. Suas relações estão em [contratos binários](BINARY-CONTRACTS-1.0.3.md); não constituem novos casts ou perks. |
| `AGGREGATE:localization` | A localização nomeia as superfícies, inclusive nomes legados sem registro atual. Não é autoridade para inventar itens/spells. |
| `AGGREGATE:auxiliary-presentation` | Modelos legados `archer_helmet`, `black_wizard_*`, `*_quiver` e textura de fallback permanecem como arquivos, sem IDs de item extras deduzidos dos nomes. Não se presume ausência de referências futuras por datapack. |

Modelos/renderers/assets efetivamente associados a entidades e equipamentos são mapeados também às fichas correspondentes. `archetype/exemple.json`, specs vazias, menu/material/tipo de BlockEntity e access transformer têm consumidores ou disposições documentados. Não há classe ou arquivo desconhecido descartado por um catch-all de conteúdo executável.

## Verificação e limite da conclusão

O [auditor reproduzível](../../../../docs/qa/acolyte_103_artifact_catalog_audit.py) verifica o hash/tamanho pinado do JAR e a correspondência exata dos caminhos, bytes e hashes dos arquivos com o manifesto, incluindo contagem de classes e diretórios. A consistência dos índices verifica as fichas/hashes/referências e o prefixo alfabético. Esses checks não executam NPCs, casting, trades ou recrutamento.

A identidade física documentada permanece release-bounded: não existe hash independente do JAR instalado no material consultado. Também não foi identificada fonte oficial vinculada pelos publishers. [Proveniência completa](BINARY-CONTRACTS-1.0.3.md).

Descobertas como validações locais ausentes no payload, armor/follow range distintos por papel, composição de RNG de ofertas, consumo de item e referências a recursos ausentes estão delimitadas no binário/dados publicados. Não são bugs/exploits reproduzidos no modpack nem autorização para contornar políticas de proteção.

## Gates pendentes

- **Certificação técnica individual para perks: 0/74.** Nenhuma entrada de `PERK-READY-CERTIFICATIONS.json` ou Stage é promovida.
- **Identidade instalada e host:** confrontar o JAR real e testar NeoForge/Iron's/Curios e os outros consumidores do pack. Referências de API não provam compatibilidade.
- **Hooks e autoridade:** nenhum mutador de range/alvo/tipo de dano/tempo/hitbox/custo foi homologado; assinatura, campo ou descriptor existente não é um hook seguro.
- **QA física:** boot cliente/dedicado, dano/casting, ownership, distância/LOS, morte/clone, persistência, reload, economia/loot, proteções e multiplayer continuam pendentes.

O índice pode encerrar esta **documentação do artefato publisher** e apontar **Aeromancy Additions** como próximo na ordem alfabética. Isso não homologa Acolyte integralmente para perks nem muda o runtime de Black Arcana, Enshrouded ou RPG Skill Tree.
