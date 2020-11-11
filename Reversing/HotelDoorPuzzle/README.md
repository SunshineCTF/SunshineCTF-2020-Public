## [Reversing 100] Hotel Door Puzzle

Given a dynamically-generated key checker, generate the correct key for the program.

## Summary

The key-checker will be a mix of conditionals (key[0]='f') and modifications (key[0]++). The user will be given a binary in hex-format which they will then have to reverse engineer to find all conditions which the flag must satisfy. Along with this, the user is given a maxmimum of _N_ seconds to solve the challenge where _N_ is a given length based on network latency, etc... The user will then be forced use a SAT solver and other automation tools to generate the correct flag.

## Deployment

To deploy the challenge, modify `flag.txt` to contain the flag you want, then run `make build`. This will create `output.c` and compile it into `attachments/hotel_key_puzzle` which is the artifact to be given to the competitiors. I include an example I created which should be used for the competition, but new ones can be made if needed.

## Generation Mechanism

Each of the conditionals will follow one of the two formats:

1.) key[index] = 'f'

and

2.) key[index] = key[index] {+-*} {1-10}

As such, the general framework will be the same:

```c
seed = {Set of ASCII Characters of length equal to the length of the flag}

if(key[index] != 'f'){
	wrong();
}

key[index] = key[index] {+-*} {1-10}

if(key[index] != 'l'){
	wrong();
}

.
.
.

return give_flag();
```

As such, the generation and ordering of the conditionals and modifications are dynamic. This along with the timing mechanism will require a SAT solver and automation in order to solve for a key.

## Generation Mechanism Technicalities

Begin with the given flag: `FLAG`. 

The generator begins at the intial state with the unmodified flag. Pick a random number between 0 and 100. This will choose whether we do a check or a modification this round. We want a 70% chance of a modification and a 30% chance of a check. We will also keep track of all modified characters and ensure that each character is modified at least once.

### Why a Length Check is Unnecessary

At first, I thought I would need a length check in order for this challenge to work. This is because any string matching `FLAG{asdf}ANYTHING` would match. That is, so long as the string _began_ with the flag it would match the pattern. But, we do not care if more than the beginning of the string matches the flag. This would give away more information about the flag than we would want. As such, I have decided to not include a lenght check

### Modification

With a 70% chance, a modification round will be generated. One of the characters in the flag (unmodified prioritized before modified) will be chosen to be modified. Two more random parameters will be generated as well:

`operator => {+-*}`
`value => {1-10}`

From the randomly chosen operator and value, we can generate a C line which modifies the input.

`key[index] = key[index] {operator} {value}`

We also need to store any modifications (as in the post-modification character) in a current state store. This way we can tell what the current state of the mechanism is.

### Validation

With a 1% chance, a character of the flag will be validated for correctness at this state. This will be a fairly simple mechanism:

1. Look at current flag modification state.
2. Pick a character (prioritize not-yet-validated characters)
3. Check if the input matches the current state


### Finish
Complete validation and modification of the flag once at least every character has been validated and every character has been modified. 
