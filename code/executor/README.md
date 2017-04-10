# NXT2 Executor
Executor for the NXT2, using the [3-Motor Chassis](http://nxtprograms.com/NXT2/3-motor_chassis/steps.html).

## Hoe werkt de nxt software?
De nxt software is gemaakt in eclipse als nxtpc project.
Om deze software te gebruiken op andere pc's moet je het project exporteren via,
file -> export -> runnable jar file -> finish.
Nu heb je een runnable jar file,
maar de classpath moet nog gezet worden, zodat de juiste libaries worden geimporteerd.
Dit doe je door de jar file te openen en in de manifest file achter classpath de jar files te zetten die je nodig hebt in je project. De libaries die samen met de jar file zijn ingeleverd zijn al inbegrepen in de classpath van de jar file. Verder heb je nog een 32 bit versie van de java development kit nodig om connectie te kunnen maken met de nxt brick. Deze kun je [hier](http://www.oracle.com/technetwork/java/javase/downloads/jdk8-downloads-2133151.html) krijgen.
