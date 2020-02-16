from model import CommandType, CommandParseResult

def processInput(input):
    matchingCommands = [member for name, member in CommandType.__members__.items() if input.startswith(member.value)]

    if len(matchingCommands) == 0:
        return CommandParseResult(CommandType.UNRECOGNIZED, input)

    return CommandParseResult(matchingCommands[0], input[len(matchingCommands[0].value[0]):].strip())