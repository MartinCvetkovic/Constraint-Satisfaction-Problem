import copy


class Algorithm:
    def get_algorithm_steps(self, tiles, variables, words):
        pass


class ExampleAlgorithm(Algorithm):
    def get_algorithm_steps(self, tiles, variables, words):
        moves_list = [['0h', 0], ['0v', 2], ['1v', 1], ['2h', 1], ['4h', None],
                      ['2h', None], ['1v', None], ['0v', 3], ['1v', 1], ['2h', 1],
                      ['4h', 4], ['5v', 5]]
        domains = {var: [word for word in words] for var in variables}
        solution = []
        for move in moves_list:
            solution.append([move[0], move[1], domains])
        return solution


class Backtracking(Algorithm):
    def get_algorithm_steps(self, tiles, variables: dict, words: list):
        tilesCol = len(tiles[0])
        domains = {var: [word for word in words] for var in variables}
        for variable in variables.keys():
            for word in words:
                if len(word) != variables[variable]:
                    domains[variable].remove(word)
        localSolution = copy.deepcopy(domains)

        variableIndex = 0
        variablesKeys = list(variables.keys())
        solution = []
        usedWords = []
        usedVariables = []
        localSolutions = []
        isBacktracking = False
        while variableIndex < len(variablesKeys):
            variable: str = variablesKeys[variableIndex]
            isHorizontal = True if variable[-1] == 'h' else False
            position = int(variable[0:-1])
            value = None
            for word in localSolution[variable]:
                wordMatches = True
                for char in word:
                    i = position // tilesCol
                    j = position % tilesCol
                    if isinstance(tiles[i][j], str) and char != tiles[i][j]:
                        wordMatches = False
                        break
                    if isHorizontal:
                        position += 1
                    else:
                        position += tilesCol
                if not wordMatches:
                    continue
                value = word
                if wordMatches and isBacktracking:
                    isBacktracking = False
                    localSolution = copy.deepcopy(domains)
                break

            if value is not None:
                usedWords.append(value)
                usedVariables.append(variable)
                solution.append([variable, domains[variable].index(value), domains])
                localSolutions.append(localSolution)

                position = int(variable[0:-1])
                for char in value:
                    tiles[position // tilesCol][position % tilesCol] = char
                    if isHorizontal:
                        position += 1
                    else:
                        position += tilesCol

                variableIndex += 1
            else:
                solution.append([variable, None, domains])
                value = usedWords.pop()
                variable: str = usedVariables.pop()
                localSolution = localSolutions.pop()
                localSolution[variable].remove(value)

                isHorizontal = True if variable[-1] == 'h' else False
                position = int(variable[0:-1])
                firstLetter = True
                i = position // tilesCol
                j = position % tilesCol
                if isHorizontal and (i == 0 and j == 0 or i > 0 and not isinstance(tiles[i - 1][j], str)):
                    for _ in value:
                        tiles[i][j] = False
                        j += 1
                elif not isHorizontal and (i == 0 and j == 0 or j > 0 and not isinstance(tiles[i][j - 1], str)):
                    for _ in value:
                        if not firstLetter:
                            tiles[i][j] = False
                        firstLetter = False
                        i += 1

                isBacktracking = True
                variableIndex -= 1
        return solution


# variables = {'0h': 2, '0v': 3, '1v': 1, '2h': 1, '4h': 2, '5v': 1}
class ForwardChecking(Algorithm):
    def get_algorithm_steps(self, tiles, variables: dict, words: list):
        tilesCol = len(tiles[0])
        domains = {var: [word for word in words] for var in variables}
        for variable in variables.keys():
            for word in words:
                if len(word) != variables[variable]:
                    domains[variable].remove(word)
        localSolution = copy.deepcopy(domains)

        variableIndex = 0
        variablesKeys = list(variables.keys())
        solution = []
        usedWords = []
        usedVariables = []
        localSolutions = []
        isBacktracking = False
        while variableIndex < len(variablesKeys):
            variable: str = variablesKeys[variableIndex]
            isHorizontal = True if variable[-1] == 'h' else False
            position = int(variable[0:-1])
            value = None
            for word in localSolution[variable]:
                wordMatches = True
                for char in word:
                    i = position // tilesCol
                    j = position % tilesCol
                    if isinstance(tiles[i][j], str) and char != tiles[i][j]:
                        wordMatches = False
                        break
                    if isHorizontal:
                        position += 1
                    else:
                        position += tilesCol
                if not wordMatches:
                    continue
                value = word
                if wordMatches and isBacktracking:
                    isBacktracking = False
                    localSolution = copy.deepcopy(domains)
                break

            if value is not None:
                usedWords.append(value)
                usedVariables.append(variable)
                solution.append([variable, domains[variable].index(value), domains])
                localSolutions.append(localSolution)

                position = int(variable[0:-1])
                for char in value:
                    tiles[position // tilesCol][position % tilesCol] = char
                    if isHorizontal:
                        position += 1
                    else:
                        position += tilesCol

                variableIndex += 1
            else:
                solution.append([variable, None, domains])
                value = usedWords.pop()
                variable: str = usedVariables.pop()
                localSolution = localSolutions.pop()
                localSolution[variable].remove(value)

                isHorizontal = True if variable[-1] == 'h' else False
                position = int(variable[0:-1])
                firstLetter = True
                i = position // tilesCol
                j = position % tilesCol
                if isHorizontal and (i == 0 and j == 0 or i > 0 and not isinstance(tiles[i - 1][j], str)):
                    for _ in value:
                        tiles[i][j] = False
                        j += 1
                elif not isHorizontal and (i == 0 and j == 0 or j > 0 and not isinstance(tiles[i][j - 1], str)):
                    for _ in value:
                        if not firstLetter:
                            tiles[i][j] = False
                        firstLetter = False
                        i += 1

                isBacktracking = True
                variableIndex -= 1
        return solution
