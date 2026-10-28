# Ace's Spell Utils — fechamento do catálogo da versão-fonte

```text
CATALOG_SOURCE_SCOPE_ONLY
AceTheEldritchKing/Aces_Spell_Utils@a0b2f4c2fcfa938c8e47239279c77c2ef82647ac
version=1.2.7.2-1.21.1
artifact_sha1=8cbcd535a0b19bef49504c0b5ecafcbcd1cb1cca
physical_qa=NOT_TESTED
mutating_hook=NOT_VERIFIED
```

## Escopo encerrado

O fechamento cobre o catálogo dos contratos integráveis encontrados na revisão acima: **245 arquivos rastreados, incluindo 132 arquivos Java**, seus registros, exemplos e consumidores. O [manifesto](SOURCE-CATALOG-MANIFEST-1.2.7.2.json) relaciona cada caminho a fichas individuais ou a suporte justificado, fixa o hash de cada arquivo de origem e de cada ficha, e permite detectar fichas novas ou alteradas antes de reutilizar o fechamento. Não é uma enumeração de todos os providers que possam consumir essa biblioteca.

São **118 fichas individuais**: 19 atributos, três escolas, três tipos de dano, 14 tags, oito raridades, cinco configurações, um attachment, uma partícula, 27 itens de exemplo, um material de armadura, oito payloads S2C, dois mixins, cinco contratos visuais e 21 contratos de sistemas/helpers. Há **0 standalone spell registrations**. Famílias de API, exemplos, animações e payloads não são somados como magias.

As 115 fichas integradas até a PR #940 foram preservadas. Esta conclusão acrescenta os contratos antes ausentes de [loot bag](systems/loot-bag-helper.md), [atributos e container de geo armor](systems/geo-armor-attribute-helper.md) e [rendering emissivo de armadura](systems/emissive-geo-armor-rendering.md), e aprofunda consumidores existentes onde faltavam fórmulas, parâmetros ou limites de ciclo de vida. [Índice com as duas medidas](INDEX.md).

## Disposições de suporte

| Grupo do manifesto | Disposição e evidência |
|---|---|
| `AGGREGATE:examples-and-development-content` | A aba `asu_item_tabs` só é registrada fora de produção; os 27 itens e o material são registrados sempre e têm fichas próprias. Modelos, tiers e código demonstrativo são associados aos helpers e exemplos consumidores. Não excluir procs executáveis: dois handlers de livros e um de sheath usam Comet. [Exemplos e rede](NETWORK-MIXINS-AND-EXAMPLES.md), [registros](REGISTRIES-AND-ATTRIBUTES.md), [livros](systems/passive-ability-spellbooks.md), [curios](systems/passive-cooldown-curios.md). |
| `AGGREGATE:provider-contract-metadata` | Wiring de registros, declaração opcional de protocolo `4.0.0`, declaração de mixins, traduções e metadados de namespace não criam novas habilidades. Seus registros e consumidores têm fichas em tags, raridades, config, payloads e mixins. [Mapa de API](API-AND-RUNTIME-SURFACES.md), [proveniência](EVIDENCE-AND-PROVENANCE.md). |
| `AGGREGATE:bootstrap-build-and-publisher-metadata` | Entrypoint, Gradle/wrapper, workflow, README e arquivos de template estabelecem inicialização e proveniência. O manifesto preserva nomes e hashes; a dependência efetiva Iron's é `3.16.2`, não a propriedade obsoleta `3.11.0`. [Proveniência](EVIDENCE-AND-PROVENANCE.md). |
| `AGGREGATE:auxiliary-artwork` | Modelos, texturas e pack artwork, incluindo nomes de affinity-ring, scroll e test-boss, não são registros de entidades, itens ou spells. Os caminhos são retidos individualmente; recursos de VFX/armadura efetivamente usados são associados aos contratos consumidores. Nomes de assets, isoladamente, não comprovam comportamento integrável. |

As disposições explicam suporte, não ocultam classes desconhecidas. A revisão relaciona todas as classes Java; um novo caminho deve ser classificado explicitamente antes de renovar o manifesto.

## Evidência binária delimitada

O JAR do publisher, arquivo `8789930`, corresponde ao SHA-1 registrado acima e possui SHA-256 `da3ec5f0201ff87d52df0d952b8ed379e77b8a5d98666558ec4bea0805fe97be`. A comparação encontrou os mesmos 132 nomes de classes externas da fonte, sem ausências ou nomes extras, e 150 classfiles incluindo internos. A declaração JSON dos mixins é semanticamente igual. [Identidade e limites](EVIDENCE-AND-PROVENANCE.md).

Isso não certifica corpos de métodos, constantes, ordem de eventos, conjunto completo de recursos ou compilação reproduzível. As fichas descrevem semântica da fonte pinada; riscos como seleção de alvo, cleanup de domínio, uso da mão na loot bag e sincronização de mana não são bugs reproduzidos em jogo.

## Gates que permanecem abertos

| Gate | Estado / próximo requisito |
|---|---|
| Documentação da versão-fonte | Fechada no universo e nos hashes declarados; mudanças invalidam o fechamento até revisão. |
| Certificação estática individual para perks | `0/118`; o ledger de certificações não é promovido por esta conclusão. |
| Hook mutador / integração executável | `NOT_VERIFIED`; requer consumidor real, contrato de autoridade e proteção contra processamento duplicado. |
| Compatibilidade de host | Fonte NeoForge `21.1.230` / Iron's `3.16.2`; BA compile/dev `21.1.248`; ledger físico `21.1.250` / Iron's `3.16.3`. Assinaturas, mixins e fluxo efetivos ainda precisam de validação. |
| QA física do provider | `NOT_TESTED`; servidor/cliente com Ace's e host reais, multiplayer, morte/clone, targeting, reload, VFX e valores de recurso precisam de casos observados. CI do Black Arcana não substitui esses testes. |

O índice alfabético pode registrar este **fechamento documental da versão-fonte** e indicar Acolyte como próxima catalogação. Isso não resolve os gates acima nem altera `COMPLETE_PERK_READY`, Stage ou runtime de Black Arcana, Enshrouded ou RPG Skill Tree.
