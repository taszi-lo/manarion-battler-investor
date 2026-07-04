from meow import Battler

if __name__ == "__main__":

    name = "mizarc" # Put your name in quotation marks here.
    tax = 25 # Put your dust tax % here.
    mob_shift = 350 # Leave it 300 unless you know what you're doing.

    battler = Battler(
        name = name,
        tax = tax,
        mob_shift= mob_shift,
    )

    # Display upgrade efficiencies.
    battler.visualizer()
