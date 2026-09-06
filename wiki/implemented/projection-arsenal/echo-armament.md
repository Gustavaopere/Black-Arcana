# Echo Armament

## Estado

`IMPLEMENTADO / CANÔNICO — REAL-MODPACK HOST ACCEPTANCE DEFERRED`

## Identidade

- **Domínio:** Projection & Arsenal
- **Provider preferencial de cast:** Iron's Spells quando hook suportado
- **Authority:** Black Arcana
- **Função:** projeção temporária de arma

## Descrição

Resolve um perfil de arma projetada allowlisted e cria uma representação efêmera para o cast/sessão. Não clona o ItemStack persistente do jogador e não copia NBT arbitrário.

## Obtenção e aprendizado

`TBD — Stage 08 / integração provider e RPG`

## Custo e casting

- **Custo normal:** `TBD — Stage 08/provider`
- **Cooldown:** `TBD — Stage 08/provider`
- **Cast time:** `TBD — Stage 08/provider`

## Efeito mecânico

A arma projetada usa um `projection profile` registrado. O perfil/lifecycle pertence ao Black Arcana; item real não é criado como recompensa persistente.

## Hard ceilings confirmados do domínio

- máximo de ecos/projeções ativas: `48`;
- raw attack damage técnico máximo de perfil: `100.0`;
- registry de profiles: `64` entradas;
- profile ID: `64` caracteres.

Esses valores são limites de segurança, não dano normal do spell.

## Segurança

- sem duplicação de inventário;
- sem cópia de NBT arbitrário;
- budget de projeções bounded;
- lifecycle libera budget ao terminar;
- cliente nunca cria autoridade de item.

## VFX

`TBD — perfil visual por arma/escola`. A projeção deve ser claramente espectral/arcana e distinguir-se de item físico dropável.

## Testes/evidência

Parte do Stage 07.03 canônico, merge PR #50. Pipeline final/post-merge validou JUnit, build NeoForge 1.21.1, JAR, GameTests e dedicated-server smoke. Aceitação com provider/modpack real permanece deferida.
