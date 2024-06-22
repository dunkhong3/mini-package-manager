from add import add
from install import install


if __name__ == '__main__':
    # modify these lines to test

    # this is a simple test but it shows we can avoid circular dependencies
    # A@1.0.0 -> B@2.0.0 -> D@1.1.0 -> A@1.0.0
    # since we used DFS with visited nodes, we will not revisit A@1.0.0 again
    add("A@1.0.0")
    add("C@1.1.0")
    install()
