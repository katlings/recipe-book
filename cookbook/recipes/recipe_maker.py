from lxml import html
import requests

debug = False

def get_parsed(url):
    page = requests.get(url)
    tree = html.fromstring(page.content)
    return tree

def find_ingredients(tree):
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

    def ingredient_score(e):
        try:
            content = e.text_content().lower()
        except ValueError:
            return 0
        return sum(map(lambda k: content.count(k), measurement_keywords))

    def find_deepest_nested_ingredients(e):
        x = ingredient_score(e)
        if debug:
            print(x)
        if x == 0:
            return None
        elif not e.getchildren():
            return e

        best_child_score = x
        best_child = e

        for c in e.iterchildren():
            if debug:
                print("child", c)
            if ingredient_score(c) == 0:
                continue
            best_in_branch = find_deepest_nested_ingredients(c)
            if best_in_branch is None:  # should not hit this case bc we're only
                                        # going into branches that score nonzero
                print("wtf happened")
                continue
            branch_score = ingredient_score(best_in_branch)
            if branch_score >= best_child_score:
                if debug:
                    print("replacing")
                best_child_score = branch_score
                best_child = best_in_branch

        if best_child is None:
            print("Could not identify ingredients through common quantities")

        return best_child
    
    return find_deepest_nested_ingredients(tree.getchildren()[1])


if __name__ == "__main__":
    tree = get_parsed('http://pixelatedcrumb.com/2011/03/06/prosciutto-and-sweet-potato-risotto')
    ingredients_block = find_ingredients(tree)
    if ingredients_block is not None:
        print(ingredients_block.text_content())
    else:
        print("ingredients not found")
