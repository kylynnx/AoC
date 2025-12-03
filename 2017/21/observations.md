# Observations

The initial position is a size `3` grid, that is enhanced into a size `4` grid:

```
...    ....
... => ....
...    ....
       ....
```

In the next iteration that grid is split into `4` size `2` grids. We denote the grids and their results with numbers:

```
         111|222
11|22    111|222
11|22    111|222
----- => -------
33|44    333|444
33|44    333|444
         333|444
```

For the next enhancement the resulting size `6` grid is split into smaller size `2` grids. Here we keep the numbers from
above, we will rename these squares in an intermediate step:

```
                        aaa|bbb|ccc
11|12|22    aa|bb|cc    aaa|bbb|ccc
11|12|22    aa|bb|cc    aaa|bbb|ccc
--------    --------    -----------
11|12|22    dd|ee|ff    ddd|eee|fff
33|34|44 => dd|ee|ff => ddd|eee|fff
--------    --------    ddd|eee|fff
33|34|44    gg|hh|ii    -----------
33|34|44    gg|hh|ii    ggg|hhh|iii
                        ggg|hhh|iii
                        ggg|hhh|iii
```

From this point the sequence repeats for the `9` size `3`grids, which can now be evolved individually. Note that this is
feasible since the size of the final state is follows the form `s = 9^(epoch) * 3 = 3^(2 * epoch + 1)`, where `epoch`
counts the iteration over one of the cycles shown above. Hence, the final state will never mix the resulting size `3`
grids. Additionally, in the intermediate steps only splits into size `2` grids are happening, which also prevents any
mixing of the sectors named `a-i` above.

Finally, it suffices to determine this cycle for **all** possible size `3` grids (there are `2^9 = 512`), noting down
which `9` grids make up their final state, and how many cells were on for the intermediate steps.
