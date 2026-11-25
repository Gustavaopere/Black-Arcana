# Marine Snow, ModFishBucketItem e Moth Dust — descoberta binária 1.0.10

**DISCOVERY_ONLY / NO_MUTATION / NOT_CERTIFIED / NOT_TESTED.** Nenhuma nova ficha ou raiz semântica contabilizada; integração e universo integral do provider em aberto.

Base canônica Black Arcana `651d9b25a0d994d413ad1c03fb883c4afc93f4d6`. A modlist sibling registra `alexscaves-1.0.10-neoforge+1.21.1.jar`, entrada física #19, mod ID `alexscaves`, SHA-1 `6960b299a39a039ac8a5eb9b07be4ad0e3e0a570`. A sonda reutiliza o pin SHA-256 `36ae0a3cbd028df466a37c671ba2fdf021c060ca1c9c1c32e9f2e95bffae0e7c` e o censo de 1.555 classfiles. O JAR não foi inspecionado nesta revisão: primeira execução e interpretação pendentes.

## Reconciliação alfabética

No [inventário](INTEGRATION-SCOPE-INVENTORY-1.0.10.json), MagicConchItem segue LimestoneSpearItem. A [ficha Magic Conch](actions/magic-conch-summon-deep-ones.md) já consta como certificada no ledger canônico, cobre charge, spawn, quantidade, duração, reputação, custos, autoria e persistência. Seu contrato não é contado novamente. Charting Call, Lasting Morale e Taxing Bellow são modificadores já documentados, não novos casts. A ausência de hook seguro mantém mutação bloqueada.

As três classes seguintes são MarineSnowItem, ModFishBucketItem e MothDustItem. A descoberta é independente da PR #1229 (que contém as três fichas parciais anteriores). Nenhum índice ou ledger compartilhado é alterado nesta fase.

## Identidades documentadas no registro técnico existente

Fonte: [Item Registry](systems/item-registry.md). A sonda requer os oito Code SHA-256 abaixo, a classe ACItemRegistry previamente selada e a instrução new tipada de cada factory. A presença de uma factory não demonstra habilidade, efeito, parâmetros ou elegibilidade para perks.

| Classe | Resource ID | Factory | Code SHA-256 |
|---|---|---|---|
| `MarineSnowItem` | `alexscaves:marine_snow` | `lambda$static$90` | `d385d5b08e71c8ae683c30c5f0402acecbcb5ec0b6f13d0e33c25bbf57cdf7ba` |
| `ModFishBucketItem` | `alexscaves:gossamer_worm_bucket` | `lambda$static$92` | `6ee50396f6047acee481212ad62d3c4cbd750e9f550376efcf754d6068cb5eae` |
| `ModFishBucketItem` | `alexscaves:lanternfish_bucket` | `lambda$static$80` | `890937e2190ba7e244b6f1dc3c35740b4af2802b9096780d845497837ba47581` |
| `ModFishBucketItem` | `alexscaves:radgill_bucket` | `lambda$static$55` | `d7729687750c047d200bb210236a4297426cad16d43e8e27a3403f58ca9bfc4b` |
| `ModFishBucketItem` | `alexscaves:sea_pig_bucket` | `lambda$static$88` | `fc3ae35eecabc8a02f3f04ab286e47880a5b1f2742409b6101bd83a9ebca3072` |
| `ModFishBucketItem` | `alexscaves:trilocaris_bucket` | `lambda$static$28` | `453b73b31f0029d7869d40793ba0788953f6c7cfe17fef1b1958c8c9bf282087` |
| `ModFishBucketItem` | `alexscaves:tripodfish_bucket` | `lambda$static$84` | `2afb9a0374d54244d796e67cdb0c0e9dd5393eab63049456bf109f686dadeb0b` |
| `MothDustItem` | `alexscaves:moth_dust` | `lambda$static$122` | `20fac1a05d60f7390148c4a90e14a151511ba918fb57388a09b978b7dbcd4948` |

## Coleta e critérios

A [sonda](../../../../docs/qa/alexscaves_1010_marine_fish_moth_probe.py) reutiliza o parser e a projeção read-only já empregados no projeto. Verifica a identidade e o roster do publisher, todas as declarações próprias dos três alvos, hashes de Code, referências tipadas, implementadores/subclasses diretos e janelas dos callsites. O recorte de JSON por nome é limitado, não prova completude de recursos. O [workflow](../../../../.github/workflows/alexscaves-1010-marine-fish-moth.yml) requer dois relatórios byte-idênticos; o hash e o tamanho ainda não são selados porque o primeiro resultado não foi observado.

- Marine Snow: investigar ativação, alvo, consumidores, custos, recursos e eventual relação causal com entidades ou efeitos.
- ModFishBucketItem: separar as seis identidades registradas, comportamento próprio e herdado; determinar se são objetos relevantes ao catálogo ou apenas transporte de entidades. Não presumir summons mágicos; investigar captura, soltura, ownership, descarte, dispenser e world safety conforme o bytecode.
- Moth Dust: identificar callbacks e consumidores efetivos, sem presumir efeito a partir do nome.

Após o resultado, reconciliar com #1229, classificar cada identidade, ampliar a auditoria downstream quando necessário e criar fichas individuais apenas para objetos relevantes. Nenhuma alteração de runtime, índices, contadores, hooks, QA física ou Stage.

## Resultado observado — primeiro replay exato

[Run 45653331096 / job 139343330423](https://github.com/Gustavaopere/Black-Arcana/actions/runs/45653331096/job/139343330423), HEAD `b5bc7f2d5f70fe485036dc7e79285fa96ae7867b`: oito checks, 25 declarações executáveis (17 próprias e oito factories), cinco owners com referência tipada, 13 JSONs no recorte de filename; duas saídas byte-idênticas, 335.054 bytes, SHA-256 `a9afad89d2771265dfbb4f86c2981bba8d204943e053d4364af82af69c5a7f41`. A revisão sela tamanho e digest. A nova HEAD precisa repetir a coleta. A main `f3f48196a0853fe51cefd0dd5ba462b354773dc2` incorporou #1229. MagicConchItem mapeado ao contrato existente; 51/81 classes do roster histórico com disposição documentada, 30 restantes neste checkpoint, não equivalentes a fichas certificadas. SweetishFishBucketItem é subclass direta, fora da coleta de corpos próprios.

### Fichas individuais parciais

- [Gossamer Worm Bucket](items/gossamer-worm-bucket.md)
- [Lanternfish Bucket](items/lanternfish-bucket.md)
- [Marine Snow](items/marine-snow.md)
- [Moth Dust](items/moth-dust.md)
- [Radgill Bucket](items/radgill-bucket.md)
- [Sea Pig Bucket](items/sea-pig-bucket.md)
- [Trilocaris Bucket](items/trilocaris-bucket.md)
- [Tripodfish Bucket](items/tripodfish-bucket.md)

Nenhuma promoção: 137/149 no recorte proposto, 276/2461 globais, raízes inalteradas. Seis baldes são objetos técnicos de integração, não summons mágicos; elegibilidade final depende de prova downstream. Próxima classe: OccultGemItem, sujeita a reconciliação.
