# About part two solution
I wouldn't have figured that one out without the internet. I thought this would be solved by keeping track of the
overall state and then some calculations. Turns out you just need to reduce the *worry level* to a small enough number.
This can be done by always taking the remainder with respect to the *product of all monkeys test number*. This keeps
the number nice and small and does not break downstream logic.