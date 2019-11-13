# Propositional logic reasoner

This mini-project was developed for the Artificial Intelligence and Decision Systems course at Instituto Superior Técnico (IST). A propositional logic reasoner based on the Resolution principle consists of the following key elements: 
* a program to convert logical sentences in propositional logic into the clausal normal form (CNF) 'convert.py'
* a resolution-based theorem prover for propositional logic, assuming a CNF knowledge base 'prove.py'

Read the [assignment description](assignment-details.pdf) for more details.

## Running the tests
The CNF convertor ('convert.py') should read from stdin sentences, one per line, and output to stdout disjunctions, one per line. Example usage:
```
python convert.py < sentences.txt 
```

The theorem prover ('prove.py') should read from stdin CNF clauses, one per line, using the same format of the CNF convertor output
```
python3 prover.py < cnf.txt 
```

Both programs should work in tandem, that is,the output of 'convert.py' can be directly fed into 'prove.py' using shell pipes
```
python3 convert.py < problem.txt | python3 prover.py
```
## Authors

* **Henrique Ferreira** - [GitHub](https://github.com/henriquebferreira)
* **Manuel Rosa** - [GitHub](https://github.com/ManuelDCR)

*Developed in 2017, Instituto Superior Técnico - Universidade de Lisboa*

## License

This project is licensed under the BSD 3-Clause "New" or "Revised" License - see the [LICENSE](LICENSE) file for details