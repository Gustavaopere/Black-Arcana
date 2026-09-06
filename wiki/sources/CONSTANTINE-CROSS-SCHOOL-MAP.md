# John Constantine — mapa transversal de práticas

## Estado

`PESQUISA DE DESIGN / DEDUP PENDENTE — NÃO É UMA NOVA ESCOLA`

John Constantine é usado aqui como referência de **amplitude de repertório ocultista**. O Black Arcana não deve criar uma escola `Constantine`, uma árvore exclusiva ou um recurso próprio inspirado no personagem. Cada prática é direcionada ao domínio já correto do modpack.

## Princípio

`uma técnica → uma autoridade semântica → um provider preferencial`

Se um mod instalado já fornece a técnica com qualidade aceitável, o Black Arcana integra/cataloga em vez de duplicar.

## Mapa de práticas

| Prática abstrata | Destino no pack | Regra de implementação/dedup |
|---|---|---|
| círculo protetor | Ordem / Bruxaria ritual | Ordem se for ward geométrica de combate; Hexalia/Eidolon se for ritual preparado. |
| ward de ocultação | Bruxaria / Ocultismo | Preferir ritual/sigil preparado; não transformar invisibilidade genérica em novo spell se provider já cobre. |
| ocultar alma/assinatura | Souls & Death / Bruxaria | Só com soul identity/provider real; sem `registry scan` ou invisibilidade universal. |
| cortar conjurador de sua fonte | Ordem / Countermagic | Novo candidato apenas se houver hook para identificar **qual recurso/provider** está alimentando o cast. |
| quebrar proteção mágica | Ordem / Countermagic | Usar dispellable/protection semantics do provider. |
| vínculo simpático de força vital | Binding / Curses | `VITAL_ENERGY`, não `BLOOD`, salvo quando sangue real fizer parte do contrato. |
| vínculo por sangue | Blood/Binding | Requer fonte `HEMATIC_BLOOD`/`ALTERED_BLOOD`; sangue é custo/chave real, não sinônimo de HP. |
| convocar demônio | Infernal / Goety/Eidolon | Provider-native summon/ritual first; ownership, lifetime e summon cap permanecem do provider. |
| banir demônio/espírito | Ordem / Divine / Occult | A escola depende da natureza do rito; não criar três versões semanticamente iguais. |
| prender demônio/espírito em recipiente | Binding / Order containment | Requer entity-type eligibility, persistence e escape/release contract; nunca delete arbitrário. |
| exorcismo | Divine/Theurgy ou Witchcraft/Occult | Preferir Eidolon/Holy/provider existente; efeito deve distinguir possession/demon/spirit real. |
| rastrear pessoa por objeto pessoal | Witchcraft / Divination | Excelente candidato de bruxaria se não houver provider equivalente: objeto-foco + identidade persistente + alcance/dimensão bounded. |
| leitura de presença/resíduo | Witchcraft / Spirit Sight | Deduplicar contra Black Arcana Spirit Sight e Malum/Eidolon antes de criar. |
| sono por erva/material | Witchcraft / Hexalia | Preparação/alquimia deve prevalecer sobre outro projétil de sleep genérico. |
| magia improvisada com objetos comuns | Witchcraft | Deve virar receitas/rituais situacionais, não um botão universal de improvisação. |
| pacto/barganha | Infernal / Divine / Occult | Contrato persistente com benefício+custo; cada entidade/provider preserva sua authority. |
| demon blood como chave | Infernal + Blood | `ALTERED_BLOOD`; pode habilitar rito infernal sem converter automaticamente para Lava Infernal ou mana. |
| manipulação de sincronicidade/probabilidade | Chaos | Reaproveitar catálogo de Probability; não criar uma segunda escola de sorte. |
| teleporte/escape espacial | Order/Space | Deduplicar contra Portal Spell, Immersive Portals, Threshold Gate, Leylines e outros providers. |
| ilusão/memória/hipnose | Witchcraft/Occult ou provider existente | Só criar quando o efeito mecânico for distinguível e seguro; client deception nunca é authority. |
| comunicação com morto/espírito | Souls & Death / Malum/Eidolon | Provider-native first; não sintetizar alma de qualquer entidade morta. |
| reanimar morto | Goety/Eidolon/necromancy | Não pertence automaticamente a Blood ou Infernal. |

