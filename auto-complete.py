import json
from string import ascii_letters, ascii_lowercase


queries = []
trie_list = {}
cursor = 0


def load():
    global queries, trie_list
    print("loading data 1 2 3.....\n")
    files = {letter: 'trie_' + letter + '.json' for letter in ascii_lowercase + ' '}
    queries = json.load(open("queries.json"))
    for letter, file in files.items():
        trie_list[letter] = json.load(open(file))[0]


class AutoComplete:
    def __init__(self, completed_string, source_text, offset, score):
        self.completed_string = completed_string
        self.source_text = source_text
        self.offset = offset
        self.score = score


def simplify_query(query):
    query = ' '.join(query.split())
    query = [letter.lower() for letter in query if letter in ascii_letters + ' ']
    return query


def get_info(completions):
    return [AutoComplete(queries[completion[0]][0],
                         queries[completion[0]][1],
                         completion[1],
                         completion[2]) for completion in completions]


def find_substrings(query):
    global cursor
    found_queries = []

    for letter in query:
        if letter in cursor['dict']:
            cursor = cursor['dict'][letter]
        else:
            break
    else:
        found_queries = cursor['completions']

    result = get_info(found_queries)
    return result


def print_matches(matches, query):
    for i, match in enumerate(matches):
        print(i + 1,
              match.completed_string[:match.offset] +
              match.completed_string[match.offset: match.offset + len(query)] +
              match.completed_string[match.offset + len(query):],
              '(', f'\033[94m{match.source_text}\033[00m', ')', f'\033[91m{match.score}\033[00m')


def find_top_five(query):
    query = simplify_query(query)
    substrings = find_substrings(query)
    print_matches(substrings, query)


def get_input():
    global cursor
    string = input("Please enter a search: ")
    cursor = trie_list[string[0]]
    find_top_five(string[:8])

    while True:
        print()
        str_ = input(string)
        if str_[-1] == '#':
            return
        if len(string) >= 8:
            get_info(cursor['completions'])
        else:
            find_top_five(str_[:8 - len(string)])
        find_top_five(str_)
        string += str_


def main():
    load()
    print("Click ctrl c to exit\n")
    while True:
        get_input()


if __name__ == '__main__':
    main()
