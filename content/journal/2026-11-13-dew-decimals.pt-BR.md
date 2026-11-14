---
title: "Por que mostrar o orvalho com casas decimais"
description: "O musgo cresce 0,1 por segundo, mas o contador de orvalho parecia travado. Assim corrigimos o formato do número."
copy_review: iris 2026-11-14
---
Moss Garden é um jogo idle (incremental) para iOS, e seu contador de orvalho parecia travado porque mostrava apenas números inteiros a partir de dez. Agora mostramos duas casas decimais abaixo de 1 e uma abaixo de 1.000, e arredondamos para baixo, para que o número nunca prometa mais do que você tem.

## Por que o número parecia travado

O musgo se acumulava a 0,1 por segundo, mas o número de orvalho no alto da tela ficava igual por muito tempo. Uma pessoa que testava nos disse que não dava para saber se ele estava contando. A causa era simples: a partir de dez, mostrávamos apenas números inteiros.

## O que mudamos

Valores abaixo de 1 agora mostram duas casas decimais, e valores abaixo de 1.000 mostram uma. Os zeros finais são removidos, então você lê 289 em vez de 289,0.

A única decisão de verdade foi o arredondamento. Mostrar 185,56 como 185,6 faria algo que você ainda não pode comprar parecer acessível. Por isso **arredondamos para baixo**: o número na tela é sempre, no máximo, o que você realmente tem.

É uma mudança minúscula, mas, num jogo sobre esperar, ver o número se mexer faz parte da recompensa.

## Perguntas frequentes

### Por que Moss Garden mostra o orvalho com casas decimais?
Porque o musgo cresce 0,1 por segundo, e números inteiros faziam o contador parecer travado. As casas decimais permitem ver que ele está contando.

### O número de orvalho é arredondado para cima ou para baixo?
Para baixo. O número na tela é sempre, no máximo, a quantidade que você realmente tem, então nada parece acessível antes da hora.
