import random
from typing import List, Dict, Any, Tuple
from enum import Enum


class Symbol(Enum):
    """Symbols that can appear on a slot machine reel."""

    CHERRY = "🍒"
    LEMON = "🍋"
    GRAPES = "🍇"
    WATERMELON = "🍉"
    BELL = "🔔"
    SEVEN = "7️⃣"


class SlotMachine:
    """
    Represents a slot machine with multiple reels.

    Attributes:
        reels (int): Number of reels in the machine.
        symbols_per_reel (int): Number of symbols on each reel.
        symbols (List[List[Symbol]]): Symbols on each reel.
        paytable (Dict[Tuple[Symbol, ...], int]): Payout for each winning combination.
    """

    def __init__(self, reels: int = 3, symbols_per_reel: int = 10):
        """
        Initialize a new slot machine.

        Args:
            reels (int, optional): Number of reels. Defaults to 3.
            symbols_per_reel (int, optional): Number of symbols per reel. Defaults to 10.
        """
        self.reels = reels
        self.symbols_per_reel = symbols_per_reel
        self.symbols = self._initialize_reels()
        self.paytable = self._initialize_paytable()

    def _initialize_reels(self) -> List[List[Symbol]]:
        """
        Initialize the symbols on each reel.

        Returns:
            List[List[Symbol]]: Symbols for each reel.
        """
        symbols = []
        all_symbols = list(Symbol)
        weights = {
            Symbol.CHERRY: 20,
            Symbol.LEMON: 15,
            Symbol.GRAPES: 15,
            Symbol.WATERMELON: 12,
            Symbol.BELL: 10,
            Symbol.SEVEN: 5,
        }

        for _ in range(self.reels):
            reel_symbols = []
            for _ in range(self.symbols_per_reel):
                # Weighted random selection
                total = sum(weights.values())
                r = random.randint(1, total)
                for symbol, weight in weights.items():
                    r -= weight
                    if r <= 0:
                        reel_symbols.append(symbol)
                        break
            symbols.append(reel_symbols)

        return symbols

    def _initialize_paytable(self) -> Dict[Tuple[Symbol, ...], int]:
        """
        Initialize the paytable with winning combinations and payouts.

        Returns:
            Dict[Tuple[Symbol, ...], int]: Paytable mapping combinations to payouts.
        """
        paytable = {}

        # Three of the same fruit (10x)
        paytable[(Symbol.CHERRY, Symbol.CHERRY, Symbol.CHERRY)] = 10
        paytable[(Symbol.LEMON, Symbol.LEMON, Symbol.LEMON)] = 10
        paytable[(Symbol.GRAPES, Symbol.GRAPES, Symbol.GRAPES)] = 10
        paytable[(Symbol.WATERMELON, Symbol.WATERMELON, Symbol.WATERMELON)] = 10
        
        # Three bells (25x)
        paytable[(Symbol.BELL, Symbol.BELL, Symbol.BELL)] = 25
        
        # Three sevens (100x)
        paytable[(Symbol.SEVEN, Symbol.SEVEN, Symbol.SEVEN)] = 100

        return paytable

    def spin(self) -> Tuple[List[Symbol], int]:
        """
        Spin the reels and determine the outcome.

        Returns:
            Tuple[List[Symbol], int]: The resulting symbols and the payout.
        """
        result = []
        for reel in self.symbols:
            result.append(random.choice(reel))

        payout = self._calculate_payout(result)
        return result, payout

    def _calculate_payout(self, result: List[Symbol]) -> int:
        """
        Calculate the payout for a given result.

        Args:
            result (List[Symbol]): The symbols from the spin.

        Returns:
            int: The payout amount.
        """
        # Check for exact matches in paytable (3 of a kind)
        if tuple(result) in self.paytable:
            return self.paytable[tuple(result)]

        # Check for 3 different fruits (3x multiplier)
        fruit_symbols = [
            Symbol.CHERRY, 
            Symbol.LEMON, 
            Symbol.GRAPES, 
            Symbol.WATERMELON
        ]
        
        # Check if all symbols are fruits
        if all(symbol in fruit_symbols for symbol in result):
            # Check if they're all different fruits
            if len(set(result)) == 3:
                return 3
        
        return 0

    def simulate_game(self, bet: int = 1) -> Dict[str, Any]:
        """
        Simulate one game (spin) of the slot machine.

        Args:
            bet (int, optional): The bet amount. Defaults to 1.

        Returns:
            Dict[str, Any]: Results of the simulation including symbols and winnings.
        """
        result, payout = self.spin()

        return {
            "bet": bet,
            "result": [symbol.value for symbol in result],
            "payout": payout,
            "net_win": payout * bet - bet,  # Multiply payout by bet and subtract bet
            "win": payout > 0,
        }
