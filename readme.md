<h1>✈️ FlightPrice - App</h1>

<br>

<div>
  <h2>📊 Sobre o Projeto</h2>

  <p>
    Este projeto é a continuação do FlightPriceML, onde foram realizados experimentos de aprendizado de máquina e testados diversos modelos para encontrar o melhor para a predição de preços de passagens aéreas.
  </p>
  
  <p>
    Com base no FlightPriceML, o modelo escolhido foi o HistGradientBoostingRegressor. No FlightPriceApp, o modelo já foi treinado previamente e salvo utilizando Joblib, permitindo que a API carregue o modelo diretamente para gerar predições em arquivos enviados pelo usuário, sem necessidade de treinar novamente.
  </p>
  
  <p>
    O front-end foi desenvolvido com <strong>TypeScript</strong>, <strong>React.js</strong>, <strong>Vite</strong> e <strong>Tailwind CSS</strong>. O back-end utiliza <strong>FastAPI</strong> com <strong>Uvicorn</strong>, e o treinamento do modelo foi feito com <strong>scikit-learn</strong>, <strong>pandas</strong> e <strong>numpy</strong>.
  </p>

  <p>
    Todo o projeto foi conteinerizado com <strong>Docker</strong>, utilizando dois containers: um para a API (FastAPI) e outro para o front-end (React).
  </p>

  <p>
    No front-end, é possível fazer o upload de um arquivo <code>.xlsx</code> contendo os dados de teste. O arquivo é processado no back-end, onde as predições são geradas e após o processamento, o usuário recebe um arquivo <code>.zip</code> contendo:
  </p>

  <ul>
    <li>Um arquivo <code>.txt</code> com as predições linha a linha</li>
    <li>O arquivo original com uma nova coluna contendo os preços previstos</li>
  </ul>
</div>
<br>

<div>
  <h2>🛠️ Instalação e Execução</h2>

  <p>Siga os passos abaixo para executar o projeto localmente:</p>

  1 - Clone esse repositório:
  
  ```
  git clone https://github.com/CaioCesarMDS/FlightPriceApp.git
  ```
  
  2 - Suba os containers com Docker:
  
  ```
  docker compose up --build
  ```
  
  3 - Acesse a aplicação no navegador::
  
  ```
  http:localhost:5173
  ```

  4 - Para testes, utilize o arquivo de exemplo localizado em <code>api/data/test_set.xlsx</code>. Basta fazer o upload na interface.

</div>

<br>

<div>
  <h2>📚 Principais Bibliotecas e Ferramentas Utilizadas</h2>

  <ul>
    <li>React</li>
    <li>Vite</li>
    <li>Tailwind.css</li>
    <li>Shadcn/Ui</li>
    <li>Docker</li>
    <li>Pandas</li>
    <li>NumPy</li>
    <li>Scikit-learn</li>
    <li>FastApi</li>
    <li>Uvicorn</li>
    <li>Joblib</li>
  </ul>
</div>


