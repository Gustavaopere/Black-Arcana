# ACDynamicAttributeItem — contrato técnico estático individual 1.0.10

**Escopo:** `STATIC_TECHNICAL_CATALOG_ONLY`, `CERTIFIED_STATIC_7_AXES` no recorte da interface e seus consumidores/outputs; `NO_MUTATION`, hook `NOT_VERIFIED`, QA física `NOT_TESTED`, perks `NOT_CERTIFIED`, runtime transformado `NOT_VERIFIED`, provider `OPEN`. Este selo só se torna canônico após CI completa e merge. Não acrescenta candidato, cast ou raiz sobrenatural. A [ficha individual](systems/dynamic-attributes.md) conserva os parâmetros e condições; a [descoberta inicial](EXACT-DYNAMIC-ATTRIBUTE-DISCOVERY-1.0.10.md) e a [construção](EXACT-DYNAMIC-ATTRIBUTE-CONSTRUCTION-1.0.10.md) preservam os checkpoints de auditoria.

## Sete eixos do recorte estático

**identity:** JAR publisher 1.0.10 SHA-exato; ABI abstrata, sete implementadores diretos e três herdados; censo tipado de 1555 classfiles; quinze bindings estáticos de ACItemRegistry.

**behavior:** Sete callbacks, seleção por slot/stack, diferença null e vazio, wrappers/bootstraps, fallback de superclasse e cache Gingerbread; projeção de construtores e consumidores de campos no publisher.

**parameters:** Valores ADD_VALUE de armas/lanças; Swiftwood float e clamp 0..3, defesa/material e bônus Diving, movimento Gingerbread 0.1+0.9*r e cache por dano, identities de modifier com ResourceLocation/fields simbólicos, operações e grupos de slot.

**targeting:** N/A para target de cast, vítima, LOS, AOE, projéteis e world effects: interface seleciona slot de equipamento e stack, não entidade-alvo. Atributos finais e ataques são consumidores externos.

**costs:** N/A para custo de cast, mana, stamina, cooldown, recarga, XP ou débito: consulta da stack e atributos, sem transação de recursos. Durabilidade como input, não consumo pelo callback.

**integration:** Cadeia NeoForge 21.1.250 oficial universal/userdev: prioridade do componente não vazio, bridge stack-aware, CommonHooks, evento e builder com chave Holder/ResourceLocation sem slot; nenhum owner individual nem hook seguro certificado. NO_MUTATION.

**validation:** Auditores read-only, identidade de artefatos, hashes canônicos reproduzíveis dos relatórios, regressões específicas de pivôs/identidade, documentação e índice; nenhuma inferência de runtime transformado/QA física.

A identidade e os valores de armas são os do publisher físico: a documentação registra os campos simbólicos `BASE_ATTACK_DAMAGE_ID` e `BASE_ATTACK_SPEED_ID` das armas, sem deduzir o valor literal externo desses campos. Os materiais Diving/Gingerbread são suportados pelo [contrato Armor Material](systems/armor-material.md), e a tabela de velocidade do clube pelo [contrato Swiftwood](enchantments/swiftwood.md). Este certificado não se propaga para ataques, habilidades, entidades, casting ou equipamentos completos.

## Selo reproduzível

- [Manifesto estável](EXACT-DYNAMIC-ATTRIBUTE-CONTRACT-1.0.10.json), com identidade dos artefatos e hashes esperados dos relatórios. Construção: `4439256ffa12570e5f20ec16d16df2912196b79297dc7757dda3a1d8dd608b77` (nome de arquivo normalizado para `alexscaves-1.0.10.jar`); builder: `5e5c751d9c2343e50b06e407dae020274e4e8a5bf913cf7121bebc9089d21dce`.
- [Execução de oito testes de construção](https://github.com/Gustavaopere/Black-Arcana/actions/runs/44307421054/job/134812482251) e [execução da projeção do builder](https://github.com/Gustavaopere/Black-Arcana/actions/runs/44310396511/job/134822711432). [Artefato da projeção](https://github.com/Gustavaopere/Black-Arcana/actions/runs/44310396511/artifacts/14429487534), temporário: a reprodução depende dos auditores e dos artefatos pinados, não da retenção desse ZIP.
- [Auditor de construção](../../../../docs/qa/alexscaves_1010_dynamic_attribute_construction.py), [projeção do builder](../../../../docs/qa/alexscaves_1010_dynamic_attribute_builder_probe.py), [regressões](../../../../docs/qa/alexscaves_1010_dynamic_attribute_builder_probe_test.py) e [workflow](../../../../.github/workflows/alexscaves-1010-dynamic-attribute-construction.yml). O workflow reproduz os dois relatórios, verifica os hashes, as condições e a identidade das classes; os testes de descoberta continuam independentes. JDK 21 e JARs com SHA exatos são obrigatórios; comandos presentes no workflow.

## Limites de autorização

A referência do NeoForge é 21.1.250, conforme a modlist física; a versão de desenvolvimento de Black Arcana indicada no README é 21.1.248. Não se afirma equivalência entre os dois, nem comportamento do jogo transformado. A semântica estática do builder não prova ordem dos listeners, stacking com todos os mods, aplicação final dos atributos, isolamento de cache em sessões, sincronização, ownership ou segurança per-player. WorldEffectPolicy, Mastery e XP não ganham novas permissões; não há efeito de mundo ou cast próprio nesta interface. Não substituir componente integralmente, nem duplicar atribuições de modificadores nativos, sem boundary e testes adequados. `NO_MUTATION` permanece obrigatório.
