from lxml import html
import requests

debug = False

measurement_keywords = [
    "cup",
    "dash",
    "lb",
    "liter",
    "litre",
    "ounce",
    "oz",
    "pinch",
    "pound",
    "tbsp",
    "tsp",
]
direction_keywords = [
    "add",
    "bake",
    "boil",
    "brown",
    "chop",
    "cube",
    "degrees",
    "heat",
    "slice",
    "simmer",
    "stir",
    "until",
]

def get_parsed(url):
    page = requests.get(url)
    tree = html.fromstring(page.content)
    return tree

def keyword_score(tree, keywords):
    try:
        content = tree.text_content().lower()
    except ValueError:
        return 0
    return sum(map(lambda k: content.count(k), keywords))

def find_deepest_nested_keywords(tree, keywords):
    x = keyword_score(tree, keywords)
    print(tree, x)
    if debug:
        print(x)
    if x == 0:
        return None
    elif not tree.getchildren():
        return tree

    best_child_score = x/2  # we're looking for better than 50% in one place
    best_child = tree

    for c in tree.iterchildren():
        if debug:
            print("child", c)
        if keyword_score(c, keywords) == 0:  # mothing to see here, movee along
            continue

        best_in_branch = find_deepest_nested_keywords(c, keywords)
        if best_in_branch is None:  # should not hit this case bc we're only
                                    # going into branches that score nonzero
            print("wtf happened")
            continue

        branch_score = keyword_score(best_in_branch, keywords)
        if branch_score >= best_child_score:
            if debug:
                print("replacing")
            best_child_score = branch_score
            best_child = best_in_branch

    if best_child is None:
        print("Could not find keywords")

    return best_child
    

if __name__ == "__main__":
    tree = get_parsed('http://pixelatedcrumb.com/2011/03/06/prosciutto-and-sweet-potato-risotto')
    body = tree.getchildren()[1]  # TODO: this but better

    ingredients_block = find_deepest_nested_keywords(body, measurement_keywords)
    if ingredients_block is not None:
        print(ingredients_block.text_content().strip())
    else:
        print("could not identify ingredients by looking for common quantities")

    directions_block = find_deepest_nested_keywords(body, direction_keywords)
    if directions_block is not None:
        print(directions_block.text_content().strip())
    else:
        print("could not identify directions by looking for common directives")