## Candidatos que Constantine realmente acrescenta ao roadmap

### 1. Ruptura de Fonte

**Categoria:** Order / Countermagic

Identifica um cast ou efeito com provider/resource causal comprovado e interrompe por uma janela curta o **vínculo daquele efeito com sua fonte**, em vez de silenciar toda magia do alvo.

Exemplos de aplicação possível após adapters:

- bloquear temporariamente um link Blood/Infernal específico;
- interromper channel alimentado por reservatório;
- desativar temporariamente um construct enquanto seu owner/resource link continua válido.

**Não pode:** zerar mana, Soul Energy, Source ou outro recurso arbitrariamente sem API; remover permanentemente progressão; afetar providers desconhecidos.

### 2. Laço Simpático Vital

**Categoria:** Binding / Curse

Relaciona duas entidades por `VITAL_ENERGY` para um efeito explicitamente definido, por exemplo compartilhamento bounded de consequência ou condição. É deliberadamente separado de Blood Binding.

**Invariante:** Iron Golem pode ser elegível para um contrato de `VITAL_ENERGY` se a classificação permitir, mas continua `NO_BLOOD` para custos hemáticos.

### 3. Busca por Vestígio

**Categoria:** Witchcraft / Divination

Ritual/spell preparado que usa um objeto realmente associado a uma entidade como foco de rastreamento. Quanto mais forte o vínculo causal do objeto com o alvo, melhor o resultado possível.

Saídas bounded candidatas:

- direção aproximada;
- dimensão conhecida/unknown;
- faixa de distância grosseira;
- último vestígio registrado, quando permitido;
- nenhuma coordenada exata se a política/proteção não autorizar.

### 4. Selo de Ocultação

**Categoria:** Witchcraft / Ward

Mascara uma assinatura reconhecida contra um **detector específico** por tempo e escopo bounded. Não é invisibilidade global e não pode enganar sistemas sem adapter.

## Vínculos e recursos — consequência importante

Constantine reforça que `vínculo` deve ser um contrato genérico tipado, não um sinônimo de sangue:

`Caster ⇄ Typed Link ⇄ Target/Source`

Tipos possíveis já separados pelo projeto:

- `HEMATIC_BLOOD`;
- `ALTERED_BLOOD`;
- `VITAL_ENERGY`;
- `SOUL/SPIRIT` quando provider expõe;
- `MANA/SOURCE/SOUL_ENERGY` somente por adapter explícito;
- `INFERNAL_RESERVOIR`/outra infraestrutura somente por contrato próprio.

Isso permite que a mesma infraestrutura de lifecycle/ownership/persistence seja reutilizada sem misturar economias mágicas.

## Aquisição e fantasia de gameplay

As técnicas inspiradas nesse arquétipo devem ser obtidas por **conhecimento, investigação, materiais, ritos, pactos e preparação**, não simplesmente por level-up automático. O jogador ocultista deve ganhar versatilidade por conhecer muitos sistemas, mas continuar limitado pelo custo e pelas regras de cada um.

## Visual

Constantine não define uma paleta de escola. O VFX vem do sistema usado:

- círculo de Ordem → geometria limpa;
- rito Hexalia/Eidolon → chalk/sigils/candles/incense/material components;
- vínculo Blood → fios/veias/pulsos hemáticos;
- vínculo vital → pulso orgânico não-hemático;
- pacto Infernal → glyphs/carvão/brasa/Lava Infernal;
- Divine/Theurgy → luz, halo, inscrições e partículas próprias.

Isso preserva a leitura visual de **qual magia está sendo usada**, em vez de transformar todo ocultismo em um único efeito visual.
