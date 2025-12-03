class Ingredient:
    def __init__(self, capacity: int, durability: int, flavor: int, texture: int, calories: int):
        self._capacity = capacity
        self._durability = durability
        self._flavor = flavor
        self._texture = texture
        self._calories = calories

    @property
    def capacity(self):
        return self._capacity

    @property
    def durability(self):
        return self._durability

    @property
    def flavor(self):
        return self._flavor

    @property
    def texture(self):
        return self._texture

    @property
    def calories(self):
        return self._calories


def main(use_calorie_gate: bool):
    sprinkles = Ingredient(capacity=2, durability=0, flavor=-2, texture=0, calories=3)
    butterscotch = Ingredient(capacity=0, durability=5, flavor=-3, texture=0, calories=3)
    chocolate = Ingredient(capacity=0, durability=0, flavor=5, texture=-1, calories=8)
    candy = Ingredient(capacity=0, durability=-1, flavor=0, texture=5, calories=8)

    best_score = 0

    for spoons_sprinkles in range(101):
        for spoons_butterscotch in range(101 - spoons_sprinkles):
            for spoons_chocolate in range(101 - spoons_sprinkles - spoons_butterscotch):
                for spoons_candy in range(101 - spoons_sprinkles - spoons_butterscotch - spoons_chocolate):
                    if spoons_sprinkles + spoons_butterscotch + spoons_chocolate + spoons_candy != 100:
                        continue

                    calories = (
                        spoons_sprinkles * sprinkles.calories
                        + spoons_butterscotch * butterscotch.calories
                        + spoons_chocolate * chocolate.calories
                        + spoons_candy * candy.calories
                    )
                    if use_calorie_gate and calories != 500:
                        continue

                    capacity_score = max(
                        spoons_sprinkles * sprinkles.capacity
                        + spoons_butterscotch * butterscotch.capacity
                        + spoons_chocolate * chocolate.capacity
                        + spoons_candy * candy.capacity,
                        0
                    )
                    durability_score = max(
                        spoons_sprinkles * sprinkles.durability
                        + spoons_butterscotch * butterscotch.durability
                        + spoons_chocolate * chocolate.durability
                        + spoons_candy * candy.durability,
                        0
                    )
                    flavor_score = max(
                        spoons_sprinkles * sprinkles.flavor
                        + spoons_butterscotch * butterscotch.flavor
                        + spoons_chocolate * chocolate.flavor
                        + spoons_candy * candy.flavor,
                        0
                    )
                    texture_score = max(
                        spoons_sprinkles * sprinkles.texture
                        + spoons_butterscotch * butterscotch.texture
                        + spoons_chocolate * chocolate.texture
                        + spoons_candy * candy.texture,
                        0
                    )

                    score = capacity_score * durability_score * flavor_score * texture_score
                    if score > best_score:
                        best_score = score

    print(best_score)


if __name__ == "__main__":
    main(False)
    main(True)
