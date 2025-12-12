from math import prod


def main(filename: str):
    with open(filename) as f:
        content = f.read()

    *presents, regions = content.split("\n\n")
    present_sizes = [_.count("#") for _ in presents]

    fitting_regions = 0

    for region in regions.split("\n"):
        size, region_presents = region.split(": ")
        size = prod(int(_) for _ in size.split("x"))
        region_presents = [int(_) for _ in region_presents.split(" ")]
        regions_present_size = sum(amount * size for amount, size in zip(region_presents, present_sizes))

        if regions_present_size <= size:
            fitting_regions += 1

    print(f"Since Santa was nice in designing the regions, {fitting_regions} regions fit all the presents.")


if __name__ == "__main__":
    main("input.txt")
