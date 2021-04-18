
- Yağmur Mutluer 160709040
- 04142021 Web Mining Course

# Apriori Algorithm

Apriori algorithm for discovering frequent itemsets for mining association rules.


## Usage

- default minsup= 0.15 minconfidence = 0.6

```
python aprioriAlgorithm.py -f filename
```

- if you want to change the values

```
python aprioriAlgorithm.py -f filename -s value -c value

```

## Expected Output

- the output written in txt files. change file name to avoid overwrite.

```
Rule: ('41',) ==> ('39',) , 0.667
Rule: ('48',) ==> ('39',) , 0.723
Rule: ('38',) ==> ('39',) , 0.731
```

```
Rule: (' Coffee',) ==> ('Apple',) , 0.615
Rule: (' Kiwi',) ==> (' Eggs',) , 0.700
```
