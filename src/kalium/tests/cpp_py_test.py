import ctypes

lib = ctypes.CDLL('src/kalium/tests/test.dll')

lib.add.argtypes = [ctypes.c_int, ctypes.c_int]
lib.add.restype = ctypes.c_int

# Call the C++ function from Python
result = lib.add(5, 3)
print("Result from C++ function:", result)

lib.strink.argtypes = [ctypes.c_char_p]
lib.strink.restype = ctypes.c_char_p

input_string = b"Hello! "
result2 = lib.strink(input_string.encode('utf-8'))  
print("Doubled string from C++ function:", result2.decode('utf-8'))  # Decode back to string

# lib.free_string(result2)


# lib.double_string.argtypes = [ctypes.c_char_p]
# lib.double_string.restype = ctypes.c_char_p

# lib.free_string.argtypes = [ctypes.c_char_p]

# input_string = "Hello! "
# result2 = lib.double_string(input_string.encode('utf-8'))  
# print("Doubled string from C++ function:", result2.decode('utf-8'))  # Decode back to string

# lib.free_string(result2)