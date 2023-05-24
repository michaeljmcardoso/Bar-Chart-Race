# Áudio para Texto

   <p> Este projeto consiste em um programa de conversão de áudio para texto, utilizando a biblioteca <strong>SpeechRecognition</strong> do Python. O objetivo principal é <strong>fornecer uma ferramenta simples e eficiente para auxiliar na transcrição de arquivos de áudio em texto.</strong>
   
## Google Web Speech API

Uma API (Application Programming Interface) é um conjunto de regras e protocolos que permite que diferentes softwares se comuniquem entre si. É como uma ponte que permite que um programa utilize as funcionalidades de outro de maneira padronizada e organizada.

O SpeechRecognition é uma biblioteca de Python que utiliza uma API de reconhecimento de fala para converter áudio em texto. Essa API, chamada de Google Web Speech API, é um serviço oferecido pela Google que faz o processamento da fala em tempo real e retorna o texto correspondente.

O funcionamento do SpeechRecognition com a API de reconhecimento de fala ocorre em etapas. Primeiro, o programa utiliza a biblioteca para ler um arquivo de áudio ou capturar áudio em tempo real. Em seguida, a biblioteca envia esse áudio para a API de reconhecimento de fala da Google. A API processa o áudio, utilizando algoritmos avançados de reconhecimento de fala, e retorna o texto correspondente.

A biblioteca SpeechRecognition lida com toda a parte de comunicação com a API, tornando o processo transparente para o desenvolvedor. Ela fornece métodos simples para gravar áudio, enviar para a API e receber o texto reconhecido como resposta. Dessa forma, os desenvolvedores podem facilmente integrar o reconhecimento de fala em seus próprios programas, sem se preocupar com os detalhes complexos da API subjacente.

Em resumo, o SpeechRecognition utiliza uma API de reconhecimento de fala para converter áudio em texto. A biblioteca facilita a comunicação com essa API, permitindo que desenvolvedores utilizem o reconhecimento de fala em seus programas de maneira simples e eficiente.
   

Inicialmente pensou-se um programa que fosse basicamente, simples e com poucas linhas de código. Assim, a primeira versão do programa acabou sendo desenvolvida para lidar com a conversão de pequenos trechos de áudio. Ela utiliza a função recognize_google da biblioteca SpeechRecognition para realizar a conversão de áudio em texto. Essa versão é adequada para transcrever áudios curtos, como mensagens de voz, anotações curtas ou pequenos trechos de diálogos. Embora seja simples, essa versão já pode ser útil para economizar tempo e esforço na transcrição manual.

No entanto, como trabalho com realização de entrevistas com meia hora ou mais de gravação, percebeu-se a necessidade de uma versão mais robusta para lidar com a transcrição de áudios longos. A segunda versão do programa foi então desenvolvida para atender a essa nessecidade. Nessa versão, o áudio é dividido em pedaços de aproximadamente 30 segundos para evitar problemas de memória durante o processamento. Além do mais, foi realizada uma melhoria na precisão do reconhecimento de fala por meio do ajuste para o ruído ambiente antes de cada gravação. Daí a imporância de se realizar boas gravações, tentando se possível minimizar as interferências do som ambiente, pois a qualidade da gravação poderá influenciar no resultado final da impresssão do texto. Essa versão é capaz de transcrever áudios longos, como palestras, entrevistas, podcasts ou reuniões.

A relevância desse tipo de programa é notável para pessoas que trabalham com a conversão manual de áudios para texto. Transcrever áudios manualmente pode ser um processo demorado e tedioso, exigindo muita atenção e esforço para ouvir cada frase e em seguida escrevê-las. Com o auxílio de um programa de conversão automática, como este, o trabalho é facilitado e acelerado, permitindo que as pessoas foquem em outras tarefas importantes. Ademais, o programa pode ajudar pessoas com deficiência auditiva ao converter áudios em tempo real, facilitando a compreensão e comunicação.

Em resumo, esse programa de conversão de áudio em texto é uma ferramenta valiosa para economizar tempo e esforço na transcrição manual. As duas versões, a primeira voltada para textos curtos e a segunda para textos longos, fornecem soluções específicas para diferentes necessidades. Através desse projeto, busca-se fornecer uma solução eficiente e acessível para melhorar a produtividade e facilitar a vida daqueles que precisam lidar com a transcrição de áudios.</p>

