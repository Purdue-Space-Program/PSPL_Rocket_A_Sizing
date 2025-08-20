import numpy as np

############# uhhhhhhh
x = np.array([[(1,2), (1,2)], [(1,2), (1,2)]])
print(x)

x = np.array([[[1,2], [1,2,3]], [[1,2], [1,2,3]]])
print(x)

# ########### check size of element in ndarray
# x = np.array(3.14)
# # print(x, x.dtype)
# # print(x.size)

# # print(len("string"))
# # print(len(["string1","string2"]))
# # print(type("string"))
# # print(type(["string1","string2"]))

# x = np.array(["string1","string2"])
# # print(x.size)

# def FindNumberOfSubElements(unknown_variable):
#     num_sub_elements = 0
    
#     # check for case when sub_element(s) are a string
#     if isinstance(unknown_variable, str):
#         num_sub_elements = 1  
    
#     # check for case when sub_elements are in an ndarray
#     elif hasattr(unknown_variable, 'dtype'):
#         num_sub_elements = unknown_variable.size
    
#     else:
#          num_sub_elements = len(unknown_variable)
#     return num_sub_elements

# for test in [["string1","string2"], np.array(["string1","string2"]), "string"]:
#     print(f"{test} = {FindNumberOfSubElements(test)}")


