# domoticz-event-energywise-freebox
Script python de type « domoticz  events». Ce script permet éteindre (grâce à un smartplug) la Freebox durant la nuit (mais uniquement si elle n’est pas utilisée).

Une Freebox (révolution) consomme environ 150kW/an (soit environ 2eur/mois). Ce script vous permet de réaliser des économies d’exergie en pilotant l’extension puis l’allumage de la Freebox.

## Prérequis :
Ce script utilise les informations remontées par le plugin "PluginDomoticzFreebox" (https://github.com/ilionel/PluginDomoticzFreebox) pour couper, via une prise connectée, la Freebox quand cette dernière n’est pas utilisée.

## Comment le script fonctionne ?
Le script éteint (mais pourra aussi rallumer) la prise connectée (ici nommé Freebox) après une heure donnée.
l’intérêt de ce script est la vérification préalable à l’extinction. La Freebox sera coupée seulement si elle est réellement "inutilisée".

## Comment savoir si la Freebox est inutilisée ?
La Freebox sera considérée comme inutilisée si :
- le débit (téléchargement up/down) est inférieur à un seuil
- le player TV n’est pas allumé (donc la TV n’est pas en cours de visionnage)
- aucun enregistrement n’est en cours ou ne démarrera durant l’intervalle de mise hors tension de la Freebox.

## Que dois-je paramétrer ?
Les variables :
- WEEK_SLEEP (horaire : pour chaque jour de la semaine)
- WEEK_WAKEUP (horaire : pour chaque jour de la semaine)
- WEEK_BOOT (optionnel, horaire : pour chaque jour de la semaine)
- SLIPPAGE (optionnel, en seconde)
 
 en fonction de l’horaire d’extinction (WEEK_SLEEP) et de redémarrage (WEEK_WAKEUP) de la Freebox.
 Notes: 
  - La variable "WEEK_BOOT" permet de redémarrer expressément le "Freebox-Server" et non pas l’intégralité des équipements liés à la Freebox (Player TV, TV...). Cela nécessite d'avoir un second smartplug.
  - La variable "SLIPPAGE" permet de mettre de reporter la mise en veille si la Freebox utilisé. Une fois le l'heure sera dépassé du nombre de secondes correspondant à "SLIPPAGE" la mise en veille ne sera plus retentée

- RATE_LIMIT

en valeur de téléchargement en ko/s en dessous de laquelle la Freebox peut être coupée

- SWITCH_FREEBOX
- SWITCH_INTERNET (optionnel)

La variable "SWITCH_FREEBOX" correspond au nom de l’interrupteur (dans Domoticz) sur lequel la Freebox est branchée
Remarque: La variable "SWITCH_INTERNET" permet de définir l’interrupteur sur lequel le "Freebox-Server" est connecté (utile uniquement lorsque l’on utilise deux smartplugs pour dissocier le "Freebox-Server" et les équipements connexes tels que Player TV, la TV...) 

### Remarque :
Le script fonctionne avec les noms par défauts donnés aux composants (devices dans Domoticz) de la Freebox. Le nommage effectué par "PluginDomoticzFreebox" (qui est indispensable au bon fonctionnement de ce script). Si vous les avez renommés, il faudra répercuter les changements avant d'utiliser le script.
