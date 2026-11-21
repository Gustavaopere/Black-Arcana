# Burrowing Arrow — flecha escavadora

**Versão:** Alex's Caves Continued 1.0.10, publisher 8856293. **Catálogo:** ✅ contrato técnico estático de munição, projétil e dispenser. Hooks mutadores `NOT_VERIFIED`, QA física `NOT_TESTED`, `NO_MUTATION`.

`alexscaves:burrowing_arrow` é uma munição que solicita a escavação temporizada do bloco atingido. O item estende `ArrowItem`. O registro usa `ACItemRegistry.lambda$static$129` e adiciona o item a `#minecraft:arrows` no recurso do publisher. `ACEntityRegistry.lambda$static$62` registra a entidade MISC com dimensões **0,5 × 0,5 bloco**, pedido de intervalo de atualização 1 e updates de velocidade habilitados (17–25). [Identidades, hashes e métodos](../EXACT-BURROWING-CAVE-ITEMS-CATALOG-1.0.10.md)

## Ativação, física e autoria

- `BurrowingArrowItem.createArrow` (0–9) passa mundo e portador a `BurrowingArrowEntity(Level, LivingEntity)`. As duas stacks recebidas ficam fora do corpo da factory. O construtor usa stack nova de munição e arma `null` na chamada ao pai. Solicita base **3,5** e incrementa piercing em **1**. O construtor posicional solicita a mesma base e conserva o piercing recebido da inicialização herdada.
- No dispenser, `ACItemRegistry.setup` registra o comportamento específico entre 396 e 414. `ACItemRegistry$6.getProjectile` constrói pelo caminho posicional e pede `pickup=ALLOWED`. O pai nativo `AbstractProjectileDispenseBehavior.execute` passa à flecha `(stepX, stepY + 0,1F, stepZ)`, potência **1,1F** e incerteza **6F** (36–68). Solicita inserção (74) e depois redução de **uma unidade** da pilha (80), inclusive com retorno falso de inserção.
- Na referência derivada Minecraft 1.21.1/NeoForge 21.1.248, `ProjectileWeaponItem.createProjectile` chama a factory virtual da munição (42). O débito em arma segue `useAmmo` e seus filtros antes da factory. O impacto herdado gera a fonte `DamageSources.arrow` e o pedido base `ceil(clamp(float(|v|) × base, 0, INT_MAX))` (11–17, 98–110), com ramos separados de crítico, arma e piercing. Esses números dependem do estado do projétil e da aceitação em jogo. [Fronteira de referência](../EXACT-BURROWING-CAVE-ITEMS-CATALOG-1.0.10.md#parâmetros-herdados-de-referência)

## Escavação

| Parâmetro | Contrato nativo |
|---|---|
| Alvo | Posição capturada por `onHitBlock`. Exige `inGround`, posição presente, owner jogador ou ausente, fluido vazio, bloco fora da tag `alexscaves:unmovable` e dureza diferente de `-1F`. |
| Limite | `DUG_BLOCK_COUNT < 5`. Ao chamar `Level.destroyBlock(pos, true)`, o corpo descarta o retorno e incrementa o contador. |
| Limiar e duração | `H = int(max(dureza, 0,2F) × 15F)`. Com contador inicial zero e avaliação elegível ininterrupta, o pós-incremento pede quebra no tick elegível `H+2`. |
| Movimento | Durante o avanço solicita `(centro − posição) × 0,2F`. Após a tentativa de quebra solicita o vetor para o centro normalizado × `0,3F`. |
| Retenção e saída | `tickDespawn` delega ao pai fora do estado `DIGGING`. Na referência, o pai incrementa a idade local e descarta a partir de 1.200 chamadas efetivas. Quebra visual é limpa ao perder a condição ou remover a entidade. |
| Sincronização | `DUG_BLOCK_COUNT` e `DIGGING` são sincronizados. O owner publisher é entregue ao construtor herdado. Passagem por unload, persistência e aceitação da escrita de mundo seguem o ambiente carregado. |

O alcance físico depende do disparo e das colisões herdadas. A classe não declara área própria ou cooldown de cast. Dano final, PvP, proteção de bloco e autorização para mudar o contador de tentativas continuam pendentes. [Offsets do ciclo de escavação](../EXACT-BURROWING-ARROW-CAUSAL-1.0.10.md)

## Receita e integração

A receita em coluna `T / S / D` usa um `alexscaves:corrodent_teeth`, uma haste de `#alexscaves:rods/wooden` e um `alexscaves:dark_tatters`. Produz **4 flechas**. O débito do dispenser, a munição de arma, o pickup e a quebra efetiva são resultados distintos. Uma futura perk precisa preservar a autoridade de cada um desses caminhos e o limite de tentativas. A ficha entra como munição técnica, com zero raízes sobrenaturais adicionais. [Receita e prova reproduzível](../EXACT-BURROWING-CAVE-ITEMS-CATALOG-1.0.10.md)
