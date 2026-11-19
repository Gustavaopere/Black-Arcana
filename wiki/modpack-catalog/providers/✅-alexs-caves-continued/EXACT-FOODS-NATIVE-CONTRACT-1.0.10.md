# ACFoods — contrato técnico estático dos presets 1.0.10

**Escopo certificado:** `STATIC_TECHNICAL_CATALOG_ONLY` / `SHA_EXACT_BINARY_BEHAVIOR` dos 63 presets de `ACFoods`, da construção de seus 46 suppliers e dos sites imediatos de leitura no publisher SHA-exato. Não é certificado dos alimentos completos, de execução de registros, dos efeitos downstream ou do runtime instalado. `mutating_hook=NOT_VERIFIED`, `runtime=NOT_VERIFIED`, `physical_qa=NOT_TESTED`, `perk_certification=NOT_CERTIFIED`, `NO_MUTATION`, provider `OPEN`, **+0 raízes mágicas**.

[Ficha e tabela completa dos 63 presets](systems/foods.md) · [Selo do contrato](EXACT-FOODS-NATIVE-CONTRACT-1.0.10.json) · [Descoberta histórica preservada](EXACT-FOODS-DISCOVERY-1.0.10.json) · [Contrato do builder](EXACT-FOOD-BUILDER-CONTRACT-1.0.10.md).

## Sete eixos de evidência

| Eixo | Evidência local e alcance |
|---|---|
| `identity` | Publisher 1.0.10, Minecraft 1.21.1, Java 21; SHA-1 `6960b299a39a039ac8a5eb9b07be4ad0e3e0a570`, SHA-256 `36ae0a3cbd028df466a37c671ba2fdf021c060ca1c9c1c32e9f2e95bffae0e7c`, 75.279.314 bytes; classfile `ACFoods` SHA-256 `a52ec981fe51c97003383a46f7c0b2de06baa5e3ca3f73db988655abce51e12e`. O selo prende 63 campos e os 48 corpos declarados, sem usar a fonte adjacente 1.1.1 como autoridade. |
| `behavior` | `<clinit>` de 606 instruções, 63 cadeias `of → nutrition/saturationMod → flags/effects → build → putstatic`; 46 BootstrapMethods resolvem para 46 suppliers do próprio owner. O builder comprovado resolve seus suppliers antes da ingestão. Suppliers próprios usam `ACEffectRegistry → Supplier.get → MobEffect → ACCompat.effect`; o corpo completo desse bridge lê `BuiltInRegistries.MOB_EFFECT` @0, chama `Registry.wrapAsHolder` @4 e retorna @9, sem aplicar status. Suppliers vanilla leem Holder diretamente. Censo tipado de 1.555 classes identifica 121 sites em oito owners e 63/63 campos referenciados; alcance somente de leitura/encaminhamento imediato. |
| `parameters` | A ficha individualiza N, m nominal, flags, tipo de efeito, probabilidade nominal, ticks, supplier e offset de escrita para cada preset. O novo selo guarda valores e bits binary32 para não confundir grafia de `javap` com decimal exato. Foram resolvidos os três argumentos `sound`; `meat` e `sound` não são consumidos por `ACFoodBuilder.resolve`. A referência do builder distingue fórmula float de saturação, 16/32 ticks de uso, clamps de FoodData e sorteio `u < p`. |
| `targeting` | Os métodos de presets e os suppliers não recebem entidade, player, stack ou mundo; nenhum cast, projétil, raio, AOE, LOS, hitbox, dano direto ou owner próprio. O recebedor de status é responsabilidade do consumidor externo de alimentação. Tipos e ticks passados ao construtor de `MobEffectInstance` não certificam aplicação, duração efetiva, dano periódico ou um alvo real. |
| `costs` | Nenhum settlement de recurso ou agendamento em `ACFoods`: mana, stamina, XP, carga, durabilidade e cooldown N/A no contrato próprio. A construção estática não consome alimento. O caminho oficial referencial de alimentação solicita consumo de uma unidade e trata materiais infinitos/recipiente; custos e overrides efetivos do item estão fora desse escopo. |
| `integration` | Presets são objetos globais: não mutá-los por jogador nem extrair deles autoria de kill/XP/Mastery. O contrato de ACFoodBuilder fornece referência oficial vanilla e NeoForge 21.1.250 para `getFoodProperties`, cópia de efeito e eventos de uso; isso não prova runtime transformado nem hook seguro. Black Arcana mantém autoridade mágica; RPG Skill Tree integra progressão por boundary individual comprovado. `NO_MUTATION`. |
| `validation` | Auditor do contrato prende identidade, roster, construção, suppliers, parâmetros e censo ao artefato exato e aos pré-requisitos históricos; regressões verificam alegações e estados fail-closed. Os arquivos da descoberta permanecem distinguíveis e com suas alegações originais de `DISCOVERY_NOT_CERTIFIED`. CI final da contribuição e preservação dos contratos anteriores são gates independentes de QA física. |

