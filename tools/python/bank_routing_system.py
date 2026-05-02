"""
NetworkBuster Bank Routing System
Simulates the routing of program payouts and grant funds.
"""

import json
from datetime import datetime
from pathlib import Path
from resident_strategy_engine import StrategicWealthManager, Resident

class BankRoutingSystem:
    """Manages simulated fund routing for the NetworkBuster project."""
    
    def __init__(self, ledger_path="PROJECT_LEDGER.json"):
        self.ledger_path = Path(ledger_path)
        self.wealth_manager = StrategicWealthManager()
        self.load_ledger()

    def load_ledger(self):
        """Loads or initializes the project ledger."""
        if self.ledger_path.exists():
            with open(self.ledger_path, 'r') as f:
                self.ledger = json.load(f)
        else:
            self.ledger = {
                "account_owner": "Andrew Middleton",
                "organization": "NetworkBuster Research Division",
                "balance": 0.0,
                "currency": "USD",
                "routing_history": [],
                "status": "ACTIVE"
            }
            self.save_ledger()

    def save_ledger(self):
        """Saves the current state of the ledger."""
        with open(self.ledger_path, 'w') as f:
            json.dump(self.ledger, f, indent=2)

    def route_funds(self, amount: float, source: str, description: str):
        """Routes funds to the primary project account."""
        timestamp = datetime.now().isoformat()
        
        transaction = {
            "timestamp": timestamp,
            "amount": amount,
            "source": source,
            "description": description,
            "transaction_id": f"NB-RT-{int(datetime.now().timestamp())}"
        }
        
        self.ledger["balance"] += amount
        self.ledger["routing_history"].append(transaction)
        
        # Update the resident simulation net worth
        for resident in self.wealth_manager.residents:
            if "Andrew" in resident.name:
                resident.net_worth += amount
                print(f"✅ Simulation Sync: Andrew's Net Worth updated to ${resident.net_worth:,.2f}")

        self.save_ledger()
        
        print(f"🚀 Routing Successful!")
        print(f"   Amount: ${amount:,.2f}")
        print(f"   Target: Project Core Account (Andrew Middleton)")
        print(f"   Balance: ${self.ledger['balance']:,.2f}")
        
        return transaction

def main():
    # Simulate the SBIR Ignite Payout Routing
    router = BankRoutingSystem()
    
    # Valuations based on BUDGET_AND_DETAILS.md (using Enterprise Growth tier as milestone value)
    payout_amount = 5236.00 
    
    router.route_funds(
        amount=payout_amount,
        source="SBIR Ignite Program / NASA",
        description="M2M-01 Milestone Payout - Phase 12 Completion"
    )

if __name__ == "__main__":
    main()
