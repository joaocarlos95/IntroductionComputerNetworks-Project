# # Introduction Computer Networks Project (2015-2016)

### Contributors
- [@hugogaspar8](https://github.com/hugogaspar8) - Hugo Gaspar
- [@joaocarlos95](https://github.com/joaocarlos95) - João Carlos
- [@jtf16](https://github.com/jtf16) - João Freitas

### About

This project consists of developing the game TIC TAC Toe in online form. The application must have a client-server architecture, using the server as intermediary in communication between clients. Each message sent to the server must be acknowledged.

The messages have the following format:
  - **Registo: Nome** - Register the client with name _Nome_ on the server.
  - **Convite: Nome** - Invite a client with name _Nome_ to join a game.
  - **ConviteR: Resposta Nome** - Client response to the invitation sent by the client with name _Nome_. The field _Resposta_ can be "Aceite" or "Recusado" for either accepted or refused, respectively.
  - **Jogada: Posição Nome** - Move made by the client with name _Nome_. The field _Posição_ is a number between 1 and 9, corresponding to the positions of the board.
  - **Fim: Perdeste/Empatamos Nome** - Message indicating the end of the game, specifying whether the client with name _Nome_ won or lost.
  - **Lista** - Message sent to the server requesting the list of players registered in the game.
  - **Lista: Nome Estado** - Messagem sent by the server indicating the players that are registered in the game and their current status.
  - **Ok** - Acknowledge
  - **Erro: Mensagem** - Error messagens with content _Mensagem_