## Preservação e fronteiras causais

A descoberta histórica registra o relatório SHA-256 `8310d35563ee74028469f192aada383c35a6cd43f70b288ec5ad93de6d8dfed1` e [job da inspeção](https://github.com/Gustavaopere/Black-Arcana/actions/runs/44332664446/job/134900918644). Ela permanece um registro de descoberta, sem alteração retroativa de seu estado. A nova ficha corrige apenas a apresentação dos três sons: `SOYLENT_GREEN → SoundEvents.HONEY_DRINK`, `PURPLE_SODA_BOTTLE/HOT_CHOCOLATE_BOTTLE → SoundEvents.GENERIC_DRINK`; os argumentos já existem no JSON histórico. A tabela antiga `sound:undefined` não é evidência de argumento desconhecido ou de som aplicado em jogo.

Há **45 presets com efeito**, **46 suppliers** e **18 presets sem chamada de efeito**. `ALEX_MEAL` tem dois suppliers. Referenciar Sugar Rush, Irradiated, Rage ou Stunned não cria outra raiz mágica nem certifica o comportamento desses efeitos. `MobEffectInstance(Holder,int)` fornece apenas Holder e duração; amplifier não é argumento explícito desses corpos publisher. A escolha nominal de probabilidade não garante efeito aceito, e um preset sem efeito pode ser usado por item com lógica adicional.

A referência já certificada de [ACFoodBuilder](systems/food-builder.md) documenta `resolve` eager, mapa JVM de identidade `BUILT`, fórmula vanilla `((float)N * m) * 2F`, defaults de uso 1.6F/0.8F s, conversão de 32/16 ticks, clamps de fome/saturação e consumo/recipiente. A referência NeoForge 21.1.250 é pin de distribuição oficial; não atesta transformação, listeners, fusão de componentes/datapacks ou sidedness instalada. Efeitos executados, aquisição, receitas, autoria, mutações por jogador, reload e QA física continuam independentes.

O recorte de censo cobre os símbolos tipados presentes nos 1.555 classfiles do publisher. Não exclui reflexão, mixins, chamadas externas ou outras versões. Os sites de registry são leituras de campos e fábricas observadas; não converter nomes em resource IDs por inferência. O provider continua aberto, apesar da conclusão documental desta ficha de suporte.

## Reprodução e regressões

- [Auditor do contrato](../../../../docs/qa/alexscaves_1010_foods_contract_audit.py), [regressões nativas](../../../../docs/qa/alexscaves_1010_foods_contract_audit_test.py), [regressões documentais](../../../../docs/qa/alexscaves_1010_foods_contract_cards_test.py) e [workflow dedicado](../../../../.github/workflows/alexscaves-1010-foods-contract.yml).
- [Auditor histórico](../../../../docs/qa/alexscaves_1010_foods_probe.py) e [regressões históricas](../../../../docs/qa/alexscaves_1010_foods_probe_test.py).
- [Selo do contrato](EXACT-FOODS-NATIVE-CONTRACT-1.0.10.json), [crosswalk histórico](EXACT-FOODS-DISCOVERY-1.0.10.json) e [pré-requisito FoodBuilder](EXACT-FOOD-BUILDER-CONTRACT-1.0.10.json).

Com publisher local verificado e JDK 21, sem carregar classes do mod:

```sh
python3 docs/qa/alexscaves_1010_foods_contract_audit.py \
  --jar /path/alexscaves-1.0.10-neoforge+1.21.1.jar \
  --javap /path/jdk-21/bin/javap \
  --seal wiki/modpack-catalog/providers/✅-alexs-caves-continued/EXACT-FOODS-NATIVE-CONTRACT-1.0.10.json \
  --output /tmp/new-foods-contract-report.json
```

O output deve ser um caminho novo. A reprodução compara o relatório e os hashes de pré-requisitos com o selo versionado; não produzir certificado a partir de uma URL mutável ou de dados sintéticos. A CI da contribuição deve concluir antes do merge. Build/GameTests gerais não substituem teste dos alimentos no modpack instalado, e testes estáticos não liberam mutações.

## Reconciliação com a referência complementar

A [prova complementar de construtores](EXACT-FOODS-CONTRACT-1.0.10.md) e seu [selo](EXACT-FOODS-CONTRACT-1.0.10.json), preservados da revisão `2d6afd4948a055ec9fa27d9fb77b8110c98a9c58`, verificam amplifier zero no construtor da referência vanilla 1.21.1. O estado `NOT_INFERRED_FROM_TWO_ARGUMENT_NATIVE_CONSTRUCTOR` deste selo distingue o argumento ausente no corpo publisher dessa prova externa; não a contradiz nem certifica execução transformada. A mesma revisão já corrige os três sons na tabela histórica; a comparação anterior a `c642587961b84ea6a2b2b5485dcf727fff5e3c4f` permanece no histórico Git.
