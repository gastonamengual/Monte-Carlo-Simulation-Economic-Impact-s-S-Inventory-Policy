# Monte Carlo Simulation of Economic Impact Using s,S Inventory Policy

This project was developed by Gastón Amengual and Ezequiel L. Castaño in college in 2020 as part of our academic work.
It was accepted and presented as a poster at the 8th National Congress on Computer Engineering / Information Systems (CoNaIISI 2020),
organized by RIISIC (CONFEDI) and hosted virtually by Universidad Tecnológica Nacional, Facultad Regional San Francisco, on November 5–6, 2020.

This project presents a discrete-event simulation model that evaluates the economic impact of different s,S inventory policy configurations on a business. The simulation integrates logistics (inventory control) and economic factors (capital flow), incorporating behavioral elements like dynamic customer response to pricing and stock availability.

🧠 Core Concepts
	•	s,S Inventory Policy: When inventory falls below s, order up to S.
	•	Monte Carlo Simulation: Thousands of runs model the stochastic behavior of customer arrivals, sales, and economic metrics.
	•	KPIs: Focused on capital level after a 6-month simulation.

⚙️ Methodology
	•	Event-based simulation: Tracks Customer Arrival, Control, and Order Arrival events.
	•	Parameters:
	•	Economic: Unit cost, profit margin, fixed costs.
	•	Logistics: Initial stock, order delays, stock ceilings.
	•	Behavioral: Customer arrival rate responds to satisfaction.
	•	Assumptions: Stable market, one product, no inflation, Poisson-based arrivals/sales.

🧪 Experiments

Simulations model 4 economic outcomes:
	1.	Profit without losses
	2.	Profit with intermediate losses
	3.	Break-even
	4.	Overall losses

Each scenario used Bayesian Optimization (Optuna) to tune inventory parameters.

📈 Results
	•	Optimal outcomes achieved with:
	•	Low control frequency
	•	High initial inventory
	•	High stock ceilings
	•	Capital variability increased over time, reflecting realistic uncertainty.
	•	No steady state was observed in any scenario.

🔧 Tech Stack
	•	Python (Numpy, Pandas, Matplotlib)
	•	Bayesian Optimization via Optuna
