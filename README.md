# <img src="https://avatars1.githubusercontent.com/u/7063040?v=4&s=200.jpg" alt="HU" width="24" /> Desafio Bravo

Construa uma API, que responda JSON, para conversão monetária. Ela deve ter uma moeda de lastro (USD) e fazer conversões entre diferentes moedas com cotações de verdade e atuais.

A API deve converter entre as seguintes moedas:
- USD
- BRL
- EUR
- BTC
- ETH


Ex: USD para BRL, USD para BTC, ETH para BRL, etc...

A requisição deve receber como parâmetros: A moeda de origem, o valor a ser convertido e a moeda final.

Ex: `?from=BTC&to=EUR&amount=123.45`

Você pode usar qualquer linguagem de programação para o desafio. Abaixo a lista de linguagens que nós aqui do HU temos mais afinidade:
- JavaScript (NodeJS)
- Python
- Go
- Ruby
- C++
- PHP

Você pode usar qualquer _framework_. Se a sua escolha for por um _framework_ que resulte em _boilerplate code_, por favor assinale no README qual pedaço de código foi escrito por você. Quanto mais código feito por você, mais conteúdo teremos para avaliar.

## Requisitos
- Forkar esse desafio e criar o seu projeto (ou workspace) usando a sua versão desse repositório, tão logo acabe o desafio, submeta um *pull request*.
- O código precisa rodar em macOS ou Ubuntu (preferencialmente como container Docker)
- Para executar seu código, deve ser preciso apenas rodar os seguintes comandos:
  - git clone $seu-fork
  - cd $seu-fork
  - comando para instalar dependências
  - comando para executar a aplicação
- A API precisa suportar um volume de 1000 requisições por segundo em um teste de estresse.



## Critério de avaliação

- **Organização do código**: Separação de módulos, view e model, back-end e front-end
- **Clareza**: O README explica de forma resumida qual é o problema e como pode rodar a aplicação?
- **Assertividade**: A aplicação está fazendo o que é esperado? Se tem algo faltando, o README explica o porquê?
- **Legibilidade do código** (incluindo comentários)
- **Segurança**: Existe alguma vulnerabilidade clara?
- **Cobertura de testes** (Não esperamos cobertura completa)
- **Histórico de commits** (estrutura e qualidade)
- **UX**: A interface é de fácil uso e auto-explicativa? A API é intuitiva?
- **Escolhas técnicas**: A escolha das bibliotecas, banco de dados, arquitetura, etc, é a melhor escolha para a aplicação?

## Dúvidas

Quaisquer dúvidas que você venha a ter, consulte as [_issues_](https://github.com/HotelUrbano/challenge-bravo/issues) para ver se alguém já não a fez e caso você não ache sua resposta, abra você mesmo uma nova issue!

Boa sorte e boa viagem! ;)




_______________________________
## Solução proposta

- Foi desenvolvida a api com Django REST.
- Para a taxas de câmbio, foi usado a api CryptoCompare. Onde a taxa é salva no banco, e não é solicitada se a próxima consulta for no tempo menor que 30 minutos.

##Funcionamento
Acessando (  http://localhost:8000/?from=BRL&to=BTC&amount=900 ), onde:
 - from = É a moeda de origem;
 - to = É a moeda de destino;
 - amount  = É o valor que será convertido.
 
 
 Ele deverá retornar:
 {
    "price": "0.00002572",
    "value": "0.02314800",
    "to_currency": "BTC",
    "from_currency": "BRL",
    "amount": "900"
}

Onde  **price** é o valor da moeda e **value** é o valor final convertido.
 

##Configurando o ambiente
1 - Clonar o projeto:
	`git clone https://github.com/karolGuimaraes/challenge-bravo.git`
2 -  Acesse a pasta /bravo
3 - Executar:
	`docker-compose up`

##Teste
**Teste unitários**
Para executa o teste:
	`docker-compose run app python manage.py test`

Resposta similar:

	Creating test database for alias 'default'...
	System check identified no issues (0 silenced).
	....3.761 3.761
	.
	----------------------------------------------------------------------
	Ran 5 tests in 1.651s

	OK
	Destroying test database for alias 'default'...

**Teste de estresse**
Para o teste foi utilizado o wrk, com o servidor rodando execute:
`wrk -t10 -c1000 -d30s 'http://localhost:8000/?from=BRL&to=BTC&amount=1'`
-- Se for necessário  brew install wrk ou sudo apt-get install wrk, para instalar o wrk.

Resposta similar:

	Running 30s test @ http://localhost:8000/?from=BRL&to=BTC&amount=1
  	8 threads and 1000 connections
 	 Thread Stats   Avg      Stdev     Max   +/- Stdev
    	Latency   108.85ms   23.19ms 311.93ms   80.52%
    	Req/Sec   133.37    111.01   490.00     82.91%
 	 31842 requests in 30.08s, 10.99MB read
	Requests/sec:   1058.69
	Transfer/sec:    374.29KB



