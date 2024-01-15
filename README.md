# jaeger matchmaking api
a very light and very flexible game matchmaking system. this is not designed for movement based games, more-so targeted at strategy games (like Chess or Pokemon) which involve 2 or more parties being pitted against each other. **this system is based on trust, if a game server fails to or sends faulty data, weird things may happen**. though players are required to be queued and enter a match for atleast N seconds before it can be a "valid" victory (tbd).

customize how the logic works and what data it should expect in the `rules`


## how to run:
- customize the socket & redis settings in `src.config.settings`
- there are 3 different json strings that the websockets accepts, more detail in `src.server`
- send the appropriate events and confirm on time, the server then feeds back a new ID for a redis pubsub channel which can be used for communications
- send a response back on the websocket if there is a timeout or forfeit


## how it works:
- you queue actors and provide the appropriate `data`. fork and add in your things if they are specific needs, all rules should have the relevant details for running most matchmaking algorithms
- the server will send a `confirm_match` event over the socket when a player has been matched, simply send back the id and it will send back a `created_match` with the pubsub room


pretty simple to be honest, but im happy with it. still a work in progress but most things are done.


code is being heavily restructured to be neater though :<
