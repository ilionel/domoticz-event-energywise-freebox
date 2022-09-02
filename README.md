# domoticz-event-energywise-freebox
Script python de type « domoticz  events» qui éteint (grâce à un smartplug) la Freebox durant la nuit (mais seulement si elle n'est pas utilisée).

Une Freebox (révolution) consomme environ 150kW/an (soit environ 2eur/mois). Ce script vous permet de réaliser des économies d’exergie en pilotant l’allumage et l’extension de la Freebox.

## Prérequis :
Ce script utilise les informations remontées par le plugin PluginDomoticzFreebox (https://github.com/ilionel/PluginDomoticzFreebox) pour couper la Freebox (via une prise connectée) quand cette dernière n'est pas utilisée.

## Comment le script fonctionne ?
Le script éteint (et pourra aussi rallumer) la prise connectée (ici nommé Freebox) après une heure donnée, mais seulement si la Freebox est "inutilisée".

## Comment savoir si la Freebox est inutilisée ?
La Freebox sera considérée (par le script) comme inutilisée si :
- le débit (téléchargement) est inférieur à un seuil
- le TV player n'est pas allumé (donc la TV n'est pas en cours de visionnage)
- aucun enregistrement n'est en cours ou ne démarrera durant l’intervalle de mise hors tension de la Freebox.

## Que dois-je paramétrer ?
Les variables :
- SLEEP_TIME
- WAKEUP_TIME 
 en fonction de horaire d’extinction et de redémarrage de la Freebox

- RATE_LIMIT
en valeur de téléchargement en ko/s en dessous de laquelle la Freebox peut être coupée

- SWITCH_FREEBOX
le nom de l’interrupteur (dans Domoticz) sur lequel la Freebox est branchée

Le script fonctionne avec le nom par défaut donné (par PluginDomoticzFreebox) aux équipements de la Freebox. Si vous les avez renommés, il faudra répercuter également ces changements dans le script.
