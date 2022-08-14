# import pysd
# model = pysd.read_vensim("./models/Teacup/teacup.mdl")

# # for component in model.components:
# #     print(component)
# #     print(model.components.__getattribute__(component))

# print(model._stateful_elements)
# sub_dict = getattr(model.components,"teacup_temperature", {})
# print(sub_dict)
import sys
sys.implementation.name

print(sys.implementation.version)