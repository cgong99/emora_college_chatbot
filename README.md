# State Transition Dialogue Manager

Defines a dialogue management framework based on state machines and 
regular expressions. 

## Installation

Users install using `pip install emora_stdm`

Developers install using:
```
git clone https://github.com/emora-chat/emora_stdm.git
pip install -r emora_stdm/requirements.txt
```

## Example usage

```python
from emora_stdm import DialogueFlow

# create a new dialogue manager and specify start state
df = DialogueFlow(initial_state='begin')

# add type-subtype relations to the ontology
# (abstract types should be marked with '&')
df.knowledge_base().add_type('dog', '&animal')
df.knowledge_base().add_type('cat', '&animal')

# load knowledge base contents from json
# (see Knowledge Base and Ontology section)
with open('kb.json', 'r') as f:
    df.knowledge_base().load_json(f.read())

# define all states of the dialogue state machine
df.add_states([
    'begin',
    'pet_chat_state',
    'movie_chat_state',
])

# add transitions to the dialogue state machine
df.add_transition(
    'begin', 'movie_chat_state',
    [
        '({movie, movies, film, films})'
    ],
    {
        'i like movies',
        'i watch movies'
    }
)

df.add_transition(
    'begin', 'pet_chat_state',
    [
        'i have a &animal'
    ],
    {
        'i have a dog'
    }
)

df.add_transition(
    'movie_chat_state', 'begin',
    [], {'cool'}, settings='e'
)

df.add_transition(
    'pet_chat_state', 'begin',
    [], {'pets are great'}, settings='e'
)

df.add_transition(
    'begin', 'begin', [], {}, settings='e'
)

# validate the DialogueFlow
df.check_error_transitions_complete()

# talk to your dialogue agent in a loop
while True:
    i = input('U: ')
    df.user_transition(i)
    print('S:', df.system_transition())
```

Class `DialogueFlow` is the main class to initialize. It defines
a state machine that drives natural language conversation. State
transitions in the state machine (alternately) represent either 
system or user turns.

`dialogue_manager = DialogueFlow('start')`
initializes a new `DialogueFlow` object with `'start'` as the 
initial state of the state machine.

All states must be specified before they are used in a transition by calling the `.add_state(state)`
method. Each state is defined as a string literal like the following:

`
dialogue_manager.add_state('start')
`

Alternatively, multiple states can be added at once using the `.add_states(states)` method where `states`
is a list of string literals, like the following:

`
dialogue_manager.add_states(['feelings_pos', 'feelings_pos_reason'])
`

To add transitions, use:
```.add_transition(source, target, NLU, NLG_list)``` method like the 
following:
```
dialogue_manager.add_transition(
    'feelings_pos', 'feelings_pos_reason',
    '{(what, &feelings_positive, {part, most, best}),'
    '(you, &feelings_positive)}',
    ['what excites you the most']
)
```
where the first two arguments are the source and target states of 
the transition, the third argument is a string that defines a set 
of natural language expressions given by a user that satisfy the 
transition (see below), and the fourth argument is a list of natural 
language expressions that the system selects as a response when
taking this transition during its turn.

If you want to define a function that is used to evaluate satisfaction of the transition, instead of
(or in addition to) the natural language expressions, you can pass the function name in as the 
optional fifth parameter `evaluation_function` of the `.add_transition` method.

Similarly, if you want to define a function that is ran upon selection of a transition, such as
to update the current variables (see below), you can pass the function name in as the 
optional sixth parameter `selection_function` of the `.add_transition` method.

A user turn can be taken, updating state, using
```
dialogue_manager.user_transition(input)
```
where input is a string representing the user utterance.

A system turn can be taken using
```
dialogue_manager.system_transition()
```


## NLU Expressions

Strings created for transition NLU define a set of user expressions
that satisfy the transition by compiling into regular expressions.
These expressions can be formed using the below constructs, which
are all arbitrarily nestable and concatenable:

### Literal
```
'hello there'
```
directly match the user utterance "hello there"

### Disjunction
```
'{hello there, hi}'
```
matches if the utterance contains any term inside `{}`, in this case 
"hello there", "hi", "hi hello there", and "oh hi bob" all match

### Conjunction
```
'<bob, hi>'
```
matches as long as the utterance contains all terms inside `<>`,
in this case, "hi bob" and "oh bob hi" both would match, but not
"hi"

