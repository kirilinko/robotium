Le projet Robotarium a été réalisé avec le framework minimaliste Flask donc python. Comme SGBD, nous avions opté pour PostgreSQL.

Prérequis
Avoir python installé 
Avoir installé PostgreSQL
Avoir les drivers de reconnaissances des plaquettes Arduino installé sur la machine

Processus d’installation
L'ensemble des différents modules utilisés pour la réalisation de cette application sont tous référencés dans le fichier "requirement.txt"

Une fois que vous aurez créé votre environnement virtuel, vous pouvez exécuter la commande : 
 " pip install -r requirement.txt " pour installer les modules.
 Une fois cela fait, vous pouvez exécuter :
" pip freeze " afin de voir si les modules ont correctement été installés

Par la suite, vous devez installer Arduino CLI en suivant les instructions se trouvant sur :
https://arduino.github.io/arduino-cli/0.35/installation/ 
Une fois téléchargé, vous devez déplacer l'exécutable "arduino-cli.exe" dans le dossier du projet comme ceci :
