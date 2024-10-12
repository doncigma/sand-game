from SandGame import SandGame

def test_cases():
        game = SandGame((5, 5), 20)
        
        # Place block test
        print("BLOCK PLACE AND ROCK OVERRIDE TEST")
        game.place_block("S", 2, 2)
        print("Sand place", (2, 2), game.get_block(2, 2))

        game.place_block("R", 2, 2)
        print("Rock place", (2, 2), game.get_block(2, 2))

        # Gravity test
        game.__reset_game_world__()
        print("\n", "GRAVITY AND LAND ON ROCK TEST")
        game.place_block("S", 2, 2)
        print("Sand place", (2, 2), game.get_block(2, 2))

        game.place_block("R", 2, 4)
        print("Rock place", (2, 4), game.get_block(2, 4))

        game.__apply_gravity_on_block__(2, 2)
        print("Block after gravity", (2, 3), game.get_block(2, 3))

        # Brownian test
        game.__reset_game_world__()
        print("\n", "BROWNIAN TEST")
        game.place_block("S", 2, 2)
        print("Sand place", game.get_block(2, 2))

        game.__apply_brownian_on_block__(2, 2)
        print("Brownian check", game.get_block(1, 2))
        print("Brownian check", game.get_block(3, 2))

        # Bottom test
        game.__reset_game_world__()
        print("\n", "BOTTOM TEST")
        game.place_block("S", 2, 3)
        print("Sand place", (2, 3), game.get_block(2, 3))

        game.__apply_gravity_on_block__(2, 3)
        print("Block after gravity", (2, 4), game.get_block(2, 4))

        game.__apply_gravity_on_block__(2, 4)
        print("Block after gravity", (2, 4), game.get_block(2, 4))

        # Edge test
        game.__reset_game_world__()
        print("\n", "EDGE TEST")
        game.place_block("S", 3, 2)
        print("Sand place", (3, 2), game.get_block(3, 2))
        
        # Simplified brownian function from SandGame to eliminate randomness
        def test_brownian(x, y):
            if game.can_move("S", x+1, y):
                game.place_block("S", x+1, y)
                game.remove_block(x, y)

        game.__apply_brownian_on_block__ = test_brownian

        game.__apply_brownian_on_block__(3, 2)
        print("Block after brownian", (4, 2), game.get_block(4, 2))

        game.__apply_brownian_on_block__(4, 2)
        print("Block after brownian", (4, 2), game.get_block(4, 2))

if __name__ == "__main__":
    test_cases()