### Negation
```
i am -bad
```
prepend `-` to negate the next term in the expression. The example
will match any expression starting with "i am" where "bad" does NOT
follow. Note that the scope of the negation extends to the end
of the utterance due to limitations in regex.

### Flexible sequence
```
'(hi, bob, how, you)'
```
matches as long as the utterance contains all terms inside `()`,
and the terms are ordered properly within the utterance. Matches
in the example include "hi bob how are you", but not "how are you 
bob"

### Inflexible sequence
```
'[how, are, you]'
```
matches an exact sequence of terms with no words inserted between
terms. The only utterance matching the example is "how are you"

### Regular expression
```
'/[A-Z a-z]+/'
```
substrings within `//` define a python regex

### Nesting
```
'[{hi, hello} (how /is|was/ weekend)]'
```
would match "hi how was your weekend", "oh hello, so how is the
weekend going", ...

### Variable assignment
```
'i am %f={good, bad}'
```
using `%var=` will assign variable `var` to the next term in
the expression. The variable will persist until overwritten,
and can be referenced in future NLU or NLG expressions.
The example would match either "i am good" or "i am bad", and
assigns variable "f" to either "good" or "bad" depending
on what the user said.

### Variable reference
```
why are you $f today
```
using `$` references a previously assigned variable. If no such
variable exists, the expression as a whole returns with no match.
The example would match "why are you good today" if `f="good"`, 
but would not match if `f="bad"`

## If NLU debugging gets tricky
For a precise understanding of the NLU expressions you produce,
you can view the compiled python regex like so:
```
print(dialogue_manager.graph().arc(source, target).re)
```
And then debug at https://regex101.com/ (make sure to switch to
python regexes)

## Knowledge base and ontology

The Knowledge Base and Ontology are optional components of the 
dialogue manager that allow you to write more generalizable
transitions. 

The Knowledge Base and Ontology are modeled as a unified (single)
directed graph. You specify the knowledge and ontology elements you 
need by updating the `database.json` file.

The Knowledge Base is defined as a list of predicates, 
where a predicate is stored as a list `[subject, relation, object]`.

```
'predicates': [
    ['dog', 'sound', 'bark'],
    ['bark', 'quality', 'annoying'],
    ['scarlett johansson', 'plays', 'black widow']
]
```

The Ontology is defined as a mapping between categories and a list of elements of that category. 
The category string must always begin with the ampersand symbol: `&`.

```
'ontology': {
    '&feeling': ['sad', 'happy', 'angry'],
    '&animal': ['dog', 'cat', 'bird']
}
```

Taking these two structures together, the final `database.json` for this example would look 
like the following:

```
{
'predicates': [
        ['dog', 'sound', 'bark'],
        ['bark', 'quality', 'annoying'],
        ['scarlett johansson', 'plays', 'black widow']
    ],
'ontology': {
        '&feeling': ['sad', 'happy', 'angry'],
        '&animal': ['dog', 'cat', 'bird']
    }
}
```

### Ontology reference
```
'i am &feeling'
```
Using a prepended `&` references a node in the ontology. Any 
subtype of the referenced node can be matched in the expression.

### Knowledge base reference
```
'a dog can #dog:sound#'
```
substrings encapsulated within `##` reference a set of nodes in the knowledge
graph. The set is created by starting at the node defined before
the initial `:`, then traversing arcs labeled by each subsequent
term following `:`. In this case, all nodes related to "dog" by
a "sound" arc are valid matches. For example, the utterances "a
dog can bark" and "a dog can growl" might be matched if "bark" and
"growl" were present in the knowledge graph.

```
'a dog is #dog:sound:quality#'
```
knowledge base expressions can chain multiple predicates together.
suppose the predicates `sound(dog, bark)` and `quality(bark, annoying)`
were present in the knowledge base. The expression would match 
"a dog is annoying"

```
'black widow is played by #black widow:/plays#'
```
using `/` reverses the direction of a knowledge graph relation. If
`plays(scarlett johansson, black widow)` is present in the KB, then
the above expression matches "black widow is played by scarlett 
johansson"

```
'a %a=&animal, can #$a:sound#'
```
knowledge graph expressions can be built using veriable references.
Together with ontology reference, highly generalizable expressions
can be written. Given an appropriately constructed KB and ontology,
this example might match "a cow can moo", "a dog can bark", and
everything in between.
