# Projet IHM : Trading / Market Simulation avec Ingescape

## Collaborateurs (à modifier)
- Nom Prénom 1
- Nom Prénom 2
- Nom Prénom 3
- Nom Prénom 4

---

## Contexte & objectif

Dans le cadre des TPs **Ingescape (Ingenuity i/o)**, notre objectif était de construire une petite **IHM de trading** basée sur une architecture **multi-agents** dans Ingescape Circle.

L’idée générale :
1. Un agent génère un **scénario de marché** (historique + futur).
2. Un autre agent **simule** et affiche l’évolution des prix.
3. L’utilisateur choisit une action (**BUY / SELL**) et le système renvoie un **résultat (gagné/perdu)**.

---

## Ce qui marche (version livrée)

### 1) ScenarioGenerator (génération de scénario)
- L’agent **ScenarioGenerator** reçoit des paramètres (Trend, Asset_Action, Asset_Category, Asset_ID, Generate).
- Lorsqu’on active `Generate`, il génère :
  - `History_Prices` (DATA)
  - `Future_Prices` (DATA)
- Il envoie ces données au format **JSON** (encodé en UTF-8 dans un DATA Ingescape).
- Quand le scénario est prêt, il peut activer `Scenario_Ready`.

### 2) MarketSimulator (simulation + affichage)
- L’agent **MarketSimulator** reçoit :
  - `History_Prices` (DATA)
  - `Future_Prices` (DATA)
- Après impulsion sur `Start_Simulation`, il :
  - Décode le JSON
  - Lance la simulation graphique (Matplotlib)
  - Publie pendant la simulation :
    - `Current_Price`
    - `Time_Index`
- À la fin, il calcule un résultat selon la décision utilisateur :
  - `User_Decision` = `"BUY"` ou `"SELL"`
  - Il publie `Decision_Result` (ex: “YOU WON …” / “YOU LOST …”).

Exemple de résultat attendu :  
- Si décision = BUY et le prix final > prix initial → **YOU WON**  
- Si décision = SELL et le prix final < prix initial → **YOU WON**  

---

## Ce qui nécessite des améliorations (problèmes rencontrés)

### 1) Whiteboard Ingescape
Nous n’avons **pas réussi à connecter / exploiter correctement le Whiteboard**, malgré :
- des essais pendant **les deux TPs**
- et un point discuté avec le professeur  
➡️ à la fin, nous n’avons pas pu finaliser cette partie.

### 2) PlatformController + UI (intégration complète)
Nous avons également eu des difficultés à réaliser une intégration stable de :
- **PlatformController**
- + une UI complète (Textual ou autre)
pour piloter toute la chaîne de manière propre.

➡️ Le fonctionnement de base (ScenarioGenerator → MarketSimulator) est stable, mais la partie “plateforme + UI centrale” n’a pas été finalisée comme prévu.

---

## Architecture actuelle (fonctionnelle)

- **ScenarioGenerator**
  - Inputs : Trend, Asset_Action, Generate, Asset_Category, Asset_ID
  - Outputs : Future_Prices, History_Prices, Scenario_Ready

- **MarketSimulator**
  - Inputs : History_Prices, Future_Prices, Start_Simulation, User_Decision
  - Outputs : Current_Price, Time_Index, Decision_Result, Simulation_Done

---

## Exemple de résultat (à illustrer)

Ajoutez ici une capture du plot Matplotlib généré par MarketSimulator :

![Plot MarketSimulator](imgs/market_plot.png)

Et ici une capture du résultat Decision_Result (YOU WON / YOU LOST) :

![Decision Result](imgs/decision_result.png)

---

## Installation & exécution

### Prérequis
- Ingescape Circle installé
- Python 3.12
- Dépendances Python :
  - ingescape
  - matplotlib

### Virtual environment (venv)
Dans notre projet, un **venv est utilisé uniquement dans `MarketSimulator/src/`** (car Matplotlib est nécessaire côté simulateur).

#### Création du venv
```bash
cd MarketSimulator/src
python3.12 -m venv venv
source venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt
