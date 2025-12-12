# What in the Math is going on here?

Let $r$ be the number of repetition, $l$ be the length of the repeated number, and $a,b,a_n$ be single digits. Then the
invalid IDs take the form:

| $r\rightarrow$ $l\downarrow$ | $2$                                                 | $3$                                                                                                                       | $r$                                                                    |
|------------------------------|-----------------------------------------------------|---------------------------------------------------------------------------------------------------------------------------|------------------------------------------------------------------------|
| $1$                          | $aa = a * (10 + 1)$                                 | $aaa = a \cdot \left(10^2 + 10 + 1\right)$                                                                                | $a \cdot \sum\limits_{n = 0}^{r - 1} 10^{1 \cdot n}$                   |
| $2$                          | $abab = ab \cdot (10^2 + 1)$                        | $ababab = ab \cdot \left(10^4 + 10^2 + 1\right)$                                                                          | $ab \cdot \sum\limits_{n = 0}^{r - 1} 10^{2 \cdot n}$                  |
| $l$                          | $a_{l-1}\dots a_0a_{l-1}\dots a_0 \cdot (10^l + 1)$ | $a_{l -1}\dots a_{0}a_{l -1}\dots a_{0}a_{l -1}\dots a_{0} = a_{l -1}\dots a_{0} \cdot \left(10^{2l} + 10^{l} + 1\right)$ | $a_{l -1}\dots a_{0} \cdot \sum\limits_{n = 0}^{r - 1} 10^{l \cdot n}$ |

where the conditions on the coefficients $a_l$ need to be determined. For the invalid ID not to begin with a $0$ it is
obvious that $a_{l-1} > 0$.

Let $A_l = a_{l-1}\dots a_0 = \sum\limits_{n = 0}^{l - 1} a_n \cdot 10^{n}$. From the condition for $a_{l-1}$ it can be
deduced that $A_l \ge 10^{l-1}$. As all $a_n$ are single digits the maximal factor is trivially given by
$A_l \le \sum\limits_{n = 0}^{l - 1} 9 \cdot 10^{n} = 10^{l} - 1$. Finally, let $A_l = \left\{x \mid x \in \mathbb{Z}
\land 10^{l-1} \le x \le 10^{l} - 1\right\}$

Let us introduce $R_{l,n} = \sum\limits_{n = 0}^{r - 1} 10^{l \cdot n}$ for the following considerations. Now for a
given range of IDs $[i_\text{min}, i_\text{max}]$, where we denote the length of the respective IDs $L_\text{min/max}$,
the invalid IDs are given as
$$
I = \bigcup\limits_{r=2}^{L_\text{max}}
  \bigcup\limits_{l=\text{max}\left\{1, \left\lfloor\frac{L_\text{min}}{r}\right\rfloor\right\}}
  ^{\left\lfloor\frac{L_\text{max}}{r}\right\rfloor}
  \left\{R_{l,n} \cdot a \mid a \in A_l\right\}
$$
