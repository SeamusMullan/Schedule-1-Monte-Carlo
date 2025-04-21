import play_blackjack
import play_rtb
import sys


def print_usage():
    print("Usage: python main.py [game]")
    print("Available games:")
    print("  blackjack - Run Blackjack simulations")
    print("  rtb       - Run Ride the Bus simulations")
    print("  all       - Run all simulations")


# Main entry point for all games
if __name__ == "__main__":
    if len(sys.argv) > 1:
        game = sys.argv[1].lower()
        
        if game == "blackjack":
            play_blackjack.main()
        elif game == "rtb":
            play_rtb.main()
        elif game == "all":
            play_blackjack.main()
            print("\n" + "=" * 60 + "\n")
            play_rtb.main()
        else:
            print(f"Unknown game: {game}")
            print_usage()
    else:
        print("No game specified.")
        print_usage()
        print("Please specify a game to run.")