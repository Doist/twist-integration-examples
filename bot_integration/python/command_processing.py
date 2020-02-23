from model import ParseResult, CommandType


def processInput(input):
    matchingCommands = [
        member
        for name, member in CommandType.__members__.items()
        if input.startswith(member.value)
    ]

    if len(matchingCommands) == 0:
        return ParseResult(CommandType.UNRECOGNIZED, input)

    commandLength = len(matchingCommands[0].value[0])

    return ParseResult(matchingCommands[0], input[commandLength:].strip())
