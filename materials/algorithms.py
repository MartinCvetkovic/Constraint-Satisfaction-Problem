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


class ForwardChecking(Algorithm):
    def get_algorithm_steps(self, tiles, variables: dict, words: list):
        tilesCol = len(tiles[0])
        domains = {var: [word for word in words] for var in variables}
        for variable in variables.keys():
            for word in words:
                if len(word) != variables[variable]:
                    domains[variable].remove(word)
        localSolution = copy.deepcopy(domains)
        fullDomain = copy.deepcopy(domains)

        variableIndex = 0
        variablesKeys = list(variables.keys())
        solution = []
        usedWords = []
        usedVariables = []
        localSolutions = []
        localDomains = []
        isBacktracking = False
        while variableIndex < len(variablesKeys):

            shouldBacktrack = False
            for var, value in domains.items():
                if len(value) == 0:
                    shouldBacktrack = True
                    break

            variable: str = variablesKeys[variableIndex]
            isHorizontal = True if variable[-1] == 'h' else False
            position = int(variable[0:-1])
            value = None

            if not shouldBacktrack:
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
                position = int(variable[0:-1])
                for char in value:
                    i = position // tilesCol
                    j = position % tilesCol
                    tiles[i][j] = char
                    varsToChange = [str(position) + "h", str(position) + "v"]
                    for var in varsToChange:
                        if domains.get(var) is not None:
                            tempDomains = copy.deepcopy(domains[var])
                            val = domains.get(var)
                            for item in val:
                                if item[0] != char:
                                    tempDomains.remove(item)
                            domains[var] = tempDomains
                    if isHorizontal:
                        position += 1
                    else:
                        position += tilesCol

                usedWords.append(value)
                usedVariables.append(variable)
                solution.append([variable, domains[variable].index(value), copy.deepcopy(domains)])
                localSolutions.append(localSolution)
                localDomains.append(copy.deepcopy(domains))
                localSolution = copy.deepcopy(domains)
                variableIndex += 1
            else:
                if len(usedWords) > 0:
                    value = usedWords.pop()
                    variable: str = usedVariables.pop()
                    localSolution = localSolutions.pop()
                solution.append([variable, None, copy.deepcopy(domains)])
                if shouldBacktrack:
                    localDomains.pop()
                if len(localDomains) > 0:
                    domains = localDomains.pop()
                else:
                    domains = copy.deepcopy(fullDomain)
                    localSolution = copy.deepcopy(fullDomain)
                if len(localSolution) > 0:
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


class ArcConsistency(Algorithm):
    def get_algorithm_steps(self, tiles, variables: dict, words: list):
        tilesCol = len(tiles[0])
        domains = {var: [word for word in words] for var in variables}
        for variable in variables.keys():
            for word in words:
                if len(word) != variables[variable]:
                    domains[variable].remove(word)
        localSolution = copy.deepcopy(domains)
        fullDomain = copy.deepcopy(domains)

        variableIndex = 0
        variablesKeys = list(variables.keys())
        solution = []
        usedWords = []
        usedVariables = []
        localSolutions = []
        localDomains = []
        isBacktracking = False
        while variableIndex < len(variablesKeys):

            shouldBacktrack = False
            for var, value in domains.items():
                if len(value) == 0:
                    shouldBacktrack = True
                    break

            variable: str = variablesKeys[variableIndex]
            isHorizontal = True if variable[-1] == 'h' else False
            position = int(variable[0:-1])
            value = None

            if not shouldBacktrack:
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
                # Forward checking
                position = int(variable[0:-1])
                for char in value:
                    i = position // tilesCol
                    j = position % tilesCol
                    tiles[i][j] = char
                    varsToChange = [str(position) + "h", str(position) + "v"]
                    for var in varsToChange:
                        if domains.get(var) is not None:
                            tempDomains = copy.deepcopy(domains[var])
                            val = domains.get(var)
                            for item in val:
                                if item[0] != char:
                                    tempDomains.remove(item)
                            domains[var] = tempDomains
                    if isHorizontal:
                        position += 1
                    else:
                        position += tilesCol

                # Arc consistency
                arcChange = True
                while arcChange:
                    arcChange = False
                    inconsistentVars = []
                    for var1, words1 in domains.items():
                        for var2, words2 in domains.items():
                            if var1 == var2:
                                continue
                            var1Len = variables[var1]
                            var2Len = variables[var2]
                            var1Dir = var1[-1]
                            var2Dir = var2[-1]
                            var1Pos = int(var1[0:-1])
                            var2Pos = int(var2[0:-1])
                            if var1Dir == var2Dir:
                                continue

                            isNeighbor = False
                            acceptedWords = []
                            for word1 in words1:
                                for word2 in words2:
                                    word1Index = var1Pos
                                    word2Index = var2Pos
                                    char1Index = 0
                                    char2Index = 0
                                    while char1Index < var1Len and char2Index < var2Len:
                                        if word1Index < word2Index:
                                            if var1Dir == "h":
                                                word1Index += 1
                                            else:
                                                word1Index += tilesCol
                                            char1Index += 1
                                        elif word1Index > word2Index:
                                            if var2Dir == "h":
                                                word2Index += 1
                                            else:
                                                word2Index += tilesCol
                                            char2Index += 1
                                        else:
                                            isNeighbor = True
                                            if word1[char1Index] == word2[char2Index]:
                                                acceptedWords.append(word2)
                                            break
                                if isNeighbor and len(acceptedWords) == 0:
                                    inconsistentVars.append((var1, word1))
                    if len(inconsistentVars) > 0:
                        arcChange = True
                    for pair in inconsistentVars:
                        var1 = pair[0]
                        word1 = pair[1]
                        if len(domains[var1]) > 0 and word1 in domains[var1]:
                            domains[var1].remove(word1)

                usedWords.append(value)
                usedVariables.append(variable)
                solution.append([variable, domains[variable].index(value), copy.deepcopy(domains)])
                localSolutions.append(localSolution)
                localDomains.append(copy.deepcopy(domains))
                localSolution = copy.deepcopy(domains)
                variableIndex += 1
            else:
                if len(usedWords) > 0:
                    value = usedWords.pop()
                    variable: str = usedVariables.pop()
                    localSolution = localSolutions.pop()
                solution.append([variable, None, copy.deepcopy(domains)])
                if shouldBacktrack:
                    localDomains.pop()
                if len(localDomains) > 0:
                    domains = localDomains.pop()
                else:
                    domains = copy.deepcopy(fullDomain)
                    localSolution = copy.deepcopy(fullDomain)
                if len(localSolution) > 0:
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
