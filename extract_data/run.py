lines = """Conducts investigations to collect valid and reliable primary and secondary data and information: Outstanding
Selects and processes appropriate qualitative and quantitative data and information using a range of appropriate media: Outstanding
Analyses and evaluates primary and secondary data and information: Outstanding
Communicates scientific understanding using suitable language and terminology for a specific audience or purpose: Outstanding
Describes and analyses evidence for the properties of light and evaluates the implications of this evidence for modern theories of physics in the contemporary world: Outstanding"""

fmt = "{}\t{}"
for line in lines.split("\n"):
    var = line.split(": ")
    print(fmt.format(var[0], var[1]))